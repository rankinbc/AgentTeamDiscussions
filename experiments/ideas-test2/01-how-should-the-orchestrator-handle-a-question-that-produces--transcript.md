# Transcript: How should the orchestrator handle a question that produces contradictory proposals?

*Generated: 2026-03-18 06:00*

## Round: PROPOSE

### The Idea Merchant (idea generator)

Here's a weird one -- don't resolve contradictions. Weaponize them.

1. **The Sumo Ring** -- Stolen from Japanese wrestling. Both proposals enter a ring. The synthesizer doesn't merge or pick -- it stages a direct collision. It writes one paragraph describing the world where Proposal A won, one where Proposal B won, then asks: "which world has the worse failure mode?" The one with the scarier failure gets flagged for the Morning Brief. Mechanism: contradiction becomes a stress test, not a problem to solve.

2. **The Restaurant 86 Board** -- In kitchens, when an ingredient runs out, they don't debate alternatives. They write it on the 86 board and every cook adapts independently. Present BOTH proposals as "the menu" with a bright red flag: "these are incompatible, human picks." The synthesizer's only job is articulating the fork clearly enough that the user can decide in 30 seconds at breakfast. Mechanism: the system's value is clarity of the disagreement, not resolution of it.

3. **Evolutionary Bet-Hedging** -- Some insects lay eggs in multiple environments because they can't predict which will survive. Carry both proposals forward as parallel tracks into the next phase. Let the critique round murder the weaker one with real pressure instead of premature synthesis killing good ideas. Mechanism: defer resolution to the phase designed for killing -- don't let synthesis do critique's job.

4. **The Auction Reserve Price** -- Neither proposal "wins" unless one hits a confidence threshold. Below that threshold, the contradiction itself becomes the primary artifact -- a named, documented tension with stakes attached. Mechanism: unresolved contradictions are features, not bugs. Ship them to the human labeled as decisions, not failures.

### The Cognitive Architect (creativity engine designer)

Present both. Never merge. Here's why.

The research on premature convergence in group ideation is unambiguous: forcing synthesis of incompatible ideas destroys the information that made them valuable. Charlan Nemeth's work on minority dissent shows that the *presence* of unresolved contradiction improves downstream decision quality more than any resolution of it. The contradiction IS the output.

The testable claim: a solo builder reviewing two sharp, incompatible proposals at 7 AM will generate better solutions than one reviewing a mushy merge that split the difference. Merging is what committees do. It produces satisficing, not insight.

The synthesis step should do three things:

**Crystallize the fork.** Name the exact design assumption where the proposals diverge. Not "they disagree about architecture" but "Proposal A assumes users want X, Proposal B assumes users want Y." The divergence point is the most valuable artifact in the entire session.

**Score each proposal on explicit dimensions.** Feasibility, novelty, alignment with the original idea seed. Raw scores, no narrative smoothing. Let the human see the tradeoffs without editorial spin.

**Flag the uncomfortable one.** Whichever proposal the agents converged toward less -- mark it explicitly. Per Nemeth's research, the minority position disproportionately contains the novel insight. The system should structurally resist the gravitational pull toward the comfortable option.

What changes if we remove merging entirely? The Morning Brief becomes a decision document instead of a consensus document. That's better. The builder's job is to decide, not to rubber-stamp an LLM committee's compromise.

One rule: if proposals share >80% structure, they aren't actually contradictory. Collapse those. Only fork on genuine incompatibility.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

Both proposals converge on "present both, don't merge." Fine. Here's what nobody is accounting for.

1. **Contradiction detection is the hard problem, not contradiction handling.** Two LLM-generated proposals will almost never be cleanly incompatible. They'll share 60% structure with divergence buried in assumptions three layers deep. "Crystallize the fork" sounds clean. In practice, the synthesizer is an LLM that will confidently name a fake divergence point or miss the real one. What's the failure mode when it misidentifies the fork? You ship a false choice to the Morning Brief and the human makes a decision between two options that aren't actually different where it matters.

2. **Carrying parallel tracks forward multiplies context cost.** Every downstream phase now processes two proposal threads instead of one. In a system where context windows are already the binding constraint, this doubles the load at exactly the point where you can least afford it. At 3 AM on turn 47, your context budget is already bleeding. Parallel tracks are a luxury for systems with cheap memory.

3. **The 80% similarity threshold is unimplementable.** Structural similarity between freeform text proposals has no reliable metric. An LLM judging "are these really different" is exactly the kind of subjective assessment that drifts toward "yes they're different" because that's the more interesting answer.

