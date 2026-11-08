"""The agentic loop as a LangGraph state machine.

    load_memory -> plan -> generate -> [sabotage] -> evaluate --pass--------------> finalize -> learn -> END
                                                      |  ^                              ^
                                                      |  '--- revise <-- fail, retries left
                                                      '-- fail, retries used up --------'

The router, not a model, decides whether to ship: ALL rubric checks must pass. The loop always ends
because `revise` can only run max_retries times.
"""
from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from . import agents, report
from .config import Settings, find_reference, slugify
from .evaluator import evaluate
from .memory import Memory, criterion_hashes, now


class LoopState(TypedDict, total=False):
    topic: str
    run_id: str
    run_dir: str
    inject_error: bool
    max_retries: int
    learn: bool
    reference: str
    grounding: str
    guidelines: str
    n_guidelines: int
    plan: dict
    attempt: int
    lesson: str
    source: str
    changelog: list
    history: list
    final: dict
    learning: list


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def build_graph(llm, settings: Settings, memory: Memory):
    """Nodes close over the shared llm/settings/memory so they stay pure functions of state."""

    def load_memory(state: LoopState) -> dict:
        topic = state["topic"]
        ref_path = find_reference(settings, topic)
        if ref_path and ref_path.exists():
            reference, grounding = ref_path.read_text(encoding="utf-8"), f"verified ({ref_path.name})"
        else:
            log("No curated reference sheet for this topic: drafting one (run will be marked unverified).")
            reference = agents.draft_reference(llm, settings, topic)
            draft = settings.path(f"knowledge/{slugify(topic)}.draft.md")
            draft.parent.mkdir(parents=True, exist_ok=True)
            draft.write_text(reference, encoding="utf-8")
            grounding = f"UNVERIFIED (model-drafted sheet saved to {draft.name}; a human should check it)"
        n_rules = len(memory.data["guidelines"]) + len(memory.data["human_feedback"][-10:])
        log(f"Memory: {len(memory.data['runs'])} past run(s), {n_rules} learned rule(s), "
            f"{len(memory.avoid_words)} learned avoid-word(s). Grounding: {grounding}")
        return {"reference": reference, "grounding": grounding, "guidelines": memory.guidelines_text(criterion_hashes(settings.rubric)),
                "n_guidelines": n_rules, "history": [], "attempt": 0, "changelog": []}

    def plan(state: LoopState) -> dict:
        log("Planner: designing the lesson outline...")
        p = agents.plan_lesson(llm, settings, state["topic"], state["reference"], state["guidelines"])
        report.write_json(Path(state["run_dir"]) / "plan.json", p)
        log(f"Planner: {len(p.get('sections', []))} sections, analogy = {str(p.get('analogy', {}).get('story', ''))[:70]!r}")
        return {"plan": p}

    def generate(state: LoopState) -> dict:
        log("Generator: writing attempt 1...")
        lesson = agents.generate_lesson(llm, settings, state["topic"], state["reference"], state["plan"],
                                        state["guidelines"])
        return {"lesson": lesson, "attempt": 1, "source": "generator",
                "changelog": ["First draft written from the plan" +
                              (f" with {state['n_guidelines']} learned rule(s) from memory" if state["n_guidelines"] else "")]}

    def sabotage(state: LoopState) -> dict:
        lesson, notes = agents.sabotage(state["lesson"])
        log("Saboteur (demo mode): planted 2 deliberate errors in the draft.")
        return {"lesson": lesson, "source": "generator + saboteur", "changelog": state["changelog"] + notes}

    def evaluate_node(state: LoopState) -> dict:
        n = state["attempt"]
        log(f"Evaluator: judging attempt {n} against {len(settings.rubric['checks'])} pass/fail checks...")
        t0 = time.time()
        ev = evaluate(llm, settings, state["lesson"], state["reference"], memory.avoid_words)
        history = list(state["history"])
        prev = history[-1] if history else None
        record = {
            "attempt": n, "source": state["source"], "changelog": state["changelog"],
            "passed": ev["passed"], "n_passed": ev["n_passed"], "n_total": ev["n_total"],
            "failed": ev["failed"], "results": ev["results"], "seconds": round(time.time() - t0, 1),
            "fixed": sorted(set(prev["failed"]) - set(ev["failed"])) if prev else [],
            "broken": sorted(set(ev["failed"]) - set(prev["failed"])) if prev else [],
        }
        history.append(record)
        report.write_attempt(Path(state["run_dir"]), record, state["lesson"])
        for r in ev["results"]:
            log(f"   {'PASS' if r['passed'] else 'FAIL'}  {r['id']:<20} {'' if r['passed'] else r['reason'][:90]}")
        log(f"Evaluator: {ev['n_passed']}/{ev['n_total']} passed -> {'SHIP' if ev['passed'] else 'REJECT'}")
        return {"history": history}

    def route(state: LoopState) -> str:
        last = state["history"][-1]
        if last["passed"]:
            return "finalize"
        if state["attempt"] > state["max_retries"]:
            log(f"Retry budget used up ({state['max_retries']} retries). Stopping.")
            return "finalize"
        return "revise"

    def revise(state: LoopState) -> dict:
        # Revise from the BEST attempt so far, not blindly from the last one, so a bad revision cannot drift.
        hist = state["history"]
        best = max(hist, key=lambda h: (h["n_passed"], h["attempt"]))
        base_lesson = (Path(state["run_dir"]) / "attempts" / f"attempt_{best['attempt']}.md").read_text(encoding="utf-8")
        n = state["attempt"] + 1
        log(f"Reviser: fixing {len(best['failed'])} failed check(s) from attempt {best['attempt']} -> attempt {n}...")
        lesson, changelog = agents.revise_lesson(llm, settings, state["topic"], state["reference"], base_lesson,
                                                 best["results"], state["guidelines"])
        changelog = [f"Revised from attempt {best['attempt']} to fix: {', '.join(best['failed'])}"] + changelog
        return {"lesson": lesson, "attempt": n, "source": "reviser", "changelog": changelog}

    def finalize(state: LoopState) -> dict:
        hist = state["history"]
        passing = [h for h in hist if h["passed"]]
        chosen = passing[-1] if passing else max(hist, key=lambda h: (h["n_passed"], h["attempt"]))
        lesson = (Path(state["run_dir"]) / "attempts" / f"attempt_{chosen['attempt']}.md").read_text(encoding="utf-8")
        status = "SHIPPED" if chosen["passed"] else "NEEDS_HUMAN_REVIEW"
        final = {"status": status, "attempt": chosen["attempt"], "lesson": lesson,
                 "failed": chosen["failed"], "results": chosen["results"]}
        log(f"Final: {status} (attempt {chosen['attempt']})")
        return {"final": final}

    def learn(state: LoopState) -> dict:
        learning: list[str] = []
        if state.get("learn", True):
            # Sabotaged attempts are artificial: do not let planted errors teach the system false lessons.
            real = [h for h in state["history"] if "saboteur" not in h["source"]]
            crit = criterion_hashes(settings.rubric)
            threshold = int(settings.raw["memory"]["coach_min_failures"])
            checks = {c["id"]: c for c in settings.rubric["checks"]}
            failed_now = {r["id"] for h in real for r in h["results"] if not r["passed"]}
            final = state["final"]

            # Phase 1 (locked): merge this run into the LATEST memory on disk, pick the checks to coach.
            to_coach = []
            with memory.locked():
                for h in real:
                    memory.record_evaluation(state["run_id"], h["attempt"], h["results"], crit)
                memory.add_run({
                    "run_id": state["run_id"], "topic": state["topic"], "finished": now(),
                    "status": final["status"], "attempts": len(state["history"]),
                    "inject_error": bool(state.get("inject_error")),
                    "failed_per_attempt": [h["failed"] for h in state["history"]],
                })
                for cid in sorted(failed_now):
                    st = memory.data["check_stats"][cid]
                    rule = memory.data["guidelines"].get(cid)
                    # write a rule once a check fails repeatedly; sharpen it only if it keeps failing after it
                    if st["fails"] < threshold or (rule and st["fails_since_rule"] < threshold):
                        continue
                    # learn only from failures judged under the CURRENT definition of the check
                    samples = [s for s in st["samples"] if s.get("crit") == crit[cid]]
                    if len(samples) < threshold:
                        continue
                    stale = bool(rule) and rule.get("crit") != crit[cid]
                    to_coach.append((cid, "" if stale else (rule or {}).get("text", ""), samples))

            # Phase 2 (unlocked): ask the coach. It is slow, so other runs are not blocked meanwhile.
            outcomes = []
            for cid, current, samples in to_coach:
                try:
                    outcomes.append((cid, agents.coach_rule(llm, settings, checks[cid], current, samples)))
                except Exception as exc:  # learning must never break a finished run
                    learning.append(f"coach failed for {cid}: {exc}")

            # Phase 3 (locked): store the new rules.
            if outcomes:
                with memory.locked():
                    for cid, out in outcomes:
                        if out["guideline"]:
                            g = memory.set_guideline(cid, out["guideline"], crit=crit[cid])
                            learning.append(f"{'New' if g['version'] == 1 else 'Sharpened'} rule "
                                            f"v{g['version']} for {cid}: {g['text']}")
                        added = memory.add_avoid_words(out["avoid_words"])
                        if added:
                            learning.append(f"Rubric tightened: AVOID_WORDS now also bans {', '.join(added)}")
            for line in learning:
                log(f"Coach: {line}")
            if not learning:
                log("Coach: no check has failed often enough yet to write a new rule.")
        state = {**state, "learning": learning}
        report.write_final(Path(state["run_dir"]), state)
        report.write_json(Path(state["run_dir"]) / "run_summary.json", {
            "run_id": state["run_id"], "topic": state["topic"], "status": state["final"]["status"],
            "final_attempt": state["final"]["attempt"], "attempts": len(state["history"]),
            "grounding": state["grounding"], "learning": learning,
            "llm_calls": getattr(llm, "calls", []),
        })
        return {"learning": learning}

    g = StateGraph(LoopState)
    for name, fn in [("load_memory", load_memory), ("plan", plan), ("generate", generate),
                     ("sabotage", sabotage), ("evaluate", evaluate_node), ("revise", revise),
                     ("finalize", finalize), ("learn", learn)]:
        g.add_node(name, fn)
    g.add_edge(START, "load_memory")
    g.add_edge("load_memory", "plan")
    g.add_edge("plan", "generate")
    g.add_conditional_edges("generate", lambda s: "sabotage" if s.get("inject_error") else "evaluate",
                            {"sabotage": "sabotage", "evaluate": "evaluate"})
    g.add_edge("sabotage", "evaluate")
    g.add_conditional_edges("evaluate", route, {"revise": "revise", "finalize": "finalize"})
    g.add_edge("revise", "evaluate")
    g.add_edge("finalize", "learn")
    g.add_edge("learn", END)
    return g.compile()


def run_loop(llm, settings: Settings, topic: str, *, inject_error: bool = False,
             max_retries: int | None = None, learn: bool = True, out_root: Path | None = None) -> dict[str, Any]:
    memory = Memory.load(settings.path(settings.raw["memory"]["path"]),
                         settings.raw["memory"].get("max_samples_per_check", 6))
    run_id = f"{datetime.now():%Y%m%d-%H%M%S}-{slugify(topic)}" + ("-inject" if inject_error else "")
    run_dir = (out_root or settings.path("outputs")) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    graph = build_graph(llm, settings, memory)
    retries = settings.max_retries if max_retries is None else max_retries
    log(f"Run {run_id}: topic={topic!r}, max_retries={retries}, inject_error={inject_error}")
    state = graph.invoke({"topic": topic, "run_id": run_id, "run_dir": str(run_dir),
                          "inject_error": inject_error, "max_retries": retries, "learn": learn},
                         {"recursion_limit": 50})
    (run_dir.parent / "LATEST.txt").write_text(run_id + "\n", encoding="utf-8")
    return state
