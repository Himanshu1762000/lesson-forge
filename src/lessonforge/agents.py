"""The worker agents: planner, generator, reviser, saboteur (demo only) and coach (self-evolution)."""
from __future__ import annotations

import json
import re

from .config import Settings, render_prompt


def clean_lesson(text: str) -> str:
    """Strip code fences / chatter around a markdown lesson."""
    text = text.strip()
    fence = re.match(r"^```(?:markdown|md)?\s*\n(.*)\n```\s*$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    m = re.search(r"^# \S", text, re.MULTILINE)
    if m and m.start() > 0:
        text = text[m.start():]
    return text.strip() + "\n"


# ---------------------------------------------------------------- reference sheet

def draft_reference(llm, settings: Settings, topic: str) -> str:
    """For topics without a curated sheet: draft one. The run is then flagged 'grounding: unverified'."""
    prompt = (
        f"Write a factual reference sheet for teaching '{topic}' to beginners. Use the format:\n"
        "## Core facts (F1, F2, ... one fact per line)\n## Must-cover points (K1..K7)\n"
        "## Known misconceptions (M1..M5)\nOnly include facts you are certain of."
    )
    return llm.chat("planner", prompt, temperature=0.1, max_tokens=4000)


# ---------------------------------------------------------------- generation side

def plan_lesson(llm, settings: Settings, topic: str, reference: str, guidelines: str) -> dict:
    g = settings.raw["generation"]
    prompt = render_prompt(settings, "planner", topic=topic, audience=settings.audience,
                           reference=reference, guidelines=guidelines)
    return llm.chat_json("planner", prompt, temperature=g["planner_temperature"], max_tokens=g["max_tokens"])


def generate_lesson(llm, settings: Settings, topic: str, reference: str, plan: dict, guidelines: str) -> str:
    g = settings.raw["generation"]
    prompt = render_prompt(settings, "generator", topic=topic, audience=settings.audience,
                           plan=json.dumps(plan, indent=2, ensure_ascii=False),
                           reference=reference, guidelines=guidelines)
    return clean_lesson(llm.chat("generator", prompt, temperature=g["generator_temperature"],
                                 max_tokens=g["max_tokens"]))


def _fmt_failures(results: list[dict]) -> str:
    out = []
    for r in results:
        if r["passed"]:
            continue
        out.append(f"- [{r['id']}] ({r['dimension']})\n  why it failed: {r['reason']}\n"
                   f"  evidence: {r.get('evidence') or '-'}\n  how to fix: {r.get('fix') or '-'}")
    return "\n".join(out)


def revise_lesson(llm, settings: Settings, topic: str, reference: str, lesson: str,
                  results: list[dict], guidelines: str) -> tuple[str, list[str]]:
    g = settings.raw["generation"]
    passing = ", ".join(r["id"] for r in results if r["passed"]) or "(none)"
    prompt = render_prompt(settings, "reviser", topic=topic, audience=settings.audience, reference=reference,
                           guidelines=guidelines, lesson=lesson, failures=_fmt_failures(results),
                           passing=passing)
    text = llm.chat("reviser", prompt, temperature=g["reviser_temperature"], max_tokens=g["max_tokens"])
    body, _, log = text.partition("===CHANGELOG===")
    changelog = [l.strip()[1:].strip() for l in log.splitlines() if l.strip().startswith(("-", "*"))]
    if not changelog:
        changelog = ["(reviser gave no changelog)"]
    return clean_lesson(body), changelog


# ---------------------------------------------------------------- saboteur (demo of the evaluator)

INJECTED_ERRORS = [
    {
        "text": ("In fact, RAG works by retraining the LLM on your documents every time you ask a question. "
                 "So the model permanently memorises them and RAG answers are always 100% correct."),
        "should_trigger": ["ACCURACY", "NO_OVERCLAIM"],
        "why": "Misconceptions M1 (RAG retrains the model) and M2 (always correct).",
    },
    {
        "text": ("Under the hood, the retriever runs ANN search with cosine similarity over dense vectors "
                 "stored in an HNSW index."),
        "should_trigger": ["JARGON", "ACRONYMS", "AVOID_WORDS"],
        "why": "Unexplained jargon, unexpanded acronyms (ANN, HNSW) and an idiom ('under the hood').",
    },
]


def sabotage(lesson: str) -> tuple[str, list[str]]:
    """Deterministically plant known errors into the 'How does it work' section."""
    block = "\n\n" + "\n\n".join(e["text"] for e in INJECTED_ERRORS) + "\n"
    m = re.search(r"^## .*how.*$", lesson, re.IGNORECASE | re.MULTILINE)
    if m:
        para_end = lesson.find("\n\n", m.end() + 1)
        para_end = len(lesson) if para_end == -1 else para_end
        lesson = lesson[:para_end] + block + lesson[para_end:]
    else:
        lesson = lesson + block
    log = [f"[SABOTEUR] injected: \"{e['text']}\" -> expected to fail {', '.join(e['should_trigger'])} ({e['why']})"
           for e in INJECTED_ERRORS]
    return lesson, log


# ---------------------------------------------------------------- coach (self-evolution)

def coach_rule(llm, settings: Settings, check: dict, current_rule: str, samples: list[dict]) -> dict:
    sample_txt = "\n".join(f"- reason: {s['reason']} | evidence: {s['evidence']}" for s in samples) or "-"
    prompt = render_prompt(settings, "coach", check_id=check["id"], description=check["description"],
                           criterion=" ".join(check.get("criterion", check["description"]).split()),
                           current_rule=current_rule or "(none)", samples=sample_txt)
    data = llm.chat_json("coach", prompt, temperature=0.2, max_tokens=2000)
    words = data.get("avoid_words") or []
    return {"guideline": str(data.get("guideline", "")).strip(),
            "avoid_words": [w for w in words if isinstance(w, str) and 0 < len(w) <= 40][:10]}
