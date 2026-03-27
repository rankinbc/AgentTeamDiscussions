# Story 3.3: Identity Layer Prompt Builder

Status: done

## Story

As a developer,
I want personality traits rendered as natural language in the Identity layer,
So that agents internalize their personality as lived experience rather than following directives.

## Acceptance Criteria

1. **Given** a validated AgentConfig with personality traits
   **When** the Identity layer prompt is built
   **Then** each trait is rendered at 5 levels: "strongly [low]" (0.0-0.2), "lean toward [low]" (0.2-0.4), "balance [low] and [high]" (0.4-0.6), "quite [high]" (0.6-0.8), "extremely [high]" (0.8-1.0)

2. **Given** a validated AgentConfig with a position
   **When** the Identity layer is built
   **Then** position is framed as the agent's authentic self-interest: "What drives you: ...", "You actively push back on: ..."

3. **Given** a validated AgentConfig with a technique
   **When** the Identity layer is built
   **Then** technique is presented as the agent's natural reasoning approach (style_description + behavioral rules)

4. **Given** the assembled Identity layer
   **When** it is inspected
   **Then** it reads as a coherent character description, not a bulleted config dump

5. **Given** a validated AgentConfig
   **When** `build_identity_layer()` is called
   **Then** rendering uses Jinja2 templates from `agentteam/prompts/templates/identity.j2`

## Tasks / Subtasks

- [x] Task 1: Create `agentteam/prompts/templates/identity.j2` (AC: 5)
  - [x] 1.1: Create directory `agentteam/prompts/templates/`
  - [x] 1.2: Write `identity.j2` template — structure matches current `build_system_prompt()` identity sections: name block, role block (drives + pushback_on + intensity), personality block, technique block
  - [x] 1.3: Use Jinja2 `trim_blocks=True`, `lstrip_blocks=True` — prevents spurious blank lines from control blocks

- [x] Task 2: Create `agentteam/prompts/identity.py` (AC: 1–5)
  - [x] 2.1: Move `_describe_trait()` from `builder.py` to `identity.py`
  - [x] 2.2: Add `_personality_lines(p: PersonalityConfig) -> list[str]` — extracted from `_build_personality_section()`, returns list of rendered trait sentences
  - [x] 2.3: Add `_intensity_line(intensity: float) -> str` — extracted from `build_system_prompt()` position block
  - [x] 2.4: Add module-level lazy `_jinja_env` using `FileSystemLoader` pointed at `Path(__file__).parent / "templates"`
  - [x] 2.5: Implement `build_identity_layer(agent: AgentConfig) -> str` — prepares context dict, calls `env.get_template("identity.j2").render(**context)`, returns rendered string
  - [x] 2.6: No `print()` or `logging` anywhere in the module

- [x] Task 3: Update `agentteam/prompts/builder.py` (AC: 1–4 regression)
  - [x] 3.1: Remove `_describe_trait()` and `_build_personality_section()` — now live in `identity.py`
  - [x] 3.2: Import `build_identity_layer` from `.identity`
  - [x] 3.3: In `build_system_prompt()`, replace the first four inline sections (name/description, position, personality, technique) with a single call to `build_identity_layer(agent)` — the result is `sections[0]` in the sections list
  - [x] 3.4: Keep `_build_antislop_section()`, `build_perspective_reminder()`, `build_context_lens()`, `filter_prior_rounds()` unchanged in `builder.py`

- [x] Task 4: Update `agentteam/prompts/__init__.py`
  - [x] 4.1: Add `build_identity_layer` to imports and `__all__`

- [x] Task 5: Create `tests/test_identity.py` (AC: 1–5)
  - [x] 5.1: `TestBuildIdentityLayer` class — test: name appears, description appears, drives appear, pushback appears, high/mid/low trait rendering (test all 5 bands), technique name appears, style_description appears, behaviors listed, domain_affinities line appears when set
  - [x] 5.2: `TestIdentityJinja2Rendering` class — test: output is string, template file exists at `agentteam/prompts/templates/identity.j2`, identical output when called twice on same agent (idempotent), different agents produce different output
  - [x] 5.3: Add module docstring: `"""Tests for agentteam.prompts.identity — Jinja2-rendered identity layer."""`
  - [x] 5.4: Use `minimal_agent` and `rich_agent` fixtures from conftest — no new fixtures needed

- [x] Task 6: Run tests and verify no regressions
  - [x] 6.1: `python -m pytest tests/test_identity.py -v` — all pass
  - [x] 6.2: `python -m pytest tests/test_prompts_builder.py -v` — all 20 existing tests still pass
  - [x] 6.3: `python -m pytest` — full suite green

## Dev Notes

### BROWNFIELD CRITICAL: `builder.py` Already Implements ACs 1–4 — Refactor, Do NOT Rewrite

