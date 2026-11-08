"""Deterministic rubric checks. Each returns a result dict with a hard pass/fail.

These cover everything that can be measured without judgement. They are cheap, repeatable and
cannot be talked out of a verdict, so the LLM judge only handles what truly needs judgement.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------- text helpers

_CODE_BLOCK = re.compile(r"```.*?```", re.DOTALL)


def headings(md: str, level: int = 2) -> list[tuple[int, str]]:
    """(char_offset, heading text) for every heading of the given level."""
    pat = re.compile(rf"^{'#' * level}\s+(.+?)\s*$", re.MULTILINE)
    return [(m.start(), m.group(1).strip()) for m in pat.finditer(md)]


def section(md: str, match: list[str]) -> str:
    """Text of the first ## section whose heading contains any phrase in `match`."""
    hs = headings(md)
    for i, (pos, title) in enumerate(hs):
        if any(p in title.lower() for p in match):
            end = hs[i + 1][0] if i + 1 < len(hs) else len(md)
            return md[pos:end]
    return ""


def prose(md: str) -> str:
    """Lesson text without code blocks, headings, tables or markdown symbols."""
    text = _CODE_BLOCK.sub(" ", md)
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("|") or set(s) <= set("-*_=> "):
            continue
        s = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", s)       # list markers
        s = re.sub(r"^>\s*", "", s)                          # quotes
        s = re.sub(r"[*_`]+", "", s)                         # emphasis
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)       # links
        lines.append(s)
    return "\n".join(lines)


def sentences(md: str) -> list[str]:
    """Split prose into sentences. Each line is also a boundary (bullets often lack full stops)."""
    out: list[str] = []
    for line in prose(md).splitlines():
        for s in re.split(r"(?<=[.!?])\s+", line):
            if re.search(r"[A-Za-z]", s):
                out.append(s.strip())
    return out


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text)


def syllables(word: str) -> int:
    if "-" in word.strip("-"):
        return sum(syllables(p) for p in word.split("-") if p)
    w = word.lower().strip("'")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def taught_terms(md: str) -> set[str]:
    """Words of the technical terms the lesson itself defines in its glossary ("Key Words") section."""
    body = section(md, ["key words", "words to remember", "glossary"])
    terms = set()
    for t in re.findall(r"\*\*([^*]+?)\*\*", body):
        t = re.sub(r"\(.*?\)", " ", t)
        terms |= {w.lower() for w in words(t)}
    # simple inflections: hallucination -> hallucinations, embedding -> embeddings
    return terms | {t + "s" for t in terms}


def flesch(md: str, exclude: set[str] | None = None) -> float:
    """Flesch Reading Ease. Words in `exclude` still count for sentence length but not for syllables."""
    sents = sentences(md)
    ws = [w for s in sents for w in words(s)]
    if not sents or not ws:
        return 0.0
    scored = [w for w in ws if w.lower() not in (exclude or set())] or ws
    syl = sum(syllables(w) for w in scored)
    return 206.835 - 1.015 * (len(ws) / len(sents)) - 84.6 * (syl / len(scored))


def _result(check: dict, passed: bool, reason: str, evidence: str = "", fix: str = "") -> dict:
    return {
        "id": check["id"], "dimension": check["dimension"], "type": "code",
        "passed": bool(passed), "reason": reason, "evidence": evidence, "fix": "" if passed else fix,
    }


# ---------------------------------------------------------------- the checks

def check_structure(md: str, check: dict) -> dict:
    found = [t for _, t in headings(md)]
    missing, idx = [], 0
    for spec in check["params"]["sections"]:
        hit = next((i for i in range(idx, len(found)) if any(p in found[i].lower() for p in spec["match"])), None)
        if hit is None:
            missing.append(spec["key"])
        else:
            idx = hit + 1
    has_title = bool(headings(md, 1))
    ok = not missing and has_title
    reason = "All sections present in order." if ok else (
        f"Missing or out-of-order sections: {', '.join(missing) or '-'}; title present: {has_title}.")
    return _result(check, ok, reason, evidence=" | ".join(found),
                   fix="Use exactly the required ## headings in the required order, plus one # title.")


def check_sentence_length(md: str, check: dict) -> dict:
    p = check["params"]
    sents = sentences(md)
    lens = [len(words(s)) for s in sents]
    avg = sum(lens) / len(lens) if lens else 0
    too_long = [s for s, n in zip(sents, lens) if n > p["max_words"]]
    ok = bool(sents) and avg <= p["max_avg_words"] and not too_long
    reason = f"Average {avg:.1f} words/sentence (max {p['max_avg_words']}); {len(too_long)} sentence(s) over {p['max_words']} words."
    return _result(check, ok, reason, evidence=" || ".join(too_long[:3]),
                   fix=f"Split long sentences. Keep every sentence under {p['max_words']} words, most under 15.")


