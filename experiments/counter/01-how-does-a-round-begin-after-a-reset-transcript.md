# Transcript: How does a round begin after a reset?

*Generated: 2026-03-17 22:38*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Round Initialization: The Morning Briefing

Think of it like waking up. You don't remember your dreams verbatim -- you remember *feelings*, *impressions*, a few vivid fragments.

**What the orchestrator assembles:**

1. **Identity block** (~2k) -- persona, style, archetype. Static. The "who you are" anchor.
2. **Save file** -- ideas with current magnitudes, stances with magnitudes, committed decisions, that 3-5 sentence personal recap. This is the agent's *memory* of last round.
3. **Curated situation** (~8-15k) -- here's where the hybrid curator earns its keep. It runs deterministic filters (drop resolved, decay old), then the LLM curator builds a *narrative summary* of where things stand. Not a transcript replay. A briefing.
4. **Between-round residue** -- results from intra-team talk (magnitude shifts), any BackgroundAgent manipulations (planted ideas, stance nudges), thinking routine outputs (reflect/research/strategize results).
5. **Task prompt** (~1-2k) -- "Round 3 is beginning. Here's the phase, here's the agenda. What do you want to open with?"

**How it differs from mid-round turns:**

Mid-round, an agent gets the *running conversation* plus a simple "respond to what was just said." The context is largely the dialogue itself.

Round-open is fundamentally different -- it's *reconstructed context*, not continued context. The agent builds a fresh mental model from curated fragments. This is the drift mechanism. What the curator emphasizes, what BackgroundAgents planted, what magnitude shifts occurred -- these *reframe* the conversation before it restarts.

Mid-round: reactive. Round-open: *agenda-setting*.

That asymmetry is the engine. Whoever frames the opening question steers the round.

## Round: COUNTER-PROPOSAL

### The Flow Orchestrator (mechanical flow designer)

## Counter-Proposal: Interrogative Reconstruction

The Cognitive Architect treats round-open as a briefing -- hand the agent a curated package and say "go." I trace a different sequence.

**Don't brief. Interrogate.**

The orchestrator doesn't assemble a monolithic context block. Instead, it runs a short *dialogue with the agent itself* to reconstruct working memory.

**Sequence:**

1. **Identity block** loads (same -- static, ~2k).
2. **Save file** loads (same -- the agent's own compressed state).
3. **No curated situation.** Instead, the orchestrator asks three targeted questions drawn from the save file and round metadata:
   - "Your idea X dropped from magnitude 7 to 3. What do you think happened?"
   - "Team consensus shifted toward Y. Does that change your position on Z?"
   - "A new idea appeared in your notes you don't remember proposing. What do you make of it?"
4. Agent responds to each. These responses *become* the situation context -- self-generated, not curator-generated.
5. **Then** the task prompt fires: "Round 3 begins. What's your opening?"

**Why this is fundamentally different:**

The briefing model is *tell-then-act*. This is *reconstruct-then-act*. The agent builds its own mental model through guided self-interrogation rather than receiving one pre-built.

**The tradeoff is real:** you burn 3-4k tokens on the interrogation exchange, and you lose curator control over framing. But you gain something the briefing can't deliver -- the agent's reasoning about *why* things changed becomes load-bearing context, not discarded pre-processing.

Drift still happens. The questions *are* the steering mechanism. What you ask shapes what they reconstruct.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## The Systems Pragmatist: Neither. Build for failure.

Both proposals describe happy paths. Let me describe what actually breaks.

**The briefing model** has a single point of failure: the curator. If it summarizes poorly, the agent starts round 3 with a distorted mental model and *no mechanism to detect that*. You've centralized interpretation in one LLM call with no error correction.

**The interrogative model** burns tokens on self-reflection that may produce confabulation. Ask an LLM "why did your idea drop from 7 to 3?" and it'll confidently fabricate a narrative. You're treating hallucination as load-bearing context.

**What I'd actually build:**

Round-open is a two-phase sequence:

1. **Deterministic assembly** -- identity, save file, raw magnitude deltas (not interpreted), committed decisions, phase/agenda metadata. No LLM touches this. It's the ground truth layer. ~4-5k tokens.

2. **One curator pass** -- summarize *only* what the agent wasn't present for (other team's positions, BackgroundAgent actions). Keep it factual: "Team B proposed X. Your teammate's idea Y gained magnitude." No narrative. ~3-4k tokens.

Skip the self-interrogation. Skip the narrative framing. Give agents *facts and numbers*, let the persona layer generate its own interpretation during the actual response.

