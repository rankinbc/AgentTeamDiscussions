# Deduplication: Code and Documentation in AgentTeamDiscussions

## What's Already Decided
- `agentteam/` is the canonical library. All logic lives there.
- `_SYSTEM/lib/` is deprecated — it contains old shims that duplicate `agentteam/`
- Engine root-level `.py` files (ask_panel.py, claude_runner.py, models.py, interact.py, conversation.py, multi_agent.py, evaluate_experiment.py) are backward-compat wrappers — the real code has moved into submodules
- `_SYSTEM/projects/engine/config/teams/` is a stale duplicate of `_SYSTEM/data/teams/`
- New AI-context docs live in `/docs/` (project root); existing design docs live in `_SYSTEM/docs/`

## Open Questions

1. **How should we eliminate `_SYSTEM/lib/`?** It contains: claude_runner.py, config_loader.py, team_loader.py, speak_to_agent.py, prompt_definitions.json, conversation_engine/, orchestrator/, types/. All of this is duplicated by `agentteam/`. What is the safest deletion strategy — check for any remaining imports first, then remove in one pass or module by module? Are there edge cases where `lib/` exports something `agentteam/` does not?

2. **What should happen to the engine's backward-compat wrapper files?** The engine root has ask_panel.py, claude_runner.py, models.py, interact.py, conversation.py, multi_agent.py, evaluate_experiment.py — each is a 1-3 line shim re-exporting from the real submodule. Should these stay indefinitely as import aliases, be deleted once all internal call sites are updated, or be converted into proper `__init__.py` re-exports?

3. **How do we reconcile the three layers of documentation?** The project now has: (a) `_SYSTEM/docs/` — design intent and concepts; (b) `/docs/` (project root) — AI context / codebase reference generated today; (c) `.planning/codebase/` — 7 codebase analysis files (ARCHITECTURE.md, CONCERNS.md, CONVENTIONS.md, INTEGRATIONS.md, STACK.md, STRUCTURE.md, TESTING.md). What is the right ownership boundary for each layer, and which files should be merged, redirected, or deleted?

4. **Should `_SYSTEM/projects/engine/config/teams/` be deleted?** The engine CLAUDE.md says it is a stale duplicate pending removal. The authoritative source is `_SYSTEM/data/teams/`. Is it safe to delete immediately, or are there any code paths that still reference it?

5. **Is `_SYSTEM/projects/engine/conversation/state.py` still needed?** The engine has a `conversation/state.py` that partially overlaps with `agentteam/conversation/state.py`. What is the plan to consolidate — delete the engine copy, redirect it, or keep it for engine-specific state not in the library?
