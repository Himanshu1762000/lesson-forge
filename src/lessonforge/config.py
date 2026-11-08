"""Loads config.yaml, the rubric, prompt templates and grounding reference sheets."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from string import Template

import yaml
from dotenv import load_dotenv

ROOT = Path(os.environ.get("LESSONFORGE_ROOT", Path(__file__).resolve().parents[2]))


@dataclass
class Settings:
    raw: dict
    rubric: dict
    root: Path = ROOT
    models: dict = field(default_factory=dict)

    @property
    def max_retries(self) -> int:
        return int(self.raw["loop"]["max_retries"])

    @property
    def audience(self) -> str:
        return " ".join(self.raw["audience"].split())

    def path(self, rel: str) -> Path:
        return self.root / rel


def load_settings(root: Path | None = None) -> Settings:
    root = Path(root) if root else ROOT
    load_dotenv(root / ".env")
    raw = yaml.safe_load((root / "config.yaml").read_text(encoding="utf-8"))
    rubric = yaml.safe_load((root / "rubric" / "rubric.yaml").read_text(encoding="utf-8"))
    gen = os.environ.get("GENERATOR_MODEL", "")
    models = {
        "default": gen,
        "generator": gen,
        "planner": os.environ.get("PLANNER_MODEL") or gen,
        "reviser": os.environ.get("REVISER_MODEL") or gen,
        "coach": os.environ.get("COACH_MODEL") or gen,
        "judge": os.environ.get("JUDGE_MODEL") or gen,
    }
    return Settings(raw=raw, rubric=rubric, root=root, models=models)


def render_prompt(settings: Settings, name: str, **values) -> str:
    text = (settings.root / "prompts" / f"{name}.md").read_text(encoding="utf-8")
    return Template(text).safe_substitute({k: str(v) for k, v in values.items()})


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "topic"


def find_reference(settings: Settings, topic: str) -> Path | None:
    """Return the grounding sheet for a topic, or None if we have none."""
    key = topic.strip().lower()
    mapping = settings.raw.get("topics", {}) or {}
    if key in mapping:
        return settings.path(mapping[key])
    for name, rel in mapping.items():  # loose match, e.g. "Intro to RAG for beginners"
        if name in key or key in name:
            return settings.path(rel)
    candidate = settings.path(f"knowledge/{slugify(topic)}.md")
    return candidate if candidate.exists() else None
