# Rejection Log — Introduction to RAG

- Run: `20261108-124101-introduction-to-rag`
- Final status: **NEEDS_HUMAN_REVIEW** (attempt 3 of 3; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): off
- Rules from memory used in this run: 6

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator | 14/18 | REJECTED | ACRONYMS, DEFINED_BEFORE_USE, JARGON, COVERAGE |
| 2 | reviser | 17/18 | REJECTED | DEFINED_BEFORE_USE |
| 3 | reviser | 17/18 | REJECTED | JARGON |

## Attempt 1 — REJECTED

**How this attempt was produced / what changed:**

- First draft written from the plan with 6 learned rule(s) from memory

**What failed and why:**

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: AI (full form 'artificial intelligence' not given near first use)
- **Evidence:** AI (full form 'artificial intelligence' not given near first use)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 1 term(s) used before being explained.
- **Evidence:** 'chunk' is used before its definition ("...our.  But RAG has limits. The answer is only as good as the chunks retrieved. If the search returns wrong...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'chunk' is used before its definition ("...our.  But RAG has limits. The answer is only as good as the chunks retrieved. If the search returns wrong...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The technical term 'model' is used in the very first sentence but is not explained in simple words at that point. The learner has no CS background, so 'model' needs a plain explanation (e.g., 'a computer program that has learned patterns from data').
- **Evidence:** A large language model (LLM) is an AI model trained on a very large amount of text.
- **Fix requested:** Add a one-sentence explanation of 'model' at first use, for example: 'A model is a computer program that has learned patterns from data.'

### COVERAGE (covers the key points, llm check)
- **Why:** K5 requires teaching that RAG provides fresh/private information, fewer made-up answers, sources, and no retraining needed; the lesson omits the 'fewer made-up answers' aspect.
- **Evidence:** MISSING: K5 - Why RAG matters: fewer made-up answers not taught in main body
- **Fix requested:** Add a statement in the 'Why Does RAG Matter?' section such as: 'RAG reduces the chance of making up answers because the model grounds its response in retrieved documents.'


## Attempt 2 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: ACRONYMS, DEFINED_BEFORE_USE, JARGON, COVERAGE
- [ACRONYMS] Expanded "AI" to "artificial intelligence (AI)" at first use in the "Before We Start" section.
- [JARGON] Added a one-sentence definition of "model" ("A model is a computer program that has learned patterns from data.") at its first use in the "Before We Start" section.
- [DEFINED_BEFORE_USE] Defined "chunk" at its first use in the "Why Does RAG Matter?" section ("A chunk is a small piece of a document, like a paragraph.").
- [COVERAGE] Added a bullet point in "Why Does RAG Matter?" stating: "RAG reduces the chance of making up answers because the model grounds its response in retrieved documents."

**Checks fixed vs previous attempt:** ACRONYMS, COVERAGE, JARGON  
**Checks newly broken:** none

**What failed and why:**

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 1 term(s) used before being explained.
- **Evidence:** 'chunk' is used before its definition ("...our.  But RAG has limits. The answer is only as good as the chunks retrieved. A **chunk** is a small piece...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'chunk' is used before its definition ("...our.  But RAG has limits. The answer is only as good as the chunks retrieved. A **chunk** is a small piece...")


## Attempt 3 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 2 to fix: DEFINED_BEFORE_USE
- [DEFINED_BEFORE_USE] Defined 'chunk' at its first use in the "Why Does RAG Matter?" section by adding "(small pieces of a document)" after "chunks".

**Checks fixed vs previous attempt:** DEFINED_BEFORE_USE  
**Checks newly broken:** JARGON

**What failed and why:**

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The term 'context' is used (as a label in the example) without ever being explained; the lesson never defines that the retrieved chunks constitute the 'context' added to the prompt.
- **Evidence:** > Context: National Scholarship 2024 applications close on 31 October 2024.
- **Fix requested:** Add a simple definition of 'context' before its first use, e.g., explain that the retrieved chunks are called the 'context' and are placed into the prompt.


## Final scorecard

| Check | Dimension | Type | Result |
|---|---|---|---|
| STRUCTURE | coherent teaching flow | code | PASS |
| FLOW | coherent teaching flow | llm | PASS |
| SENTENCE_LENGTH | beginner-friendly language | code | PASS |
| READABILITY | beginner-friendly language | code | PASS |
| AVOID_WORDS | beginner-friendly language | code | PASS |
| PLAIN_LANGUAGE | beginner-friendly language | llm | PASS |
| LENGTH | beginner-friendly language | code | PASS |
| ACRONYMS | clear, no unexplained jargon | code | PASS |
| DEFINED_BEFORE_USE | clear, no unexplained jargon | code | PASS |
| GLOSSARY | clear, no unexplained jargon | code | PASS |
| JARGON | clear, no unexplained jargon | llm | **FAIL** |
| ANALOGY | teaches by example | llm | PASS |
| WORKED_EXAMPLE | teaches by example | llm | PASS |
| ACCURACY | accurate & grounded | llm | PASS |
| GROUNDED_DEFINITION | accurate & grounded | llm | PASS |
| NO_OVERCLAIM | accurate & grounded | llm | PASS |
| COVERAGE | covers the key points | llm | PASS |
| QUIZ | covers the key points | code | PASS |

## What the system learned from this run (saved to memory)

- Sharpened rule v3 for ACRONYMS: At the first occurrence of any acronym, write its complete expanded form directly before the acronym in parentheses, with no other words between them (e.g., 'artificial intelligence (AI)').
- Sharpened rule v2 for DEFINED_BEFORE_USE: When introducing any of the terms embedding model, retraining, vector, chunk, embedding for the first time, place a concise definition in parentheses right after the term, with no other words between the term and the opening parenthesis.
- Sharpened rule v3 for JARGON: When a technical term from the list first appears anywhere in the lesson (heading, body, bullet, or learning‑goal list), insert a plain‑language definition of ≤12 words right after the term, separated by a comma or dash.