**Mid-round vs round-open difference:** Mid-round context is the live transcript. Round-open context is *reconstructed state plus deltas*. That's it. Don't romanticize the reset -- engineer it to be auditable.

The curator earns its keep through *compression*, not *interpretation*. The moment it starts editorializing, you've lost reproducibility.

### The Adversarial Critic (adversarial reviewer)

## The Adversarial Critic

Both proposals have a structural blind spot: they assume the round-open is where agency lives. It isn't. It's where *illusion of agency* lives.

**Against the Briefing Model:** You're handing a stateless LLM a narrative and hoping it role-plays continuity. The "morning briefing" metaphor is charming but misleading -- the agent doesn't *wake up*. It's instantiated. That curated situation block is the curator's mental model of what matters, laundered through the agent's voice. You've just moved authorship upstream and called it memory.

**Against Interrogative Reconstruction:** Cleverer, but worse. You burn tokens having the agent *confabulate* explanations for magnitude shifts it never experienced. "What do you think happened?" -- it doesn't *think* anything happened. It'll generate a plausible-sounding narrative that has zero causal relationship to actual events. You've replaced curator bias with hallucination and called it reasoning.

**The real question neither addresses:** What's the failure mode? Briefing fails gracefully -- bad curation means stale topics, but the agent still functions. Interrogation fails catastrophically -- one confabulated answer poisons the self-generated context that everything else builds on, and the agent has no external reference to self-correct.

**What I'd stress-test:** Run both approaches with deliberately corrupted save files. Plant contradictions. See which one produces agents that notice something's wrong versus agents that cheerfully confabulate around the damage. That tells you which mechanism is actually load-bearing versus decorative.

The interrogation model is intellectually seductive and operationally fragile. Pick the boring one, then make it less boring.

## Round: EVALUATE

### The Product Oracle (user advocate)

## The Product Oracle

The user's job-to-be-done here is **resume a meaningful conversation without reading the whole transcript**. That's the product problem. Everything else is implementation.

The Pragmatist is closest. Here's why.

**The agent needs to answer one question at round-open: "What should I care about right now?"** The answer comes from facts, not narratives. Magnitudes already encode what matters -- that's the whole point of the magnitude system. A save file showing Idea X at 8.2 and Idea Y at 1.4 *is* the briefing. The agent's persona does the interpretation.

**Assemble this, in this order:**

1. Identity (static, ~2k)
2. Save file -- ideas, stances, magnitudes, committed decisions, personal recap
3. Factual deltas -- what changed since you last spoke, stated without editorialization
4. Curator compression of *what you missed* -- other team's moves, BackgroundAgent actions, teammate shifts from between-round talk
5. Task prompt -- phase, agenda, "what's your opening move?"

**How it differs from mid-round:** Mid-round, the conversation *is* the context. Round-open, you're reconstructing context from state. Mid-round is reactive. Round-open is agenda-setting.

**Skip interrogative reconstruction.** It's solving a problem users don't have. Agents don't need to "understand why" magnitudes shifted -- they need to know *that* they shifted and respond in character. The persona layer handles meaning-making for free.

Build the boring version. The magnitude system is already your interesting part.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon: Budget the Reset, Don't Design It

Four proposals. Let me count tokens.

The Briefing model costs ~13-20k on assembly before the agent speaks. The Interrogation model burns an additional 3-4k on self-dialogue that produces unverifiable context. The Pragmatist strips it to ~8-9k of ground truth. The Critic says pick boring.

The Critic is closest. Here's why from a budget perspective.

**Every token in round-open context competes with thinking space.** An agent with 100k context that burns 20k on briefing has 80k for the actual round. One that burns 9k has 91k. Over a 6-round discussion, that delta compounds -- you're buying roughly one extra round of conversation depth.

**My recommendation:** Layer the round-open as a strict token budget, not an architecture.

- **Layer 0: Ground truth** (~4k ceiling). Identity, save file, raw deltas. Deterministic. Non-negotiable.
- **Layer 1: Compressed externals** (~3k ceiling). What happened outside your view. Factual summaries only. Curator compresses, does not interpret.
- **Layer 2: Discretionary** (~2k ceiling). This is where you experiment. Narrative framing, interrogation prompts, planted questions -- whatever. But capped. Hard.

Total: ~9k. The Pragmatist's number, arrived at differently.

The interrogation model is a Layer 2 experiment, not a foundation. Test it inside the cap. If self-generated context outperforms curator narrative within the same 2k budget, adopt it. If not, cut it.

Don't romanticize the reset. Budget it.
