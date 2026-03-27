### The Cognitive Architect (creativity engine designer)

## Role-Differentiated Memory Windows

The framing of "what history to keep" misses the real opportunity. The question isn't *how much* each agent sees — it's *which lens* each agent's summary is filtered through.

Here's the mechanism I'd commit to: **asymmetric role-filtered summarization**.

Every agent gets identical recent context (last 8-10 turns verbatim — recency matters for coherence). But beyond that window, agents don't receive the same compressed history. They receive summaries shaped by their cognitive role:

- **Adversarial Critic** gets a summary that foregrounds unresolved contradictions, waffled commitments, and assertions that went unchallenged
- **Synthesizer** gets a summary emphasizing convergence points and emerging consensus
- **Architect** gets a summary of structural decisions, constraints locked in, design space narrowed

This isn't cosmetic. It's grounded in transactive memory theory (Wegner, 1987) — effective groups distribute memory asymmetrically, with different members holding different knowledge chunks. Uniform truncation collapses this advantage. Every agent entering round 4 with identical compressed context will reason from identical priors, producing surface variation at best.

There's also a testable prediction here: agents with role-filtered history should produce *lower cross-agent semantic similarity* in proposals than agents receiving uniform summaries. That's a real metric, not a vibe.

Implementation: one summarization call per agent per truncation event, with a role-specific summarization prompt. Modest cost. High leverage.

The sliding window treats all agents as identical readers. They're not. Make the memory architecture match the cognitive architecture.

### The Flow Orchestrator (mechanical flow designer)

## Sequence First, Theory Second

The Cognitive Architect's proposal is intellectually coherent but describes a desired *output state*, not an *operation sequence*. Let me trace what actually has to happen:

1. Truncation event fires (trigger: undefined — token count? turn count? both?)
2. System calls summarization N times — once per agent role
3. Each call completes with unknown latency
4. Results stored — where? keyed how?
5. At turn dispatch, system fetches correct summary for each agent
6. Assembles context: `[role_summary] + [verbatim_window]`
7. Routes to agent

That's six distinct steps added to every turn past the threshold. Steps 2-4 introduce async coordination — if one summary call fails or times out, do you block the round? Retry? Fall back to uniform?

The trigger in step 1 is hand-waved. That's not a minor detail — it determines how often you pay this cost and whether it fires mid-conversation or between rounds.

My counter-proposal: **one shared summary + fixed verbatim window.** Single summarization call per truncation event. No routing complexity. No per-agent state management. All agents get identical compressed history plus last N turns verbatim.

The role-differentiation hypothesis is testable — I'd defer it to an experiment mode, not bake it into the base flow. The current system already has experiment modes for exactly this kind of variation.

Cut to what works. Instrument it. Then layer in asymmetry if the baseline proves insufficient.


<!-- complete -->
