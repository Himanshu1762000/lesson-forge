# Rejection Log — Introduction to RAG

- Run: `20261108-103851-introduction-to-rag-inject`
- Final status: **SHIPPED** (attempt 3 of 3; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): ON
- Rules from memory used in this run: 6

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator + saboteur | 9/18 | REJECTED | FLOW, AVOID_WORDS, PLAIN_LANGUAGE, ACRONYMS, DEFINED_BEFORE_USE, JARGON, ANALOGY, ACCURACY, NO_OVERCLAIM |
| 2 | reviser | 16/18 | REJECTED | DEFINED_BEFORE_USE, JARGON |
| 3 | reviser | 18/18 | PASS | - |

## Attempt 1 — REJECTED

**How this attempt was produced / what changed:**

- First draft written from the plan with 6 learned rule(s) from memory
- [SABOTEUR] injected: "In fact, RAG works by retraining the LLM on your documents every time you ask a question. So the model permanently memorises them and RAG answers are always 100% correct." -> expected to fail ACCURACY, NO_OVERCLAIM (Misconceptions M1 (RAG retrains the model) and M2 (always correct).)
- [SABOTEUR] injected: "Under the hood, the retriever runs ANN search with cosine similarity over dense vectors stored in an HNSW index." -> expected to fail JARGON, ACRONYMS, AVOID_WORDS (Unexplained jargon, unexpanded acronyms (ANN, HNSW) and an idiom ('under the hood').)

**What failed and why:**

### FLOW (coherent teaching flow, llm check)
- **Why:** The term "prompt" is used before being explained, violating the rule that every idea must be introduced before it is used.
- **Evidence:** "Augmented means added to or made stronger. The retrieved text is added to the question in the prompt (the input text given to the LLM)."
- **Fix requested:** Add a simple definition of "prompt" before its first use, e.g., explain that a prompt is the input text given to the LLM.

### AVOID_WORDS (beginner-friendly language, code check)
- **Why:** Found: under the hood.
- **Evidence:** ses them and RAG answers are always 100% correct. Under the hood, the retriever runs ANN search with cosine simila
- **Fix requested:** Replace these with simple everyday words: under the hood

