You are a careful editor improving a beginner lesson. An automatic reviewer rejected it.

TOPIC: $topic

LEARNER:
$audience

REFERENCE SHEET (ground truth):
<<<
$reference
>>>

LESSONS LEARNED FROM PAST RUNS:
$guidelines

THE LESSON THAT WAS REJECTED:
<<<
$lesson
>>>

FAILED CHECKS (each one must be fixed):
$failures

CHECKS THAT ALREADY PASS (do not break these):
$passing

Instructions
- Fix every failed check. Use the quoted evidence to find the exact place to change.
- Change only what is needed. Keep the headings, structure and every part that already works.
- Keep sentences short and words simple.
- Do NOT add any technical word that is not already in the lesson (for example "context window", "top-k",
  "indexing", "cosine similarity"). Fixing one problem must not create a new one. If you remove a term,
  remove it everywhere, including the glossary.
- To fix an unexplained term, either explain it in simple words at its FIRST use, or replace it with plain
  words everywhere. Every definition must agree with the reference sheet. Never merge two different terms
  (for example "context" = the retrieved text placed in the prompt; "context window" = the limit on how
  much text fits).
- Do not add facts that are not in the reference sheet.

Output format (exactly):
1. The full revised lesson in markdown (not just the changed parts).
2. Then a line containing only: ===CHANGELOG===
3. Then one bullet per change, in the form: "- [CHECK_ID] what you changed and where".
