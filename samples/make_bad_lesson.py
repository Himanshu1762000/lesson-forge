"""Build samples/bad_lesson.md by planting known mistakes into a lesson that passed every check.

Usage: python samples/make_bad_lesson.py outputs/<run_id>/lesson.md
Each planted mistake is listed in samples/README.md together with the check that must catch it.
"""
import re
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
md = src

def insert_after_heading(md: str, heading_word: str, text: str) -> str:
    m = re.search(rf"^## [^\n]*{heading_word}[^\n]*$", md, re.IGNORECASE | re.MULTILINE)
    assert m, heading_word
    return md[: m.end()] + "\n\n" + text + "\n" + md[m.end():]

# 1. Wrong full form (misconception M7)                      -> GROUNDED_DEFINITION, ACRONYMS
md = md.replace("Retrieval-Augmented Generation", "Retrieval-Automated Generation")
# 2. RAG retrains the model (M1) + overclaim (M2)            -> ACCURACY, NO_OVERCLAIM
md = insert_after_heading(md, "Why", "The best part is that RAG retrains the model with your documents every night, "
                          "so its answers are always 100% correct.")
# 3. Unexplained jargon, unexpanded acronym, idiom           -> JARGON, ACRONYMS, AVOID_WORDS
md = insert_after_heading(md, "How", "In a nutshell, the retriever uses cosine similarity over an HNSW index.")
# 4. One very long, complex sentence                         -> SENTENCE_LENGTH, PLAIN_LANGUAGE
md = insert_after_heading(md, "Before We Start",
    "Notwithstanding the aforementioned considerations regarding the architecture of contemporary language "
    "systems, it is nevertheless imperative that the learner appreciates the multifaceted interplay between "
    "parametric memory and non-parametric retrieval mechanisms in modern deployments.")
# 5. Quiz answers removed                                    -> QUIZ
md = re.sub(r"^\*\*Answer:\*\*.*$\n?", "", md, flags=re.MULTILINE)

out = Path(__file__).with_name("bad_lesson.md")
out.write_text(md, encoding="utf-8")
print(f"wrote {out}")

