### The Cognitive Architect (creativity engine designer)

# The Only Metric That Matters Is Decision Divergence

Forget semantic similarity scores. Forget embedding distance. Those measure *linguistic* variation, which is exactly the theater we're trying to detect. Two agents can produce outputs with cosine similarity of 0.3 and still recommend identical architectures using different metaphors.

**Decision-point extraction is the validation mechanism.** Every design question contains implicit binary or multi-way trade-offs. "Should we use a queue or a pub/sub?" "Latency or throughput?" "Flexibility or simplicity?" A post-round extractor identifies the concrete decision points each agent addressed and maps their positions. If five agents all land on the same side of every trade-off but describe it with different adjectives, your BITs are cosmetic. If three agents cluster on option A and two on option B with structurally different justifications, you have real cognitive diversity.

**Implementation: the Divergence Ledger.** After each proposal round, an LLM pass extracts `(decision_point, position, justification_type)` triples from each agent's output. Score the round on two axes: (1) **positional spread** -- did agents actually disagree on decisions? (2) **justification orthogonality** -- did they use different *reasoning strategies* (cost argument vs. risk argument vs. user-impact argument), not just different words?

This runs as always-on instrumentation, consistent with Q4 decisions. No flags. It layers onto the existing anti-coordination scoring. It produces a per-question diversity score that's auditable by humans: you can read the extracted triples and immediately see whether the engine is generating real intellectual friction or performing it.

The baseline comparison is V1 output. Run identical briefs through both. If V2 doesn't measurably increase positional spread, the BIT system is decoration.

## Position Summary
I advocate decision-point divergence scoring -- extracting concrete trade-off positions from agent outputs and measuring whether agents actually land on different sides of real decisions with structurally different reasoning. I reject embedding-distance and semantic-similarity approaches because they measure linguistic variation, which is precisely the cosmetic diversity the research doc warns about. The only honest test of cognitive diversity is whether agents produce genuinely incompatible recommendations that force real synthesis, not whether they *sound* different while agreeing.

### The Flow Orchestrator (mechanical flow designer)

# The Divergence Ledger Adds an LLM Pass You Haven't Costed

The Cognitive Architect's instinct is right -- positional spread beats semantic similarity. But the proposal hand-waves the hardest part: **who runs the extraction, when, and what happens when it's wrong?**

"An LLM pass extracts triples" is doing enormous work in that sentence. That's a full Claude call per agent per round, parsing unstructured prose into structured `(decision_point, position, justification_type)` triples. You've just added N agent calls to every round's critical path. At 5 agents and 3 rounds, that's 15 extra LLM invocations per question -- purely for instrumentation. The extraction prompt itself becomes a design surface that needs validation. Who validates the validator?

**The cheaper version that actually ships:** skip real-time extraction entirely. The validation framework is a **post-session offline tool**, not a runtime component. You run identical briefs through V1 and V2. A human reads both transcripts and codes the decision points manually for the first 5-10 sessions. That produces ground truth. *Then* you build automated extraction calibrated against human judgment. You don't instrument the engine until you know what correct instrumentation looks like.

This respects the decided critical path: blind proposals ship first, instrumentation layers on independently. Building a Divergence Ledger into the round loop couples validation to execution before either is proven.

**The sequence is:** ship V2 mechanics, collect output pairs, human-code divergence manually, identify patterns, *then* automate. Three of those steps require zero code changes.

## Position Summary
I advocate post-session offline comparison as the validation mechanism -- human-coded decision-point divergence on matched V1/V2 output pairs, with automated extraction built only after ground truth exists. I reject runtime divergence extraction because it adds 15+ uncosted LLM calls per question, creates a validation-of-the-validator problem, and couples instrumentation to the execution path before either is proven. The cheapest honest test is a human reading two transcripts side by side.


<!-- complete -->
