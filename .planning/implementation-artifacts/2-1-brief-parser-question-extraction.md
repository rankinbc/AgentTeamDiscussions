# Story 2.1: Brief Parser & Question Extraction

Status: done

## Story

As a user,
I want to write a markdown brief with my product idea and open questions,
so that the system can extract individual questions for sequential discussion.

## Acceptance Criteria

1. **Given** a markdown brief file with product description, constraints, and open questions sections
   **When** `parse_brief_structured(path)` processes it
   **Then** it returns a `Brief` dataclass with `product_description: str`, `constraints: list[str]`, `questions: list[dict]`

2. **Given** a valid brief
   **When** questions are extracted
   **Then** each dict has `number: int`, `title: str`, `body: str` keys — ready for the discussion loop

3. **Given** a brief missing the `## Open Questions` section
   **When** the parser processes it
   **Then** `BriefParseError` is raised with a clear message

4. **Given** a brief with `## Open Questions` but no numbered items
   **When** the parser processes it
   **Then** `BriefParseError` is raised with a clear message

5. **Given** a brief with no `## What's Already Decided` section
   **When** the parser processes it
   **Then** `Brief.constraints` is an empty list (not an error)

## Tasks / Subtasks

- [x] Task 1: Add `Brief` dataclass to `agentteam/brief/parser.py` (AC: 1)
  - [x] 1.1: Add `from dataclasses import dataclass` to stdlib imports at top of file
  - [x] 1.2: Define `Brief` as a `@dataclass` with fields: `product_description: str`, `constraints: list[str]`, `questions: list[dict]`
  - [x] 1.3: Place `Brief` definition before `BriefParseError` in the file

- [x] Task 2: Implement `parse_brief_structured(path: Path) -> Brief` (AC: 1, 2, 3, 4, 5)
  - [x] 2.1: Extract product description — H1 line (strip `# `) + any text between H1 and first `##` heading, joined and stripped
  - [x] 2.2: Parse constraints — reuse "What's Already Decided" regex; split into lines; strip `- ` or `* ` prefix; drop blank lines → `list[str]`
  - [x] 2.3: Parse questions — reuse existing "Open Questions" regex + numbered question pattern; return same `{number, title, body}` dicts
  - [x] 2.4: Raise `BriefParseError` (same messages as existing `parse_brief`) for missing section and empty question list
  - [x] 2.5: Add function after the existing `parse_brief` function, before `slugify`

- [x] Task 3: Update exports in `agentteam/brief/__init__.py` (AC: 1)
  - [x] 3.1: Import `Brief` and `parse_brief_structured` from `.parser`
  - [x] 3.2: Add both to `__all__`

- [x] Task 4: Add tests in `_SYSTEM/tests/test_brief_parser.py` (AC: 1–5)
  - [x] 4.1: Add `TestBrief` class — verify dataclass fields `product_description`, `constraints`, `questions` exist on an instance
  - [x] 4.2: Add `TestParseBriefStructured` class:
    - `test_returns_brief_instance` — result is a `Brief`
    - `test_product_description_from_h1_and_text` — H1 title + description text extracted
    - `test_product_description_no_h1` — brief with no H1 → product_description is text before first `##`
    - `test_constraints_parsed_as_list` — bullet items from "What's Already Decided" become `list[str]`
    - `test_constraints_strip_dash_prefix` — `"- Constraint"` → `"Constraint"` (no leading `- `)
    - `test_no_decided_section_gives_empty_constraints` — missing section → `[]`
    - `test_questions_have_correct_keys` — each question dict has `number`, `title`, `body`
    - `test_question_count` — correct number of questions extracted
    - `test_missing_open_questions_raises` — BriefParseError raised
    - `test_empty_questions_raises` — BriefParseError raised

## Dev Notes

### CRITICAL: Backward Compatibility — Do Not Break Existing `parse_brief`

`agentteam/brief/parser.py` already has a working `parse_brief(path: Path) -> tuple[str, list[dict]]`.
**DO NOT change this function's signature or behavior** — it is called at:
- `_SYSTEM/projects/engine/session/runner.py` line 74: `from agentteam.brief.parser import parse_brief, slugify`
- `_SYSTEM/lib/orchestrator/brief_parser.py` (shim that re-exports everything)

Also do not remove `BriefParseError` or `slugify` — both are exported and tested.

Existing tests in `TestParseBrief` and `TestSlugify` must continue passing.

### Brief File Format (real-world example from `briefs/v1-spec-gaps.md`)

```
# V1 Orchestrator Spec Gaps

An adversarial review of the V1 orchestrator spec found 13 issues.

## What's Already Decided

- V1 is a single-team system
- Agents are stateless claude -p CLI calls

## Open Questions

1. **How does the Morning Brief get generated?** Body text...
2. **How does decision extraction work?** Body text...
```

