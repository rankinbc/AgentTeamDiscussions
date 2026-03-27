# Story 3.1: Agent YAML Schema & Validation

Status: done

## Story

As a user,
I want to define agents in YAML with personality traits, positions, and techniques,
So that I can create distinct agent identities without writing code.

## Acceptance Criteria

1. **Given** an agent YAML file with personality (8 traits, 0.0–1.0), position (role, drives, intensity), and technique (primary, style_description, behaviors)
   **When** `load_agent()` reads the file
   **Then** it validates against the canonical `AgentConfig` Pydantic model without error

2. **Given** a valid `AgentConfig`
   **When** the model is inspected
   **Then** all 8 personality float dimensions (`assertiveness`, `creativity_temp`, `risk_tolerance`, `attention_span`, `stubbornness`, `idea_receptivity`, `bluntness`, `patience`) are present and constrained to 0.0–1.0

3. **Given** a valid `AgentConfig`
   **When** the position is inspected
   **Then** `drives` is a list of 3–5 non-empty strings and `pushback_on` is a list of 3–5 non-empty strings

4. **Given** a valid `AgentConfig`
   **When** the technique is inspected
   **Then** `behaviors` is a list of 5–8 non-empty strings

5. **Given** an agent YAML with invalid field values (float out of range, list too short/long, missing required field)
   **When** `load_agent()` reads the file
   **Then** a `ValidationError` is raised with a message identifying the specific invalid field

6. **Given** all 33 existing agent YAML files in `data/discussionAgents/`
   **When** `load_agent()` reads each file
   **Then** every file loads without error (no `ValidationError`)

## Tasks / Subtasks

- [x] Task 1: Add list-length validators to `agentteam/types/agent.py` (AC: 3, 4, 5)
  - [x] 1.1: In `PositionConfig`, change `drives` field to `Field(default_factory=list, min_length=3, max_length=5)` — position with explicit drives must have 3–5
  - [x] 1.2: In `PositionConfig`, change `pushback_on` field to `Field(default_factory=list, min_length=3, max_length=5)` — same constraint
  - [x] 1.3: In `TechniqueConfig`, change `behaviors` field to `Field(default_factory=list, min_length=5, max_length=8)` — technique with explicit behaviors must have 5–8
  - [x] 1.4: Do NOT change any float validators (`ge=0.0, le=1.0` already correct), do NOT change any defaults, do NOT change `__all__` exports

- [x] Task 2: Fix YAML compliance — behaviors too few (AC: 6)
  - [x] 2.1: For each agent YAML with 4 behaviors (21 files listed below), append one behavior line. Use the agent's existing style. A safe generic addition is: `"Acknowledge when you are genuinely uncertain rather than papering over doubt with confidence."` Adapt voice to match the agent's tone/style.
  - [x] 2.2: Files requiring one new behavior (currently behaviors=4):
    ```
    ev18hornet__emergence_theorist.yaml
    ev18hornet__ev_purist.yaml
    ev18hornet__flight_dreamer.yaml
    ev18hornet__player_advocate.yaml
    ev18hornet__scope_warden.yaml
    normal-people__diana.yaml
    normal-people__keiko.yaml
    normal-people__marcus.yaml
    normal-people__raj.yaml
    normal-people__tony.yaml
    normal-people__zara.yaml
    spec-builders__creative_director.yaml
    spec-builders__game_designer.yaml
    spec-builders__player_advocate.yaml
    spec-builders__scope_wrangler.yaml
    spec-builders__tech_lead.yaml
    tmos-dreamers__art_director.yaml
    tmos-dreamers__game_designer.yaml
    tmos-dreamers__narrative_designer.yaml
    tmos-dreamers__producer.yaml
    tmos-dreamers__tech_lead.yaml
    ```

- [x] Task 3: Fix YAML compliance — behaviors too many (AC: 6)
  - [x] 3.1: For agents with 9–10 behaviors, trim to 8 by removing the last 1–2 items. The trailing behaviors are typically meta-formatting instructions ("Before responding, verify...") that are lowest priority.
  - [x] 3.2: Files requiring trimming:
    ```
    beta-agents__cognitive_architect.yaml  (9 → 8: remove last item)
    beta-agents__product_oracle.yaml       (10 → 8: remove last 2 items)
    beta-agents__systems_pragmatist.yaml   (10 → 8: remove last 2 items)
    ```

