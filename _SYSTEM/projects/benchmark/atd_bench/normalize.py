"""Put every condition's design doc in the same shape before judging.

The judge should compare substance, not tells. So we drop the engine's title and
"*Generated: ...*" header, drop the mechanical "## Ledger" appendix, and replace agent
names and persona titles with a neutral word.
"""

from __future__ import annotations

import re
from pathlib import Path

NEUTRAL = "a reviewer"


def load_display_names(engine_root: Path) -> list[str]:
    """Names to scrub: agent keys, full display names, and the short name before '('."""
    import yaml

    path = engine_root / "config" / "agent_display.yaml"
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    names: set[str] = set()
    for key, display in (data.get("display_names") or {}).items():
        names.add(key)
        names.add(key.replace("_", " "))
        display = str(display)
        names.add(display)
        short = display.split("(")[0].strip()
        if short:
            names.add(short)
            if short.lower().startswith("the "):
                names.add(short[4:])
    return sorted((n for n in names if len(n) > 2), key=len, reverse=True)


def strip_engine_header(text: str) -> str:
    text = text.lstrip("﻿")
    text = re.sub(r"\A\s*#\s[^\n]*\n", "", text)
    text = re.sub(r"\A\s*\*Generated:[^\n]*\n", "", text)
    return text.strip()


def strip_ledger(text: str) -> str:
    return re.split(r"^## Ledger\s*$", text, maxsplit=1, flags=re.M)[0].strip()


def role_nouns(names: list[str]) -> list[str]:
    """Short forms like "the Architect" from "The Cognitive Architect". Matched only when
    capitalized, so ordinary words such as "orchestrator" in prose are left alone."""
    nouns = {n.split()[-1] for n in names if n.lower().startswith("the ") and "(" not in n and len(n.split()) >= 3}
    return sorted(nouns)


def anonymize(text: str, names: list[str]) -> str:
    for name in names:
        text = re.sub(rf"(?<![\w-]){re.escape(name)}(?![\w-])", NEUTRAL, text, flags=re.I)
    for noun in role_nouns(names):
        text = re.sub(rf"\b(?:[Tt]he )?{re.escape(noun)}(?=\b)", NEUTRAL, text)
    # The plain panel's moderator may name "Panelist 3"; treat it like an agent name.
    return re.sub(r"\bpanelist\s+\d+\b", NEUTRAL, text, flags=re.I)


def normalize_doc(text: str, names: list[str]) -> str:
    return anonymize(strip_ledger(strip_engine_header(text)), names)


def decisions_section(text: str) -> str:
    """The '## Decisions' section, carried forward as prior decisions for later questions."""
    m = re.search(r"^## Decisions[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))
