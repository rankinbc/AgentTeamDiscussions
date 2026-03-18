# How should the orchestrator handle a question that produces contradictory proposals?

*Generated: 2026-03-18 06:09 | Question 1 | 129s | Mode: compete*

## Decisions

### D1: Default Path is Merge; Divergence Path is Deferred

The synthesis step uses a single merge prompt for all proposals in V1. There is no automated contradiction detection, no alternate prompt template, and no branching logic based on critique output.

Rationale: Reliable contradiction detection from stateless LLM calls is an unsolved classification problem. Building detection infrastructure before observing real contradictions in actual system output produces speculative code with no grounding. The merge path ships first. Real output teaches what "incompatible" looks like.

### D2: Present Both Proposals When Divergence is Detected

When a future version introduces divergence detection, the synthesis step presents both proposals side by side. It never merges incompatible proposals into a single recommendation.

The output structure for a divergent pair:

- **Proposal A summary** -- what it optimizes for, what it sacrifices (2-3 sentences)
- **Proposal B summary** -- what it optimizes for, what it sacrifices (2-3 sentences)
- **Point of conflict** -- one sentence identifying the specific assumption or structural choice where they diverge

Total budget: 150 tokens maximum. No recommendation. No confidence score.

Rationale: Merging incompatible designs produces incoherent output that loses the distinctive strengths of each original. Preserving the disagreement in minimal form respects the user's attention budget while giving them the information needed to decide.

### D3: No Confidence Tags

The synthesis step never produces confidence scores (high/medium/low) on recommendations or comparisons. An uncalibrated LLM assigning confidence labels creates false signal that the user cannot verify or trust.

When the system needs to convey uncertainty, it quotes the specific disagreement verbatim: "Agent A proposed X. Agent B proposed the opposite." Direct quotation is more trustworthy than a synthetic confidence metric.

### D4: No Synthesizer Recommendation for Contradictions

When two proposals are flagged as divergent (in the future version that supports this), the synthesis step does not pick a winner or state a preference. It produces only the structured comparison from D2.

Rationale: The synthesizer is a stateless LLM call with no ground truth, no user context beyond what is in the prompt, and no domain expertise. A recommendation from this position carries no signal and risks anchoring the user toward a choice the system is not qualified to make. The Morning Brief surfaces the fork as a "needs decision" item. The human decides.

### D5: Divergence Detection Belongs in the Synthesizer, Not the Critique Round

When contradiction detection is eventually built, it runs inside the synthesis step, not the critique round. The synthesizer already holds both proposals in context. The critique round agents each see only one proposal's context plus the other's summary, making them poorly positioned to assess structural compatibility.

Detection heuristic (deferred to implementation): the synthesizer evaluates whether the two proposals require mutually exclusive structural choices (different data models, incompatible control flow, contradictory state management). If yes, it switches from merge output to comparison output. The specific threshold and test criteria will be derived from observed examples of real contradictions in session output.

### D6: Divergence Reports Must Be Rare

If more than roughly 1 in 5 topics in a session produce "needs decision" items, the mechanism is over-triggering and the user will stop reading them. The detection threshold, once implemented, must be tuned to flag only structural incompatibilities, not surface-level disagreements or differences in emphasis.

Monitoring: track the ratio of divergence flags to total topics per session. If the ratio exceeds 20% across multiple runs, tighten the detection criteria.

---

## Synthesis Rules

### V1 Behavior (Ship This)

1. The synthesis step receives all proposals and all critique output.
2. It runs a single merge prompt. No branching, no detection, no alternate templates.
3. Output is a single synthesized position per topic.
4. If the merged output is incoherent, the user catches it during Morning Brief review. This is acceptable. The human reviews all output in V1.

### V2 Behavior (Build After Observing Real Output)

1. The synthesizer receives all proposals and critique output.
2. Before merging, it evaluates whether proposals require mutually exclusive structural choices.
3. If yes: produce the minimal comparison structure (D2). Tag the topic as "needs decision" in session output. The Morning Brief surfaces it.
4. If no: produce the normal merged synthesis.
5. No confidence tags. No recommendation. No rationale beyond the point-of-conflict sentence.

### Output Structure for Divergent Topics

```
## [Topic Name] -- NEEDS DECISION

**Proposal A** ([Agent Name]):
[What it optimizes for. What it sacrifices. 2-3 sentences.]

**Proposal B** ([Agent Name]):
[What it optimizes for. What it sacrifices. 2-3 sentences.]

**Conflict:** [One sentence: the specific assumption or structural choice where they diverge.]
```

This block replaces the normal synthesis output for that topic. It appears in the session artifacts and is flagged in the Morning Brief.

### What This Design Explicitly Excludes

- **Confidence scoring** on any synthesis output (D3)
- **Synthesizer recommendations** for divergent proposals (D4)
- **Critique-round detection** of incompatibility (D5)
- **Assumption mapping** beyond the single conflict sentence (token budget constraint)
- **Multi-proposal divergence handling** (three-way contradictions where A conflicts with B but not C) -- deferred until the system runs with more than two proposers

### Failure Modes Accepted in V1

| Failure | Impact | Mitigation |
|---|---|---|
| Merge produces incoherent output from incompatible proposals | User reads mush in Morning Brief | Human review catches it; real examples inform V2 detection |
| Good ideas lost in bad merge | Weaker synthesis output | Proposals preserved in session history for manual review |
| User doesn't notice incoherence | Wrong direction taken | Low risk given V1 is advisory, not autonomous |