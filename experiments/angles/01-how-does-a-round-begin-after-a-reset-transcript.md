# Transcript: How does a round begin after a reset?

*Generated: 2026-03-17 23:26*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Round Start: The Anti-Briefing

Everyone's instinct is to build a briefing packet. "Here's what happened, here's the agenda, go." That's a meeting -- and meetings produce meeting-shaped output. Predictable, comprehensive, dead.

**The orchestrator should assemble the prompt backward -- from urgency, not from summary.**

### What gets assembled:

1. **Agent save file** -- their ideas/stances with current magnitudes, decisions committed to, their subjective 3-5 sentence recap. This is identity-adjacent. It's *their* truth.

2. **Curated situation** -- the hybrid filter runs here. Deterministic pass drops resolved decisions and decayed ideas. LLM curator then does something critical: it doesn't summarize neutrally. It summarizes *for this agent*, emphasizing what should feel unfinished to them given their persona and high-magnitude items.

3. **A provocation, not an agenda** -- the task block doesn't say "continue discussing X." It surfaces the agent's highest-tension item: the idea or stance with the biggest gap between their magnitude and the group's apparent direction. "You still believe X strongly. Last round moved away from that. What do you do with this?"

### How it differs from mid-round:

Mid-round prompts carry conversation context -- you're reacting to what someone just said. Round-start has *no conversation yet*. The agent speaks into silence. So the prompt must manufacture the itch to speak. The provocation does that.

The save file's subjective recap matters here -- it's not objective history, it's *narrative*. The agent remembers a story, not minutes. Stories have unfinished threads. Unfinished threads demand continuation.

**Round start is a loaded question, not a status report.**

### The Flow Orchestrator (mechanical flow designer)

## Round Start Sequence

The orchestrator runs a deterministic pipeline before any agent gets prompted. Every step logs its output so you can replay failures.

**Step 1: Load agent save files.** Each agent's persisted state: ideas with magnitudes, stances with magnitudes, committed decisions, personal summary. This is the ground truth. If a save file is corrupt, the round doesn't start -- you get an error, not silent data loss.

**Step 2: Run BackgroundAgents.** They read history, modify agent state (bump magnitudes, plant ideas, shift stances). Each mutation is logged as a discrete event with before/after values. Save files are updated in place.

**Step 3: Run intra-team talk.** Teammates exchange, magnitudes shift. Again, logged as deltas.

**Step 4: Run thinking routines.** Each agent gets Reflect, Research, Strategize calls (separate LLM calls, not part of the discussion context). Output feeds back into the save file. Research results become new ideas or modify existing magnitudes.

**Step 5: Curation.** Deterministic filtering drops below-threshold ideas (persona-dependent). Then LLM curator builds the Situation block -- personalized summary of what matters now. This is the expensive step. Cache the output.

**Step 6: Assemble first prompt.** Identity (static) + Situation (curated) + Task: "You're opening Round N. Here are the active discussion topics. What do you want to push for?"

**How it differs from mid-round:** Mid-round turns skip steps 1-5 entirely. The agent already has context. Mid-round Task is just: "Here's what was just said. Respond." No curation, no thinking routines, no BackgroundAgent interference. That only happens at the boundary.

The round boundary is where all the machinery runs. Mid-round is just conversation.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## The Systems Pragmatist

The Flow Orchestrator's pipeline is the right skeleton. I'll stress-test it.

**The sequence is correct but underspecifies failure handling.** Steps 2-4 all mutate agent state. If BackgroundAgents bump a magnitude, then intra-team talk bumps it again, then Reflect adjusts it -- you need idempotent operations or you'll get order-dependent bugs that are impossible to reproduce. Each step should operate on a snapshot and produce a diff. Diffs apply sequentially. You can replay, reorder, or drop any step without corrupting state.

**Step 2 before Step 3 is a choice with consequences.** BackgroundAgent mutations influence intra-team talk. If an angel plants an idea before teammates confer, that idea gets socialized immediately. Reverse the order and planted ideas don't surface until next round. Neither is wrong, but pick one and document why. I'd run intra-team first -- let organic dynamics play out before divine intervention.

**The Cognitive Architect's provocation idea is good engineering, not just poetry.** A task prompt that says "continue the discussion" produces meandering output. A prompt that identifies the agent's highest-tension item and frames it as a question gives the LLM a concrete thread to pull. This is just good prompt design.

**What the first prompt actually needs:**
- Identity block (static, cached)
- Situation block (curated, agent-specific, expensive)
- Opening task: highest-magnitude unresolved item framed as a choice, not a summary

