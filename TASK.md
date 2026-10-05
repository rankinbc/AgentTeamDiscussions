# TASK

## Active Tasks

| Task | Description | Date Added |
|------|-------------|------------|
| Run engine benchmark | Run `_SYSTEM/projects/benchmark` on the four complete sessions (32 questions): generate baselines, judge, blind-rate, publish results.md and update README Status with the outcome | 2026-10-05 |

## Completed Tasks

| Task | Description | Date Completed |
|------|-------------|----------------|
| Benchmark harness | Python harness (LangChain + LangGraph) comparing engine design docs blind against single-call, self-critique and no-persona panel baselines; pairwise judge in both orders, sign test, blind A/B packet for human ratings. Offline tests with fake models. | 2026-10-05 |
| Context engineering setup | Added PLANNING.md, TASK.md, PRP workflow (template-generator pattern), INITIAL.md, generate-prp/execute-prp commands | 2026-03-26 |
| Docs reorganization | Consolidated all docs into root `docs/` with v1/v2/concepts/research/references/archive structure. Moved 76 files from `_SYSTEM/docs/`, 14 impl artifacts to `.planning/`, 2 feature specs to `PRPs/`. Deleted 21 duplicates from `_bmad-output/`. Created `docs/index.md`, `docs/v2/ROADMAP.md`. Fixed broken links in system-overview index and agent-panel index. Updated CLAUDE.md and PLANNING.md. | 2026-03-26 |

## Discovered During Work

- `docs/v1/system-overview-docs/index.md` had broken links (missing `-overview` suffix) — fixed during reorg
- `docs/concepts/conversation-engine/agent-panel-index.md` transcript links were broken (missing `transcripts/` prefix) — fixed during reorg
- `docs/references/index.md` referenced Python-era commands (pip, pytest, python) — updated to C#/.NET commands
- Question 09 in agent panel has no design doc, only a transcript — pre-existing gap, not caused by reorg

## Backlog

<!-- Future ideas and low-priority items -->
