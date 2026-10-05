# TASK

## Active Tasks

| Task | Description | Date Added |
|------|-------------|------------|

## Completed Tasks

| Task | Description | Date Completed |
|------|-------------|----------------|
| Claude Code plugin prototype | Added `_SYSTEM/projects/plugin/` (`agent-discuss`): persona YAML → 33 generated subagents, Python step engine (init/next/save/resume) that ports brief parsing, prompt assembly, cascade rules, ledger and session persistence; `/agent-discuss:discuss` and `/agent-discuss:list-teams` skills; unit tests + dry run. Output uses the engine's session layout. See plugin README for gaps (no context-budget enforcer, no SSE, no eval). | 2026-10-05 |
| Context engineering setup | Added PLANNING.md, TASK.md, PRP workflow (template-generator pattern), INITIAL.md, generate-prp/execute-prp commands | 2026-03-26 |
| Docs reorganization | Consolidated all docs into root `docs/` with v1/v2/concepts/research/references/archive structure. Moved 76 files from `_SYSTEM/docs/`, 14 impl artifacts to `.planning/`, 2 feature specs to `PRPs/`. Deleted 21 duplicates from `_bmad-output/`. Created `docs/index.md`, `docs/v2/ROADMAP.md`. Fixed broken links in system-overview index and agent-panel index. Updated CLAUDE.md and PLANNING.md. | 2026-03-26 |

## Discovered During Work

- `docs/v1/system-overview-docs/index.md` had broken links (missing `-overview` suffix) — fixed during reorg
- `docs/concepts/conversation-engine/agent-panel-index.md` transcript links were broken (missing `transcripts/` prefix) — fixed during reorg
- `docs/references/index.md` referenced Python-era commands (pip, pytest, python) — updated to C#/.NET commands
- Question 09 in agent panel has no design doc, only a transcript — pre-existing gap, not caused by reorg
- Engine bugs found while porting to the plugin (not fixed in C#): `SessionRunner` appends the ledger to "What's Already Decided" twice; `SessionPersistence.CountCompletedQuestions` counts round files and `eval-*.md` as completed questions, so resume over-skips; prompt templates are loaded with `LoadPromptRaw` and never rendered, so `{{ question_number }}` reaches the model literally and no run has produced a `## Ledger` section; `AgentLoader.ParsePositionConfig` never reads `allergies`; `SessionPreparer` reads modes from `_SYSTEM/data/teams/` (no `modes:` there) while `SessionRunner` reads the engine-local copy.

## Backlog

<!-- Future ideas and low-priority items -->
