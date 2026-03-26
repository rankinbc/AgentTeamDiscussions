"""Parse BMAD workflow step files to extract questions for agent debate.

Scans .claude/skills/bmad-* directories, reads step files, and extracts
questions from markdown prose. Used as the fallback when no curated
debate prompts exist for a BMAD workflow.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ParsedWorkflowStep:
    step_number: int
    step_name: str
    questions: list[str] = field(default_factory=list)
    context_notes: str = ""


@dataclass
class ParsedWorkflow:
    name: str
    skill_path: str
    steps: list[ParsedWorkflowStep] = field(default_factory=list)
    template_path: str | None = None


# Patterns that indicate rhetorical or instruction questions (skip these)
_SKIP_PATTERNS = [
    r"^why would",
    r"^how could we not",
    r"^what if we",
    r"^shall we",
    r"^ready to",
    r"^want to",
    r"^should we proceed",
    r"^would you like",
    r"^can you",
    r"^do you want",
    r"^have you",
    r"^did you",
]

# Section headers in step files that signal question blocks
_QUESTION_SECTION_LABELS = [
    "questions", "ask", "gather", "discovery", "exploration",
    "considerations", "deep dive",
]


def _is_rhetorical(question: str) -> bool:
    """Check if a question is rhetorical or procedural (not worth debating)."""
    q_lower = question.lower().strip()
    for pattern in _SKIP_PATTERNS:
        if re.match(pattern, q_lower):
            return True
    # Skip very short questions (likely not substantive)
    if len(question) < 15:
        return True
    return False


def _in_code_block(lines: list[str], line_idx: int) -> bool:
    """Check if a line index is inside a fenced code block."""
    fence_count = 0
    for i in range(line_idx):
        if lines[i].strip().startswith("```"):
            fence_count += 1
    return fence_count % 2 == 1


def extract_questions(step_markdown: str) -> list[str]:
    """Extract debate-worthy questions from a BMAD step file's markdown."""
    lines = step_markdown.split("\n")
    questions = []
    seen = set()

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip code blocks
        if _in_code_block(lines, i):
            continue

        # Skip lines that are headers, frontmatter, or rule markers
        if stripped.startswith("#") or stripped.startswith("---") or stripped.startswith("- 🛑") or \
           stripped.startswith("- 📖") or stripped.startswith("- 🔄") or stripped.startswith("- 📋") or \
           stripped.startswith("- ✅") or stripped.startswith("- 🚫") or stripped.startswith("- 💬") or \
           stripped.startswith("- 🎯") or stripped.startswith("- 💾"):
            continue

        # Match lines ending with ? (the main heuristic)
        if stripped.endswith("?"):
            # Clean up list markers
            q = re.sub(r"^[-*•]\s*", "", stripped)
            q = re.sub(r"^\d+\.\s*", "", q)
            # Remove bold/italic markers
            q = q.replace("**", "").replace("*", "")
            # Remove leading quotes
            q = q.strip('"').strip("'").strip()

            if q and not _is_rhetorical(q) and q not in seen:
                seen.add(q)
                questions.append(q)

    return questions


def _parse_step_file(step_path: Path) -> ParsedWorkflowStep | None:
    """Parse a single step file into a ParsedWorkflowStep."""
    name = step_path.stem
    # Extract step number from filename like step-02-vision.md
    match = re.match(r"step-(\d+\w*)-(.+)", name)
    if not match:
        return None

    step_num_str = match.group(1)
    # Handle things like "01b" -> just use the numeric part
    step_num = int(re.match(r"(\d+)", step_num_str).group(1))
    step_name = match.group(2).replace("-", " ").title()

    text = step_path.read_text(encoding="utf-8")
    questions = extract_questions(text)

    # Extract context from the STEP GOAL section if present
    context = ""
    goal_match = re.search(r"## STEP GOAL:\s*\n\s*(.+?)(?:\n\n|\n##)", text, re.DOTALL)
    if goal_match:
        context = goal_match.group(1).strip()

    return ParsedWorkflowStep(
        step_number=step_num,
        step_name=step_name,
        questions=questions,
        context_notes=context,
    )


def parse_workflow(skill_path: str | Path) -> ParsedWorkflow:
    """Parse a BMAD workflow skill directory into a ParsedWorkflow."""
    skill_path = Path(skill_path)
    name = skill_path.name.replace("bmad-create-", "").replace("bmad-", "").replace("-", " ").title()

    # Find template file
    template = None
    for ext in ["*.template.md", "template.md"]:
        templates = list(skill_path.glob(ext))
        if templates:
            template = str(templates[0])
            break

    # Parse step files
    steps_dir = skill_path / "steps"
    steps = []
    # Skip init, continue, and complete steps (procedural, not debate-worthy)
    skip_names = {"init", "continue", "complete", "session-setup"}
    if steps_dir.exists():
        for step_file in sorted(steps_dir.glob("step-*.md")):
            stem = step_file.stem
            # Skip files like step-01-init, step-01b-continue, step-06-complete
            parts = stem.split("-", 2)
            step_label = parts[2] if len(parts) > 2 else ""
            if step_label in skip_names:
                continue
            parsed = _parse_step_file(step_file)
            if parsed and parsed.questions:
                steps.append(parsed)

    return ParsedWorkflow(
        name=name,
        skill_path=str(skill_path),
        steps=steps,
        template_path=template,
    )


def scan_bmad_workflows(skills_root: str | Path | None = None) -> list[dict]:
    """Scan for available BMAD workflows that can be used for agent debates.

    Returns list of dicts with keys: key, name, skill_path, has_steps
    """
    if skills_root is None:
        # Default: project root .claude/skills/
        skills_root = Path(__file__).resolve().parent.parent.parent / ".claude" / "skills"

    skills_root = Path(skills_root)
    if not skills_root.exists():
        return []

    workflows = []
    # Target workflows that produce structured artifacts
    target_prefixes = [
        "bmad-create-product-brief",
        "bmad-brainstorming",
        "bmad-create-prd",
        "bmad-create-architecture",
        "bmad-create-ux-design",
    ]

    for prefix in target_prefixes:
        skill_dir = skills_root / prefix
        if skill_dir.exists():
            steps_dir = skill_dir / "steps"
            has_steps = steps_dir.exists() and any(steps_dir.glob("step-*.md"))
            key = prefix.replace("bmad-create-", "").replace("bmad-", "")
            name = key.replace("-", " ").title()
            workflows.append({
                "key": key,
                "name": name,
                "skill_path": str(skill_dir),
                "has_steps": has_steps,
            })

    return workflows


def parsed_to_sections(workflow: ParsedWorkflow) -> list[dict]:
    """Convert parsed BMAD questions into debate-ready sections.

    Output format matches SPEC_SECTIONS structure so the existing
    conversation engine can drive them identically.
    """
    sections = []
    for step in workflow.steps:
        if not step.questions:
            continue
        q_text = "\n".join(f"- {q}" for q in step.questions)
        sections.append({
            "name": step.step_name,
            "bmad_step": step.step_number,
            "prompt": (
                f"Discuss these questions and reach consensus:\n{q_text}\n\n"
                f"Debate the answers. Challenge assumptions. The group must "
                f"converge on clear answers to each question."
            ),
            "extract": (
                f"Write concise answers to each question based on the discussion. "
                f"Use the agents' consensus where it exists, note dissent where it doesn't. "
                f"Output ONLY the answers."
            ),
            "output_section": f"## {step.step_name}",
        })
    return sections
