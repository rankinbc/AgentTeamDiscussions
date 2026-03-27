# Story 3.4: Output Constraints & Anti-Pattern Enforcement

Status: done

## Story

As a user,
I want agents to respect word limits, format rules, and forbidden phrase lists,
So that output is consistently structured and free of generic AI slop.

## Acceptance Criteria

1. **Given** an agent config with a `brevity` setting
   **When** the prompt is assembled
   **Then** word limit is injected: `concise` → "Under 300 words.", `normal` → "Under 600 words.", `thorough` → no hard limit ("Be comprehensive when warranted, but don't pad.")

2. **Given** an agent config with an `operating_level`
   **When** the prompt is assembled
   **Then** operating level constrains the response framing: `requirements` → WHAT/WHY framing, `design` → decisions/tradeoffs framing, `implementation` → concrete/technical framing

3. **Given** an agent config with a `job` type
   **When** the prompt is assembled
   **Then** job type sets the response directive: `propose` / `critique` / `evaluate` / `simplify` / `ideate` each produce a distinct directive sentence

4. **Given** an agent config with a non-empty `anti_patterns` list
   **When** the prompt is assembled
   **Then** anti-patterns are rendered in the Voice section as an explicit "NEVER use these phrases:" list with each phrase quoted

5. **Given** an agent config with anti-slop rules enabled
   **When** the prompt is assembled
   **Then** anti-slop rules are rendered as behavioral constraints in a separate "## Anti-Slop Rules" section (agreement_tax, perspective_enforcement, devils_advocate_duty, uncomfortable_idea_quota, domain_pivot_trigger)

## Tasks / Subtasks

- [x] Task 1: Create `agentteam/prompts/templates/output.j2` (AC: 1–5)
  - [x] 1.1: Create `output.j2` in the existing `agentteam/prompts/templates/` directory
  - [x] 1.2: Write the Voice section block (`## Your Voice`, tone, optional vocabulary_hints, optional anti_patterns list)
  - [x] 1.3: Write the Output section block (`## Your Output`, level_desc, job_desc, brevity_desc — each pre-resolved in Python)
  - [x] 1.4: Write the conditional Anti-Slop section (`{% if antislop_text %}## Anti-Slop Rules\n\n{{ antislop_text }}{% endif %}`)
  - [x] 1.5: Use same Jinja2 env settings as `identity.j2`: `trim_blocks=True`, `lstrip_blocks=True`, `keep_trailing_newline=True`

- [x] Task 2: Create `agentteam/prompts/output.py` (AC: 1–5)
  - [x] 2.1: Add module-level `_TEMPLATES_DIR = Path(__file__).parent / "templates"` and lazy `_jinja_env` pattern (identical to `identity.py`)
  - [x] 2.2: Move `_build_antislop_section(a: AntiSlopConfig) -> str` from `builder.py` to `output.py` — function body unchanged
  - [x] 2.3: Add `_level_desc(level: OperatingLevel) -> str` — returns the exact string from the current `level_desc` dict in `build_system_prompt()`
  - [x] 2.4: Add `_job_desc(job: JobType) -> str` — returns the exact string from the current `job_desc` dict
  - [x] 2.5: Add `_brevity_desc(brevity: Brevity) -> str` — returns the exact string from the current `brevity_desc` dict
  - [x] 2.6: Implement `build_output_layer(agent: AgentConfig) -> str`:
    - Builds context dict (see Dev Notes for exact keys)
    - Calls `_get_jinja_env().get_template("output.j2").render(**context).rstrip()`
    - Returns rendered string
  - [x] 2.7: No `print()` or `logging` anywhere in the module

- [x] Task 3: Update `agentteam/prompts/builder.py` (AC: 1–5 regression)
  - [x] 3.1: Remove `_build_antislop_section()` — now lives in `output.py`
  - [x] 3.2: Remove the inline `level_desc`, `job_desc`, `brevity_desc` dicts from `build_system_prompt()`
  - [x] 3.3: Import `build_output_layer` from `.output`
  - [x] 3.4: In `build_system_prompt()`, replace the three inline sections (voice_lines, out_lines, antislop) with a single call: `sections.append(build_output_layer(agent))`
  - [x] 3.5: Keep `build_perspective_reminder()`, `build_context_lens()`, `filter_prior_rounds()`, and the `## Remember` section unchanged

- [x] Task 4: Update `agentteam/prompts/__init__.py`
  - [x] 4.1: Add `build_output_layer` to imports from `.output` and to `__all__`

