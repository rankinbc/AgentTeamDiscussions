# PLANNING

## Architecture Overview

AgentTeamDiscussions is a multi-agent AI orchestration platform where agent teams discuss open questions through structured rounds, producing design documents and executive summaries.

### Zones

| Zone | Path | Purpose |
|------|------|---------|
| Engine | `_SYSTEM/projects/engine/` | C# .NET 8 discussion engine — orchestration, sessions, rounds, synthesis, evaluation |
| UI | `_SYSTEM/projects/engine/ui/` | React 19 + Vite live dashboard with SSE streaming |
| Data | `_SYSTEM/data/` | Authoritative agent YAML and team YAML |
| Briefs | `_SYSTEM/projects/engine/input/` | Brief files — input to engine AND output destination for generated briefs |
| Config | `_SYSTEM/projects/engine/config/` | YAML-driven runtime settings (timeouts, display, overlays, modes) |
| Templates | `_SYSTEM/projects/engine/templates/` | Scriban prompt templates for LLM calls |
| Docs | `docs/` | All project documentation (v1 specs, v2 ideas, concepts, research, references) |
| Planning | `.planning/` | Implementation artifacts, codebase snapshots |
| Output | `_SYSTEM/projects/engine/output/` | Write-only runtime session artifacts |

### Data Flow

1. User creates a **brief** (markdown with open questions) or starts an interactive session
2. **SessionPreparer** builds the session config (team, agents, mode, questions)
3. **SessionRunner** orchestrates the question lifecycle with crash-safe persistence
4. **DiscussionEngine** runs rounds (propose -> critique -> evaluate) per the mode definition
5. **RoundRunner** executes agents sequentially with speaking-order scoring
6. **ClaudeRunner** shells out to `claude -p` for each agent turn
7. Synthesis merges round outputs into design docs; **MorningBriefGenerator** produces executive summary
8. Optional **Evaluator** runs post-session LLM scoring
9. **LiveServer** (ASP.NET SSE) streams events to the React dashboard in real-time

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Engine | C# .NET 8, ASP.NET Web SDK |
| UI | React 19, TypeScript, Vite 8, Tailwind CSS 4 |
| LLM | Claude CLI (`claude -p` subprocess) |
| Config | YAML (YamlDotNet), Scriban templates |
| Tests | xUnit (78 tests: agent loading, brief parsing, config, sessions, persistence) |
| CLI | System.CommandLine 2.0.0-beta4 |

## Style & Conventions

### C# Engine
- PascalCase for classes, methods, properties
- camelCase for local variables and parameters
- Interfaces prefixed with `I` (e.g., `IClaudeRunner`, `IConfigLoader`)
- One class per file, file named after the class
- Enums in `Types/Enums.cs`
- Abstractions (interfaces) in `Abstractions/`
- DI wired in `Program.cs`

### YAML Data
- Agent files: `{team}__{agent_key}.yaml` (double underscore delimiter)
- Team files: `{team_name}.yaml`
- All keys use `snake_case`
- Agent top-level keys: `personality`, `position`, `technique`, `anti_slop`, `voice`, `output`

### React UI
- TypeScript strict mode
- Functional components with hooks
- Tailwind CSS for styling
- Vite for bundling

## Current Goals / Roadmap

<!-- Fill in your current goals and priorities here -->

- [ ] _Example: Add new discussion mode for brainstorming_
- [ ] _Example: Improve evaluation scoring rubric_

## Constraints

- **NEVER** modify `_bmad/` — external tooling only
- **NEVER** edit files in `output/` — write-only runtime artifacts
- **DO NOT** modify agent YAML during a session (loaded at start, cached)
- **DO NOT** delete `<!-- complete -->` markers (crash recovery mechanism)
- **DO NOT** reorganize files during normal work
- Use `config/defaults.yaml` for config changes, not C# code
- Use `data/teams/*.yaml` to add modes (team-level concern)
- Agent/team YAML authoritative source is `_SYSTEM/data/`, not `projects/engine/data/`
- All documentation lives in root `docs/`, NOT `_SYSTEM/docs/`
- `_bmad-output/` is frozen after cleanup — read-only historical reference
