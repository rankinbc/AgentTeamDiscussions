# Transcript: Token budget allocation: agent state vs conversation history vs synthesis.

*Generated: 2026-03-26 11:46*

## Round: PROPOSE

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

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals share a dangerous blind spot: they treat token allocation as a *design* problem when it's actually an *empirical measurement* problem. Neither has data. The Cognitive Architect builds a phase-adaptive system on the assumption that identity tokens matter more early -- but what if the LLM ignores 80% of identity tokens regardless of placement? The Flow Orchestrator assumes two fixed profiles suffice, but "simplest that works" requires knowing what "works" means before you've run anything.

**Five problems nobody's addressing:**

1. **No measurement baseline exists.** Both proposals optimize allocation without knowing current utilization. How many identity tokens does Claude actually attend to? Nobody's measured attention decay across prompt sections. You're allocating a budget with no accounting.

2. **"Agent identity" is not a monolithic category.** Personality instructions, output format constraints, anti-slop rules, and positional priming all live in "identity" but have wildly different impact on output quality. Compressing "identity" treats these as interchangeable. They aren't.

3. **History truncation strategy matters more than allocation ratios.** Whether you cut oldest-first, summarize, or drop low-relevance exchanges dominates the outcome. Both proposals skip this entirely.

4. **The Architect's phase detection requires knowing what phase you're in mid-generation.** That means either predetermined allocation (which is just the Orchestrator's approach with more steps) or an intermediate classification call (which the Orchestrator correctly flags as expensive).

5. **Neither addresses context window variance across models.** A 200K window allocation strategy is meaningless if you switch to a model with 128K. Ratios don't transfer when the constraint surface changes shape.

The real first-to-break component: whatever truncation strategy gets chosen by default when history exceeds its allocation. That failure mode is invisible during small tests and catastrophic at scale.

## Position Summary
I advocate solving the truncation strategy problem before any allocation ratios are set, because how you *cut* matters more than how you *divide*. I reject both phase-adaptive and fixed-profile approaches as premature optimization over an unmeasured system. Without empirical data on actual token utilization and attention patterns, any allocation scheme is architectural theater.

### The Systems Pragmatist (infrastructure realist)

The Critic is right that this is an empirical problem, but then makes the same mistake everyone else is making: treating the token budget as a *scarce resource requiring careful allocation*. Let me challenge that shared assumption.

**The dangerous consensus nobody's questioning: that token budgets are actually the binding constraint.**

Current Claude context windows are 200K tokens. A 7-agent discussion with 3 rounds generates maybe 15-20K tokens of history. Agent identity prompts run 500-2000 tokens each. We're arguing about dividing a pie that's 10x larger than what we're putting on the plate. The *actual* constraint today is **wall-clock time per LLM call**, not token capacity. Every proposal optimizes for the wrong bottleneck.

**Where this breaks in practice:**

1. **The truncation problem the Critic raised is real but distant.** With current session sizes, you hit the 10-minute timeout on complex synthesis calls long before you hit token limits. Truncation strategy matters for sessions with 20+ agents or 10+ rounds -- neither of which the engine supports today.

2. **Adaptive allocation requires state management that *will* corrupt.** The Architect's phase-adaptive model means session recovery must reconstruct not just position but allocation state. The current crash recovery uses completion markers. Adding allocation phase tracking doubles the recovery surface area for zero measured benefit.

3. **The Orchestrator's "two profiles" approach is closest to correct but still over-engineered.** One profile works until measurement proves otherwise. The delta between "slightly suboptimal allocation" and "correct allocation" is noise compared to prompt quality differences.

## Position Summary
I advocate a single static allocation with no phase adaptation, because the token budget is not currently the binding constraint -- wall-clock time is. I reject all allocation optimization as premature until someone demonstrates a real session that actually hits context limits. Solve the problem you have, not the problem you imagine.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

**Verdict: The Pragmatist wins. The Critic's critique is the reason why.**

The Critic correctly identified that both the Architect's phase-adaptive model and the Orchestrator's two-profile model are designing solutions to an undemonstrated problem. The Pragmatist then drove the nail: wall-clock time is the actual binding constraint, not token budgets. No one has shown a session that hits context limits.

The Architect's breathing model is elegant but unjustified. Phase-adaptive allocation requires measuring agreement levels mid-session, which means extra LLM calls, which means more wall-clock cost -- the thing that actually hurts. You're optimizing the wrong variable.

The Orchestrator's fixed two-profile approach survives the critique better than the Architect's, but still falls to the Pragmatist's core objection: why optimize allocation at all before demonstrating the problem exists? The Orchestrator at least has the instinct toward simplicity, but even two profiles is one too many when zero profiles (just use the default context window and truncate when you must) hasn't been proven insufficient.

The Critic's point about truncation strategy deserving priority over allocation ratios is valid but secondary. You need to know *if* you're truncating before you optimize *how*.

**What actually matters now:** Instrument the current system. Log token utilization per round, per agent. Find out if any session actually pressures the context window. If it does, *then* design allocation. If it doesn't, you just saved yourself an entire subsystem of complexity.

Solving imaginary problems is the most expensive form of engineering waste.

## Position Summary
I advocate instrumenting actual token utilization before designing any allocation strategy, because no evidence exists that token budgets are a binding constraint. I reject both phase-adaptive and fixed-profile allocation schemes as premature optimization over an unmeasured system. Wall-clock time is the real bottleneck; solve that first, and let data -- not architecture diagrams -- dictate whether allocation logic is ever needed.

### The Product Oracle (user advocate)

**Verdict: The Pragmatist is right, but for the wrong reason. The Surgeon lands it.**

The Pragmatist says wall-clock time is the binding constraint. True today. But the Surgeon makes the sharper argument: *you don't even know if the problem exists*. That's a different claim. The Pragmatist is saying "don't optimize this"; the Surgeon is saying "you can't optimize this because you have no data." The Surgeon's version is stronger because it gives you an exit condition -- instrument, measure, then decide.

Here's what I care about: what does the user see in the Morning Brief because of this choice? Nothing. Zero. No allocation strategy, no matter how elegant, changes the quality of what lands in front of the human reader *unless* the system is currently degrading output due to context pressure. Nobody has shown that it is.

The Architect's breathing model is product poison -- it adds configuration surface area, failure modes, and cognitive load for the person running sessions, all for a benefit that's purely theoretical. The Orchestrator's two-profile approach is less dangerous but still premature. You're asking a solo builder to understand token allocation profiles before they've even validated that their agent team produces useful output.

The Critic's truncation-first argument has merit but puts the cart before the horse. You truncate *when something needs truncating*. Measure first.

Ship instrumentation. It's a logging change, not an architecture decision. If the data shows pressure, *then* the Orchestrator's simple two-profile model is where you start -- not the Architect's adaptive complexity.

## Position Summary
I advocate instrumenting token utilization before building any allocation system, because no user-visible output problem has been demonstrated. I reject both phase-adaptive and fixed-profile allocation as premature product complexity that burdens the solo builder with configuration decisions that don't improve the Morning Brief. Let measurement data -- not architectural elegance -- trigger allocation work if and when it's actually needed.


<!-- complete -->
