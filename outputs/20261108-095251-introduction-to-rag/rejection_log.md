# Rejection Log — Introduction to RAG

- Run: `20261108-095251-introduction-to-rag`
- Final status: **NEEDS_HUMAN_REVIEW** (attempt 3 of 3; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): off
- Rules from memory used in this run: 0

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator | 11/16 | REJECTED | FLOW, READABILITY, ACRONYMS, JARGON, ANALOGY |
| 2 | reviser | 13/16 | REJECTED | FLOW, READABILITY, JARGON |
| 3 | reviser | 14/16 | REJECTED | READABILITY, JARGON |

## Attempt 1 — REJECTED

**How this attempt was produced / what changed:**

- First draft written from the plan

**What failed and why:**

### FLOW (coherent teaching flow, llm check)
- **Why:** The term "prompt" is used before being explained, breaking the flow where ideas must be introduced before use.
- **Evidence:** The retrieved text is added to the user question in the prompt.
- **Fix requested:** Introduce and explain what a prompt is before its first use, e.g., in the "Before We Start" section.

### READABILITY (beginner-friendly language, code check)
- **Why:** Flesch Reading Ease 58.1 (need >= 60).
- **Evidence:** 58.1
- **Fix requested:** Use shorter sentences and shorter, more common words.

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: LLM (full form 'large language model' not given near first use); NOT (never expanded or explained); LPA (never expanded or explained); TCS (never expanded or explained)
- **Evidence:** LLM (full form 'large language model' not given near first use); NOT (never expanded or explained); LPA (never expanded or explained); TCS (never expanded or explained)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The technical term "prompt" appears without prior explanation; a definition only later or in a glossary does not satisfy the rule.
- **Evidence:** The retrieved text is added to the user question in the prompt.
- **Fix requested:** Define "prompt" at its first use, e.g., "Prompt = the instructions and context given to the LLM."

### ANALOGY (teaches by example, llm check)
- **Why:** No everyday Indian analogy (e.g., open‑book exam, kirana shop register, railway enquiry) is provided to explain the core idea of RAG and map its parts to retrieval and generation.
- **Evidence:** MISSING: everyday analogy from life in India
- **Fix requested:** Add an analogy such as an open‑book exam: retrieval = finding the right page, generation = writing the answer using that page, and explicitly map each step.


## Attempt 2 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: FLOW, READABILITY, ACRONYMS, JARGON, ANALOGY
- [FLOW] Defined "prompt" in the "Before We Start" section before its first use in "What Is RAG?".
- [JARGON] Added definition of "prompt" at first use in "Before We Start".
- [READABILITY] Shortened sentences and simplified vocabulary throughout (e.g., broke long sentences, replaced "colleagues" with "team", "semantic search" explained simply).
- [ACRONYMS] Expanded LLM at first use in "What You Will Learn"; changed "NOT" to "does not"; expanded LPA and TCS in the example.
- [ANALOGY] Added an open-book exam analogy in "What Is RAG?" with explicit mapping to retrieval and generation.

**Checks fixed vs previous attempt:** ACRONYMS, ANALOGY  
**Checks newly broken:** none

**What failed and why:**

### FLOW (coherent teaching flow, llm check)
- **Why:** The term "retraining" is used before it is explained later in the lesson.
- **Evidence:** It is cheaper and faster than retraining the model.
- **Fix requested:** Introduce a brief explanation of retraining/fine‑tuning before this sentence, or move the explanation earlier.

### READABILITY (beginner-friendly language, code check)
- **Why:** Flesch Reading Ease 59.7 (need >= 60).
- **Evidence:** 59.7
- **Fix requested:** Use shorter sentences and shorter, more common words.

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The technical term "model weights" appears before being defined or explained.
- **Evidence:** RAG does not change model weights.
- **Fix requested:** Provide a short definition of model weights (e.g., "the internal numbers the model learned during training") before this sentence.


## Attempt 3 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 2 to fix: FLOW, READABILITY, JARGON
- [FLOW] Added a brief explanation of "retraining" in the "Why Does RAG Matter?" section right before the sentence that uses the term.
- [READABILITY] Simplified sentences throughout the lesson: broke long sentences, replaced complex words with simpler ones (e.g., "organisation" -> "organization" kept but context simplified, "mimics" -> "copies" not used but kept simple). Overall reduced sentence length and used more common vocabulary.
- [JARGON] Added a definition for "model weights" at first use in the "How Does RAG Work?" section: "Model weights are the internal numbers the model learned during training." Also added "Model Weights" to the Key Words list.

**Checks fixed vs previous attempt:** FLOW  
**Checks newly broken:** none

**What failed and why:**

### READABILITY (beginner-friendly language, code check)
- **Why:** Flesch Reading Ease 59.8 (need >= 60).
- **Evidence:** 59.8
- **Fix requested:** Use shorter sentences and shorter, more common words.

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The term 'fine-tuning' is used in the bullet list before any explanation is given; its first appearance lacks a simple definition.
- **Evidence:** * RAG does not retrain the model (different from fine-tuning).
- **Fix requested:** Explain fine-tuning at first mention, e.g., '* RAG does not retrain the model (different from fine‑tuning, which is further training that changes the model’s weights).' Also explain 'top‑k' as 'the few most similar chunks'.


## Final scorecard

| Check | Dimension | Type | Result |
|---|---|---|---|
| STRUCTURE | coherent teaching flow | code | PASS |
| FLOW | coherent teaching flow | llm | PASS |
| SENTENCE_LENGTH | beginner-friendly language | code | PASS |
| READABILITY | beginner-friendly language | code | **FAIL** |
| AVOID_WORDS | beginner-friendly language | code | PASS |
| PLAIN_LANGUAGE | beginner-friendly language | llm | PASS |
| LENGTH | beginner-friendly language | code | PASS |
| ACRONYMS | clear, no unexplained jargon | code | PASS |
| JARGON | clear, no unexplained jargon | llm | **FAIL** |
| ANALOGY | teaches by example | llm | PASS |
| WORKED_EXAMPLE | teaches by example | llm | PASS |
| ACCURACY | accurate & grounded | llm | PASS |
| GROUNDED_DEFINITION | accurate & grounded | llm | PASS |
| NO_OVERCLAIM | accurate & grounded | llm | PASS |
| COVERAGE | covers the key points | llm | PASS |
| QUIZ | covers the key points | code | PASS |

## What the system learned from this run (saved to memory)

- New rule v1 for FLOW: Define every technical term (e.g., 'prompt', 'retraining') in the sentence where it first appears, and do not use the term again until after that definition has been given.
- New rule v1 for JARGON: For each term in the list (model, LLM, prompt, token, training data, knowledge cutoff, hallucination, retrieval, chunk, embedding, vector, vector database, semantic search, context, fine‑tuning, weights), give a simple definition at or before its first appearance in the lesson body.
- New rule v1 for READABILITY: Write sentences averaging no more than 18 words; ensure at least 80% of words have two syllables or fewer; avoid jargon and passive voice.
