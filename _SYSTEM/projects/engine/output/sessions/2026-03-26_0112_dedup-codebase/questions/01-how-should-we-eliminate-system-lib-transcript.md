# Transcript: How should we eliminate `_SYSTEM/lib/`?

*Generated: 2026-03-26 01:14*

## Round: PROPOSE

### The Flow Orchestrator (mechanical flow designer)

## Deletion Sequence — First-Pass Agenda

Before we debate one-pass vs. incremental, we need ground truth. Here is the required sequence:

**Phase 1: Import Graph (blocking prerequisite)**
Run a full grep across the entire repo — not just `_SYSTEM/` — for any `from lib.` or `import lib.` or relative imports resolving through `lib/`. This produces a definitive hit list. No deletion happens until this list exists and is reviewed. This is not optional.

**Phase 2: Gap Analysis (second blocking gate)**
The CLAUDE.md note is precise: `lib/speak_to_agent.py` and `lib/prompt_builder.py` are flagged as "last real implementations" — migration targets, not confirmed duplicates. That language means `agentteam/` may not yet have absorbed their full surface area. Before we touch anything, someone must diff these two files against their `agentteam/` counterparts and confirm parity. I want a binary answer: is every callable present and behaviorally equivalent?

**Phase 3: Deletion Order (only after Phases 1–2 clear)**
If Phase 1 returns zero hits and Phase 2 confirms parity, one-pass deletion is fine. If Phase 1 returns hits, each callsite must be re-pointed before the corresponding `lib/` module is removed — module by module, not file by file, following dependency order (types → config → runner → speak → prompt).

**Decision Point I'm Flagging Now:**
Nobody has stated whether `prompt_definitions.json` has a counterpart in `agentteam/`. That is a data file, not a Python module. It may not be covered by the import scan. Explicitly confirm its destination before assuming lib/ deletion is clean.

That is the sequence. What does the import scan show?

### The Cognitive Architect (creativity engine designer)

## Building on Flow Orchestrator's Sequence — Two Additions

The phased approach is correct. I want to add two things that aren't covered.

**The import scan has a blind spot: `isinstance` checks.**

If any code does `isinstance(x, lib.types.SomeClass)` and `agentteam/` defines a *different* class object with the same name, the import scan returns zero hits but runtime blows up silently. Type identity in Python is by object, not by name. The `types/` subdirectory in `lib/` makes this non-hypothetical. The gap analysis in Phase 2 needs to include type hierarchy checks, not just callable surface area.

**The "migration target" language is evidence of incomplete work, not a status update.**

CLAUDE.md doesn't say "these are the last files *being* migrated" — it says "migration targets." That's a TODO. The behavioral delta between `lib/speak_to_agent.py` and its `agentteam/` counterpart may be real and tested-against in production sessions. Before diffing for parity, I'd run the existing test suite (`python -m pytest` from `_SYSTEM/`) with imports temporarily re-pointed to `agentteam/` equivalents and watch for failures. Test failures are faster than manual diff review.

**On `prompt_definitions.json`:** Flow Orchestrator is right to flag it separately. The `conversation_engine/` and `orchestrator/` subdirectories may also contain non-Python assets. Glob for `*.json`, `*.yaml`, `*.md`, `*.j2` inside `lib/` before declaring the import scan sufficient.

Phase sequence stands. Scope the gap analysis wider than Python callables.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## The Deletion Problem Is Simpler Than This Discussion Makes It Look

Stop. We're building a migration strategy for what should be a search-and-delete operation.

**The actual question:** Does anything in the running codebase import from `lib/` that `agentteam/` doesn't satisfy? That's it.

**Do this first, before any strategy:**

```bash
grep -r "from lib\." _SYSTEM/ --include="*.py" | grep -v "_SYSTEM/lib/"
grep -r "import lib\." _SYSTEM/ --include="*.py" | grep -v "_SYSTEM/lib/"
```

If that returns zero hits outside `lib/` itself, the migration is already done. Delete `lib/`. Done. No phases needed.

If it returns hits, you have a concrete list of broken imports. Fix them one file at a time. Then delete.

**On the `isinstance` concern:** Valid, but only matters if `lib/types/` exports classes that external code instantiates *and* checks. Run the grep first — if nothing imports from `lib/types/` externally, the concern is moot.

**On `prompt_definitions.json`:** Check whether anything outside `lib/` references it by path. One grep. Either it's referenced or it isn't.

**The "module by module" framing is complexity theater.** There's no safety benefit to incremental deletion if the test suite covers the behavior. Run `python -m pytest` after the grep confirms zero external imports, then delete the whole directory in one commit. Rollback is `git revert`.

