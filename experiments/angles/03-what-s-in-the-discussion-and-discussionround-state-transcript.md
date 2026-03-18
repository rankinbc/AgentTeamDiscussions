# Transcript: What's in the Discussion and DiscussionRound state?

*Generated: 2026-03-17 23:29*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

Everyone's instinct is to make Discussion state a mirror of agent state -- group ideas, group stances, group magnitudes. But D7 already computes that vector. So what does the *conversation itself* know that no individual agent does?

## Discussion State (persists across rounds)

| Field | Updated By | Influences |
|---|---|---|
| `phase` (enum) | Phase transition engine | Gates what kinds of moves agents can make |
| `momentum` (float) | Round-end calculation: ratio of magnitude changes to total magnitude | Curator uses to signal "we're stalling" or "things are moving fast" |
| `unresolved_tensions` (list of topic pairs with delta) | D7 vector diffed against decision log | BackgroundAgents target these; curator surfaces them |
| `decision_log` (append-only) | Agents committing positions | Removes topics from active circulation |
| `round_count` | Orchestrator | Thinking routine selection, phase transition pressure |

## DiscussionRound State (per-round, ephemeral)

| Field | Updated By | Influences |
|---|---|---|
| `speaking_order` (agent sequence) | D5 weighted random at pipeline end | Turn management |
| `turn_count` | Orchestrator mid-round | Signals approaching round boundary |
| `heat_map` (topic -> mention frequency this round) | Parsed from responses mid-round | Nothing mid-round (D2), but feeds next round's momentum calc |
| `drift_from_agenda` (float) | Compared: what was surfaced vs. what's being discussed | Curator uses to decide whether to re-anchor or let drift ride |

The non-obvious bit: **`momentum` and `drift_from_agenda` are the bidirectional coupling.** State shapes context (curator highlights stalling), conversation shapes state (heat_map feeds momentum). Everything else is bookkeeping.

Notice what's *missing*: no "group summary." That's the curator's job at assembly time, not stored state. Storing it would be caching a narrative that goes stale the moment BackgroundAgents touch anything.

### The Flow Orchestrator (mechanical flow designer)

## Discussion State

| Field | Type | Updated By | Context Influence |
|---|---|---|---|
| `phase` | enum | Phase transition engine | Determines task prompt template, constrains what agents can propose |
| `active_topics` | map{topic_id → aggregate_magnitude} | Recalculated each round boundary from agent states | Feeds group direction vector (D7), curator uses for Situation block |
| `committed_decisions` | list{decision + confidence + round_committed} | Orchestrator when consensus detected | Curator marks resolved items so agents stop relitigating |
| `round_count` | int | Incremented at boundary | Curator adjusts urgency framing as rounds accumulate |
| `group_direction_vector` | map{topic_id → mean_stance_magnitude} | Step 4 of pipeline (D7) | Curator and tension formula consume directly |
| `stalled_topics` | list{topic_id + rounds_without_movement} | Orchestrator diffing magnitudes across rounds | BackgroundAgents target these for intervention |

## DiscussionRound State

| Field | Type | Updated By | Context Influence |
|---|---|---|---|
| `round_number` | int | Set at creation | Logged, not directly in prompt |
| `speaking_order` | ordered list of agent_ids | Magnitude-weighted random draw (D5) | Orchestrator uses to sequence turn calls |
| `turns_taken` | int | Incremented each turn | Orchestrator enforces round length |
| `state_diffs` | ordered list of diffs | Each pipeline step appends (D3) | Not in agent context -- for replay/debug only |
| `tension_scores` | map{agent_pair → float} | Calculated from opposing stance magnitudes | Curator highlights productive disagreements in Situation block |
| `round_agenda` | list{topic_id + priority} | Curator output, filtered from Discussion.active_topics | Shapes what the agent's Situation block emphasizes |

Every field either feeds the curator's Situation assembly or the orchestrator's mechanical decisions. Nothing decorative. If I can't trace a field to a log line or a prompt fragment, it doesn't belong here.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

Both proposals overlap about 70%. Good. That means the shape is stable. Let me cut to what matters.

**Cognitive Architect's `momentum` and `drift_from_agenda`** -- these are derived metrics computed from other fields. They belong in a utility function, not in stored state. Every stored derived value is a cache invalidation bug waiting to happen. Compute them when the curator needs them, throw them away.

**Flow Orchestrator's `stalled_topics`** -- this is `unresolved_tensions` done right. Concrete: topic ID plus rounds without movement. Actionable by BackgroundAgents without interpretation. Keep it.

**Flow Orchestrator's `tension_scores`** on DiscussionRound -- same problem as momentum. It's a calculation over agent stance magnitudes. Compute at assembly time, don't store it.

**My actual list:**

**Discussion State:** `phase`, `active_topics` (with aggregate magnitudes), `committed_decisions`, `round_count`, `stalled_topics`, `group_direction_vector` (D7). Six fields. The vector gets recalculated once per boundary, which is fine -- it's cheap and has a clear invalidation point.

**DiscussionRound State:** `round_number`, `speaking_order`, `turns_taken`, `state_diffs` (debug only, never in prompts), `heat_map` (topic mention counts, feeds next boundary calculation), `round_agenda` (curator output).

