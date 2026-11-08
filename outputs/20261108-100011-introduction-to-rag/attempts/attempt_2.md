# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn

In this lesson you will learn:
- What an **LLM (Large Language Model)** is and its limits.
- The full form of **RAG (Retrieval-Augmented Generation)** and what each word means.
- The three steps: **retrieve** (find information), **augment** (add to question), **generate** (write answer).
- How documents are prepared for search (split into chunks, turned into embeddings, stored in a vector database).
- Why RAG helps with fresh and private data.
- One key limitation of RAG.
- That RAG does not change the model.

## Before We Start: Some Basic Ideas

A **model** is a computer program that learns patterns from data.  
An **LLM (Large Language Model)** is a model trained on a huge amount of text. It learns to predict the next word.  
The text used to teach the model is called **training data**.  
The model’s knowledge stops at a fixed date. This date is called the **knowledge cutoff**. After that date the model knows nothing.  
The model does not know private information. For example, it does not know your college fee list or your company rules.  
Sometimes the model makes up an answer that sounds confident but is wrong. This is called **hallucination**.  
When you type a question to the model, that text is called a **prompt**.  
The model reads and writes in small pieces called **tokens**. A token can be a word or part of a word.

## What Is RAG?

**RAG** stands for **Retrieval-Augmented Generation**.  
- **Retrieval** means finding relevant pieces of information.  
- **Augmented** means adding those pieces to the question.  
- **Generation** means the LLM writes the answer using the added text.  

The idea was first published in a 2020 paper by Patrick Lewis and his team.

## An Everyday Analogy: Open-Book Exam

Think of a student in an open-book exam. The student is like the LLM. The textbook is like the vector database. When a question comes, the student first finds the right page in the book. This is **retrieval**. Then the student reads that page and writes the answer using only that information. This is **generation**. In a closed-book exam, the student must answer from memory alone, which can lead to mistakes. RAG works like the open-book student: it retrieves the relevant text first, then generates the answer.

## Why Does RAG Matter?

RAG gives several benefits:
- Answers can use up-to-date and private information.
- There are fewer made-up answers, though not zero.
- Answers can show sources so you can check them.
- You do not need to retrain the model. You just update the documents.
- It is cheaper and faster than fine-tuning the model.

## How Does RAG Work?

### Preparation (done once before questions arrive)

First, you collect your documents. For example, a college prospectus or a company policy.  
You split each document into small pieces. Each piece is called a **chunk**.  
You turn each chunk into a list of numbers that captures its meaning. This list is called an **embedding**.  
An **embedding model** creates these embeddings.  
You store the embeddings in a **vector database**. A **vector** is just a list of numbers. A vector database lets you search by meaning, not just by keywords.  
This preparation is also called indexing.

### Question-time steps (happen for every question)

**Step 1: Retrieve**  
The user asks a question. The system turns the question into an embedding. Then it does a **semantic search** in the vector database. Semantic search finds chunks whose meaning is closest to the question. The system picks the top few chunks (often called top‑k).

**Step 2: Augment**  
The system puts the retrieved chunks into the prompt together with the question. It also adds an instruction like “answer using only this information”. The retrieved text is now called the **context**.

**Step 3: Generate**  
The LLM reads the prompt (question + context + instruction) and writes the answer. The model’s **weights** (its internal learned numbers) do not change. Only the documents change.

**Fine‑tuning** is different. Fine‑tuning trains the model further on new examples and changes its weights. It is slower and costlier. RAG is usually the better first choice for giving a model new or changing facts.

## Example: College Fee Query

Riya, a 12th‑grade graduate from Bhopal, wants to know the fee for B.Sc. Computer Science at her college.

**Question:**  
What is the annual fee for B.Sc. Computer Science at Government College Bhopal?

**Documents in the vector database:**  
1. Government College Bhopal prospectus 2024: B.Sc. Computer Science fee ₹12,000 per year.  
2. Government College Bhopal prospectus 2023: B.Sc. Computer Science fee ₹10,000 per year.

**Retrieved chunk (top match):**  
Government College Bhopal prospectus 2024: B.Sc. Computer Science fee ₹12,000 per year.

**Prompt sent to the LLM (simplified):**  
> Context: Government College Bhopal prospectus 2024: B.Sc. Computer Science fee ₹12,000 per year.  
> Question: What is the annual fee for B.Sc. Computer Science at Government College Bhopal?  
> Instruction: Answer using only the context.

**Answer without RAG (plain LLM):**  
The fee is around ₹15,000 per year. (This is a hallucination.)

**Answer with RAG:**  
According to the 2024 prospectus, the fee is ₹12,000 per year.

## Key Words to Remember

model, LLM, training data, knowledge cutoff, hallucination, prompt, token, retrieval, chunk, embedding, vector, vector database, semantic search, context, augment, generate, fine‑tuning, weights

## Quick Check

1. What does RAG stand for?  
**Answer:** Retrieval‑Augmented Generation.

2. Which step comes first: retrieve or generate?  
**Answer:** Retrieve.

3. Does RAG change the model weights?  
**Answer:** No, the model weights stay the same.

4. What is a chunk?  
**Answer:** A small piece of a document used for search.

5. Name one limitation of RAG.  
**Answer:** The answer depends on the quality of the retrieved chunks.

## Summary

- An LLM learns from training data and has a knowledge cutoff.  
- It cannot see private data and may hallucinate.  
- RAG adds a retrieval step before generation so the model uses fresh or private documents.  
- Documents are split into chunks, turned into embeddings, and stored in a vector database.  
- At query time the system retrieves, augments the prompt, then generates.  
- RAG does not retrain the model; updating knowledge means updating documents.  
- Benefits: up-to-date answers, sources, lower cost. Limitation: answer quality depends on retrieval.
