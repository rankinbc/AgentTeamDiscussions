# TASK

## Active Tasks

| Task | Description | Date Added |
|------|-------------|------------|

## Completed Tasks

| Task | Description | Date Completed |
|------|-------------|----------------|
| Step 1: persona team vs single call | Blind pre-mortem comparison on the 5 V2 roadmap questions (single Opus call vs 3 Sonnet persona critics + synthesizer, 10 blind LLM judgments). Team did not clear the ≥3/5 bar: 1 win, 2 losses, 2 splits; judges favored their own model. Findings and blind pairs in `docs/research/premortem-eval-2026-10-05/`. | 2026-10-05 |
| Claude Code plugin prototype | Added `_SYSTEM/projects/plugin/` (`agent-discuss`): persona YAML → 33 generated subagents, Python step engine (init/next/save/resume) that ports brief parsing, prompt assembly, cascade rules, ledger and session persistence; `/agent-discuss:discuss` and `/agent-discuss:list-teams` skills; unit tests + dry run. Output uses the engine's session layout. See plugin README for gaps (no context-budget enforcer, no SSE, no eval). | 2026-10-05 |
| Context engineering setup | Added PLANNING.md, TASK.md, PRP workflow (template-generator pattern), INITIAL.md, generate-prp/execute-prp commands | 2026-03-26 |
| Docs reorganization | Consolidated all docs into root `docs/` with v1/v2/concepts/research/references/archive structure. Moved 76 files from `_SYSTEM/docs/`, 14 impl artifacts to `.planning/`, 2 feature specs to `PRPs/`. Deleted 21 duplicates from `_bmad-output/`. Created `docs/index.md`, `docs/v2/ROADMAP.md`. Fixed broken links in system-overview index and agent-panel index. Updated CLAUDE.md and PLANNING.md. | 2026-03-26 |

## Discovered During Work

- `docs/v1/system-overview-docs/index.md` had broken links (missing `-overview` suffix) — fixed during reorg
- `docs/concepts/conversation-engine/agent-panel-index.md` transcript links were broken (missing `transcripts/` prefix) — fixed during reorg
- `docs/references/index.md` referenced Python-era commands (pip, pytest, python) — updated to C#/.NET commands
- Question 09 in agent panel has no design doc, only a transcript — pre-existing gap, not caused by reorg
- Engine bugs found while porting to the plugin — all fixed 2026-10-05: `SessionRunner` appended the ledger to "What's Already Decided" twice; `SessionPersistence.CountCompletedQuestions` counted round files and `eval-*.md` as completed questions, so resume over-skipped (now counts the leading run of finished design docs from the question list); the synthesis template's `{{ question_number }}` / `{{ topic_tag }}` / `{{ max_ledger_words }}` reached the model literally, so no run ever produced a usable `## Ledger` section (now filled per question in `DiscussionEngine.FillSynthesisTemplate`); `AgentLoader.ParsePositionConfig` never read `allergies`; `SessionPreparer` read modes from `_SYSTEM/data/teams/` (which had none for beta-agents/ev18hornet) while `SessionRunner` read the engine-local copy (modes added to the shared YAMLs, both now resolve through `IAgentLoader.ResolveTeamPath`).
- `_SYSTEM/projects/engine/data/` is a diverged, now-unused copy of `_SYSTEM/data/` (older `agents/` with `allergies` and belief-style roles; `teams/` with modes). Left in place per the "do not reorganize" rule; candidate for deletion.

- V2 roadmap pre-mortem (both arms agree, see `docs/research/premortem-eval-2026-10-05/README.md`): V2 specs target a Python/live-conversation engine that no longer exists; no measurement baseline exists for any critical-path step; phase exit gates are not computable; round-boundary compression drops research findings and moderator directives; "blind proposals" may already be mostly true of the current engine.

## Backlog

<!-- Future ideas and low-priority items -->
