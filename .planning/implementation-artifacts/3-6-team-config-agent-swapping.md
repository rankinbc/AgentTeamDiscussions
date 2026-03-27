# Story 3.6: Team Config & Agent Swapping

Status: done

## Story

As a user,
I want to swap team configurations between sessions by specifying a different YAML file,
So that I can iterate on team composition without modifying code.

## Acceptance Criteria

1. **Given** a team YAML file containing multiple agent definitions
   **When** I run `session_runner.py brief.md --team my-team.yaml`
   **Then** all agents in the team file are loaded and validated via Pydantic (validation errors surface as `ValidationError`, not silent failures)

2. **Given** a team YAML where each agent has `output.job` set (propose/critique/evaluate/ideate/simplify)
   **When** `assign_rounds_from_job_types(team)` is called
   **Then** it returns `{"propose": [...], "critique": [...], "evaluate": [...]}` mapping each agent key to its round based on `output.job`
   **And** `ideate` agents map to the `propose` round
   **And** `simplify` agents map to the `evaluate` round
   **And** a `ValueError` is raised if no agents qualify for the `propose` round

3. **Given** `--team` is omitted
   **When** the session runner starts
   **Then** the default team (`data/teams/beta-agents.yaml`) is used unchanged

4. **Given** a custom team YAML whose agent files are co-located (same directory as the team YAML, not in `_AGENTS_DIR`)
   **When** `load_team(config_path)` is called
   **Then** it resolves agent file paths relative to the team file's parent directory when the file is not found in `_AGENTS_DIR`

5. **Given** a session runs to completion
   **When** the session status is written
   **Then** `session_status.json` includes a `"team"` key recording the absolute path of the team file used

## Tasks / Subtasks

- [x] Task 1: Add `job:` field to beta-agent YAMLs (AC: 2)
  - [x] 1.1: Add `job: propose` to `data/discussionAgents/beta-agents__cognitive_architect.yaml` output section
  - [x] 1.2: Add `job: propose` to `data/discussionAgents/beta-agents__flow_orchestrator.yaml` output section
  - [x] 1.3: Add `job: critique` to `data/discussionAgents/beta-agents__systems_pragmatist.yaml` output section
  - [x] 1.4: Add `job: critique` to `data/discussionAgents/beta-agents__adversarial_critic.yaml` output section
  - [x] 1.5: Add `job: evaluate` to `data/discussionAgents/beta-agents__product_oracle.yaml` output section
  - [x] 1.6: Add `job: evaluate` to `data/discussionAgents/beta-agents__context_surgeon.yaml` output section
  - [x] 1.7: Add `job: ideate` to `data/discussionAgents/beta-agents__idea_merchant.yaml` output section

- [x] Task 2: Add `assign_rounds_from_job_types()` to `agentteam/agents/loader.py` (AC: 2)
  - [x] 2.1: Implement function with `_JOB_TO_ROUND` mapping (`ideate → propose`, `simplify → evaluate`)
  - [x] 2.2: Raises `ValueError` if resulting `propose` list is empty
  - [x] 2.3: Returns `{"propose": [...], "critique": [...], "evaluate": [...]}` — always includes all three keys (empty lists if no agents)

- [x] Task 3: Fix `load_team()` agent file path resolution in `agentteam/agents/loader.py` (AC: 1, 4)
  - [x] 3.1: Capture team file's parent directory (`team_dir = path.parent`) at start of `load_team()`
  - [x] 3.2: In the `isinstance(raw["agents"], list)` branch, when `agent_file` is present and `_AGENTS_DIR / agent_file` does not exist, try `team_dir / agent_file` as fallback
  - [x] 3.3: Do NOT modify the `load_team_by_name()` path (it has its own `a_dir` parameter)

- [x] Task 4: Export `assign_rounds_from_job_types` from `agentteam/agents/__init__.py` (AC: 2)
  - [x] 4.1: Add import from `.loader`
  - [x] 4.2: Add to `__all__`