def check_readability(md: str, check: dict) -> dict:
    # The topic's own vocabulary (retrieval, hallucination, ...) is unavoidable and is policed by the JARGON
    # check, so it is left out of the syllable count: we score the difficulty of the *surrounding* English.
    terms = taught_terms(md)
    score = flesch(md, terms)
    raw = flesch(md)
    ok = score >= check["params"]["min_flesch"]
    sents = sentences(md)
    hardest = sorted(sents, key=lambda s: -sum(syllables(w) for w in words(s) if w.lower() not in terms))[:3]
    return _result(check, ok,
                   f"Flesch Reading Ease {score:.1f} on everyday words (need >= {check['params']['min_flesch']}; "
                   f"raw score incl. {len(terms)} taught terms: {raw:.1f}).",
                   evidence=" || ".join(hardest),
                   fix="Rewrite the hardest sentences (see evidence) with shorter, more common words.")


def check_avoid_words(md: str, check: dict, extra_words: list[str] | None = None) -> dict:
    vocab = list(dict.fromkeys([w.lower() for w in check["params"]["words"] + (extra_words or [])]))
    body = prose(md)
    hits = []
    for w in vocab:
        m = re.search(rf"(?<![A-Za-z]){re.escape(w)}(?![A-Za-z])", body, re.IGNORECASE)
        if m:
            line = body[max(0, m.start() - 50): m.end() + 50].replace("\n", " ")
            hits.append((w, line.strip()))
    ok = not hits
    return _result(check, ok,
                   "No difficult words or idioms found." if ok else f"Found: {', '.join(h[0] for h in hits)}.",
                   evidence=" || ".join(h[1] for h in hits[:4]),
                   fix="Replace these with simple everyday words: " + ", ".join(h[0] for h in hits))


