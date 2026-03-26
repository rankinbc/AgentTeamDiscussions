# Is the UNKNOWN estimation approach viable for game generation?

*Generated: 2026-03-26 18:58 | Q5 | 200s | Mode: compete*

## Decisions

### 1. The UNKNOWN Estimation Approach Is Retained Unchanged

`[UNKNOWN: est X-Y]` tags are kept exactly as currently specified. No new fields, no coupling annotations, no range-distribution metadata. The format is optimal for its actual current consumer: a human reader who applies judgment when encountering an unfindable value. Cascading arithmetic errors are not a failure mode for human-readable output.

### 2. Coupling Annotation Proposals Are Rejected as Premature

The `chain:<downstream>` annotation (Cognitive Architect) and the co-location-as-coupling-signal approach (Flow Orchestrator) are both rejected.

**Why the chain annotation fails:** It requires a cross-file dependency resolution pipeline — parse all UNKNOWN tags, extract chain references, resolve free-text strings to file locations, build a dependency graph, topologically sort, lock and propagate. That pipeline is unspecified and non-trivial. Naming a downstream target in a tag does not constitute specifying how a generator resolves it.

**Why co-location fails:** It handles the local case only. The dominant failure mode in a hierarchically organized knowledge base is transitive cross-file dependencies — combat formulas referencing character stats referencing level curves referencing economy. These live in different files by architectural intent. Co-location solves the easy couplings and ignores the hard ones.

**Why both fail at the root:** Both proposals design representation for a generator whose value-selection behavior is unspecified. A generator that picks a point value from `[UNKNOWN: est 50-200]` — whether by uniform random, midpoint, or weighted sampling — has not been defined. Annotation schemes for a black box are overhead with no payoff.

### 3. The Cascade Problem Is Real but Currently Dormant

The cascade inaccuracy concern is structurally valid: interacting ranges compound non-linearly. Two independent UNKNOWN estimates produce bounded output; two coupled unknowns feeding the same formula produce a variance space that can span unplayable extremes. This is an arithmetic fact, not a labeling problem.

However, this problem only instantiates under programmatic consumption — when a deterministic generator treats UNKNOWN values as numeric inputs to formula chains. That generator does not exist. Adding coupling machinery now is optimizing for a hypothetical system at the cost of the actual one.

### 4. Ranges Encode Ignorance, Not Variance

`[UNKNOWN: est 50-200]` does not mean enemy HP is drawn from a uniform distribution over that interval. It means a researcher estimated within a 4x spread because the actual value is not currently findable. Downstream statistical arithmetic on this signal amplifies noise. Treating UNKNOWN estimates as distribution parameters is false precision.

The appropriate consumer behavior is: use the estimate as a plausibility signal and a research gap indicator. A human designer reading `[UNKNOWN: est 50-200]` understands the value warrants investigation; they do not sample from it.

### 5. A Re-Entry Condition Is Added to the Conventions Document

Deferral without a trigger is permanent abandonment. The shared conventions document must record the following condition explicitly:

> **UNKNOWN Coupling — Deferred.** When a generator specification exists that consumes UNKNOWN values as programmatic numeric inputs — defining how point values are selected from estimated ranges and how those values propagate through formula chains — the coupling representation question must be revisited at that time. The cascade problem is real and will require a solution at that layer. This decision defers it, it does not dismiss it.

This condition is written into the conventions document as a named open item, not buried in a ledger entry. It re-enters the design process when generator architecture is specified, not before.

### 6. What Is Not Decided Here

- How a future generator selects a point value from an estimated range (uniform, midpoint, median-weighted, or other)
- Whether future coupling representation uses annotation, co-location, a separate dependency manifest, or a constraint solver
- Whether the constraint solver approach becomes viable once formal playability bounds are known
- How UNKNOWN estimate rot interacts with coupling once a generator exists (that problem is addressed separately under the estimate rot lightweight fix from Q4)
<!-- complete -->
