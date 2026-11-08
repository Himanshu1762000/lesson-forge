# Reference Sheet: Retrieval-Augmented Generation (RAG)

This sheet is the ground truth the evaluator uses for the "accurate & grounded" checks.
The lesson may simplify these facts but must never contradict them.

## Core facts

F1. A Large Language Model (LLM) is an AI model trained on a very large amount of text. It
    generates text by predicting the next word (more exactly, the next "token", a word or part of a word).
    Examples: the models behind ChatGPT, Gemini, Claude, Llama.
F2. An LLM's knowledge comes from its training data, which stops at a fixed date (the "knowledge cutoff").
    It does not know about events after that date.
F3. An LLM does not know private or organisation-specific information it was never trained on
    (for example a company's internal policy, a college's fee list, your own notes).
F4. LLMs can produce answers that sound confident but are wrong or made up. This is called "hallucination".
F5. RAG stands for Retrieval-Augmented Generation. Before the LLM answers, the system first finds
    (retrieves) relevant information from an outside knowledge source and adds it to the prompt, so the
    LLM writes its answer using that information.
    - Retrieval = finding/fetching the relevant pieces of information.
    - Augmented = added to / made stronger: the retrieved text is added to the question in the prompt.
    - Generation = the LLM writes (generates) the answer.
F6. The term was introduced in a 2020 research paper by Patrick Lewis and colleagues (Facebook AI Research / Meta).
F7. Preparation step (indexing, done before questions arrive): collect the documents, split them into
    small pieces called "chunks", turn each chunk into an "embedding" (a list of numbers that captures the
    meaning of the text) using an embedding model, and store them in a searchable index, often a
    "vector database".
F8. Question-time steps:
    1. Retrieve: the user's question is also turned into an embedding, and the system finds the chunks whose
       meaning is most similar (semantic search). Keyword search, or a mix of both, can also be used.
       Usually the top few (top-k) chunks are taken.
    2. Augment: the retrieved chunks are placed into the prompt together with the question and an
       instruction such as "answer using only this information".
    3. Generate: the LLM writes the answer from the question plus the retrieved context. It can also
       point to (cite) the sources it used.
F9. RAG does NOT change or retrain the model. The model's weights (its learned internal numbers) stay the
    same. To update knowledge you update the documents, not the model.
F10. Fine-tuning is different: it trains the model further on new examples and changes its weights. It is
     slower and costlier, and is mainly used to change style or behaviour. RAG is usually the better first
     choice for giving a model new or changing facts.
F11. Benefits of RAG: answers can use up-to-date and private information; fewer made-up answers
     (reduced, not removed); answers can show their sources; cheaper and faster than retraining;
     knowledge is easy to update by changing the documents.
F12. Limits of RAG: the answer is only as good as what is retrieved. If the search returns the wrong or
     outdated chunks, the answer can be wrong. The LLM can still hallucinate or ignore the context. Only a
     limited amount of text fits in the prompt (the "context window"). It adds extra steps, cost and delay,
     and the documents must be kept up to date.
F13. Common uses: customer-support chatbots that answer from company policies, chatbots over a college
     prospectus or government scheme documents, "chat with your PDF" tools, internal company help desks,
     search engines that give answers with sources.
F14. A helpful analogy: an open-book exam. A closed-book student answers only from memory (like a plain
     LLM). An open-book student first finds the right page, then writes the answer using it (like RAG).

## Must-cover points (a beginner lesson must teach all of these)

K1. What an LLM is, in simple words, and its limits: knowledge cutoff, no private data, can make things up.
K2. What RAG is, including the full form and what each of the three words means.
K3. The three question-time steps: retrieve, augment, generate, in the correct order.
K4. How the knowledge is prepared: documents are split into chunks and stored so they can be searched by
    meaning (embeddings explained in simple words).
K5. Why RAG matters: fresh/private information, fewer made-up answers, sources, no retraining needed.
K6. At least one limitation: the answer depends on the quality of what is retrieved.
K7. RAG does not retrain or change the model (contrast with retraining / fine-tuning).

## Known misconceptions (any of these in the lesson = factual error)

M1. "RAG retrains / fine-tunes the model" or "the model permanently learns or memorises your documents".
M2. "RAG makes the LLM always correct" or "RAG completely removes hallucinations".
M3. "RAG means the AI searches the whole internet" (retrieval is from whatever knowledge source the
    system is connected to, very often private documents).
M4. "Embeddings are encryption / a password / compression of the file" (they represent meaning as numbers).
M5. "The LLM reads every document for every question" (only the few most relevant chunks are retrieved).
M6. Wrong order of steps (for example generating before retrieving).
M7. Wrong full form (for example "Random Access Generation" or "Retrieval-Automated Generation").
