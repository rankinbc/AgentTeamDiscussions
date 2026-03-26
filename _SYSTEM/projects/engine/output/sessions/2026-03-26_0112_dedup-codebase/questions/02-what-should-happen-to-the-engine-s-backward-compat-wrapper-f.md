# What should happen to the engine's backward-compat wrapper files?

*Generated: 2026-03-26 01:17 | Question 2 | 142s | Mode: default*

## Decisions

**The `__init__.py` re-export option is rejected.** Converting shims to `__init__.py` re-exports defers the deletion decision indefinitely, creates a new ambiguous namespace that competes with the real submodules, and is invisible to any future Gate 1 grep pass. There is no terminal state for this path. It is not a valid resolution option at any point in this work.

**The four unconfirmed files must be read before any deletion sequence is designed.** The prior decisions explicitly name `ask_panel.py`, `claude_runner.py`, and `models.py` as backward-compat wrappers. The status of `interact.py`, `conversation.py`, `multi_agent.py`, and `evaluate_experiment.py` is unverified. The working definition of "1-3 line shim" is asserted, not confirmed. A shim that has accumulated unmigrated logic is not a shim — it is a migration target. Classification precedes sequencing.

**For each of the seven files, the classification determines the path:**
- Confirmed shim (re-exports only, no logic of its own): enters the deletion list.
- Contains unmigrated logic: migration to the canonical submodule completes first, then the file enters the deletion list. This migration work is separate from and prior to deletion.

**The caller scan runs after classification, not before.** Once all seven files are confirmed or resolved, run a single grep covering Python, YAML, Jinja2 templates, and JSON across the full project scope — not scoped to `_SYSTEM` alone:

```
grep -r "ask_panel\|claude_runner\|models\|interact\|conversation\|multi_agent\|evaluate_experiment" \
  . --include="*.py" --include="*.yaml" --include="*.j2" --include="*.json"
```

Exclude hits within `_SYSTEM/projects/engine/` itself. What remains is the external caller set.

**If zero external callers:** delete all confirmed shims in one commit alongside any internal call site updates. No intermediate state.

**If external callers exist:** re-point each external call site to the canonical submodule path, then delete the shims, in the same commit. Do not delete before re-pointing. Do not re-point and delete in separate commits — splitting the change makes bisection of any regression harder without adding safety.

**The acceptance criterion is unchanged from the prior design doc.** A completed session where the Morning Brief writes and is non-empty is the sole behavioral gate. Import graph cleanliness is a means to that end. This cleanup does not proceed ahead of any work that directly affects the Morning Brief pipeline.

**"External caller" is defined as:** any call site outside `_SYSTEM/projects/engine/`. This includes test files in `_SYSTEM/tests/`, scripts in `temp/`, any file in `agentteam/`, and any tooling or config outside the engine directory. Test files that import from these shims are testing dead code; they are deleted alongside the shims they test.

**Scope boundary:** this work covers only the seven engine root-level wrapper files. `_SYSTEM/lib/` deletion, `config/teams/` cleanup, and any reorganization outside the engine root remain governed by their own prior decisions and are not bundled with this change.
<!-- complete -->
