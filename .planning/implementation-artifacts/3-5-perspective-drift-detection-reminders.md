# Story 3.5: Perspective Drift Detection & Reminders

Status: done

## Story

As a user,
I want agents nudged back into character when they drift from their assigned role,
So that discussions maintain diverse perspectives throughout the session.

## Acceptance Criteria

1. **Given** an agent's previous response and their configured position/role
   **When** the orchestrator prepares the next turn for that agent
   **Then** it checks for drift signals: agreeing with positions contrary to their drives, abandoning their pushback items, generic responses that could come from any agent

2. **Given** drift is detected in a previous response
   **When** the agent payload is assembled
   **Then** a perspective reminder is injected into the Task layer: "Remember, you are [role]. Your drives are [drives]. Push back on [pushback items]."

3. **Given** a drift reminder is injected
   **When** the reminder is constructed
   **Then** the reminder adds minimal tokens (< 100 words) to avoid blowing the token ceiling

4. **Given** the drift detection logic
   **When** it runs
   **Then** it uses keyword/stance matching on the previous response text — no additional LLM call

5. **Given** a previous response that mentions the agent's drive or pushback keywords
   **When** drift is evaluated
   **Then** drift is NOT detected — agent is speaking in character

## Tasks / Subtasks

- [x] Task 1: Create `agentteam/agents/drift.py` (AC: 1, 2, 3, 4, 5)
  - [x] 1.1: Implement `_extract_anchor_words(agent: AgentConfig) -> frozenset[str]` — extracts content words (len > 3) from all drives + pushback_on items combined
  - [x] 1.2: Implement `detect_drift(previous_response: str, agent: AgentConfig) -> bool` using three-signal logic (see Dev Notes)
  - [x] 1.3: Implement `build_drift_reminder(agent: AgentConfig) -> str` — produces the AC-specified format with fallback text when drives/pushback empty
  - [x] 1.4: Add module-level `_AGREEMENT_PHRASES` and `_CAPITULATION_PHRASES` frozensets (see Dev Notes for exact values)
  - [x] 1.5: No `print()` or `logging` — pure library code

- [x] Task 2: Update `agentteam/agents/__init__.py` (AC: all)
  - [x] 2.1: Add `detect_drift` and `build_drift_reminder` to imports from `.drift`
  - [x] 2.2: Add both to `__all__`

- [x] Task 3: Update `agentteam/conversation/orchestrator.py` (AC: 1, 2)
  - [x] 3.1: Add `from agentteam.agents.drift import build_drift_reminder, detect_drift` import
  - [x] 3.2: Add `previous_response: str = ""` parameter to `build_agent_payload()` — appended after existing positional params, before keyword-only params
  - [x] 3.3: In `build_agent_payload()`, after the existing `build_perspective_reminder()` call, add conditional drift reminder injection (see Dev Notes for exact placement and format)
  - [x] 3.4: Add `previous_responses: dict[str, str] | None = None` parameter to `run_round()`
  - [x] 3.5: In `run_round()`, pass `previous_response=(previous_responses or {}).get(agent_key, "")` to `build_agent_payload()`

- [x] Task 4: Create `tests/test_drift.py` (AC: 1–5)
  - [x] 4.1: `TestDetectDrift` class — 8 tests covering all signal paths (see Dev Notes)
  - [x] 4.2: `TestBuildDriftReminder` class — 6 tests including token count, format structure, fallback text
  - [x] 4.3: `TestBuildAgentPayloadDriftIntegration` class — 3 tests verifying orchestrator wiring
  - [x] 4.4: `TestRunRoundDriftIntegration` class — 2 tests verifying `previous_responses` forwarding
  - [x] 4.5: Add module docstring: `"""Tests for agentteam.agents.drift and drift integration in orchestrator."""`

- [x] Task 5: Run tests and verify no regressions
  - [x] 5.1: `python -m pytest tests/test_drift.py -v` — 19/19 pass
  - [x] 5.2: `python -m pytest tests/test_conversation_orchestrator.py -v` — all 16 existing tests still pass
  - [x] 5.3: `python -m pytest` — 376/376 green

## Dev Notes

### BROWNFIELD CRITICAL: `build_perspective_reminder()` Already Exists — Do NOT Replace It

`agentteam/prompts/builder.py` already has `build_perspective_reminder(agent)` and it is **always** called unconditionally in `build_agent_payload()` (line 48). Story 3.5 adds a *second*, more targeted reminder that fires only when drift is detected — it is ADDITIONAL, not a replacement. Both reminders appear in the payload when drift fires.

The `build_perspective_reminder()` output:
```
[You are {name} -- {role}. Style: {cognitive_style}, {emotional_baseline}. Technique: {primary}. Stay in character. Add substance or stay silent.]
```

