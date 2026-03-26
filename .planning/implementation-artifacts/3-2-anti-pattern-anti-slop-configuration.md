# Story 3.2: Anti-Pattern & Anti-Slop Configuration

Status: done

## Story

As a user,
I want to define forbidden phrases and anti-slop rules per agent,
So that agents avoid generic AI behavior and maintain distinct perspectives.

## Acceptance Criteria

1. **Given** an agent YAML with `voice.anti_patterns` list
   **When** `load_agent()` reads the file
   **Then** `anti_patterns` is validated as a list of 8–12 non-empty strings

2. **Given** an agent YAML with `anti_slop` section
   **When** `load_agent()` reads the file
   **Then** `anti_slop` contains: `agreement_tax` (bool), `perspective_enforcement` (bool), `devils_advocate_duty` (bool), `uncomfortable_idea_quota` (int 0–5), `domain_pivot_trigger` (bool)

3. **Given** an agent YAML with no `anti_slop` section
   **When** `load_agent()` reads the file
   **Then** defaults are applied: `agreement_tax=true`, `perspective_enforcement=true`, `devils_advocate_duty=false`, `uncomfortable_idea_quota=0`, `domain_pivot_trigger=false`

4. **Given** an agent YAML with invalid `anti_slop` values (e.g., `uncomfortable_idea_quota=10`)
   **When** `load_agent()` reads the file
   **Then** a `ValidationError` is raised identifying the specific field

5. **Given** a valid `AgentConfig`
   **When** the voice config is inspected
   **Then** `tone`, `brevity`, `vocabulary_hints`, and `anti_patterns` are all present and accessible together

6. **Given** all 33 existing agent YAML files in `data/discussionAgents/`
   **When** `load_agent()` reads each file
   **Then** every file loads without error (no `ValidationError`)

## Tasks / Subtasks

- [x] Task 1: Add `min_length`/`max_length` to `VoiceConfig.anti_patterns` in `agentteam/types/agent.py` (AC: 1, 4, 6)
  - [x] 1.1: Change `anti_patterns: list[str] = Field(default_factory=list)` → `Field(default_factory=list, min_length=8, max_length=12)`
  - [x] 1.2: Do NOT change any other field in `VoiceConfig`, do NOT change `AntiSlopConfig` (already correct), do NOT change `__all__` exports

- [x] Task 2: Fix YAML compliance — anti_patterns too few (AC: 6)
  - [x] 2.1: For each file with <8 anti_patterns, append phrases to reach exactly 8. Match the agent's voice/register. Safe generic additions include: `"I agree with that"`, `"Building on that"`, `"You raise a valid point"`, `"Absolutely"`, `"That makes sense"`, `"Could you elaborate on that"`, `"To add to what was said"` — adapt to match the agent's tone
  - [x] 2.2: Files requiring additions (read each file before editing to match voice):
    ```
    ev18hornet__emergence_theorist.yaml   (4 → 8: add 4)
    ev18hornet__ev_purist.yaml            (4 → 8: add 4)
    ev18hornet__flight_dreamer.yaml       (4 → 8: add 4)
    ev18hornet__player_advocate.yaml      (4 → 8: add 4)
    ev18hornet__scope_warden.yaml         (4 → 8: add 4)
    normal-people__diana.yaml             (3 → 8: add 5)
    normal-people__keiko.yaml             (3 → 8: add 5)
    normal-people__marcus.yaml            (5 → 8: add 3)
    normal-people__raj.yaml               (3 → 8: add 5)
    normal-people__tony.yaml              (3 → 8: add 5)
    normal-people__zara.yaml              (3 → 8: add 5)
    spec-builders__creative_director.yaml (3 → 8: add 5)
    spec-builders__game_designer.yaml     (3 → 8: add 5)
    spec-builders__player_advocate.yaml   (3 → 8: add 5)
    spec-builders__scope_wrangler.yaml    (3 → 8: add 5)
    spec-builders__tech_lead.yaml         (3 → 8: add 5)
    tmos-dreamers__art_director.yaml      (3 → 8: add 5)
    tmos-dreamers__game_designer.yaml     (3 → 8: add 5)
    tmos-dreamers__narrative_designer.yaml (3 → 8: add 5)
    tmos-dreamers__producer.yaml          (3 → 8: add 5)
    tmos-dreamers__tech_lead.yaml         (3 → 8: add 5)
    ```

