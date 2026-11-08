# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn

After this lesson you will be able to:
- Explain what a Large Language Model (LLM) is and its limits.
- Define Retrieval-Augmented Generation (RAG) and each word in the name.
- Describe the three question-time steps: retrieve, augment, generate.
- List two benefits and one limitation of RAG.

## Before We Start: Some Basic Ideas

Artificial intelligence (AI) is a computer system that can do tasks that usually need human intelligence. A **Large Language Model (LLM)** is an AI model trained on a very large amount of text. It generates text by predicting the next **token** (a word or part of a word). Examples are the models behind ChatGPT, Gemini, and Claude.

An LLM has three main limits.

First, it has a **knowledge cutoff**. Its training data stops at a fixed date. It does not know events after that date.

Second, it does not know private or organisation-specific information it was never trained on. For example, it does not know your college fee list or your company policy.

Third, an LLM can produce answers that sound confident but are wrong or made up. This is called **hallucination**.

## What Is RAG?

**RAG (Retrieval-Augmented Generation)** is a method that helps an LLM use fresh or private information. The name has three words.

**Retrieval** means finding and fetching relevant pieces of information from an outside source.

**Augmented** means added to or made stronger. The retrieved text is added to the question in the prompt.

**Generation** means the LLM writes the answer using the question plus the retrieved context.

RAG does not change or retrain the model. The model's weights (its learned internal numbers) stay the same.

## Why Does RAG Matter?

RAG matters because it solves the three limits of a plain LLM.

RAG lets the LLM use up-to-date and private information. You just add new documents to the knowledge base.

RAG reduces made-up answers (hallucinations), though it does not remove them completely.

Answers can show their sources, so you can check them.

RAG is cheaper and faster than **retraining** (teaching the model again from scratch) or **fine-tuning** (training the model further on new examples, which changes its weights). Fine-tuning is slower, costlier, and mainly used to change style or behaviour.

Knowledge is easy to update by changing the documents, not the model.

One limitation: the answer is only as good as the retrieved chunks. If the search returns wrong or outdated chunks, the answer can be wrong. The LLM can still hallucinate or ignore the context. Also, only a limited amount of text fits in the prompt (the **context window**).

## How Does RAG Work?

RAG has two phases: preparation (done once) and question-time (done for each question).

### Preparation (Indexing)

Before any question arrives, we prepare the knowledge base.

1. Collect the documents (PDFs, web pages, text files).
2. Split them into small pieces called **chunks** (a small piece of a document).
3. Turn each chunk into an **embedding** (a list of numbers that captures the meaning of text) using an **embedding model** (a tool that turns text into embeddings).
4. Store the embeddings in a **vector database** (a searchable store of vectors). A **vector** is a list of numbers representing data.

### Question-Time Steps

When a user asks a question, three steps happen in order.

**Step 1: Retrieve.** The user's question is also turned into an embedding. The system finds the chunks whose meaning is most similar. This is called **semantic search** (search by meaning, not just keywords). Usually the top few (top-k) chunks are taken.

**Step 2: Augment.** The retrieved chunks are placed into the prompt together with the question and an instruction such as "answer using only this information".

**Step 3: Generate.** The LLM writes the answer from the question plus the retrieved context. It can also cite the sources it used.

## Example: College Hostel Fee Chatbot

**Setting:** A college student in Bhopal uses a chatbot on the college website.

**Question:** "What is the hostel fee for first-year B.Sc students this year?"

**Documents in the knowledge base:**
1. Hostel Fee Notice 2024-25: First-year B.Sc hostel fee is ₹45,000 per year, payable in two instalments.
2. Hostel Fee Notice 2023-24: First-year B.Sc hostel fee was ₹40,000 per year.
3. Mess Menu: Monday breakfast is poha and tea.

**Retrieved snippet (Step 1):**  
Hostel Fee Notice 2024-25: First-year B.Sc hostel fee is ₹45,000 per year, payable in two instalments.

**Prompt sent to LLM (Step 2 - Augment):**  
```
Answer using only the information below.

Context: Hostel Fee Notice 2024-25: First-year B.Sc hostel fee is ₹45,000 per year, payable in two instalments.

Question: What is the hostel fee for first-year B.Sc students this year?
```

**Answer with RAG (Step 3 - Generate):**  
According to the 2024-25 notice, the hostel fee for first-year B.Sc students is ₹45,000 per year, payable in two instalments.

**Answer without RAG (plain LLM):**  
The hostel fee for first-year B.Sc students is ₹40,000 per year. (This is wrong because the LLM's knowledge cutoff is before 2024-25.)

## Key Words to Remember

- **Large Language Model (LLM)**: an AI model trained on huge text that predicts the next token.
- **Knowledge cutoff**: the date after which the LLM knows nothing.
- **Hallucination**: a confident but wrong or made-up answer.
- **Retrieval-Augmented Generation (RAG)**: a method that retrieves relevant text, adds it to the prompt, then generates the answer.
- **Chunk**: a small piece of a document.
- **Embedding**: a list of numbers that captures the meaning of text.
- **Embedding model**: a tool that turns text into embeddings.
- **Vector**: a list of numbers representing data.
- **Vector database**: a searchable store of vectors.
- **Semantic search**: search by meaning, not just keywords.
- **Context window**: the limited amount of text the model can read at once.
- **Fine-tuning**: training the model further on new examples, which changes its weights.
- **Retraining**: teaching the model again from scratch or continuing training, which changes its weights.

## Quick Check

1. What are the three limits of a plain LLM?  
**Answer:** Knowledge cutoff, no private data, hallucination.

2. What does RAG stand for?  
**Answer:** Retrieval-Augmented Generation.

3. What are the three question-time steps in order?  
**Answer:** Retrieve, augment, generate.

4. Does RAG change the model's weights?  
**Answer:** No, RAG does not change the model's weights. The model stays the same.

5. Name one benefit and one limitation of RAG.  
**Answer:** Benefit: uses fresh or private data. Limitation: answer depends on quality of retrieved chunks.

## Summary

A Large Language Model (LLM) predicts the next token but has a knowledge cutoff, lacks private data, and can hallucinate. Retrieval-Augmented Generation (RAG) adds a retrieval step before generation so the LLM uses fresh or private information. The three steps are retrieve, augment, generate, in that order. RAG does not retrain the model; it only changes the documents in the knowledge base. Benefits: up-to-date answers, fewer hallucinations, sources shown. Limitation: the answer is only as good as the retrieved chunks.
