# Engine

Primary discussion application. Structured multi-round sessions, live conversation, and evaluation.

## Entry Points

### session_runner.py — Structured brief-based discussions

Briefs live in `_SYSTEM/data/briefs/`. Output goes to `output/` at the repo root.

```bash
python session_runner.py _SYSTEM/data/briefs/my-brief.md          # full overnight session
python session_runner.py brief.md --mode compete                   # specific experiment mode
python session_runner.py brief.md --no-session                     # design docs → output/design-docs/
python session_runner.py brief.md --live                           # with live web dashboard
python session_runner.py brief.md --resume 2026-03-18_0553         # resume interrupted session
python session_runner.py brief.md --eval                           # run evaluation after session
```

**Output locations:**
- Full sessions → `output/sessions/{YYYY-MM-DD_HHMM}_{brief-slug}/`
- `--no-session` design docs → `output/design-docs/`
- Brainstorm panel runs → `output/panel-runs/`

| Flag | Default | Description |
|---|---|---|
| `--mode` | `compete` | `default`, `counter`, `lean`, `compete`, `bigsmall`, `angles`, `ideas`, `ideas_compete` |
| `--timeout` | `120` | Seconds per LLM call |
| `--no-session` | off | Skip session management; writes docs to `--output-dir` |
| `--live` | off | Enable web dashboard on port 8899 |
| `--resume` | none | Resume session by folder name |
| `--eval` | off | Run evaluation scoring after session |

### live_conversation.py — Interactive real-time agent chat

```bash
python live_conversation.py "How should we handle error recovery?"
python live_conversation.py "A music tool for producers" --mode spec
python live_conversation.py "topic" --agents cognitive_architect,adversarial_critic --turns 20
```

## Hard Rules

**NEVER** use `config/teams/` as agent source of truth — use `_SYSTEM/data/teams/` and `_SYSTEM/data/discussionAgents/`.

**DO NOT** import from `run_discussion` — that module was renamed to `discussion/engine.py`.

**DO NOT** import from `lib.*` — `lib/` has been deleted. Import from `agentteam.*` directly.

## Configuration

All behavior is config-driven. Edit YAML, not Python:

| What to change | File |
|---|---|
| Timeouts, truncation limits, health thresholds | `config/defaults.yaml` |
| Discussion modes (agent groupings) | `config/experiment_modes.yaml` |
| Agent display names and colors | `config/agent_display.yaml` |
| Per-role instruction overlays | `config/role_overlays.yaml` |
| Prompt templates | `templates/prompts/*.md.j2` |

**Adding a new experiment mode:** add entry to `config/experiment_modes.yaml`. No Python changes required.
**Adding a new prompt template:** add `templates/prompts/{name}.md.j2`, load via `config_loader.load_prompt_raw()`.

## Project Structure

```
discussion/engine.py      → Round orchestration, synthesis, transcript formatting
session/runner.py         → Session lifecycle, crash recovery, ledger, Morning Brief
live/server.py            → SSE-based HTTP server for live dashboard
conversation/             → state.py, modes.py, interactive.py
brainstorm/               → Panel queries and analysis pipeline
bmad/                     → BMAD workflow parser
evaluation/evaluator.py   → LLM-based quality scoring
config/                   → All tunable YAML config
templates/                → Jinja2 prompt templates and HTML dashboard
```

## Brief File Format

```markdown
## What's Already Decided
- Decision 1

## Open Questions
1. **Question Title** Question body with context.
```

## Experiment Modes

| Mode | Description |
|---|---|
| `default` | Original 6-agent, 3-round structure |
| `counter` | 2nd proposer must counter-propose the 1st |
| `lean` | 4 agents only |
| `compete` | Competitive vs Minimalist proposers |
| `bigsmall` | Maximalist vs Minimalist proposers |
| `angles` | Contrarian vs Operator proposers |
| `ideas` | Idea Merchant + Architect proposing |
| `ideas_compete` | Idea Merchant vs Minimalist |

## Reference

Read `_SYSTEM/docs/concepts/` before modifying conversation engine or discussion rounds.
Read `_SYSTEM/docs/v1/` before changing session lifecycle, ledger, or Morning Brief.
Read `config/defaults.yaml` for all tunable thresholds — change config, not Python.