- [x] Task 5: Create `tests/test_output.py` (AC: 1–5)
  - [x] 5.1: `TestBuildOutputLayer` class:
    - `test_voice_tone_in_output` — tone appears
    - `test_vocabulary_hints_in_output` — hints appear with repr-style single quotes
    - `test_anti_patterns_in_output` — each phrase appears quoted in "NEVER use these phrases:"
    - `test_no_vocabulary_hints_when_empty` — "Phrases that fit" absent
    - `test_no_anti_patterns_section_when_empty` — "NEVER use these phrases:" absent
    - `test_brevity_concise` — "300 words" appears
    - `test_brevity_normal` — "600 words" appears
    - `test_brevity_thorough` — "300 words" and "600 words" absent; "comprehensive" appears
    - `test_operating_level_requirements` — "WHAT and WHY" appears
    - `test_operating_level_design` — "design decisions and tradeoffs" appears
    - `test_operating_level_implementation` — "concrete and technical" appears
    - `test_job_type_propose` — "PROPOSE" appears
    - `test_job_type_critique` — "CRITIQUE" appears
    - `test_job_type_evaluate` — "EVALUATE" appears
    - `test_job_type_simplify` — "SIMPLIFY" appears
    - `test_job_type_ideate` — "IDEATE" appears
    - `test_antislop_agreement_tax_included` — "AGREEMENT TAX" appears when enabled
    - `test_antislop_perspective_enforcement_included` — "PERSPECTIVE LOCK" appears when enabled
    - `test_antislop_devils_advocate_included` — "DEVIL'S ADVOCATE DUTY" appears when enabled
    - `test_antislop_uncomfortable_quota_included` — "UNCOMFORTABLE IDEA QUOTA" appears when > 0
    - `test_antislop_domain_pivot_included` — "DOMAIN PIVOT" appears when enabled
    - `test_no_antislop_section_when_all_disabled` — "## Anti-Slop Rules" absent when all False/0
  - [x] 5.2: `TestOutputJinja2Rendering` class:
    - `test_returns_non_empty_string` — isinstance str, len > 0
    - `test_template_file_exists` — `_TEMPLATES_DIR / "output.j2"` exists
    - `test_idempotent` — same agent produces same output twice
    - `test_different_agents_produce_different_output` — minimal vs rich differ
    - `test_no_raw_jinja_tags_in_output` — `{{` and `{%` absent
    - `test_voice_section_header_present` — "## Your Voice" in output
    - `test_output_section_header_present` — "## Your Output" in output
  - [x] 5.3: Add module docstring: `"""Tests for agentteam.prompts.output — Jinja2-rendered output layer."""`
  - [x] 5.4: Use `minimal_agent` and `rich_agent` fixtures; construct additional `AgentConfig` inline for specific AC tests

- [x] Task 6: Run tests and verify no regressions
  - [x] 6.1: `python -m pytest tests/test_output.py -v` — all pass
  - [x] 6.2: `python -m pytest tests/test_prompts_builder.py -v` — all 20 existing tests still pass
  - [x] 6.3: `python -m pytest` — full suite green

## Dev Notes

### BROWNFIELD CRITICAL: `builder.py` Already Implements All 5 ACs — Refactor, Do NOT Rewrite

`agentteam/prompts/builder.py` already implements the full Voice, Output, and Anti-Slop sections inline in `build_system_prompt()`. Story 3.4 is a **structural refactor**: extract these sections into `output.py` + `output.j2`, then update `builder.py` to call `build_output_layer(agent)`. The output of `build_system_prompt()` must be **identical** before and after.

### What `build_output_layer()` Must Return

The Jinja2 template + function must produce the SAME text as the three sections currently built inline in `build_system_prompt()`. Specifically, a single string with the Voice section, Output section, and (optionally) Anti-Slop section joined with `"\n\n"`.

**Section 1 — Voice block:**
```
## Your Voice

Tone: {voice.tone}
[blank line]
Phrases that fit your style: {', '.join(repr(v) for v in voice.vocabulary_hints)}
[blank line]
NEVER use these phrases:
- "{anti_pattern_1}"
- "{anti_pattern_2}"
...
```
Vocabulary hints line and anti-patterns block are only included when non-empty.

**Section 2 — Output block:**
```
## Your Output

{level_desc}

{job_desc}

{brevity_desc}
```

Level descriptions (exact strings from builder.py):
- `requirements` → `"Focus on WHAT and WHY, not HOW. Describe behavior, rules, and decisions. Do NOT write code or schemas."`
- `design` → `"Focus on design decisions and tradeoffs. You may reference technical concepts but keep the emphasis on choices and rationale."`
- `implementation` → `"Be concrete and technical. Include schemas, code patterns, and specific implementation guidance."`

