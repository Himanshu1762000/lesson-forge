# Loom video script (15–20 min)

Keep your face visible in the corner the whole time. Before recording, start the model gateway and run
`lessonforge memory` once so you know the current state.

## 1. Intro (1 min)
- Who you are. The task: a lesson generator that judges its own work and decides whether to ship it.
- The learner: a 12th-grade graduate from India, limited English, non-English-medium background.
- The key idea: **the evaluator is the product**. Generation is the easy part.

## 2. Architecture walkthrough (4 min), from `docs/ARCHITECTURE.md`
- Show the Mermaid diagram (`lessonforge graph`). Walk through each node: load_memory, planner, generator,
  evaluator, router, reviser, finalize, learn.
- Open `rubric/rubric.yaml`: 18 hard pass/fail checks across the 6 dimensions. Explain the split: 9 code
  checks and 9 LLM checks, and why.
- Open `knowledge/rag_reference.md`: facts, must-cover points, misconceptions. Explain that this is how
  "accurate" is defined.
- Explain the judge safeguards: quotes are required and verified, fail-closed, a separate judge model.

## 3. End-to-end run (5 min)
- `lessonforge run --topic "Introduction to RAG"`
- While it runs: point out the planner output, the per-check PASS/FAIL lines, the reviser fixing
  specific checks, and the final SHIP decision.
- Open `outputs/<run>/rejection_log.md`: the attempt table, what failed and why, the evidence quotes, the
  changelog, the checks fixed and broken.
- Open `lesson.md`: scroll the final lesson (analogy, worked example, glossary, quiz).

## 4. The evaluator catching a deliberate error (3 min)
- Option A (live loop): `lessonforge run --inject-error`. The saboteur plants
  "RAG retrains the LLM … always 100% correct" and "Under the hood … ANN … HNSW index".
  Show ACCURACY, NO_OVERCLAIM, JARGON, ACRONYMS and AVOID_WORDS failing on attempt 1, with quotes. Then
  show the reviser removing the errors and attempt 2 passing.
- Option B (fast): `lessonforge evaluate samples/bad_lesson.md`. Each planted mistake (listed in
  `samples/README.md`) is caught by a named check.

## 5. Memory & self-evolution (2 min)
- `lessonforge memory`: failure stats per check, the rules the coach wrote (with versions), and learned
  avoid-words.
- Explain the timeline: run 1 failed FLOW, JARGON and READABILITY repeatedly, so the coach wrote rules.
  Run 2 used those rules and passed sooner.
- `lessonforge feedback "..."`: human feedback goes into every future prompt.
- Point out that injected (demo) errors are never learned from.

## 6. Trade-offs and what's next (2 min)
- The all-pass gate versus a weighted score. Curated grounding versus open topics. Cost and latency of
  the judge.
- The run-2 story: the LLM judge missed jargon. I caught it in review and added the deterministic
  DEFINED_BEFORE_USE check. The lesson: wherever a quality rule can be measured, measure it in code.
- Next: calibrate the judge against lessons labelled by humans, add a simulated-learner quiz-taker, and
  produce versions in Indian regional languages.
