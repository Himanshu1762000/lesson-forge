# Rejection Log — Introduction to RAG

- Run: `20261108-100011-introduction-to-rag`
- Final status: **SHIPPED** (attempt 2 of 2; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): off
- Rules from memory used in this run: 3

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator | 12/16 | REJECTED | LENGTH, ACRONYMS, JARGON, ANALOGY |
| 2 | reviser | 16/16 | PASS | - |

## Attempt 1 — REJECTED

**How this attempt was produced / what changed:**

- First draft written from the plan with 3 learned rule(s) from memory

**What failed and why:**

### LENGTH (beginner-friendly language, code check)
- **Why:** 833 words (allowed 900-2600).
- **Evidence:** 833
- **Fix requested:** Add depth to thin sections.

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: LLM (full form 'large language model' not given near first use)
- **Evidence:** LLM (full form 'large language model' not given near first use)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** Technical terms (LLM, RAG, retrieve, augment, generate, model) appear in the "What You Will Learn" list before any explanation in the body. The criterion requires every technical term to be explained at or before its first use, including in that list.
- **Evidence:** What an LLM is and its limits.
- **Fix requested:** Either add simple explanations for each term in the "What You Will Learn" list, or move the list after the "Before We Start" section where the terms are defined.

### ANALOGY (teaches by example, llm check)
- **Why:** The lesson contains no everyday analogy from life in India (e.g., open-book exam, kirana shop register, railway enquiry) that explains RAG and maps its parts to retrieval and generation.
- **Evidence:** MISSING: any analogy mapping RAG to a familiar Indian scenario.
- **Fix requested:** Insert an analogy such as an open-book exam: the student (LLM) first finds the relevant page (retrieval), then writes the answer using that page (generation). Explicitly label which part is retrieval and which is generation.


## Attempt 2 — PASSED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: LENGTH, ACRONYMS, JARGON, ANALOGY
- [LENGTH] Added an analogy section (~90 words) and expanded the "What You Will Learn" bullets with explanations (~60 words) to bring total word count above 900.
- [ACRONYMS] Expanded "LLM" to "Large Language Model" and "RAG" to "Retrieval-Augmented Generation" at their first use in the "What You Will Learn" list.
- [JARGON] Added simple explanations for each technical term (retrieve, augment, generate, etc.) directly in the "What You Will Learn" bullets so they are defined at first appearance.
- [ANALOGY] Inserted a new section "An Everyday Analogy: Open-Book Exam" after "What Is RAG?" that maps retrieval to finding a textbook page and generation to writing the answer, using a familiar Indian exam scenario.

**Checks fixed vs previous attempt:** ACRONYMS, ANALOGY, JARGON, LENGTH  
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
| JARGON | clear, no unexplained jargon | llm | PASS |
| ANALOGY | teaches by example | llm | PASS |
| WORKED_EXAMPLE | teaches by example | llm | PASS |
| ACCURACY | accurate & grounded | llm | PASS |
| GROUNDED_DEFINITION | accurate & grounded | llm | PASS |
| NO_OVERCLAIM | accurate & grounded | llm | PASS |
| COVERAGE | covers the key points | llm | PASS |
| QUIZ | covers the key points | code | PASS |

## What the system learned from this run (saved to memory)

- New rule v1 for ACRONYMS: Before or immediately after the first occurrence of any acronym, insert its full expanded form in parentheses.
- New rule v1 for ANALOGY: Include one Indian everyday analogy (open‑book exam, kirana shop register, railway enquiry counter) explaining RAG, and label the analogy’s part as retrieval and the other as generation.