`agentteam/prompts/builder.py` already has the full identity layer inline. Story 3.3 is a **structural refactor**: extract the identity-specific logic into `identity.py` + `identity.j2`, then update `builder.py` to call it. The output of `build_system_prompt()` must be identical before and after.

### Architecture File Location: Prompt Templates Go in `agentteam/prompts/templates/`

Architecture spec: `agentteam/prompts/templates/*.j2`. This is **NOT** `_SYSTEM/templates/`. The ConfigLoader's default template dir (`_SYSTEM/templates/`) is for config-driven templates; prompt layer templates are bundled inside the package.

Use a module-level Jinja2 Environment in `identity.py` (same lazy-init pattern as ConfigLoader):

```python
_TEMPLATES_DIR = Path(__file__).parent / "templates"
_jinja_env = None


def _get_jinja_env():
    global _jinja_env
    if _jinja_env is None:
        from jinja2 import Environment, FileSystemLoader
        _jinja_env = Environment(
            loader=FileSystemLoader(str(_TEMPLATES_DIR)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
    return _jinja_env
```

Do NOT use `ConfigLoader` or `render_prompt()` from `agentteam/config/loader.py` — that's for config-dir templates.

### What `build_identity_layer()` Must Return

The Jinja2 template + function must produce the SAME text as the first 4 sections currently built inline in `build_system_prompt()`. Specifically:

**Section 1 — Name block:**
```
# You are {name}

{description}
```

**Section 2 — Role block:**
```
## Your Role: {role.title()}

What drives you:
- {drive_1}
...

You actively push back on:
- {pushback_1}
...

{intensity_line}
```
Where `intensity_line` is one of:
- `>= 0.7` → `"You express your views with force and passion -- you're not here to play nice."`
- `>= 0.4` → `"You express your views with conviction but remain open to dialogue."`
- `< 0.4` → `"You express your views with measured restraint."`

**Section 3 — Personality block:**
```
## Your Personality

{trait_line_1}
{trait_line_2}
...
```
Each trait via `_describe_trait(value, low_desc, high_desc)`:
- `>= 0.8` → `"You are extremely {high_desc}."`
- `>= 0.6` → `"You are quite {high_desc}."`
- `>= 0.4` → `"You balance {low_desc} and {high_desc} tendencies."`
- `>= 0.2` → `"You lean toward being {low_desc}."`
- `< 0.2` → `"You are strongly {low_desc}."`

Trait definitions (low_desc → high_desc):
- `assertiveness`: `"reserved and diplomatic"` → `"assertive -- you fight hard for your ideas and don't back down easily"`
- `creativity_temp`: `"conventional and proven-path"` → `"wildly creative -- you reach for novel, unexpected ideas"`
- `risk_tolerance`: `"risk-averse and safety-focused"` → `"risk-tolerant -- you embrace bold bets and untested approaches"`
- `attention_span`: `"a topic-hopper who jumps between ideas freely"` → `"deeply focused -- you drill into one thread exhaustively"`
- `stubbornness`: `"flexible and quick to update your views"` → `"stubborn -- you hold your ground and require strong evidence to change your mind"`
- `idea_receptivity`: `"an agenda driver who stays focused on your own ideas"` → `"deeply engaged with others' ideas -- you build on what others say and genuinely absorb their perspective"`
- `bluntness`: `"diplomatic and tactful -- you soften hard truths"` → `"brutally direct -- you say exactly what you think with zero sugar-coating"`
- `patience`: `"impatient -- you cut off tangents and push to move on"` → `"patient -- you let discussions breathe and don't rush to conclusions"`
- `cognitive_style`: rendered as `f"Your cognitive style is {p.cognitive_style.value} -- this shapes how you approach every problem."`
- `emotional_baseline`: rendered as `f"Your emotional baseline is {p.emotional_baseline.value} -- this colors your reactions and framing."`
- `domain_affinities` (optional): `f"You naturally draw from these domains: {', '.join(p.domain_affinities)}."`

**Section 4 — Technique block:**
```
## Your Thinking Technique: {primary.replace('_', ' ').title()}

{style_description}

Behavioral rules:
- {behavior_1}
...
```

### How to Update `build_system_prompt()` in `builder.py`

Replace sections 1–4 inline assembly with one call:

```python
# BEFORE (4 separate sections appended individually):
sections.append(f"# You are {agent.name}\n\n{agent.description.strip()}")
sections.append("\n".join(pos_lines))
sections.append(f"## Your Personality\n\n{_build_personality_section(agent.personality)}")
sections.append("\n".join(tech_lines))

# AFTER (single identity layer call):
from .identity import build_identity_layer
sections.append(build_identity_layer(agent))
```

The identity layer renders all 4 sections joined with `"\n\n"` internally. The outer `"\n\n".join(sections)` in `build_system_prompt()` then adds the separator between identity + the remaining sections (Voice, Output, Anti-Slop, Remember).