The new `build_drift_reminder()` output (targeted, drives/pushback specific):
```
[DRIFT ALERT: Remember, you are {role}. Your drives are: {drive1}; {drive2}; .... Push back on: {pushback1}; {pushback2}; ....]
```

### `detect_drift()` — Three-Signal Algorithm

```python
_AGREEMENT_PHRASES: frozenset[str] = frozenset([
    "i agree", "you're right", "that's correct", "great point",
    "exactly right", "well said", "i concede", "you've convinced me",
    "i was wrong", "you are right",
])

_CAPITULATION_PHRASES: frozenset[str] = frozenset([
    "perhaps you're right", "i'll concede", "i take that back",
    "i withdraw", "you make a good point about", "i'll drop",
    "i abandon", "let's forget my earlier",
])


def _extract_anchor_words(agent: AgentConfig) -> frozenset[str]:
    """Words (len > 3) from drives + pushback_on — used to verify agent is speaking in character."""
    words: set[str] = set()
    for item in agent.position.drives + agent.position.pushback_on:
        for word in item.split():
            if len(word) > 3:
                words.add(word.lower().strip(".,;:"))
    return frozenset(words)


def detect_drift(previous_response: str, agent: AgentConfig) -> bool:
    if not previous_response:
        return False

    drives = agent.position.drives
    pushback_on = agent.position.pushback_on

    # No identity anchors — can't meaningfully detect drift
    if not drives and not pushback_on:
        return False

    lower = previous_response.lower()
    anchor_words = _extract_anchor_words(agent)
    has_anchors = bool(anchor_words) and any(word in lower for word in anchor_words)

    # Signal 1: Agreement without identity anchors (agent abandoned their position)
    if any(phrase in lower for phrase in _AGREEMENT_PHRASES) and not has_anchors:
        return True

    # Signal 2: Explicit capitulation phrases (unconditional — no anchor check needed)
    if any(phrase in lower for phrase in _CAPITULATION_PHRASES):
        return True

    return False
```

Key invariant: If the response contains any of the agent's drive or pushback keywords, Signal 1 does NOT fire — agent is speaking in character, even if they also happen to agree with something.

### `build_drift_reminder()` — Format and Token Budget

```python
def build_drift_reminder(agent: AgentConfig) -> str:
    pos = agent.position
    drives_text = "; ".join(pos.drives) if pos.drives else "your stated priorities"
    pushback_text = "; ".join(pos.pushback_on) if pos.pushback_on else "overreach and vagueness"
    return (
        f"[DRIFT ALERT: Remember, you are {pos.role}. "
        f"Your drives are: {drives_text}. "
        f"Push back on: {pushback_text}.]"
    )
```

Token budget: With typical drives (3-5 items) + pushback_on (3-5 items), this renders to ~30-60 words — well under the 100-word ceiling. Tests should verify `len(result.split()) < 100` on a fully populated agent.

### Where to Inject in `build_agent_payload()`

Inject the drift reminder **immediately after** the existing `build_perspective_reminder()` call — before the context lens and all decision/history sections. This ensures it appears at the top of the agent's context, making it maximally visible.

```python
# CURRENT code (lines 48-53):
reminder = build_perspective_reminder(agent)
parts.append(reminder)

context_lens = build_context_lens(agent)
if context_lens:
    parts.append(context_lens)

# AFTER change:
reminder = build_perspective_reminder(agent)
parts.append(reminder)

# Drift detection — inject targeted reminder if agent has drifted
if previous_response and detect_drift(previous_response, agent):
    parts.append(build_drift_reminder(agent))

context_lens = build_context_lens(agent)
if context_lens:
    parts.append(context_lens)
```

### Where to Add `previous_responses` in `run_round()`

Add as the LAST parameter (after `on_agent_done`). This preserves backwards compatibility — all existing callers pass positional args up through `timeout`, and keyword args `round_instruction`, `on_agent_start`, `on_agent_done` are unaffected.

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
    previous_responses: dict[str, str] | None = None,  # ← NEW
) -> dict[str, str]:
    ...
    payload = build_agent_payload(
        agent_key, team, question, decisions, prior_rounds,
        prior_specs, open_questions, round_instruction, this_round_so_far,
        previous_response=(previous_responses or {}).get(agent_key, ""),  # ← NEW
    )
