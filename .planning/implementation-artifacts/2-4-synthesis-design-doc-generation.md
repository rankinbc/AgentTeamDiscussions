# Story 2.4: Synthesis & Design Doc Generation

Status: done

## Story

As a user,
I want agent responses synthesized into a structured design document after each question,
So that I get actionable decisions rather than raw conversation transcripts.

## Acceptance Criteria

1. **Given** three rounds of agent responses for a question
   **When** the synthesis step runs
   **Then** it calls Claude with all round responses assembled into a structured input and a synthesis system prompt

2. **Given** synthesis completes successfully
   **When** the design doc is returned
   **Then** the output follows the design doc template: decision-with-rationale, exclusions ("what was cut and why"), blocking open items, non-blocking open items

3. **Given** synthesis output is available
   **When** the design doc is written to disk
   **Then** it is written to the session's questions directory with UTF-8 encoding via `write_with_marker`

4. **Given** the synthesis call to Claude fails or returns an empty/minimal response
   **When** the failure is detected
   **Then** the function raises an exception (caller is responsible for cascade handling — no data loss)

## Tasks / Subtasks

- [x] Task 1: Create `agentteam/synthesis/doc.py` (AC: 1–4)
  - [x] 1.1: Add module docstring: `"""Design doc synthesis — calls Claude to merge round responses into a structured design document."""`
  - [x] 1.2: Add `build_synthesis_input(question, round_responses, round_labels, decisions, prior_specs,
        open_questions) -> str` — assembles all round text into the synthesis input payload
  - [x] 1.3: Add `async def synthesize(question, round_responses, round_labels, system_prompt, timeout,
        decisions="", prior_specs="", open_questions="") -> str` — calls `run_claude_async` and returns
        the design doc; raises `RuntimeError` if output is empty or under 50 chars
  - [x] 1.4: No `print()`, no `logging` — pure library; no `AGENT_DISPLAY_NAMES` import

- [x] Task 2: Export from `agentteam/synthesis/__init__.py` (AC: 1)
  - [x] 2.1: Add `from .doc import build_synthesis_input, synthesize`
  - [x] 2.2: Add both to `__all__`

- [x] Task 3: Add tests in `_SYSTEM/tests/test_synthesis_doc.py` (AC: 1–4)
  - [x] 3.1: Create new test file with module docstring
  - [x] 3.2: `TestBuildSynthesisInput` class:
    - `test_contains_question_title` — question title appears in output
    - `test_contains_question_body` — question body appears in output
    - `test_contains_round_label` — each round label appears as a section header
    - `test_contains_agent_responses` — agent response text appears in output
    - `test_contains_decisions_when_provided` — decisions block present when non-empty
    - `test_omits_decisions_when_empty` — no decisions section when decisions=""
    - `test_contains_prior_specs_when_provided` — prior specs block present when non-empty
    - `test_round_order_preserved` — rounds appear in `round_labels` order
  - [x] 3.3: `TestSynthesize` class (mock `run_claude_async`):
    - `test_returns_string_on_success` — returns non-empty string from Claude
    - `test_raises_on_empty_response` — empty string response raises RuntimeError
    - `test_raises_on_short_response` — response under 50 chars raises RuntimeError
    - `test_passes_system_prompt` — system_prompt arg is passed as first arg to `run_claude_async`
    - `test_passes_timeout` — timeout arg is passed through to `run_claude_async`
    - `test_input_contains_synthesis_instruction` — the assembled input ends with synthesis directive

## Dev Notes

### BROWNFIELD: Synthesis Logic Already Exists in Engine

**DO NOT** modify `discussion/engine.py`. The existing `synthesize()` there stays unchanged.
It is used by `run_question()` and `run_question_with_cascade()` in the same file/runner.

**The only gap:** `agentteam/synthesis/doc.py` doesn't exist yet. Create it as a clean,
engine-agnostic library module. The `synthesis/` package currently only has `live.py`
(rolling snapshots for live conversation — separate concern).

### New Module: `agentteam/synthesis/doc.py`

**Key difference from `discussion/engine.py`'s `synthesize()`:**

