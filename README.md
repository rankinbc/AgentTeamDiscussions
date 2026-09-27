# AgentTeamDiscussions

A multi-agent orchestration engine where a team of AI agents — each with its own personality, position, and technique — works through an open design question in structured rounds and produces a design document and an executive summary at the end.

Give it a brief with a few open questions, pick a team, and watch the agents propose, critique, and evaluate each other's ideas live in a browser dashboard.

## How it works

1. You write a **brief** — a markdown file with the questions you want answered — or start a session interactively from the CLI.
2. The engine loads a **team** (YAML) and its **agents** (one YAML file each, defining personality, position, technique, voice, and anti-slop rules).
3. For each question, the **DiscussionEngine** runs the team's mode — by default *propose → critique → evaluate* — with agents speaking in a scored order.
4. Each agent turn is a separate `claude -p` subprocess; the engine owns the prompts (Scriban templates), the context budget, and the compression of prior rounds.
5. Round outputs are **synthesized** into a design document, and a **MorningBriefGenerator** writes the executive summary. An optional **Evaluator** scores the session afterwards.
6. A **LiveServer** (ASP.NET, Server-Sent Events) streams every event to a React dashboard while the session runs.

Sessions persist to disk after every step and can be resumed after a crash with `--resume`.

## Stack

| Layer | Technology |
|---|---|
| Engine | C# / .NET 8, System.CommandLine, YamlDotNet, Scriban |
| Live dashboard | React 19, TypeScript, Vite, Tailwind CSS 4, SSE |
| LLM | Claude CLI (`claude -p`) |
| Tests | xUnit — agent loading, brief parsing, config, prompt building, context budgeting, compression, persistence |

## Quick start

Prerequisites: .NET 8 SDK, and the `claude` CLI installed and authenticated.

```bash
cd _SYSTEM/projects/engine
dotnet build

# Interactive: prompts for topic, team, agents, mode
dotnet run --project src/EngineStandalone -- new

# Non-interactive, with the live dashboard
dotnet run --project src/EngineStandalone -- new \
  --topic "How should we handle errors?" \
  --team beta-agents \
  --agents cognitive_architect,adversarial_critic \
  --live

# Run from a brief file
dotnet run --project src/EngineStandalone -- input/my-brief.md

# Resume an interrupted session
dotnet run --project src/EngineStandalone -- --resume 2026-03-26_1430_my-brief

# See available teams and their modes
dotnet run --project src/EngineStandalone -- list-teams
```

Session output (transcripts, design docs, summaries) lands in `_SYSTEM/projects/engine/output/`.

## Repository layout

```
_SYSTEM/
  projects/engine/     C# engine, React UI, config, prompt templates, briefs, output
  data/                Agent and team YAML (authoritative)
docs/                  Specs, roadmap, design concepts, research notes
PRPs/                  Active feature work (Product Requirements Prompts)
```

Full zone map and conventions: [PLANNING.md](PLANNING.md). Engine internals and CLI flags: [`_SYSTEM/projects/engine/CLAUDE.md`](_SYSTEM/projects/engine/CLAUDE.md).

## Defining a team

Teams live in `_SYSTEM/data/teams/<team>.yaml` and list their agents; each agent is `_SYSTEM/data/discussionAgents/<team>__<agent_key>.yaml` with `personality`, `position`, `technique`, `anti_slop`, `voice`, and `output` sections. Discussion modes (round structure and assignments) are defined at the team level, so adding a new mode is a YAML change, not a code change.

## Roadmap

Blind proposals (agents propose without seeing each other first), a phase system (brainstorm → refine → specify → review), anti-sycophancy drift measurement, and additional artifact types (PRD, architecture doc, user stories). Details in [`docs/v2/ROADMAP.md`](docs/v2/ROADMAP.md).
