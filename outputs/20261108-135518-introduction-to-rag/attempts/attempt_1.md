# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn
- You will learn what a large language model (LLM) is.  
- You will learn the limits of an LLM such as knowledge cutoff and no private data.  
- You will learn that LLMs can hallucinate.  
- You will learn what RAG stands for.  
- You will learn the three steps: retrieve, augment, generate.  
- You will learn benefits like fresh data and sources.  
- You will learn one limitation about retrieval quality.

## Before We Start: Some Basic Ideas
A **large language model (LLM)** is an AI model trained on a huge amount of text. It predicts the next **token** (a word or part of a word).  
Its knowledge stops at a fixed date called the **knowledge cutoff**. It does not know events after that date.  
It also does not know private or organisation data it never saw during training.  
Sometimes an LLM gives a confident but wrong answer. This is called **hallucination**.

## What Is RAG?
**RAG (Retrieval-Augmented Generation)** is a method that adds a search step before the LLM answers.  
- **Retrieval** means finding relevant pieces of information.  
- **Augmented** means adding those pieces to the prompt.  
- **Generation** means the LLM writes the answer using the added pieces.  
RAG does not change the model weights. The model stays the same.

## Why Does RAG Matter?
- Answers can use up‑to‑date information.  
- Answers can use private or organisation data.  
- Fewer made‑up answers, though not zero.  
- Answers can show sources.  
- It is cheaper and faster than **retraining** (training the model again from scratch) or **fine‑tuning** (extra training that changes model weights).  
- Knowledge is easy to update by changing the **documents** (the text files you store).  

**Limitation:** The answer is only as good as the retrieved pieces. If the search returns a wrong or old chunk, the answer can be wrong. The LLM can still hallucinate or ignore the context. Only a limited amount of text fits in the **context window** (the maximum text the model can see at once).

## How Does RAG Work?
### Preparation (done once)
1. Collect the **documents** you want the system to know.  
2. Split each document into small pieces called **chunks** (a small piece of a document).  
3. Turn each chunk into an **embedding** (a list of numbers that captures the meaning of the text) using an **embedding model** (a model that converts text to numbers).  
4. Store the embeddings in a **vector database** (an index that stores embeddings for fast search). A **vector** is just a list of numbers.

### Question time (three steps)
1. **Retrieve:** The user question is also turned into an embedding. The system finds the chunks whose meaning is most similar. This is semantic search. Usually the top few chunks are taken.  
2. **Augment:** The retrieved chunks are placed into the prompt together with the question and an instruction such as “answer using only this information”.  
3. **Generate:** The LLM writes the answer from the prompt. It can also cite the sources it used.  

The LLM weights stay the same. This is different from **fine‑tuning**, which changes the weights. RAG is usually the better first choice for giving a model new or changing facts.

## Example: College Scholarship Query
**Setting:** A student in Delhi uses a chatbot on the college website.  
**Question:** “What is the last date to apply for the PM Scholarship 2024?”  

**Documents in the knowledge base**  
- PM Scholarship 2024: Application opens 1 Jan 2024, closes 31 March 2024.  
- Eligibility: Indian citizens, family income below 8 lakh.  
- Contact: email scholarships@gov.in  

**Retrieved chunk**  
> PM Scholarship 2024: Application opens 1 Jan 2024, closes 31 March 2024.  

**Prompt sent to the LLM (augmented)**  
```
Use the information below to answer.
Information: PM Scholarship 2024: Application opens 1 Jan 2024, closes 31 March 2024.
Question: What is the last date to apply for the PM Scholarship 2024?
Answer:
```

**Answer without RAG (plain LLM)**  
The last date is 30 June 2024.  *(This is a hallucination.)*  

**Answer with RAG**  
The last date to apply is 31 March 2024, according to the official scheme document.  

The RAG answer uses the retrieved chunk and cites the source. The plain LLM guessed a wrong date.

## Key Words to Remember
- **LLM**: large language model, predicts the next token.  
- **Token**: a word or part of a word.  
- **Knowledge cutoff**: date after which the model knows nothing.  
- **Hallucination**: confident but wrong answer.  
- **RAG**: retrieval‑augmented generation.  
- **Retrieval**: finding relevant chunks.  
- **Augment**: adding chunks to the prompt.  
- **Generation**: LLM writes the answer.  
- **Chunk**: small piece of a document.  
- **Embedding**: list of numbers representing meaning.  
- **Vector database**: index that stores embeddings for fast search.  
- **Fine‑tuning**: extra training that changes model weights.  
- **Context window**: maximum text the model can see at once.

## Quick Check
1. What does RAG stand for?  
**Answer:** Retrieval‑Augmented Generation.  

2. Which step comes first: retrieve or generate?  
**Answer:** Retrieve.  

3. Does RAG change the model weights?  
**Answer:** No, RAG does not change the model weights.  

4. Name one benefit of RAG.  
**Answer:** It lets the model use up‑to‑date or private information.  

5. What happens if the retrieved chunk is wrong?  
**Answer:** The answer can be wrong because the model relies on that chunk.

## Summary
- An LLM predicts tokens but has a knowledge cutoff and can hallucinate.  
- RAG adds a retrieval step before generation so the model uses fresh or private data.  
- Preparation builds a vector database of chunk embeddings.  
- At query time the system retrieves, augments, then generates.  
- RAG does not retrain the model; it is cheaper and easier to update.  
- The answer quality depends on the quality of retrieved chunks.
