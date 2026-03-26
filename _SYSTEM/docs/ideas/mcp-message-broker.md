# MCP Message Broker

> **V2 Concept** — Not in V1 scope. V1 uses direct orchestrator routing. Documented here to capture intent and inform V1 design decisions.

## What It Is

The MCP Message Broker is the communication backbone that enables true team-to-team conversations. It's a standalone TypeScript server that manages message channels, enforces visibility boundaries between teams, handles artifact versioning, and maintains phase state. Teams communicate exclusively through the broker — they never share context directly.

## Why It Exists

The core architectural insight of AgentTeamDiscussions is that productive team discussions require information asymmetry. When all agents share the same context, they converge. When teams have independent context windows and communicate only through structured channels, they develop genuine positions, deliberate internally, and present synthesized viewpoints — just like real cross-functional teams.

The MCP Message Broker enforces this boundary. It's what makes the difference between "a group of agents in one conversation" and "two teams negotiating through a shared communication layer."

For overnight autonomy, the broker also provides durability. Messages are persisted, artifacts are versioned, and the broker's state can be reconstructed after a crash.

## How It Fits the System

The MCP Message Broker is the communication infrastructure that all other components interact through:

- **Conversation Engine routes through it**: All cross-team messages pass through MCP channels. The engine never bypasses the broker
- **Discussion Agents communicate via it**: Agents send and receive messages through typed channels. Internal deliberation stays on internal channels (team-only visibility)
- **Session Platform reads from it**: Session transcripts, decision logs, and artifacts are collected from the broker's persistent storage
- **Context Management queries it**: When assembling context for an agent turn, Context Management fetches relevant messages from the broker (with visibility filtering)
- **Team Configuration defines channel membership**: Which agents belong to which team determines what they can see

## Core Responsibilities

### Message Channels
The broker manages typed communication channels:
- **Brainstorm**: Cross-team idea exchange — high volume, low structure
- **Internal**: Team-only deliberation — invisible to the other team
- **Research**: Research findings and external data
- **Decisions**: Logged decisions with confidence scores and commitment levels
- **Specs**: Generated artifacts (PRDs, architecture docs, requirements)

Each channel has visibility rules. Internal channels are team-scoped. All other channels are visible to both teams.

### Spokesperson Model
Raw internal debate never crosses team boundaries. Instead:
- Teams deliberate internally on their internal channel
- One agent synthesizes the team's position
- The synthesized message is posted to the cross-team channel
- The receiving team sees a composed position, not a debate transcript
- Contested decisions are surfaced explicitly with both sides noted

This mirrors how real teams communicate — you don't expose your internal disagreements to the other team.

### Phase State Management
The broker tracks the current discussion phase and enforces transition rules:
- Maintains phase state (brainstorm/refine/specify/review)
- Evaluates gate criteria for phase transitions
- Adjusts deliberation budgets per phase (e.g., more internal turns during specify)
- Generates Phase Transition Documents (PTDs) for context refresh at boundaries

### Artifact Management
The broker handles versioned artifacts produced during discussion:
- Draft and final states for specs, PRDs, architecture docs
- Version tracking as artifacts evolve across phases
- Traceability back to the decisions that spawned them
- Validation gates checking for completeness and implementation-readiness

### Message Persistence
All messages are stored with GUID filenames for efficient retrieval:
- Metadata in pointer files for fast scanning without reading full content
- Messages include sender, channel, type (question/proposal/agreement/challenge), confidence, and summary
- Provenance chains track how ideas evolved across turns

## Key Design Constraints

- **Standalone server**: Runs independently from the orchestrator. Could theoretically serve multiple orchestrators
- **Strict isolation**: The broker is the ONLY path for cross-team communication. No backdoor context sharing
- **File-based persistence**: GUID-named message files with metadata pointers. No database dependency
- **Channel-level visibility**: Agents see messages based on channel membership, not individual permissions
- **Stateless queries**: The broker serves context on request — it doesn't push context to agents

## Interactions

| Component | Relationship |
|---|---|
| Conversation Engine | Routes all cross-team messages through the broker; reads phase state |
| Discussion Agents | Send messages to channels; receive messages filtered by team visibility |
| Context Management | Queries the broker for relevant messages when assembling agent context |
| Session Platform | Collects transcripts, decisions, and artifacts from broker storage |
| Team Configuration | Defines team membership, which determines channel visibility |
| Creativity Engine | No direct interaction — creativity rules are enforced at the agent/engine level |

## Current State

The MCP Message Broker is designed but not yet implemented. V1 uses direct orchestrator routing — the Python orchestrator manages all message flow without a separate broker. The broker is the key infrastructure needed to move from single-team multi-agent discussions to true two-team conversations. Design specs exist for channels, phase management, artifact handling, and the spokesperson model.
