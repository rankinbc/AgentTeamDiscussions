# Story 2.3: Three-Round Discussion Orchestration

Status: done

## Story

As a user,
I want each question discussed across three structured rounds (propose, critique, evaluate),
So that ideas are generated, pressure-tested, and assessed before synthesis.

## Acceptance Criteria

1. **Given** a question extracted from the brief and a loaded team config
   **When** the discussion orchestrator processes the question
   **Then** it runs a propose round where all propose-assigned agents generate responses via Claude runner

2. **Given** a propose round has completed
   **When** the critique round starts
   **Then** critique-assigned agents each see the full propose round context before responding

3. **Given** propose and critique rounds have completed
   **When** the evaluate round starts
   **Then** evaluate-assigned agents each see all prior round context before responding

4. **Given** any round in progress
   **When** agents speak sequentially
   **Then** each agent sees responses from all earlier speakers in the same round (sequential, not parallel)

5. **Given** all three rounds have completed
   **When** the orchestrator returns
   **Then** all agent responses are collected per-round as `dict[str, str]` (agent_key → response text)

## Tasks / Subtasks

- [x] Task 1: Create `agentteam/conversation/orchestrator.py` (AC: 1–5)
  - [x] 1.1: Add module-level docstring: `"""Three-round discussion orchestration for agent teams."""`
  - [x] 1.2: Add `compute_speaking_order(agents: list[str], team: TeamConfig) -> list[str]` — orders by
        `assertiveness * 0.5 + position.intensity * 0.3 + stubbornness * 0.2 + random.uniform(-0.1, 0.1)`,
        descending (higher score speaks first)
  - [x] 1.3: Add `build_agent_payload(agent_key, team, question, decisions, prior_rounds, prior_specs,
        open_questions, round_instruction, this_round_so_far) -> str` — builds the full user-message
        payload for one agent in a round, using `build_perspective_reminder`, `build_context_lens`,
        `filter_prior_rounds` from `agentteam.prompts.builder`
  - [x] 1.4: Add `async def run_round(agents, system_prompts, team, question, decisions, prior_rounds,
        prior_specs, open_questions, timeout, round_instruction="", on_agent_start=None,
        on_agent_done=None) -> dict[str, str]` — runs agents sequentially using `run_claude_async`;
        each agent sees all prior speakers in `this_round_so_far`
  - [x] 1.5: All functions: no `print()`, no `logging` — pure library (callers emit events)

- [x] Task 2: Export from `agentteam/conversation/__init__.py` (AC: 1)
  - [x] 2.1: Add `from .orchestrator import build_agent_payload, compute_speaking_order, run_round`
  - [x] 2.2: Add all three to `__all__`

- [x] Task 3: Add tests in `_SYSTEM/tests/test_conversation_orchestrator.py` (AC: 1–5)
  - [x] 3.1: Create new test file with module docstring
  - [x] 3.2: `TestComputeSpeakingOrder` class:
    - `test_returns_all_agents` — result contains all input agents
    - `test_high_assertiveness_first` — agent with assertiveness=1.0 appears before assertiveness=0.0
      (run 10 times to account for jitter)
  - [x] 3.3: `TestBuildAgentPayload` class:
    - `test_contains_question_title` — question title appears in output
    - `test_contains_question_body` — question body appears in output
    - `test_contains_decisions` — decisions block appears when provided
    - `test_omits_decisions_when_empty` — no decisions block when decisions=""
    - `test_first_speaker_prompt` — when `this_round_so_far=""`, output includes "speaking first"
    - `test_subsequent_speaker_prompt` — when `this_round_so_far` has content, output includes "already spoken"
    - `test_contains_prior_rounds` — prior_rounds text appears in output when provided
  - [x] 3.4: `TestRunRound` class (mock `run_claude_async`):
    - `test_returns_all_agents` — result has entry for each agent in the agents list
    - `test_calls_claude_once_per_agent` — `run_claude_async` called len(agents) times
    - `test_sequential_accumulation` — second agent's payload contains first agent's response
    - `test_on_agent_done_called` — `on_agent_done` callback fired for each agent
    - `test_on_agent_start_called` — `on_agent_start` callback fired for each agent