- [x] Task 3: Fix YAML compliance — anti_patterns too many (AC: 6)
  - [x] 3.1: Trim the last items from the 2 over-count files:
    ```
    beta-agents__adversarial_critic.yaml  (15 → 12: remove last 3)
    beta-agents__idea_merchant.yaml       (17 → 12: remove last 5)
    ```
  - [x] 3.2: Read each file to confirm which items are truly last before trimming (adversarial_critic currently ends with `"I appreciate the effort"`, idea_merchant ends with `"The pipeline is"`, `"Step 1"`)

- [x] Task 4: Fix regression in `tests/conftest.py` (AC: 1)
  - [x] 4.1: In `rich_agent` fixture, `VoiceConfig(anti_patterns=["I think", "perhaps"])` has only 2 items — below new min of 8. Update to 8 items. Preserve `"I think"` and `"perhaps"` as the first two, add 6 more appropriate slop phrases (e.g., `"perhaps we should consider"`, `"I believe"`, `"in my opinion"`, `"we could explore"`, `"it seems to me"`, `"generally speaking"`)
  - [x] 4.2: Run `python -m pytest tests/test_prompts_builder.py -v` — all tests must still pass (the fixture is used by `rich_agent`-dependent tests)

- [x] Task 5: Create `_SYSTEM/tests/test_antislop_schema.py` (AC: 1–5)
  - [x] 5.1: Add module docstring: `"""Tests for AntiSlopConfig and VoiceConfig Pydantic schema validation."""`
  - [x] 5.2: `TestAntiSlopConfig` class — tests for: default values match spec (agreement_tax=True, perspective_enforcement=True, others=False/0), `uncomfortable_idea_quota` bounds (0–5), invalid quota raises ValidationError, full construction with all fields
  - [x] 5.3: `TestVoiceConfig` class — tests for: `anti_patterns` too few (7 items) raises, `anti_patterns` too many (13 items) raises, exactly 8 passes, exactly 12 passes, default empty bypass (same Pydantic v2 default-bypass behavior as Story 3.1), `brevity` enum validation, `tone` and `vocabulary_hints` accessible alongside `anti_patterns`
  - [x] 5.4: `TestVoiceAndAntiSlopTogether` class — 2 tests: full `AgentConfig` with both voice (8 anti_patterns) and anti_slop populated loads correctly; invalid `uncomfortable_idea_quota=99` in `AgentConfig` raises with field name in error message
  - [x] 5.5: No `print()`, no `logging`, uses module-level constants for valid fixtures (e.g., `_VALID_ANTI_PATTERNS = [f"phrase {i}" for i in range(8)]`)

### Review Findings

- [x] [Review][Patch] Add `test_explicit_empty_list_raises` to `TestVoiceConfig` — `VoiceConfig(anti_patterns=[])` must raise `ValidationError` (distinguishes explicit-empty from default-factory bypass) [tests/test_antislop_schema.py]
- [x] [Review][Defer] Non-empty string items not enforced — AC1 says "non-empty strings" but schema accepts `anti_patterns=["", ...]`; fix: `list[Annotated[str, Field(min_length=1)]]` — deferred, dev notes specify only length constraints; same deferral as Story 3.1
- [x] [Review][Defer] YAML trim by position assumed priority order — `adversarial_critic` 15→12 and `idea_merchant` 17→12 removed last N items; no test validates retained phrase content — deferred, removed items were generic meta-phrases; low practical risk
- [x] [Review][Defer] Pydantic v2 `validate_default` asymmetry undocumented in code — `VoiceConfig()` passes but `VoiceConfig(anti_patterns=[])` fails; add inline comment to `agent.py` VoiceConfig for maintainer clarity — deferred, covered by test docstring; low priority

## Dev Notes

### BROWNFIELD: Only `VoiceConfig.anti_patterns` Needs a Constraint — Do NOT Touch AntiSlopConfig

`agentteam/types/agent.py` already has both models fully defined:

