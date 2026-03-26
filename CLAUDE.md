# AgentTeamDiscussions

Multi-agent AI orchestration platform. AI agent teams discuss open questions through structured rounds, producing design documents and executive summaries.

**Last Updated:** 2026-03-26

---

## Hard Rules

**NEVER** modify `_bmad/` — external tooling updated via BMAD upgrades only.

**NEVER** edit files in `output/` — write-only runtime artifacts.

**DO NOT** reorganize files during normal work. Only when explicitly asked.

---

## Project Map

```
_SYSTEM/
  projects/engine/          → C# .NET 8 discussion engine (see _SYSTEM/projects/engine/CLAUDE.md)
    src/EngineStandalone/   → Main application
    ui/                     → React + Vite live dashboard
    config/                 → YAML configuration (defaults, display, overlays)
    data/                   → Agent/team YAML definitions
    templates/              → Prompt templates (Scriban/Jinja2)
    input/                  → Place brief files here
    output/                 → Runtime session output
  data/                     → Shared data (agent YAML, team YAML, briefs)
  docs/                     → Design documentation
_bmad/                      → BMAD framework — do not modify
_bmad-output/               → BMAD planning artifacts — reference only
design-artifacts/           → WDS design pipeline output — reference only
output/                     → All runtime output — write-only
```

---

## Zone Routing

| Working on... | Read... |
|---|---|
| Discussion engine, sessions, agents, evaluation | `_SYSTEM/projects/engine/CLAUDE.md` |
| Agent personas, team definitions, briefs | `_SYSTEM/data/CLAUDE.md` |

---

## Tech Stack

- **Engine:** C# .NET 8 (ASP.NET Web SDK)
- **UI:** React 19 + TypeScript + Vite + Tailwind CSS
- **LLM:** Claude CLI (`claude -p` subprocess calls)
- **Config:** YAML (YamlDotNet) + Scriban templates
- **Tests:** xUnit

## Quick Start

```bash
cd _SYSTEM/projects/engine
dotnet build
dotnet run --project src/EngineStandalone -- new
```

With live dashboard:
```bash
# Terminal 1: engine with SSE
dotnet run --project src/EngineStandalone -- new --live

# Terminal 2: UI dev server
cd ui && npm run dev
# Open http://localhost:5173
```
