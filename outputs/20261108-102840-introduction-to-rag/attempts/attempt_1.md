# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn
- You will explain what a large language model (LLM) is and its limits.
- You will define RAG and its three steps in order.
- You will describe how documents are prepared for RAG search.
- You will list two benefits and one limitation of RAG.

## Before We Start: Some Basic Ideas
A **large language model (LLM)** is a computer program that has read a huge amount of text. It can write like a human. The text it read during learning is called **training data**. The LLM knows nothing after a fixed date. This date is called the **knowledge cutoff**. The LLM does not know private information like your college fee list. Sometimes the LLM makes up answers that sound true but are false. This is called **hallucination**.

A **model** is a computer program that learns patterns from data. A **token** is a word or part of a word that the LLM reads and writes. A **prompt** is the text you send to the LLM to get an answer.

## What Is RAG?
**RAG (Retrieval-Augmented Generation)** stands for three words.
- **Retrieval** means finding relevant information from an outside knowledge source.
- **Augmented** means adding that information to the question in the prompt.
- **Generation** means the LLM writes the answer using the question plus the added information.

RAG does not change the model's **weights** (the internal numbers of the model that change during training). The model stays the same.

## Why Does RAG Matter?
RAG lets the LLM use up-to-date and private information. RAG reduces made-up answers but does not remove them completely. RAG can show the sources it used. RAG is cheaper and faster than **retraining** (teaching the model again on new data).

**Fine-tuning** trains the model further on new examples and changes its weights. It is slower and costlier. RAG is usually the better first choice for giving a model new or changing facts.

One limitation: the answer is only as good as the retrieved **chunks** (small pieces of a document). If the search returns wrong or old chunks, the answer can be wrong.

## How Does RAG Work?
### Preparation (done once before questions arrive)
1. Collect **documents** (pieces of text like PDFs or web pages).
2. Split each document into small pieces called **chunks**.
3. Turn each chunk into an **embedding** (a list of numbers that represents the meaning of the text) using an **embedding model** (a program that turns text into embeddings).
4. Store the embeddings in a **vector database** (a special database that stores embeddings and can search by meaning).

A **vector** is the same as an embedding: a list of numbers that represents meaning. **Semantic search** means searching by meaning, not just keywords.

### Question-time steps
**Step 1 – Retrieve:** The user's question is turned into an embedding. The system finds the top chunks with the most similar meaning.
**Step 2 – Augment:** The retrieved chunks are placed into the prompt together with the question and an instruction like "answer using only this information". The added information is called **context**.
**Step 3 – Generate:** The LLM writes the answer from the question plus the retrieved context. It can cite the sources.

## Example: College Scholarship Chatbot
**Setting:** A college student in Delhi uses a chatbot on the college website.

**Question:** "What is the last date to apply for the XYZ scholarship?"

**Documents in the knowledge base:**
1. The XYZ scholarship application opens on 1st June 2024 and closes on 31st July 2024.
2. Eligibility: Students with 80% marks in 12th grade.
3. Contact: scholarship@college.edu

**Retrieved snippet:** The XYZ scholarship application opens on 1st June 2024 and closes on 31st July 2024.

**Prompt sent to LLM (augmented):**
> Context: The XYZ scholarship application opens on 1st June 2024 and closes on 31st July 2024.
> Question: What is the last date to apply for the XYZ scholarship?
> Instruction: Answer using only the context.

**Answer without RAG:** The last date is 31st December 2023. (This is a hallucination from old training data.)

**Answer with RAG:** The last date to apply is 31st July 2024, according to the scholarship notice.

## Key Words to Remember
- **large language model (LLM)**: a computer program that has read a huge amount of text and can write like a human.
- **training data**: the text the LLM read during its learning.
- **knowledge cutoff**: the date after which the LLM knows nothing new.
- **hallucination**: when the LLM makes up answers that sound true but are false.
- **model**: a computer program that learns patterns from data.
- **token**: a word or part of a word that the LLM reads and writes.
- **prompt**: the text you send to the LLM to get an answer.
- **retrieval**: finding relevant information from a knowledge source.
- **augment**: adding that information to the question in the prompt.
- **generation**: the LLM writing the answer using the question plus the added information.
- **fine-tuning**: training the model further on new examples to change its behaviour.
- **weights**: the internal numbers of the model that change during training.
- **document**: a piece of text like a PDF or web page.
- **chunk**: a small piece of a document.
- **embedding**: a list of numbers that represents the meaning of text.
- **embedding model**: a program that turns text into embeddings.
- **vector**: same as embedding, a list of numbers that represents meaning.
- **vector database**: a special database that stores embeddings and can search by meaning.
- **semantic search**: searching by meaning, not just keywords.
- **context**: the information given to the LLM along with the question.

## Quick Check
1. What does RAG stand for?  
**Answer:** Retrieval-Augmented Generation.

2. What are the three steps of RAG in order?  
**Answer:** Retrieve, Augment, Generate.

3. Does RAG change the model's weights?  
**Answer:** No, the model stays the same.

4. Name one benefit of using RAG.  
**Answer:** It lets the LLM use up-to-date or private information.

5. What is one limitation of RAG?  
**Answer:** The answer is only as good as the retrieved chunks.

## Summary
A plain LLM has a knowledge cutoff, no private data, and can hallucinate. RAG adds a retrieval step before generation so the LLM uses fresh, relevant information. Documents are split into chunks, turned into embeddings, and stored in a vector database. At question time the system retrieves the best chunks, augments the prompt, and generates the answer. RAG does not retrain the model; it is cheaper and faster than fine-tuning. The answer quality depends on the quality of the retrieved chunks.
