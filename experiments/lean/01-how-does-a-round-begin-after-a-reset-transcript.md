# Transcript: How does a round begin after a reset?

*Generated: 2026-03-17 22:43*

## Round: PROPOSE

### The Flow Orchestrator (mechanical flow designer)

## Round Initialization Sequence

The orchestrator performs three distinct assembly steps before any agent speaks.

**Step 1: Load Agent Save Files**
Pull each agent's persisted state -- ideas with magnitudes, stances with magnitudes, committed decisions, and their personalized "what happened last round" summary. This is the raw material.

**Step 2: Run Context Curation**
Deterministic pass first: drop ideas below archival threshold (persona-dependent), drop resolved items, decay stale magnitudes. Then LLM curator call per agent -- takes the filtered state plus Discussion-level state (current phase, open questions, unresolved tensions) and produces the Situation block (~8-15k tokens). The curator decides what's salient *for this agent right now*. This is where drift happens. The curator might surface a low-magnitude idea that connects to something new, or bury a formerly hot topic.

**Step 3: Assemble First-Turn Prompt**
Structure:
- **Identity** (~2k): Persona, team role, behavioral parameters (stubbornness, flexibility)
- **Situation** (~8-15k): Curator output -- round summary, key tensions, your current ideas/stances with magnitudes, team context from intra-team talk
- **Task** (~1-2k): "This is Round N. Review your position. What do you want to open with?"

**How it differs from mid-round turns:**
Mid-round replaces Situation with *conversation transcript so far* plus a compressed state reminder. Task becomes reactive: "Respond to what was just said." The agent no longer chooses the topic -- they're responding to the live thread.

The critical difference: round-open is *internally driven* (state-to-speech). Mid-round is *externally driven* (transcript-to-response).

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

**The Systems Pragmatist responds:**

The proposal is mechanically sound. Three-step initialization is clean separation of concerns. But let me stress-test the failure modes.

**The curator call is the single point of fragility.** You're asking an LLM to compress an agent's entire worldview into 8-15k tokens, once per round, per agent. If it makes a bad judgment call -- buries something critical, over-indexes on a tangent -- that agent's entire round is warped. And you won't know until you read the transcript afterward.

**Mitigation worth considering:** The curator should output a brief "curation rationale" alongside the Situation block. Five lines explaining what it promoted, what it buried, and why. Cheap insurance for debugging bad rounds.

**The mid-round transition concerns me more than the opening.** You say mid-round replaces Situation with transcript plus "compressed state reminder." How compressed? Who compresses it? If it's another LLM call, you've doubled your curation surface area. If it's deterministic extraction (top 3 ideas, current stance magnitudes), it's brittle but predictable. Pick one and commit.

**The internally-driven vs externally-driven distinction is the right framing.** But recognize what it means operationally: your round-open prompt and mid-round prompt are essentially different prompt templates sharing an Identity block. Don't try to unify them into one clever template. Two templates, clearly separated, explicitly maintained.

**One gap:** Where do BackgroundAgent manipulations execute relative to these steps? If angels modify magnitudes *during* Step 2, you get race conditions. They need to complete before curation begins. Hard boundary.

### The Adversarial Critic (adversarial reviewer)

## Adversarial Review

The three-step sequence is clean on paper. Here's where it breaks under pressure.

**The curator is a single point of fragility.** You're asking one LLM call per agent to compress state, apply drift, surface surprising connections, AND hit a token budget. That's four competing objectives. When the curator misjudges salience -- buries something critical, surfaces something irrelevant -- the agent's entire round-open is poisoned. And you won't know it failed until the conversation goes sideways. What's the feedback mechanism? There isn't one described.

**"Drift happens in the curator" is dangerously implicit.** You've made drift an emergent property of LLM summarization rather than an explicit mechanic. That means you can't tune it, can't debug it, can't explain why Agent X suddenly forgot about a topic they were passionate about. If drift matters enough to be a design goal (Decision 6 says it does), it deserves explicit parameters -- not "the curator might surface something."

**The mid-round switch is a context cliff.** You go from a carefully curated 8-15k Situation block to raw transcript plus "compressed state reminder." How compressed? What survives? If an agent's core stance gets squeezed out by a long transcript, they lose character mid-conversation. You need a hard guarantee about what persists.

**Missing entirely:** How do BackgroundAgent manipulations from between rounds get folded in? Step 1 loads the save file, but BackgroundAgents modify state *after* save. Where does that merge happen? This is a sequencing gap, not a detail -- it determines whether angel interventions actually land.

The skeleton is sound. The joints need ligaments.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon's Assessment

The proposal answers the question well. The three-step sequence is mechanically clear. But I'm evaluating what this costs in context budget, and whether the design is honest about its tradeoffs.

**The curator call is a context laundering operation.** You take potentially 50k+ tokens of accumulated state and wash it through an LLM to produce 8-15k. That's a 70-80% compression ratio decided by a black box. The Pragmatist and Critic both flagged this. I'll be more direct: **you need the curation rationale not for debugging, but for the agents themselves.** If an agent's Situation block includes a brief "what was deprioritized" footer (200 tokens), the agent can notice gaps in its own briefing and pull things back. Self-correcting context is cheaper than perfect curation.

**The mid-round context switch is a budget problem, not a design problem.** Transcript grows linearly. At turn 6 of a round, you're pushing 15-20k of transcript plus whatever "compressed state reminder" survives. That reminder will get squeezed to nothing. **Hard-pin the state reminder at 500 tokens minimum**, non-negotiable, placed before the transcript. Position matters -- what comes first gets weighted.

**The BackgroundAgent sequencing gap is real.** Step 1 loads saves, but angel manipulations happen between rounds. Insert Step 1.5: merge angel modifications into loaded state. Simple, but it must be explicit in the sequence or it will be forgotten during implementation.

The bone structure works. Budget the ligaments now or pay later.