- [x] Task 5: Record team path in session metadata in `projects/engine/session/runner.py` (AC: 5)
  - [x] 5.1: After `status["mode"] = mode_name` (line ~549), add `status["team"] = str(_team_path.resolve())`
  - [x] 5.2: `_team_path` is already set at line 399 — no new variable needed

- [x] Task 6: Create `tests/test_team_swapping.py` (AC: 1–5)
  - [x] 6.1: `TestAssignRoundsFromJobTypes` class — 6 tests (expanded from 5 to include idea_merchant integration)
  - [x] 6.2: `TestLoadTeamPathResolution` class — 2 tests (see Dev Notes)
  - [x] 6.3: Module docstring: `"""Tests for assign_rounds_from_job_types and load_team path resolution."""`

- [x] Task 7: Run full test suite and verify no regressions
  - [x] 7.1: `python -m pytest tests/test_team_swapping.py -v` — 8/8 pass
  - [x] 7.2: `python -m pytest tests/test_agent_loader.py -v` — all existing tests still pass
  - [x] 7.3: `python -m pytest` — 387/387 green

### Review Findings

- [x] [Review][Patch] Flip `load_team` resolution order — `team_dir` takes priority over `_AGENTS_DIR`; local/portable teams override canonical agents [loader.py, `load_team` list branch]
- [x] [Review][Patch] Silent `load_agent_by_key` fallback when both paths miss — now raises `FileNotFoundError` [loader.py, `load_team` list branch]
- [x] [Review][Defer] Unknown `JobType` defaults to `"propose"` silently via `.get(..., "propose")` [loader.py:`_JOB_TO_ROUND`] — deferred, by design per spec Dev Notes
- [x] [Review][Defer] `load_agent_by_key` glob match is non-deterministic when multiple files match `*__{key}.yaml` [loader.py:`load_agent_by_key`] — deferred, pre-existing
- [x] [Review][Defer] `list_teams` / `load_team` have inconsistent contracts for missing `agents` key (permissive vs strict) [loader.py:`list_teams`] — deferred, pre-existing
- [x] [Review][Defer] Integration tests have no `skipif` guard for missing data directory [tests/test_team_swapping.py] — deferred, pre-existing concern (data dir present; CI risk)
- [x] [Review][Defer] `resolve_agent` `hasattr(agent, "id")` is always `True` for Pydantic model; guard is redundant [loader.py:`resolve_agent`] — deferred, pre-existing
- [x] [Review][Defer] Absolute `agent_file` path in team YAML accidentally works via pathlib join behaviour [loader.py:`load_team`] — deferred, pre-existing undocumented edge case
- [x] [Review][Defer] Empty `agents: []` in team YAML silently returns empty `TeamConfig` [loader.py:`load_team`] — deferred, pre-existing
- [x] [Review][Defer] Dict-format `agents` branch bypasses all new path-resolution logic [loader.py:`load_team` else-branch] — deferred, by design per Task 3.3
- [x] [Review][Defer] `load_team_by_name` has no `team_dir` fallback — diverges intentionally from `load_team` [loader.py:`load_team_by_name`] — deferred, by design per Task 3.3
- [x] [Review][Defer] `status["team"]` not written in no-session mode (`session_management=False`) [runner.py] — deferred, by design (AC5 scoped to full-session path)
- [x] [Review][Defer] `assign_rounds_from_job_types` not re-exported from top-level `agentteam` package [agentteam/__init__.py] — deferred, pre-existing pattern

## Dev Notes

### BROWNFIELD CRITICAL: `--team` Flag and `run_session()` Already Exist

**DO NOT re-implement these** — they already exist in `projects/engine/session/runner.py`:

```python
# main() lines 907-936: --team flag already parsed
parser.add_argument("--team", default=None, help="Path to team YAML file")
# ...
if args.team:
    team_path = Path(args.team).resolve()
    if not team_path.is_file():
        print(f"ERROR: Team config not found: {team_path}")
        sys.exit(1)
else:
    team_path = None

# run_session() lines 374-386: team_yaml param already exists
async def run_session(
    ...
    team_yaml: Path | None = None,
):
    _team_path = team_yaml if team_yaml else TEAM_CONFIG  # line 399
```

