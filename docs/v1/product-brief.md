# AgentTeamDiscussions — Product Brief

## One-Liner

An overnight AI discussion engine that turns a product idea into a complete planning package — specs, requirements, architecture decisions — by running structured multi-agent debates while you sleep.

## The Problem

You're a builder with product ideas. The bottleneck isn't coding — AI coding agents handle that increasingly well. The bottleneck is *planning*. Thinking through edge cases, writing requirements, mapping user journeys, resolving architectural tradeoffs. This work is tedious, takes days, and you're doing it alone — without the cross-functional team that would catch your blind spots.

A single AI conversation doesn't solve this. One AI produces one perspective. It agrees with you, takes the safe path, and misses the things a skeptical engineer or a demanding product person would catch. You don't need a helpful assistant — you need a team that argues.

## The Solution

AgentTeamDiscussions runs a structured multi-agent debate on your idea overnight. You provide a high-level concept with enough context to be useful (1-2 pages), configure a team of AI agents with distinct perspectives and thinking styles, and let it run. In the morning, you get:

- A **Morning Brief** summarizing what was decided, what's risky, and what needs your input
- **Design specifications** synthesized from structured rounds of proposal, critique, and evaluation
- A **decision ledger** tracking every conclusion with confidence levels
- Clear identification of **gaps you hadn't considered**

The output is structured markdown — ready to hand to AI coding agents (Claude Code, Cursor, etc.) for implementation.

## How It Works

### The Discussion Loop

Each question in your brief goes through structured rounds:

1. **Propose** — Agents generate solutions, mechanisms, and approaches (parallel)
2. **Critique** — Different agents challenge assumptions, find gaps, stress-test (parallel)
3. **Evaluate** — A third group assesses feasibility and user impact (parallel)
4. **Synthesize** — A neutral moderator merges all rounds into a coherent design document

Agents within a round run in parallel. Rounds run sequentially so each builds on the previous. Decisions accumulate in an append-only ledger that chains forward as context.

### What Makes Agents Actually Disagree

The core technical challenge is preventing LLM convergence — six agents producing six variations of the same safe answer. AgentTeamDiscussions solves this through:

- **Personality Model**: 8+ scalar dimensions (assertiveness, risk tolerance, stubbornness, etc.) translated into natural language behavioral descriptions
- **Positional Framing**: Each agent has authentic motivation — what drives them, what they push back on, how intensely they hold positions
- **Anti-Slop Mechanisms**: Agreement tax (must add something new to agree), uncomfortable idea quotas, devil's advocate duty, domain pivot triggers
- **Voice Constraints**: Per-agent tone, vocabulary, and anti-patterns (phrases they must never use)

These aren't cosmetic — they produce measurably different output across agents, validated across 14 experiment runs.

### Overnight Autonomy

The system is designed to run 8+ hours unattended:
- **Stateless agent invocations**: Every turn reconstructs context from files. No persistent state to corrupt
- **Immediate disk persistence**: Every completed turn is written before the next starts
- **Crash recovery**: On restart, scan session folder and resume from the last completed question
- **Graceful degradation**: If critique fails, save the proposal. If synthesis fails, save all rounds as raw artifacts

## The Pipeline

```
Your Idea (1-2 pages)
    ↓
AgentTeamDiscussions (overnight, unattended)
    ↓
Planning Package (specs, PRD, architecture, decisions)
    ↓
AI Coding Agents (Claude Code, Cursor, etc.)
    ↓
Working Application
```

You're automating the planning layer. Idea to code with minimal manual effort.

## Success Criteria

**The success moment**: You open the output, skim it, and think "they caught that edge case I would've missed" and "I wouldn't have thought to structure it this way." Not perfect — but 80-90% there, saving you days of planning work.

**Measurable outcomes:**
- End-to-end: idea input to complete spec package in < 8 hours unattended
- Spec completeness: output addresses > 80% of requirements a human PM would identify
- Gap discovery: at least 3 non-obvious insights per session that weren't in the input
- Review time: < 1 hour to review and modify output before it's implementation-ready
- Reliability: < 10% session failure rate on well-formed inputs

## V1 System Architecture

Six core concepts power the system:

| Concept | Purpose |
|---|---|
| **Conversation Engine** | Orchestrates rounds, phases, turn sequencing, artifact quality |
| **Creativity Engine** | Makes agents genuinely different — personality, anti-slop, voice |
| **Discussion Agents** | Stateless AI participants shaped by configuration |
| **Session Platform** | Persistence, crash recovery, decision ledgers, Morning Brief |
| **Context Management** | Assembles what each agent sees per turn within token budgets |
| **Evaluation & Improvement** | Review session output, identify failures, feed insights back |

## V1 Scope (MVP)

- Single group of agents discussing one idea (6 agents, configurable via YAML)
- Three-round discussion per question (propose/critique/evaluate + synthesis)
- Prior context chaining across questions (decisions ledger)
- Morning Brief output with decisions and open items
- Session folder with transcripts and design docs
- Crash-safe disk writes with session resume
- CLI invocation: `python session_runner.py brief.md`

## V2 Scope (Growth)

- **Multi-team communication** via MCP message broker (two teams with independent context, spokesperson model)
- **Team Configuration** — separate teams with cross-team dynamics and visibility boundaries
- **Research Engine** — agents verify claims, check feasibility, ground specs in external reality
- Phase system (Brainstorm → Refine → Specify → Review) with automatic transitions
- Moderator input (live steering of running sessions)
- Dynamic turn ordering (rebuttal priority / urgency meter)
- Multiple output artifact types (PRD, architecture doc, user stories)

## What's Different

| Approach | Limitation |
|---|---|
| Single AI conversation | One perspective, convergence to safe answers, misses blind spots |
| Multi-agent frameworks (AutoGen, CrewAI, LangGraph) | General plumbing — no creativity engine, no anti-slop, no structured debate. You'd build everything on top |
| Human cross-functional team | Expensive, slow, scheduling overhead. Not available at 2 AM when you have an idea |
| Solo planning | Your blind spots are invisible to you. You spend days on work that's tedious but necessary |

AgentTeamDiscussions is differentiated by:
1. **Anti-convergence mechanisms** that produce genuinely different perspectives (not cosmetic variation)
2. **Structured opposition** (propose/critique/evaluate) rather than freeform agent chat
3. **Overnight autonomy** as a first-class design constraint
4. **Planning artifacts** as the output — not conversation, but implementable specs

## Open Challenges

1. **Artifact quality gap**: The distance between "good decisions from debate" and "implementable specification with acceptance criteria and edge cases" is the hardest unsolved problem. Synthesis must do heavy lifting to bridge this
2. **Evaluation harness**: How to efficiently review overnight output and identify what to improve — the "morning after" UX problem
3. **Spec completeness**: Agents reason from training data only (V1). Without research capability, specs may contain unverifiable technical assumptions

## Technical Requirements

- Python (orchestrator, agent management, session runner)
- Claude Max subscription (OAuth token, not API key)
- Claude CLI (`claude -p` subprocess invocations)
- No database — file-based persistence (portable, human-readable)
- Runs on a single machine — no infrastructure required