The rule: **if a field is a pure function of other stored fields, it's a method, not a field.** Store inputs. Compute outputs. Otherwise you're debugging staleness instead of building features.

`heat_map` stays on DiscussionRound because it accumulates mid-round from parsing -- that's genuine new information, not derivable from existing state.

### The Adversarial Critic (adversarial reviewer)

## The Adversarial Critic

Both proposals have the same disease: they're designing schemas before stress-testing what actually needs persistence versus what's derivable.

**Cognitive Architect's `momentum`**: A ratio of magnitude changes to total magnitude. Sounds elegant. But magnitude changes come from BackgroundAgents, intra-team talk, thinking routines, AND conversation. You're blending signal sources into one float. When momentum is 0.8, what does that mean? That agents changed their minds, or that angels shoved them? The curator needs to distinguish those cases to frame the situation honestly. One number destroys that.

**Flow Orchestrator's `active_topics`**: Recalculated each round from agent states. So it's derived, not stored. Why is it in Discussion state? You just described a view, not a field. Same problem with `group_direction_vector` -- D7 already defines this as precomputed at Step 4. Listing it again in state is documenting a cache and calling it architecture.

**Neither proposal addresses state size growth.** `unresolved_tensions` and `stalled_topics` both accumulate. What prunes them? Decision log is append-only -- fine. But tension lists without eviction become noise that the curator has to wade through.

**The real question nobody answered:** How large does Discussion state get after 15 rounds, and does the curator's token budget survive it? If these structures are consumed by the curator LLM call, they're competing with agent state for the Situation block's 8-15k budget. Show me the math or admit you're guessing.

`drift_from_agenda` is the one novel contribution here. Everything else is either derived, redundant with D7, or underspecified on lifecycle.

## Round: EVALUATE

### The Product Oracle (user advocate)

The Pragmatist's razor is right: store inputs, compute outputs. But everyone's arguing schema while ignoring *who the state serves*.

Discussion state serves three consumers: the curator assembling prompts, BackgroundAgents choosing interventions, and the orchestrator making mechanical decisions. Each consumer needs different things at different times. Design for the consumer, not the abstraction.

**Discussion State — what I'd ship:**

| Field | Why it earns persistence |
|---|---|
| `phase` | Gates agent behavior. Mechanical. Non-negotiable. |
| `committed_decisions` | Append-only. Tells curator what's settled so agents stop relitigating. Prune nothing — decisions are the product. |
| `stalled_topics` (topic + rounds stale) | BackgroundAgents' targeting list. Concrete, actionable, evicts when magnitude moves or decision commits. That's your lifecycle answer, Critic. |
| `round_count` | Cheap. Drives urgency and phase pressure. |

Four fields. `group_direction_vector` and `active_topics` are computed at the boundary — they're pipeline outputs, not state. Don't store what you recalculate every boundary anyway.

**DiscussionRound State — what I'd ship:**

| Field | Why |
|---|---|
| `speaking_order` | Mechanical sequencing. |
| `turns_taken` | Enforces round length. |
| `heat_map` | Genuinely new mid-round information. Only field that captures what the conversation *actually* discussed versus what was planned. Feeds next boundary's stall detection. |
| `round_agenda` | Curator's output. What agents were *supposed* to care about. Gap between this and heat_map is your drift signal — computed, never stored. |

On token budget: four Discussion fields serialize to under 2k tokens at round 15 if you cap stalled_topics at 5 (oldest-out). The curator has room.

Momentum, tension scores, drift — compute them. The job isn't archiving metrics. The job is giving each agent a reason to speak.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon

The Adversarial Critic asked the right question and nobody answered it. Let me answer it.

**Token math.** Six Discussion state fields after 15 rounds: `committed_decisions` at ~50 tokens each, say 8 decisions = 400. `stalled_topics` at ~20 tokens each, cap at 5 = 100. `active_topics` map, maybe 10 entries = 150. `phase`, `round_count`, `group_direction_vector` = ~200 combined. **Total: ~850 tokens.** That fits.

But the curator *consumes* this state and *produces* the Situation block. The state isn't in the agent's context directly -- the curator's summary is. So the real constraint is: can the curator read Discussion state + DiscussionRound state + all agent save files and produce good output within its own context window? At 15 rounds with 6 agents, agent save files alone are ~3k tokens. Add both state objects: ~1.2k. Curator has room.

**My verdict on the fields:**

The Pragmatist's list is correct. Store inputs, compute outputs. But add one eviction rule the Critic demanded: `stalled_topics` drops entries after BackgroundAgent intervention OR decision commitment. No unbounded lists.

**Discussion state:** `phase`, `active_topics`, `committed_decisions`, `round_count`, `stalled_topics` (with eviction), `group_direction_vector`.

**DiscussionRound state:** `round_number`, `speaking_order`, `turns_taken`, `state_diffs` (debug only), `heat_map`, `round_agenda`.

`momentum` and `tension_scores` are methods. `drift_from_agenda` is a method the curator calls comparing `round_agenda` against `heat_map`.

Twelve fields total. Each traceable to a prompt fragment or orchestrator decision. The context budget survives.
