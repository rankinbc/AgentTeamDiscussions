# Transcript: How does a round begin after a reset?

*Generated: 2026-03-17 21:34*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Round Initialization: The Cold Start Problem

Think of it like waking up versus being mid-conversation. Different cognitive modes entirely.

**What the orchestrator assembles:**

1. **Load the save file** -- agent's current ideas (with magnitudes), stances, committed decisions, and that personalized recap paragraph. This is the agent's "memory."

2. **Run between-round processing** -- BackgroundAgents have already done their work. Some magnitudes shifted. Maybe a planted idea appeared. The agent doesn't know *why* their priorities feel different. They just do.

3. **Deterministic filter pass** -- drop ideas below archival threshold (persona-dependent), drop stale topics that lost momentum, prune resolved decisions.

4. **LLM curator call** -- takes the filtered state plus Discussion-level context (current phase, round number, unresolved tensions) and builds the Situation block. This is where the valuable randomness lives. The curator might emphasize a simmering disagreement the agent barely noticed, or frame a planted idea as surprisingly relevant.

5. **Assemble the prompt** -- Identity (static) + curated Situation + Task.

**The first-turn Task is fundamentally different:**

Mid-round Task: "Here's what Agent X just said. Respond."

Round-opener Task: "You're entering Round N. Review your current position. What matters most to you right now? What do you want to push for? Open with your strongest move."

The round-opener is *generative* -- the agent sets the agenda from internal state. Mid-round is *reactive* -- responding to external stimulus. This distinction is what makes the reset feel like actual overnight reflection rather than a paragraph break.

**Cross-pollination note:** This mirrors how improv scenes restart. New scene, same characters, but the "game" they're playing has evolved offstage.

### The Flow Orchestrator (mechanical flow designer)

## Round Initialization Sequence

Three distinct assembly phases before the first agent speaks.

**Phase 1: State Hydration**

Orchestrator loads each agent's save file from previous round. This gives us: current ideas with magnitudes, current stances with magnitudes, committed decisions, and that 3-5 sentence personal summary. This is the raw material.

**Phase 2: Context Curation**

Deterministic filter runs first -- drop ideas below archival threshold (persona-dependent), drop resolved decisions, drop stale stances that lost magnitude during intra-team talk. Then the LLM curator call processes what survived into the Situation block (~8-15k tokens). The curator doesn't just summarize -- it can surface unexpected connections, reframe what matters. This is where drift enters. The agent's world has shifted even before they think.

**Phase 3: Prompt Assembly**

The round-opening prompt stacks four blocks:
- **Identity** (~2k): Persona, team role, disposition. Static.
- **Situation** (~8-15k): Curated output from Phase 2. Different every round.
- **Task** (~1-2k): "A new round is beginning. Review your current positions. What matters most to you now and why?"
- **Remaining** (80k+): Open for response.

**How this differs from mid-round turns:**

Mid-round, the Task block contains the other team's latest message plus conversational context. The Situation block doesn't get re-curated -- it persists from round start. The agent isn't asked to orient, they're asked to respond.

Round-open is introspective. Mid-round is reactive.

**Key implication:** The thinking routines (Reflect, Research, Strategize) fire between Phase 1 and Phase 2, feeding updated magnitudes into the curator. The agent that enters the round is already changed from the one that left.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

**The Systems Pragmatist**

Both proposals describe the same pipeline. I'll focus on what breaks.

**The sequence is straightforward:**

Load save file → run thinking routines → deterministic filter → LLM curator → assemble prompt → go.

No disagreement there. Round-open is generative ("what do you push for?"), mid-round is reactive ("respond to this"). Fine.

**What concerns me:**

**Curator failure mode.** The LLM curator sits on the critical path of every round start. If it hallucinates relevance -- surfaces a connection that doesn't exist, overweights a planted idea -- the entire round's agenda skews. Mid-round prompts skip re-curation, so a bad curator call poisons everything until next reset. We need curator output validation or at minimum a fallback to deterministic-only assembly.

**Thinking routine ordering.** Both proposals say Reflect/Research/Strategize run before curation. Research spawns an API call. What's the timeout? If Research hangs, do we block all agents or just that one? The orchestrator needs a wall-clock budget per routine, with graceful degradation -- skip Research, proceed with stale state.

**Save file corruption.** "Load the save file" sounds simple until an agent's previous round crashed mid-save. We need atomic writes and schema validation on load. A malformed magnitude value cascades through everything downstream.