### Jinja2 Template Design: Use `trim_blocks` and `lstrip_blocks`

With `trim_blocks=True` + `lstrip_blocks=True`, Jinja2 block tags are invisible in output — no extra blank lines from `{% if %}` / `{% for %}` / `{% endif %}` / `{% endfor %}`. Use this to conditionally include blocks (drives, pushback, domain_affinities) without adding spurious whitespace.

### `build_system_prompt()` Output Must Not Change

The existing 20 tests in `test_prompts_builder.py` verify the output content of `build_system_prompt()`. After this refactor, all 20 must continue to pass — the function's public behavior is unchanged.

### Architecture Rules

- No `print()` or `logging` in `agentteam/` — library code only
- Python 3.11+ syntax
- `asyncio_mode = "auto"` in pytest — no `@pytest.mark.asyncio` needed
- Line length: 100 (ruff)

### File Touch List

| File | Action |
|---|---|
| `agentteam/prompts/templates/identity.j2` | **CREATE** — Jinja2 template for identity layer |
| `agentteam/prompts/identity.py` | **CREATE** — `build_identity_layer()` + extracted helpers |
| `agentteam/prompts/builder.py` | **MODIFY** — remove extracted helpers, call `build_identity_layer()` |
| `agentteam/prompts/__init__.py` | **MODIFY** — export `build_identity_layer` |
| `tests/test_identity.py` | **CREATE** — identity layer tests |

### References

- [Source: `agentteam/prompts/builder.py`] — current inline implementation to extract from
- [Source: `agentteam/config/loader.py`] — Jinja2 Environment setup pattern to follow (lazy init, `trim_blocks`, `lstrip_blocks`)
- [Source: `agentteam/prompts/__init__.py`] — current exports to extend
- [Source: `tests/conftest.py`] — `minimal_agent`, `rich_agent` fixtures available
- [Source: `tests/test_prompts_builder.py`] — 20 existing tests that must stay green
- [Source: Architecture spec] — `agentteam/prompts/templates/*.j2` location

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- 3 test failures on first run: `TechniqueConfig.behaviors` requires min 5 items (Story 3.1 schema constraint) — tests fixed to use 5+ behaviors

### Completion Notes List

- Created `agentteam/prompts/templates/identity.j2` — Jinja2 template rendering all 4 identity sections (name/desc, role, personality, technique) with `trim_blocks`+`lstrip_blocks` to suppress control-tag whitespace
- Created `agentteam/prompts/identity.py` with `build_identity_layer()`, `_describe_trait()`, `_personality_lines()`, `_intensity_line()` helpers; module-level lazy Jinja2 env via `FileSystemLoader` pointed at bundled templates dir
- Updated `builder.py`: removed `_describe_trait()` and `_build_personality_section()`; first sections block replaced with `build_identity_layer(agent)` call; voice/output/antislop/remember sections unchanged
- Updated `prompts/__init__.py` to export `build_identity_layer`
- 27 new tests in `test_identity.py`: all 5 trait bands, drives/pushback presence, technique rendering, template existence, idempotency, no raw Jinja2 tags in output
- 320/320 full suite passing — all 20 existing `test_prompts_builder.py` tests pass (public API of `build_system_prompt()` unchanged)

### Review Findings

- [x] [Review][Patch] Add boundary-exact tests for `_describe_trait()` at 0.2/0.4/0.6/0.8 and `_intensity_line()` at 0.4/0.7 — threshold-slip would silently pass current suite [tests/test_identity.py]
- [x] [Review][Defer] `_jinja_env` module global uses no lock — same lazy-init pattern as ConfigLoader; CPython GIL prevents corruption; pre-existing design choice
- [x] [Review][Defer] `style_description=""` suppression path not directly tested — empty default suppresses the section via Jinja2 `{% if %}` check; covered implicitly by minimal_agent tests
- [x] [Review][Defer] Multi-line `description`/`domain_affinities` entries produce extra blank lines in rendered output — no agent YAMLs trigger this; address in E4 context assembly
- [x] [Review][Defer] `keep_trailing_newline=True` in Jinja2 env not specified in Dev Notes — harmless; taken from ConfigLoader pattern
- [x] [Review][Defer] `filter_prior_rounds` idx=-1 edge case (no `\n[` in tail of truncated text) — pre-existing function, unchanged by this story; address in Epic 5 reliability work

### File List

- _SYSTEM/agentteam/prompts/templates/identity.j2 (new)
- _SYSTEM/agentteam/prompts/identity.py (new)
- _SYSTEM/agentteam/prompts/builder.py (modified)
- _SYSTEM/agentteam/prompts/__init__.py (modified)
- _SYSTEM/tests/test_identity.py (new)
