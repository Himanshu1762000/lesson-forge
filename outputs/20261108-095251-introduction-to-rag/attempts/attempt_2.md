# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn

In this lesson you will learn:

* What an **LLM (Large Language Model)** is and its three main limits: knowledge cutoff, no private data, hallucination.
* The full form of RAG and the meaning of each word: Retrieval, Augmented, Generation.
* The three steps when a user asks a question: Retrieve → Augment → Generate.
* How documents are prepared: chunks, embeddings, vector database.
* Benefits of RAG: fresh data, private data, fewer hallucinations, sources, no retraining.
* One limitation: answer quality depends on retrieval quality.
* RAG does not retrain the model (different from fine-tuning).

## Before We Start: Some Basic Ideas

**AI (Artificial Intelligence)** is a computer program that can do tasks needing human-like thinking. Examples: Google search, UPI fraud detection.

**LLM (Large Language Model)** is an AI model trained on huge text from books and websites. It generates text by predicting the next **token**. A token is a word or part of a word. Examples: models behind ChatGPT, Gemini.

**Prompt** is the instruction and context you give to the LLM. It tells the LLM what to do and what information to use.

A plain LLM has three limits:

1. **Knowledge Cutoff**: Training stops at a fixed date. The LLM knows nothing after that date.
2. **No Private Data**: The LLM never saw your college fee list, company policy, or personal notes.
3. **Hallucination**: The LLM can sound confident but give wrong or made-up answers.

## What Is RAG?

**RAG** stands for **Retrieval-Augmented Generation**. The term came from a 2020 research paper by Patrick Lewis and his team at Meta.

* **Retrieval** = Finding and fetching relevant pieces of information from an outside source.
* **Augmented** = Added to / made stronger. The retrieved text is added to the user question in the prompt.
* **Generation** = The LLM writes (generates) the answer using the question plus the retrieved context.

Simple definition: Before answering, the system first searches your documents, adds the found text to the question, then the LLM answers.

### An Everyday Analogy: Open-Book Exam

Think of an open-book exam.  
A closed-book student answers only from memory (like a plain LLM).  
An open-book student first finds the right page (Retrieval), then writes the answer using that page (Generation).  
RAG works the same way: the system finds the right chunk, then the LLM writes the answer with it.

## Why Does RAG Matter?

RAG helps in real-world use because:

* It uses up-to-date information (solves knowledge cutoff).
* It uses private or organisation data (college prospectus, company policy).
* It reduces hallucinations (fewer made-up answers) — but does not remove them completely.
* Answers can show sources (citations) so you can verify.
* It is cheaper and faster than retraining the model.
* Knowledge is easy to update: just change documents, not the model.

## How Does RAG Work?

There are two phases: preparation (done once) and question-time (every user question).

### Preparation (Indexing)

Done before any question arrives:

1. Collect documents (PDFs, web pages, notes).
2. Split into small pieces called **chunks** (1-2 paragraphs each).
3. Turn each chunk into an **embedding** — a list of numbers that captures the meaning of the text. This is not encryption, not compression.
4. Store embeddings in a **vector database** for fast meaning-based search.

### Question-Time Steps

For every user question:

1. **Retrieve**: User question → embedding → **semantic search** (find chunks with closest meaning) → take top-k chunks.
2. **Augment**: Put retrieved chunks into the prompt with the question and an instruction like "Answer using only this information".
3. **Generate**: LLM writes answer from question plus retrieved context. It can cite sources.

**Important**: RAG does **not** change model weights. To update knowledge, update documents, not the model.

**Fine-tuning** is different: it trains the model further, changes weights, slower and costlier, used for style or behaviour.

## Example: College Scholarship Chatbot

**Setting**: Priya, a 12th-pass student from Bhopal, uses a college chatbot on her phone.

**Question**: "What is the last date to apply for the Merit Scholarship 2024 at Bhopal Engineering College?"

**Knowledge base has 3 documents**:

