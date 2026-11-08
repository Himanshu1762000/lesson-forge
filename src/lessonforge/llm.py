"""Model-agnostic LLM client (any OpenAI-compatible endpoint) with retries and JSON extraction."""
from __future__ import annotations

import json
import os
import re
import time

_THINK = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


class LLMError(RuntimeError):
    pass


def extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model reply (handles ```json fences and chatter)."""
    text = _THINK.sub("", text).strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object found")
    blob = text[start : end + 1]
    # Repairs for common model slips, tried one after another (each builds on the previous).
    repairs = [
        lambda s: s,
        lambda s: re.sub(r",\s*([}\]])", r"\1", s),                                  # trailing commas
        lambda s: re.sub(r":\s*(PASS|FAIL)\b(?!\")", r': "\1"', s),                   # "verdict": PASS
        lambda s: s.replace("“", '"').replace("”", '"'),                              # smart quotes as delimiters
        lambda s: re.sub(r"\bTrue\b", "true", re.sub(r"\bFalse\b", "false", re.sub(r"\bNone\b", "null", s))),
        lambda s: re.sub(r"[\x00-\x1f]", " ", s),                                     # raw newlines/tabs in strings
    ]
    last: Exception | None = None
    for fix in repairs:
        blob = fix(blob)
        try:
            return json.loads(blob)
        except json.JSONDecodeError as exc:
            last = exc
    raise ValueError(f"unparseable JSON: {last}")


class LLM:
    """Thin wrapper so every agent calls models the same way: chat(role, prompt)."""

    def __init__(self, models: dict, base_url: str | None = None, api_key: str | None = None,
                 timeout: float = 300.0, attempts: int = 3):
        from openai import OpenAI

        base_url = base_url or os.environ.get("LLM_BASE_URL")
        api_key = api_key or os.environ.get("LLM_API_KEY")
        if not base_url or not api_key or not models.get("default"):
            raise LLMError("Set LLM_BASE_URL, LLM_API_KEY and GENERATOR_MODEL in .env (see .env.example).")
        self.client = OpenAI(base_url=base_url, api_key=api_key, timeout=timeout, max_retries=0)
        self.models = models
        self.attempts = attempts
        self.calls: list[dict] = []  # lightweight trace: role, model, seconds, tokens

    def model_for(self, role: str) -> str:
        return self.models.get(role) or self.models["default"]

    def chat(self, role: str, prompt: str, *, system: str | None = None,
             temperature: float = 0.4, max_tokens: int = 8000) -> str:
        model = self.model_for(role)
        messages = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": prompt}
        ]
        last: Exception | None = None
        for i in range(self.attempts):
            t0 = time.time()
            try:
                resp = self.client.chat.completions.create(
                    model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
                )
                text = _THINK.sub("", resp.choices[0].message.content or "").strip()
                usage = getattr(resp, "usage", None)
                self.calls.append({
                    "role": role, "model": getattr(resp, "model", model),
                    "seconds": round(time.time() - t0, 1),
                    "tokens": getattr(usage, "total_tokens", None),
                })
                if text:
                    return text
                last = LLMError("empty response")
            except Exception as exc:  # network, rate limit, provider error
                last = exc
                self.calls.append({"role": role, "model": model, "seconds": round(time.time() - t0, 1),
                                   "tokens": None, "error": str(exc)[:120]})
            time.sleep(min(2 ** (i + 1), 20))
        raise LLMError(f"{role} call to {model} failed after {self.attempts} attempts: {last}")

    def chat_json(self, role: str, prompt: str, tries: int = 3, **kw) -> dict:
        """Ask for JSON; on unreadable output ask again (fresh call) up to `tries` times."""
        ask = prompt
        for i in range(tries):
            text = self.chat(role, ask, **kw)
            try:
                return extract_json(text)
            except ValueError as exc:
                self.calls.append({"role": role, "json_error": str(exc)[:200]})
                save_bad_reply(role, text)
                ask = (prompt + "\n\nIMPORTANT: your previous reply was not valid JSON (" + str(exc)[:120] +
                       "). Reply again with ONLY one valid JSON object: double quotes around every key and "
                       "string, no comments, no trailing commas, escape any \" inside strings.")
        raise LLMError(f"{role}: no valid JSON after {tries} tries")


def save_bad_reply(role: str, text: str) -> None:
    """Keep the last unreadable reply per role for debugging (outputs/_debug/)."""
    try:
        from .config import ROOT
        d = ROOT / "outputs" / "_debug"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"bad_json_{role}.txt").write_text(text, encoding="utf-8")
    except Exception:
        pass