| Feature | `discussion/engine.py` | `agentteam/synthesis/doc.py` |
|---|---|---|
| System prompt source | `SYNTHESIS_SYSTEM_PROMPT` global loaded at import | `system_prompt: str` parameter |
| Agent display names | `AGENT_DISPLAY_NAMES.get(key, key)` | Agent key directly (no lookup) |
| Failure handling | Returns whatever Claude returns (caller checks) | Raises `RuntimeError` on empty/short |
| Dependencies | `config_loader` (engine-local) | Only `agentteam.runner.claude` |

**`build_synthesis_input` — assembles the synthesis user-message:**
```python
def build_synthesis_input(
    question: dict,
    round_responses: dict[str, dict[str, str]],
    round_labels: list[str],
    decisions: str = "",
    prior_specs: str = "",
    open_questions: str = "",
) -> str:
    parts: list[str] = []
    parts.append(f"# Design Question: {question['title']}\n\n## The Question\n\n{question['body']}")

    if decisions:
        parts.append(f"## Prior Decisions (from brief)\n\n{decisions}")

    if prior_specs:
        parts.append(f"## Prior Design Docs\n\n{prior_specs}")

    if open_questions:
        parts.append(
            f"## Unresolved Open Questions from Prior Docs\n\n"
            f"Resolve any of these that this discussion addresses:\n\n{open_questions}"
        )

    for round_name in round_labels:
        responses = round_responses.get(round_name, {})
        label = "COUNTER-PROPOSAL" if round_name == "counter" else round_name.upper()
        section = f"## Round: {label}\n\n"
        for agent_key, response in responses.items():
            section += f"### {agent_key}\n\n{response}\n\n"
        parts.append(section.rstrip())

    parts.append(
        "Synthesize into a single design doc. No code. Focus on behavior and rules.\n\n"
        "IMPORTANT: Output ONLY the design doc. Start with '## Decisions'. "
        "Do not request file permissions, describe what you would write, or add any "
        "meta-commentary before or after the document."
    )

    return "\n\n".join(parts)
```

**`synthesize` — calls Claude and validates output:**
```python
_MIN_SYNTHESIS_LENGTH = 50  # chars — anything shorter is considered a failure

async def synthesize(
    question: dict,
    round_responses: dict[str, dict[str, str]],
    round_labels: list[str],
    system_prompt: str,
    timeout: int,
    decisions: str = "",
    prior_specs: str = "",
    open_questions: str = "",
) -> str:
    """Call Claude to synthesize round responses into a design doc.

    Raises RuntimeError if synthesis output is empty or too short to be useful.
    """
    synth_input = build_synthesis_input(
        question, round_responses, round_labels, decisions, prior_specs, open_questions
    )
    result = await run_claude_async(system_prompt, synth_input, timeout=timeout)
    if not result or len(result.strip()) < _MIN_SYNTHESIS_LENGTH:
        raise RuntimeError(
            f"Synthesis produced empty/minimal output ({len(result or '')} chars)"
        )
    return result
```

### `__init__.py` Update

Current `agentteam/synthesis/__init__.py`:
```python
"""Rolling synthesis engine."""
from .live import ConversationSnapshot, LiveSynthesizer
__all__ = ["ConversationSnapshot", "LiveSynthesizer"]
```

Add to it (do NOT change the existing live imports):
```python
from .doc import build_synthesis_input, synthesize
__all__ = ["ConversationSnapshot", "LiveSynthesizer", "build_synthesis_input", "synthesize"]
```

### Design Doc Template (from epics AC)

The synthesis system prompt (outside this story's scope — it's in `templates/prompts/synthesis.md.j2`)
instructs Claude to produce:
- `## Decisions` — decision with rationale
- `## Exclusions` — what was considered but cut and why
- `## Blocking Open Items` — questions that must be resolved before implementation
- `## Non-Blocking Open Items` — questions that can be resolved during implementation

This story does NOT define the synthesis prompt — it is passed as `system_prompt`. The session
runner (`discussion/engine.py`) loads `SYNTHESIS_SYSTEM_PROMPT` from config and passes it. New code
using this module will load the prompt via `ConfigLoader`.

### File Writing (AC 3)