Job descriptions (exact strings from builder.py):
- `propose` → `"Your job is to PROPOSE -- put forward designs, ideas, and solutions."`
- `critique` → `"Your job is to CRITIQUE -- find problems, weak assumptions, and failure modes. Do not propose full alternatives."`
- `evaluate` → `"Your job is to EVALUATE -- assess proposals through user value, feasibility, and real-world impact."`
- `simplify` → `"Your job is to SIMPLIFY -- find the minimum viable version. Ask what can be cut or deferred."`
- `ideate` → `"Your job is to IDEATE -- generate 3+ specific, named, surprising ideas stolen from non-software domains."`

Brevity descriptions (exact strings from builder.py):
- `concise` → `"Be direct and brief. Under 300 words."`
- `normal` → `"Be thorough but not exhaustive. Under 600 words."`
- `thorough` → `"Be comprehensive when warranted, but don't pad."`

Note: `brevity` lives on `VoiceConfig`, not `OutputConfig`. The function takes `agent: AgentConfig` so both `agent.output` and `agent.voice` are accessible.

**Section 3 — Anti-Slop block (only if non-empty):**
```
## Anti-Slop Rules

{antislop_text}
```
Where `antislop_text` is the result of `_build_antislop_section(agent.anti_slop)` — the same function from `builder.py`, moved verbatim to `output.py`.

### Context Dict for `build_output_layer()`

```python
voice = agent.voice
out = agent.output
context = {
    "tone": voice.tone,
    "vocabulary_hints_str": ", ".join(repr(v) for v in voice.vocabulary_hints),
    "anti_patterns": voice.anti_patterns,
    "level_desc": _level_desc(out.operating_level),
    "job_desc": _job_desc(out.job),
    "brevity_desc": _brevity_desc(voice.brevity),
    "antislop_text": _build_antislop_section(agent.anti_slop),
}
```

Key: `vocabulary_hints_str` is pre-computed in Python (preserving `repr()` single-quote behavior) rather than rendering in Jinja2.

### Jinja2 Template: `output.j2`

```jinja2
## Your Voice

Tone: {{ tone }}
{% if vocabulary_hints_str %}

Phrases that fit your style: {{ vocabulary_hints_str }}
{% endif %}
{% if anti_patterns %}

NEVER use these phrases:
{% for ap in anti_patterns %}
- "{{ ap }}"
{% endfor %}
{% endif %}

## Your Output

{{ level_desc }}

{{ job_desc }}

{{ brevity_desc }}
{% if antislop_text %}

## Anti-Slop Rules

{{ antislop_text }}
{% endif %}
```

With `trim_blocks=True` + `lstrip_blocks=True`, block tags consume their trailing newline — no extra blank lines from `{% if %}`/`{% for %}`/`{% endif %}`/`{% endfor %}`. The blank lines in the template body become the section separators.

### How to Update `build_system_prompt()` in `builder.py`

```python
# BEFORE — three separate sections:
voice_lines = [f"## Your Voice\n\nTone: {voice.tone}"]
# ... vocabulary hints, anti-patterns ...
sections.append("\n".join(voice_lines))

out_lines = ["## Your Output"]
# ... level_desc, job_desc, brevity_desc dicts ...
sections.append("\n".join(out_lines))

antislop = _build_antislop_section(agent.anti_slop)
if antislop:
    sections.append(f"## Anti-Slop Rules\n\n{antislop}")

# AFTER — single output layer call:
from .output import build_output_layer
sections.append(build_output_layer(agent))
```

The output layer renders all three sections (Voice + Output + Anti-Slop) joined with `"\n\n"` internally. The outer `"\n\n".join(sections)` in `build_system_prompt()` then adds the separator between identity, output layer, and the `## Remember` section.

### `build_system_prompt()` Output Must Not Change

The existing 20 tests in `test_prompts_builder.py` verify the output content of `build_system_prompt()`. After this refactor, all 20 must continue to pass. Pay particular attention to:
- `test_anti_patterns_listed` — checks `"I think"` in rich_agent prompt (from voice.anti_patterns)
- `test_concise_brevity_mentioned` — checks `"300 words"` in rich_agent prompt
- `test_agreement_tax_rule_included` — checks `"AGREEMENT TAX"` in rich_agent prompt
- `test_devils_advocate_rule_included` — checks `"DEVIL"` in rich_agent prompt
- `test_no_antislop_section_when_all_disabled` — checks `"Anti-Slop"` absent when all rules disabled

### Lazy Jinja2 Environment Pattern

Use the same pattern as `identity.py`:

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

### Architecture Rules

- No `print()` or `logging` in `agentteam/` — library code only
- Python 3.11+ syntax
- `asyncio_mode = "auto"` in pytest — no `@pytest.mark.asyncio` needed
- Line length: 100 (ruff)

### File Touch List