- [x] Task 4: Fix regression in `tests/test_output_transcripts.py` (AC: 3, 4 — existing fixture)
  - [x] 4.1: In `make_team()`, update the `"position"` dict to include `"drives"` and `"pushback_on"` with 3 items each.
  - [x] 4.2: Update the `"technique"` dict in `make_team()` to include `"behaviors"` with 5 items.
  - [x] 4.3: Run `python -m pytest tests/test_output_transcripts.py -v` — all 14 tests must still pass

- [x] Task 5: Create `_SYSTEM/tests/test_agent_schema.py` (AC: 1–5)
  - [x] 5.1: Add module docstring: `"""Tests for AgentConfig Pydantic schema validation."""`
  - [x] 5.2: `TestPersonalityConfig` class — 6 tests covering float range validation and all 8 dimensions
  - [x] 5.3: `TestPositionConfig` class — 10 tests covering drives/pushback_on length constraints and defaults
  - [x] 5.4: `TestTechniqueConfig` class — 5 tests covering behaviors length constraints and defaults
  - [x] 5.5: `TestAgentConfig` class — 5 tests covering required fields, full construction, error propagation

- [x] Task 6: Create `_SYSTEM/tests/test_agent_loader.py` (AC: 1, 5, 6)
  - [x] 6.1: Add module docstring
  - [x] 6.2: `TestLoadAgent` class — 6 tests covering valid load, missing file, invalid YAML, _meta stripping
  - [x] 6.3: `TestLoadAgentRealFiles` — 33 parametrized tests, all real agents pass
  - [x] 6.4: `TestLoadTeam` — 3 tests: inline dict format, missing file, missing agents key
  - [x] 6.5: `TestResolveAgent` — 2 tests: resolve by key, missing key raises with available list
  - [x] 6.6: No `print()`, no `logging`, uses `tmp_path` fixture

## Dev Notes

### BROWNFIELD: AgentConfig Already Exists — Add Constraints Only

`agentteam/types/agent.py` already has `AgentConfig`, `PositionConfig`, `TechniqueConfig`, `PersonalityConfig`, and all sub-models fully defined. **DO NOT rewrite the file.**

The only change to `agent.py` is adding `min_length` / `max_length` parameters to 3 existing `Field()` calls:

```python
# BEFORE (in PositionConfig):
drives: list[str] = Field(default_factory=list)
pushback_on: list[str] = Field(default_factory=list)

# AFTER:
drives: list[str] = Field(default_factory=list, min_length=3, max_length=5)
pushback_on: list[str] = Field(default_factory=list, min_length=3, max_length=5)

# BEFORE (in TechniqueConfig):
behaviors: list[str] = Field(default_factory=list)

# AFTER:
behaviors: list[str] = Field(default_factory=list, min_length=5, max_length=8)
```

### Pydantic v2 Default Behavior: Empty Defaults Bypass min_length

In Pydantic v2, `validate_default=False` is the default. This means:
- `PositionConfig()` → `drives=[]` — the empty default is NOT validated against `min_length=3` ✓
- `PositionConfig(drives=["a"])` → validated, raises `ValidationError` (1 < min 3) ✓
- `PositionConfig(drives=["a","b","c"])` → validated, passes ✓

This is intentional: test fixtures and internal code can construct minimal configs without specifying all fields, but real agent YAMLs that explicitly define drives must use the correct count.

### Pydantic v2 Import Note

`min_length` and `max_length` on list fields are native Pydantic v2 `Field()` parameters — no extra imports needed. Do NOT use `conlist()` (Pydantic v1 pattern).

### YAML Fix Strategy for behaviors=4 Agents

For the 21 agents with only 4 behaviors, append one behavior in the same voice as the agent's existing behaviors. Look at the last existing behavior for style, then add a natural 5th. Examples by agent type:

- **normal-people agents** (informal voice): `"Be honest when you don't know something rather than bluffing your way through."`
- **spec-builders / tmos-dreamers** (professional voice): `"Acknowledge genuine trade-offs rather than presenting one path as obviously correct."`
- **ev18hornet** (technical/domain voice): Read existing behaviors; add a self-consistency check like `"If your stance has shifted from your opening, name the reason explicitly."`

Read each agent's existing behaviors before adding to match register and voice.

### YAML Fix Strategy for behaviors=9-10 Agents

These 3 beta-agents have redundant formatting/meta behaviors at the end. Remove the **last** 1 or 2 items:

