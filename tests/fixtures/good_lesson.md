# Introduction to RAG (Retrieval-Augmented Generation)

## What You Will Learn

- What a chat AI is and where it makes mistakes.
- How a computer can look up the right notes before it answers.
- Why this helps, and what can still go wrong.

## Before We Start: Some Basic Ideas

AI (Artificial Intelligence) means a computer that does tasks that need thinking.
An LLM (Large Language Model) is an AI that learns from a huge amount of text.
That text is called **training data**.
The model reads text in small parts. Each part is called a **token**.
The model stops learning on one date. This date is the **knowledge cutoff** (the last day of its learning).
Sometimes the model makes up an answer. This is a **hallucination** (a confident but wrong answer).
The words you type to the model are called a **prompt**.

## What Is RAG?

RAG (Retrieval-Augmented Generation) means the computer first finds the right notes.
Then it adds them to your question. Then the model writes the answer.
Think of an open-book exam. You find the page first. Then you write the answer.

## Why Does RAG Matter?

The model can use new and private facts.
It makes fewer made-up answers, but not zero.
If the search finds the wrong page, the answer can still be wrong.

## How Does RAG Work?

First, we cut each document into small parts. Each part is a **chunk** (a small piece of a document).
Each chunk becomes an **embedding** (a list of numbers that shows its meaning).
We keep them in a **vector database** (a store that can search by meaning).
When you ask, the computer finds the closest chunks. Then it adds them to the prompt.
Then the model writes the answer. The model itself does not change.

## Example: College Fee Question

Riya asks: "What is the hostel fee this year?"
The search finds: "Hostel fee for 2024 is 40,000 rupees per year."
The prompt now has the question and this line.
The model answers: "The hostel fee is 40,000 rupees per year."

## Key Words to Remember

- **training data**: the text the model learned from
- **token**: a small part of text
- **knowledge cutoff**: the last day of learning
- **hallucination**: a confident but wrong answer
- **prompt**: the words you give the model
- **chunk**: a small piece of a document
- **embedding**: numbers that show meaning
- **vector database**: a store that searches by meaning

## Quick Check

1. What does RAG do first?
**Answer:** It finds the right notes.

2. Does RAG change the model?
**Answer:** No. Only the notes change.

3. Can RAG still be wrong?
**Answer:** Yes, if it finds the wrong notes.

## Summary

RAG finds notes, adds them to the question, and then writes the answer.
