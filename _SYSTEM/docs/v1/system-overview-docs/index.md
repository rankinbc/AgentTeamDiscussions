# System Concepts

AgentTeamDiscussions enables unmonitored, overnight AI conversations that turn a high-level idea into thorough specifications and requirements — with no gaps and no human intervention.

## V1 Core Concepts

These five concepts define the V1 system. Each document describes what the component does, why it exists, and how it interacts with the others.

| # | Concept | Purpose |
|---|---------|---------|
| 1 | [Conversation Engine](conversation-engine.md) | Orchestrates discussion flow — round structure, phase progression, turn sequencing, convergence detection, artifact quality |
| 2 | [Creativity Engine](creativity-engine.md) | Makes agents genuinely different — personality model, anti-slop mechanisms, voice constraints, cognitive techniques |
| 3 | [Discussion Agents](discussion-agents.md) | The individual AI participants — stateless invocations shaped by configuration, producing output with signal metadata |
| 4 | [Session Platform](session-platform.md) | Manages session lifecycle — persistence, crash recovery, decision ledgers, Morning Brief generation |
| 5 | [Context Management](context-management.md) | Assembles what each agent sees per turn — token budgets, truncation, history windowing, external context (future) |
| 6 | [Evaluation & Improvement](evaluation-and-improvement.md) | Review session output, identify successes/failures, feed insights back into configuration and structure |
| 7 | [Agent Workshop](agent-workshop.md) | Optional web UI for creating, tuning, and reusing agents and groups — visual configuration and iteration |
| 8 | [Agent Actions](agent-actions.md) | Configurable capabilities (prompt-based V1, tool-based V2) injected into agent turns by the engine |

## V2 Concepts

These concepts extend V1 with multi-team dynamics, external knowledge, and cross-team communication.

| # | Concept | Purpose |
|---|---------|---------|
| 9 | [Team Configuration](team-configuration.md) | Multi-team YAML surface — defines separate teams, cross-team dynamics, and spokesperson rules |
| 10 | [MCP Message Broker](mcp-message-broker.md) | Cross-team communication backbone — channels, visibility boundaries, artifact versioning |
| 11 | [Research Engine](research-engine.md) | External knowledge gathering — agents verify claims, check feasibility, and ground specs in reality |

## How They Connect (V1)

```
         Agent Configuration (YAML)
                   |
            defines agents
                   |
     +-------------+-------------+
     |                           |
Creativity Engine         Conversation Engine
(shapes HOW agents       (controls WHEN/WHO speaks,
 think & differ)          enforces artifact quality)
     |                           |
     +-----> Discussion Agents <-+
                   |
          context assembled by
                   |
            Context Management
            (token budgets, history,
             future: external sources)
                   |
            persisted by
                   |
            Session Platform
            (decisions, artifacts,
             Morning Brief)
                   |
            reviewed by
                   |
         Evaluation & Improvement
         (what worked, what didn't,
          feed back into config)
                   |
         tunes ----+----> Agent Configuration
                   +----> Conversation Engine
                   +----> Creativity Engine
```

## V2 Extension

```
  V1 Core (above)
       |
       + Team Configuration -----> Multiple agent groups with independent context
       |
       + MCP Message Broker -----> Cross-team channels, visibility, spokesperson model
       |
       + Research Engine ---------> Sub-agents that verify, research, ground in reality
```

## End Goal

A user provides a high-level idea and agent configuration. The system runs overnight. In the morning, the user finds:

- A **Morning Brief** summarizing decisions, risks, and open questions
- **Implementable specifications** with acceptance criteria, edge cases, and dependency mapping
- A **decision ledger** tracking every conclusion with confidence and commitment levels
- Clear identification of **gaps that need human input**

No monitoring required. No prompt babysitting. Just useful output from a group of AIs that actually disagree with each other.
