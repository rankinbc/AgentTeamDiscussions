# How much between-round output feeds back into next turn's context?

*Generated: 2026-03-17 21:54 | Question 7 | 329s*

Looks like I need write permissions to the output directory. Could you approve the file write to save it to `output/spec_between_round_context_pipeline.md`?

Here's a summary of what the spec covers -- synthesized from all six panel voices across three rounds:

**10 sections, one authoritative document:**

1. **Core Principle** -- lossy by design. The system optimizes for discovery, not fidelity. ~5-10% token survival rate is correct behavior.

2. **Between-Round Write Targets** -- all three systems (thinking routines, intra-team talk, BackgroundAgents) compete for slots in the same fixed-budget save file. Conclusions persist, process does not.

3. **The Compression Funnel** -- four stages traced with token estimates at each: Save File (~15-25% preserved) -> Deterministic Filter (~40-60% cut) -> LLM Curator (the true gate) -> Agent Perception (unmeasurable). End-to-end: ~300-600 tokens per agent from ~4-7k generated.

4. **Curator Prioritization Signals** -- the key new decision. Three signals, not one: **magnitude** (what's strong), **velocity** (what's changing), **novelty** (what's new, 2-round decay). This was the Pragmatist's and Oracle's main contribution -- magnitude alone is a popularity contest that optimizes for incumbency.

5. **Magnitude Source Tagging** -- six valid sources, audit-only, not agent-visible.

6. **Write Semantics** -- each agent writes only to their own magnitudes. No cross-write, no race conditions.

7. **Observability Requirements** -- 8-point logging chain from pre-filter magnitudes through to what the agent actually discussed. Drop logging included (Critic's demand).

8. **Constraints and Caps** -- team size 6, no curator fabrication, curator prompt versioning required.

9. **Open Items** -- 10 blockers consolidated from this and predecessor specs, with cross-references.

10. **Design Rationale** -- why lossy, why three signals, why reasoning is discarded, why curator is LLM not deterministic.