The design doc writing to disk is handled by the **session runner** (`session/runner.py`), NOT by
`agentteam/synthesis/doc.py`. The library module returns the design doc string; the caller writes it.

Current runner writes to: `questions_dir / f"{q_num:02d}-{slug}.md"` (flat structure)
Architecture specifies: `sessions/{ts}/q{N}-{topic}/design-doc.md` (per-question subdirectory)

This naming discrepancy is **pre-existing**. Do NOT change the runner's file writing in this story.
The library module (`synthesize()`) is correct — it returns text, not a path.

AC 3 is satisfied by the library function returning the synthesizable string, which the caller
then writes with `write_with_marker` from `agentteam.session.persistence`.

### Test Architecture

```python
# _SYSTEM/tests/test_synthesis_doc.py
from unittest.mock import AsyncMock, patch
import pytest
from agentteam.synthesis.doc import _MIN_SYNTHESIS_LENGTH, build_synthesis_input, synthesize

SAMPLE_QUESTION = {"number": 1, "title": "How should auth work?", "body": "Describe the auth flow."}
SAMPLE_ROUND_RESPONSES = {
    "propose": {"agent_a": "I propose JWT tokens.", "agent_b": "I suggest OAuth2."},
    "critique": {"agent_c": "JWT has expiry issues.", "agent_d": "OAuth2 is complex."},
    "evaluate": {"agent_e": "JWT is better for our use case."},
}
ROUND_LABELS = ["propose", "critique", "evaluate"]
SYNTHESIS_PROMPT = "You are a neutral moderator. Synthesize the discussion."
```

**`test_input_contains_synthesis_instruction`:** Check `"Start with '## Decisions'"` appears
in the assembled input's final section.

**`test_round_order_preserved`:** Call `build_synthesis_input` with `round_labels=["evaluate", "propose"]`
and confirm "EVALUATE" appears before "PROPOSE" in the output string.

**`test_raises_on_short_response`:** Mock returns `"Too short"` (9 chars < `_MIN_SYNTHESIS_LENGTH`).

### Architecture Rules

- Line length: **100** (ruff)
- **No `print()` or `logging`** anywhere in `agentteam/` — pure library
- Python 3.11+ union syntax: `str | None`, not `Optional[str]`
- Module constant `_MIN_SYNTHESIS_LENGTH = 50` — use it in test imports

### Testing Rules

- New file: `_SYSTEM/tests/test_synthesis_doc.py`
- Run from `_SYSTEM/`: `python -m pytest tests/test_synthesis_doc.py -v`
- Mock `run_claude_async` for all async tests — no real Claude calls
- `asyncio_mode = "auto"` — no `@pytest.mark.asyncio`

### File Touch List

| File | Action |
|---|---|
| `_SYSTEM/agentteam/synthesis/doc.py` | New file — design doc synthesis function |
| `_SYSTEM/agentteam/synthesis/__init__.py` | Add `build_synthesis_input`, `synthesize` to imports + `__all__` |
| `_SYSTEM/tests/test_synthesis_doc.py` | New file — unit tests with mocked Claude |

### References

- [Source: _SYSTEM/projects/engine/discussion/engine.py#synthesize] — existing (L221-260)
- [Source: _SYSTEM/agentteam/synthesis/__init__.py] — current exports (extend, don't replace)
- [Source: _SYSTEM/agentteam/runner/claude.py] — `run_claude_async`
- [Source: _SYSTEM/agentteam/session/persistence.py] — `write_with_marker` (used by caller)
- [Source: _bmad-output/planning-artifacts/architecture.md] — synthesis module location
- [Source: _bmad-output/project-context.md] — 38 project rules

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List

- _SYSTEM/agentteam/synthesis/doc.py
- _SYSTEM/agentteam/synthesis/__init__.py
- _SYSTEM/tests/test_synthesis_doc.py

### Review Findings

- [x] [Review][Patch] Error string ≥50 chars from `run_claude_async` passes synthesis length check and returns as design doc [doc.py:synthesize] — `is_error_response()` not called; a long Claude CLI error message (e.g. rate-limit message) is silently returned as a valid design document
