from conftest import GOOD

from lessonforge.agents import sabotage
from lessonforge.checks import run_code_check
from lessonforge.judge import evidence_in_lesson
from lessonforge.llm import extract_json


def _check(settings, cid):
    return next(c for c in settings.rubric["checks"] if c["id"] == cid)


def run(settings, cid, md, **kw):
    return run_code_check(md, _check(settings, cid), **kw)


def test_good_fixture_passes_every_code_check(settings):
    for c in settings.rubric["checks"]:
        if c["type"] == "code":
            r = run_code_check(GOOD, c)
            assert r["passed"], (c["id"], r["reason"], r["evidence"])


def test_structure_detects_missing_and_out_of_order(settings):
    assert not run(settings, "STRUCTURE", GOOD.replace("## Quick Check", "## Practice"))["passed"]
    swapped = GOOD.replace("## Why Does RAG Matter?", "## TMP").replace("## How Does RAG Work?", "## Why Does RAG Matter?") \
                  .replace("## TMP", "## How Does RAG Work?")
    assert not run(settings, "STRUCTURE", swapped)["passed"]


def test_acronym_must_be_expanded_near_first_use(settings):
    bad = GOOD.replace("An LLM (Large Language Model) is", "An LLM is").replace("Language Model", "")
    r = run(settings, "ACRONYMS", bad)
    assert not r["passed"] and "LLM" in r["reason"]
    assert not run(settings, "ACRONYMS", GOOD + "\nIt uses an HNSW index.\n")["passed"]
    assert run(settings, "ACRONYMS", GOOD + "\nThis is NOT magic.\n")["passed"]  # emphasis is not an acronym


def test_defined_before_use_catches_early_jargon(settings):
    bad = GOOD.replace("Then it adds them to your question.", "It uses embeddings and a vector database.")
    r = run(settings, "DEFINED_BEFORE_USE", bad)
    assert not r["passed"]
    assert "embedding" in r["evidence"] and "vector database" in r["evidence"]


def test_goal_list_may_name_terms(settings):
    ok = GOOD.replace("- How a computer can look up", "- What chunks and embeddings are, and how a computer can look up")
    assert run(settings, "DEFINED_BEFORE_USE", ok)["passed"]


def test_parenthetical_definition_counts(settings):
    ok = GOOD.replace("Then it adds them to your question.", "It cuts notes into small pieces (chunks) first.")
    assert run(settings, "DEFINED_BEFORE_USE", ok)["passed"]
    assert run(settings, "ACRONYMS", GOOD + "\nThe office opens at 10 AM and closes at 5 PM.\n")["passed"]


def test_term_used_but_never_defined(settings):
    bad =GOOD.replace("## Key Words to Remember", "Some people use fine-tuning instead.\n\n## Key Words to Remember")
    r = run(settings, "DEFINED_BEFORE_USE", bad)
    assert not r["passed"] and "never defined" in r["evidence"]


def test_glossary_needs_meanings(settings):
    bare = GOOD.split("## Key Words to Remember")[0] + "## Key Words to Remember\n\nchunk, token, prompt\n\n## Quick Check\n1. Q?\n**Answer:** a\n2. Q?\n**Answer:** b\n3. Q?\n**Answer:** c\n\n## Summary\nx\n"
    assert not run(settings, "GLOSSARY", bare)["passed"]


def test_sentence_length_and_avoid_words(settings):
    long = "This sentence " + "keeps going and going " * 10 + "until it is far too long for a beginner."
    assert not run(settings, "SENTENCE_LENGTH", GOOD.replace("## Summary", "## Summary\n\n" + long))["passed"]
    assert not run(settings, "AVOID_WORDS", GOOD + "\nIn a nutshell, RAG is great.\n")["passed"]
    # memory-learned words tighten the check
    assert not run(settings, "AVOID_WORDS", GOOD + "\nKindly read this.\n", learned_avoid_words=["kindly"])["passed"]


def test_quiz_requires_answers(settings):
    no_answers = GOOD.replace("**Answer:**", "")
    assert not run(settings, "QUIZ", no_answers)["passed"]


def test_saboteur_trips_code_checks(settings):
    bad, notes = sabotage(GOOD)
    assert len(notes) == 2
    assert not run(settings, "ACRONYMS", bad)["passed"]      # ANN, HNSW
    assert not run(settings, "AVOID_WORDS", bad)["passed"]   # "under the hood"


def test_evidence_verification():
    lesson = "RAG finds the right notes. Then it writes the answer."
    assert evidence_in_lesson("finds the right notes", lesson)
    assert evidence_in_lesson("MISSING: K4 chunks", lesson)
    assert not evidence_in_lesson("RAG retrains the model every day", lesson)


def test_extract_json_handles_fences_and_trailing_commas():
    assert extract_json('Sure!\n```json\n{"a": [1, 2,],}\n```') == {"a": [1, 2]}
    assert extract_json('<think>hmm {"x":0}</think>{"b": 1}') == {"b": 1}
    assert extract_json('{"results": [{"id": "FLOW", "verdict": PASS}]}')["results"][0]["verdict"] == "PASS"
    assert extract_json('{"a": "line one\nline two"}') == {"a": "line one line two"}
