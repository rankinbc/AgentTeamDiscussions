"""Crash-safe session files — port of SessionPersistence.cs, DecisionsLedger.cs
and the session.json shape from SessionConfig.cs.

Every persisted artifact ends with the completion marker; a file without it is
treated as never written. session.json carries an extra `plugin` block (speaking
orders, the pending step, timing) that the C# engine ignores on read.
"""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

MARKER = "\n<!-- complete -->\n"
MARKER_TEXT = "<!-- complete -->"


def write_with_marker(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
        f.write(MARKER)
        f.flush()


def is_complete(path: Path) -> bool:
    try:
        return path.exists() and MARKER_TEXT in path.read_text(encoding="utf-8")
    except OSError:
        return False


def read_without_marker(path: Path) -> str:
    text = path.read_text(encoding="utf-8").lstrip("﻿")
    return text.replace(MARKER, "").replace(MARKER_TEXT, "").strip()


def _dotnet_json_string(text: str) -> str:
    """System.Text.Json default encoding: `"`, `'`, `<`, `>`, `&`, `+`, controls and
    non-ASCII become \\uXXXX (lowercase hex); backslash is doubled."""
    out = []
    for ch in text:
        code = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch in '"\'<>&+' or code < 0x20 or code > 0x7E:
            out.append(f"\\u{code:04x}")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def hash_question_list(questions) -> str:
    """SHA256 over the C# JSON serialization of [{"n":1,"t":"title"}, ...] (SessionPersistence.HashQuestionList)."""
    payload = "[" + ",".join(f'{{"n":{q.number},"t":{_dotnet_json_string(q.title)}}}' for q in questions) + "]"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def create_session_dir(sessions_root: Path, slug: str) -> Path:
    name = f"{datetime.now().strftime('%Y-%m-%d_%H%M')}_{slug}"
    session_dir = sessions_root / name
    (session_dir / "questions").mkdir(parents=True, exist_ok=True)
    (session_dir / "work").mkdir(exist_ok=True)
    return session_dir


# --- session.json -----------------------------------------------------------

def session_path(session_dir: Path) -> Path:
    return session_dir / "session.json"


def new_session_config(brief, *, team: str, agents, mode: str, source: str, timeout: int = 120) -> dict:
    return {
        "version": 1,
        "created": datetime.now(timezone.utc).isoformat(),
        "title": brief.title,
        "decided": list(brief.decided),
        "context": brief.context,
        "questions": [{"number": q.number, "title": q.title, "body": q.body} for q in brief.questions],
        "team": team,
        "agents": list(agents) if agents else None,
        "mode": mode,
        "timeout": timeout,
        "source": source,
        "question_hash": hash_question_list(brief.questions),
        "state": {
            "status": "ready",
            "session_complete": False,
            "total_elapsed_seconds": 0,
            "completed_questions": 0,
            "failed_questions": 0,
            "questions": {},
        },
        "plugin": {"orders": {}, "pending": None, "started": None, "question_started": {}},
    }


def write_session(session_dir: Path, config: dict) -> None:
    clean = {k: v for k, v in config.items() if v is not None}
    with open(session_path(session_dir), "w", encoding="utf-8", newline="\n") as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)


def load_session(session_dir: Path) -> dict:
    with open(session_path(session_dir), encoding="utf-8") as f:
        config = json.load(f)
    config.setdefault("state", {}).setdefault("questions", {})
    config.setdefault("plugin", {"orders": {}, "pending": None, "started": None, "question_started": {}})
    return config


# --- Decisions ledger ----------------------------------------------------------

def ledger_path(session_dir: Path) -> Path:
    return session_dir / "decisions_ledger.md"


def read_ledger(session_dir: Path) -> str:
    p = ledger_path(session_dir)
    return read_without_marker(p) if p.exists() else ""


def extract_ledger_section(design_doc: str):
    m = re.search(r"## Ledger\s*\n(.*?)(?=\n## |\Z)", design_doc, re.S)
    if m:
        return m.group(0).strip()
    decisions = re.search(r"## Decisions\s*\n(.*?)(?=\n## |\Z)", design_doc, re.S)
    if not decisions:
        return None
    headings = re.findall(r"^### (.+)$", decisions.group(1), re.M)
    if not headings:
        return None
    return "\n".join(f"- DECIDED: {h.strip()}" for h in headings)


def fallback_ledger_entry(number: int, title: str) -> str:
    return f"### Q{number}: {title[:40]}\n- DECIDED: See design doc for details\n"


def hallucination_check(design_doc: str, ledger_section: str, ratio_max=4.0, ratio_min=0.2) -> bool:
    doc_decisions = len(re.findall(r"(?:^### D\d|^### [A-Z]|\d+\.\s+\*\*)", design_doc, re.M))
    if doc_decisions == 0:
        doc_decisions = len(re.findall(r"^### ", design_doc, re.M))
    if doc_decisions == 0:
        return True
    ledger_decisions = len(re.findall(r"- (DECIDED|CONTESTED):", ledger_section))
    ratio = ledger_decisions / doc_decisions
    return ratio_min <= ratio <= ratio_max


def append_to_ledger(session_dir: Path, ledger_section: str, number: int, title: str) -> None:
    existing = read_ledger(session_dir)
    header = f"### Q{number}:"
    if header in existing:
        return
    if header not in ledger_section:
        ledger_section = f"### Q{number}: {title[:60]}\n{ledger_section}"
    content = (existing.rstrip() + "\n\n" + ledger_section + "\n") if existing else ledger_section + "\n"
    write_with_marker(ledger_path(session_dir), content)
