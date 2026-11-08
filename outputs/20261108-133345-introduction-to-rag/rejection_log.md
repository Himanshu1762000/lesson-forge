# Rejection Log — Introduction to RAG

- Run: `20261108-133345-introduction-to-rag`
- Final status: **SHIPPED** (attempt 2 of 2; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): off
- Rules from memory used in this run: 5

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator | 14/18 | REJECTED | PLAIN_LANGUAGE, DEFINED_BEFORE_USE, JARGON, ANALOGY |
| 2 | reviser | 18/18 | PASS | - |

## Attempt 1 — REJECTED

**How this attempt was produced / what changed:**

- First draft written from the plan with 5 learned rule(s) from memory

**What failed and why:**

### PLAIN_LANGUAGE (beginner-friendly language, llm check)
- **Why:** Uses passive voice instead of active voice, making the sentence harder for a beginner to understand.
- **Evidence:** The retrieved text is added to the question in the prompt.
- **Fix requested:** Rewrite in active voice, e.g., 'We add the retrieved text to the question in the prompt.'

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 4 term(s) used before being explained.
- **Evidence:** 'training data' is used but never defined (first use: "...ree main limits.  First, it has a **knowledge cutoff**. Its training data stops at a fixed date. It does not know...") || 'prompt' is used before its definition ("...tronger. The retrieved text is added to the question in the prompt.  **Generation** means the LLM writes t...") || 'vector' is used before its definition ("...embeddings in a **vector database** (a searchable store of vectors). A **vector** is a list of numbers rep...") || 'chunk' is used before its definition ("...One limitation: the answer is only as good as the retrieved chunks. If the search returns wrong or outdate...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'training data' is used but never defined (first use: "...ree main limits.  First, it has a **knowledge cutoff**. Its training data stops at a fixed date. It does not know..."); 'prompt' is used before its definition ("...tronger. The retrieved text is added to the question in the prompt.  **Generation** means the LLM writes t..."); 'vector' is used before its definition ("...embeddings in a **vector database** (a searchable store of vectors). A **vector** is a list of numbers rep..."); 'chunk' is used before its definition ("...One limitation: the answer is only as good as the retrieved chunks. If the search returns wrong or outdate...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** Technical terms prompt, training data, context, and weights are used without being explained in simple words at or before their first use.
- **Evidence:** The retrieved text is added to the question in the prompt.
- **Fix requested:** Define each term at first use: prompt = the instructions and question given to the LLM; training data = the text the model learned from; context = the extra information provided to help answer; weights = the internal numbers the model learned.

### ANALOGY (teaches by example, llm check)
- **Why:** No everyday Indian analogy (e.g., open-book exam, librarian) is provided to explain the core idea of RAG and map its parts to retrieval and generation.
- **Evidence:** MISSING: analogy
- **Fix requested:** Add an analogy such as comparing RAG to an open-book exam: retrieval = finding the right page, generation = writing the answer using that page.


## Attempt 2 — PASSED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: PLAIN_LANGUAGE, DEFINED_BEFORE_USE, JARGON, ANALOGY
- [PLAIN_LANGUAGE] Changed passive sentence "The retrieved text is added to the question in the prompt." to active voice "We add the retrieved text to the question in the prompt." in the What Is RAG? section.
- [DEFINED_BEFORE_USE] Defined 'training data' at first use in Before We Start: added "(the text the model learned from)".
- [DEFINED_BEFORE_USE] Defined 'prompt' at first use in What Is RAG?: added "(the instructions and question given to the LLM)".
- [DEFINED_BEFORE_USE] Defined 'vector' at first use in Preparation: changed "vector database" to "vector (a list of numbers representing data) database" and removed the separate definition sentence.
- [DEFINED_BEFORE_USE] Defined 'chunk' at first use in Why Does RAG Matter?: added "(small pieces of a document)".
- [JARGON] Defined 'context' at first use in What Is RAG?: added "(the extra information provided to help answer)".
- [JARGON] Simplified definition of 'weights' at first use in What Is RAG?: changed "(its learned internal numbers)" to "(the internal numbers the model learned)".
- [JARGON] Added glossary entries for 'Training data', 'Prompt', 'Context', 'Weights' to match simplified definitions.
- [ANALOGY] Added an open-book exam analogy in What Is RAG? section, labeling retrieval (finding the right page) and generation (writing the answer using that page).

**Checks fixed vs previous attempt:** ANALOGY, DEFINED_BEFORE_USE, JARGON, PLAIN_LANGUAGE  
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
