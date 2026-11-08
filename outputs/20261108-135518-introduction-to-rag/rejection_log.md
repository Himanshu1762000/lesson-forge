# Rejection Log — Introduction to RAG

- Run: `20261108-135518-introduction-to-rag`
- Final status: **SHIPPED** (attempt 3 of 3; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): off
- Rules from memory used in this run: 5

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator | 13/18 | REJECTED | LENGTH, ACRONYMS, DEFINED_BEFORE_USE, JARGON, ANALOGY |
| 2 | reviser | 17/18 | REJECTED | JARGON |
| 3 | reviser | 18/18 | PASS | - |

## Attempt 1 — REJECTED

**How this attempt was produced / what changed:**

- First draft written from the plan with 5 learned rule(s) from memory

**What failed and why:**

### LENGTH (beginner-friendly language, code check)
- **Why:** 821 words (allowed 900-2600).
- **Evidence:** 821
- **Fix requested:** Add depth to thin sections.

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: AI (full form 'artificial intelligence' not given near first use)
- **Evidence:** AI (full form 'artificial intelligence' not given near first use)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 4 term(s) used before being explained.
- **Evidence:** 'semantic search' is used but never defined (first use: "...tem finds the chunks whose meaning is most similar. This is semantic search. Usually the top few chunks are taken....") || 'weights' is used but never defined (first use: "...wer using the added pieces.   RAG does not change the model weights. The model stays the same....") || 'prompt' is used but never defined (first use: "...rmation.   - **Augmented** means adding those pieces to the prompt.   - **Generation** means the LLM write...") || 'chunk' is used before its definition ("...the retrieved pieces. If the search returns a wrong or old chunk, the answer can be wrong. The LLM can s...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'semantic search' is used but never defined (first use: "...tem finds the chunks whose meaning is most similar. This is semantic search. Usually the top few chunks are taken...."); 'weights' is used but never defined (first use: "...wer using the added pieces.   RAG does not change the model weights. The model stays the same...."); 'prompt' is used but never defined (first use: "...rmation.   - **Augmented** means adding those pieces to the prompt.   - **Generation** means the LLM write..."); 'chunk' is used before its definition ("...the retrieved pieces. If the search returns a wrong or old chunk, the answer can be wrong. The LLM can s...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** Technical terms 'model', 'prompt', 'context', and 'weights' are used without simple explanations at first use.
- **Evidence:** A large language model (LLM) is an AI model trained on a huge amount of text.
- **Fix requested:** Explain each term simply when first introduced: e.g., 'model' = a mathematical system that learns patterns; 'prompt' = the instructions and data given to the AI; 'context' = the background information the AI can see at once; 'weights' = the internal numbers the model learned during training.

### ANALOGY (teaches by example, llm check)
- **Why:** No everyday analogy from Indian life (e.g., open‑book exam, library, kirana shop, railway enquiry) is provided to explain RAG and map its parts.
- **Evidence:** MISSING: analogy
- **Fix requested:** Add an analogy such as: 'RAG is like an open‑book exam: first you retrieve the relevant page (retrieval), you add those notes to your answer sheet (augmentation), then you write the answer using those notes (generation).'


## Attempt 2 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: LENGTH, ACRONYMS, DEFINED_BEFORE_USE, JARGON, ANALOGY
- [LENGTH] Added depth to "Before We Start", "What Is RAG?", "Why Does RAG Matter?", and "How Does RAG Work?" sections to increase word count above 900.
- [ACRONYMS] Expanded "AI" to "artificial intelligence (AI)" at first use in the "Before We Start" section.
- [DEFINED_BEFORE_USE] Defined 'model' at first use as "a mathematical system that learns patterns from data"; defined 'prompt' at first use as "the instructions and data given to the AI"; defined 'weights' at first use as "the internal numbers the model learned during training"; defined 'chunk' at first use in the limitation section as "a small piece of a document"; defined 'semantic search' at first use as "search by meaning, not just keywords"; defined 'context window' and explained 'context' at first use.
- [JARGON] Provided simple explanations for 'model', 'prompt', 'context', and 'weights' at their first occurrences.
- [ANALOGY] Added an Indian open‑book exam analogy in a new subsection under "What Is RAG?" with clear labels for retrieval, augmentation, and generation.

**Checks fixed vs previous attempt:** ACRONYMS, ANALOGY, DEFINED_BEFORE_USE, LENGTH  
**Checks newly broken:** none

**What failed and why:**

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The technical term 'context' (referring to the context window) is used before its definition is provided later in the same paragraph.
- **Evidence:** The LLM can still hallucinate or ignore the context.
- **Fix requested:** Define 'context' at its first use, e.g., change the sentence to 'The LLM can still hallucinate or ignore the context (the text the model can see at once)' or move the definition of 'context window' before this sentence.


## Attempt 3 — PASSED

**How this attempt was produced / what changed:**

- Revised from attempt 2 to fix: JARGON
- [JARGON] Defined 'context' at first use in the Limitations paragraph: changed "The LLM can still hallucinate or ignore the context." to "The LLM can still hallucinate or ignore the context (the text the model can see at once)."

**Checks fixed vs previous attempt:** JARGON  
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

## What the system learned from this run (saved to memory)

- Sharpened rule v3 for ANALOGY: When describing RAG, insert one familiar Indian analogy—such as an open‑book exam, a library visit, a kirana shopkeeper consulting a register, or a railway enquiry counter—and clearly label which element corresponds to retrieval and which to generation.
- Sharpened rule v3 for DEFINED_BEFORE_USE: On first use of any core technical term—training data, prompt, semantic search, weights, knowledge cutoff—immediately follow it with a concise definition in parentheses or a dash.
- New rule v1 for JARGON: Define each listed technical term (model, LLM, prompt, token, training data, knowledge cutoff, hallucination, retrieval, chunk, embedding, vector, vector database, semantic search, context, fine‑tuning, weights) in simple words at its first use.
