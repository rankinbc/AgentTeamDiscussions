### The Cognitive Architect (creativity engine designer)

The three options collapse into a prior question that isn't asked: **who are the callers?**

Internal callers (code inside `_SYSTEM/projects/engine/`) can be updated in one pass — those shims have no reason to exist once the internal sites are re-pointed. Delete them with the callsite changes as a single commit.

External callers (scripts, notebooks, anything outside the engine directory importing `from ask_panel import X`) are a different matter. If they exist, you can't delete without coordination. But I'd bet most don't — these look like implementation artifacts, not public API surface.

The `__init__.py` re-export path is a trap. It sounds clean but it just moves the confusion: now you have both `engine/__init__.py` and `engine/discussion/engine.py` and `engine/brainstorm/` all competing to be the "real" entry point. You've replaced zombie files with a zombie package namespace.

The cognitive science angle that matters here: **consistency of location signals.** If the rule is "real code lives in submodules," then anything at root level violates that signal and taxes every new contributor's mental model. Vestigial files don't stay neutral — they actively mislead.

**Concrete recommendation:** Gate 1 from the `lib/` deletion protocol applies here too. Run the same grep scoped to these seven filenames across the whole repo. If external call sites are zero, delete them. If call sites exist, schedule a single-commit re-point-and-delete. The `__init__.py` option only makes sense if these files represent a *deliberate public API contract* — which shims never are.

What's the actual caller distribution? That determines everything.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect is right on the core question. But "run Gate 1 scoped to these seven filenames" is a trigger without a sequence. Let me make it concrete.

**The operation sequence is fixed regardless of what Gate 1 returns:**

1. Run grep: `grep -r "ask_panel\|claude_runner\|models\|interact\|conversation\|multi_agent\|evaluate_experiment" _SYSTEM --include="*.py"` — exclude the shim files themselves from results
2. Triage hits into two buckets: inside `_SYSTEM/projects/engine/` vs. outside
3. **If zero external hits:** delete all seven in one commit, no re-pointing required
4. **If external hits exist:** re-point each callsite to the canonical submodule path, then delete shims in the same commit

What I won't accept: the `__init__.py` option as a resolution path. That path has no terminal state. It defers the deletion decision indefinitely and introduces a new ambiguity — does `engine` the package export these names deliberately or accidentally? There's no mechanism to force that question to be answered later. Shims that become `__init__.py` exports stay forever.

The Cognitive Architect flagged "consistency of location signals" — I'll frame that operationally: **every file at the engine root is a decision point that must be evaluated on entry.** Seven ambiguous files means seven branch points in the mental model. That's not neutral overhead, it accumulates.

**Decision point I need answered before sequencing completes:** are `interact.py`, `conversation.py`, and `multi_agent.py` confirmed as shims, or do any contain logic not yet migrated? The prior decisions call out only three files explicitly (`ask_panel.py`, `claude_runner.py`, `models.py`). The other four need explicit status before they enter the deletion sequence.


<!-- complete -->
