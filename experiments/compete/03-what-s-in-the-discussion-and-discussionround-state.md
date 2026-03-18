# What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 23:20 | Question 3 | 127s | Mode: compete*

## Decisions

### D1: Canonical Magnitude Lives on Agent Save Files

Discussion state does not store idea magnitudes. Each agent owns their conviction about each idea as a magnitude value in their save file. When any system component needs "room-level magnitude" (e.g., what the room cares about most), it computes it at read time by querying across agent save files -- average, max, or weighted by persona authority. One source of truth, zero desync risk.

Discussion state tracks ideas as concepts only: text, origin, and ID. The scoreboard is distributed across agents. The catalog is centralized.

### D2: Discussion State Has Four Fields

Discussion state persists across all rounds for the lifetime of the session.

| Field | Type | Updated By | Influences |
|-------|------|------------|------------|
| `phase` | enum | Orchestrator, when transition criteria are met | Task directive template selection; constrains allowed agent actions per phase |
| `idea_registry` | list of {id, text, origin_agent, round_introduced} | Agent utterances (new ideas surface here), BackgroundAgent plants | Curator knows what ideas exist; agent save files reference these IDs for their magnitude entries |
| `decisions` | list of {id, text, confidence, round_committed} | Consensus detection at round-end, when opposing agents converge on the same position | Curator's deterministic filter drops resolved decisions from future context; written to session output |
| `round_count` | int | Orchestrator increments at round boundary | Staleness calculation for idea decay; phase transition evaluation |

No tension maps. No momentum deltas. No artifact version tracking. Those are queries the curator runs during context assembly, not fields that get persisted and maintained. Storing derived values creates two sources of truth and desync bugs.

### D3: DiscussionRound State Has Four Fields

DiscussionRound state is created at round-start and destroyed after round-end extraction. It exists only for the duration of one round.

| Field | Type | Updated By | Influences |
|-------|------|------------|------------|
| `round_id` | int | Orchestrator at round creation | Links messages to round in transcript; used for save-file summary attribution |
| `turn_order` | list of agent_ids | Orchestrator (randomized or phase-dependent) | Determines who speaks when during the round |
| `messages` | ordered list of {agent_id, content, timestamp} | Each agent utterance appends | Mid-round prompts pull recent messages for reactive context; round-end processing uses full list for save-file summary generation |
| `pending_state_updates` | list of {target_agent_id, update_type, payload} | BackgroundAgents (magnitude bumps, idea plants, stance shifts), intra-team talk (magnitude adjustments from teammate reactions) | Buffered changes applied to agent save files at round boundary -- never mid-round |

The pending updates buffer is the critical coherence mechanism. BackgroundAgents and intra-team talk produce state changes that must not leak into the active round. Agents mid-conversation see stable ground. An angel bumping an idea's magnitude mid-round would cause a priority shift the agent didn't cause and can't explain. The buffer prevents this.

### D4: Round Boundary Application Order

The round boundary executes three operations in strict sequence. Ordering matters because save-file summaries and magnitude values serve different purposes.

1. **Generate save-file summaries.** The orchestrator produces each agent's 3-5 sentence personalized summary of "what happened this round from your perspective." This summary reflects what the agent actually experienced -- the exchanges they participated in, the positions they took. It does not reflect BackgroundAgent interventions or intra-team magnitude shifts that happened behind the scenes.

2. **Apply pending state updates.** All buffered changes from `pending_state_updates` are written to agent save files. Magnitude bumps from BackgroundAgents, planted ideas, stance shifts from intra-team talk -- all applied now. This updates the numeric state (magnitudes, stances) without revising the narrative state (summary).

3. **Extract and destroy DiscussionRound.** Commit messages to session transcript. Update Discussion-level fields (decisions if consensus detected, idea_registry if new ideas surfaced, round_count increment). Then discard the DiscussionRound object.

**Rationale for this ordering:** The summary captures subjective experience. The magnitudes capture objective state including invisible interventions. An agent enters the next round with a summary that honestly reflects what they lived through, but magnitudes that incorporate everything -- including what angels did after the fact. The agent notices the gap organically: "I remember arguing against X, but I find myself less opposed now." This is the drift mechanic working as designed.

### D5: Derived Metrics Are Queries, Not State

The following are explicitly not persisted. They are computed at read time by the curator or orchestrator when needed.

| Metric | Computation | Consumer |
|--------|-------------|----------|
| Tension | Compare magnitudes for the same idea across agents on opposing teams | BackgroundAgent targeting; curator highlights in situation block |
| Momentum | Diff current magnitudes against previous round's save-file snapshot | Curator highlights rising/falling topics; dream events target stale ideas |
| Heat | Count exchanges per topic in DiscussionRound.messages | Intra-team talk prioritizes hot topics |
| Emerging consensus | Detect when opposing agents' magnitudes converge on the same idea | Orchestrator evaluates phase transition acceleration |
| Deadlocks | Detect when magnitude gap on an idea persists across 3+ exchanges without movement | BackgroundAgent trigger for idea-planting interventions |
| Agenda seeds | Sort active ideas by magnitude at round-start | Curator uses as input for "what the room cares about" in situation block |

Each of these reduces to "compare magnitudes across agents and time." One underlying signal, queried different ways. Persisting them creates maintenance surface area for marginal information gain and steals context budget from agent thinking.

### D6: Idea Registry Is the Catalog, Agent Save Files Are the Scoreboard

The relationship between Discussion.idea_registry and agent save files must be unambiguous.

- `idea_registry` is the global catalog of ideas that exist in the discussion. It stores identity (id, text, origin) and lifecycle metadata (round_introduced). It does not store any agent's opinion about the idea.

- Agent save files store per-agent idea entries referencing registry IDs, each with their own magnitude. Two agents can hold the same idea at different magnitudes. This is correct and expected -- it represents genuine disagreement.

- When a BackgroundAgent plants an idea, two writes occur: one to the idea_registry (new catalog entry) and one to the target agent's pending_state_updates (the agent will "have" this idea next round with an initial magnitude).

- When an agent surfaces a new idea during discussion, the orchestrator registers it in idea_registry and adds it to the speaking agent's save file. Other agents may adopt it during the round -- their save files get updated at round boundary via pending_state_updates if intra-team talk endorses it, or they explicitly engage with it in exchanges.

### D7: What Agents Never See

Agents never see raw state objects. They see what the curator assembles into their situation block. Specifically:

- Agents never see `pending_state_updates`. Changes arrive as updated magnitudes in their save file next round.
- Agents never see other agents' save files. Cross-team knowledge comes only through exchanges in the discussion.
- Agents never see Discussion.idea_registry directly. The curator selects which ideas to surface based on magnitude queries and phase relevance.
- Agents never see their own save file mid-round. It is a round-boundary artifact only, loaded at round-start and written at round-end. Leaking it mid-round wastes tokens and invites recalculation instead of commitment.
- Agents never see computed metrics (tension, momentum, heat). The curator may use these to decide what to include in the situation block, but the agent receives narrative context, not dashboards.

### D8: Bidirectional Flow Pattern

Discussion state flows **down** through the curator into agent situation blocks. The curator queries Discussion fields and agent save files, then compresses the result into the situation block that agents receive.

DiscussionRound state flows **sideways** into mid-round prompts (recent messages become the reactive context for the next speaker) and **up** into save-file generation and BackgroundAgent triggers at round-end.

Agent utterances flow **into** DiscussionRound.messages during the round, and their effects propagate to Discussion state and agent save files at the round boundary. The round boundary is the only point where state crosses levels.