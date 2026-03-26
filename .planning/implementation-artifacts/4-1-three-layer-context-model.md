# Story 4.1: Three-Layer Context Model

Status: ready-for-dev

## Story

As a discussion engine developer,
I want a `ContextAssembler` that builds the per-turn user payload from Situation and Task layers with a hard 4,000-token ceiling,
so that agent prompts stay within budget and can be deterministically trimmed when they grow too large.

## Acceptance Criteria

1. `estimate_tokens(text: str) -> int` exists in `agentteam/utils/tokens.py` and uses the formula `int(len(text.split()) * 1.3)`. The constant `TOKEN_CEILING = 4000` is declared in the same file. No other module inlines the formula.

2. `ContextAssembler` class exists in `agentteam/context/assembler.py` with a constructor that accepts `ceiling: int = TOKEN_CEILING` and `cut_order: list[str] | None = None`.

3. `ContextAssembler.assemble(...)` accepts the Situation-layer inputs (history entries, perspective reminder, context lens, prior design doc summary) and the Task-layer directive string. It returns a single `str` that is the assembled user payload.

4. When the assembled payload exceeds `ceiling` tokens, the assembler trims according to `cut_order`, removing sections in order until the payload fits. Default cut order: `["oldest_history", "compressed_history", "prior_spec", "constraint_details"]`.

5. Identity layer (system prompt) is NOT assembled here — it is built by the existing `build_system_prompt()` in `agentteam/prompts/builder.py`. `ContextAssembler` only builds the user-turn payload.

6. `agentteam/utils/__init__.py` exports `estimate_tokens` and `TOKEN_CEILING`.

7. `agentteam/context/__init__.py` exports `ContextAssembler`.

8. Tests in `tests/test_context_assembler.py` cover: token estimation accuracy, assembly under ceiling (no trimming), assembly over ceiling triggers cut in order, custom cut order is respected, empty history assembles without error, Task directive is always present in output (never cut).

## Tasks / Subtasks

- [ ] Create `agentteam/utils/tokens.py` (AC: 1)
  - [ ] Define `TOKEN_CEILING = 4000`
  - [ ] Define `estimate_tokens(text: str) -> int` using `int(len(text.split()) * 1.3)`
  - [ ] Add `__all__ = ["TOKEN_CEILING", "estimate_tokens"]`

- [ ] Update `agentteam/utils/__init__.py` (AC: 6)
  - [ ] Import and re-export `estimate_tokens` and `TOKEN_CEILING` from `.tokens`

- [ ] Create `agentteam/context/` package (AC: 2, 3, 4, 5, 7)
  - [ ] Create `agentteam/context/__init__.py` exporting `ContextAssembler`
  - [ ] Create `agentteam/context/assembler.py` with `ContextAssembler` class
  - [ ] Implement constructor: `ceiling: int = TOKEN_CEILING`, `cut_order: list[str] | None = None`
  - [ ] Implement `assemble(history, perspective_reminder, context_lens, prior_spec, task_directive, constraint_details="")` → `str`
  - [ ] Implement trim loop: measure total, remove sections in cut_order until under ceiling
  - [ ] Protect Task directive from trimming (always included last)

- [ ] Write tests in `tests/test_context_assembler.py` (AC: 8)
  - [ ] `test_estimate_tokens_basic` — known input yields expected count
  - [ ] `test_estimate_tokens_empty` — empty string returns 0
  - [ ] `test_assemble_under_ceiling_no_trim` — small inputs pass through intact
  - [ ] `test_assemble_over_ceiling_trims_oldest_history_first` — oldest history cut first
  - [ ] `test_assemble_custom_cut_order_respected` — custom order overrides default
  - [ ] `test_assemble_empty_history_no_error` — empty history list assembles cleanly
  - [ ] `test_task_directive_always_present` — task directive survives aggressive trim

## Dev Notes

- **Identity layer is out of scope.** `build_system_prompt(agent)` in `agentteam/prompts/builder.py` already handles it. `ContextAssembler` only builds the *user-turn* payload (Situation + Task layers).
- **Do NOT wire `ContextAssembler` into `engine.py` in this story.** Integration into the live discussion runner is Story 4.2+. This story delivers the module and tests only.
- **History windowing** (first-2 + last-10 recency strategy) is Story 4.2. Story 4.1 history input is a plain `list[str]` of turn strings; windowing is the caller's responsibility.
- **`estimate_tokens` must never be inlined.** Architecture mandates every caller import from `agentteam.utils`. [Source: architecture.md — `estimate_tokens` spec]
- The `prior_spec` parameter holds the compressed/summarized output from a prior design-doc run, or empty string. Do not load it from disk here — the caller provides it.
- `constraint_details` is an optional free-text block (e.g. anti-slop rules summary). It is the last item in the default cut order because it is a "nice to have" at context time.
- The protected fields that must never be cut: perspective reminder, context lens, task directive. Removing these breaks agent identity.
- Use `pathlib.Path` and `encoding="utf-8"` for any file I/O — though this module has no file I/O. Rule applies to test fixtures only (use `tmp_path`).
- No `print()` or `logging` in `agentteam/` per hard rule in `agentteam/CLAUDE.md`.

### Project Structure Notes

New files:
```
_SYSTEM/agentteam/utils/tokens.py          ← new
_SYSTEM/agentteam/context/__init__.py      ← new package
_SYSTEM/agentteam/context/assembler.py     ← new
_SYSTEM/tests/test_context_assembler.py    ← new
```

Modified:
```
_SYSTEM/agentteam/utils/__init__.py        ← add exports
```

No changes to `engine.py`, `runner/`, `prompts/`, or `session/`.

### References

- [Source: _bmad-output/planning-artifacts/epics.md — Epic 4, Story 4.1 AC]
- [Source: _bmad-output/planning-artifacts/system-overview-docs/context-management-overview.md — Three-layer model, TOKEN_CEILING, truncation strategy]
- [Source: _bmad-output/planning-artifacts/architecture.md — estimate_tokens formula, file locations, TOKEN_CEILING]
- [Source: _bmad-output/planning-artifacts/conversation-engine/context-assembly-template.md — 7-section assembly order, cut priority, protected fields]
- [Source: _SYSTEM/agentteam/prompts/builder.py — existing build_system_prompt(), build_perspective_reminder(), build_context_lens()]
- [Source: _SYSTEM/agentteam/utils/io.py — utility module pattern to follow]
- [Source: _SYSTEM/agentteam/CLAUDE.md — hard rules: no print/logging, test file naming convention]

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List
