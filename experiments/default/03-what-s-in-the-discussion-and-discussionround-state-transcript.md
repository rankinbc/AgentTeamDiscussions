# Transcript: What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 22:34*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

Good question. These are the containers everything else floats in.

---

## Discussion State

Persistent across all rounds.

| Field | Updated By | Agents See It? |
|---|---|---|
| `phase` (brainstorm/refine/specify/review) | Orchestrator via transition criteria | Yes -- gates what actions feel appropriate |
| `committed_decisions[]` | Agents via explicit commit action | Yes -- these are settled, stop relitigating |
| `active_tensions[]` (named disagreements, participating agents) | Orchestrator extracts from transcript | Yes -- curated into situation context |
| `artifact_registry[]` (specs, PRDs produced) | MCP server on artifact creation | Referenced by ID, not inlined |
| `round_count` | Orchestrator increments | Yes -- agents know how deep they are |
| `entropy` (0-1 float, how stale the conversation feels) | Orchestrator computes from magnitude variance across agents | No -- but drives BackgroundAgent activation thresholds |

## DiscussionRound State

Lives and dies within one round.

| Field | Updated By | Agents See It? |
|---|---|---|
| `turn_number` | Orchestrator increments | Yes |
| `speaker_order[]` | Orchestrator (rotation with priority bumps) | Current speaker only |
| `hot_topics[]` (ideas with highest aggregate magnitude this round) | Recalculated after each turn from agent states | Yes -- curated summary, not raw numbers |
| `momentum` (which direction the room is leaning) | Orchestrator sentiment extraction post-turn | Indirectly -- shapes curator's summary |
| `round_goals[]` (what this round should accomplish) | Seeded from phase criteria + prior round gaps | Yes -- task context |

---

The key insight: `entropy` and `momentum` are invisible levers. Agents never see the numbers, but those numbers decide when BackgroundAgents intervene and how aggressively the curator prunes. The room steers itself.

### The Flow Orchestrator (mechanical flow designer)

---

# Discussion and DiscussionRound State Fields

## Discussion (persists across rounds)

| Field | Type | Updated By | Flows Into Agent Context |
|---|---|---|---|
| `phase` | enum (brainstorm/refine/specify/review) | Orchestrator on transition criteria met | Included in Situation block; gates what agents are *asked* to do |
| `active_decisions` | list of {id, description, status, confidence} | Agents committing positions; orchestrator marking resolved | Curated into Situation; agents see what's decided vs. open |
| `unresolved_tensions` | list of {id, parties, description, magnitude} | Orchestrator extracts from transcript when agents disagree | Fed to BackgroundAgents for synthesis; surfaced to agents if magnitude stays high |
| `artifact_registry` | list of {id, type, version, phase_created} | Agents producing specs/PRDs; orchestrator versioning | Agents see artifact *existence and version*, not full content unless requested |
| `round_count` | int | Orchestrator increments | Used in decay calculations and phase transition rules |

## DiscussionRound (created fresh, destroyed on reset)

| Field | Type | Updated By | Flows Into Agent Context |
|---|---|---|---|
| `turn_order` | list of agent_ids | Orchestrator sets at round-open | Agents know who speaks next (prevents cross-talk) |
| `turn_count` | int | Orchestrator increments per turn | Caps round length; triggers wind-down prompts |
| `heat_map` | dict {topic_id: float} | Orchestrator tallies from transcript mentions + magnitude | Curator uses this to weight Situation block -- hot topics get more tokens |
| `surfaced_ideas` | set of idea_ids | Marked when agent first mentions an idea this round | Prevents re-introduction spam; curator can deprioritize already-surfaced items |
| `round_goal` | string | Orchestrator derives from phase + Discussion state | Injected into Task block. This is *the specific question* the round should advance. |

Key dependency: `heat_map` feeds the context curator. Without it, the curator has no signal for what matters *this round* versus historically.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

Two solid proposals. Let me stress-test the gaps.

**Where I agree:** The split is right. Discussion persists, DiscussionRound doesn't. Both proposals nail that.

**Where I'm skeptical:**

`entropy` and `momentum` as invisible levers sound elegant. But who validates them? Orchestrator "sentiment extraction" and "magnitude variance" are hand-wavy. These are computed fields driving critical behavior (BackgroundAgent activation, curator aggressiveness). If the computation is wrong, the whole room drifts silently. No agent can report "something feels off" because they can't see the inputs.

**Failure mode I want addressed:** `surfaced_ideas` tracking. Good idea, but what's the scope? If Agent A mentions idea #42 obliquely versus building an argument around it, do both count? Binary "surfaced" is too coarse. Make it a count or weight, or the curator suppresses ideas that were mentioned but never actually discussed.

**What I'd merge from both proposals:**

- Take Flow Orchestrator's `active_decisions` over Cognitive Architect's `committed_decisions`. Decisions have lifecycle (proposed/debated/committed/reopened). A flat list of "committed" ones loses the pipeline.
- Take Cognitive Architect's `entropy` concept but make it a **logged diagnostic**, not a silent driver. Log it, let BackgroundAgents read it, but don't hide the steering from debugging.
- `heat_map` and `hot_topics` are the same thing with different names. Pick one. I prefer `heat_map` -- it's a data structure, not a summary.