def check_length(md: str, check: dict) -> dict:
    n = len(words(prose(md)))
    p = check["params"]
    ok = p["min_words"] <= n <= p["max_words"]
    return _result(check, ok, f"{n} words (allowed {p['min_words']}-{p['max_words']}).", evidence=str(n),
                   fix="Add depth to thin sections." if n < p["min_words"] else "Cut repetition; stay focused.")


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[-_*`]", " ", s.lower()))


def check_acronyms(md: str, check: dict) -> dict:
    p = check["params"]
    allow = set(p.get("allow", []))
    known = {k: v.lower() for k, v in p.get("known", {}).items()}
    text = _CODE_BLOCK.sub(" ", md)
    norm_text = _norm(text)
    problems = []
    seen = set()
    for m in re.finditer(r"\b[A-Z]{2,}s?\b", text):
        acr = m.group(0)
        base = acr[:-1] if acr.endswith("s") and acr[:-1].isupper() and acr[:-1] in known else acr
        if base in allow or base in seen:
            continue
        seen.add(base)
        # position of first use, mapped approximately into the normalised text
        pos = len(_norm(text[: m.start()]))
        window_end = pos + p["window_chars"]
        if base in known:
            exp = known[base]
            idx = norm_text.find(exp)
            if idx == -1 or idx > window_end:
                problems.append(f"{acr} (full form '{known[base]}' not given near first use)")
        else:
            after = text[m.end(): m.end() + 150].lower()
            if not (after.lstrip().startswith("(") or "stands for" in after or " means" in after):
                problems.append(f"{acr} (never expanded or explained)")
    ok = not problems
    return _result(check, ok, "All acronyms expanded at first use." if ok else "Unexpanded acronyms: " + "; ".join(problems),
                   evidence="; ".join(problems[:5]),
                   fix="Write each acronym in full at its first use, e.g. 'LLM (Large Language Model)'.")


def check_quiz(md: str, check: dict) -> dict:
    body = section(md, ["quick check", "quiz", "check your understanding"])
    questions = [l for l in body.splitlines()[1:] if l.strip().rstrip("*").endswith("?")]
    answers = len(re.findall(r"answer", body, re.IGNORECASE))
    need = check["params"]["min_questions"]
    ok = len(questions) >= need and answers >= len(questions)
    return _result(check, ok, f"{len(questions)} question(s), {answers} answer marker(s); need >= {need} with answers.",
                   evidence=" | ".join(q.strip() for q in questions[:5]),
                   fix=f"Add a Quick Check with at least {need} questions ending in '?', each followed by '**Answer:** ...'.")


_DASHES = re.compile(r"[‐-―−]")  # non-breaking / en / em dashes -> "-"


def _body_for_terms(md: str) -> str:
    """Lesson text up to the glossary, with headings blanked (same length, so offsets stay valid)."""
    md = _DASHES.sub("-", md)
    hs = headings(md)
    cut = next((pos for pos, t in hs if any(k in t.lower() for k in ("key words", "words to remember", "glossary"))),
               len(md))
    body = md[:cut]
    # The "What You Will Learn" list only names goals ("what a chunk is"); naming a goal is not a use.
    learn = [(i, pos) for i, (pos, t) in enumerate(hs) if "what you will learn" in t.lower() and pos < cut]
    if learn:
        i, start = learn[0]
        end = hs[i + 1][0] if i + 1 < len(hs) else cut
        body = body[:start] + re.sub(r"\S", " ", body[start:end]) + body[end:]
    return re.sub(r"^#.*$", lambda m: " " * len(m.group(0)), body, flags=re.MULTILINE)


def check_defined_before_use(md: str, check: dict) -> dict:
    """Every listed technical term must be defined (bolded, or 'X is a/means/(...)/called X') before any other use."""
    body = _body_for_terms(md)
    terms = sorted({t.lower() for t in check["params"]["terms"]}, key=len, reverse=True)
    problems = []
    for term in terms:
        t = re.escape(term).replace(r"\-", "[- ]")
        occ = [m for m in re.finditer(rf"(?<![A-Za-z]){t}(?:s|es)?(?![A-Za-z])", body, re.IGNORECASE)]
        # ignore uses that sit inside a longer listed term ("vector" inside "vector database")
        longer = [lt for lt in terms if len(lt) > len(term) and term in lt]
        spans = [(m.start(), m.end()) for lt in longer
                 for m in re.finditer(re.escape(lt).replace(r"\-", "[- ]"), body, re.IGNORECASE)]
        occ = [m for m in occ if not any(a <= m.start() < b for a, b in spans)]
        if not occ:
            continue
        def_idx = None
        for i, m in enumerate(occ):
            before, after = body[max(0, m.start() - 12): m.start()], body[m.end(): m.end() + 14]
            if (before.endswith("**") and after.startswith("**")) or re.search(r"called (?:an? |the )?\**$", before, re.I) \
                    or (re.search(r"\(\**$", before) and re.match(r"\**\)", after)) \
                    or re.match(r"\**\s*(?:\(|is an? |is the |means |stands for )", after, re.I):
                def_idx = i
                break
        line = lambda m: body[max(0, m.start() - 60): m.end() + 40].replace("\n", " ").strip()
        if def_idx is None:
            problems.append(f"'{term}' is used but never defined (first use: \"...{line(occ[0])}...\")")
        elif def_idx > 0:
            problems.append(f"'{term}' is used before its definition (\"...{line(occ[0])}...\")")
    ok = not problems
    return _result(check, ok, "Every listed term is defined before it is used." if ok else
                   f"{len(problems)} term(s) used before being explained.",
                   evidence=" || ".join(problems[:6]),
                   fix="Define each listed term (bold it, e.g. '**chunk** (a small piece of a document)') at its "
                       "FIRST use, or replace the earlier uses with plain words. Terms: "
                       + "; ".join(problems))


def check_glossary(md: str, check: dict) -> dict:
    body = section(md, ["key words", "words to remember", "glossary"])
    lines = [l for l in body.splitlines()[1:] if l.strip()]
    entries = [l for l in lines if re.match(r"^\s*(?:[-*+]|\d+[.)])?\s*\**[^:*\n]{1,50}?\**\s*(?::|\s[-–—]\s)\s*\S.{3,}", l)]
    need = check["params"]["min_entries"]
    ok = len(entries) >= need
    return _result(check, ok, f"{len(entries)} glossary entries with a meaning (need >= {need}).",
                   evidence=" | ".join(lines[:3]),
                   fix=f"Write the Key Words section as a list of at least {need} lines: '- **term**: simple meaning'.")


REGISTRY = {
    "defined_before_use": check_defined_before_use,
    "glossary": check_glossary,
    "structure": check_structure,
    "sentence_length": check_sentence_length,
    "readability": check_readability,
    "avoid_words": check_avoid_words,
    "length": check_length,
    "acronyms": check_acronyms,
    "quiz": check_quiz,
}


def run_code_check(md: str, check: dict, learned_avoid_words: list[str] | None = None) -> dict:
    fn = REGISTRY[check["fn"]]
    if check["fn"] == "avoid_words":
        return fn(md, check, learned_avoid_words)
    return fn(md, check)
