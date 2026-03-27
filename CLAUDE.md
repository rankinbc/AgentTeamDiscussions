# AgentTeamDiscussions

Multi-agent AI orchestration platform. AI agent teams discuss open questions through structured rounds, producing design documents and executive summaries.

**Last Updated:** 2026-03-26

---

## Hard Rules

**NEVER** modify `_bmad/` — external tooling updated via BMAD upgrades only.

**NEVER** edit files in `_SYSTEM/projects/engine/output/` — write-only runtime artifacts.

**DO NOT** reorganize files during normal work. Only when explicitly asked.

---

## Project Map

```
_SYSTEM/
  projects/engine/          → C# .NET 8 discussion engine (see _SYSTEM/projects/engine/CLAUDE.md)
    src/EngineStandalone/   → Main application
    ui/                     → React + Vite live dashboard
    config/                 → YAML configuration (defaults, display, overlays)
    data/                   → Agent/team YAML definitions (local copy)
    templates/              → Prompt templates (Scriban/Jinja2)
    input/                  → Briefs — input to engine, also output destination for generated briefs
    output/                 → ALL runtime session output (sessions, design-docs)
  data/                     → Shared data (agent YAML, team YAML) [AUTHORITATIVE]
docs/                       → ALL project documentation
  v1/                       → V1 specs: PRD, product brief, system overviews, engine specs
  v2/                       → V2 roadmap and deferred ideas
  concepts/                 → Design principles, agent panel explorations
  research/                 → Applied research, multi-agent best practices
  references/               → Architecture docs, guides, data models
  archive/                  → Superseded docs
PRPs/                       → Product Requirements Prompts (active feature work)
.planning/                  → Implementation artifacts, codebase snapshots
_bmad/                      → BMAD framework — do not modify
_bmad-output/               → BMAD planning artifacts — frozen read-only reference
design-artifacts/           → WDS design pipeline output — reference only
```

---

## Zone Routing

| Working on... | Read... |
|---|---|
| Discussion engine, sessions, agents, evaluation | `_SYSTEM/projects/engine/CLAUDE.md` |
| Agent personas, team definitions, briefs | `_SYSTEM/data/CLAUDE.md` |
| Product specs, PRD, system design | `docs/v1/` + `docs/index.md` |
| V2 planning, deferred features | `docs/v2/ROADMAP.md` |
| Research foundations | `docs/research/` |
| Implementation sprint artifacts | `.planning/implementation-artifacts/` |

---

## Tech Stack

- **Engine:** C# .NET 8 (ASP.NET Web SDK)
- **UI:** React 19 + TypeScript + Vite + Tailwind CSS
- **LLM:** Claude CLI (`claude -p` subprocess calls)
- **Config:** YAML (YamlDotNet) + Scriban templates
- **Tests:** xUnit

## Project Awareness & Context

- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn't listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Leverage examples extensively** — study existing patterns before creating new ones.

## Research Methodology

- **Web search first** — always do extensive web research before implementation.
- **Documentation deep dive** — study official docs, best practices, and common patterns.
- **Codebase exploration** — trace data flow through existing features before adding new ones.
- **Gotcha documentation** — document common pitfalls and edge cases in the PRP.

## Task Completion

- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a "Discovered During Work" section.

## PRP Workflow

Use the PRP (Product Requirements Prompt) process for non-trivial features:

1. Fill out `INITIAL.md` with your feature request (be detailed — the more context, the better the PRP)
2. Run `/generate-prp INITIAL.md` to research and create a comprehensive PRP
3. **Review and refine the PRP** — you are part of the process to ensure quality
4. Run `/execute-prp PRPs/{feature-name}.md` to implement

PRP templates are in `PRPs/templates/`. Add reference docs to `PRPs/ai_docs/`.

## Code Structure & Modularity

- **Never create a file longer than 500 lines.** If a file approaches this limit, refactor by splitting into modules.
- **Organize code into clearly separated modules** grouped by feature or responsibility.
- **Follow existing DI patterns** in Program.cs for new services.
- **Follow established coding standards** and conventions (see PLANNING.md).

## Implementation Standards

- **Follow the PRP workflow** — don't skip steps.
- **Always validate before proceeding** to the next step.
- **Use existing patterns as templates** rather than creating from scratch.
- **Include comprehensive error handling** in all implementations.
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** — only use known, verified packages.

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
