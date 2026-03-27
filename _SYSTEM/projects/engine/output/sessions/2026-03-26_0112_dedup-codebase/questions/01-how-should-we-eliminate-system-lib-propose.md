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


<!-- complete -->