Story 3.6 adds metadata recording (Task 5) to the existing `run_session()`. The team loading (`load_team()`) and session passing are already wired.

### BROWNFIELD: `load_team()` Current Behavior (MUST UNDERSTAND BEFORE TOUCHING)

Current `load_team()` (`agentteam/agents/loader.py:57-77`) has a subtle issue in the list-based branch:

```python
def load_team(config_path: str) -> TeamConfig:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(...)
    ...
    if isinstance(raw["agents"], list):
        for entry in raw["agents"]:
            agent_key = entry["agent_key"]
            agent_file = entry.get("file")
            if agent_file:
                agent_path = _AGENTS_DIR / agent_file  # ← hardcoded to _AGENTS_DIR
                agents[agent_key] = load_agent(str(agent_path)) if agent_path.exists() else load_agent_by_key(agent_key)
```

**Fix for Task 3.2** — add team-dir fallback when `_AGENTS_DIR / agent_file` not found:

```python
def load_team(config_path: str) -> TeamConfig:
    path = Path(config_path)
    team_dir = path.parent  # ← ADD THIS
    if not path.exists():
        raise FileNotFoundError(...)
    ...
    if isinstance(raw["agents"], list):
        for entry in raw["agents"]:
            agent_key = entry["agent_key"]
            agent_file = entry.get("file")
            if agent_file:
                agent_path = _AGENTS_DIR / agent_file
                if not agent_path.exists():
                    agent_path = team_dir / agent_file  # ← ADD THIS fallback
                agents[agent_key] = load_agent(str(agent_path)) if agent_path.exists() else load_agent_by_key(agent_key)
```

The `else` branch (dict-based `agents`) doesn't use file refs — no change needed there.

### `assign_rounds_from_job_types()` — Algorithm and Exact API

```python
from agentteam.types import JobType, TeamConfig

_JOB_TO_ROUND: dict[str, str] = {
    "propose": "propose",
    "ideate": "propose",    # idea generators participate in the proposal round
    "critique": "critique",
    "evaluate": "evaluate",
    "simplify": "evaluate", # simplifiers join the evaluation round
}


def assign_rounds_from_job_types(team: TeamConfig) -> dict[str, list[str]]:
    """Derive discussion round groups from each agent's output.job type.

    Returns {"propose": [...], "critique": [...], "evaluate": [...]} with all
    three keys always present (empty list if no agents have that job).

    JobType.IDEATE maps to "propose" (idea generators participate in proposal round).
    JobType.SIMPLIFY maps to "evaluate".

    Raises:
        ValueError: If no agents qualify for the "propose" round (discussion
            cannot start without at least one proposer).
    """
    groups: dict[str, list[str]] = {"propose": [], "critique": [], "evaluate": []}
    for key, agent in team.agents.items():
        round_name = _JOB_TO_ROUND.get(agent.output.job.value, "propose")
        groups[round_name].append(key)
    if not groups["propose"]:
        raise ValueError(
            "Team has no agents with job=propose or job=ideate. "
            "At least one proposer is required to run a discussion."
        )
    return groups
```

Place `_JOB_TO_ROUND` as a module-level constant in `loader.py` (just before `assign_rounds_from_job_types`). Do NOT import `JobType` in the function body — it's already imported at module level via `from agentteam.types import AgentConfig, TeamConfig`. Add `JobType` to that import.

### Beta-Agent YAML Edit Pattern

The `output:` section in the beta-agent YAMLs currently looks like:

```yaml
output:
  operating_level: requirements
```

Add `job:` between `output:` and `operating_level:`:

```yaml
output:
  job: critique        # ← ADD (values: propose / critique / evaluate / ideate)
  operating_level: requirements
```

Job assignments for beta-agents (must match `experiment_modes.yaml` round groupings):
- `cognitive_architect` → `propose`
- `flow_orchestrator` → `propose`
- `systems_pragmatist` → `critique`
- `adversarial_critic` → `critique`
- `product_oracle` → `evaluate`
- `context_surgeon` → `evaluate`
- `idea_merchant` → `ideate`

