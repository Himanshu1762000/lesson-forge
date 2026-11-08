# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn

In this lesson you will learn:
- What a large language model (LLM) is and why it can give wrong answers.
- What RAG (Retrieval-Augmented Generation) means and what each word in the name does.
- The three steps that happen when you ask a question in a RAG system.
- One benefit and one limitation of RAG.

## Before We Start: Some Basic Ideas

A **large language model (LLM)** is an **artificial intelligence (AI)** model trained on a very large amount of text. A **model** is a computer program that has learned patterns from data. It learns to predict the next **token** (a word or part of a word). Examples are the models behind ChatGPT, Gemini, and Claude.

The **training data** is the collection of text the model learned from. This data stops at a certain date. That date is called the **knowledge cutoff**. The model knows nothing after that date.

The model also does not know private information. For example, it does not know your college fee list or your company policy.

Sometimes the model makes up facts that sound real. This is called **hallucination**.

When you talk to the model, you give it a **prompt**. The prompt is the input text you type to get an answer.

## What Is RAG?

**RAG (Retrieval-Augmented Generation)** is a method that helps an LLM give better answers. The name has three parts:

- **Retrieval** means finding relevant pieces of information from a knowledge source.
- **Augmented** means adding those pieces to the prompt.
- **Generation** means the LLM writes the final answer using the augmented prompt.

Think of an open‑book exam. A student first looks up the right page in the textbook. That is **retrieval**. Then the student writes the answer using that page. That is **generation**.

## Why Does RAG Matter?

RAG helps in several ways:
- Answers can use up‑to‑date information. The model does not need to know the fact during training.
- Answers can use private documents. For example, a company policy or a college prospectus.
- The answer can show its sources. You can see which document the answer came from.
- RAG reduces the chance of making up answers because the model grounds its response in retrieved documents.
- You do not need to **retrain** the model. Retraining means teaching the model again from scratch. It changes the model’s **weights** (the internal numbers the model learned). RAG only updates the documents.
- RAG is cheaper and faster than **fine‑tuning**. Fine‑tuning is extra training that changes the model weights to change style or behaviour.

But RAG has limits. The answer is only as good as the chunks retrieved. A **chunk** is a small piece of a document, like a paragraph. If the search returns wrong or old chunks, the answer can be wrong. The model can still hallucinate or ignore the context. Also, only a limited amount of text fits in the prompt. This limit is called the **context window**.

## How Does RAG Work?

RAG has two phases: preparation and question time.

### Preparation (done once before questions arrive)

1. Collect the documents you want the system to know.
2. Split each document into small pieces called **chunks**. A **chunk** is a small piece of a document, like a paragraph.
3. Turn each chunk into an **embedding** using an **embedding model**. An **embedding model** turns text into a list of numbers that capture the meaning of the text. That list of numbers is called an **embedding** or a **vector**.
4. Store the embeddings in a **vector database**. A **vector database** holds embeddings for fast search.

### Question time (three steps)

**Step 1: Retrieve**  
The user asks a question. The system turns the question into an embedding. Then it does a **semantic search**. Semantic search finds chunks whose meaning matches the question. It picks the top few chunks (top‑k).

**Step 2: Augment**  
The system places the retrieved chunks into the prompt. It adds an instruction like “Answer using only this information.”

**Step 3: Generate**  
The LLM reads the prompt and writes the answer. It can also cite the sources it used.

Only a limited amount of text fits in the prompt. That limit is the **context window**.

## Example: College Scholarship Chatbot

**Setting:** A student in Delhi uses a chatbot to check scholarship deadlines.

**Question:** “What is the last date to apply for the National Scholarship 2024?”

**Documents stored in the knowledge base:**
1. National Scholarship 2024 applications close on 31 October 2024.
2. Eligibility requires 60% marks in 12th grade.
3. Apply online at scholarships.gov.in.

**Retrieval:** The system finds the first document because it matches the question.

**Without RAG:** The LLM answers from its training data. It might say: “The last date is 15 September 2023.” That is a hallucination.

**With RAG:** The prompt sent to the LLM looks like this:

> Context: National Scholarship 2024 applications close on 31 October 2024.  
> Question: What is the last date to apply for the National Scholarship 2024?  
> Instruction: Answer using only the context.

**Answer with RAG:** “The last date to apply is 31 October 2024, according to the official scholarship notice.”

The answer is correct and cites the source.

## Key Words to Remember

- **large language model (LLM)**: AI that predicts the next token from huge text.
- **training data**: Text used to teach the model.
- **knowledge cutoff**: Date after which the model knows nothing.
- **hallucination**: Model makes up false facts.
- **prompt**: Input text you give the model.
- **token**: Word or part of a word.
- **retrieval**: Finding relevant chunks.
- **augmented**: Adding chunks to the prompt.
- **generation**: Model writes the answer.
- **RAG (Retrieval-Augmented Generation)**: Method that retrieves, augments, then generates.
- **embedding model**: Turns text into meaning numbers.
- **embedding**: The meaning numbers.
- **vector**: Same as embedding.
- **chunk**: Small document piece.
- **vector database**: Stores embeddings for search.
- **semantic search**: Search by meaning.
- **context window**: Max text the prompt can hold.
- **fine‑tuning**: Extra training that changes model weights.
- **weights**: Internal numbers the model learns.
- **retraining**: Teaching the model again from scratch.

## Quick Check

1. What does RAG stand for?  
**Answer:** Retrieval-Augmented Generation.

2. Which step comes first at question time: retrieve, augment, or generate?  
**Answer:** Retrieve.

3. Does RAG change the model’s weights?  
**Answer:** No, RAG does not change the model weights.

4. Give one limitation of RAG.  
**Answer:** The answer depends on the quality of the retrieved chunks.

## Summary

- An LLM knows only its training data and can hallucinate.
- RAG adds a retrieval step so the model uses fresh or private documents.
- The three steps are retrieve, augment, generate, in that order.
- Documents are split into chunks, turned into embeddings, and stored in a vector database.
- RAG gives sourced, up‑to‑date answers without retraining the model.
- The answer is only as good as the chunks retrieved.