- `beta-agents__cognitive_architect.yaml` (9 → 8): Remove the last item: `"Before responding, verify: Am I in character? Am I at the right abstraction level? Am I adding substance or just filling space?"`
- `beta-agents__product_oracle.yaml` (10 → 8): Remove the last 2 items (inspect the file to identify them).
- `beta-agents__systems_pragmatist.yaml` (10 → 8): Remove the last 2 items.

Read each file before editing to confirm which items are truly redundant.

### Existing loader.py — No Changes Needed

`agentteam/agents/loader.py` already handles:
- `load_agent()` — reads YAML, strips `_meta`/`meta` keys, constructs `AgentConfig(**raw)`
- `load_team()` — handles both inline-dict and list-of-refs team formats
- `load_agent_by_key()` — discovers by exact name or `__key` pattern
- `resolve_agent()` — finds by key, name, or id

**DO NOT modify loader.py.** The Pydantic validation in `AgentConfig` automatically applies when `AgentConfig(**raw)` is called.

### Test for Real Files: Correct Path Setup

```python
# tests/test_agent_loader.py

import pytest
from pathlib import Path
from agentteam.agents.loader import load_agent

# Resolve from the test file location up to _SYSTEM/
_SYSTEM_DIR = Path(__file__).resolve().parent.parent
_AGENTS_DIR = _SYSTEM_DIR / "data" / "discussionAgents"

def get_agent_yamls():
    return list(_AGENTS_DIR.glob("*.yaml"))

class TestLoadAgentRealFiles:
    @pytest.mark.parametrize("agent_file", get_agent_yamls(), ids=lambda f: f.name)
    def test_all_real_agents_load(self, agent_file):
        agent = load_agent(str(agent_file))
        assert agent.name  # non-empty name
```

The `get_agent_yamls()` call happens at collection time. The `ids=lambda f: f.name` gives readable test names in the output.

### Minimal Valid Agent YAML for Fixtures

```yaml
name: Test Agent
description: A test agent for validation purposes.
position:
  role: tester
  drives:
  - drive one
  - drive two
  - drive three
  pushback_on:
  - pushback one
  - pushback two
  - pushback three
technique:
  primary: testing
  behaviors:
  - behavior one
  - behavior two
  - behavior three
  - behavior four
  - behavior five
```

Use this pattern for `tmp_path`-based tests in `test_agent_loader.py`.

### Architecture Rules

- Line length: **100** (ruff)
- **No `print()` or `logging`** in `agentteam/` — pure library
- Python 3.11+ union syntax
- `tmp_path` fixture for all file I/O tests
- `asyncio_mode = "auto"` — no `@pytest.mark.asyncio` needed

### Testing Rules

- Run from `_SYSTEM/`: `python -m pytest tests/test_agent_schema.py tests/test_agent_loader.py tests/test_output_transcripts.py -v`
- After YAML fixes, run: `python -m pytest tests/test_agent_loader.py::TestLoadAgentRealFiles -v` (33 parametrized tests)
- Full suite must remain green: `python -m pytest`

### File Touch List

| File | Action |
|---|---|
| `_SYSTEM/agentteam/types/agent.py` | Add `min_length`/`max_length` to `drives`, `pushback_on`, `behaviors` fields |
| `_SYSTEM/tests/test_agent_schema.py` | New file — Pydantic model validation tests |
| `_SYSTEM/tests/test_agent_loader.py` | New file — loader tests including real-file parametrized |
| `_SYSTEM/tests/test_output_transcripts.py` | Update `make_team` fixture: add `drives`, `pushback_on`, `behaviors` |
| `_SYSTEM/data/discussionAgents/*.yaml` (24 files) | Fix behaviors count: add 1 to 21 files with 4; trim 1-2 from 3 files with 9-10 |

### Review Findings

- [x] [Review][Defer] Non-empty string items not enforced — AC 3 & 4 say "3–5 non-empty strings" but schema accepts `drives=["","",""]`; fix: `list[Annotated[str, Field(min_length=1)]]` in PositionConfig/TechniqueConfig — deferred, dev notes specify only length constraints; low-priority, all real YAMLs use non-empty strings
- [x] [Review][Defer] `loader.py` null-check missing on `yaml.safe_load()` result — empty YAML file returns `None`, then `None.pop()` raises `AttributeError` instead of a clean error [agentteam/agents/loader.py:21] — deferred, pre-existing issue in loader.py (not introduced by this story)
- [x] [Review][Defer] `get_agent_yamls()` at collection time silently produces empty parametrize list if `_AGENTS_DIR` missing — all 33 tests pass with no warning [tests/test_agent_loader.py:69] — deferred, pre-existing test infrastructure concern; add guard if agents dir is ever relocated