Note: The other teams (spec-builders, ev18hornet, tmos-dreamers, etc.) already have `output.job` set correctly. Only the 7 beta-agent files need updating.

### `__init__.py` Update Pattern

Follow the existing pattern from Story 3.5:

```python
"""Agent and team loading from YAML files."""
from .drift import build_drift_reminder, detect_drift
from .loader import (
    assign_rounds_from_job_types,   # ← ADD
    list_agents, list_teams, load_agent, load_agent_by_key,
    load_team, load_team_by_name, resolve_agent,
)
__all__ = [
    "load_agent", "load_agent_by_key", "load_team", "load_team_by_name",
    "resolve_agent", "list_teams", "list_agents",
    "detect_drift", "build_drift_reminder",
    "assign_rounds_from_job_types",  # ← ADD
]
```

### Session Metadata Change — Exact Location

In `projects/engine/session/runner.py`, in `run_session()`, find the block that writes initial session state (around line 547-551):

```python
# CURRENT:
status["question_hash"] = q_hash
status["mode"] = mode_name
status["brief"] = brief_path.name
write_session_status(session_dir, status)

# AFTER change:
status["question_hash"] = q_hash
status["mode"] = mode_name
status["brief"] = brief_path.name
status["team"] = str(_team_path.resolve())  # ← ADD
write_session_status(session_dir, status)
```

`_team_path` is already in scope at this point (set at line 399). `resolve()` makes it absolute.

Note: `TEAM_CONFIG` is a `Path` object (line 47 of `discussion/engine.py`). `team_yaml` (the parameter) is also a `Path` or `None`. So `_team_path` is always a `Path` — `.resolve()` is safe on both.

### Test Scaffold for `tests/test_team_swapping.py`

