"""Writes every artefact of a run: attempts, evaluations, final lesson, rejection log, summary."""
from __future__ import annotations

import json
from pathlib import Path


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_attempt(run_dir: Path, record: dict, lesson: str) -> None:
    n = record["attempt"]
    (run_dir / "attempts").mkdir(parents=True, exist_ok=True)
    (run_dir / "attempts" / f"attempt_{n}.md").write_text(lesson, encoding="utf-8")
    write_json(run_dir / "attempts" / f"attempt_{n}_evaluation.json", record)


def _scorecard(results: list[dict]) -> str:
    rows = ["| Check | Dimension | Type | Result |", "|---|---|---|---|"]
    for r in results:
        rows.append(f"| {r['id']} | {r['dimension']} | {r['type']} | {'PASS' if r['passed'] else '**FAIL**'} |")
    return "\n".join(rows)


def rejection_log_md(state: dict) -> str:
    hist = state["history"]
    final = state["final"]
    out = [
        f"# Rejection Log — {state['topic']}",
        "",
        f"- Run: `{state['run_id']}`",
        f"- Final status: **{final['status']}** (attempt {final['attempt']} of {len(hist)}; max retries {state['max_retries']})",
        f"- Grounding: {state.get('grounding', 'verified')}",
        f"- Error injection (demo mode): {'ON' if state.get('inject_error') else 'off'}",
        f"- Rules from memory used in this run: {state.get('n_guidelines', 0)}",
        "",
        "## Attempt overview",
        "",
        "| Attempt | Produced by | Checks passed | Verdict | Failed checks |",
        "|---|---|---|---|---|",
    ]
    for h in hist:
        out.append(f"| {h['attempt']} | {h['source']} | {h['n_passed']}/{h['n_total']} | "
                   f"{'PASS' if h['passed'] else 'REJECTED'} | {', '.join(h['failed']) or '-'} |")

    for i, h in enumerate(hist):
        out += ["", f"## Attempt {h['attempt']} — {'PASSED' if h['passed'] else 'REJECTED'}", ""]
        if h.get("changelog"):
            out += ["**How this attempt was produced / what changed:**", ""]
            out += [f"- {c}" for c in h["changelog"]] + [""]
        if i > 0:
            out += [f"**Checks fixed vs previous attempt:** {', '.join(h.get('fixed', [])) or 'none'}  ",
                    f"**Checks newly broken:** {', '.join(h.get('broken', [])) or 'none'}", ""]
        fails = [r for r in h["results"] if not r["passed"]]
        if not fails:
            out.append("All checks passed.")
            continue
        out += ["**What failed and why:**", ""]
        for r in fails:
            out += [f"### {r['id']} ({r['dimension']}, {r['type']} check)",
                    f"- **Why:** {r['reason']}",
                    f"- **Evidence:** {r.get('evidence') or '-'}",
                    f"- **Fix requested:** {r.get('fix') or '-'}", ""]

    out += ["", "## Final scorecard", "", _scorecard(final["results"])]
    if state.get("learning"):
        out += ["", "## What the system learned from this run (saved to memory)", ""]
        out += [f"- {x}" for x in state["learning"]] or ["- nothing new"]
    return "\n".join(out) + "\n"


def write_final(run_dir: Path, state: dict) -> None:
    final = state["final"]
    header = ""
    if final["status"] != "SHIPPED":
        header = ("> **NOT SHIPPED - needs human review.** The lesson did not clear every check within the retry "
                  f"budget. Failing checks: {', '.join(final['failed'])}. This is the best attempt.\n\n")
    (run_dir / "lesson.md").write_text(header + final["lesson"], encoding="utf-8")
    (run_dir / "rejection_log.md").write_text(rejection_log_md(state), encoding="utf-8")
    write_json(run_dir / "rejection_log.json", {
        "run_id": state["run_id"], "topic": state["topic"], "status": final["status"],
        "final_attempt": final["attempt"], "attempts": state["history"], "learning": state.get("learning", []),
    })