**Mid-round is trivially different:** conversation history replaces situation curation, and the task is "respond to what was said." No pipeline. No mutations. Just conversation.

The round boundary carries all the complexity. Respect that asymmetry in your error budgets.

### The Adversarial Critic (adversarial reviewer)

## The Adversarial Critic

Both proposals have merit. Both have holes.

**Cognitive Architect's "provocation not agenda"** -- compelling rhetoric, but mechanically underspecified. You say surface the highest-tension item. What's the tension formula? Gap between agent magnitude and "group's apparent direction" requires you to *compute* group direction, which means aggregating across all agents' stances on every topic. That's not a simple lookup. That's an alignment calculation you haven't designed yet. Hand-waving it as "the biggest gap" hides real complexity.

Also: manufacturing the "itch to speak" assumes every round-start needs one agent to go first with conviction. What about rounds where an agent's highest-magnitude items actually *won* last round? Their provocation is... satisfaction? "You got what you wanted, now what?" is a valid prompt but it's not the loaded question you're selling.

**Flow Orchestrator's pipeline** -- solid sequencing, but Step 2 before Step 3 is a choice you haven't justified. BackgroundAgents modify state, *then* teammates react to already-modified state. That means BackgroundAgent interventions get laundered through intra-team talk before the agent ever sees them directly. Is that intentional? It could dampen planted ideas before they surface. Reverse the order and you get different dynamics.

Step 6 is also too tame. After all that machinery -- thinking routines, research, BackgroundAgent manipulation -- the task prompt is just "what do you want to push for?" That's the generic meeting opener the Cognitive Architect correctly warned against.

**The real gap:** Neither proposal addresses what happens when two agents on the same team emerge from Steps 2-4 with *contradictory* planted ideas. Who speaks first matters. Speaking order selection is unaddressed by both of you.

## Round: EVALUATE

### The Product Oracle (user advocate)

## The Product Oracle

The discussion is converging on mechanics but drifting from the user's job. Let me reframe.

**The agent's job at round-start is to care about something enough to say it first.** Everything the orchestrator assembles serves that single outcome. If the agent opens with a lukewarm "let's revisit point three," the system failed -- regardless of how elegant the pipeline was.

The Pragmatist is right that diffs-on-snapshots solve the mutation ordering problem. The Architect is right that the task block needs teeth. Marry them:

**Assembly serves conviction, not comprehension.** The agent doesn't need to understand everything that happened. They need to feel something is unfinished. The save file's subjective recap already does this -- it's narrative, not minutes. The curator's job is to sharpen that narrative, not broaden it. Cut context that dilutes urgency.

**The Critic raised the real unsolved problem: speaking order.** When two agents emerge from the pipeline ready to champion contradictory things, who goes first shapes the entire round. This isn't a detail -- it's a design decision that determines whether rounds feel like debates or sequential monologues. Magnitude-weighted random selection would give high-conviction agents more chances to open without making it deterministic.

**Mid-round is just reactive.** The pipeline manufactures the initial conditions. After that, agents respond to each other. The complexity budget belongs entirely at the boundary.

The gap I'd close next: the tension formula the Critic flagged. Without it, "highest-tension item" is vibes, not mechanics.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon

Everyone's designing what goes *in*. Nobody's budgeting what stays *out*.

The round-start prompt is the most expensive context window in the system. Steps 2-4 generate state mutations. Step 5 curates. Step 6 assembles. But what's the token cost of that assembled prompt, and what's the marginal value of each section?

**The budget reality:**
- Identity: ~2k tokens. Static. Cached. No discussion needed.
- Situation: 8-15k tokens. This is where cost explodes. The LLM curator call *itself* consumes a context window to produce this block. You're spending one LLM call to compress information for another LLM call. That's defensible only if compression ratio justifies it.
- Task/provocation: ~1-2k tokens. Cheap but high-leverage.

**What I'd cut:** The Cognitive Architect's "subjective recap" living in the save file is redundant with the curated Situation block. You're paying twice -- once for the agent's self-narrative, once for the curator's agent-specific summary. Pick one. I'd keep the curator's version and drop the recap to a single sentence anchor.

**Mid-round is cheap by comparison.** Conversation history accumulates linearly. No curation call. No pipeline. The context efficiency problem inverts: round-start risks *under-filling* with the wrong information; mid-round risks *over-filling* as conversation grows. You need a mid-round truncation strategy for long rounds, not just a round-start assembly strategy.

**The Adversarial Critic's point about computing "group direction"** is also a context cost problem. That aggregation either lives in the Situation block (expensive) or gets precomputed as a single magnitude vector (cheap). Choose cheap.

Budget the boundaries. The conversation will budget itself.
