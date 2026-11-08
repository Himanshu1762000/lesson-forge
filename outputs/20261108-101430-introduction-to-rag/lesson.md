> **NOT SHIPPED - needs human review.** The lesson did not clear every check within the retry budget. Failing checks: ACRONYMS, DEFINED_BEFORE_USE, JARGON. This is the best attempt.

# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn

In this lesson you will learn:
- What an LLM (Large Language Model) is and what its limits are.
- What RAG stands for and what each word means.
- The three steps of RAG: retrieve, augment, generate.
- How knowledge is prepared by splitting documents into small pieces and turning them into numbers that capture meaning.
- Why RAG helps and one key limit.

## Before We Start: Some Basic Ideas

A **model** is a computer program that learns patterns from data.

An **LLM (Large Language Model)** is a model trained on a huge amount of text. It predicts the next **token** (a word or part of a word) to generate text. Examples are the models behind ChatGPT, Gemini, Claude, and Llama.

**Training data** is the text used to teach the LLM. The LLM's knowledge stops at a fixed date called the **knowledge cutoff**. It does not know events after that date.

The LLM does not know private or organisation-specific information it was never trained on. For example, it does not know your college fee list or a company policy.

LLMs can produce answers that sound confident but are wrong or made up. This is called **hallucination**.

A **prompt** is the text you give to the LLM to start its answer. A **token** is a word or part of a word that the LLM reads or writes.

## What Is RAG?

**RAG** stands for **Retrieval-Augmented Generation**. The term was introduced in a 2020 research paper by Patrick Lewis and colleagues at Meta.

**Retrieval** means finding or fetching relevant pieces of information from an outside source.

**Augmented** means added to or made stronger. The retrieved text is added to the question in the prompt.

**Generation** means the LLM writes the answer using the question plus the retrieved text.

Think of an open-book exam. A closed-book student answers only from memory. An open-book student first finds the right page in the book, then writes the answer using that page. Finding the right page is **retrieval**. Writing the answer using that page is **generation**. The book is the outside knowledge source.

## Why Does RAG Matter?

RAG lets the LLM use up-to-date and private information.

It reduces made-up answers (hallucinations), though it does not remove them completely.

Answers can show their sources so you can check them.

It is cheaper and faster than **retraining** (teaching the model again from scratch). Knowledge is easy to update by changing the documents, not the model.

