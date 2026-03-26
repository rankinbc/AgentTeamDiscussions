# Documentation Index

## V1 Specification (What We Built)

The V1 PRD and supporting specs that define the MVP.

- **[product-brief.md](v1/product-brief.md)** — Core value proposition, problem, solution, how it works
- **[prd.md](v1/prd.md)** — V1 Product Requirements Document (57 FRs, 19 NFRs, 5 user journeys)
- **[v1-orchestrator-spec.md](v1/v1-orchestrator-spec.md)** — V1 technical architecture, session lifecycle, deferred features
- **[v1-spec-gaps.md](v1/v1-spec-gaps.md)** — 7 open implementation questions

### System Overviews
How the system works at a conceptual level. See **[index](v1/system-overview-docs/index.md)** for full map.

- [Conversation Engine](v1/system-overview-docs/conversation-engine-overview.md) — Round structure, phase progression, turn sequencing
- [Creativity Engine](v1/system-overview-docs/creativity-engine-overview.md) — Personality model, anti-slop, voice constraints
- [Discussion Agents](v1/system-overview-docs/discussion-agents-overview.md) — Stateless invocations shaped by config
- [Session Platform](v1/system-overview-docs/session-platform-overview.md) — Persistence, crash recovery, Morning Brief
- [Context Management](v1/system-overview-docs/context-management-overview.md) — Token budgets, 3-layer assembly
- [Evaluation & Improvement](v1/system-overview-docs/evaluation-and-improvement-overview.md) — Review output, feed insights back
- [Agent Workshop](v1/system-overview-docs/agent-workshop-overview.md) — Optional web UI for agent creation/tuning
- [Agent Actions](v1/system-overview-docs/agent-actions-overview.md) — Configurable prompt directives injected into turns
- [Agent Workshop UI Spec](v1/system-overview-docs/agent-workshop-ui-spec.md) — Detailed UI specification

### Conversation Engine Specs
- **[turn-anatomy.md](v1/conversation-engine/turn-anatomy.md)** — Atomic turn structure, two turn types, context layers, output signals
- **[context-assembly-template.md](v1/conversation-engine/context-assembly-template.md)** — Prompt template: 7 sections, 4000-token ceiling, cut priority tiers
- **[morning-brief-format.md](v1/conversation-engine/morning-brief-format.md)** — Output format: RED/YELLOW/GREEN sections, 90-second read

### Creativity Engine Specs
- **[personalities.md](v1/creativity-engine/personalities.md)** — 8-dimension personality model with trait definitions
- **[positions.md](v1/creativity-engine/positions.md)** — 8 stakeholder positions with conflict matrix
- **[techniques.md](v1/creativity-engine/techniques.md)** — 10 agent archetypes with reasoning methods
- **[anti-slop-mechanisms.md](v1/creativity-engine/anti-slop-mechanisms.md)** — 8 LLM failure modes, 10 countermeasures

---

## V2 Roadmap & Ideas

- **[ROADMAP.md](v2/ROADMAP.md)** — Confirmed V2 features, critical path, and idea index
- 13 deferred idea docs in [v2/ideas/](v2/ideas/) — Phase dynamics, moderator input, key takeaways, team config, MCP, and more

---

## Concepts & Design Philosophy

- **[design-principles.md](concepts/design-principles.md)** — Three-layer context model, bias statements, forcing functions
- **[creativity-engine-overview.md](concepts/creativity-engine-overview.md)** — Cross-walk index for creativity engine mechanisms

### Agent Panel Design Explorations
9 design Q&As + 10 raw transcripts from agent discussion panels. See **[agent-panel-index.md](concepts/conversation-engine/agent-panel-index.md)** for navigation.

---

## Research

- **[research-applied.md](research/research-applied.md)** — 10 research domains mapped to 26 mechanisms
- **[MakingAgentsNotActLikeAI.md](research/MakingAgentsNotActLikeAI.md)** — 40+ mechanisms from psychology, improv, game theory
- **[EngineeringRobustMultiAgentLLMDiscussions.md](research/EngineeringRobustMultiAgentLLMDiscussions.md)** — Best practices from AutoGen, CrewAI, LangGraph
- **[RESEARCH-PROMPT.md](research/RESEARCH-PROMPT.md)** — Research agenda for 10 cross-domain areas

---

## References

Generated architecture docs, guides, and data models. See **[references/index.md](references/index.md)** for the full list.

---

## Tech Debt

- **[CONCERNS.md](CONCERNS.md)** — Known technical debt and behavioral issues

---

## Archive

Superseded docs in [archive/](archive/) — old PRD, early briefs, prior reviews.
