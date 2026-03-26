"""Decision ledger — append-only constraint log."""
import re
from pathlib import Path
from agentteam.session.persistence import COMPLETION_MARKER, read_without_marker, write_with_marker

def get_ledger_path(session_dir: Path) -> Path:
    return session_dir / "decisions_ledger.md"

def read_ledger(session_dir: Path) -> str:
    path = get_ledger_path(session_dir)
    return read_without_marker(path) if path.exists() else ""

def extract_ledger_section(design_doc: str) -> str | None:
    match = re.search(r"## Ledger\s*\n(.*?)(?=\n## |\Z)", design_doc, re.DOTALL)
    return match.group(0).strip() if match else None

def hallucination_check(design_doc: str, ledger_section: str, ratio_max: float = 4.0, ratio_min: float = 0.2) -> bool:
    doc_decisions = len(re.findall(r"(?:^### D\d|^### [A-Z]|\d+\.\s+\*\*)", design_doc, re.MULTILINE))
    if doc_decisions == 0:
        doc_decisions = len(re.findall(r"^### ", design_doc, re.MULTILINE))
    ledger_decisions = ledger_section.count("- DECIDED:")
    if doc_decisions == 0: return True
    ratio = ledger_decisions / doc_decisions
    return not (ratio > ratio_max or ratio < ratio_min)

def append_to_ledger(session_dir: Path, ledger_section: str, q_num: int):
    path = get_ledger_path(session_dir)
    existing = path.read_text(encoding="utf-8").replace(COMPLETION_MARKER, "").replace("<!-- complete -->", "") if path.exists() else ""
    if f"### Q{q_num}:" in existing: return
    write_with_marker(path, existing.rstrip() + "\n\n" + ledger_section + "\n")
