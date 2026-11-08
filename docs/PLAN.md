# Build Plan — LessonForge (Self-Evaluating Lesson Generator)

## 1. What the brief asks for

| Requirement | Where it lives |
|---|---|
| Input a topic, learner starts from zero | `lessonforge run --topic "..."` |
| Generate a standalone beginner lesson (what / why / how) | `planner` + `generator` nodes, `prompts/` |
| Evaluate against hard pass/fail rubric (no partial credit) | `rubric/rubric.yaml`, `checks.py` (code checks), `judge.py` (LLM checks) |
| Regenerate on fail, feed reasons back, max 1–2 retries | `reviser` node + router in `graph.py` (`max_retries: 2`) |
| Output: passing lesson + rejection log | `outputs/<run_id>/lesson.md`, `rejection_log.md/.json` |
| Self-evolving: learn from repeated failures | `coach` node → `memory/memory.json` guidelines + learned avoid-words |
| Memory across runs, learns from feedback + logs | `memory.py`, `lessonforge feedback "..."` |
| Demo: evaluator catches a deliberate error | `--inject-error` flag and `lessonforge evaluate samples/bad_lesson.md` |

## 2. Task breakdown (build order)

1. **Foundations** — config (`config.yaml`, `.env`), model-agnostic LLM client (any OpenAI-compatible endpoint), robust JSON parsing.
2. **Knowledge & rubric** — RAG reference sheet (ground truth + must-cover points + known misconceptions); rubric of 15 binary checks across the 6 dimensions.
3. **Evaluator** — deterministic code checks (structure, sentence length, readability, length, quiz, acronyms, banned words) + LLM judge in two groups (grounding, pedagogy) that must quote evidence; evidence is verified against the lesson text.
4. **Generator side** — planner (outline from reference + memory), generator (full lesson), reviser (fix only failed checks, emit changelog), saboteur (deterministic error injection for the demo).
5. **Loop** — LangGraph state machine: `load_memory → plan → generate → [sabotage] → evaluate → (revise ↺ | finalize) → learn`. Keeps the best attempt; always terminates.
6. **Memory & self-evolution** — per-check failure stats, failure samples, coach-written guidelines (versioned, refined when they stop working), learned avoid-words that tighten the code rubric, human feedback.
7. **Reporting** — every attempt saved, per-attempt evaluation JSON, human-readable rejection log with "what failed / why / what changed / which checks flipped".
8. **Quality** — unit tests for code checks, loop-termination tests with a fake LLM.
9. **Docs & demo** — README (setup/run), ARCHITECTURE (reasoning + trade-offs), video script.

## 3. Folder structure

```
lesson-forge/
├── README.md                 setup & run
├── config.yaml               loop + model + audience settings
├── .env.example              LLM endpoint / keys / model names
├── pyproject.toml            package + `lessonforge` CLI
├── rubric/rubric.yaml        the pass/fail checkpoints (single source of truth)
├── knowledge/                grounding reference sheets per topic
│   └── rag_reference.md
├── prompts/                  every prompt as an editable template
│   ├── planner.md  generator.md  reviser.md
│   ├── judge.md    coach.md
├── src/lessonforge/
│   ├── cli.py                run | evaluate | feedback | memory
│   ├── config.py             load config, rubric, prompts
│   ├── llm.py                OpenAI-compatible client, retries, JSON extraction
│   ├── checks.py             deterministic rubric checks
│   ├── judge.py              LLM-as-judge with evidence verification
│   ├── evaluator.py          runs all checks → verdict
│   ├── agents.py             planner, generator, reviser, saboteur, coach
│   ├── memory.py             persistent memory store
│   ├── graph.py              LangGraph loop
│   └── report.py             lesson + rejection log writers
├── samples/bad_lesson.md     lesson with planted errors (evaluator demo)
├── tests/                    pytest (no network needed)
├── memory/memory.json        created on first run, persists across runs
├── outputs/<run_id>/         lesson.md, attempts/, rejection_log.md, …
└── docs/                     PLAN.md, ARCHITECTURE.md, DEMO_SCRIPT.md
```
