"""Command line: run | evaluate | feedback | memory | graph"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import find_reference, load_settings
from .memory import Memory


def _llm(settings):
    from .llm import LLM
    cfg = settings.raw.get("llm", {})
    return LLM(settings.models, timeout=float(cfg.get("timeout_seconds", 180)),
               attempts=int(cfg.get("attempts", 2)))


def cmd_run(args, settings) -> int:
    from .graph import run_loop

    state = run_loop(_llm(settings), settings, args.topic, inject_error=args.inject_error,
                     max_retries=args.max_retries, learn=not args.no_learn)
    run_dir = Path(state["run_dir"])
    print("\n" + "=" * 70)
    print(f"STATUS : {state['final']['status']}  (final attempt {state['final']['attempt']} of {len(state['history'])})")
    print(f"Lesson : {run_dir / 'lesson.md'}")
    print(f"Log    : {run_dir / 'rejection_log.md'}")
    print("=" * 70)
    return 0 if state["final"]["status"] == "SHIPPED" else 2


def cmd_evaluate(args, settings) -> int:
    from .evaluator import evaluate

    lesson = Path(args.file).read_text(encoding="utf-8")
    ref = find_reference(settings, args.topic)
    if not ref:
        print(f"No reference sheet for topic {args.topic!r}.", file=sys.stderr)
        return 1
    memory = Memory.load(settings.path(settings.raw["memory"]["path"]))
    if args.votes:
        settings.raw["loop"]["judge_votes"] = args.votes
    ev = evaluate(_llm(settings), settings, lesson, ref.read_text(encoding="utf-8"), memory.avoid_words)
    for r in ev["results"]:
        votes = f" [{r['votes']}]" if r.get("votes") and not r["votes"].endswith("1 pass") else ""
        print(f"{'PASS' if r['passed'] else 'FAIL'}  {r['id']:<20}{votes} {r['reason']}")
        if not r["passed"] and r.get("evidence"):
            print(f"      evidence: {r['evidence'][:200]}")
    print(f"\n{ev['n_passed']}/{ev['n_total']} checks passed -> {'SHIP' if ev['passed'] else 'REJECT'}")
    if args.json:
        Path(args.json).write_text(json.dumps(ev, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0 if ev["passed"] else 2


def cmd_feedback(args, settings) -> int:
    path = settings.path(settings.raw["memory"]["path"])
    memory = Memory.load(path)
    run_id = args.run or (settings.path("outputs/LATEST.txt").read_text().strip()
                          if settings.path("outputs/LATEST.txt").exists() else None)
    memory.add_feedback(args.text, run_id)
    memory.save()
    print(f"Saved. This note will be given to the planner, generator and reviser in every future run.")
    return 0


def cmd_memory(args, settings) -> int:
    m = Memory.load(settings.path(settings.raw["memory"]["path"])).data
    print(f"Runs: {len(m['runs'])}")
    for r in m["runs"][-10:]:
        print(f"  {r['run_id']}: {r['status']} after {r['attempts']} attempt(s); fails per attempt {r['failed_per_attempt']}")
    print("\nFailure stats (fails / evaluations):")
    for cid, st in sorted(m["check_stats"].items(), key=lambda kv: -kv[1]["fails"]):
        print(f"  {cid:<20} {st['fails']}/{st['evaluations']}")
    print("\nLearned rules:")
    for cid, g in m["guidelines"].items():
        print(f"  [{cid} v{g['version']}] {g['text']}")
    print("\nHuman feedback:")
    for f in m["human_feedback"]:
        print(f"  - {f['text']}")
    print(f"\nLearned avoid-words: {', '.join(m['learned_avoid_words']) or '-'}")
    return 0


def cmd_graph(args, settings) -> int:
    from .graph import build_graph

    class _NoLLM:  # graph structure does not need a model
        pass

    g = build_graph(_NoLLM(), settings, Memory(Path("unused.json")))
    print(g.get_graph().draw_mermaid())
    return 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):  # Windows consoles: never crash on a non-ASCII character
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    p = argparse.ArgumentParser(prog="lessonforge", description="Self-evaluating lesson generator")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="generate -> evaluate -> regenerate a lesson")
    r.add_argument("--topic", default="Introduction to RAG")
    r.add_argument("--inject-error", action="store_true", help="demo: plant known errors in draft 1")
    r.add_argument("--max-retries", type=int, default=None)
    r.add_argument("--no-learn", action="store_true", help="do not update memory")

    e = sub.add_parser("evaluate", help="evaluate an existing lesson file")
    e.add_argument("file")
    e.add_argument("--topic", default="Introduction to RAG")
    e.add_argument("--json", help="also write the full evaluation to this file")
    e.add_argument("--votes", type=int, help="judge each LLM check N times, majority wins (default: config)")

    f = sub.add_parser("feedback", help="add reviewer feedback to memory")
    f.add_argument("text")
    f.add_argument("--run")

    sub.add_parser("memory", help="show what the system has learned")
    sub.add_parser("graph", help="print the LangGraph as a Mermaid diagram")

    args = p.parse_args(argv)
    settings = load_settings()
    return {"run": cmd_run, "evaluate": cmd_evaluate, "feedback": cmd_feedback,
            "memory": cmd_memory, "graph": cmd_graph}[args.cmd](args, settings)


if __name__ == "__main__":
    sys.exit(main())