### PLAIN_LANGUAGE (beginner-friendly language, llm check)
- **Why:** Contains the idiom "Under the hood" and unexplained technical jargon, making the sentence difficult for a beginner with limited English.
- **Evidence:** "Under the hood, the retriever runs ANN search with cosine similarity over dense vectors stored in an HNSW index."
- **Fix requested:** Replace with plain language, e.g., "To find the best matching chunks, the system compares the question’s embedding with stored embeddings using a similarity measure."

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: AI (full form 'artificial intelligence' not given near first use); ANN (never expanded or explained); HNSW (never expanded or explained)
- **Evidence:** AI (full form 'artificial intelligence' not given near first use); ANN (never expanded or explained); HNSW (never expanded or explained)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 2 term(s) used before being explained.
- **Evidence:** 'vector' is used but never defined (first use: "...retriever runs ANN search with cosine similarity over dense vectors stored in an HNSW index.   Preparation...") || 'chunk' is used before its definition ("....    **Limit**: The answer is only as good as the retrieved chunks. If retrieval fails, the answer can be...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'vector' is used but never defined (first use: "...retriever runs ANN search with cosine similarity over dense vectors stored in an HNSW index.   Preparation..."); 'chunk' is used before its definition ("....    **Limit**: The answer is only as good as the retrieved chunks. If retrieval fails, the answer can be...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** Technical terms such as "prompt", "vector", "vector database", and "context" are not explained in simple words at their first use.
- **Evidence:** "Augmented means added to or made stronger. The retrieved text is added to the question in the prompt (the input text given to the LLM)."
- **Fix requested:** Define each term at first use: prompt = input text given to the LLM; vector = list of numbers representing meaning; vector database = storage for vectors; context = the retrieved text placed in the prompt.

### ANALOGY (teaches by example, llm check)
- **Why:** No everyday analogy from Indian life is provided to explain the core idea of RAG.
- **Evidence:** MISSING: analogy
- **Fix requested:** Add an analogy such as comparing RAG to an open-book exam or a kirana shop owner checking a register, and map retrieval to finding the page/register entry and generation to writing the answer.

### ACCURACY (accurate & grounded, llm check)
- **Why:** Contradicts reference facts F9, F10 and introduces misconceptions M1 (RAG retrains/fine-tunes) and M2 (answers always correct).
- **Evidence:** In fact, RAG works by retraining the LLM on your documents every time you ask a question. So the model permanently memorises them and RAG answers are always 100% correct.
- **Fix requested:** Remove or correct that sentence; replace with an accurate description of preparation (indexing) that does not involve retraining the model.

### NO_OVERCLAIM (accurate & grounded, llm check)
- **Why:** Overstates RAG's effectiveness, violating the requirement not to oversell and contradicts the teaching of a real limitation.
- **Evidence:** answers are always 100% correct.
- **Fix requested:** Remove the overclaim sentence; ensure no claims that RAG is always correct or removes hallucinations.


## Attempt 2 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: FLOW, AVOID_WORDS, PLAIN_LANGUAGE, ACRONYMS, DEFINED_BEFORE_USE, JARGON, ANALOGY, ACCURACY, NO_OVERCLAIM
- [FLOW] Added definition of "prompt" in "Before We Start" before its first use in "What Is RAG?".
- [AVOID_WORDS] Removed the phrase "under the hood" from the Preparation section.
- [PLAIN_LANGUAGE] Replaced the technical jargon sentence ("Under the hood, the retriever runs ANN search...") with a correct, simple description of preparation (indexing) in the Preparation section.
- [ACRONYMS] Expanded "AI" to "artificial intelligence (AI)" at first use. Removed unexplained acronyms ANN and HNSW by deleting the erroneous sentence.
- [DEFINED_BEFORE_USE] Defined "chunk" in the Preparation section before its use in the Limit bullet. Defined "vector" in the Preparation section at first use.
- [JARGON] Added one-sentence definitions for "prompt", "vector", "vector database", "context", "model", "fine‑tuning", "weights", "retraining", "embedding model", "semantic search", "context window" at their first occurrence.
- [ANALOGY] Added an Indian-relevant open‑book exam analogy in a new subsection under "What Is RAG?" mapping retrieval to finding the page and generation to writing the answer.
- [ACCURACY] Removed the false claims that RAG retrains the model and that answers are always 100% correct. Replaced with accurate description of preparation (indexing) and the limit that retrieval quality matters.
- [NO_OVERCLAIM] Deleted the overclaim "RAG answers are always 100% correct" and ensured the lesson states RAG reduces but does not remove hallucinations.

**Checks fixed vs previous attempt:** ACCURACY, ACRONYMS, ANALOGY, AVOID_WORDS, FLOW, NO_OVERCLAIM, PLAIN_LANGUAGE  
**Checks newly broken:** none

**What failed and why:**

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 1 term(s) used before being explained.
- **Evidence:** 'vector' is used before its definition ("...embeddings in a **vector database** (a searchable store of vectors). A **vector** is another word for embe...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'vector' is used before its definition ("...embeddings in a **vector database** (a searchable store of vectors). A **vector** is another word for embe...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The technical term 'indexing' appears in the section heading but is never explained in simple words in the body of the lesson.
- **Evidence:** ### Preparation (Indexing)
- **Fix requested:** Add a simple explanation of indexing at or before the heading, e.g., 'Indexing means organizing the chunks so they can be searched quickly.'


## Attempt 3 — PASSED

**How this attempt was produced / what changed:**

- Revised from attempt 2 to fix: DEFINED_BEFORE_USE, JARGON
- [DEFINED_BEFORE_USE] Moved the definition of 'vector' before its use in 'vector database'. Added a sentence "A **vector** is a list of numbers that represents the meaning of text." right before the vector database sentence in the Preparation (Indexing) section.
- [JARGON] Added a simple definition of 'indexing' at the start of the Preparation (Indexing) section: "**Indexing** means organizing the chunks so they can be searched quickly."

**Checks fixed vs previous attempt:** DEFINED_BEFORE_USE, JARGON  
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
