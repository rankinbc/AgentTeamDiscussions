# Documentation Index

## V1 Planning (Authoritative)

The V1 PRD and supporting specs that define what we're building now.

- **[product-brief.md](v1/product-brief.md)** -- Core value proposition, problem, solution, how it works
- **[prd.md](v1/prd.md)** -- V1 Product Requirements Document (43 FRs, 19 NFRs, 5 user journeys)
- **[v1-orchestrator-spec.md](v1/v1-orchestrator-spec.md)** -- V1 technical architecture, session lifecycle, deferred features
- **[v1-spec-gaps.md](v1/v1-spec-gaps.md)** -- 7 open implementation questions (decision extraction, error handling, synthesis reliability)

### System Overview (High-Level)
How the system works at a conceptual level. See **[index](v1/system-overview-docs/index.md)** for the full map.

- [Conversation Engine](v1/system-overview-docs/conversation-engine-overview.md) -- Round structure, phase progression, turn sequencing
- [Creativity Engine](v1/system-overview-docs/creativity-engine-overview.md) -- Personality model, anti-slop, voice constraints
- [Discussion Agents](v1/system-overview-docs/discussion-agents-overview.md) -- Stateless invocations shaped by config
- [Session Platform](v1/system-overview-docs/session-platform-overview.md) -- Persistence, crash recovery, Morning Brief
- [Context Management](v1/system-overview-docs/context-management-overview.md) -- Token budgets, 3-layer assembly, future external sources
- [Evaluation & Improvement](v1/system-overview-docs/evaluation-and-improvement-overview.md) -- Review output, feed insights back
- [Agent Workshop](v1/system-overview-docs/agent-workshop-overview.md) -- Optional web UI for agent creation/tuning
- [Agent Actions](v1/system-overview-docs/agent-actions-overview.md) -- Configurable prompt directives injected into turns
- [Agent Workshop UI Spec](v1/system-overview-docs/agent-workshop-ui-spec.md) -- Detailed UI specification

### Conversation Engine (V1 Specs)
- **[turn-anatomy.md](v1/conversation-engine/turn-anatomy.md)** -- Atomic turn structure, two turn types, context layers, output signals
- **[context-assembly-template.md](v1/conversation-engine/context-assembly-template.md)** -- Prompt template: 7 sections, 4000-token ceiling, cut priority tiers
- **[morning-brief-format.md](v1/conversation-engine/morning-brief-format.md)** -- Output format: RED/YELLOW/GREEN sections, 90-second read

### Creativity Engine (V1 Specs)
- **[personalities.md](v1/creativity-engine/personalities.md)** -- 8-dimension personality model with trait definitions
- **[positions.md](v1/creativity-engine/positions.md)** -- 8 stakeholder positions with conflict matrix
- **[techniques.md](v1/creativity-engine/techniques.md)** -- 10 agent archetypes with reasoning methods
- **[anti-slop-mechanisms.md](v1/creativity-engine/anti-slop-mechanisms.md)** -- 8 LLM failure modes, 10 countermeasures

---

## Concepts

Design philosophy, research, and agent-panel explorations.

- **[design-principles.md](concepts/design-principles.md)** -- Three-layer context model, bias statements, forcing functions, signals
- **[creativity-engine-overview.md](concepts/creativity-engine-overview.md)** -- Cross-walk index for creativity engine specs

### Research
- **[research-applied.md](concepts/research/research-applied.md)** -- 10 research domains mapped to 26 mechanisms
- **[MakingAgentsNotActLikeAI.md](concepts/research/MakingAgentsNotActLikeAI.md)** -- 40+ mechanisms from psychology, improv, game theory
- **[EngineeringRobustMultiAgentLLMDiscussions.md](concepts/research/EngineeringRobustMultiAgentLLMDiscussions.md)** -- Best practices from AutoGen, CrewAI, LangGraph
- **[RESEARCH-PROMPT.md](concepts/research/RESEARCH-PROMPT.md)** -- Research agenda for 10 cross-domain areas

### Conversation Engine Concepts (Agent Panel Output)
9 design explorations + 10 raw transcripts. See **[agent-panel-index.md](concepts/conversation-engine/agent-panel-index.md)** for navigation.

---

## Ideas (Deferred Features)

Unused or deferred ideas worth revisiting for V2+. Not stale -- just not V1.

- **[entity-model.md](ideas/entity-model.md)** -- Magnitude-based ideas/stances, BackgroundAgents, complex entity persistence
- **[orchestrator-event-cadence.md](ideas/orchestrator-event-cadence.md)** -- Per-turn convergence detection, disruption injection, dropped-thread callbacks
- **[key-takeaway-mechanism.md](ideas/key-takeaway-mechanism.md)** -- Convergence voting: proposal, confirmation, tombstones, contestation
- **[rebuttal-priority.md](ideas/rebuttal-priority.md)** -- Dynamic turn ordering via urgency meter + ego injection
- **[moderator-input.md](ideas/moderator-input.md)** -- Live steering via HTTP endpoint during sessions
- **[phase-dynamics.md](ideas/phase-dynamics.md)** -- Per-phase personality weighting (Brainstorm/Refine/Specify/Review)
- **[session-platform.md](ideas/session-platform.md)** -- Agent library, session-as-package, interactive setup, feedback loop
- **[research-scope-controls.md](ideas/research-scope-controls.md)** -- 4-layer research cost control stack
- **[agent-behavior-philosophy.md](ideas/agent-behavior-philosophy.md)** -- Ego simulation, behavioral prescription, thermostat-vs-diary
- **[implementation-gaps.md](ideas/implementation-gaps.md)** -- V2+ gaps: voting prompt, footer compliance
- **[team-configuration.md](ideas/team-configuration.md)** -- Multi-team YAML surface, cross-team dynamics, spokesperson rules
- **[mcp-message-broker.md](ideas/mcp-message-broker.md)** -- Cross-team communication backbone, channels, visibility boundaries
- **[research-engine.md](ideas/research-engine.md)** -- External knowledge gathering, claim verification, feasibility checks

---

## Canonical Types

Authoritative Pydantic models at `_SYSTEM/lib/types/`. Code is the spec -- these models validate at runtime and can't drift from reality. New shared concepts (Session, Brief, MorningBrief, Decision, AgentAction) should be defined here, not in markdown.

- **[discussionAgent.py](../../_SYSTEM/lib/types/discussionAgent.py)** -- Canonical Discussion Agent type (UUID identity, 8 personality traits, position, technique, anti-slop, voice, output, actions, workshop metadata)

---

## References

- **[agent-creation-guide.md](references/agent-creation-guide.md)** -- How to create agents: YAML schema, personality design, anti-slop config
- **[discussion-brief-template.md](references/discussion-brief-template.md)** -- Template for discussion session briefs

---

## Archive

Superseded or completed docs kept for history.

- old-prd.md, conversation-system-v1-brief.md, conversation-engine-review.md, discussion-productivity-status.md, documentation-reorg-todo.md
