# LessonForge — a self-evaluating lesson generator

An agentic system that **writes a beginner lesson, judges it against a hard pass/fail rubric, and rewrites it
until it is good enough to ship**. It also learns from its own failures across runs.

Built for the *GenAI Engineer – Content Systems* take-home.
Topic: **Introduction to RAG**.
Learner: a 12th-grade graduate from India with limited English and a non-English-medium background.

```
topic -> load memory -> plan -> generate -> evaluate (18 pass/fail checks) --all pass--> ship
                                              ^            | any fail
                                              '-- revise <-'  (max 2 retries, then "needs human review")
                                                                     -> learn: update memory, write new rules
```

- **Stack:** Python + LangGraph. Works with any OpenAI-compatible model (OpenAI, Groq, OpenRouter, Ollama, a local gateway…).
- **Evaluator:** 9 deterministic code checks + 9 LLM-judge checks. The judge must quote evidence, and the quotes are checked against the lesson.
- **Output:** the final lesson, every attempt, and a rejection log: what failed, why, the evidence, what changed, and which checks were fixed or broken.
- **Memory:** `memory/memory.json` keeps failure stats, rules written by the coach, human feedback and learned banned words across runs.

**Final lesson:** [`FINAL_LESSON.md`](FINAL_LESSON.md). The system shipped it in run `20261108-133345`
(attempt 2, 18/18). A human review then made 3 small clarity edits: it rewrote one awkward "vector database"
sentence, defined "model", and turned the bracketed "weights" note into full sentences. The edited version
was checked again with `lessonforge evaluate FINAL_LESSON.md --votes 3` and passed 18/18 by 3-vote majority
(`outputs/final_lesson_evaluation.json`). Evaluator demo: [`samples/README.md`](samples/README.md).

Design reasoning: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) · Build plan: [`docs/PLAN.md`](docs/PLAN.md) · Video script: [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md)

## Setup

```bash
git clone <this repo> && cd lesson-forge
python -m venv .venv
# Windows: .venv\Scripts\activate     macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # then fill in LLM_BASE_URL, LLM_API_KEY, GENERATOR_MODEL, JUDGE_MODEL
```

Any OpenAI-compatible endpoint works. Use a **different** model for `JUDGE_MODEL` if you can.

## Run

```bash
# 1. The full loop, end to end
lessonforge run --topic "Introduction to RAG"

# 2. Demo: plant 2 known errors in the first draft and watch the evaluator catch them
lessonforge run --topic "Introduction to RAG" --inject-error

# 3. Evaluate any lesson file on its own (e.g. the sample with planted mistakes)
lessonforge evaluate samples/bad_lesson.md

# 4. Teach the system: add reviewer feedback (used in every future run)
lessonforge feedback "Use examples from cricket or Indian Railways more often."

# 5. See what the system has learned
lessonforge memory

# 6. Print the LangGraph as a Mermaid diagram
lessonforge graph

# Tests (offline, no API key needed: they use a scripted fake LLM)
pytest
```

`python -m lessonforge ...` works the same way as `lessonforge ...`.

## What a run produces

```
outputs/<run_id>/
├── lesson.md               the final lesson (or the best attempt with a "NOT SHIPPED" banner)
├── rejection_log.md        what failed, why, the evidence, what changed, checks fixed / broken
├── rejection_log.json      the same, machine-readable
├── plan.json               the planner's outline
├── run_summary.json        status, grounding, what was learned, and every LLM call (model, time, tokens)
└── attempts/attempt_N.md + attempt_N_evaluation.json
```

## Repository layout

```
config.yaml            loop, model and audience settings
rubric/rubric.yaml     the 18 pass/fail checks (single source of truth)
knowledge/             grounding reference sheet (facts F1-F14, must-cover K1-K7, misconceptions M1-M7)
prompts/               planner, generator, reviser, judge, coach (editable templates)
src/lessonforge/       graph.py (loop) · evaluator.py · checks.py · judge.py · agents.py · memory.py · report.py · cli.py
samples/bad_lesson.md  a lesson with planted mistakes, for the evaluator demo
tests/                 unit tests for the checks + loop tests with a fake LLM
memory/memory.json     persistent memory (created on the first run)
outputs/               one folder per run
```

## Exit codes

`run` and `evaluate` exit with `0` when the lesson ships and `2` when it is rejected or needs human review,
so they can be used in CI.
