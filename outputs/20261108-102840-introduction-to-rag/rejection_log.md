# Rejection Log — Introduction to RAG

- Run: `20261108-102840-introduction-to-rag`
- Final status: **SHIPPED** (attempt 2 of 2; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): off
- Rules from memory used in this run: 6

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator | 15/18 | REJECTED | PLAIN_LANGUAGE, ACRONYMS, ANALOGY |
| 2 | reviser | 18/18 | PASS | - |

## Attempt 1 — REJECTED

**How this attempt was produced / what changed:**

- First draft written from the plan with 6 learned rule(s) from memory

**What failed and why:**

### PLAIN_LANGUAGE (beginner-friendly language, llm check)
- **Why:** The sentence uses passive voice and does not speak directly to the learner with "you", making it harder for a beginner to understand.
- **Evidence:** The text it read during learning is called training data.
- **Fix requested:** Rewrite to active voice and address the learner, e.g., 'You can think of the text the LLM read during learning as its training data.'

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: XYZ (never expanded or explained)
- **Evidence:** XYZ (never expanded or explained)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### ANALOGY (teaches by example, llm check)
- **Why:** No analogy such as an open‑book exam, library, kirana shop owner checking a register, or railway enquiry counter is provided, nor is any analogy mapped to the retrieval and generation steps of RAG.
- **Evidence:** MISSING: everyday analogy from life in India mapping retrieval and generation.
- **Fix requested:** Add an analogy, for example: 'RAG is like an open‑book exam: first you look up the relevant page in a book (retrieval), then you write your answer using that page (generation).'


## Attempt 2 — PASSED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: PLAIN_LANGUAGE, ACRONYMS, ANALOGY
- [PLAIN_LANGUAGE] Changed passive sentences in "Before We Start" to active voice addressing the learner: "You can think of the text the LLM read during learning as its training data.", "We call this date the knowledge cutoff.", "We call this hallucination."
- [ACRONYMS] Expanded the placeholder acronym XYZ at first use in the example question to "XYZ (Example Scholarship)".
- [ANALOGY] Added a new subsection "An Analogy: Open-Book Exam" under "What Is RAG?" that maps retrieval to finding the right page and generation to writing the answer.

**Checks fixed vs previous attempt:** ACRONYMS, ANALOGY, PLAIN_LANGUAGE  
**Checks newly broken:** none

All checks passed.

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
| JARGON | clear, no unexplained jargon | llm | PASS |
| ANALOGY | teaches by example | llm | PASS |
| WORKED_EXAMPLE | teaches by example | llm | PASS |
| ACCURACY | accurate & grounded | llm | PASS |
| GROUNDED_DEFINITION | accurate & grounded | llm | PASS |
| NO_OVERCLAIM | accurate & grounded | llm | PASS |
| COVERAGE | covers the key points | llm | PASS |
| QUIZ | covers the key points | code | PASS |