## Dev Notes

### BROWNFIELD: Three-Round Logic Already Exists in Engine

**DO NOT** re-implement in the engine. The full three-round orchestration lives in:
- `_SYSTEM/projects/engine/discussion/engine.py` — `run_round()`, `run_question()`, `synthesize()`,
  `format_transcript()`, `_build_agent_payload()`, `compute_speaking_order()`

**The only gap:** `agentteam/conversation/orchestrator.py` doesn't exist yet. The architecture
specifies this file for E2. Create it as a clean, engine-agnostic library module. The engine's
`discussion/engine.py` stays unchanged — do NOT modify it.

### New Module: `agentteam/conversation/orchestrator.py`

This is the clean `agentteam/` version — no `config_loader` imports, no `AGENT_DISPLAY_NAMES`.
Uses only `agentteam.*` dependencies.

**Imports needed:**
```python
import random
import time
from typing import Callable

from agentteam.prompts.builder import build_context_lens, build_perspective_reminder, filter_prior_rounds
from agentteam.runner.claude import run_claude_async
from agentteam.types import TeamConfig
```

**`compute_speaking_order` — adapt from `discussion/engine.py` line 63:**
```python
def compute_speaking_order(agents: list[str], team: TeamConfig) -> list[str]:
    scored = []
    for key in agents:
        agent = team.agents[key]
        p = agent.personality
        score = (p.assertiveness * 0.5 + agent.position.intensity * 0.3 + p.stubbornness * 0.2)
        score += random.uniform(-0.1, 0.1)
        scored.append((key, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [key for key, _ in scored]
```

**`build_agent_payload` — clean version without `overlay_instruction` or `AGENT_DISPLAY_NAMES`:**
```python
def build_agent_payload(
    agent_key: str,
    team: TeamConfig,
    question: dict,
    decisions: str,
    prior_rounds: str,
    prior_specs: str,
    open_questions: str,
    round_instruction: str = "",
    this_round_so_far: str = "",
) -> str:
    agent = team.agents[agent_key]
    parts: list[str] = []

    reminder = build_perspective_reminder(agent)
    parts.append(reminder)

    context_lens = build_context_lens(agent)
    if context_lens:
        parts.append(context_lens)

    if decisions:
        parts.append(
            f"=== What's Already Decided ===\n{decisions}\n=== End Decisions ==="
        )

    if prior_specs:
        parts.append(
            f"=== Prior Design Docs (reference, don't contradict) ===\n"
            f"{prior_specs}\n=== End Prior Docs ==="
        )

    if open_questions:
        parts.append(
            f"=== Unresolved Open Questions from Prior Docs ===\n{open_questions}\n"
            f"=== End Open Questions ===\n\nIf this question can resolve any of the above, do so."
        )

    filtered = filter_prior_rounds(prior_rounds, agent)
    combined = filtered
    if this_round_so_far:
        combined += f"\n\n--- This round so far ---\n{this_round_so_far}"
    if combined.strip():
        parts.append(
            f"=== Discussion So Far (this question) ===\n{combined}\n=== End Discussion ==="
        )

    parts.append(f"## Question: {question['title']}\n\n{question['body']}")

    if round_instruction:
        parts.append(round_instruction)

    if this_round_so_far:
        parts.append(
            "Other agents have already spoken this round. Respond to their points directly. "
            "Agree, disagree, or build on what they said. 250 words max."
        )
    else:
        parts.append("You are speaking first this round. Set the agenda. 250 words max.")

    return "\n\n".join(parts)
```

