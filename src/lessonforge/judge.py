"""LLM-as-judge for the checks that need judgement.

Design choices
- Checks are judged in small groups (grounding / pedagogy) so each call has a focused job.
- Every verdict must carry evidence: an exact quote from the lesson or "MISSING: ...".
- Quotes are verified against the lesson. A FAIL whose quote is not in the lesson is treated as a judge
  hallucination: that group is re-judged once. This stops the judge from rejecting good lessons for
  invented reasons, while keeping its ability to catch real errors.
- Fail-closed: a check the judge never answers counts as FAIL, so a broken judge cannot ship a lesson.
- Optional majority vote (judge_votes > 1) for extra stability.
"""
from __future__ import annotations

import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from .config import Settings, render_prompt


def _norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[*_`#>\"“”‘’']", "", s)
    return re.sub(r"\s+", " ", s).strip()


def evidence_in_lesson(evidence: str, lesson: str) -> bool:
    ev = _norm(evidence)
    if not ev or ev.startswith("missing"):
        return True
    body = _norm(lesson)
    if ev in body:
        return True
    # tolerate ellipses / small edits: every substantial fragment must be present
    parts = [p.strip() for p in re.split(r"\.\.\.|…", ev) if len(p.strip()) >= 12]
    if parts and all(p in body for p in parts):
        return True
    return len(ev) > 40 and ev[:40] in body


def _format_checks(checks: list[dict]) -> str:
    return "\n".join(f"- {c['id']} ({c['dimension']}): {' '.join(c['criterion'].split())}" for c in checks)


def _one_pass(llm, settings: Settings, lesson: str, reference: str, checks: list[dict],
              tag: str = "") -> dict[str, dict]:
    prompt = render_prompt(settings, "judge", audience=settings.audience, reference=reference,
                           lesson=lesson, checks=_format_checks(checks))
    if tag:  # makes each vote / re-judge a distinct request, so gateways cannot serve a cached verdict
        prompt += f"\n\n(Independent review {tag}.)"
    jcfg = settings.raw["judge"]
    try:
        data = llm.chat_json("judge", prompt, temperature=jcfg["temperature"], max_tokens=jcfg["max_tokens"])
    except Exception as exc:
        # An unreadable or failed judge must never crash the run. Returning no verdicts makes the caller
        # re-judge once and then fail these checks closed, so nothing ships on a broken judgement.
        kind = "unreadable reply" if "JSON" in str(exc) else "call failed"
        print(f"   [judge] {kind} ({str(exc)[:120]}); these checks will be re-judged, then fail closed",
              flush=True)
        return {}
    out = {}
    for r in data.get("results", []):
        cid = str(r.get("id", "")).strip().upper()
        if cid:
            out[cid] = r
    return out


def judge_group(llm, settings: Settings, lesson: str, reference: str, checks: list[dict],
                vote: int = 0) -> list[dict]:
    raw = _one_pass(llm, settings, lesson, reference, checks, tag=f"#{vote + 1}" if vote else "")
    bad_quote = [c["id"] for c in checks
                 if c["id"] in raw and str(raw[c["id"]].get("verdict", "")).upper() == "FAIL"
                 and not evidence_in_lesson(str(raw[c["id"]].get("evidence", "")), lesson)]
    missing = [c["id"] for c in checks if c["id"] not in raw]
    rejudged = False
    if bad_quote or missing:
        retry = _one_pass(llm, settings, lesson, reference, checks, tag=f"#{vote + 1}-recheck")
        for cid in set(bad_quote) | set(missing):
            if cid in retry:
                raw[cid] = retry[cid]
        rejudged = True

    results = []
    for c in checks:
        r = raw.get(c["id"])
        if r is None:
            results.append({"id": c["id"], "dimension": c["dimension"], "type": "llm", "passed": False,
                            "reason": "Judge returned no verdict (fail-closed).", "evidence": "", "fix": "",
                            "evidence_verified": False, "rejudged": rejudged})
            continue
        passed = str(r.get("verdict", "")).strip().upper() == "PASS"
        ev = str(r.get("evidence", "")).strip()
        results.append({
            "id": c["id"], "dimension": c["dimension"], "type": "llm", "passed": passed,
            "reason": str(r.get("reason", "")).strip(), "evidence": ev,
            "fix": "" if passed else str(r.get("fix", "")).strip(),
            "evidence_verified": evidence_in_lesson(ev, lesson), "rejudged": rejudged,
        })
    return results


def judge(llm, settings: Settings, lesson: str, reference: str, checks: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for c in checks:
        groups[c.get("group", "general")].append(c)
    votes = max(1, int(settings.raw["loop"].get("judge_votes", 1)))

    jobs = [(name, v) for name in groups for v in range(votes)]
    run = lambda job: judge_group(llm, settings, lesson, reference, groups[job[0]], vote=job[1])
    if settings.raw["judge"].get("parallel", True) and len(jobs) > 1:
        # groups are independent, so judge them at the same time (the slowest call sets the pace)
        with ThreadPoolExecutor(max_workers=min(4, len(jobs))) as pool:
            outputs = list(pool.map(run, jobs))
    else:
        outputs = [run(j) for j in jobs]
    by_group: dict[str, list[list[dict]]] = defaultdict(list)
    for (name, _), out in zip(jobs, outputs):
        by_group[name].append(out)

    final: list[dict] = []
    for name, group_checks in groups.items():
        rounds = by_group[name]
        for i, c in enumerate(group_checks):
            ballots = [r[i] for r in rounds]
            n_pass = sum(b["passed"] for b in ballots)
            passed = n_pass * 2 > len(ballots)
            pick = next(b for b in ballots if b["passed"] == passed)
            pick = dict(pick, votes=f"{n_pass}/{len(ballots)} pass")
            final.append(pick)
    return final
