# Context Management

## What It Is

Context Management is the subsystem responsible for assembling what each agent sees on every turn. It builds the context payload — the combination of identity, conversation history, accumulated decisions, and task directive — that fits within token budgets while preserving maximum signal. It's the system's editor: deciding what to include, what to compress, and what to cut.

## Why It Exists

Each agent turn is a stateless Claude call. The agent has no memory of previous turns — everything it knows must be in the prompt. Over an 8-hour discussion with dozens of questions and hundreds of turns, the accumulated context grows far beyond what fits in a single prompt. Something has to decide what matters right now.

Context Management makes this decision systematically. Without it, agents would either see too little context (losing thread of the discussion) or hit token limits (failing entirely). It's the reason overnight sessions stay coherent from question 1 to question 10.

## How It Fits the System

Context Management sits between the data sources (conversation history, decision ledger, artifacts) and the agent invocation:

- **Called by Conversation Engine**: Before each agent turn, the engine requests an assembled context payload
- **Reads from Session Platform**: Accesses the decision ledger and prior design documents
- **Incorporates Creativity Engine rules**: Includes perspective reminders to fight identity drift
- **Reads from agent configuration**: Agent identity content determines Layer 1

Context Management is a separate module from the Conversation Engine — not a sub-responsibility — because its scope will grow significantly. In V1, context comes from conversation history and the decision ledger. In future versions, context will include external sources: prior session results, user-provided reference material, research findings, RAG-retrieved knowledge, and other data that exists outside the conversation itself. Keeping context assembly as its own module ensures this growth doesn't bloat the Conversation Engine.

## Core Responsibilities

### Three-Layer Context Assembly
Every agent turn receives a context payload assembled in three layers:

**Layer 1 — Identity (~2,000 tokens)**
- Agent persona, role, description
- Personality trait descriptions (rendered from scalar values to natural language)
- Positional framing (drives, pushback, intensity)
- Technique and behavioral rules
- Anti-slop constraints
- Voice rules

This layer is static per agent across the session. Built once from agent YAML configuration.

**Layer 2 — Situation (~3,000-5,000 tokens)**
- Current phase and progress indicators
- Decision ledger (all accumulated decisions — never truncated)
- Recent message history (full fidelity for last 3-5 turns)
- Compressed summaries of older turns
- Prior design document (the most recent synthesized spec)
- Relevant artifacts from the current phase

This layer changes every turn. It's where the budget pressure lives.

**Layer 3 — Task (~500 tokens)**
- The specific question or directive for this turn
- Round instruction (propose/critique/evaluate)
- Forcing function (a concrete ask, not a vague "discuss")
- Perspective reminder (compact identity reinforcement)

### Truncation Strategy
When context exceeds budget, cuts happen in priority order:
1. Keep full recent history (last 3-5 turns — agents need conversational continuity)
2. Compress older turns to decisions + key proposals only
3. Drop explanatory text from old turns (keep conclusions, cut reasoning)
4. Trim prior design docs (keep decisions section, cut background)

The decision ledger is never truncated. It grows linearly (~250 chars per question) and stays well within budget even at question 10.

### Prior Context Chaining
Each question in a session builds on previous ones:
- **Layer 1**: Decision ledger (all prior decisions, append-only)
- **Layer 2**: Previous design document only (not a sliding window of multiple docs)
- Total budget at question 8: ~4,000 characters — comfortably within limits

This design ensures agents know what's been decided without drowning in historical detail.

### Perspective Reminders
Compact identity reinforcement injected into each turn to fight LLM drift:
- Built from the agent's position and technique
- Reminds the agent what they care about and how they think
- Short enough (~100 tokens) to always fit within budget

### History Windowing
For multi-agent conversations, history is truncated to maintain relevance:
- Keep the first 2 messages (establish topic and framing)
- Keep the last 10 messages (recent conversational context)
- Drop middle messages entirely (they're captured in decisions and summaries)

## Key Design Constraints

- **Hard token ceiling**: ~4,000 tokens per turn (identity + situation + task). Context Management must always fit within this
- **Decision ledger is sacred**: Never summarized, never truncated. It's the thread of continuity across the session
- **Recency bias is intentional**: Recent turns get full fidelity. Older turns get compressed. This mirrors how productive conversations work — you build on the last few exchanges, not the opening statement
- **Extensible by design**: The module is structured to accommodate new context sources (external data, prior sessions, research findings) without changing the Conversation Engine
- **No agent self-management**: Agents don't decide what context they see. The system decides for them

## Interactions

| Component | Relationship |
|---|---|
| Conversation Engine | Requests assembled context payloads before each agent turn. Heavily coupled — the engine is the primary consumer |
| Session Platform | Source of decision ledger and prior design documents |
| Creativity Engine | Provides perspective reminders for identity reinforcement |
| Discussion Agents | Consumers of assembled context — they receive it, don't manage it |

## Current State

V1 implements the three-layer context assembly, history windowing (first 2 + last 10), perspective reminders, and prior-context chaining (decision ledger + previous design doc). The ~4,000 token budget is respected. Truncation strategies are functional but simple.

**Future growth areas:**
- External context sources (prior sessions, user-provided references, RAG)
- Research Engine findings injection (V2)
- LLM-based summarization of older turns (replacing simple truncation)
- Cross-team visibility filtering when MCP Message Broker is added (V2)