### References

- [Source: _SYSTEM/agentteam/types/agent.py] — `PositionConfig`, `TechniqueConfig`, `PersonalityConfig` (modify only listed fields)
- [Source: _SYSTEM/agentteam/agents/loader.py] — `load_agent`, `load_team`, `load_agent_by_key` (do not modify)
- [Source: _SYSTEM/tests/test_output_transcripts.py#make_team] — fixture to update (regression fix)
- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.1] — acceptance criteria
- [Source: _bmad-output/planning-artifacts/architecture.md#Epic-to-Directory Mapping] — E3 → `agentteam/agents/`, `prompts/identity.py`

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Added `min_length=3, max_length=5` to `PositionConfig.drives` and `PositionConfig.pushback_on`
- Added `min_length=5, max_length=8` to `TechniqueConfig.behaviors` in `agentteam/types/agent.py`
- Pydantic v2 default-bypass behavior: empty defaults (via `default_factory=list`) are NOT validated; `validate_default=False` is the Pydantic v2 default
- Fixed 21 YAML files (behaviors=4): appended a 5th behavior in each agent's voice (ev18hornet, normal-people, spec-builders, tmos-dreamers groups)
- Fixed 3 YAML files (behaviors=9-10): trimmed to 8 by removing last formatting/meta behavior(s) from beta-agents (cognitive_architect, product_oracle, systems_pragmatist)
- Fixed regression in `tests/test_output_transcripts.py::make_team` — added `drives`, `pushback_on` (3 items each) and `behaviors` (5 items) to fixture
- Fixed regression in `tests/test_prompts_builder.py` — 3 `PositionConfig` fixtures updated to use 3+ items
- All 33 real agent files load without ValidationError (verified by parametrized test)
- 273/273 tests passing — no regressions

### File List

- _SYSTEM/agentteam/types/agent.py
- _SYSTEM/tests/test_agent_schema.py
- _SYSTEM/tests/test_agent_loader.py
- _SYSTEM/tests/test_output_transcripts.py
- _SYSTEM/tests/test_prompts_builder.py
- _SYSTEM/data/discussionAgents/ev18hornet__emergence_theorist.yaml
- _SYSTEM/data/discussionAgents/ev18hornet__ev_purist.yaml
- _SYSTEM/data/discussionAgents/ev18hornet__flight_dreamer.yaml
- _SYSTEM/data/discussionAgents/ev18hornet__player_advocate.yaml
- _SYSTEM/data/discussionAgents/ev18hornet__scope_warden.yaml
- _SYSTEM/data/discussionAgents/normal-people__diana.yaml
- _SYSTEM/data/discussionAgents/normal-people__keiko.yaml
- _SYSTEM/data/discussionAgents/normal-people__marcus.yaml
- _SYSTEM/data/discussionAgents/normal-people__raj.yaml
- _SYSTEM/data/discussionAgents/normal-people__tony.yaml
- _SYSTEM/data/discussionAgents/normal-people__zara.yaml
- _SYSTEM/data/discussionAgents/spec-builders__creative_director.yaml
- _SYSTEM/data/discussionAgents/spec-builders__game_designer.yaml
- _SYSTEM/data/discussionAgents/spec-builders__player_advocate.yaml
- _SYSTEM/data/discussionAgents/spec-builders__scope_wrangler.yaml
- _SYSTEM/data/discussionAgents/spec-builders__tech_lead.yaml
- _SYSTEM/data/discussionAgents/tmos-dreamers__art_director.yaml
- _SYSTEM/data/discussionAgents/tmos-dreamers__game_designer.yaml
- _SYSTEM/data/discussionAgents/tmos-dreamers__narrative_designer.yaml
- _SYSTEM/data/discussionAgents/tmos-dreamers__producer.yaml
- _SYSTEM/data/discussionAgents/tmos-dreamers__tech_lead.yaml
- _SYSTEM/data/discussionAgents/beta-agents__cognitive_architect.yaml
- _SYSTEM/data/discussionAgents/beta-agents__product_oracle.yaml
- _SYSTEM/data/discussionAgents/beta-agents__systems_pragmatist.yaml
