# V2 Roadmap

## Confirmed V2 Features (from PRD Growth Section)

These are the features explicitly scoped as post-MVP growth:

1. **Phase System** — Brainstorm → Refine → Specify → Review with automatic transitions
2. **Moderator Input** — Live steering via HTTP during discussions
3. **Dynamic Turn Ordering** — Rebuttal priority / urgency meter
4. **Key Takeaway Mechanism** — Convergence detection and voting
5. **Evaluation Engine** — Rubric scoring against design doc quality dimensions
6. **Multiple Output Artifact Types** — PRD, architecture doc, user stories
7. **Research Engine** — External data gathering during discussions

## Critical Path (from Agent Panel Analysis)

Recommended build order based on dependency analysis and user value:

1. **Blind Proposals** (1-2 days) — Suppress prior context in propose phase. Highest immediate user value.
2. **Manifest Versioning** (0.5 day) — Co-deliver with blind proposals for schema evolution.
3. **Phase System** (2-3 days) — Metadata labeling, phase-specific prompt injection, transition logic. Foundational infrastructure for most V2 features.
4. **Key Takeaways** (1 day) — Extraction at phase boundaries.
5. **Stale Detection** (2 days) — Compare outputs across phase boundaries for repetition signals.
6. **Anti-Sycophancy Detection** (2 days) — Measure blind vs revealed position drift (measurement only).
7. **BIT System** (parallel track) — Personality dimensions, measurable independently.

Key insight: Start with blind proposals (changes what user reads immediately) rather than phases (invisible infrastructure). Phases enable blind proposals to be cleaner, but blind proposals work without phases.

## Vision (Post-V2)

- **Team Configuration Layer** — Multi-team with spokesperson/internal deliberation
- **MCP Message Broker** — Cross-team communication channel
- **Full Magnitude System** — Ideas/stances tracking and BackgroundAgents
- **Intra-team Deliberation** — Between rounds
- **Context Management** — Prior sessions, RAG, research findings
- **Web UI** — Session monitoring and artifact browsing
- **Agent Library** — Sharable team configurations

## Idea Index

| Idea | Summary | Scope |
|------|---------|-------|
| [entity-model.md](ideas/entity-model.md) | Magnitude-based ideas/stances, BackgroundAgents, complex entity persistence | Vision |
| [orchestrator-event-cadence.md](ideas/orchestrator-event-cadence.md) | Per-turn convergence detection and event-driven orchestration | V2 |
| [key-takeaway-mechanism.md](ideas/key-takeaway-mechanism.md) | Convergence voting system for extracting key insights | V2 |
| [rebuttal-priority.md](ideas/rebuttal-priority.md) | Dynamic turn ordering based on conversation content | V2 |
| [moderator-input.md](ideas/moderator-input.md) | Live steering via HTTP during discussions | V2 |
| [phase-dynamics.md](ideas/phase-dynamics.md) | Per-phase personality weighting in creativity engine | V2 |
| [session-platform.md](ideas/session-platform.md) | Agent library, session-as-package, management layer | Vision |
| [research-scope-controls.md](ideas/research-scope-controls.md) | 4-layer research cost control for external data gathering | V2 |
| [agent-behavior-philosophy.md](ideas/agent-behavior-philosophy.md) | Ego simulation, behavioral prescription mechanisms | V2 |
| [implementation-gaps.md](ideas/implementation-gaps.md) | V2+ gaps identified during spec review | V2 |
| [team-configuration.md](ideas/team-configuration.md) | Multi-team YAML surface with spokesperson/deliberation | Vision |
| [mcp-message-broker.md](ideas/mcp-message-broker.md) | Cross-team communication backbone via MCP | Vision |
| [research-engine.md](ideas/research-engine.md) | External knowledge gathering during discussions | V2 |
| [agent-identity-and-resolution.md](ideas/agent-identity-and-resolution.md) | GUID-based agent identity, multi-source resolution, session snapshots | V2 |

## Open Questions (from V1 Spec Gaps Relevant to V2)

- How should phase transitions be triggered? (time-based, convergence-based, round-count?)
- How does the evaluation engine feed back into agent behavior for subsequent sessions?
- What's the boundary between moderator input and phase system auto-transitions?
- How do research engine results integrate into the context assembly pipeline?
