import json

from conftest import FakeLLM

from lessonforge.graph import run_loop
from lessonforge.memory import Memory


def _run(settings, llm, tmp_path, **kw):
    return run_loop(llm, settings, "Introduction to RAG", out_root=tmp_path / "out", **kw)


def test_ships_on_first_attempt(settings, tmp_path):
    state = _run(settings, FakeLLM(), tmp_path)
    assert state["final"]["status"] == "SHIPPED"
    assert len(state["history"]) == 1
    run_dir = tmp_path / "out" / state["run_id"]
    assert (run_dir / "lesson.md").exists() and (run_dir / "rejection_log.md").exists()


def test_regenerates_with_feedback_then_ships(settings, tmp_path):
    llm = FakeLLM(fail_plan=[{"JARGON", "ANALOGY"}, set()])
    state = _run(settings, llm, tmp_path)
    assert state["final"]["status"] == "SHIPPED" and state["final"]["attempt"] == 2
    second = state["history"][1]
    assert set(second["fixed"]) == {"JARGON", "ANALOGY"} and second["broken"] == []
    log = (tmp_path / "out" / state["run_id"] / "rejection_log.md").read_text(encoding="utf-8")
    assert "JARGON" in log and "defined the term at first use" in log


def test_loop_always_terminates_and_flags_for_human(settings, tmp_path):
    llm = FakeLLM(fail_plan=[{"ACCURACY"}])  # never fixed
    state = _run(settings, llm, tmp_path, max_retries=2)
    assert len(state["history"]) == 3  # 1 draft + 2 retries, then stop
    assert state["final"]["status"] == "NEEDS_HUMAN_REVIEW"
    assert sum(c["role"] == "reviser" for c in llm.calls) == 2
    lesson = (tmp_path / "out" / state["run_id"] / "lesson.md").read_text(encoding="utf-8")
    assert lesson.startswith("> **NOT SHIPPED")


def test_judge_silence_fails_closed(settings, tmp_path):
    state = _run(settings, FakeLLM(silent={"COVERAGE"}), tmp_path, max_retries=0)
    assert "COVERAGE" in state["history"][0]["failed"]
    assert state["final"]["status"] == "NEEDS_HUMAN_REVIEW"


def test_unreadable_judge_does_not_crash_and_fails_closed(settings, tmp_path):
    class GarbageJudge(FakeLLM):
        def chat_json(self, role, prompt, **kw):
            if role == "judge":
                raise ValueError("unparseable JSON: Expecting value: line 1 column 185")
            return super().chat_json(role, prompt, **kw)

    state = _run(settings, GarbageJudge(), tmp_path, max_retries=1)
    assert len(state["history"]) == 2  # loop still ran its course
    assert state["final"]["status"] == "NEEDS_HUMAN_REVIEW"
    assert {"ACCURACY", "JARGON"} <= set(state["history"][0]["failed"])


def test_injected_errors_are_caught_and_not_learned(settings, tmp_path):
    state = _run(settings, FakeLLM(), tmp_path, inject_error=True)
    first = state["history"][0]
    assert "saboteur" in first["source"] and not first["passed"]
    assert {"ACRONYMS", "AVOID_WORDS"} <= set(first["failed"])
    assert state["final"]["status"] == "SHIPPED"
    mem = Memory.load(settings.path(settings.raw["memory"]["path"]))
    assert "ACRONYMS" not in mem.data["check_stats"] or mem.data["check_stats"]["ACRONYMS"]["fails"] == 0


def test_memory_persists_and_coach_learns(settings, tmp_path):
    path = settings.path(settings.raw["memory"]["path"])
    _run(settings, FakeLLM(fail_plan=[{"JARGON"}, set()]), tmp_path)
    mem = Memory.load(path)
    assert len(mem.data["runs"]) == 1 and mem.data["check_stats"]["JARGON"]["fails"] == 1
    assert "JARGON" not in mem.data["guidelines"]  # one failure is not a pattern yet

    _run(settings, FakeLLM(fail_plan=[{"JARGON"}, set()]), tmp_path)
    mem = Memory.load(path)
    assert len(mem.data["runs"]) == 2
    assert mem.data["guidelines"]["JARGON"]["version"] == 1
    assert "kindly" in mem.avoid_words  # rubric tightened from memory
    assert "Define every term" in mem.guidelines_text()


def test_parallel_runs_do_not_overwrite_each_others_memory(settings, tmp_path):
    path = settings.path(settings.raw["memory"]["path"])
    a, b = Memory.load(path), Memory.load(path)  # two runs that started at the same time
    with a.locked():
        a.add_run({"run_id": "A"})
    with b.locked():  # b's stale in-RAM copy must be refreshed before writing
        b.add_run({"run_id": "B"})
    assert [r["run_id"] for r in Memory.load(path).data["runs"]] == ["A", "B"]
    assert not path.with_suffix(".lock").exists()


def test_rules_from_an_old_check_definition_are_not_used(settings):
    from lessonforge.memory import criterion_hashes

    m = Memory(settings.path("memory/x.json"))
    crit = criterion_hashes(settings.rubric)
    m.set_guideline("JARGON", "old strict rule", crit="outdated-hash")
    m.set_guideline("FLOW", "current rule", crit=crit["FLOW"])
    text = m.guidelines_text(crit)
    assert "current rule" in text and "old strict rule" not in text


def test_human_feedback_reaches_the_prompts(settings, tmp_path):
    path = settings.path(settings.raw["memory"]["path"])
    m = Memory.load(path)
    m.add_feedback("Use cricket examples.")
    m.save()

    seen = {}

    class Spy(FakeLLM):
        def chat(self, role, prompt, **kw):
            seen.setdefault(role, prompt)
            return super().chat(role, prompt, **kw)

    _run(settings, Spy(), tmp_path)
    assert "Use cricket examples." in seen["generator"] and "Use cricket examples." in seen["planner"]
