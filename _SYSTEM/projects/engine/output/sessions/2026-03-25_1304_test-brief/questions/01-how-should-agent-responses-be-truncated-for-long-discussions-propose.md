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


<!-- complete -->
