# Evaluator demo: a lesson with planted mistakes

`bad_lesson.md` is the lesson that **shipped** in run `20261108-102840` (18/18 checks passed), with the
mistakes below planted by `make_bad_lesson.py`. Every other part of the lesson is unchanged, so every
failure comes from a planted mistake.

```bash
lessonforge evaluate samples/bad_lesson.md          # -> REJECT, 8/18 passed
```

| # | Planted mistake | Caught by (real result, `bad_lesson_evaluation.json`) |
|---|---|---|
| 1 | Wrong full form: "Retrieval-**Automated** Generation" (misconception M7) | GROUNDED_DEFINITION, ACCURACY, COVERAGE (K2), ACRONYMS (correct full form never given) |
| 2 | "RAG **retrains the model** … every night, so its answers are **always 100% correct**" (M1 + M2) | ACCURACY, NO_OVERCLAIM |
| 3 | "**In a nutshell**, the retriever uses cosine similarity over an **HNSW** index." | AVOID_WORDS (idiom), ACRONYMS (HNSW) |
| 4 | A 40-word sentence: "Notwithstanding the aforementioned considerations …" | SENTENCE_LENGTH, AVOID_WORDS, PLAIN_LANGUAGE, FLOW |
| 5 | All quiz answers removed | QUIZ |

**What it missed:** the LLM's JARGON check did not flag "cosine similarity" in mistake 3. The same sentence
was still caught by two deterministic checks, so the lesson could not ship. This is the reason the design
pairs every LLM check with a code backstop wherever possible.