**Missing from both:** No field tracks *failed* ideas -- things that were raised and explicitly shot down. Without that, BackgroundAgents might replant ideas the room already rejected. You need a `rejected_ideas` list with round number and reason, or you'll get zombie ideas.

### The Adversarial Critic (adversarial reviewer)

Both proposals converge on the right skeleton but dodge the hard questions.

**`entropy` is a vanity metric.** Cognitive Architect defines it as "magnitude variance across agents" -- that's one possible formula, not a spec. What's the window? Variance of what magnitudes? All ideas? Only active ones? A single outlier agent with one high-magnitude pet idea skews this number. You'll tune it forever and never trust it.

**`momentum` is worse.** "Orchestrator sentiment extraction post-turn" means an LLM call per turn to produce a float nobody sees directly. That's expensive instrumentation with no defined consumer besides "shapes curator's summary." If the curator is already an LLM call, you're spending one LLM call to produce a number that nudges another LLM call. Just give the curator the transcript.

**`heat_map` vs `hot_topics` -- pick one.** Flow Orchestrator's `heat_map` is strictly more useful than Cognitive Architect's `hot_topics` because it's per-topic rather than a ranked list. But neither proposal specifies the aggregation function. "Transcript mentions + magnitude" is hand-waving.

**`surfaced_ideas` is genuinely good.** It's the only field here that solves a concrete failure mode (re-introduction spam). Keep it.

**What's actually missing:** Neither proposal includes a `stalled_turns` counter -- how many consecutive turns produced no magnitude changes or new ideas. That's your real staleness signal, not `entropy`. It's observable, cheap, and directly actionable.

Stop inventing atmospheric floats. Count things that happened.

## Round: EVALUATE

### The Product Oracle (user advocate)

The room's converging. Let me cut to what matters from the user's seat.

**The agents are the users here.** Every field exists to help them do one job: *make better contributions next turn*. If a field doesn't change what an agent says, kill it.

**My take on the open disputes:**

**Drop `momentum`. Keep `entropy` as diagnostics only.** The Critic is right -- spending an LLM call to produce a float that nudges another LLM call is laundering intuition through math. The curator already reads the transcript. Let it do its job. But `entropy` as a *logged diagnostic* (Pragmatist's suggestion) earns its keep for debugging and post-session analysis. Just don't let it silently steer.

**`stalled_turns` over `entropy` for activation triggers.** The Critic nailed this. "Three turns, nothing moved" is a signal you can act on. "Variance decreased by 0.15" is a signal you'll argue about.

**`rejected_ideas` is non-negotiable.** This is the zombie idea prevention the Pragmatist flagged. Without it, BackgroundAgents replant what the room already killed. That's the fastest way to make agents feel like they're not being heard -- and agents that feel unheard produce worse output.

**`active_decisions` with lifecycle beats `committed_decisions`.** Decisions aren't binary. They're proposed, debated, committed, occasionally reopened. The pipeline matters because it tells agents *where to put their energy*.

**`surfaced_ideas` should be weighted, not binary.** A passing mention isn't a discussion. Count references or track depth. The curator needs that granularity.

Ship `heat_map`, not `hot_topics`. Data structures beat summaries.

### The Context Surgeon (context efficiency evaluator)

**EVALUATE — The Context Surgeon**

---

The discussion has converged. Here's what survives scrutiny.

**Discussion State (persists across rounds):**

| Field | Type | Updates | Context Role |
|---|---|---|---|
| `phase` | enum | Orchestrator on transition criteria | Situation block; gates agent behavior |
| `active_decisions` | list {id, status, confidence} | Agents commit; orchestrator resolves | Curated into Situation; shows decided vs. open |
| `unresolved_tensions` | list {id, parties, magnitude} | Orchestrator extracts from transcript | Fed to BackgroundAgents; surfaced if persistent |
| `artifact_registry` | list {id, type, version} | MCP server on creation | Agents see existence, not content |
| `round_count` | int | Orchestrator increments | Decay calculations, phase transitions |
| `rejected_ideas` | list {id, round, reason} | Orchestrator logs on explicit rejection | Prevents BackgroundAgents replanting dead ideas |

**DiscussionRound State (created fresh each round):**

| Field | Type | Updates | Context Role |
|---|---|---|---|
| `turn_order` | list of agent_ids | Orchestrator at round-open | Agents know speaking sequence |
| `turn_count` | int | Orchestrator per turn | Caps length; triggers wind-down |
| `heat_map` | dict {topic_id: float} | Aggregated from mentions + magnitudes | Drives curator token allocation |
| `surfaced_ideas` | dict {idea_id: int} | Incremented on substantive mention | Weighted count, not binary — prevents premature suppression |
| `round_goal` | string | Derived from phase + Discussion gaps | Injected into Task block |
| `stalled_turns` | int | Incremented when no magnitude changes occur | Direct staleness signal; triggers BackgroundAgent intervention |

**What's cut:** `entropy` (underspecified formula, untestable), `momentum` (LLM call producing a float that nudges another LLM call — pay twice for ambiguity). Replace both with `stalled_turns`: observable, cheap, actionable.

**Key ruling on `surfaced_ideas`:** weighted count, not binary. Oblique mention scores lower than sustained argument. Curator uses this to avoid suppressing under-discussed ideas.