The failure mode I'm flagging: we spend three hours designing a careful phased approach for a change that takes fifteen minutes if we look at the actual import graph first.

### The Adversarial Critic (adversarial reviewer)

## The Grep-and-Delete Plan Has Three Silent Failure Modes

Systems Pragmatist is right that the grep is the first move. That part is not controversial. But "zero grep hits means safe to delete" contains assumptions worth stress-testing before someone runs `git rm -rf`.

**Failure mode 1: Dynamic imports.** `importlib.import_module("lib.speak_to_agent")` or string-constructed module paths won't appear in a static grep. If any agent YAML, config file, or template references a module path as a string, the grep returns clean and runtime explodes. Check `*.yaml`, `*.json`, `*.j2`, `*.md` for the string `"lib."` — not just Python files.

**Failure mode 2: The test suite may be testing `lib/` directly.** If `_SYSTEM/tests/` imports from `lib/` to test the shims, the grep-then-delete sequence destroys the tests alongside the shims. The tests passing *after* deletion proves nothing if they were testing the thing you deleted.

**Failure mode 3: `prompt_definitions.json` is not Python.** The grep flags Python imports. It will not catch `open("lib/prompt_definitions.json")` or a hardcoded relative path. One path-based reference in `config_loader.py` or a template and the "safe" deletion breaks quietly at runtime, not at import time.

Cognitive Architect's `isinstance` point is valid but secondary — it only bites if external code touches `lib/types/` objects. The grep will show that.

The actual gap in both proposals: neither specifies what "the test suite covers the behavior" means for a project where sessions are the primary output. Unit tests may be thin here.

## Round: EVALUATE

### The Product Oracle (user advocate)

## What the User Cares About: None of This

Let me reframe before we go deeper into deletion choreography.

The user's job is: *wake up to a Morning Brief that made good decisions overnight*. `lib/` is invisible to that job. Which means the deletion risk isn't "do we get the migration right" — it's "do we accidentally break the session runner at 2am when no one is watching."

That reframe has a concrete implication: **the test question the Adversarial Critic raised is the only one that matters for user impact.** Not the import graph elegance. Not module-by-module sequencing. Does the session runner still produce a Morning Brief after deletion? That's the acceptance criterion.

So here's the agenda I'd set:

**One gate, not three phases:** Run the grep. If zero external hits, run a full session end-to-end — even a short one — against `agentteam/` imports. If the session completes and the Morning Brief writes, delete `lib/` in one commit. The Brief is the smoke test.

**The dynamic import concern is real but scoped.** Check `*.yaml`, `*.j2`, `*.json` for string `"lib."` — thirty seconds, not a phase. Either it's there or it isn't.

**`prompt_definitions.json` is the only wildcard I'd protect.** Don't delete it until you've traced exactly where it's loaded. One bad path reference breaks prompt generation silently — the Brief still writes, but it's hollow. That failure mode is invisible until someone reads it.

The phases are process for its own sake. One grep, one session run, one commit.

### The Context Surgeon (context efficiency evaluator)

## The Discussion Has Already Converged — Execute It

Product Oracle's framing is correct, and the Adversarial Critic's three failure modes are real but already handled by the same two-step grep the Pragmatist proposed. We're circling.

The actual checklist, stated once:

```bash
# Step 1: Static + non-Python references (~2 min)
grep -r "lib\." _SYSTEM --include="*.py" --include="*.yaml" \
  --include="*.j2" --include="*.json" --include="*.md"

# Step 2: Dynamic import patterns (~30 sec)
grep -r "import_module\|importlib" _SYSTEM --include="*.py"

# Step 3: Smoke test
python session_runner.py brief.md --no-session
# Verify Morning Brief writes. That's the acceptance criterion.
```

If those return clean: delete `lib/` in one commit. Not module-by-module — that's ceremony that creates intermediate broken states and splits blame across commits.

**One genuine hold:** `prompt_definitions.json`. It's the only artifact without a `.py` import signature. Before deletion, confirm `config_loader.py` in `agentteam/` loads prompts from its own path, not a hardcoded `lib/` relative path. One `grep -r "prompt_definitions" _SYSTEM` resolves this.

**On the test suite concern:** if `_SYSTEM/tests/` is importing from `lib/` to test shims, those tests are testing dead code. They should be deleted with the shims, not preserved. Tests that survive the deletion are the only tests worth having.

The three failure modes are one grep pass. Stop planning the plan.

<!-- complete -->