```

### Pydantic v2 Default-Bypass

`PositionConfig.drives` and `PositionConfig.pushback_on` use `Field(default_factory=list, min_length=3, max_length=5)` with `validate_default=False` — the empty list `[]` is the actual default even though `min_length=3`. This is the established pattern from Stories 3.1/3.2. `detect_drift()` MUST handle empty `drives` and `pushback_on` gracefully (return False). Do NOT add a Pydantic assertion that lists are non-empty — that would break existing tests.

### `__init__.py` Update Pattern

Follow the existing `agents/__init__.py` pattern:

```python
"""Agent and team loading from YAML files."""
from .loader import list_agents, list_teams, load_agent, load_agent_by_key, load_team, load_team_by_name, resolve_agent
from .drift import build_drift_reminder, detect_drift
__all__ = [
    "load_agent", "load_agent_by_key", "load_team", "load_team_by_name",
    "resolve_agent", "list_teams", "list_agents",
    "detect_drift", "build_drift_reminder",
]
```

### Test Structure

Tests are flat in `tests/` (not mirrored to subdirs). Follow the pattern from `tests/test_conversation_orchestrator.py`.

**`tests/test_drift.py`** test scaffold:

```python
"""Tests for agentteam.agents.drift and drift integration in orchestrator."""
import pytest
from agentteam.agents.drift import build_drift_reminder, detect_drift
from agentteam.conversation.orchestrator import build_agent_payload
from agentteam.types import AgentConfig, PositionConfig, TeamConfig


def make_positioned_agent(
    role="systems architect",
    drives=None,
    pushback_on=None,
) -> AgentConfig:
    """Helper: AgentConfig with non-empty drives and pushback_on."""
    return AgentConfig(
        name="Architect",
        description="A test agent with a position.",
        position=PositionConfig(
            role=role,
            drives=drives or ["data-driven decisions", "cost efficiency", "maintainability"],
            pushback_on=["premature optimization", "scope creep", "over-engineering"],
        ),
    )


class TestDetectDrift:
    def test_no_drift_empty_response(self): ...
    def test_no_drift_no_identity_anchors(self): ...  # minimal_agent with no drives
    def test_detects_agreement_without_drive_keywords(self): ...  # "I agree." → True
    def test_no_drift_agreement_with_drive_keywords(self): ...  # "I agree that data-driven decisions are key" → False
    def test_detects_capitulation_phrase(self): ...  # "Perhaps you're right, we should reconsider." → True
    def test_detects_i_withdraw_phrase(self): ...  # "I withdraw my previous objection." → True
    def test_no_drift_response_with_pushback_keywords(self): ...  # mentions "premature optimization" → False
    def test_case_insensitive(self): ...  # "I AGREE with everything" → True


class TestBuildDriftReminder:
    def test_contains_role(self): ...
    def test_contains_drives(self): ...
    def test_contains_pushback_on(self): ...
    def test_under_100_words(self): ...  # len(result.split()) < 100
    def test_minimal_agent_uses_fallback_text(self): ...  # no drives/pushback → uses fallback strings
    def test_format_matches_ac_spec(self): ...  # "Remember, you are" and "drives are" and "Push back on" in result


class TestBuildAgentPayloadDriftIntegration:
    def test_drift_reminder_injected_when_drift_detected(self): ...
    def test_no_drift_reminder_when_previous_response_empty(self): ...
    def test_no_drift_reminder_when_no_drift(self): ...


class TestRunRoundDriftIntegration:
    async def test_previous_responses_forwarded(self): ...  # previous_responses dict → values passed to build_agent_payload
    async def test_no_crash_when_previous_responses_none(self): ...
