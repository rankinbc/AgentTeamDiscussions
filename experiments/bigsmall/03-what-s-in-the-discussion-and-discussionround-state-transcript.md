# Transcript: What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 23:24*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

# Discussion & DiscussionRound State

## Discussion (persists across all rounds)

| Field | Updated By | Context Influence |
|---|---|---|
| `phase` | Phase transition engine on criteria met | Determines task prompt template, available actions |
| `active_ideas[]` | Agent proposals, BackgroundAgent plants, archival sweeps | Curator pulls top-N by magnitude for situation block |
| `committed_decisions[]` | Explicit agent consensus + confidence threshold | Locked into every agent's context as ground truth |
| `open_tensions[]` | Detected when agents hold opposing high-magnitude stances | BackgroundAgents target these for synthesis; curator highlights them |
| `artifact_registry{}` | Artifact production during specify/review phases | Referenced by ID in context, full content fetched on demand |
| `turn_count` | Incremented each cross-team message | Phase transition criteria check against this |

## DiscussionRound (created fresh, destroyed on reset)

| Field | Updated By | Context Influence |
|---|---|---|
| `round_number` | Orchestrator on initialization | Agents know temporal position ("round 4 of brainstorm") |
| `agenda_declarations{}` | Each agent's opening prompt response | Curator weighs agenda items higher in mid-round summaries |
| `momentum_map{}` | Tracks per-idea mention frequency within round | Ideas mentioned repeatedly get magnitude boost at round-end |
| `message_log[]` | Raw append each turn | Mid-round context is just this, unprocessed |
| `drift_events[]` | Random event system fires between rounds | Injected into next round's curation as "things that shifted" |
| `round_summary` | Generated at round close | Feeds into agent save files as "what happened" narrative |

The key asymmetry: Discussion state is the *territory*, DiscussionRound state is the *weather*. Agents navigate both but only the territory persists. The weather shapes what they notice right now. Momentum_map is the sleeper field -- it's how organic discussion energy feeds back into the magnitude system without any angel intervention.

### The Flow Orchestrator (mechanical flow designer)

## Discussion State

| Field | Updated By | Influences Context |
|---|---|---|
| `phase` | Orchestrator (phase transition rules) | Curator uses it to weight what survives -- brainstorm phase keeps more exploratory ideas, specify phase favors converged positions |
| `round_number` | Orchestrator (increment on reset) | Curator uses recency relative to this; agents never see the number directly |
| `committed_decisions[]` | Agents (explicit commits during rounds) | Persist across rounds, included verbatim in situation block until resolved |
| `global_topic_heat{}` | Derived from cross-team message frequency per topic | Curator boosts ideas aligned with hot topics, suppresses cold ones |

## DiscussionRound State

| Field | Updated By | Influences Context |
|---|---|---|
| `turn_count` | Orchestrator (increment per message) | Orchestrator uses it to enforce round length; agents don't see it |
| `active_threads[]` | Created by agent agenda statements, extended by replies | Mid-round messages append to threads; curator references these for next round's situation block |
| `surfaced_disagreements[]` | Detected by orchestrator when agents contradict on same topic | BackgroundAgents consume these to decide where to plant synthesized ideas |
| `round_summary` | Generated at round end (cheap LLM call) | Feeds into each agent's save file narrative; curator uses it as primary input next round |

That's it. Eight fields total across both levels.

Things I cut: mood tracking, per-agent engagement scores, message-level metadata. None of them drive decisions in the initialization sequence from D1. If a BackgroundAgent needs engagement data, it reads message history directly -- we don't pre-compute it into state.

`global_topic_heat` is the only derived field. Everything else is written by exactly one source.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## State Fields: What Actually Needs to Exist at Runtime

Flow Orchestrator's instinct to cut is right. Eight fields is closer to correct than the Cognitive Architect's twelve. But both proposals have problems.

**Discussion State (persistent)**

| Field | Writer | Failure if Missing |
|---|---|---|
| `phase` | Orchestrator | Curator can't select prompt template. Fatal. |
| `committed_decisions[]` | Agent consensus | Agents relitigate settled questions. Wastes rounds. |
| `active_ideas[]` | Agents, BackgroundAgents, archival | Curator has nothing to rank. Fatal. |
| `open_tensions[]` | Derived from opposing stances | BackgroundAgents synthesize blindly. Degrades quality. |

**DiscussionRound State (ephemeral)**

| Field | Writer | Failure if Missing |
|---|---|---|
| `round_number` | Orchestrator | Agents lose temporal grounding. Mild but disorienting. |
| `message_log[]` | Raw append | No conversation. Fatal. |
| `round_summary` | LLM call at close | Save files have no narrative. Breaks reflection. |

That's seven. Here's what I'm cutting and why:

