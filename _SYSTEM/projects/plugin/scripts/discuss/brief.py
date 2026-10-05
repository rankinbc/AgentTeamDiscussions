"""Brief parsing — port of Brief/BriefParser.cs.

Brief format:
    # Title
    ## What's Already Decided   (bullets every agent sees)
    ## Context                  (optional reference material, never trimmed)
    ## Open Questions           (required; `N. **Title** body`)
Sections end at the next level-2 heading, so use ### or deeper inside them.
"""

import re
from dataclasses import dataclass


class BriefParseError(Exception):
    pass


@dataclass
class Question:
    number: int
    title: str
    body: str


@dataclass
class Brief:
    title: str
    decided: list
    context: str
    questions: list


_SECTION_END = r"(?=\n## |\Z)"
_QUESTION_RE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*?)(?=^\d+\.\s+\*\*|\Z)", re.M | re.S)


def _section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?){_SECTION_END}", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def looks_like_brief(text: str) -> bool:
    return re.search(r"^## Open Questions", text, re.M) is not None


def parse_questions(questions_text: str) -> list:
    return [
        Question(int(m.group(1)), m.group(2).strip(), m.group(3).strip())
        for m in _QUESTION_RE.finditer(questions_text)
    ]


def parse_brief_text(text: str, fallback_title: str = "") -> Brief:
    text = text.lstrip("﻿")
    title_match = re.search(r"^# (.+)$", text, re.M)
    questions_text = _section(text, "Open Questions")
    if not questions_text and not looks_like_brief(text):
        raise BriefParseError("No 'Open Questions' section found in brief.")
    questions = parse_questions(questions_text)
    if not questions:
        raise BriefParseError("No questions parsed from brief.")

    # SessionPreparer splits the decided section per line and strips a leading -/* bullet.
    decided = []
    for line in _section(text, "What's Already Decided").splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith(("- ", "* ")):
            s = s[2:].strip()
        elif s.startswith("-") and len(s) > 1:
            s = s[1:].strip()
        decided.append(s)

    title = title_match.group(1).strip() if title_match else (fallback_title or questions[0].title)
    return Brief(title=title, decided=decided, context=_section(text, "Context"), questions=questions)


def slugify(title: str, max_length: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")
    return slug or "untitled"
