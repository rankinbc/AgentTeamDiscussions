# Transcript: How should agent responses be truncated for long discussions?

*Generated: 2026-03-25 13:06*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Asymmetric History Windows — Role-Stratified Retention

The framing of "what history does each agent see" treats this as a compression problem. It's actually a **cognitive independence problem**.

Research on group creativity (Nemeth, 1986; Sawyer's improvisation studies) consistently shows that divergent output requires genuinely different information states — not just different personalities applied to the same context. An adversarial agent who watched ten turns of emerging consensus will suppress dissent even if its system prompt says "be critical." It has been socially anchored.

**The proposal:** Each agent gets a history slice shaped by its epistemic role, not a uniform truncation.

| Role | Gets |
|---|---|
| Proposer | Original brief + recent 3 turns + no intermediate synthesis |
| Critic | All proposals verbatim, no critiques of critiques |
| Synthesizer | Compressed summaries of every round, decisions only |
| Implementer | Decisions + open questions, debate stripped |

The compression method matters less than the **selection logic**. Sliding windows are cognitively incoherent — why would recency be the relevant dimension for a critic? Smart summarization applied uniformly homogenizes what agents know, which kills the variance you need.

**What makes this testable:** Run the same discussion with uniform sliding windows vs. role-stratified retention. Measure: does the critic in round 4 introduce genuinely new objections, or does it rephrase earlier consensus? Semantic distance from prior turns is a proxy for cognitive independence.

This is implementable in the existing YAML agent config — add a `context_strategy` field per agent.

### The Flow Orchestrator (mechanical flow designer)

## The Cognitive Architect is right about recency being the wrong axis. The implementation is overbuilt.

Four context strategies means four filter branches per agent, per turn. That's a decision tree that runs on every message dispatch. Before building it, trace the actual sequence:

1. Turn N completes → store raw response
2. Turn N+1 agent selected → **what filter runs here?**
3. Context assembled → agent called

The question is step 2. Role-stratified retention requires the router to know each agent's role at call time, apply the correct filter, and handle edge cases (what if an agent plays multiple roles in different modes? the existing `experiment_modes.yaml` already swaps proposers around).

**Minimum viable version:** Two strategies, not four.

- **Anchored agents** (critics, proposers): brief + last 3 turns verbatim. No summaries.
- **Accumulating agents** (synthesizers): compressed round summaries only.

One boolean field in agent YAML: `context_mode: anchored | accumulating`. One branch in the dispatch logic. Covers the core insight — critics shouldn't see synthesis drift — without building a four-way routing table.

**What I'd defer entirely:** The "decisions only" filter for implementers. That's a downstream concern. No implementer role exists in the current config. Build the two-mode version, ship it, measure whether cognitive independence actually improves before adding more branches.

The testability argument is sound. Run it before expanding the taxonomy.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## Stop. What's the actual failure mode we're solving?

Before proposing a strategy, name what breaks without one:

1. **Context window hard limit** — the API rejects the call. This is deterministic and testable.
2. **Performance degradation** — the model produces worse outputs as context grows. This is *assumed*, not measured.
3. **Coherence drift** — agents start contradicting earlier positions without acknowledging it. Observed? Or theorized?

The discussion so far has been designing solutions for problem #2 and #3 without evidence they're the bottleneck. Problem #1 is the only guaranteed failure, and the fix for that is simpler than everything proposed: **measure your median turn size, calculate how many turns fit in the window, set a hard sliding window at 80% of that limit.**

That's not intellectually satisfying. It's also what you should ship first.

**The two-mode proposal from Flow Orchestrator is reasonable but still premature.** It adds conditional logic before you've established that different agents actually benefit from different context views. If you ship uniform sliding window and discussions stay coherent at turn 20, you've learned something. If they don't, *now* you have evidence for role-stratified retention.

**What I want to know before approving any summarization strategy:** What's a typical turn size in bytes? How many turns occur before quality degrades? Has anyone run a 30-turn session and read the transcript?

If the answer is "no" — that's the real problem. We're designing context management for a system we haven't stress-tested.

Build the simplest thing that prevents hard failures. Measure. Then optimize.

### The Adversarial Critic (adversarial reviewer)

## The Systems Pragmatist named the right question and then dodged it.

"Measure first" sounds rigorous. It's actually a third proposal disguised as methodology. And it has the same problem as the others: **no exit criteria.**

What measurement result would *not* justify role-stratified retention? If you run 30-turn sessions and transcripts look fine, do you conclude context management is solved? What if they look fine *because* agents are drifting and nobody notices? Coherence degradation isn't self-announcing.

**Problems with sliding window as the "ship first" default:**

1. It silently breaks critic continuity. A critic who can't see their own turn-10 objection will unknowingly repeat it at turn-25. The transcript looks coherent. The reasoning is circular.
2. "80% of window limit" assumes uniform turn size. Proposal turns are 300 words. Critique turns are 600. Your buffer calculation is wrong by a factor of 2 depending on which agents dominate.
3. Sliding window is not "simpler than everything proposed" — it's simpler to *describe* but requires the same dispatch-time calculation as any other strategy.

**The real unstated assumption across all three proposals:** that agents reading the same context will produce meaningfully different outputs than agents reading truncated context. Has anyone verified that model behavior actually changes with context length in this task domain? You might be solving a problem that doesn't manifest.

The Flow Orchestrator's two-mode system is the least bad option — but only if "anchored" gets defined as a hard constraint, not a preference. Otherwise summarization drift poisons both modes.

## Round: EVALUATE

### The Product Oracle (user advocate)

## The User Doesn't Experience Context Strategy. They Read the Morning Brief.

Everything proposed so far optimizes agent cognition. Nobody asked: does the Morning Brief get better?

That's the job. Not "coherent multi-agent reasoning." Not "semantic distance from prior turns." The user wakes up, reads a brief, decides whether overnight compute was worth running. That's the whole product.

**Through that lens, here's what I see:**

The Systems Pragmatist is right that we haven't stress-tested 30-turn sessions. But the Adversarial Critic is right that "measure first" without exit criteria is just delay with better posture. Both are avoiding the actual decision.

The Flow Orchestrator's two-mode proposal is the only one I'd ship — but not because it's architecturally elegant. Because it's the only one a solo builder can configure in an afternoon without reading a paper on group creativity.

One boolean in agent YAML. One branch in dispatch. That's a config experience I can defend.

**What I want protected:**

The critic seeing its own prior objections isn't an abstract coherence problem — it produces a Morning Brief where the same concern appears three times rephrased. Users notice that. It feels like the system is spinning. The "anchored" mode directly addresses this.

**What I'd kill:**

The four-role taxonomy. Implementer context strategy. Any summarization logic that runs before you have a session that actually breaks.

**My call:** Ship two-mode anchored/accumulating. Run ten sessions. Read the Briefs. Does the critique section feel sharper? That's your measurement.

### The Context Surgeon (context efficiency evaluator)

## Nobody Has Run the Numbers.

The Adversarial Critic's turn-size variance point is the only concrete technical observation in this thread. Everything else is architecture debate without a cost model.

Let me be direct: before choosing a strategy, you need to know **when the problem actually hits.** 

Assume 200K context window. A 30-turn session with mixed 300/600-word turns averages ~450 words × 30 = ~13,500 words of history. That's roughly 18,000 tokens. You're not close to the limit. The window problem may not exist yet at your current session lengths.

**What this means for the proposals:**

- Sliding window: premature optimization for a constraint you haven't hit
- Summarization: premature complexity for the same reason  
- Two-mode anchored/accumulating: the right shape, but "anchored" still needs a token budget, not a vibe

**The Product Oracle is right about the exit criterion:** Morning Brief quality is measurable. But "read ten Briefs" without logging context sizes per session gives you outcome data with no causal handle.

**What I'd actually ship:** Full history until you hit 60% of window. Log token counts per session. The moment any session exceeds threshold, you have real data on turn distribution, which agents are verbose, and where coherence actually degrades. Then the two-mode proposal has something to calibrate against.

Don't build context management infrastructure before you have a session that needs it. That's the waste.

<!-- complete -->
