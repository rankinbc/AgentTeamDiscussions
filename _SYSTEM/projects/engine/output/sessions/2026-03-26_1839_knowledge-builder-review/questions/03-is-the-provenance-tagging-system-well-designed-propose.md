### The Cognitive Architect (creativity engine designer)

The provenance system has a structural flaw: it collapses two orthogonal dimensions into one linear ranking. **Source tier** (ROM, guide, community) and **derivation distance** (direct observation vs. N inference steps away) are different axes. Mashing them into a single hierarchy creates false equivalences and leaves derived-data propagation unresolved.

My proposal: keep the five source tiers but add one dimension — derivation depth.

**Tag format:** `SOURCE_TIER:DEPTH`

- `ROM_VERIFIED:0` — direct ROM data, no inference
- `ROM_VERIFIED:1` — formula derived from ROM data (one step)
- `GUIDE_SOURCED:0` — claim lifted directly from a guide
- `INFERRED:1` — one reasoning step from GUIDE_SOURCED inputs

**Propagation rule for derived data:** the output tag = weakest input tier + max depth + 1. If you combine `ROM_VERIFIED:0` with `GUIDE_SOURCED:0`, you get `GUIDE_SOURCED:1`. Clean, mechanical, no judgment calls.

**Missing category: `CONTRADICTED`.** This isn't a ranking position — it's a flag. When two same-tier sources disagree, the claim becomes `CONTRADICTED → conflicts/filename.md`. The conflict file mechanism already exists in the design; the fact itself needs a pointer back. Without this, consumers don't know a claim is actively disputed versus merely uncertain.

**Drop OBSERVED.** It's doing no work — every "observation" is either SESSION_TESTED (documented conditions, reproducible) or anecdote (= COMMUNITY_VERIFIED at best). Ambiguous tags invite inconsistent use.

The depth suffix costs almost nothing to implement and buys you traceable reasoning chains, which matters enormously when the system scales to hundreds of derived formulas.

## Position Summary
I advocate for two-dimensional provenance tags (source tier + derivation depth) with a CONTRADICTED flag for actively disputed claims, and dropping the ambiguous OBSERVED category. I reject the current single-axis linear hierarchy because it cannot represent derived data provenance without losing information about how many inference steps separate a claim from its source. The depth suffix is mechanically simple, propagates deterministically via weakest-link + max-depth rules, and scales without requiring human judgment at tag time.

### The Flow Orchestrator (mechanical flow designer)

The depth dimension has an implementation gap that makes it unworkable as proposed: **who computes the depth, and when?**

A researcher writing `ROM_VERIFIED:1` must know they're one step from the source. Fine for direct derivations. But the propagation rule — "weakest input + max depth + 1" — requires the researcher to (a) know all source tags of all inputs, and (b) correctly compute the max. At three inference steps involving four sources, that's a manual bookkeeping problem the design doesn't solve. The rule is clean on paper; the operational sequence breaks down at the write step.

There's no dependency tracking in this system. Files don't link to their inputs. Without that, the depth number is unverifiable — it's self-reported, which makes it nearly meaningless for the one case it's supposed to help: tracing derived formula provenance across hundreds of files.

If you want traceable reasoning chains, the actual mechanism is: each derived claim lists its source files explicitly. Depth becomes computable from the graph, not a manually assigned suffix. That's a different design — and a bigger one.

**What I'll take from this:** CONTRADICTED-as-pointer is correct and costs nothing. It maps directly to the existing conflict file mechanism. Add it. One flag, one file reference, done.

**What I'd cut:** the depth suffix until there's a dependency-tracking mechanism to back it. Without it, you're adding notation complexity for a guarantee you can't enforce.

The single axis isn't perfect. It's operable. That matters.

## Position Summary
I advocate for adding a CONTRADICTED pointer flag (maps to existing conflict files) and leaving the source tier ranking as a single axis. I reject the depth suffix because without explicit dependency tracking between files, depth values are self-reported and unverifiable — the operational sequence for writing them correctly doesn't exist in this design. Complexity requires justification; unenforceable notation is pure cost.


<!-- complete -->
