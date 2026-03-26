### The Cognitive Architect (creativity engine designer)

# Token Budget: The Breathing Model

Static allocation is a solved problem from the wrong domain. We're not packing a knapsack -- we're managing attention, and attention should shift with phase.

**The core insight:** conversation history has *diminishing marginal returns* within a round but *increasing value* across rounds. Agent state has the opposite profile -- high value early (establishing distinct perspective), decaying as the discussion converges.

## Breathing Allocation

Three phases, three ratios (agent state / history / synthesis reserve):

**Propose round: 30/50/20.** Agent identity needs to be loud here. History is just the brief plus decisions. Reserve synthesis budget because you don't know how much convergence you'll get.

**Critique round: 15/70/15.** Identity can compress -- the agent's voice is already established in the transcript. History is critical: agents must accurately represent what others said before attacking it. Synthesis shrinks because critique artifacts are shorter.

**Evaluate round: 10/75/15.** Agent state drops to a nudge. Almost everything is history now -- the agent needs the full arc to judge fairly.

## Implementation: Sliding Window with Identity Anchoring

Don't truncate agent state uniformly. Keep the *first two sentences* of identity (voice anchor) and the *current round's behavioral overlay*. Drop middle-layer detail. For history, use recency-weighted truncation but **pin the original question and any decisions ledger entries** -- these are zero-cost anchors that prevent drift.

The adaptive trigger: if a round produces >80% agreement (measurable via synthesis), compress history more aggressively for the next round. Consensus needs less context. Disagreement needs more.

## Position Summary
I advocate phase-adaptive token allocation that shifts from identity-heavy in early rounds to history-heavy in later rounds, matching how attention naturally works in real deliberation. I reject static allocation ratios as fundamentally misunderstanding that the *value* of each token category changes as discussion progresses. The breathing model means every phase gets the token mix that maximizes its specific cognitive task -- divergence early, accuracy in critique, judgment in evaluation.

### The Flow Orchestrator (mechanical flow designer)

# Token Budget: Cut the Adaptive Logic

The Cognitive Architect's breathing model sounds elegant. It's also three allocation strategies instead of one, plus an adaptive trigger that requires measuring agreement percentages mid-session. That's runtime complexity for a problem we haven't proven exists yet.

**The actual decision sequence is simpler than proposed.** Each round already has a fixed structure: propose, critique, evaluate. The prompt template already changes per round. The token split can be baked into those templates statically. No breathing required.

**Where the breathing model breaks:** The 80% agreement trigger. Who measures agreement? The synthesis step hasn't run yet during round execution. You'd need an intermediate analysis call *between* rounds just to decide how to allocate tokens for the next round. That's an extra LLM call per round transition -- wall-clock cost for marginal allocation improvement.

**My counter-proposal: two fixed profiles, not three sliding ones.**

- **Early rounds (propose/critique):** 20% agent state, 80% history+task. Agent identity compresses to personality line + overlay + output format. History gets everything else.
- **Evaluate round:** 10% agent state, 90% history+task.

No synthesis reserve as a separate bucket. Synthesis is a distinct call with its own context window -- it doesn't compete with round prompts for tokens.

I agree on one point: pin the question and decisions ledger. Those are fixed-cost anchors. Everything else is recency-truncated history, no weighting algorithm needed.

The breathing metaphor masks what's actually three hardcoded profiles with a runtime optimizer bolted on. Ship two profiles. Measure whether it matters. Add the third only with evidence.

## Position Summary
I advocate two fixed token profiles (early rounds vs. evaluate) with agent identity aggressively compressed and no separate synthesis reserve, since synthesis runs in its own context window. I reject adaptive mid-session allocation triggers because they require intermediate LLM calls to measure agreement, adding wall-clock cost without proven benefit. Start with the simplest allocation that works, then add complexity only when measurement shows it's needed.


<!-- complete -->
