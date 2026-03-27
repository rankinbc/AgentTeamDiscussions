# Discussion Agents

## What It Is

Discussion Agents are the individual AI participants in a conversation. Each agent is a configured Claude instance with a unique identity, perspective, and behavioral profile. They are the voices in the discussion — the ones generating ideas, challenging proposals, evaluating feasibility, and synthesizing conclusions.

An agent is not a persistent process. It's a stateless invocation: a system prompt (built from configuration) + assembled context + a task directive = one turn of output. The agent exists for that turn, produces a response with metadata signals, and is gone. The next turn reconstructs everything from scratch.

## Why It Exists

The system's value comes from the quality and diversity of agent output. A single AI producing a spec will hit its blind spots and biases. Multiple agents with different drives, expertise lenses, and thinking styles cover more ground, challenge more assumptions, and produce output that a human can trust without having been in the room.

Discussion Agents are the unit of perspective. Each one represents a way of looking at the problem that the others don't naturally take. Together they approximate the coverage of a real cross-functional team — but one that can run overnight without breaks.

## How It Fits the System

Discussion Agents are where configuration meets execution:

- **Defined by agent configuration**: Agent identity, personality, position, techniques, voice — all from YAML
- **Shaped by Creativity Engine**: Personality traits and anti-slop rules are rendered into the agent's system prompt
- **Directed by Conversation Engine**: The engine tells the agent what round it's in, what question to address, and what role to play (propose/critique/evaluate)
- **Context provided by Context Management**: Each turn's context payload is assembled by the context system — the agent doesn't manage its own history
- **Output captured by Session Platform**: Every agent response is persisted immediately

## Core Responsibilities

### Generate Substantive Output
Each agent turn produces a response that advances the discussion:
- Proposals with concrete mechanisms and rationale
- Critiques that identify specific gaps, risks, or contradictions
- Evaluations that assess feasibility and user impact
- Synthesis that merges multiple viewpoints into coherent direction

Agents are constrained to ~250 words per turn. They don't produce code, schemas, or implementation details — they work at the requirements/design level.

### Emit Signal Metadata
Alongside prose output, each agent turn produces structured signals for the Conversation Engine:
- **Stance**: agreeing, challenging, extending, proposing, synthesizing, pivoting, questioning
- **Confidence**: 0.0-1.0 on their position
- **Ready to advance**: Whether they believe the current phase/round has sufficient coverage
- **Key claim**: One-sentence summary of their main point
- **Needs**: What would help them next (more research, counter-argument, evidence, team input)

These signals are invisible to other agents — only the Conversation Engine reads them.

### Execute Actions
Agents can receive [Agent Actions](agent-actions.md) — structured directives injected into their task layer by the Conversation Engine. Actions shape what the agent does on a specific turn beyond its normal discussion response:
- "Write the post-mortem for when this fails" (failure_postmortem)
- "Borrow a mechanism from a different industry" (steal_mechanism)
- "List every assumption this design makes" (assumption_audit)

Agents don't choose when to use actions — the engine decides based on configuration and discussion state. The agent simply receives an augmented directive and responds accordingly.

### Maintain Perspective Integrity
Agents must stay in character across turns. This is harder than it sounds — LLMs naturally drift toward a generic helpful persona. Agents fight this through:
- Perspective reminders injected into each turn's context
- Anti-slop rules that penalize generic agreement
- Positional framing that gives them authentic motivation to disagree

## Agent Archetypes

The system supports diverse agent types. Examples from existing configurations:

| Archetype | Drive | Example |
|---|---|---|
| Architect | System coherence and mechanism validation | "Does this actually work as a system?" |
| Pragmatist | Failure modes and operational reality | "What breaks at 3 AM with no one watching?" |
| Advocate | User outcomes and value delivery | "Does the user actually get what they need?" |
| Critic | Finding gaps and challenging assumptions | "Here are 5 things wrong with this proposal" |
| Ideator | Novel approaches from unexpected domains | "What if we stole this mechanism from improv comedy?" |
| Synthesizer | Data flow and integration coherence | "How does information actually move through this?" |

Agents can also represent realistic personas (e.g., a bedroom music producer, a skeptical mastering engineer) for domain-specific product discussions.

## Key Design Constraints

- **Stateless**: Every turn is a fresh Claude call. No persistent memory within the agent — all continuity comes from Context Management
- **Prompt-only identity**: Agent personality exists entirely in the system prompt. No fine-tuning, no agent-specific model weights
- **Parallel execution**: Agents within the same round run simultaneously. No agent can depend on another agent's output within the same round
- **Output constraints**: ~250 words, no code, no schemas. Stay at the requirements/ideas operating level
- **No self-awareness of the system**: Agents don't know they're part of an orchestrated discussion platform. They just respond to their directive

## Interactions

| Component | Relationship |
|---|---|
| Agent Configuration (YAML) | Defines agent identity, personality, position, techniques, voice |
| Creativity Engine | Shapes how agents think and express themselves via prompt engineering |
| Conversation Engine | Directs agents — issues turn directives, assigns round roles |
| Context Management | Assembles the context payload each agent sees per turn |
| Agent Actions | Actions augment the agent's task directive on specific turns |
| Session Platform | Persists every agent response and extracted signals |

## Current State

V1 has 7 agent archetypes in the beta-agents team, plus 4 additional domain-specific teams (22 agents total across 5 teams). Agents run as `claude -p` subprocess calls with full system prompt + context assembly. Anti-slop mechanisms and personality traits produce measurably different outputs across agents. Multi-team features (spokesperson model, internal deliberation, cross-team channels) are V2 scope.
