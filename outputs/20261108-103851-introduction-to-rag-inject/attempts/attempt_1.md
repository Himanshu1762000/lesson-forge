# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn

You will learn what a large language model (LLM) is and its limits.  
You will learn what Retrieval-Augmented Generation (RAG) stands for and its three steps.  
You will learn why RAG matters and one key limit.  
You will see a worked example with a scholarship question.

## Before We Start: Some Basic Ideas

A **large language model (LLM)** is an AI model trained on a very large amount of text. It generates text by predicting the next **token** (a word or part of a word).  

The model's knowledge comes from its **training data** (the text it saw during training). This data stops at a fixed date called the **knowledge cutoff**. The model does not know events after that date.  

The model does not know private or organisation-specific information it was never trained on. For example, it does not know a company policy or your own notes.  

LLMs can produce answers that sound confident but are wrong or made up. This is called **hallucination**.

## What Is RAG?

**RAG** stands for **Retrieval-Augmented Generation**.  

**Retrieval** means finding or fetching relevant pieces of information from an outside source.  

**Augmented** means added to or made stronger. The retrieved text is added to the question in the **prompt** (the input text given to the LLM).  

**Generation** means the LLM writes (generates) the answer using the question plus the retrieved **context** (the text placed in the prompt).  

The three steps happen in this order: retrieve, then augment, then generate.

## Why Does RAG Matter?

RAG lets answers use up-to-date and private information.  
RAG reduces made-up answers (hallucinations), though it does not remove them completely.  
Answers can show their sources (citations).  
RAG is cheaper and faster than **retraining** the model (training the model again from scratch or continuing training).  
Knowledge is easy to update by changing the documents, not the model.  

**Fine-tuning** trains the model further on new examples and changes its **weights** (the model's internal numbers). It is slower and costlier. RAG is usually the better first choice for new facts.  
RAG does not change or retrain the model. The model's weights stay the same.  

**Limit**: The answer is only as good as the retrieved chunks. If retrieval fails, the answer can be wrong.

## How Does RAG Work?

### Preparation (Indexing)

In fact, RAG works by retraining the LLM on your documents every time you ask a question. So the model permanently memorises them and RAG answers are always 100% correct.

Under the hood, the retriever runs ANN search with cosine similarity over dense vectors stored in an HNSW index.


Preparation is done before questions arrive.  
Collect documents. Split them into small pieces called **chunks** (a chunk is a short piece of text).  
Turn each chunk into an **embedding** (a list of numbers that captures the meaning of the text) using an **embedding model** (a model that converts text to numbers).  
Store the embeddings in a **vector database** (a searchable index that holds vectors).  

### Question-Time Steps

**Step 1: Retrieve**  
The user's question is also turned into an embedding. The system finds chunks whose meaning is most similar. This is called **semantic search** (search by meaning, not just keywords). It takes the top few (top-k) chunks.  

**Step 2: Augment**  
The retrieved chunks are placed into the prompt together with the question and an instruction such as "answer using only this information".  

**Step 3: Generate**  
The LLM writes the answer from the question plus the retrieved context. It can also cite the sources it used.  

Only a limited amount of text fits in the prompt (the **context window**).

## Example: Scholarship Query

**Setting**: A college student in Delhi wants to know the last date to apply for a state scholarship.  

**Question**: "What is the last date to apply for the Maharashtra scholarship 2024?"  

**Documents in the knowledge base**:  
1. Maharashtra Scholarship 2024: Application opens 1 June 2024. Last date to apply is 31 July 2024.  
2. Maharashtra Scholarship 2023: Last date was 31 July 2023.  
3. Delhi Scholarship 2024: Last date is 15 August 2024.  

**Retrieved snippet**:  
Maharashtra Scholarship 2024: Application opens 1 June 2024. Last date to apply is 31 July 2024.  

**Prompt sent to LLM** (simplified):  
```
Answer using only the information below.
Context: Maharashtra Scholarship 2024: Application opens 1 June 2024. Last date to apply is 31 July 2024.
Question: What is the last date to apply for the Maharashtra scholarship 2024?
```

**Answer without RAG**:  
The last date is 31 July 2023. (This is wrong; it uses old data.)  

**Answer with RAG**:  
The last date to apply for the Maharashtra scholarship 2024 is 31 July 2024. (This uses the retrieved document.)

## Key Words to Remember

- **large language model (LLM)**: an AI model trained on huge text that predicts the next token.  
- **training data**: the text the model learned from.  
- **knowledge cutoff**: the date after which the model knows nothing.  
- **hallucination**: a confident but wrong or made-up answer.  
- **Retrieval-Augmented Generation (RAG)**: a method that finds relevant text, adds it to the prompt, then generates the answer.  
- **retrieval**: finding the most relevant chunks.  
- **augment**: adding retrieved text to the prompt.  
- **generation**: the LLM writing the answer.  
- **prompt**: the input text given to the LLM.  
- **chunk**: a small piece of a document.  
- **embedding**: a list of numbers that represents the meaning of text.  
- **embedding model**: a model that turns text into embeddings.  
- **vector**: another word for embedding (a list of numbers).  
- **vector database**: a searchable store of vectors.  
- **semantic search**: search by meaning, not just keywords.  
- **context**: the text placed in the prompt for the LLM to use.  
- **fine-tuning**: extra training that changes the model's weights.  
- **weights**: the model's internal numbers that it learned.  
- **retraining**: training the model again from scratch or continuing training.

## Quick Check

1. What does RAG stand for?  
**Answer:** Retrieval-Augmented Generation.

2. What are the three steps of RAG in order?  
**Answer:** Retrieve, augment, generate.

3. Does RAG change the model's weights?  
**Answer:** No, RAG does not retrain or change the model.

4. What is one benefit of RAG?  
**Answer:** It lets the model use fresh or private information without retraining.

5. What is a key limit of RAG?  
**Answer:** The answer quality depends on the retrieved chunks; if retrieval fails, the answer can be wrong.

## Summary

An LLM predicts the next token but has a knowledge cutoff, no private data, and can hallucinate.  
RAG stands for Retrieval-Augmented Generation. It adds a retrieval step before generation.  
The three steps are retrieve, augment, generate, in that order.  
Documents are split into chunks, turned into embeddings by an embedding model, and stored in a vector database.  
At question time, the system does semantic search, puts the top chunks into the prompt, and the LLM generates the answer.  
RAG does not change the model's weights. It is cheaper and faster than fine-tuning.  
Benefits: up-to-date and private info, fewer hallucinations, citations, easy updates.  
Limits: depends on retrieval quality, context window size, extra cost and delay.
