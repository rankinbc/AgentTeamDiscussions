# Blind proposal rounds: how much independence before interaction?

*Generated: 2026-03-26 11:50 | Q3 | 253s | Mode: compete*

## Decisions

### Primary Decision: Two-Phase Visibility with Deterministic Rotation

Adopt a two-phase visibility model as the default for all discussion types:

- **Phase 1 (Blind Draft):** Each agent produces its response with no visibility into other agents' output. Mandatory for all discussion types, not just brainstorming.
- **Phase 2+ (Full Visibility):** All subsequent rounds expose the complete prior-round responses. Presentation order rotates deterministically across agents and rounds, logged for reproducibility.

Three-phase graduated exposure (blind draft, thesis-only reveal, full transcript) is deferred to the bake-off backlog. It is not rejected permanently but requires solving the thesis extraction problem and demonstrating measurable benefit before earning architecture commitment.

### Secondary Decision: Ship Diversity Instrumentation Alongside the Structure

Call-level instrumentation measuring position diversity across agents ships with the two-phase structure, not after it. This is not diagnostic tooling — it is the mechanism that validates whether blind rounds produce genuine independence or cosmetic variation from a shared underlying model.

### Tertiary Decision: Surface Diversity as a User-Visible Signal

Diversity measurement should appear on output documents (Morning Brief, design docs) as a confidence indicator, giving users visibility into whether a question received genuine multi-perspective debate or superficial agreement.

---

## Visibility Rules

### Blind Round (Round 1)

Each agent receives:
- Its own identity prompt (personality, position, technique layers)
- The question context (title, body, prior decisions)
- No output from any other agent

This is mandatory for every question in every session. There is no configuration bypass. The blind round exists because even convergent questions benefit from independently framed problem definitions, not just divergent solutions.

### Subsequent Rounds (Critique, Evaluate, etc.)

Each agent receives:
- Its own identity prompt with round-appropriate behavioral overlay
- The question context
- All prior-round agent responses, presented in deterministic rotation order

**Rotation rule:** For each agent assembling its context, the order of other agents' responses rotates based on the agent's index and the round number. The rotation sequence is logged per round in the session manifest for debugging and correlation analysis.

**Why deterministic, not random:** Reproducibility. Random order prevents correlating presentation position with influence on output. Deterministic rotation with logging lets instrumentation detect whether position-in-prompt systematically biases responses.

### Synthesis

The synthesis step receives all round transcripts in full. No visibility restrictions apply during synthesis.

---

## What This Does Not Include

**Thesis-only extraction.** No mechanism for extracting a position summary from agent output and presenting it separately from reasoning. This requires either an additional LLM call per agent per round transition (unacceptable cost increase) or reliable structured output parsing (not enforced today). If future instrumentation data shows that full visibility in round 2 causes measurable convergence that a partial reveal would prevent, the extraction problem gets solved then — justified by data, not theory.

**Parallel agent execution.** The engine runs agents sequentially via Claude CLI subprocesses. The blind round is "sequential with deferred visibility," not truly simultaneous. This is an implementation reality, not a design choice. Parallel execution is a separate infrastructure decision.

**Discussion-type exemptions.** No mechanism for skipping the blind round based on discussion type. The cost of a blind round is zero additional mechanism (agents already don't see each other in round 1). Building a bypass adds complexity for a scenario nobody has requested.

---

## Instrumentation Requirements

### What to Measure

**Position divergence:** After the blind round, compute a similarity metric across agent responses. This requires an LLM scoring call (lightweight, one call per question per round, not per agent) that rates how structurally different the proposed approaches are on a scale. Log this per question.

**Convergence rate:** Track how position divergence changes between rounds. High divergence in round 1 collapsing to near-zero in round 2 suggests the full-visibility phase is overwhelming independent positions. This is the signal that would justify revisiting graduated exposure.

**Rotation-position correlation:** Log which agent's response appeared first in each other agent's context. Over multiple sessions, correlate first-position with influence on subsequent responses (measured by semantic similarity to the final synthesis).

### Where It Surfaces

- **Session manifest (session.json):** Raw diversity scores per question per round, rotation order per agent per round.
- **Morning Brief:** A human-readable confidence line per question — something like "Position diversity: High (4 distinct approaches) / Moderate (2 clusters) / Low (broad agreement)." Exact format TBD during implementation.
- **Evaluation output:** If eval is run, diversity metrics feed into quality scoring.

### What Triggers Escalation

If instrumentation consistently shows one or more of:
- Blind-round divergence is no higher than a hypothetical no-blind baseline (the blind round adds nothing)
- Round 2 convergence is immediate and total (full visibility destroys independence)
- Rotation position consistently predicts influence (anchoring persists despite rotation)

Then the three-phase graduated exposure model re-enters active design as a candidate solution, with the extraction problem scoped against the specific failure mode observed.

---

## Implementation Sequence

1. **Deterministic rotation in context assembly.** Modify prompt assembly to rotate the order of prior-round responses based on agent index and round number. Log the order in the session manifest. This is a small change to PromptBuilder.
2. **Diversity scoring call.** Add a lightweight LLM call after each round that scores position divergence across agent responses. Log to session manifest.
3. **Morning Brief integration.** Pass diversity scores to the Morning Brief generator. Include a confidence line per question in the output.
4. **Bake-off variant.** Add three-phase graduated exposure as an optional mode in the bake-off framework, gated behind a flag, for comparative testing if and when diversity data justifies it.

---

## Dissenting Positions Preserved

**The Cognitive Architect** argued that thesis-only reveal is the critical mechanism for forcing genuine intellectual engagement — that full visibility causes pattern-matched rebuttal rather than independent counter-reasoning. This claim is plausible but unvalidated. The instrumentation framework is designed to detect exactly this failure mode. If convergence data confirms it, the thesis-only mechanism earns its complexity budget.

**The Adversarial Critic** argued that procedural blindness cannot produce meaningful cognitive diversity from a single underlying model, and that the entire visibility discussion is secondary to the shared-training bias problem. This is the deepest challenge to the architecture. Diversity instrumentation is the direct response — it will reveal whether structural independence produces genuine diversity or cosmetic variation. If the latter, the problem is in agent differentiation (persona design, priming strategies), not visibility structure.
<!-- complete -->