* Doc 1: Bhopal Engineering College Prospectus 2024. Merit Scholarship: Amount ₹20,000 per year. Eligibility: 85% in 12th. Application opens 1 June 2024. Last date to apply: 31 July 2024.
* Doc 2: Hostel Fee Structure 2024. Boys hostel: ₹60,000/year. Girls hostel: ₹55,000/year. Mess charges extra.
* Doc 3: Placement Stats 2023. Highest package ₹18 **LPA (Lakhs Per Annum)**. Average ₹6 LPA. Top recruiters: **TCS (Tata Consultancy Services)**, Infosys, Wipro.

**Retrieve**: Semantic search finds Doc 1 snippet with scholarship dates.

**Retrieved snippet**:
> Merit Scholarship: Amount ₹20,000 per year. Eligibility: 85% in 12th. Application opens 1 June 2024. Last date to apply: 31 July 2024.

**Augment**: The snippet is added to the prompt with instruction.

**Prompt sent to LLM**:
> Answer using only this information.
> Context: Merit Scholarship: Amount ₹20,000 per year. Eligibility: 85% in 12th. Application opens 1 June 2024. Last date to apply: 31 July 2024.
> Question: What is the last date to apply for the Merit Scholarship 2024 at Bhopal Engineering College?

**Generate**: LLM answers.

**Answer with RAG**:
> According to the Bhopal Engineering College Prospectus 2024, the last date to apply for the Merit Scholarship 2024 is 31 July 2024. [Source: Doc 1]

**Answer without RAG** (LLM guesses):
> The last date for most college scholarships in India is usually 30 June or 15 July. You should check the website.

With RAG, Priya gets the correct, sourced answer. Without RAG, the LLM hallucinates a wrong date.

## Key Words to Remember

* **AI**: Computer program that mimics human thinking.
* **LLM (Large Language Model)**: Predicts next token to generate text.
* **Token**: A word or part of a word (LLM works in tokens).
* **Prompt**: Instruction and context given to the LLM.
* **Knowledge Cutoff**: Date when LLM training stopped.
* **Hallucination**: Confident but wrong or made-up answer.
* **RAG**: Retrieval-Augmented Generation.
* **Retrieval**: Finding relevant chunks from knowledge base.
* **Augmented**: Adding retrieved text to the prompt.
* **Generation**: LLM writing the final answer.
* **Chunk**: Small piece of a document (1-2 paragraphs).
* **Embedding**: List of numbers representing meaning of text.
* **Vector Database**: Storage for embeddings, enables meaning-based search.
* **Semantic Search**: Search by meaning, not just keywords.
* **Context Window**: Max text LLM can take in one prompt (limits chunks).
* **Fine-tuning**: Training model further to change weights (different from RAG).

## Quick Check

1. What are the three limits of a plain LLM?  
**Answer:** 1) Knowledge cutoff (fixed date), 2) No private data, 3) Can hallucinate (make up answers).

2. What does RAG stand for? Explain each word in one sentence.  
**Answer:** Retrieval = find relevant chunks. Augmented = add chunks to prompt. Generation = LLM writes answer using them.

3. What is the correct order of steps when a user asks a question in RAG?  
**Answer:** Retrieve → Augment → Generate.

4. Does RAG retrain or change the LLM model?  
**Answer:** No. RAG does not change model weights. To update knowledge, you update the documents only.

5. If the retrieval step returns a wrong or outdated chunk, what happens to the answer?  
**Answer:** The answer can be wrong because RAG answer quality depends on retrieval quality.

## Summary

* LLM = predicts next token; limits: cutoff date, no private data, hallucination.
* RAG = Retrieval-Augmented Generation. Before answering, system retrieves relevant chunks, adds them to prompt, then LLM generates.
* Preparation: documents → chunks → embeddings → vector database (done once).
* Question-time: Retrieve (semantic search) → Augment (add to prompt) → Generate (answer with citations).
* Benefits: fresh/private data, fewer hallucinations, sources, no retraining. Limitation: answer only as good as retrieved chunks. RAG ≠ fine-tuning.