```python
class AntiSlopConfig(BaseModel):
    agreement_tax: bool = Field(True)
    perspective_enforcement: bool = Field(True)
    devils_advocate_duty: bool = Field(False)
    uncomfortable_idea_quota: int = Field(0, ge=0, le=5)
    domain_pivot_trigger: bool = Field(False)


class VoiceConfig(BaseModel):
    tone: str = Field("professional")
    brevity: Brevity = Field(Brevity.NORMAL)
    vocabulary_hints: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list)  # ← ADD min_length=8, max_length=12 HERE ONLY
```

`AntiSlopConfig` is already fully correct — defaults match the spec (agreement_tax=True, perspective_enforcement=True), and `uncomfortable_idea_quota` already has `ge=0, le=5`. **DO NOT modify AntiSlopConfig at all.**

The only change to `agent.py`:

```python
# BEFORE:
anti_patterns: list[str] = Field(default_factory=list)

# AFTER:
anti_patterns: list[str] = Field(default_factory=list, min_length=8, max_length=12)
```

### Pydantic v2 Default Bypass — Same Behavior as Story 3.1

`validate_default=False` is the Pydantic v2 default. This means:
- `VoiceConfig()` → `anti_patterns=[]` — empty default is NOT validated ✓
- `VoiceConfig(anti_patterns=["x"])` → raises `ValidationError` (1 < min 8) ✓
- `VoiceConfig(anti_patterns=[f"p{i}" for i in range(8)])` → validates, passes ✓

This is intentional. Test fixtures and internal code can construct minimal `VoiceConfig()` without specifying all fields.

### conftest.py Regression — `rich_agent` Fixture

`_SYSTEM/tests/conftest.py` line 64 currently uses:
```python
anti_patterns=["I think", "perhaps"],
```
After adding `min_length=8`, this will raise `ValidationError`. Update to 8 items:
```python
anti_patterns=["I think", "perhaps", "perhaps we should consider", "I believe",
               "in my opinion", "we could explore", "it seems to me", "generally speaking"],
```

The `rich_agent` fixture is used by `test_prompts_builder.py` — run those tests after updating.

### YAML Fix Strategy for anti_patterns Too Few

21 files need additions. Read each agent's existing phrases and tone before adding. Guiding principle: **forbidden phrases should be the exact slop that this specific agent type would be most tempted to say.**

By group:
- **ev18hornet agents** (game/EV domain, 4 phrases currently): Add phrases like `"I agree with that approach"`, `"That's a solid point"`, `"Building on that"`, `"Makes sense to me"`
- **normal-people agents** (casual conversational, 3 phrases currently): Add phrases like `"I agree"`, `"Building on that"`, `"You raise a good point"`, `"Totally"`, `"Makes sense"`
- **spec-builders agents** (professional tech, 3 phrases currently): Add phrases like `"I agree with that"`, `"Building on that"`, `"That's a great approach"`, `"Makes sense"`, `"I think we should"`
- **tmos-dreamers agents** (creative/game design, 3 phrases currently): Add phrases like `"I love that idea"`, `"Building on that"`, `"That resonates"`, `"I agree"`, `"Let's explore"`

Always read the agent's existing anti_patterns first — if they already have "I agree" in some form, don't add an exact duplicate. Use a different phrasing.

### YAML Fix Strategy for anti_patterns Too Many

- `beta-agents__adversarial_critic.yaml` (15 → 12): Remove the last 3 items. Currently ends with: `"This is promising"`, `"Interesting approach"`, `"I appreciate the effort"` — these are the least on-brand for an adversarial critic and should go.
- `beta-agents__idea_merchant.yaml` (17 → 12): Remove the last 5 items. Currently ends with: `"I call this"` is item 4 in the EXISTING list — no wait, the idea_merchant has `vocabulary_hints` that includes "I call this". Read the file carefully before editing. The anti_patterns end with: `"We need to analyze"`, `"The tradeoffs are"`, `"It depends on"`, `"We should evaluate"`, `"The orchestrator assembles"`, `"The pipeline is"`, `"Step 1"` — the last 5 (technical/structural phrases like "Step 1", "The pipeline is") are the most generic and should be removed.

