"""Persistent memory shared by every run (a readable JSON file, on purpose: easy to inspect and diff).

What is remembered
- runs:               one summary per run (attempts, verdicts, which checks failed)
- check_stats:        per-check failure counts + recent failure samples (reason + evidence)
- guidelines:         per-check rules written by the coach; versioned and sharpened if they stop working
- human_feedback:     notes a reviewer adds with `lessonforge feedback "..."`
- learned_avoid_words: words/idioms the coach found in failures; they tighten the AVOID_WORDS code check

How it is used next run
- guidelines + human feedback are injected into the planner, generator and reviser prompts
- learned_avoid_words are added to the deterministic AVOID_WORDS check (the rubric itself gets stricter)
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def criterion_hashes(rubric: dict) -> dict[str, str]:
    """Fingerprint of each check's definition. When a check is redefined, old lessons about it go stale."""
    return {c["id"]: hashlib.sha1(json.dumps({k: c.get(k) for k in ("criterion", "params", "description")},
                                             sort_keys=True).encode()).hexdigest()[:10]
            for c in rubric["checks"]}


EMPTY = {
    "version": 1,
    "runs": [],
    "check_stats": {},
    "guidelines": {},
    "human_feedback": [],
    "learned_avoid_words": [],
}


class Memory:
    def __init__(self, path: Path, data: dict | None = None, max_samples: int = 6):
        self.path = Path(path)
        self.data = data or json.loads(json.dumps(EMPTY))
        self.max_samples = max_samples

    # ------------------------------------------------------------ io
    @classmethod
    def load(cls, path: Path, max_samples: int = 6) -> "Memory":
        path = Path(path)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            for k, v in EMPTY.items():
                data.setdefault(k, json.loads(json.dumps(v)))
            return cls(path, data, max_samples)
        return cls(path, None, max_samples)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(self.path)  # atomic: a crash never leaves half-written memory

    def reload(self) -> None:
        """Re-read memory from disk, so updates made by another run since we started are kept."""
        fresh = Memory.load(self.path, self.max_samples)
        self.data = fresh.data

    @contextmanager
    def locked(self, timeout: float = 120.0):
        """Cross-process lock around read-modify-write, so two parallel runs cannot overwrite each other."""
        lock = self.path.with_suffix(".lock")
        lock.parent.mkdir(parents=True, exist_ok=True)
        start = time.time()
        while True:
            try:
                fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                break
            except FileExistsError:
                if time.time() - lock.stat().st_mtime > 600:  # stale lock from a killed run
                    lock.unlink(missing_ok=True)
                    continue
                if time.time() - start > timeout:
                    raise TimeoutError(f"memory is locked by another run ({lock})")
                time.sleep(0.5)
        try:
            self.reload()
            yield self
            self.save()
        finally:
            lock.unlink(missing_ok=True)

    # ------------------------------------------------------------ reading
    def guidelines_text(self, current: dict[str, str] | None = None) -> str:
        """Rules for the prompts. With `current` (check id -> criterion hash), rules learned under an older
        version of a check's criterion are left out: they may demand things the rubric no longer asks."""
        def fresh(cid, g):
            return current is None or g.get("crit") in (None, current.get(cid))
        lines = [f"- ({cid}) {g['text']}" for cid, g in sorted(self.data["guidelines"].items()) if fresh(cid, g)]
        lines += [f"- (reviewer feedback) {f['text']}" for f in self.data["human_feedback"][-10:]]
        return "\n".join(lines) if lines else "- (none yet: this is an early run)"

    @property
    def avoid_words(self) -> list[str]:
        return list(self.data["learned_avoid_words"])

    # ------------------------------------------------------------ writing
    def record_evaluation(self, run_id: str, attempt: int, results: list[dict],
                          crit: dict[str, str] | None = None) -> None:
        crit = crit or {}
        for r in results:
            st = self.data["check_stats"].setdefault(
                r["id"], {"evaluations": 0, "fails": 0, "fails_since_rule": 0, "samples": []})
            st["evaluations"] += 1
            if not r["passed"]:
                st["fails"] += 1
                st["fails_since_rule"] += 1
                st["samples"].append({"run_id": run_id, "attempt": attempt, "crit": crit.get(r["id"]),
                                      "reason": r.get("reason", ""), "evidence": r.get("evidence", "")[:300]})
                st["samples"] = st["samples"][-self.max_samples:]

    def set_guideline(self, check_id: str, text: str, source: str = "coach", crit: str | None = None) -> dict:
        old = self.data["guidelines"].get(check_id)
        g = {"text": text.strip(), "source": source, "version": (old["version"] + 1) if old else 1, "crit": crit,
             "updated": now(), "previous": old["text"] if old else None}
        self.data["guidelines"][check_id] = g
        if check_id in self.data["check_stats"]:
            self.data["check_stats"][check_id]["fails_since_rule"] = 0
        return g

    def add_avoid_words(self, new_words: list[str]) -> list[str]:
        have = {w.lower() for w in self.data["learned_avoid_words"]}
        added = [w.strip() for w in new_words if w and w.strip() and w.strip().lower() not in have]
        self.data["learned_avoid_words"] += added
        return added

    def add_feedback(self, text: str, run_id: str | None = None) -> None:
        self.data["human_feedback"].append({"text": text.strip(), "run_id": run_id, "created": now()})

    def add_run(self, summary: dict) -> None:
        self.data["runs"].append(summary)
