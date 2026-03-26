# EngineStandalone

C# .NET 8 multi-agent discussion engine. Agents discuss questions in structured rounds (propose, critique, evaluate), then a synthesis step merges responses into design docs. Sessions persist to disk with crash recovery.

## Running the Engine

Prerequisites: .NET 8 SDK, `claude` CLI on PATH and authenticated.

```bash
cd _SYSTEM/projects/engine_standalone
dotnet build
```

### Commands

```bash
# Run from a brief markdown file
dotnet run --project src/EngineStandalone -- input/my-brief.md

# Interactive session creation (prompts for topic, team, agents, mode)
dotnet run --project src/EngineStandalone -- new

# Quick session from CLI (non-interactive)
dotnet run --project src/EngineStandalone -- new --topic "Design the auth system"
dotnet run --project src/EngineStandalone -- new --topic "How should we handle errors?" --team beta-agents --agents cognitive_architect,adversarial_critic

# Resume a crashed/interrupted session
dotnet run --project src/EngineStandalone -- --resume 2026-03-26_1430_my-brief

# With live SSE dashboard
dotnet run --project src/EngineStandalone -- new --topic "Auth design" --live

# Evaluate experiment output
dotnet run --project src/EngineStandalone -- eval output/sessions/2026-03-26_my-session/questions

# List teams and their available modes
dotnet run --project src/EngineStandalone -- list-teams
```

### CLI Flags

| Command | Flag | Description |
|---------|------|-------------|
| root | `<brief>` | Brief markdown file (auto-discovers from `input/` if omitted) |
| root | `--resume` `-r` | Resume session by folder name |
| root | `--live` | Start SSE dashboard |
| root | `--eval` `-e` | Run evaluation after session |
| `new` | `--topic` `-t` | Topic to discuss (skip interactive prompt) |
| `new` | `--team` | Team name (skip team selection) |
| `new` | `--agents` | Comma-separated agent keys to include |
| `new` | `--live` | Start SSE dashboard |
| `new` | `--eval` | Run evaluation after session |

All other settings (timeouts, truncation, ports, paths) come from `config/defaults.yaml`.

## Brief File Format

Place in `input/` directory:

```markdown
# Topic Title

Optional intro paragraph.

## What's Already Decided

- Decision 1
- Decision 2

## Open Questions

1. **Question Title** Question body with context.
2. **Another Question** More context here.
```

## Session Output

```
output/sessions/{timestamp}_{slug}/
  session.json              <- unified manifest (config + runtime state)
  session_status.json       <- legacy compat
  decisions_ledger.md       <- append-only decisions
  summary.md                <- Morning Brief
  questions/
    01-{slug}.md            <- design doc
    01-{slug}-transcript.md <- full agent transcript
    01-{slug}-propose.md    <- round responses
    01-{slug}-critique.md
    01-{slug}-evaluate.md
```

## session.json

The session manifest — single source of truth for a session:

```json
{
  "version": 1,
  "title": "Auth System Design",
  "decided": ["Using JWT tokens", "Session duration 24h"],
  "questions": [{"number": 1, "title": "How should tokens work?", "body": "..."}],
  "team": "beta-agents",
  "agents": ["cognitive_architect", "adversarial_critic", "flow_orchestrator"],
  "mode": "compete",
  "timeout": 120,
  "state": { "status": "complete", "session_complete": true, "questions": {...} }
}
```

When `agents` is null, all team agents participate. When set, only listed agents are used and mode round groups are filtered accordingly.

## Teams and Modes

Teams are in `data/teams/*.yaml`. Each team defines its own modes (round structures):

| Team | Agents | Default Mode |
|------|--------|-------------|
| beta-agents | 7 (architect, pragmatist, critic, oracle, orchestrator, surgeon, merchant) | compete |
| ev18hornet | 5 (flight dreamer, emergence theorist, EV purist, player advocate, scope warden) | default |

Modes define which agents go in which round and what behavioral overlays they get. Modes are part of the team YAML, not a separate config. Available modes for beta-agents: default, counter, lean, compete, bigsmall, angles, ideas, ideas_compete.

## Configuration

All in `config/`:

| File | Controls |
|------|----------|
| `defaults.yaml` | Timeouts, truncation limits, health checks, paths, ports |
| `agent_display.yaml` | Display names and colors for agents |
| `role_overlays.yaml` | Behavioral overlays (competitive, minimalist, contrarian, etc.) |

## Architecture

```
Program.cs                  <- CLI entry + DI container
Abstractions/               <- Interfaces (IClaudeRunner, IConfigLoader, IAgentLoader, etc.)
Types/Enums.cs              <- SessionRunStatus, QuestionRunStatus, RoundRunStatus
Session/
  SessionConfig.cs          <- Unified session manifest model
  SessionPreparer.cs        <- Interactive + programmatic session creation
  SessionRunner.cs          <- Session orchestrator (cascade error handling, ledger, Morning Brief)
  SessionPersistence.cs     <- Crash-safe file I/O with completion markers
  DecisionsLedger.cs        <- Append-only decisions ledger
Discussion/
  DiscussionEngine.cs       <- Round orchestration + synthesis
  RoundRunner.cs            <- Single-round agent execution with speaking order
Agents/
  AgentConfig.cs            <- 6-layer agent model (personality, position, technique, anti-slop, voice, output)
  AgentLoader.cs            <- YAML agent/team deserialization
  PromptBuilder.cs          <- 3-layer prompt assembly (identity, situation, task)
Config/
  ConfigLoader.cs           <- YAML config loading with caching
  AppSettings.cs            <- Settings classes
Runner/
  ClaudeRunner.cs           <- Claude CLI subprocess wrapper with retry
Synthesis/
  MorningBriefGenerator.cs  <- LLM-based executive summary from ledger
Evaluation/
  Evaluator.cs              <- Post-session LLM scoring
Live/
  LiveServer.cs             <- ASP.NET SSE server
  SseSessionEmitter.cs      <- Lock-free event distribution
  ISessionEventEmitter.cs   <- Event types
```

## Hard Rules

**DO NOT** modify agent YAML files during a session — they are loaded at session start and cached.

**DO NOT** edit files in `output/` — they are write-only runtime artifacts.

**DO NOT** delete `<!-- complete -->` markers from session files — they are the crash recovery mechanism.

**Use** `config/defaults.yaml` to change timeouts, truncation, thresholds — not C# code.

**Use** `data/teams/*.yaml` to add modes — modes are a team-level concern.

## Tests

```bash
cd _SYSTEM/projects/engine_standalone
dotnet test
```

78 tests covering: agent loading, brief parsing, config loading, decisions ledger, session persistence, session config serialization, session preparation.