```python
"""Tests for assign_rounds_from_job_types and load_team path resolution."""
import pytest
import yaml
from pathlib import Path

from agentteam.agents.loader import assign_rounds_from_job_types, load_team
from agentteam.types import AgentConfig, JobType, OutputConfig, TeamConfig


def make_team_with_jobs(**job_map) -> TeamConfig:
    """Build TeamConfig with agents having specific output.job values.

    Usage: make_team_with_jobs(alice="propose", bob="critique", carol="evaluate")
    """
    agents = {}
    for key, job_str in job_map.items():
        agents[key] = AgentConfig(
            name=key.title(),
            description=f"Test agent with job {job_str}.",
            output=OutputConfig(job=JobType(job_str)),
        )
    return TeamConfig(agents=agents)


class TestAssignRoundsFromJobTypes:
    def test_basic_three_round_assignment(self):
        """Agents with propose/critique/evaluate jobs → correct groups."""
        team = make_team_with_jobs(a="propose", b="critique", c="evaluate")
        result = assign_rounds_from_job_types(team)
        assert result["propose"] == ["a"]
        assert result["critique"] == ["b"]
        assert result["evaluate"] == ["c"]

    def test_ideate_maps_to_propose_round(self):
        """ideate agents participate in the propose round."""
        team = make_team_with_jobs(merchant="ideate", critic="critique", eval="evaluate")
        result = assign_rounds_from_job_types(team)
        assert "merchant" in result["propose"]
        assert result["critique"] == ["critic"]

    def test_simplify_maps_to_evaluate_round(self):
        """simplify agents participate in the evaluate round."""
        team = make_team_with_jobs(p="propose", s="simplify")
        result = assign_rounds_from_job_types(team)
        assert "s" in result["evaluate"]

    def test_no_proposers_raises_value_error(self):
        """Team with no propose/ideate agents raises ValueError."""
        team = make_team_with_jobs(a="critique", b="evaluate")
        with pytest.raises(ValueError, match="propose"):
            assign_rounds_from_job_types(team)

    def test_all_three_keys_always_present(self):
        """All three round keys are always in the return dict, even if empty."""
        team = make_team_with_jobs(a="propose")
        result = assign_rounds_from_job_types(team)
        assert "propose" in result
        assert "critique" in result
        assert "evaluate" in result
        assert result["critique"] == []
        assert result["evaluate"] == []

    def test_real_beta_agents_team_loads_and_assigns(self):
        """Integration: beta-agents team assigns agents matching experiment_modes.yaml."""
        from agentteam.agents.loader import load_team_by_name
        team = load_team_by_name("beta-agents")
        result = assign_rounds_from_job_types(team)
        # cognitive_architect and flow_orchestrator are proposers
        assert "cognitive_architect" in result["propose"]
        assert "flow_orchestrator" in result["propose"]
        # systems_pragmatist and adversarial_critic are critics
        assert "systems_pragmatist" in result["critique"]
        assert "adversarial_critic" in result["critique"]
        # product_oracle and context_surgeon are evaluators
        assert "product_oracle" in result["evaluate"]
        assert "context_surgeon" in result["evaluate"]


class TestLoadTeamPathResolution:
    _MINIMAL_AGENT_YAML = """\
name: Portable Agent
description: Agent for path-resolution testing.
position:
  role: tester
  drives: [drive one, drive two, drive three]
  pushback_on: [pushback one, pushback two, pushback three]
technique:
  primary: testing
  behaviors: [b one, b two, b three, b four, b five]
output:
  job: propose
  operating_level: requirements
"""

    def test_agent_file_resolved_relative_to_team_dir(self, tmp_path):
        """Agent files in same dir as team YAML load correctly."""
        agent_file = tmp_path / "my_agent.yaml"
        agent_file.write_text(self._MINIMAL_AGENT_YAML, encoding="utf-8")

        team_yaml = tmp_path / "my_team.yaml"
        team_yaml.write_text(yaml.dump({
            "name": "Portable Team",
            "agents": [{"agent_key": "portable", "file": "my_agent.yaml"}],
        }), encoding="utf-8")

        team = load_team(str(team_yaml))
        assert "portable" in team.agents
        assert team.agents["portable"].name == "Portable Agent"

    def test_agent_file_in_agents_dir_still_works(self, tmp_path):
        """Existing teams with files in _AGENTS_DIR continue to load."""
        from agentteam.agents.loader import load_team_by_name
        team = load_team_by_name("beta-agents")
        assert len(team.agents) >= 6
```

Key test notes:
- `test_real_beta_agents_team_loads_and_assigns` requires Task 1 (beta-agent YAML updates) to pass — it will fail if `job:` is missing from those files (all would default to `propose`, breaking the critique/evaluate assertions)
- Use `asyncio_mode = "auto"` is in pytest config — no `@pytest.mark.asyncio` needed; these tests are all sync so no issue
- `make_team_with_jobs` helper — directly constructs `TeamConfig` with `OutputConfig(job=JobType(...))` — matches the Pydantic model exactly
- Do NOT mock YAML loading in path-resolution tests — use `tmp_path` fixture with real file writes

### Pydantic Note — `JobType` Enum Access

`agent.output.job` is a `JobType` enum. Its `.value` gives the lowercase string:
```python
>>> agent.output.job
<JobType.PROPOSE: 'propose'>
>>> agent.output.job.value
'propose'
```

`_JOB_TO_ROUND` keys are strings (`.value`). The `.get(..., "propose")` fallback handles any future unknown job types gracefully.

### Architecture Rules