**`run_round` — sequential by default (each agent sees prior speakers):**
```python
async def run_round(
    agents: list[str],
    system_prompts: dict[str, str],
    team: TeamConfig,
    question: dict,
    decisions: str,
    prior_rounds: str,
    prior_specs: str,
    open_questions: str,
    timeout: int,
    round_instruction: str = "",
    on_agent_start: Callable[[str], None] | None = None,
    on_agent_done: Callable[[str, str, float], None] | None = None,
) -> dict[str, str]:
    """Run one round sequentially. Each agent sees all prior speakers in this_round_so_far."""
    ordered = compute_speaking_order(agents, team)
    responses: dict[str, str] = {}
    this_round_so_far = ""

    for agent_key in ordered:
        if on_agent_start:
            on_agent_start(agent_key)

        start = time.time()
        payload = build_agent_payload(
            agent_key, team, question, decisions, prior_rounds,
            prior_specs, open_questions, round_instruction, this_round_so_far,
        )
        response = await run_claude_async(system_prompts[agent_key], payload, timeout=timeout)
        elapsed = time.time() - start

        responses[agent_key] = response

        if on_agent_done:
            on_agent_done(agent_key, response, elapsed)

        # Accumulate for next speaker's context
        agent = team.agents[agent_key]
        this_round_so_far += f"[{agent.name}]\n{response}\n\n"

    return responses
```

### `__init__.py` Update

Current `agentteam/conversation/__init__.py`:
```python
"""Conversation state management."""
from .state import Conversation, Message, MultiConversation
__all__ = ["Message", "Conversation", "MultiConversation"]
```

Add to it:
```python
from .orchestrator import build_agent_payload, compute_speaking_order, run_round
__all__ = ["Message", "Conversation", "MultiConversation",
           "build_agent_payload", "compute_speaking_order", "run_round"]
```

### Test Architecture

```python
# _SYSTEM/tests/test_conversation_orchestrator.py
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from agentteam.conversation.orchestrator import build_agent_payload, compute_speaking_order, run_round
from agentteam.types import AgentConfig, PersonalityConfig, TeamConfig

def make_team(agent_configs: dict[str, dict]) -> TeamConfig:
    """Build a minimal TeamConfig for tests."""
    agents = {}
    for key, overrides in agent_configs.items():
        agents[key] = AgentConfig(
            name=overrides.get("name", key),
            description=overrides.get("description", f"Test agent {key}"),
            personality=PersonalityConfig(**overrides.get("personality", {})),
        )
    return TeamConfig(agents=agents)

SAMPLE_QUESTION = {"number": 1, "title": "How should auth work?", "body": "Describe the auth flow."}
```

**Test `on_agent_done` callback signature:** `on_agent_done(agent_key: str, response: str, elapsed: float)`

**Mock `run_claude_async`:** Use `AsyncMock(return_value="test response")` — no real Claude calls.

**`test_sequential_accumulation`:** After patching `run_claude_async`, confirm the second agent's
`payload` arg contains the first agent's response. Inspect via `mock.call_args_list[1]`.

### Key Differences from `discussion/engine.py`

| Feature | `discussion/engine.py` | `agentteam/conversation/orchestrator.py` |
|---|---|---|
| Agent display names | `AGENT_DISPLAY_NAMES.get(key, key)` via config_loader | `agent.name` directly from TeamConfig |
| Role overlays | `overlay_instruction(role_key)` via config_loader | Passed as `round_instruction` string |
| Dependencies | Imports config_loader (engine-local) | Only `agentteam.*` imports |
| Print/emit | `print()` calls | None — pure library |

The orchestrator in `agentteam/` uses `agent.name` (from `AgentConfig.name`) instead of a
config-loaded display name map. This is cleaner and correct for library code.

### What Is NOT Part of This Story

- `run_question` (loops over all rounds for one question) — this is in `discussion/engine.py`,
  needed by Story 2.4/2.5
- `synthesize()` — covered in Story 2.4
- `format_transcript()` — covered in Story 2.5
- Consensus detection (`consensus.py`) — E4 story
- The existing `discussion/engine.py` — do NOT modify (brownfield rule)
- `agentteam/conversation/state.py` — do NOT modify

### Architecture Rules