Product description = H1 line (sans `#`) + any text before first `##`. In the example: `"V1 Orchestrator Spec Gaps\n\nAn adversarial review..."`.

### Constraint Parsing Logic

```python
# From "What's Already Decided" section text, parse list items:
constraints = []
for line in decisions_text.splitlines():
    stripped = line.strip()
    if stripped.startswith("- ") or stripped.startswith("* "):
        constraints.append(stripped[2:].strip())
    elif stripped.startswith("-") and len(stripped) > 1:
        constraints.append(stripped[1:].strip())
```

### Product Description Extraction

```python
# Extract H1 title and text before first ## heading
h1_match = re.match(r"^#\s+(.+)", text, re.MULTILINE)
pre_section = re.split(r"^##\s+", text, maxsplit=1, flags=re.MULTILINE)[0]
# pre_section contains H1 line + description text
# Strip the "# " prefix from H1 line for clean output
product_description = re.sub(r"^#\s+", "", pre_section, count=1).strip()
```

### Architecture Rules (from project-context.md)

- `@dataclass` — not Pydantic — for `Brief` (parsed result, no field validation needed)
- `pathlib.Path` only — never `os.path`
- `encoding="utf-8"` on all file reads
- **NO `print()` or `logging`** anywhere in `agentteam/` — pure library
- Line length: **100** (ruff enforced, not 79/88)
- Import order: stdlib → third-party → local (ruff isort)
- Python 3.11+ union syntax: `str | None` not `Optional[str]`

### Testing Rules (from project-context.md)

- File: `_SYSTEM/tests/test_brief_parser.py` — **append** new classes, do NOT recreate file
- Run from `_SYSTEM/`: `python -m pytest tests/test_brief_parser.py`
- `asyncio_mode = "auto"` configured — no `@pytest.mark.asyncio` decorator
- Use `tmp_path` fixture for all file writes — never write to real dirs
- Test classes, not module-level functions
- The `sample_brief` fixture (in `conftest.py`) uses a brief with "What's Already Decided" and "Open Questions" but **no H1 title** — account for this in product description tests

### File Touch List

| File | Action |
|---|---|
| `_SYSTEM/agentteam/brief/parser.py` | Add `Brief` dataclass + `parse_brief_structured` function |
| `_SYSTEM/agentteam/brief/__init__.py` | Add `Brief`, `parse_brief_structured` to imports + `__all__` |
| `_SYSTEM/tests/test_brief_parser.py` | Append `TestBrief` and `TestParseBriefStructured` classes |

### References

- [Source: _SYSTEM/agentteam/brief/parser.py] — full existing implementation to extend
- [Source: _SYSTEM/agentteam/brief/__init__.py] — current 3-item exports
- [Source: _SYSTEM/tests/test_brief_parser.py] — existing tests (all must pass)
- [Source: _SYSTEM/tests/conftest.py] — `sample_brief` fixture (no H1, two questions)
- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.1] — acceptance criteria
- [Source: _bmad-output/project-context.md] — 38 implementation rules

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Added `Brief` dataclass (product_description, constraints, questions) with field defaults via `dataclasses.field`
- Added `parse_brief_structured()` reusing existing regex patterns; backward-compatible (existing `parse_brief` unchanged)
- Updated `__init__.py` exports to include `Brief` and `parse_brief_structured`
- 41 tests pass (21 existing + 20 new): `TestBrief` (5) + `TestParseBriefStructured` (15) + sample_brief fixture test
- Fixed test assertion: `sample_brief` constraints contain full bullet text ("We use Python 3.11+"), not substrings

### File List

- _SYSTEM/agentteam/brief/parser.py
- _SYSTEM/agentteam/brief/__init__.py
- _SYSTEM/tests/test_brief_parser.py

### Review Findings

- [x] [Review][Patch] `slugify` returns empty string for all-symbol input titles [parser.py:slugify] — `re.sub` produces `"-"`, `strip("-")` produces `""`, callers receive empty string with no error producing broken filenames
- [x] [Review][Patch] `slugify` can produce trailing hyphen after `max_length` truncation [parser.py:slugify] — `strip("-")` runs before the slice, so `slug[:max_length]` can re-expose a trailing hyphen (e.g. `"aaa-bbb-"` when cut lands on a hyphen-converted space)
- [x] [Review][Defer] IO exceptions from `read_text` not wrapped as `BriefParseError` [parser.py:18,36] — deferred, pre-existing design choice (module handles missing sections, not missing files)
- [x] [Review][Defer] BOM-prefixed UTF-8 files cause H1 stripping to fail in `parse_brief_structured` [parser.py:parse_brief_structured] — deferred, use `utf-8-sig` encoding to fix; low-priority edge case