| File | Action |
|---|---|
| `agentteam/prompts/templates/output.j2` | **CREATE** — Jinja2 template for output/voice/anti-slop layer |
| `agentteam/prompts/output.py` | **CREATE** — `build_output_layer()` + moved/extracted helpers |
| `agentteam/prompts/builder.py` | **MODIFY** — remove extracted code, call `build_output_layer()` |
| `agentteam/prompts/__init__.py` | **MODIFY** — export `build_output_layer` |
| `tests/test_output.py` | **CREATE** — output layer tests |

### References

- [Source: `agentteam/prompts/builder.py`] — current inline implementation to extract from (Voice lines 43-52, Output lines 54-97, AntiSlop lines 8-35 + 99-101)
- [Source: `agentteam/prompts/identity.py`] — lazy Jinja2 env pattern, `build_identity_layer()` structure to mirror
- [Source: `agentteam/prompts/templates/identity.j2`] — template style/conventions to follow
- [Source: `agentteam/prompts/__init__.py`] — current exports to extend
- [Source: `tests/conftest.py`] — `minimal_agent`, `rich_agent` fixtures
- [Source: `tests/test_prompts_builder.py`] — 20 existing tests that must stay green
- [Source: `agentteam/types/agent.py`] — `VoiceConfig`, `OutputConfig`, `AntiSlopConfig`, `Brevity`, `OperatingLevel`, `JobType` definitions

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- No failures. All 29 new tests passed on first run. Full suite 355/355 green immediately.

### Completion Notes List

- Created `agentteam/prompts/templates/output.j2` — Jinja2 template rendering Voice section (tone, optional vocabulary_hints, optional anti_patterns list), Output section (level_desc, job_desc, brevity_desc — pre-resolved in Python), and conditional Anti-Slop Rules section; `trim_blocks`+`lstrip_blocks` suppress control-tag whitespace
- Created `agentteam/prompts/output.py` with `build_output_layer()`, `_build_antislop_section()` (moved verbatim from builder.py), `_level_desc()`, `_job_desc()`, `_brevity_desc()` helpers, and module-level lazy Jinja2 env via `FileSystemLoader`; `vocabulary_hints_str` pre-computed in Python to preserve `repr()` single-quote style
- Updated `builder.py`: removed `_build_antislop_section()` and inline Voice/Output/AntiSlop sections; replaced with single `build_output_layer(agent)` call; `## Remember` section and all other functions unchanged
- Updated `prompts/__init__.py` to export `build_output_layer`
- 29 new tests in `test_output.py`: all 5 brevity/level/job combos, anti-pattern presence/absence, all 5 anti-slop rules, Jinja2 rendering quality (no tags, idempotent, template exists)
- 355/355 full suite passing — all existing `test_prompts_builder.py` tests pass (public API of `build_system_prompt()` unchanged)

### Review Findings

- [x] [Review][Patch] Add boundary tests for `uncomfortable_idea_quota` at values 1 and 5 — threshold-slip in `max(5, 10 - quota)` formula would go undetected [tests/test_output.py]
- [x] [Review][Defer] `_jinja_env` module global uses no lock — same lazy-init pattern as identity.py; CPython GIL prevents corruption; pre-existing design choice
- [x] [Review][Defer] Jinja2 autoescape disabled — template injection via config fields possible but pre-existing pattern identical to identity.py; sandboxed env deferred
- [x] [Review][Defer] Template path resolved via `__file__` — fails in zip-imported packages; pre-existing pattern from identity.py
- [x] [Review][Defer] Empty `tone` string produces malformed `Tone: ` line — no guard in template; VoiceConfig default is "professional"; no agent YAML triggers this
- [x] [Review][Defer] Anti-pattern value containing `"` corrupts double-quoted bullet — no existing agent YAML triggers this; address in agent YAML authoring guidelines
- [x] [Review][Defer] Multi-line anti-pattern string corrupts bullet list — same class as Story 3.3 multi-line field defer; address in E4 context assembly
- [x] [Review][Defer] `_job_desc`/`_level_desc` silent fallback for missing enum entries — intentional safety valve; new enum values require both dict + fallback update; acceptable design
- [x] [Review][Defer] `vocabulary_hints` with empty-string items passes through unguarded — degenerate input; agent schema provides no validation; address when vocab_hints become configurable
- [x] [Review][Defer] `uncomfortable_idea_quota` implements turn cadence not a count — naming mismatch is pre-existing from builder.py; address in Epic 7 action system work

### File List

- _SYSTEM/agentteam/prompts/templates/output.j2 (new)
- _SYSTEM/agentteam/prompts/output.py (new)
- _SYSTEM/agentteam/prompts/builder.py (modified)
- _SYSTEM/agentteam/prompts/__init__.py (modified)
- _SYSTEM/tests/test_output.py (new)