```

For `TestRunRoundDriftIntegration`, use `unittest.mock.patch` to intercept `detect_drift` — the same mock pattern used in `test_conversation_orchestrator.py`:
```python
from unittest.mock import AsyncMock, patch
```

For `test_drift_reminder_injected_when_drift_detected` in payload tests, create an agent with drives/pushback_on, use a `previous_response` containing an agreement phrase without any drive keywords, and assert `"DRIFT ALERT"` in the payload.

### Architecture Rules

- No `print()` or `logging` in `agentteam/` — library code only
- Python 3.11+ syntax (use `dict[str, str] | None`)
- `asyncio_mode = "auto"` in pytest — no `@pytest.mark.asyncio` needed (see `test_conversation_orchestrator.py`)
- Line length: 100 (ruff)
- Use `from agentteam.types import AgentConfig` — not from `agentteam.types.agent`

### File Touch List

| File | Action |
|---|---|
| `agentteam/agents/drift.py` | **CREATE** — `detect_drift()`, `build_drift_reminder()`, `_extract_anchor_words()`, module-level frozensets |
| `agentteam/agents/__init__.py` | **MODIFY** — add `detect_drift`, `build_drift_reminder` imports and `__all__` entries |
| `agentteam/conversation/orchestrator.py` | **MODIFY** — `previous_response` param to `build_agent_payload`, `previous_responses` param to `run_round`, drift import |
| `tests/test_drift.py` | **CREATE** — full test suite for drift module + orchestrator integration |

### References

- [Source: `agentteam/agents/__init__.py`] — existing module structure to extend
- [Source: `agentteam/agents/loader.py`] — existing agents module; `drift.py` is a peer module
- [Source: `agentteam/conversation/orchestrator.py`] — `build_agent_payload()` (line 29-94), `run_round()` (line 97-145); exact insertion points
- [Source: `agentteam/prompts/builder.py`] — `build_perspective_reminder()` (line 25-33), `build_context_lens()` (line 36-59); these are NOT changed
- [Source: `agentteam/types/agent.py`] — `PositionConfig` (role, drives, pushback_on, intensity); `AgentConfig`
- [Source: `tests/test_conversation_orchestrator.py`] — existing orchestrator tests, `make_team()` helper, mock pattern
- [Source: `tests/conftest.py`] — `minimal_agent` fixture (no drives/pushback — use for fallback/no-anchor tests)
- [Source: `_bmad-output/planning-artifacts/architecture.md`] — E3 column maps `agentteam/agents/drift.py`; `estimate_tokens()` is E4, not available yet

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- No failures. All 19 new tests passed on first run. Full suite 376/376 green immediately.

### Completion Notes List

- Created `agentteam/agents/drift.py` with `detect_drift()` (two-signal keyword matching — no LLM call), `build_drift_reminder()` (role+drives+pushback format, < 100 words), and `_extract_anchor_words()` helper; `_AGREEMENT_PHRASES` and `_CAPITULATION_PHRASES` frozensets at module level
- Updated `agentteam/agents/__init__.py` to export `detect_drift` and `build_drift_reminder`
- Updated `agentteam/conversation/orchestrator.py`: `previous_response: str = ""` param added to `build_agent_payload()` with conditional drift injection after `build_perspective_reminder()`; `previous_responses: dict[str, str] | None = None` param added to `run_round()` with `(previous_responses or {}).get(agent_key, "")` forwarding
- 19 new tests in `tests/test_drift.py`: 8 signal detection tests, 6 reminder format/content tests, 3 payload integration tests, 2 run_round integration tests
- 376/376 full suite passing — all 16 existing `test_conversation_orchestrator.py` tests pass (backwards-compatible default params)

### Review Findings

- [x] [Review][Decision] Capitulation signal unconditional vs AC5 — resolved: apply AC5 to all signals; capitulation now suppressed when anchor words present; `has_anchors` check added to Signal 2 [agentteam/agents/drift.py:58-60]
- [x] [Review][Patch] Short-word positions → empty anchor_words → false positive drift — fixed: early return False when `anchor_words` is empty frozenset (even with non-empty drives/pushback_on); 3 boundary tests added [agentteam/agents/drift.py:47-52]
- [x] [Review][Defer] "Generic response" third signal (AC1) not implemented — AC1 specifies three drift signals; only agreement and capitulation are implemented; generic-response heuristic not defined in Dev Notes [agentteam/agents/drift.py]
- [x] [Review][Defer] Curly-quote apostrophes not normalized — frozenset phrases use straight apostrophes; LLM output may use U+2019 curly quotes; "you're right" would miss [agentteam/agents/drift.py:5-15]
- [x] [Review][Defer] No cooldown/deduplication on drift reminder injection — `build_drift_reminder` appended every turn drift fires; no cap or cooldown; token growth unbounded across many drifting rounds [agentteam/conversation/orchestrator.py:54-55]
- [x] [Review][Defer] No runtime enforcement of < 100 words docstring constraint — `build_drift_reminder` docstring claims < 100 words but does not truncate; only test-time assertion enforces this [agentteam/agents/drift.py:65-78]
- [x] [Review][Defer] Asymmetric punctuation strip — extraction strips `.,;:` from words, detection does substring search on raw lowercased response; `!?'"` variants not handled in extraction [agentteam/agents/drift.py:24]
- [x] [Review][Defer] No word boundaries in anchor matching — `word in lower` substring check; anchor "scope" matches in "microscope"; direction of error is missed drift (false negative) which is safer than false alarm [agentteam/agents/drift.py:52]
- [x] [Review][Defer] `previous_responses` key mismatch undetected — silent `.get(agent_key, "")` fallback; key format drift (hyphen vs underscore) silently skips detection [agentteam/conversation/orchestrator.py:136]
- [x] [Review][Defer] Stateless detection — `detect_drift` has no memory across turns; a single in-character response resets the drift signal even after multiple drifting turns; intentional per-call design [agentteam/agents/drift.py]

### File List

- _SYSTEM/agentteam/agents/drift.py (new)
- _SYSTEM/agentteam/agents/__init__.py (modified)
- _SYSTEM/agentteam/conversation/orchestrator.py (modified)
- _SYSTEM/tests/test_drift.py (new)
