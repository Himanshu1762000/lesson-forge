# Rejection Log — Introduction to RAG

- Run: `20261108-101430-introduction-to-rag`
- Final status: **NEEDS_HUMAN_REVIEW** (attempt 2 of 3; max retries 2)
- Grounding: verified (rag_reference.md)
- Error injection (demo mode): off
- Rules from memory used in this run: 5

## Attempt overview

| Attempt | Produced by | Checks passed | Verdict | Failed checks |
|---|---|---|---|---|
| 1 | generator | 15/18 | REJECTED | ACRONYMS, DEFINED_BEFORE_USE, JARGON |
| 2 | reviser | 15/18 | REJECTED | ACRONYMS, DEFINED_BEFORE_USE, JARGON |
| 3 | reviser | 14/18 | REJECTED | FLOW, ACRONYMS, DEFINED_BEFORE_USE, JARGON |

## Attempt 1 — REJECTED

**How this attempt was produced / what changed:**

- First draft written from the plan with 5 learned rule(s) from memory

**What failed and why:**

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: PM (never expanded or explained)
- **Evidence:** PM (never expanded or explained)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 5 term(s) used before being explained.
- **Evidence:** 'embedding model' is used but never defined (first use: "...of numbers that captures the meaning of the text) using an embedding model. 4. Store them in a **vector database**...") || 'retraining' is used but never defined (first use: "...urces so you can check them.  It is cheaper and faster than retraining the model.  Knowledge is easy to update...") || 'embedding' is used before its definition ("...ent, generate. - How knowledge is prepared using chunks and embeddings. - Why RAG helps and one key limit....") || 'vector' is used before its definition ("...Store them in a **vector database** (a searchable index for vectors).  A **vector** is a list of numbers th...") || 'chunk' is used before its definition ("...rieve, augment, generate. - How knowledge is prepared using chunks and embeddings. - Why RAG helps and one...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'embedding model' is used but never defined (first use: "...of numbers that captures the meaning of the text) using an embedding model. 4. Store them in a **vector database**..."); 'retraining' is used but never defined (first use: "...urces so you can check them.  It is cheaper and faster than retraining the model.  Knowledge is easy to update..."); 'embedding' is used before its definition ("...ent, generate. - How knowledge is prepared using chunks and embeddings. - Why RAG helps and one key limit...."); 'vector' is used before its definition ("...Store them in a **vector database** (a searchable index for vectors).  A **vector** is a list of numbers th..."); 'chunk' is used before its definition ("...rieve, augment, generate. - How knowledge is prepared using chunks and embeddings. - Why RAG helps and one...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** Three technical terms are used at first appearance without a simple explanation: (1) 'indexing' in the heading 'Preparation (Indexing)' is never defined; (2) 'embedding model' in 'using an embedding model' is not explained; (3) 'context window' in 'the context window' is mentioned but not defined.
- **Evidence:** Preparation (Indexing)
- **Fix requested:** Define each term at first use: for 'indexing' add a sentence like 'Indexing is the process of preparing documents so they can be searched quickly.' For 'embedding model' add 'an embedding model is a tool that turns text into embeddings.' For 'context window' add 'the context window is the maximum amount of text the LLM can take at once.'


## Attempt 2 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 1 to fix: ACRONYMS, DEFINED_BEFORE_USE, JARGON
- [ACRONYMS] Expanded "PM" to "Prime Minister (PM)" at first use in the Example section.
- [DEFINED_BEFORE_USE] Replaced technical terms in "What You Will Learn" bullet 4 with plain language to avoid using 'chunks', 'embeddings', 'vector' before definition.
- [DEFINED_BEFORE_USE] Defined 'chunk' at first use in Preparation step 2.
- [DEFINED_BEFORE_USE] Defined 'embedding' and 'embedding model' at first use in Preparation step 3.
- [DEFINED_BEFORE_USE] Defined 'vector' at first use in Preparation step 4 (before using it in vector database definition).
- [DEFINED_BEFORE_USE] Defined 'retraining' at first use in "Why Does RAG Matter?" section.
- [JARGON] Defined 'indexing' in a sentence immediately after the "Preparation (Indexing)" heading.
- [JARGON] Defined 'embedding model' at first use in Preparation step 3.
- [JARGON] Defined 'context window' at first use in the limitations paragraph.
- [JARGON] Added definitions for 'embedding model', 'retraining', 'indexing', 'context window' to the Key Words glossary.

**Checks fixed vs previous attempt:** none  
**Checks newly broken:** none

