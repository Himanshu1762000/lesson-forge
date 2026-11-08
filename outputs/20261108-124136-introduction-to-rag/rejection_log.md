# Rejection Log — Introduction to RAG

- Run: `20261108-124136-introduction-to-rag`
- Final status: **NEEDS_HUMAN_REVIEW** (attempt 2 of 3; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): off
- Rules from memory used in this run: 6

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator | 14/18 | REJECTED | ACRONYMS, DEFINED_BEFORE_USE, JARGON, ANALOGY |
| 2 | reviser | 17/18 | REJECTED | JARGON |
| 3 | reviser | 16/18 | REJECTED | FLOW, JARGON |

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
- **Evidence:** 'chunk' is used before its definition ("...g facts.  **Limitation:** The answer is only as good as the chunks that are retrieved. If the search retur...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'chunk' is used before its definition ("...g facts.  **Limitation:** The answer is only as good as the chunks that are retrieved. If the search retur...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The terms "model" and "vector" are used without prior simple explanation.
- **Evidence:** A large language model (LLM) is an AI model trained on a very large amount of text.; Store the embeddings in a vector database (a searchable store of embeddings).
- **Fix requested:** Add a brief definition for "model" (e.g., a program that learns patterns from data) before its first use, and define "vector" as a list of numbers representing an embedding before mentioning "vector database".

### ANALOGY (teaches by example, llm check)
- **Why:** No everyday Indian analogy (e.g., open-book exam, kirana shop register) is provided to explain the core idea of RAG.
- **Evidence:** MISSING: analogy
- **Fix requested:** Include an analogy such as comparing RAG to an open-book exam where retrieval is looking up the relevant page and generation is writing the answer using that page, and map each part to RAG steps.


## Attempt 2 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: ACRONYMS, DEFINED_BEFORE_USE, JARGON, ANALOGY
- [ACRONYMS] Expanded "AI" to "artificial intelligence (AI)" at first use in the "Before We Start" section.
- [JARGON] Added definition for "model" as "a program that learns patterns from data" at first use in the same sentence.
- [DEFINED_BEFORE_USE] Defined "chunk" as "small pieces of a document" at its first appearance in the "Limitation" section.
- [JARGON] Defined "vector" as "lists of numbers that represent embeddings" when introducing "vector database" in the Preparation section.
- [ANALOGY] Added a new subsection "An Everyday Analogy: Open‑Book Exam" after "What Is RAG?" with retrieval and generation mapped to RAG steps.

**Checks fixed vs previous attempt:** ACRONYMS, ANALOGY, DEFINED_BEFORE_USE  
**Checks newly broken:** none

**What failed and why:**

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The term "context" is used before being explained; its definition appears only in the glossary at the end.
- **Evidence:** The LLM writes the answer from the question plus the retrieved context.
- **Fix requested:** Define "context" at its first use, e.g., add explanation in parentheses: "(the retrieved chunks placed in the prompt)".


## Attempt 3 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 2 to fix: JARGON
- [JARGON] Added definition for "context" at its use in the Generate step: changed "retrieved context." to "retrieved context (the retrieved chunks placed in the prompt)."

**Checks fixed vs previous attempt:** none  
**Checks newly broken:** FLOW

**What failed and why:**

### FLOW (coherent teaching flow, llm check)
- **Why:** The term 'chunks' is used in the 'Why Does RAG Matter?' section before it is defined in the later 'How Does RAG Work?' preparation section.
- **Evidence:** The answer is only as good as the chunks (small pieces of a document) that are retrieved.
- **Fix requested:** Move the definition of 'chunks' earlier, or reorder sections so the preparation (indexing) explanation comes before the 'Why Does RAG Matter?' section.

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** Technical terms 'context window', 'top-k', and 'indexing' appear in the body without any explanation at or before first use.
- **Evidence:** Only a limited amount of text fits in the prompt (the context window).
- **Fix requested:** Explain each term at first use: e.g., 'context window (the maximum amount of text the model can consider at once)', 'top-k (the top few most relevant chunks, typically 3–5)', and 'indexing (organizing the embeddings so they can be searched quickly)'.


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

- Sharpened rule v3 for ACRONYMS: When introducing an acronym for the first time, place its complete expanded form immediately before the acronym in parentheses, with no intervening words (e.g., 'artificial intelligence (AI)'); repeat this definition for each new acronym.
- Sharpened rule v2 for ANALOGY: Insert one Indian everyday analogy (open‑book exam, kirana shop register, railway enquiry counter, or library) describing RAG, and clearly label the analogy component that represents retrieval and the component that represents generation.
- Sharpened rule v2 for DEFINED_BEFORE_USE: At the first mention of each core term—embedding model, retraining, vector, chunk, embedding—insert a brief definition in parentheses right after the term (or as an appositive set off by commas/dashes), e.g., 'vector (a list of numbers representing data)'.
- Sharpened rule v2 for FLOW: Maintain the fixed section order (Problem → What RAG is → Why it matters → How it works → Worked example → Recap) and, for every technical term, define it at its first use in the same sentence before any later use.
- Sharpened rule v3 for JARGON: Before the first occurrence of any term from the list—in headings, body, bullets, or the 'What You Will Learn' list—add a plain‑language definition of ≤12 words right after the term.
