# Conversation Engine

## What It Is

The Conversation Engine is the orchestration core of AgentTeamDiscussions. It controls how discussions flow: who speaks when, what structure each round follows, how phases progress, and when a conversation has produced enough signal to move forward. It is the system's conductor — it doesn't generate ideas, but it ensures the right agents engage at the right time in the right way.

## Why It Exists

Unmonitored AI conversations collapse without structure. Agents agree too quickly, repeat each other, or spiral into unfocused tangent chains. The Conversation Engine imposes the minimum structure needed to keep discussions productive across hours of unattended operation — without over-constraining the creative output.

The end goal: a user submits a high-level idea before bed and wakes up to a thorough, gap-free specification. The Conversation Engine is what makes that journey reliable.

## How It Fits the System

The Conversation Engine sits at the center of the V1 architecture:

- **Reads agent configuration**: Which agents participate, their roles, and round assignments (from YAML configs)
- **Drives Discussion Agents**: Determines who speaks next, what directive they receive, what context they see
- **Delegates to Context Management**: Requests assembled context payloads for each agent turn
- **Enforces Creativity Engine rules**: Applies anti-slop triggers and role constraints at turn boundaries
- **Reports to Session Platform**: Emits events (turn complete, round complete, phase transition) for persistence and recovery
- **Owns artifact quality**: Ensures synthesized output meets completeness standards before marking a question done

## Core Responsibilities

### Round Structure
Each discussion question follows a structured multi-round pattern:
- **Propose**: Agents generate solutions, mechanisms, and approaches
- **Critique**: Different agents challenge assumptions, find gaps, and stress-test proposals
- **Evaluate**: A third group assesses feasibility, user impact, and implementation readiness
- **Synthesize**: A neutral moderator merges all rounds into a single coherent design document

Agents within a round run in parallel. Rounds execute sequentially so each builds on the previous.

### Phase Progression
Conversations move through phases with explicit gate criteria:
- **Brainstorm**: Divergent thinking, volume of ideas, no premature convergence
- **Refine**: Narrow scope, challenge assumptions, prioritize
- **Specify**: Pin down requirements, acceptance criteria, concrete details
- **Review**: Adversarial check — find what's missing, ambiguous, or wrong

Phase transitions are not time-based. They trigger when gate criteria are met (e.g., sufficient idea diversity, topic coverage, spec validation).

### Turn Sequencing
The engine decides who speaks next based on:
- Round role assignments (propose/critique/evaluate)
- Urgency signals from prior turns (rebuttal priority)
- Convergence detection (inject dissent when agents agree too quickly)
- Bench recall triggers (bring in sidelined agents when topics shift)

### Action Injection
The engine controls when [Agent Actions](agent-actions.md) fire. Actions are structured directives injected into the agent's task layer to shape their thinking on a specific turn. Three trigger mechanisms:
- **Configuration-driven**: Actions assigned to agents, rounds, or phases in YAML
- **Engine-scheduled**: Rules like "inject every 5th turn" or "on convergence detection"
- **Signal-requested**: Agents request an action via metadata signals; the engine grants or ignores

Actions are additive — they augment the normal turn directive, not replace it. See the Agent Actions concept doc for details.

### Convergence and Completion Detection
The engine monitors signal metadata from each agent turn (stance, confidence, ready-to-advance flags) to determine:
- When a round has sufficient coverage to synthesize
- When a phase gate is satisfied
- When the overall discussion has produced actionable output

### Artifact Quality (Open Challenge)
The gap between "decisions made in debate" and "implementable specification" is a core challenge. The Conversation Engine must bridge this through:

- **Structured artifact templates**: Synthesis produces specs with required sections (decision, rationale, acceptance criteria, edge cases, dependencies) — not freeform prose
- **Specification round**: After synthesis, agents review the synthesized doc against a completeness checklist — catching gaps before the question is marked done
- **Validation gates**: A spec isn't "complete" until it passes quality checks (no ambiguous requirements, no missing acceptance criteria, no unresolved dependencies)

This is the hardest unsolved problem in V1. The propose/critique/evaluate structure produces good *decisions*, but decisions alone don't constitute an implementable spec. The synthesis step must do heavy lifting to transform debate output into structured, actionable artifacts.

## Key Design Constraints

- **No shared state between agents**: Each turn is a stateless Claude call with fully reconstructed context
- **Token budget awareness**: The engine respects the ~4,000 token ceiling per turn and coordinates with Context Management on what to include
- **Crash resilience**: Every completed turn is persisted immediately; the engine can resume from any point
- **Overnight autonomy**: Must run 8+ hours without human intervention, making all sequencing decisions independently

## Interactions

| Component | Relationship |
|---|---|
| Discussion Agents | Engine directs agents — issues turn directives, receives responses and signals |
| Context Management | Engine requests context payloads; Context Management assembles them within budget |
| Creativity Engine | Engine enforces creativity rules at turn boundaries (anti-slop, role constraints) |
| Session Platform | Engine emits lifecycle events; Session Platform persists state and enables recovery |
| Agent Actions | Engine decides when to inject actions into agent turns based on config, schedule, or signals |

## Current State

V1 implements the core round structure (propose/critique/evaluate/synthesize) with parallel agent execution within rounds and sequential round progression. Phase gating and bench management are designed but not yet implemented. Artifact quality — ensuring synthesis produces implementable specs, not just decision summaries — is the primary open challenge.
