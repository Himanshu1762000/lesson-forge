"""Runs the whole rubric against one lesson and returns a single verdict.

Code checks run first. LLM checks always run too (even if a code check failed) so the reviser gets the
full list of problems in one round instead of discovering them one retry at a time.
"""
from __future__ import annotations

from .checks import run_code_check
from .config import Settings
from .judge import judge


def evaluate(llm, settings: Settings, lesson: str, reference: str,
             learned_avoid_words: list[str] | None = None) -> dict:
    checks = settings.rubric["checks"]
    results = [run_code_check(lesson, c, learned_avoid_words) for c in checks if c["type"] == "code"]
    llm_checks = [c for c in checks if c["type"] == "llm"]
    if llm_checks:
        results += judge(llm, settings, lesson, reference, llm_checks)

    order = {c["id"]: i for i, c in enumerate(checks)}
    results.sort(key=lambda r: order.get(r["id"], 999))
    failed = [r["id"] for r in results if not r["passed"]]
    return {
        "passed": not failed,              # hard gate: ALL checks must pass
        "n_passed": len(results) - len(failed),
        "n_total": len(results),
        "failed": failed,
        "results": results,
    }