- No `print()` or `logging` in `agentteam/` — library code only
- Python 3.11+ syntax
- `assign_rounds_from_job_types` goes in `loader.py` (it's a team-loading concern), not a new file
- Tests are flat in `_SYSTEM/tests/` — `tests/test_team_swapping.py`
- Session metadata change is in `projects/engine/session/runner.py` (engine scope, not library scope)

### File Touch List

| File | Action |
|---|---|
| `data/discussionAgents/beta-agents__cognitive_architect.yaml` | **MODIFY** — add `job: propose` to output section |
| `data/discussionAgents/beta-agents__flow_orchestrator.yaml` | **MODIFY** — add `job: propose` to output section |
| `data/discussionAgents/beta-agents__systems_pragmatist.yaml` | **MODIFY** — add `job: critique` to output section |
| `data/discussionAgents/beta-agents__adversarial_critic.yaml` | **MODIFY** — add `job: critique` to output section |
| `data/discussionAgents/beta-agents__product_oracle.yaml` | **MODIFY** — add `job: evaluate` to output section |
| `data/discussionAgents/beta-agents__context_surgeon.yaml` | **MODIFY** — add `job: evaluate` to output section |
| `data/discussionAgents/beta-agents__idea_merchant.yaml` | **MODIFY** — add `job: ideate` to output section |
| `agentteam/agents/loader.py` | **MODIFY** — add `assign_rounds_from_job_types()` + fix `load_team()` path resolution |
| `agentteam/agents/__init__.py` | **MODIFY** — export `assign_rounds_from_job_types` |
| `projects/engine/session/runner.py` | **MODIFY** — add `status["team"]` metadata line |
| `tests/test_team_swapping.py` | **CREATE** — full test suite |

### References

- [Source: `agentteam/agents/loader.py`] — `load_team()` list-branch (lines 65-75), `load_team_by_name()` (lines 38-54) — only modify `load_team()`
- [Source: `agentteam/agents/__init__.py`] — current exports from Story 3.5; follow same pattern
- [Source: `agentteam/types/agent.py`] — `JobType` enum (line 46), `OutputConfig.job` (line 104)
- [Source: `projects/engine/session/runner.py`] — `run_session()` lines 374-550; `_team_path` set at line 399; status dict written at line 550
- [Source: `projects/engine/discussion/engine.py`] — `TEAM_CONFIG` (line 47), `experiment_modes.yaml` round groups (for reference only — do NOT change these)
- [Source: `projects/engine/config/experiment_modes.yaml`] — current hardcoded agent-to-round assignments; used to derive correct `job:` values for beta-agent YAML updates
- [Source: `tests/test_agent_loader.py`] — existing loader test patterns, YAML fixture strings, `_AGENTS_DIR` reference
- [Source: `tests/conftest.py`] — `minimal_agent`, `tmp_path` fixture usage

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- No failures. All 8 new tests passed on first run. Full suite 387/387 green immediately.
- Task 1 was pre-done: all 7 beta-agent YAMLs already had correct `job:` fields when story was opened.

### Completion Notes List

- All 7 beta-agent YAMLs confirmed to have correct `output.job` values (cognitive_architect/flow_orchestrator→propose, systems_pragmatist/adversarial_critic→critique, product_oracle/context_surgeon→evaluate, idea_merchant→ideate)
- Added `assign_rounds_from_job_types(team: TeamConfig) -> dict[str, list[str]]` to `agentteam/agents/loader.py` with module-level `_JOB_TO_ROUND` mapping; ideate→propose, simplify→evaluate; raises ValueError if propose list is empty
- Added `JobType` to imports in `loader.py`
- Fixed `load_team()` to capture `team_dir = path.parent` and fall back to `team_dir / agent_file` when `_AGENTS_DIR / agent_file` does not exist
- Exported `assign_rounds_from_job_types` from `agentteam/agents/__init__.py`
- Added `status["team"] = str(_team_path.resolve())` in `projects/engine/session/runner.py` after status["brief"] line
- Created `tests/test_team_swapping.py` with 8 tests: 6 in `TestAssignRoundsFromJobTypes` (including real beta-agents integration test), 2 in `TestLoadTeamPathResolution`
- 387/387 full suite passing — all 33 existing `test_agent_loader.py` tests pass (load_team changes are backwards-compatible)

### File List

- _SYSTEM/agentteam/agents/loader.py (modified)
- _SYSTEM/agentteam/agents/__init__.py (modified)
- _SYSTEM/projects/engine/session/runner.py (modified)
- _SYSTEM/tests/test_team_swapping.py (new)