- **`momentum_map`** -- Derived metric with no single writer. Compute it on demand during round-end processing. Don't maintain it as live state.
- **`global_topic_heat`** -- Same problem. Derive it when the curator needs it. Storing derived state means staleness bugs.
- **`agenda_declarations`** -- These are just the first entries in `message_log`. Don't duplicate.
- **`active_threads`** -- Threading is a curator presentation concern, not state. The log is flat.
- **`drift_events`** -- These belong on the Discussion level since they persist into next round's curation. If they're round-scoped they get destroyed before anyone reads them.

Every stored field should have exactly one writer. Derived fields get computed at point of use. That's how you avoid state synchronization bugs at 3am when nobody's watching.

### The Adversarial Critic (adversarial reviewer)

# Adversarial Critique

Two proposals, one bloated, one lean. The Flow Orchestrator's eight-field model is closer to correct. Here's why the Cognitive Architect's version has problems:

**`active_ideas[]` doesn't belong on Discussion.** Ideas live on *agents*, not on the discussion. Each agent's save file holds their ideas with magnitudes. The Discussion doesn't need a redundant global registry -- the curator already pulls from agent state during step 4 of D1. Duplicating it creates a sync problem: whose magnitude wins when agent state and Discussion state disagree?

**`open_tensions[]` is derived, not stored.** You detect tensions by comparing agent stances. Storing them separately means something has to keep them current. What invalidates a tension? When does it get removed? You've created a cache without a cache invalidation strategy.

**`momentum_map{}` is `global_topic_heat{}` with a worse name.** Both track mention frequency feeding back into magnitudes. Pick one. The Orchestrator's version is cleaner because it's explicitly derived and owned by one source.

**`drift_events[]` on DiscussionRound is wrong placement.** Drift events fire *between* rounds per D1. They feed into the *next* round's curation. Storing them on the round they affect means writing to a DiscussionRound that doesn't exist yet when the events fire. Put them on Discussion or generate them transiently during step 2.

**What I'd actually ship:** The Orchestrator's eight fields, plus `artifact_registry{}` from the Architect (that one's real -- artifacts need tracking). Nine fields. Everything else is either derived on demand or already lives in agent save files.

Stop modeling data you can compute.

## Round: EVALUATE

### The Product Oracle (user advocate)

# The Product Oracle's Take

The Pragmatist and Critic converged on the right answer. Let me frame it through the lens of what job each field does.

## Discussion State (the territory)

| Field | Job It Does |
|---|---|
| `phase` | Tells the system what kind of conversation we're having right now |
| `committed_decisions[]` | Prevents agents from relitigating what's settled -- respects the user's time |
| `active_ideas[]` | **Lives on agents, not here.** Critic is right. The curator reads agent save files directly. No global registry. |
| `artifact_registry{}` | Lets agents reference specs by ID without stuffing full documents into context |

## DiscussionRound State (the weather)

| Field | Job It Does |
|---|---|
| `round_number` | Grounds agents temporally -- "we're in round 4, time to converge" |
| `message_log[]` | The conversation itself. Non-negotiable. |
| `round_summary` | Feeds the save file narrative that makes next round's reflection meaningful |

That's **seven fields**. Four persistent, three ephemeral.

I'm siding with the Critic on dropping `open_tensions[]`. Tensions are what BackgroundAgents *discover* by reading history, not what we pre-compute for them. Pre-computing it is doing their job for them and doing it worse.

The field nobody's fighting about matters most: `committed_decisions[]`. That's what makes overnight runs produce *outcomes* instead of circular debates. Every decision locked in is one fewer thing burning context budget next round. Decisions are how the system makes progress while the user sleeps.

Derive everything you can. Store only what you'd lose.

### The Context Surgeon (context efficiency evaluator)

# Context Surgeon's Cut

The debate converged. Here's what survives my analysis.

## Discussion State (persistent)

| Field | Writer | Context Role |
|---|---|---|
| `phase` | Orchestrator | Selects prompt template and curator strategy |
| `committed_decisions[]` | Agent consensus | Injected verbatim into every situation block |
| `artifact_registry{}` | Spec/review phase production | Referenced by ID; full content fetched on demand only |

Three fields. That's it. Ideas and stances live on **agent save files**, not here. The Adversarial Critic caught the sync problem -- duplicating them onto Discussion creates two sources of truth. The curator already reads agent state during D1 step 4.

`open_tensions` and `topic_heat` are derived at point of use. Storing them means maintaining cache invalidation logic that runs unattended. No.

## DiscussionRound State (ephemeral)

| Field | Writer | Context Role |
|---|---|---|
| `round_number` | Orchestrator | Temporal grounding in situation block |
| `message_log[]` | Raw append per turn | IS the mid-round context (per D3) |
| `round_summary` | LLM call at round close | Feeds agent save file narratives |
| `drift_events[]` | Random system, written to Discussion, consumed during next round's curation | Injected as "things that shifted" |

Wait -- `drift_events` fires between rounds. It belongs on **Discussion**, consumed transiently during D1 step 4, then cleared. Not round state. Moving it.

**Final count: 3 persistent, 3 ephemeral. Six fields.**

Every field has one writer. Nothing is derived. Nothing duplicates agent state. Every token of context budget spent on these fields earns its keep.