**What failed and why:**

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: PM (never expanded or explained)
- **Evidence:** PM (never expanded or explained)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 2 term(s) used before being explained.
- **Evidence:** 'vector' is used before its definition ("...Store them in a **vector database** (a searchable index for vectors). A **vector** is a list of numbers tha...") || 'chunk' is used before its definition ("...what is retrieved. If the search returns wrong or outdated chunks, the answer can be wrong. The LLM can s...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'vector' is used before its definition ("...Store them in a **vector database** (a searchable index for vectors). A **vector** is a list of numbers tha..."); 'chunk' is used before its definition ("...what is retrieved. If the search returns wrong or outdated chunks, the answer can be wrong. The LLM can s...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** Technical terms (LLM, RAG, retrieve, augment, generate, chunks, embeddings) appear in the "What You Will Learn" list without explanation at that point; the first use of each term must be explained there or earlier.
- **Evidence:** What an LLM (Large Language Model) is and what its limits are.
- **Fix requested:** Either add a one-sentence plain-language explanation for each term in the learning-objectives list, or move the list after the definitions, or replace the technical terms with plain descriptions in the list.


## Attempt 3 — REJECTED

**How this attempt was produced / what changed:**

- Revised from attempt 2 to fix: ACRONYMS, DEFINED_BEFORE_USE, JARGON
- [ACRONYMS] Expanded "PM" to "Prime Minister (PM)" at first use in the example section.
- [DEFINED_BEFORE_USE] Defined "chunk" at its first use in the "Why Does RAG Matter?" section by adding "(small pieces of a document)".
- [DEFINED_BEFORE_USE] Defined "vector" before "vector database" in the Preparation section by adding "This list of numbers is called a **vector**." before the vector database sentence.
- [JARGON] Added plain-language explanations for each technical term in the "What You Will Learn" list.

**Checks fixed vs previous attempt:** none  
**Checks newly broken:** FLOW

**What failed and why:**

### FLOW (coherent teaching flow, llm check)
- **Why:** The term 'chunks' is used in the 'Why Does RAG Matter?' section before it is defined in the later 'How Does RAG Work?' section (Preparation).
- **Evidence:** If the search returns wrong or outdated chunks
- **Fix requested:** Move the definition of 'chunks' (and the preparation/indexing explanation) before the 'Why Does RAG Matter?' section, or remove the reference to 'chunks' from that section until after it has been introduced.

### ACRONYMS (clear, no unexplained jargon, code check)
- **Why:** Unexpanded acronyms: PM (never expanded or explained)
- **Evidence:** PM (never expanded or explained)
- **Fix requested:** Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.

### DEFINED_BEFORE_USE (clear, no unexplained jargon, code check)
- **Why:** 2 term(s) used before being explained.
- **Evidence:** 'embedding' is used before its definition ("...chunks) and turning them into numbers that capture meaning (embeddings). - Why RAG helps and one key limit....") || 'chunk' is used before its definition ("...ledge is prepared by splitting documents into small pieces (chunks) and turning them into numbers that cap...")
- **Fix requested:** Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its FIRST use, or replace the earlier uses with plain words. Terms: 'embedding' is used before its definition ("...chunks) and turning them into numbers that capture meaning (embeddings). - Why RAG helps and one key limit...."); 'chunk' is used before its definition ("...ledge is prepared by splitting documents into small pieces (chunks) and turning them into numbers that cap...")

### JARGON (clear, no unexplained jargon, llm check)
- **Why:** The technical term 'chunk' (and 'chunks') is used in the body of the lesson ('Why Does RAG Matter?') before it is explained in simple words. Its first explanation appears later in 'How Does RAG Work?' under Preparation.
- **Evidence:** If the search returns wrong or outdated chunks
- **Fix requested:** Define 'chunk' in simple words at or before its first use in the body (e.g., in 'Why Does RAG Matter?' add a parenthetical explanation: 'chunks (small pieces of a document)').


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
| ACRONYMS | clear, no unexplained jargon | code | **FAIL** |
| DEFINED_BEFORE_USE | clear, no unexplained jargon | code | **FAIL** |
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

- Sharpened rule v2 for ACRONYMS: On the first occurrence of any acronym, write its full expanded form immediately followed by the acronym in parentheses, with no other words between them (e.g., 'large language model (LLM)').
- New rule v1 for DEFINED_BEFORE_USE: On the first occurrence of any core technical term from the set {embedding model, retraining, vector, chunk, embedding}, the writer must supply a brief definition either directly after the term in parentheses or as an appositive clause within the same sentence.
- Sharpened rule v2 for JARGON: When first using any term from the list (model, LLM, prompt, token, training data, knowledge cutoff, hallucination, retrieval, chunk, embedding, vector, vector database, semantic search, context, fine‑tuning, weights) in headings, body, or bullets, add a plain‑language one‑sentence definition right after it.
