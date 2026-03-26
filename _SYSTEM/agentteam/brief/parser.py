"""Discussion brief parser. Raises ValueError instead of sys.exit."""
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Brief:
    """Structured representation of a parsed discussion brief."""
    product_description: str
    constraints: list[str] = field(default_factory=list)
    questions: list[dict] = field(default_factory=list)


class BriefParseError(ValueError):
    pass


def parse_brief(path: Path) -> tuple[str, list[dict]]:
    """Parse a discussion brief. Returns (decisions_text, questions_list)."""
    text = path.read_text(encoding="utf-8")
    decisions_match = re.search(r"## What's Already Decided\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    decisions = decisions_match.group(1).strip() if decisions_match else ""
    questions_match = re.search(r"## Open Questions[^\n]*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not questions_match:
        raise BriefParseError("No 'Open Questions' section found in brief.")
    questions_text = questions_match.group(1).strip()
    pattern = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*?)(?=^\d+\.\s+\*\*|\Z)", re.MULTILINE | re.DOTALL)
    questions = [{"number": int(m.group(1)), "title": m.group(2).strip(), "body": m.group(3).strip()}
                 for m in pattern.finditer(questions_text)]
    if not questions:
        raise BriefParseError("No questions parsed from brief.")
    return decisions, questions


def parse_brief_structured(path: Path) -> Brief:
    """Parse a discussion brief into a structured Brief object.

    Returns a Brief with product_description, constraints (list[str]),
    and questions (list[dict] with number/title/body keys).
    Raises BriefParseError if the Open Questions section is missing or empty.
    """
    text = path.read_text(encoding="utf-8")

    # Product description: H1 title + any text before the first ## heading
    pre_section = re.split(r"^##\s+", text, maxsplit=1, flags=re.MULTILINE)[0]
    product_description = re.sub(r"^#\s+", "", pre_section, count=1).strip()

    # Constraints: bullet items from "What's Already Decided"
    constraints: list[str] = []
    decided_match = re.search(
        r"## What's Already Decided\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL
    )
    if decided_match:
        for line in decided_match.group(1).splitlines():
            stripped = line.strip()
            if stripped.startswith("- ") or stripped.startswith("* "):
                constraints.append(stripped[2:].strip())
            elif stripped.startswith("-") and len(stripped) > 1:
                constraints.append(stripped[1:].strip())

    # Questions: numbered items from "Open Questions"
    questions_match = re.search(
        r"## Open Questions[^\n]*\n(.*?)(?=\n## |\Z)", text, re.DOTALL
    )
    if not questions_match:
        raise BriefParseError("No 'Open Questions' section found in brief.")
    questions_text = questions_match.group(1).strip()
    pattern = re.compile(
        r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*?)(?=^\d+\.\s+\*\*|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    questions = [
        {"number": int(m.group(1)), "title": m.group(2).strip(), "body": m.group(3).strip()}
        for m in pattern.finditer(questions_text)
    ]
    if not questions:
        raise BriefParseError("No questions parsed from brief.")

    return Brief(
        product_description=product_description,
        constraints=constraints,
        questions=questions,
    )


def slugify(title: str, max_length: int = 60) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:max_length].strip("-") or "untitled"
