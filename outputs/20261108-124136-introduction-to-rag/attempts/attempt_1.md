# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn
In this lesson you will learn:
- What a large language model (LLM) is and its main limits.
- The full form of RAG and the meaning of each word.
- The three steps that happen when a question is answered with RAG.
- One benefit and one limitation of using RAG.

## Before We Start: Some Basic Ideas
A **large language model (LLM)** is an AI model trained on a very large amount of text. It generates text by predicting the next **token** (a word or part of a word). Examples are the models behind ChatGPT, Gemini, and Claude.

The model’s knowledge comes from its **training data** (the text collection used to teach the model). This data stops at a fixed date called the **knowledge cutoff**. The model does not know about events after that date.

An LLM does not know private or organisation‑specific information it never saw during training. For example, it does not know your college’s fee list or a company’s internal policy.

LLMs can produce answers that sound confident but are wrong or made up. This is called **hallucination**.

## What Is RAG?
**RAG** stands for **Retrieval‑Augmented Generation**.  
- **Retrieval** means finding the relevant pieces of information from an outside source.  
- **Augmented** means adding those pieces to the user question inside the **prompt** (the full text sent to the model).  
- **Generation** means the LLM writes the answer using the question plus the added information.

The term was introduced in a 2020 research paper by Patrick Lewis and colleagues.

## Why Does RAG Matter?
RAG helps in several ways:
- Answers can use up‑to‑date and private information.
- Fewer made‑up answers (hallucinations are reduced, not removed).
- Answers can show their sources.
- It is cheaper and faster than **retraining** (teaching the model again from scratch or on new data).
- Knowledge is easy to update by changing the documents, not the model.

RAG does not change the model’s **weights** (the internal numbers the model learns during training). **Fine‑tuning** (extra training that changes the model weights) does change them. RAG is usually the better first choice for giving a model new or changing facts.

**Limitation:** The answer is only as good as the chunks that are retrieved. If the search returns wrong or outdated chunks, the answer can be wrong. The LLM can still hallucinate or ignore the context. Only a limited amount of text fits in the prompt (the **context window**). It adds extra steps, cost, and delay, and the documents must be kept up to date.

## How Does RAG Work?
There are two phases: preparation (indexing) and question time.

### Preparation (Indexing)
1. Collect the documents.
2. Split them into small pieces called **chunks** (a small piece of a document).
3. Turn each chunk into an **embedding** (a list of numbers that captures the meaning of the text) using an **embedding model** (a model that converts text into embeddings).
4. Store the embeddings in a **vector database** (a searchable store of embeddings) so they can be searched by meaning.

### Question‑Time Steps
1. **Retrieve**: The user question is also turned into an embedding. The system finds the chunks whose meaning is most similar using **semantic search** (searching by meaning, not just keywords). Usually the top few (top‑k) chunks are taken.
2. **Augment**: The retrieved chunks are placed into the prompt together with the question and an instruction such as “answer using only this information”. The retrieved chunks become the **context** (the retrieved chunks placed in the prompt).
3. **Generate**: The LLM writes the answer from the question plus the retrieved context. It can also cite the sources it used.

Only the top few chunks are used; the LLM does not read every document.

## Example: College Scholarship Chatbot
**Setting:** A first‑year college student in Bhopal uses a chatbot on the college website to ask about the new merit‑scholarship rules.

**Question:** “What is the income limit for the merit scholarship this year?”

**Documents in the knowledge base:**
1. Scholarship Notice 2024: Family annual income must not exceed ₹2,50,000 for merit scholarship eligibility.
2. Hostel Fee Circular 2023: Hostel fees are ₹12,000 per semester for all students.
3. Exam Schedule 2024: Semester exams start on 15 November 2024.

**Retrieved chunk (by semantic search):**
> Scholarship Notice 2024: Family annual income must not exceed ₹2,50,000 for merit scholarship eligibility.

**Prompt sent to the LLM (augmented):**
```
Answer using only the information below.
Context: Scholarship Notice 2024: Family annual income must not exceed ₹2,50,000 for merit scholarship eligibility.
Question: What is the income limit for the merit scholarship this year?
```

**Answer without RAG (model guesses):**
> The income limit is ₹3,00,000 per year. (This is made up; the model guessed.)

**Answer with RAG (model uses the retrieved chunk):**
> According to the 2024 scholarship notice, the family annual income must not exceed ₹2,50,000.

## Key Words to Remember
- **large language model (LLM)**: an AI model trained on huge text that predicts the next token.
- **token**: a word or part of a word that the model reads or writes.
- **training data**: the text collection used to teach the model.
- **knowledge cutoff**: the date after which the model knows nothing.
- **hallucination**: a confident but wrong answer made up by the model.
- **retrieval**: finding the most relevant document pieces for a question.
- **augmented**: adding those pieces to the prompt.
- **generation**: the model writing the final answer.
- **embedding**: a list of numbers that represents the meaning of text.
- **vector database**: a searchable store of embeddings.
- **semantic search**: searching by meaning, not just keywords.
- **prompt**: the full text sent to the model, including question and context.
- **context**: the retrieved chunks placed in the prompt.
- **fine‑tuning**: extra training that changes the model weights.
- **weights**: the internal numbers the model learns during training.
- **retraining**: teaching the model again from scratch or on new data.

## Quick Check
1. What does RAG stand for?  
**Answer:** Retrieval‑Augmented Generation.

2. In RAG, which step comes first when a user asks a question?  
**Answer:** Retrieve.

3. Does RAG modify the model’s internal weights?  
**Answer:** No, RAG does not change the model weights.

4. Give one advantage of using RAG over fine‑tuning.  
**Answer:** RAG is cheaper and faster and lets you update knowledge by changing documents.

5. What is a key limitation of RAG?  
**Answer:** The answer quality depends on the relevance and correctness of the retrieved chunks.

## Summary
A large language model (LLM) generates text but has a knowledge cutoff, no private data, and can hallucinate.  
RAG (Retrieval‑Augmented Generation) adds a retrieval step before generation so the model answers from up‑to‑date or private documents.  
Documents are split into chunks, turned into embeddings, and stored in a vector database.  
At question time the system retrieves the best chunks, augments the prompt, and the LLM generates a grounded answer.  
RAG is cheaper and faster than retraining, but its quality depends on the retrieved chunks.
