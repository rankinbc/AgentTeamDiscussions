# Story 2.5: Transcript & Session Output

Status: done

## Story

As a user,
I want human-readable transcripts for each question showing all agent responses,
So that I can review the full discussion and understand how decisions were reached.

## Acceptance Criteria

1. **Given** completed discussion rounds for a question
   **When** the transcript writer runs
   **Then** per-round transcript files are written: `round-1-propose.md`, `round-2-critique.md`, `round-3-evaluate.md`

2. **Given** a round transcript is written
   **When** the file is read
   **Then** it shows agent name, role (from `position.role`), and full response text in readable markdown

3. **Given** all round transcripts for a question are written
   **When** the session folder is inspected
   **Then** files exist at `{question_dir}/round-{N}-{round_name}.md` with UTF-8 encoding and valid markdown

4. **Given** the `write_atomic` utility
   **When** it writes any session file
   **Then** it writes to `{path}.tmp` first and then uses `os.replace()` to atomically replace the target

## Tasks / Subtasks

- [x] Task 1: Create `agentteam/utils/io.py` (AC: 4)
  - [x] 1.1: Add module docstring: `"""Atomic file I/O utility."""`
  - [x] 1.2: Add `write_atomic(path: Path | str, content: str, encoding: str = "utf-8") -> None`
    — writes to `{path}.tmp`, then calls `os.replace(tmp, path)`
    — parent directory must already exist (caller's responsibility)
  - [x] 1.3: No `print()`, no `logging` — pure utility

- [x] Task 2: Create `agentteam/utils/__init__.py` (AC: 4)
  - [x] 2.1: Add `from .io import write_atomic`
  - [x] 2.2: Add `__all__ = ["write_atomic"]`

- [x] Task 3: Create `agentteam/output/transcripts.py` (AC: 1–3)
  - [x] 3.1: Add module docstring: `"""Per-round transcript formatting and writing."""`
  - [x] 3.2: Add `format_round_transcript(question, round_num, round_name, responses, team) -> str`
    — header: `# Round {round_num}: {label}\n\n*Question: {question['title']}*`
    — for each agent in responses: `## {agent.name} ({agent.position.role})\n\n{response}`
    — label: `"COUNTER-PROPOSAL"` when `round_name == "counter"`, else `round_name.upper()`
    — agents not in team.agents are emitted with key only (no role)
    — returns formatted markdown string, no I/O
  - [x] 3.3: Add `write_round_transcripts(question_dir, round_responses, round_labels, question, team) -> list[Path]`
    — iterates `enumerate(round_labels, start=1)` to get `round_num, round_name`
    — for each round: formats via `format_round_transcript`, writes via `write_atomic`
    — file path: `question_dir / f"round-{round_num}-{round_name}.md"`
    — returns list of written Path objects
    — raises `ValueError` if `question_dir` does not exist
  - [x] 3.4: No `print()`, no `logging`, no `AGENT_DISPLAY_NAMES` import

- [x] Task 4: Create `agentteam/output/__init__.py` (AC: 1)
  - [x] 4.1: Add `from .transcripts import format_round_transcript, write_round_transcripts`
  - [x] 4.2: Add `__all__ = ["format_round_transcript", "write_round_transcripts"]`

- [x] Task 5: Add tests `_SYSTEM/tests/test_utils_io.py` (AC: 4)
  - [x] 5.1: `TestWriteAtomic` class:
    - `test_writes_content` — file exists with correct content after write
    - `test_tmp_file_cleaned_up` — `.tmp` file does not exist after write
    - `test_overwrites_existing_file` — subsequent write replaces file correctly
    - `test_encoding_utf8` — content with non-ASCII chars round-trips correctly
    - `test_parent_must_exist` — raises when parent dir is missing
  - [x] 5.2: Use `tmp_path` pytest fixture — never write to real session directories

- [x] Task 6: Add tests `_SYSTEM/tests/test_output_transcripts.py` (AC: 1–3)
  - [x] 6.1: `TestFormatRoundTranscript` class:
    - `test_header_contains_round_num_and_label` — `# Round 1: PROPOSE` in output
    - `test_header_contains_question_title` — question title in header
    - `test_agent_name_and_role` — `## Alice (Systems Architect)` pattern present
    - `test_response_text_present` — agent response appears in output
    - `test_counter_label_formatted` — round_name `"counter"` → `COUNTER-PROPOSAL`
    - `test_multiple_agents_ordered` — all agents in responses appear in output
    - `test_unknown_agent_key_no_crash` — agent_key not in team → emits key with no role
  - [x] 6.2: `TestWriteRoundTranscripts` class:
    - `test_creates_round_files` — all three round files exist after call
    - `test_file_names_correct` — `round-1-propose.md`, `round-2-critique.md`, `round-3-evaluate.md`
    - `test_returns_paths` — return value is list of Path objects pointing to written files
    - `test_file_content_readable_markdown` — written file contains expected markdown header
    - `test_raises_when_dir_missing` — `ValueError` when `question_dir` does not exist
    - `test_utf8_encoding` — verify file readable with UTF-8

## Dev Notes

### Architecture: Two New Modules

This story introduces two previously-missing library modules:

| Module | Purpose |
|---|---|
| `agentteam/utils/io.py` | `write_atomic` — atomic write pattern, prerequisite for all session writes |
| `agentteam/output/transcripts.py` | Per-round transcript formatting and file writing |

Both are **pure library code** — no print, no logging, no config_loader, no AGENT_DISPLAY_NAMES.

### CRITICAL: `write_atomic` vs `write_with_marker`

`agentteam/session/persistence.py` already has `write_with_marker`. **Do NOT use it here.**

The architecture mandates `write_atomic` (`os.replace` pattern) for all session output files.
`write_with_marker` is a legacy crash-detection pattern from the brownfield codebase.
The new `agentteam/utils/io.py` `write_atomic` is the authoritative pattern going forward.

```python
# CORRECT for this story and all future session writes
from agentteam.utils.io import write_atomic
write_atomic(question_dir / "round-1-propose.md", content)

# WRONG — do not use for session output files
with open(path, "w") as f: f.write(content)
```

### `write_atomic` Implementation

```python
import os
from pathlib import Path

def write_atomic(path: Path | str, content: str, encoding: str = "utf-8") -> None:
    """Write content to path atomically: write to .tmp, then os.replace."""
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding=encoding)
    os.replace(tmp, path)
```

`os.replace()` is atomic on POSIX (rename syscall) and on Windows NTFS. The `.tmp` file is always in the same directory so `os.replace` is always same-filesystem (required for rename atomicity).

### Transcript Format (AC 2)

```markdown
# Round 1: PROPOSE

*Question: How should auth work?*

## Alice (Systems Architect)

I propose JWT tokens because they are stateless and...

## Bob (Devil's Advocate)

Stateless tokens complicate revocation. Consider...
```

Key rules:
- Header: `# Round {N}: {LABEL}` — `N` is 1-based position in `round_labels`
- Subheader: `## {agent.name} ({agent.position.role})`
- `agent.name` comes from `team.agents[key].name`
- `agent.position.role` comes from `team.agents[key].position.role` (default: `"participant"`)
- If `agent_key` not in `team.agents`: emit `## {agent_key}` (no role) — do not crash

### Round Number Derivation

The caller passes `round_labels` in order. The round number is `enumerate(..., start=1)`:

```python
for round_num, round_name in enumerate(round_labels, start=1):
    content = format_round_transcript(question, round_num, round_name,
                                       round_responses.get(round_name, {}), team)
    path = question_dir / f"round-{round_num}-{round_name}.md"
    write_atomic(path, content)
    paths.append(path)
```

This means the file names match the standard `round-1-propose.md`, `round-2-critique.md`, `round-3-evaluate.md` when `round_labels = ["propose", "critique", "evaluate"]`.

### BROWNFIELD: Engine Already Writes Transcripts

`projects/engine/discussion/engine.py` has `format_transcript()` at line 263 which writes a **single combined transcript** per question (`{filename}-transcript.md`). The new architecture writes **per-round files** instead.

**DO NOT** modify `discussion/engine.py`. The existing engine transcript remains unchanged. The new `agentteam/output/transcripts.py` is a clean, engine-agnostic library version.

### Session Folder Structure (AC 3)

The `question_dir` passed to `write_round_transcripts` is the per-question subdirectory created by the session runner. This story is responsible for the round files only:

```
sessions/{timestamp}/
└── q01-payment-flow/          ← caller creates this directory
    ├── design-doc.md          ← written by synthesize (Story 2.4)
    ├── round-1-propose.md     ← written by this story ✓
    ├── round-2-critique.md    ← written by this story ✓
    └── round-3-evaluate.md    ← written by this story ✓
```

The session runner (Story 2.2) is responsible for creating the `q{N:02d}-{slug}/` directory.

### Architecture Rules

- Line length: **100** (ruff)
- **No `print()` or `logging`** anywhere in `agentteam/` — pure library
- Python 3.11+ union syntax: `Path | str`, not `Union[Path, str]`
- Import `from agentteam.utils.io import write_atomic` — never `open(path, "w")`
- Use `tmp_path` pytest fixture for all file I/O tests

### Testing Rules

- Run from `_SYSTEM/`: `python -m pytest tests/test_utils_io.py tests/test_output_transcripts.py -v`
- `asyncio_mode = "auto"` in pyproject.toml — no `@pytest.mark.asyncio` needed
- `test_parent_must_exist` in `TestWriteAtomic`: use `tmp_path / "nonexistent_dir" / "file.md"` and assert `FileNotFoundError` or `OSError` is raised
- `test_unknown_agent_key_no_crash`: pass an agent_key not in `team.agents` in the responses dict — verify no exception is raised and key appears in output

### File Touch List

| File | Action |
|---|---|
| `_SYSTEM/agentteam/utils/__init__.py` | New package init |
| `_SYSTEM/agentteam/utils/io.py` | New file — `write_atomic` |
| `_SYSTEM/agentteam/output/__init__.py` | New package init |
| `_SYSTEM/agentteam/output/transcripts.py` | New file — transcript formatting + writing |
| `_SYSTEM/tests/test_utils_io.py` | New file — unit tests for write_atomic |
| `_SYSTEM/tests/test_output_transcripts.py` | New file — unit tests for transcripts |

### Review Findings

- [x] [Review][Defer] Stale `.tmp` file not cleaned up on write failure [agentteam/utils/io.py] — deferred, pre-existing
- [x] [Review][Defer] Bare `KeyError` on missing `title` key in `question` dict [agentteam/output/transcripts.py] — deferred, pre-existing

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Atomic Write Pattern] — `write_atomic` spec, `os.replace` rationale
- [Source: _bmad-output/planning-artifacts/architecture.md#Project Directory Structure] — session folder layout
- [Source: _bmad-output/planning-artifacts/epics.md#Story 2.5] — acceptance criteria
- [Source: _SYSTEM/projects/engine/discussion/engine.py#format_transcript L263] — existing (brownfield) transcript format, do not modify
- [Source: _SYSTEM/agentteam/types/agent.py#PositionConfig L74] — `agent.position.role` field
- [Source: _SYSTEM/agentteam/session/persistence.py] — `write_with_marker` (do NOT use for new code)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Created `agentteam/utils/io.py` with `write_atomic` using `os.replace()` atomic pattern
- Created `agentteam/utils/__init__.py` exporting `write_atomic`
- Created `agentteam/output/transcripts.py` with `format_round_transcript` and `write_round_transcripts`
- Created `agentteam/output/__init__.py` exporting both transcript functions
- `format_round_transcript` uses `agent.name` and `agent.position.role`; unknown agent keys rendered without role (no crash)
- `write_round_transcripts` raises `ValueError` when `question_dir` does not exist
- 7 tests in `test_utils_io.py`, 14 tests in `test_output_transcripts.py` — all pass
- Fixed: `AgentConfig` requires `description` field in Pydantic model — added to `make_team` test fixture
- 203/203 tests passing (no regressions)

### File List

- _SYSTEM/agentteam/utils/__init__.py
- _SYSTEM/agentteam/utils/io.py
- _SYSTEM/agentteam/output/__init__.py
- _SYSTEM/agentteam/output/transcripts.py
- _SYSTEM/tests/test_utils_io.py
- _SYSTEM/tests/test_output_transcripts.py
