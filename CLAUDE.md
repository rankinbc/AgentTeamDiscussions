# AgentTeamDiscussions

Multi-agent AI orchestration platform. Two AI teams communicate through an MCP message broker, deliberating internally and producing specs/PRDs overnight.

**Last Updated:** 2026-03-26

---

## Hard Rules

**NEVER** modify `_bmad/` — external tooling updated via BMAD upgrades only.

**NEVER** edit files in `output/` — write-only runtime artifacts (sessions, design-docs, panel-runs).

**NEVER** move or rename protected files (`CLAUDE.md`, `.gitignore`, `pyproject.toml`, `.env.*`) without explicit permission.

**DO NOT** reorganize files during normal work. Only when explicitly asked.

---

## Data vs Session Output Rule

- **User-configured, reusable data** (briefs, agent YAML, team YAML) → `_SYSTEM/data/`
- **Runtime session output** (transcripts, Morning Briefs, design docs, panel runs) → `output/`

## Project Map

```
_SYSTEM/                  → All active code, docs, config, data (see _SYSTEM/CLAUDE.md)
  agentteam/              → Installable Python library (see _SYSTEM/agentteam/CLAUDE.md)
  projects/engine/        → Primary discussion app (see _SYSTEM/projects/engine/CLAUDE.md)
  data/                   → Agent/team YAML + reusable briefs (see _SYSTEM/data/CLAUDE.md)
_bmad/                    → BMAD framework — do not modify
_bmad-output/             → BMAD planning artifacts — reference only
design-artifacts/         → WDS design pipeline output (A–G) — reference only
output/                   → All runtime output — write-only
  sessions/               → Full session runs (Morning Brief, transcripts, ledger)
  design-docs/            → Design docs from --no-session runs
  panel-runs/             → Brainstorm panel analysis output
temp/                     → Scratch — not committed, delete freely
```

---

## Zone Routing

| Working on... | Read... |
|---|---|
| agentteam package, types, prompts, runner, session I/O | `_SYSTEM/agentteam/CLAUDE.md` |
| Discussion engine, session runner, evaluation, live chat | `_SYSTEM/projects/engine/CLAUDE.md` |
| Agent personas, team definitions, briefs (YAML/MD) | `_SYSTEM/data/CLAUDE.md` |
| Anything in `_SYSTEM/` | `_SYSTEM/CLAUDE.md` |

---

## Reference

Read `design-artifacts/` for WDS design pipeline context — committed reference, do not regenerate.
