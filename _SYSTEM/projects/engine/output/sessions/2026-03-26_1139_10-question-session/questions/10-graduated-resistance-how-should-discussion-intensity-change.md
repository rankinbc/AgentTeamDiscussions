# Graduated resistance: how should discussion intensity change over time?

*Generated: 2026-03-26 12:16 | Q10 | 194s | Mode: compete*

## Decisions

### Primary Decision: Defer Resistance Architecture Until Instrumentation Data Exists

Do not implement graduated resistance, constant-intensity resistance, rotating analytical frames, or any per-round behavioral variation. The current system -- uniform overlay per mode, fixed round counts -- ships unchanged.

This decision follows the instrument-first principle established in Q2 (token budget), Q5 (stale detection), Q6 (phase separation), and Q8 (verbosity management). Resistance architecture has the weakest case of any question for breaking that principle: it has zero demonstrated impact on what the user reads in the Morning Brief.

### Secondary Decision: Define Semantic Similarity Between Rounds as the Convergence Gate

When Q2/Q8 instrumentation is live, add a post-hoc measurement: semantic similarity of agent positions across rounds within a question. This is the metric that would reopen the resistance question.

- If rounds 2-3 show high similarity to round 1 positions, that is evidence of convergence (the problem graduated resistance would solve).
- If rounds 2-3 show divergence or stable diversity, graduated resistance is a solution to a problem that does not exist.

No threshold is defined now. The first measurement pass establishes the baseline. The second pass (after any future structural change) establishes whether the baseline shifted.

### Tertiary Decision: Reject Rotating Analytical Frames and Natural Escalation as Unsubstantiated

Two competing proposals were evaluated and both rejected:

**Rotating analytical frames** (attack problem space, then attack proposals, then attack own positions) adds per-round overlay variation that couples `RoundRunner` to `PromptBuilder` through round-index-dependent template logic. This creates debugging surface and maintenance cost for an effect that is unmeasured and consumes context tokens that compete directly with conversation history. It optimizes for mechanism elegance while the user experience stays flat.

**Natural escalation through context accumulation** (the claim that agents reading more prior-round output naturally increase friction) is an untested hypothesis. The equally plausible counterargument -- that context accumulation produces anchoring and convergence, not escalation -- stands unrebutted. Treating this claim as settled architecture would be building on an assumption about LLM behavior that no one in the discussion could substantiate.

Both proposals fail the same test: they prescribe optimization of a system whose baseline output quality has not been measured.

---

## Rationale

### What Was Argued

Five positions were represented across three rounds:

1. **Constant full-intensity resistance with rotating frames** -- every round at maximum intellectual force, shifting only the analytical lens (problem space, then proposals, then self-critique). Claimed support from human creativity research showing early disagreement outperforms deferred judgment.

2. **Single overlay, zero rotation** -- context accumulation between rounds provides natural escalation without any orchestrator mechanism. Round-differentiation logic is unnecessary complexity.

3. **Defer until instrumented** -- neither constant intensity nor natural escalation can be evaluated without output-quality data. The instrument-first principle from six prior decisions applies here.

4. **Defer with an explicit measurement gate** -- semantic similarity between rounds as the trigger metric. Without a defined gate, "defer" becomes "forget."

5. **Defer as a context budget question** -- resistance overlays compete with conversation history for finite context window. Adding per-round behavioral modifiers is blind allocation without Q8 prompt-size data.

### Why the Creativity Research Argument Failed

The appeal to Nemeth's work on authentic dissent in human groups does not transfer to this system. Human dissent works through social mechanisms: people remember being challenged, adjust their confidence, build on disagreements across turns. LLM agents in stateless subprocess calls do none of this. Each invocation is a fresh context window responding to a prompt and a transcript. The mechanism of action that makes early human disagreement productive does not exist in the current architecture.

### Why Natural Escalation Was Not Trusted

The claim that context accumulation produces escalation is plausible but so is its opposite. Instruction-following models reading growing transcripts tend toward anchoring on prominent positions, not increased friction. This is an empirical question about LLM behavior that was asserted as architectural fact. The discussion correctly refused to build on it.

### Why Six Prior Decisions Made This One Easy

The pattern is consistent: Q2 said instrument token budgets before allocating them. Q5 said fix round counts, skip runtime detection. Q6 said defer phase separation until data exists. Q8 said log prompt sizes before optimizing verbosity. Every decision where the team faced "optimize now vs. measure first" landed on measure first. Resistance architecture presented no evidence strong enough to break that pattern.

---

## What This Means for Implementation

**Nothing changes in the engine.** The current architecture -- uniform overlay per mode, fixed round structure defined in team YAML, no per-round behavioral variation -- is the correct architecture until data says otherwise.

**When Q2/Q8 instrumentation ships**, add semantic similarity measurement between agent positions across rounds as a post-hoc analysis step. This does not require runtime changes. It runs against session output after completion, the same way evaluation already works.

**If convergence is detected** (agent positions becoming more similar across rounds rather than maintaining diversity), revisit this question with data. The first intervention to consider is not graduated resistance but context hygiene -- the Q7 decision already identified context-window management as the highest-leverage anti-convergence tool available.

**If convergence is not detected**, this question is permanently closed. The system produces adequate diversity without resistance modulation, and the mechanism debate was solving a problem that did not exist.
<!-- complete -->