**Fine-tuning** trains the model further on new examples and changes its **weights** (the model's internal numbers that store what it learned). It is slower, costlier, and mainly used to change style or behaviour. RAG is usually the better first choice for new or changing facts.

One limit: the answer is only as good as what is retrieved. If the search returns wrong or outdated chunks, the answer can be wrong. The LLM can still hallucinate or ignore the context. Also, only a limited amount of text fits in the prompt (the **context window**, which is the maximum amount of text the LLM can take at once). RAG adds extra steps, cost, and delay, and the documents must be kept up to date.

## How Does RAG Work?

### Preparation (Indexing)

**Indexing** is the process of preparing documents so they can be searched quickly. Preparation is done before questions arrive:
1. Collect documents.
2. Split them into small pieces called **chunks** (a small piece of a document).
3. Turn each chunk into an **embedding** (a list of numbers that captures the meaning of the text) using an **embedding model** (a tool that turns text into embeddings).
4. Store them in a **vector database** (a searchable index for vectors). A **vector** is a list of numbers that represents meaning.

**Semantic search** finds chunks whose meaning is most similar to the question.

### Question-Time Steps

When a user asks a question, three steps happen:

1. **Retrieve**: The user's question is turned into an embedding. The system finds the top few chunks with the most similar meaning (semantic search). Keyword search or a mix can also be used.
2. **Augment**: The retrieved chunks are placed into the prompt together with the question and an instruction like "answer using only this information". This combined text is called the **context**.
3. **Generate**: The LLM writes the answer from the question plus the retrieved context. It can also cite the sources it used.

RAG does not change or retrain the model. The model's weights stay the same. To update knowledge you update the documents.

## Example: College Scholarship Chatbot

**Setting**: A college student in Delhi asks a chatbot on the college website about the Prime Minister (PM) Scholarship 2024 last date.

**Question**: "What is the last date to apply for the PM Scholarship 2024?"

**Documents in the knowledge base**:
- PM Scholarship 2024: Application opens 1 July 2024. Last date to apply is 31 October 2024. Apply on the National Scholarship Portal.
- PM Scholarship 2023: Last date was 31 October 2023. The scheme is for students of armed forces families.
- College notice: The college office will help students fill the form until 25 October 2024.

**Retrieved snippet**: PM Scholarship 2024: Application opens 1 July 2024. Last date to apply is 31 October 2024. Apply on the National Scholarship Portal.

**Prompt sent to LLM** (simplified):
```
Answer using only this information:
PM Scholarship 2024: Application opens 1 July 2024. Last date to apply is 31 October 2024. Apply on the National Scholarship Portal.

Question: What is the last date to apply for the PM Scholarship 2024?
```

**Answer without RAG**: The plain LLM guesses a wrong date and wrong portal (hallucination). Example: "The last date is 31 December 2024. You can apply on any government website."

**Answer with RAG**: The correct date and portal, with a source citation. Example: "The last date to apply for PM Scholarship 2024 is 31 October 2024. You must apply on the National Scholarship Portal. (Source: PM Scholarship 2024 document)"

## Key Words to Remember

- **model**: a computer program that learns patterns from data
- **LLM**: Large Language Model, a model trained on huge text to predict next token
- **training data**: the text used to teach the LLM
- **knowledge cutoff**: the date after which the LLM knows nothing
- **hallucination**: a confident but wrong or made-up answer
- **prompt**: the text you give to the LLM to start its answer
- **token**: a word or part of a word the LLM reads or writes
- **RAG**: Retrieval-Augmented Generation
- **retrieval**: finding relevant pieces of information
- **augmented**: added to the prompt to make it stronger
- **generation**: the LLM writing the answer
- **fine-tuning**: training the model further to change its weights
- **weights**: the model's internal numbers that store what it learned
- **chunk**: a small piece of a document
- **embedding**: a list of numbers that captures the meaning of text
- **embedding model**: a tool that turns text into embeddings
- **vector**: a list of numbers that represents meaning
- **vector database**: a searchable index that stores vectors
- **semantic search**: finding chunks by meaning similarity, not just keywords
- **context**: the retrieved chunks plus the question placed in the prompt
- **indexing**: the process of preparing documents so they can be searched quickly
- **retraining**: teaching the model again from scratch
- **context window**: the maximum amount of text the LLM can take at once

## Quick Check

1. What does LLM stand for?
**Answer:** Large Language Model.

2. What are the three steps of RAG in order?
**Answer:** Retrieve, Augment, Generate.

3. Does RAG change the model's weights?
**Answer:** No, RAG does not change the model's weights. The model stays the same.

4. What is a chunk?
**Answer:** A small piece of a document created during preparation.

5. Why might a RAG answer still be wrong?
**Answer:** If the search returns the wrong or outdated chunks, or if the LLM ignores the context, the answer can be wrong.

## Summary

- An LLM generates text from memory but has a knowledge cutoff, no private data, and can hallucinate.
- RAG (Retrieval-Augmented Generation) adds an outside knowledge source. It retrieves relevant chunks, augments the prompt, and generates the answer.
- Knowledge is prepared by splitting documents into chunks, turning them into embeddings (vectors), and storing them in a vector database.
- RAG gives up-to-date, private information, shows sources, and avoids retraining. But the answer depends on the quality of retrieved chunks, and the LLM can still hallucinate.
- RAG does not change the model's weights. Fine-tuning does, but it is slower and costlier.