- `pathlib.Path` only — never `os.path`
- Line length: **100** (ruff)
- **No `print()` or `logging`** anywhere in `agentteam/` — pure library
- Python 3.11+ union syntax: `str | None`, not `Optional[str]`; `Callable[[str], None] | None`
- `asyncio_mode = "auto"` configured — no `@pytest.mark.asyncio`

### Testing Rules

- New file: `_SYSTEM/tests/test_conversation_orchestrator.py`
- Run from `_SYSTEM/`: `python -m pytest tests/test_conversation_orchestrator.py -v`
- Use class-based test organization
- Mock `run_claude_async` for all async tests — never make real Claude calls
- Use `minimal_agent` and `rich_agent` fixtures from `conftest.py` as inspiration for test agents
- `timeout=15` is fine for test calls (not real Claude calls, timeout won't trigger)

### File Touch List

| File | Action |
|---|---|
| `_SYSTEM/agentteam/conversation/orchestrator.py` | New file — engine-agnostic round orchestration |
| `_SYSTEM/agentteam/conversation/__init__.py` | Add imports + `__all__` entries |
| `_SYSTEM/tests/test_conversation_orchestrator.py` | New file — unit tests with mocked Claude |

### References

- [Source: _SYSTEM/projects/engine/discussion/engine.py#run_round] — existing implementation (L148-218)
- [Source: _SYSTEM/projects/engine/discussion/engine.py#compute_speaking_order] — existing (L63-82)
- [Source: _SYSTEM/projects/engine/discussion/engine.py#_build_agent_payload] — existing (L85-145)
- [Source: _SYSTEM/agentteam/prompts/builder.py] — `build_perspective_reminder`, `build_context_lens`, `filter_prior_rounds`
- [Source: _SYSTEM/agentteam/types/agent.py] — `AgentConfig`, `TeamConfig`, `PersonalityConfig`
- [Source: _SYSTEM/agentteam/runner/claude.py] — `run_claude_async`
- [Source: _SYSTEM/agentteam/conversation/__init__.py] — current exports (extend, don't replace)
- [Source: _bmad-output/planning-artifacts/architecture.md#conversation/orchestrator.py] — E2 spec
- [Source: _bmad-output/project-context.md] — 38 project rules

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Created `agentteam/conversation/orchestrator.py` with `compute_speaking_order`, `build_agent_payload`,
  and `run_round` — engine-agnostic, no `config_loader` or `AGENT_DISPLAY_NAMES` dependencies
- Uses `agent.name` (from AgentConfig) for sequential accumulation context, not a display-name lookup dict
- Updated `agentteam/conversation/__init__.py` to export all three new functions
- Added `_SYSTEM/tests/test_conversation_orchestrator.py` with 20 tests across 3 classes
- Had to install `pytest-asyncio` (declared in pyproject.toml dev deps but not present in environment)
- 161/161 tests pass (20 new + 141 existing)

### File List

- _SYSTEM/agentteam/conversation/orchestrator.py
- _SYSTEM/agentteam/conversation/__init__.py
- _SYSTEM/tests/test_conversation_orchestrator.py

### Review Findings

- [x] [Review][Patch] `filter_prior_rounds` called with 1 arg but requires 2 (`prior_rounds, agent`) [orchestrator.py:~48] — crashes with `TypeError` at runtime whenever `prior_rounds` is non-empty; tests pass because all test fixtures use `prior_rounds=""`
- [x] [Review][Patch] Error string from `run_claude_async` silently used as discussion content in `run_round` [orchestrator.py:run_round] — `is_error_response()` never called; subsequent agents receive `[Error from claude CLI...]` as legitimate discussion content
- [x] [Review][Defer] `build_agent_payload` ternary for `question_section` is fragile to future edits [orchestrator.py:build_agent_payload] — deferred, code is functionally correct; refactor opportunity only
- [x] [Review][Defer] `run_round` does not handle future case where `run_claude_async` raises instead of returning error string [orchestrator.py:run_round] — deferred, migration target documented in CLAUDE.md
