# Research Engine

> **V2 Concept** — Not in V1 scope. Documented here to capture intent and inform V1 design decisions.

## What It Is

The Research Engine gives agents the ability to look things up during a discussion. Instead of reasoning purely from what's in their prompt, agents can spawn research sub-tasks that verify claims, check API feasibility, survey competitive approaches, or gather domain-specific data. It's the difference between agents debating from opinion and agents debating from evidence.

## Why It Exists

V1 agents are closed-world reasoners — they can only work with what's in their context window. This is fine for brainstorming and high-level design, but falls short of the "no gaps" promise. Thorough specifications require grounding:

- "Use WebSockets for real-time updates" — but does the target platform support them?
- "Integrate with Stripe for payments" — but what does their API actually look like?
- "This approach scales to 10K users" — based on what evidence?

The Research Engine closes the gap between "plausible spec" and "grounded spec" by letting agents verify their assumptions against real information.

## How It Would Fit the System

- **Triggered by Conversation Engine**: When an agent signals `needs: more-research`, the engine can spawn a research sub-task
- **Results flow through Context Management**: Research findings become part of the situation layer for subsequent turns
- **Scoped by Session Platform**: Research has a budget (max spawns, max time) to prevent runaway costs
- **Independent of Creativity Engine**: Research agents don't need personality — they need accuracy

## Core Responsibilities (Planned)

### Research Sub-Agent Spawning
- Dedicated research agents with web search, documentation lookup, and API exploration capabilities
- Scoped queries with clear deliverables ("verify that X supports Y" not "research everything about X")
- Results formatted for context injection — concise, factual, citable

### Feasibility Verification
- Check that technical assumptions in specs are grounded
- Verify API capabilities, library support, platform constraints
- Flag specs that make unverifiable claims

### Competitive and Domain Research
- Survey existing solutions in the problem space
- Identify patterns and anti-patterns from similar systems
- Bring external context that agents can't generate from training data alone

### Budget Management
- Maximum research spawns per session
- Time limits per research task
- Cost tracking (research calls consume additional LLM invocations)

## Key Design Constraints

- Research must be scoped and budgeted — unbounded research defeats the overnight autonomy goal
- Research results must be concise enough to fit in context windows without displacing discussion history
- Research agents are utility agents, not discussion participants — they don't have opinions
- Results should be cached within a session to avoid redundant lookups

## V1 Implications

Even without a Research Engine, V1 should:
- Design Context Management to accommodate external data injection (future-proofing the situation layer)
- Include `needs: more-research` as a valid agent signal, even if nothing acts on it yet
- Structure the Session Platform to store research artifacts when they eventually exist

## Current State

Not implemented. V1 agents reason from training data and provided context only. The Research Engine is planned for V2 alongside multi-team support and the MCP Message Broker.
