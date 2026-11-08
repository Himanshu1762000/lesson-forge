"""Shared test fixtures: an isolated project copy and a scripted fake LLM (no network needed)."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import pytest
import yaml

from lessonforge.config import load_settings

REPO = Path(__file__).resolve().parents[1]
GOOD = (REPO / "tests" / "fixtures" / "good_lesson.md").read_text(encoding="utf-8")


@pytest.fixture
def settings(tmp_path):
    for d in ("prompts", "rubric", "knowledge"):
        shutil.copytree(REPO / d, tmp_path / d)
    shutil.copy(REPO / "config.yaml", tmp_path / "config.yaml")
    # the fixture lesson is short on purpose; relax only the length bar
    rub = yaml.safe_load((tmp_path / "rubric" / "rubric.yaml").read_text(encoding="utf-8"))
    for c in rub["checks"]:
        if c["id"] == "LENGTH":
            c["params"]["min_words"] = 100
    (tmp_path / "rubric" / "rubric.yaml").write_text(yaml.safe_dump(rub), encoding="utf-8")
    s = load_settings(tmp_path)
    s.models = {"default": "fake"}
    return s


class FakeLLM:
    """Scripted model. `fail_plan[i]` = set of LLM check ids the judge fails on attempt i+1
    (the last entry repeats). Missing ids in `silent` are left out of the judge reply."""

    def __init__(self, fail_plan=None, silent=(), lesson=GOOD):
        self.fail_plan = fail_plan or [set()]
        self.silent = set(silent)
        self.lesson = lesson
        self.attempt = 0
        self.calls = []

    def chat(self, role, prompt, **kw):
        self.calls.append({"role": role})
        if role == "planner":
            return json.dumps({"sections": [{"heading": "What Is RAG?"}], "analogy": {"story": "open-book exam"}})
        if role == "generator":
            self.attempt = 1
            return self.lesson
        if role == "reviser":
            self.attempt += 1
            return self.lesson + "\n===CHANGELOG===\n- [JARGON] defined the term at first use\n"
        if role == "coach":
            return json.dumps({"guideline": "Define every term at first use.", "avoid_words": ["kindly"]})
        if role == "judge":
            ids = re.findall(r"^- ([A-Z_]+) \(", prompt, re.MULTILINE)
            fails = self.fail_plan[min(self.attempt, len(self.fail_plan)) - 1]
            res = [{"id": i, "verdict": "FAIL" if i in fails else "PASS",
                    "evidence": "MISSING: something" if i in fails else "",
                    "reason": f"{i} problem" if i in fails else "ok", "fix": "fix it"}
                   for i in ids if i not in self.silent]
            return json.dumps({"results": res})
        raise AssertionError(role)

    def chat_json(self, role, prompt, **kw):
        return json.loads(self.chat(role, prompt, **kw))
