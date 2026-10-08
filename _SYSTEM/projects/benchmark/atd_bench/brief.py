"""Load what the engine discussed: questions, decided constraints, context, and its design docs.

The engine session's session.json is the source of truth for the questions, so every
condition answers exactly what the engine answered. The brief file is read only for
the parts session.json does not store (product description and the ## Context section),
using the same section rules as Brief/BriefParser.cs.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROUND_SUFFIXES = ("-transcript", "-propose", "-critique", "-evaluate", "-counter")


@dataclass
class Question:
    number: int
    title: str
    body: str


@dataclass
class Brief:
    title: str
    description: str
    decided: list[str]
    context: str
    questions: list[Question]
    team: str = ""
    mode: str = ""


@dataclass
class EngineDoc:
    number: int
    path: Path
    text: str
    seconds: float | None = None


@dataclass
class EngineSession:
    path: Path
    brief: Brief
    docs: dict[int, EngineDoc] = field(default_factory=dict)


def _section(text: str, heading: str) -> str:
    """Body of a level-2 section, ending at the next level-2 heading (BriefParser rule)."""
    m = re.search(rf"^## {heading}[^\n]*\n(.*?)(?=\n## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def parse_brief_text(text: str) -> Brief:
    """Python port of BriefParser.Parse for full briefs."""
    text = text.lstrip("﻿")
    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    pre = re.split(r"^##\s+", text, maxsplit=1, flags=re.M)[0]
    description = re.sub(r"^#\s+.*$", "", pre, flags=re.M).strip()

    decided_block = _section(text, "What's Already Decided")
    decided = [ln.strip()[2:].strip() for ln in decided_block.splitlines() if ln.strip().startswith("- ")]

    questions: list[Question] = []
    q_block = _section(text, "Open Questions")
    for m in re.finditer(r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*?)(?=^\d+\.\s+\*\*|\Z)", q_block, re.M | re.S):
        questions.append(Question(int(m.group(1)), m.group(2).strip(), m.group(3).strip()))

    return Brief(
        title=title_m.group(1).strip() if title_m else "Untitled",
        description=description,
        decided=decided,
        context=_section(text, "Context"),
        questions=questions,
    )


def _resolve_brief_path(session_json: dict, engine_root: Path) -> Path | None:
    source = session_json.get("source") or ""
    name = re.split(r"[\\/]", source)[-1] if source else ""
    candidate = engine_root / "input" / name
    return candidate if name and candidate.exists() else None


def _doc_seconds(text: str) -> float | None:
    m = re.search(r"^\*Generated:[^*]*\|\s*(\d+(?:\.\d+)?)s\s*\|", text, re.M)
    return float(m.group(1)) if m else None


def load_engine_session(session_dir: Path, brief_path: Path | None = None) -> EngineSession:
    session_dir = Path(session_dir)
    manifest = json.loads((session_dir / "session.json").read_text(encoding="utf-8-sig"))
    engine_root = session_dir.parent.parent.parent  # engine/output/sessions/<id>

    brief_path = brief_path or _resolve_brief_path(manifest, engine_root)
    parsed = parse_brief_text(brief_path.read_text(encoding="utf-8-sig")) if brief_path else None

    brief = Brief(
        title=parsed.title if parsed else manifest.get("title", session_dir.name),
        description=parsed.description if parsed else "",
        decided=list(manifest.get("decided") or (parsed.decided if parsed else [])),
        context=parsed.context if parsed else "",
        questions=[Question(q["number"], q["title"], q.get("body", "")) for q in manifest["questions"]],
        team=manifest.get("team", ""),
        mode=manifest.get("mode", ""),
    )

    docs: dict[int, EngineDoc] = {}
    for f in sorted((session_dir / "questions").glob("*.md")):
        m = re.match(r"^(\d+)-", f.name)
        if not m or f.stem.endswith(ROUND_SUFFIXES):
            continue
        text = f.read_text(encoding="utf-8-sig")
        docs[int(m.group(1))] = EngineDoc(int(m.group(1)), f, text, _doc_seconds(text))

    return EngineSession(session_dir, brief, docs)


def load_round_counts(engine_root: Path, team: str, mode: str) -> dict[str, int]:
    """Agents per round for the session's team mode, so the plain panel mirrors its shape."""
    import yaml

    default = {"propose": 2, "critique": 2, "evaluate": 2}
    team_file = engine_root / "data" / "teams" / f"{team}.yaml"
    if not team or not team_file.exists():
        return default
    data = yaml.safe_load(team_file.read_text(encoding="utf-8")) or {}
    modes = data.get("modes") or {}
    chosen = modes.get(mode or data.get("default_mode", ""), {})
    groups = chosen.get("groups") or {}
    return {name: len(agents) for name, agents in groups.items()} or default
