# EngineStandalone

A self-contained C# .NET 8 multi-agent AI discussion engine. Multiple AI agents with distinct personalities, positions, and techniques discuss open questions through structured rounds, producing design documents and an executive summary.

## What It Does

You give it a topic and a team of AI agents. The engine runs a structured multi-round discussion:

1. **Propose** — Two agents independently propose solutions
2. **Critique** — Two different agents challenge the proposals
3. **Evaluate** — Two more agents assess what survives critique
4. **Synthesize** — A neutral moderator merges everything into a design document

Each question produces a design doc, a full transcript, and extracted decisions. At the end, a Morning Brief summarizes all decisions into a 90-second executive read.

## Quick Start

### Prerequisites

- .NET 8 SDK
- [Claude CLI](https://docs.anthropic.com/en/docs/claude-cli) installed and authenticated (`claude` on PATH)

### Build and Run

```bash
cd _SYSTEM/projects/engine
dotnet build

# Interactive — prompts for topic, team, agents, mode
dotnet run --project src/EngineStandalone -- new

# Quick — topic from CLI
dotnet run --project src/EngineStandalone -- new --topic "How should we handle authentication?"

# From a brief file
dotnet run --project src/EngineStandalone -- input/my-brief.md
```

### What You Get

```
output/sessions/2026-03-26_1430_authentication/
  session.json              # Complete session manifest
  decisions_ledger.md       # All decisions extracted across questions
  summary.md                # Morning Brief — the executive summary
  questions/
    01-authentication.md    # Design document
    01-authentication-transcript.md  # Full agent discussion
```

## Commands

### `new` — Create a Session Interactively

```bash
# Full interactive flow (prompts for everything)
dotnet run --project src/EngineStandalone -- new

# Skip prompts with flags
dotnet run --project src/EngineStandalone -- new --topic "Design the error handling strategy"

# Pick specific agents from a team
dotnet run --project src/EngineStandalone -- new \
  --topic "Auth system" \
  --team beta-agents \
  --agents cognitive_architect,adversarial_critic,flow_orchestrator

# With live web dashboard
dotnet run --project src/EngineStandalone -- new --topic "Error handling" --live
```

| Flag | Description |
|------|-------------|
| `--topic` `-t` | Topic to discuss (skip interactive prompt) |
| `--team` | Team name (skip team selection) |
| `--agents` | Comma-separated agent keys to include |
| `--live` | Start SSE web dashboard |
| `--eval` | Run quality evaluation after session |

### `<brief.md>` — Run from a Brief File

```bash
dotnet run --project src/EngineStandalone -- input/my-brief.md
dotnet run --project src/EngineStandalone -- input/my-brief.md --live --eval
dotnet run --project src/EngineStandalone -- --resume 2026-03-26_1430_my-brief
```

Brief files use this format:

```markdown
# Project Title

## What's Already Decided

- Constraint 1
- Constraint 2

## Open Questions

1. **Question Title** Detailed question body with context.
2. **Another Question** More context explaining the design decision needed.
```

### `eval` — Evaluate Session Output

```bash
dotnet run --project src/EngineStandalone -- eval output/sessions/my-session/questions
```

Runs LLM-based scoring on design docs and transcripts, producing a report with scores for clarity, completeness, actionability, engagement, and diversity.

### `list-teams` — Show Available Teams

```bash
dotnet run --project src/EngineStandalone -- list-teams
```

## Teams and Agents

### Beta Agents (7 agents)

The default general-purpose discussion team:

| Agent | Role | Job |
|-------|------|-----|
| Cognitive Architect | Creativity engine designer | Propose |
| Flow Orchestrator | Mechanical flow designer | Propose |
| Systems Pragmatist | Infrastructure realist | Critique |
| Adversarial Critic | Adversarial reviewer | Critique |
| Product Oracle | User advocate | Evaluate |
| Context Surgeon | Context efficiency evaluator | Evaluate |
| Idea Merchant | Idea generator | Propose (alt) |

### EV18Hornet (5 agents)

Game design team for a specific project:

| Agent | Role | Job |
|-------|------|-----|
| Max (Flight Dreamer) | Atmospheric flight advocate | Propose |
| Ren (Emergence Theorist) | Emergence systems theorist | Propose |
| Vera (EV Purist) | EV systems historian | Critique |
| Nadia (Player Advocate) | New-player experience | Critique |
| Soren (Scope Warden) | Solo dev scope realist | Evaluate |

### Agent Selection

You don't have to use all agents. During interactive setup, or via `--agents`, pick a subset:

```bash
# Use only 3 agents for a focused discussion
dotnet run --project src/EngineStandalone -- new \
  --agents cognitive_architect,adversarial_critic,flow_orchestrator
```

The engine automatically filters round groups to only include your selected agents and drops empty rounds.

### Adding a New Team

1. Create agent YAML files in `data/agents/{team}__{agent_key}.yaml`
2. Create `data/teams/{team}.yaml` with agent references and modes
3. No C# changes needed

## Discussion Modes

Each team defines its own modes — round structures with optional behavioral overlays.

### Beta Agents Modes

| Mode | Description |
|------|-------------|
| `compete` (default) | Competitive vs Minimalist proposers |
| `default` | 6-agent, 3-round, no overlays |
| `counter` | 1st proposes, 2nd must counter-propose |
| `lean` | 4 agents only |
| `bigsmall` | Maximalist vs Minimalist |
| `angles` | Contrarian vs Operator, User-first evaluator |
| `ideas` | Idea Merchant + Architect proposing |
| `ideas_compete` | Idea Merchant (wild) vs Orchestrator (minimalist) |

## How It Works

### Agent Architecture (6 layers)

Each agent is defined by six independent configuration layers:

1. **Personality** — 8 scalar traits (0.0-1.0): assertiveness, creativity, risk tolerance, stubbornness, bluntness, patience, idea receptivity, attention span. Plus cognitive style and emotional baseline.
2. **Position** — Role, drives (what they fight for), pushback triggers, intensity
3. **Technique** — Primary thinking method, style description, specific behaviors
4. **Anti-Slop** — Countermeasures against LLM convergence: agreement tax, perspective enforcement, devil's advocate duty, uncomfortable idea quotas, domain pivoting
5. **Voice** — Tone, brevity, vocabulary hints, forbidden phrases
6. **Output** — Operating level (requirements/design/implementation), job type (propose/critique/evaluate)

### Prompt Assembly (3 tiers per turn)

- **Identity Layer** (~2K tokens, static) — Persona, personality-as-prose, position, technique, anti-slop, voice
- **Situation Layer** (~3-5K tokens, dynamic) — Decisions, prior rounds, prior design docs, open questions
- **Task Layer** (~500 tokens, never cut) — Question body, round instruction, speaking reminder

### Speaking Order

Agents speak in a computed order within each round:
`score = assertiveness * 0.5 + intensity * 0.3 + stubbornness * 0.2 + jitter`

Higher-scoring agents speak first and set the agenda. Later speakers see what earlier speakers said.

### Crash Recovery

Every file is written with a `<!-- complete -->` marker. On resume, files missing the marker are treated as incomplete and regenerated. Progress is derived from artifacts on disk, not a checkpoint file.

### Error Handling (Cascade Rules)

- Propose fails: skip entire question
- Critique/evaluate fails: save what we have, mark partial
- Synthesis fails: save transcript, no design doc
- 3 consecutive question failures: circuit breaker stops the session

### Session Manifest (session.json)

The unified session manifest replaces the old split between brief files, CLI flags, and status files:

```json
{
  "version": 1,
  "title": "Auth System Design",
  "decided": ["Using JWT tokens"],
  "questions": [{"number": 1, "title": "Token storage", "body": "..."}],
  "team": "beta-agents",
  "agents": ["cognitive_architect", "adversarial_critic"],
  "mode": "compete",
  "timeout": 120,
  "state": {
    "status": "complete",
    "session_complete": true,
    "completed_questions": 3,
    "failed_questions": 0,
    "questions": {
      "q1": {"status": "complete", "elapsed_seconds": 165, "file": "01-token-storage.md"}
    }
  }
}
```

## Configuration

All tunable settings live in `config/defaults.yaml`:

| Section | Key Settings |
|---------|-------------|
| `timeouts` | `default: 120`, `discussion: 420`, `evaluation: 300` |
| `truncation` | `prior_specs: 6000`, `design_doc_chain: 3000` |
| `health_checks` | `circuit_breaker_threshold: 3`, `min_response_length: 20` |
| `paths` | `sessions_dir`, `output_dir`, `default_team` |
| `session` | `run_eval: false`, `live_port: 8899` |

Role overlays (behavioral modifiers) are in `config/role_overlays.yaml`: competitive, minimalist, maximalist, contrarian, operator, user_first.

## Project Structure

```
engine/
  src/
    EngineStandalone/           # Main application
      Abstractions/             # Service interfaces (DI)
      Types/                    # Enums (SessionRunStatus, etc.)
      Agents/                   # AgentConfig, AgentLoader, PromptBuilder
      Brief/                    # BriefParser
      Config/                   # ConfigLoader, AppSettings, TemplateRenderer
      Discussion/               # DiscussionEngine, RoundRunner
      Evaluation/               # Evaluator (LLM-based scoring)
      Live/                     # SSE server, event emitter, event types
      Runner/                   # ClaudeRunner (subprocess wrapper)
      Session/                  # SessionRunner, SessionConfig, SessionPreparer, persistence
      Synthesis/                # MorningBriefGenerator
    EngineStandalone.Tests/     # xUnit tests (105 tests)
  config/                       # YAML configuration
  data/
    agents/                     # Individual agent YAML files
    teams/                      # Team manifests with modes
  input/                        # Place brief files here
  output/
    sessions/                   # Full session output
    design-docs/                # No-session mode output
  templates/
    prompts/                    # Jinja2/Scriban prompt templates
    evaluation/                 # Evaluation prompt templates
```

## Dependencies

- **YamlDotNet 15.1.2** — YAML parsing for agent/team/config files
- **Scriban 7.0.5** — Template rendering (Jinja2-compatible)
- **System.CommandLine 2.0.0-beta4** — CLI argument parsing
- **ASP.NET Core** (via Web SDK) — SSE server for live dashboard

## Tests

```bash
dotnet test
```

105 tests covering agent loading, brief parsing, config loading, prompt building (including history-windowing edge cases), context telemetry, context budget enforcement, discussion compression, decisions ledger, session persistence, session config serialization (with enum round-tripping), and session preparation (topic parsing, title extraction).