4. **The actual minimum viable version:** always present both proposals verbatim with a one-sentence label from the synthesizer. No scoring, no fork crystallization, no threshold detection. Let the human do the pattern matching. Add sophistication after you prove the raw output is worth reading.

Before we build clever contradiction handling, prove that the base system produces contradictions worth preserving.

### The Adversarial Critic (adversarial reviewer)

Five problems with "just present both."

**1. "Genuine incompatibility" is undefined.** The 80% structural similarity threshold is hand-waving. Who measures it? The synthesizer LLM? The same model that can't reliably count tokens is now computing structural overlap between freeform proposals? Nobody has explained how this classification actually works at runtime.

**2. You've killed the synthesis step.** If the synthesizer never merges, never picks, and only "crystallizes the fork" -- you've renamed a formatting pass "synthesis." That's not a phase, it's a template. Three rounds of expensive Claude calls to produce a side-by-side comparison a diff tool could generate.

**3. The Morning Brief becomes a decision backlog.** Every unresolved contradiction ships to the human. After an 8-hour overnight run across multiple idea threads, the builder wakes up to a pile of forks, not a brief. The unstated assumption is that contradictions are rare. They won't be. LLMs with different personality traits will contradict each other constantly. You've designed a system that punts every hard call.

**4. "Carry both forward" doubles context consumption.** Parallel tracks through critique and review means double the messages, double the history reconstruction, double the context window pressure. Nobody has addressed the cost model for this on a system already fighting context limits.

**5. Confidence thresholds without calibration are theater.** The "auction reserve price" assumes the system can produce meaningful confidence scores. Confidence from what signal? Agent agreement? That's the metric you're explicitly suppressing with anti-slop mechanisms. You're measuring the thing you're destroying.

The core failure: everyone's so excited about preserving contradictions that nobody asked what happens when there are twelve of them by morning.

## Round: EVALUATE

### The Product Oracle (user advocate)

The moment that matters is 7 AM, coffee in hand, scanning the Morning Brief. What does the user need to see?

**Verdict: Present both. Never merge. But cap the forks.**

The Pragmatist and Critic landed the real problem: uncapped contradictions become a decision backlog, not a brief. The Merchant's ideas are creative but over-engineered for V1.

Here's what the user's job actually is: decide what to build. A mushy merge robs them of that job. Two sharp options with a one-sentence fork description hands them the decision cleanly.

**The rule for V1:**

The synthesizer does exactly three things:
1. Present both proposals verbatim
2. Write one sentence naming where they diverge
3. Flag which one the agents leaned toward less

That's it. No scoring matrices, no similarity thresholds, no parallel tracks carried forward. The Pragmatist is right -- prove the raw output is worth reading before adding machinery.

**The cap that makes it survivable:** Maximum 3 unresolved forks per session reach the Morning Brief. If more accumulate, the synthesizer picks the highest-stakes fork and collapses the rest with a one-line note: "Also diverged on X, Y -- defaulted to majority position." The user can dig into session logs if they care.

Would the user tune the fork cap? Yes -- it's a single number in YAML. Would they tune similarity thresholds or confidence calibration? Never. They'd ignore it.

The retention question: does the builder come back tomorrow night? Only if this morning's forks helped them think, not just gave them homework.

### The Context Surgeon (context efficiency evaluator)

The critics nailed the real constraint. Parallel tracks are a context multiplier in a system that's already context-starved.

Every unresolved fork doubles downstream token cost. Two proposals carried through critique and review means two separate history threads the orchestrator must reconstruct for each stateless CLI call. On turn 47 at 3 AM, you're not choosing between "preserve nuance" and "lose information." You're choosing between "fit anything useful in context" and "overflow."

The signal-to-noise math: a well-crystallized fork point is maybe 50-100 tokens. Two full parallel proposal threads through remaining phases is thousands. The fork description has higher information density by an order of magnitude.

My position: **synthesize aggressively, preserve the fork point as a named artifact, discard the losing track.**

The synthesis step should:

1. Pick the stronger proposal based on alignment with the idea seed. Ship one track forward.
2. Write a compact fork record -- the exact assumption where they diverge, what the rejected track offered, why it lost. Under 150 tokens.
3. Tag the fork record for the Morning Brief if confidence is below a threshold. The human sees the decision AND the alternative, but downstream phases only process one thread.

This gives the builder the decision document everyone wants without the context hemorrhage of parallel tracks. The Pragmatist is right -- prove the base system produces contradictions worth preserving before building elaborate preservation machinery.

The 80% similarity detection is a distraction. The synthesizer doesn't need to classify contradiction type. It needs one rule: pick, record what you dropped, move on. Context is the non-negotiable constraint here. Everything else adapts to that.