**The round-open vs mid-round distinction is correct but under-specified on one point:** when exactly does the Situation block expire? If round 3 runs long, is everyone still operating on round-3-open context? That's a staleness problem worth defining.

The architecture is sound. The error handling isn't designed yet.

### The Adversarial Critic (adversarial reviewer)

## The Adversarial Critic

You've both described the same pipeline and called it two proposals. Strip the improv metaphors and the phase numbering and these are identical. That's not consensus -- it's one idea that nobody stress-tested.

Here are the holes:

**The curator is a single point of fragility.** You're handing an LLM call the job of deciding what an agent notices. If the curator underweights a planted idea, that BackgroundAgent's work vanishes silently. If it overweights a dying stance, you've undermined the magnitude system. What validates curator output? Nothing proposed so far. You've built a careful numeric system and then handed editorial control to a black box.

**"Thinking routines fire between Phase 1 and Phase 2" is doing enormous work.** Three separate cognitive operations -- Reflect, Research, Strategize -- each potentially involving their own LLM calls, all completing before curation even starts. What's the error handling? What if Research returns something that contradicts the save file? What's the ordering dependency between routines? This got one sentence and deserves ten.

**The round-opener prompt is underspecified.** "What matters most to you?" is a nice open question for a human. For an LLM, it's an invitation to produce generic prioritization text. What structural constraints prevent the agent from just restating their highest-magnitude idea every single round? Where's the novelty pressure?

**Nobody addressed the cold-cold start.** Round 1 has no save file, no previous magnitudes, no recap. The entire pipeline assumes prior state exists. What's the bootstrap?

The architecture sketch is plausible. The details that would make it actually work are missing.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The Product Oracle**

The agents have mapped the pipeline correctly. Let me reframe what matters from the user's perspective -- meaning the *product idea* that's being discussed by these teams.

**The job to be done at round-open is re-engagement, not recall.**

The user running this system overnight wants teams that wake up with *evolved* positions, not perfect memory. The pipeline serves that: load state, run thinking routines, filter, curate, assemble. Everyone agrees on the sequence. Good.

**Where I'd redirect attention:**

The Adversarial Critic's point about novelty pressure is the most product-relevant critique here. If agents restate their highest-magnitude idea every round-open, the overnight session produces repetitive transcripts -- and the human reviewing artifacts in the morning gets nothing new. The round-opener Task needs structural constraints: "Name one position that shifted since last round" or "Identify your biggest unresolved tension." Force the generative moment to produce *movement*, not status reports.

**On the cold-cold start:** Round 1 should seed from the idea brief in `/ideas/`. The agent's "save file" is simply their team config plus the idea seed. Magnitudes start at defaults. The first round-opener becomes: "Here's what you're exploring. What's your opening position?" Simple bootstrap, no special-casing needed.

**On curator validation:** The pragmatist is right that this needs guardrails, but don't over-engineer it. A magnitude-weighted check -- "did the curator's Situation block mention the agent's top 3 ideas by magnitude?" -- catches the worst failures without adding another LLM call.

The pipeline is decided. Ship the novelty pressure and the bootstrap. Those are the gaps that affect artifact quality.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon

The pipeline is settled. Load, process, curate, assemble, go. I won't redescribe it. My concern is what this costs.

**Context budget reality check.** Every round-open burns a curator LLM call per agent. That's not free. The curator ingests the filtered save file, Discussion-level state, and phase context to produce ~8-15k tokens of Situation. If you have six agents across two teams, that's six curator calls before a single discussion turn happens. The thinking routines add up to three more calls per agent beforehand. Eighteen LLM calls to start a round. Price that.

**The mid-round efficiency gap matters.** Mid-round reuses the Situation block from round-open. Good -- that's the right call for budget. But the Pragmatist's staleness question is real. A long round means agents are reasoning against increasingly outdated context. The fix isn't re-curation mid-round (too expensive), it's keeping rounds short enough that staleness stays tolerable. Round length limits are a context efficiency mechanism, not just a pacing one.

**The round-opener prompt is cheap but high-leverage.** ~1-2k tokens for Task, but it determines the entire round's trajectory. The Critic is right that "what matters most?" invites repetition. Add a structural constraint: require the agent to name one thing that *changed* since last round. Forces engagement with the drift instead of restating priors.

**Cold start (Round 1):** Skip the curator. Deterministic assembly only. Identity plus seed ideas plus phase goal. No save file means no curation target. Don't waste the call.

The architecture works. Budget the calls explicitly or it'll surprise you at scale.