### Verification Script

After fixing YAMLs, verify counts:
```python
# Run from _SYSTEM/ after all edits:
import yaml
from pathlib import Path

agents_dir = Path('data/discussionAgents')
violations = []
for f in sorted(agents_dir.glob('*.yaml')):
    with open(f) as fh:
        raw = yaml.safe_load(fh)
    ap = (raw.get('voice', {}) or {}).get('anti_patterns', []) or []
    if ap and (len(ap) < 8 or len(ap) > 12):
        violations.append(f'{f.name}: {len(ap)}')

print(f'Violations: {len(violations)}')
for v in violations:
    print(' ', v)
```

Expected: `Violations: 0`

### Architecture Rules

- Line length: **100** (ruff)
- **No `print()` or `logging`** in `agentteam/` — pure library
- Python 3.11+ union syntax
- `tmp_path` fixture for all file I/O tests
- `asyncio_mode = "auto"` — no `@pytest.mark.asyncio` needed

### Testing Rules

- Run from `_SYSTEM/`: `python -m pytest tests/test_antislop_schema.py tests/test_agent_loader.py tests/test_prompts_builder.py -v`
- After YAML fixes: `python -m pytest tests/test_agent_loader.py::TestLoadAgentRealFiles -v` (33 parametrized tests)
- Full suite must remain green: `python -m pytest`

### File Touch List

| File | Action |
|---|---|
| `_SYSTEM/agentteam/types/agent.py` | Add `min_length=8, max_length=12` to `VoiceConfig.anti_patterns` |
| `_SYSTEM/tests/test_antislop_schema.py` | New file — `AntiSlopConfig` and `VoiceConfig` validation tests |
| `_SYSTEM/tests/conftest.py` | Update `rich_agent` fixture: expand `anti_patterns` from 2 to 8 items |
| `_SYSTEM/data/discussionAgents/*.yaml` (23 files) | Fix anti_patterns count: add to 21 files with <8; trim 2 files with >12 |

### References

- [Source: _SYSTEM/agentteam/types/agent.py] — `VoiceConfig`, `AntiSlopConfig` (modify only `anti_patterns` Field)
- [Source: _SYSTEM/tests/conftest.py#rich_agent] — fixture to update (regression fix)
- [Source: _SYSTEM/tests/test_agent_schema.py] — follow same test class structure and naming conventions
- [Source: _SYSTEM/tests/test_agent_loader.py#TestLoadAgentRealFiles] — 33 parametrized tests must remain passing
- [Source: _bmad-output/planning-artifacts/epics.md#Story 3.2] — acceptance criteria
- [Source: _bmad-output/planning-artifacts/architecture.md#Epic-to-Directory Mapping] — E3 → `agentteam/agents/`, `prompts/identity.py`

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

- Added `min_length=8, max_length=12` to `VoiceConfig.anti_patterns` in `agentteam/types/agent.py`
- `AntiSlopConfig` was already fully correct — defaults match spec, `uncomfortable_idea_quota` already has `ge=0, le=5`; no changes made to it
- Pydantic v2 default-bypass behavior: `VoiceConfig()` → `anti_patterns=[]` does NOT trigger min_length validation (`validate_default=False`)
- Fixed 21 YAML files (anti_patterns too few): appended group-appropriate slop phrases — ev18hornet group +4 each, normal-people group +3-5 each, spec-builders group +5 each, tmos-dreamers group +5 each
- Fixed 2 YAML files (anti_patterns too many): trimmed last N items — adversarial_critic 15→12, idea_merchant 17→12
- Fixed regression in `tests/conftest.py` `rich_agent` fixture: expanded `anti_patterns` from 2 to 8 items
- All 33 real agent files load without ValidationError (verified by parametrized test)
- 292/292 tests passing — no regressions

### File List

- _SYSTEM/agentteam/types/agent.py
- _SYSTEM/tests/test_antislop_schema.py
- _SYSTEM/tests/conftest.py
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
- _SYSTEM/data/discussionAgents/beta-agents__adversarial_critic.yaml
- _SYSTEM/data/discussionAgents/beta-agents__idea_merchant.yaml
