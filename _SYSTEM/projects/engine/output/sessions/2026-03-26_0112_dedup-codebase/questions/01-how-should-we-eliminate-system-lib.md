# How should we eliminate `_SYSTEM/lib/`?

*Generated: 2026-03-26 01:14 | Question 1 | 152s | Mode: default*

## Decisions

**`agentteam/` is the canonical library.** `_SYSTEM/lib/` is deprecated and will be fully removed. No new imports from `lib/` are permitted at any point before or after deletion.

**Deletion is a single commit, not a phased migration.** Incremental module-by-module removal creates intermediate broken states and splits blame across commits. Once the pre-deletion checklist clears, `lib/` is deleted in one pass.

**The acceptance criterion is a completed session, not a clean import graph.** The Morning Brief writing successfully is the smoke test. Import hygiene is a means to that end, not the goal.

---

## Pre-Deletion Checklist (all gates must clear before deletion)

### Gate 1 — Full Reference Scan

Run a single grep pass covering Python files, config, templates, and data files. This catches both static imports and path-based references in non-Python assets:

```
grep -r "lib\." _SYSTEM --include="*.py" --include="*.yaml" \
  --include="*.j2" --include="*.json" --include="*.md"
```

No hits outside `_SYSTEM/lib/` itself means Gate 1 clears. Any hit is a callsite that must be re-pointed to `agentteam/` before proceeding. There are no exceptions.

### Gate 2 — Dynamic Import Check

Static grep does not catch `importlib.import_module("lib.something")` or string-constructed module paths. Run separately:

```
grep -r "import_module\|importlib" _SYSTEM --include="*.py"
```

Review any hits for references to `lib.*` module paths. These are the only failure mode the reference scan misses.

### Gate 3 — `prompt_definitions.json` Resolution

`prompt_definitions.json` is a data file, not a Python module. It has no import signature and will not appear in Gate 1 or Gate 2. It must be resolved explicitly:

```
grep -r "prompt_definitions" _SYSTEM
```

Confirm that `agentteam/config_loader.py` loads prompt definitions from its own package path and not from a hardcoded `lib/`-relative path. If `agentteam/` has a counterpart file, confirm it is loaded from the correct location. Do not delete `prompt_definitions.json` until this is confirmed.

### Gate 4 — Type Identity Check (conditional)

If Gate 1 returns any external imports from `lib/types/`, a type identity check is required. Python `isinstance` checks resolve by object identity, not by name — a class defined in `lib/types/SomeClass` and a class defined in `agentteam/types/SomeClass` are distinct objects even if structurally identical. Any code that instantiates objects from `lib/types/` and checks their type elsewhere will fail silently at runtime after deletion. If Gate 1 returns zero hits from `lib/types/`, this gate is moot and can be skipped.

### Gate 5 — Smoke Test

Run a short session end-to-end:

```
python session_runner.py brief.md --no-session
```

Verify that the Morning Brief writes and is non-empty. This is the sole behavioral acceptance criterion. Unit tests are not a substitute — they may be testing `lib/` shims directly, in which case they are testing dead code and should be removed with the shims.

---

## Rules for `speak_to_agent.py` and `prompt_builder.py`

CLAUDE.md marks these as "migration targets," not confirmed duplicates. Before Gate 1 is run, do not assume parity with their `agentteam/` counterparts. The Gate 1 scan will reveal whether anything still calls these files. If external callers exist, diff each file's exported callables against the `agentteam/` equivalents and confirm behavioral equivalence. If no external callers exist, the diff is unnecessary — the files are dead and delete with the rest of `lib/`.

---

## Test Suite Handling

If `_SYSTEM/tests/` imports from `lib/` to test shim behavior, those tests are testing code that will be deleted. They are not a reason to delay deletion. Delete them alongside the shims. The only tests worth preserving after this change are tests that import from `agentteam/` and pass against the live library. A test suite that shrinks after `lib/` deletion is a correct outcome.

---

## What Does Not Change

- `agentteam/` package structure is not modified by this work.
- Engine root-level backward-compat wrappers (`ask_panel.py`, `claude_runner.py`, `models.py`, etc.) are out of scope — they are a separate deprecation track.
- `_SYSTEM/projects/engine/config/teams/` stale duplicate is out of scope.
- No reorganization of files outside `lib/` is permitted as part of this change.
<!-- complete -->
