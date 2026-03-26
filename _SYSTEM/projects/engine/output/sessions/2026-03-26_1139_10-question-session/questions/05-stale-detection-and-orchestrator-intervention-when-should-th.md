# Stale detection and orchestrator intervention: when should the system disrupt a conversation?

*Generated: 2026-03-26 11:58 | Q5 | 244s | Mode: compete*

## Decisions

### Primary Decision: Fixed Round Counts Per Mode, No Runtime Stagnation Detection

The system uses fixed round counts configured per mode in team YAML. No runtime stagnation detection, no dynamic termination, no orchestrator intervention mechanisms.

**Rationale:** Four of five agents converged on this position through independent reasoning paths. The user never sees stagnation metrics — they see output quality. No evidence exists that dynamic intervention improves output quality over fixed rounds. Every runtime detection mechanism proposed (transformation tracking, artifact counting, cost modeling) requires either additional LLM calls on the critical path or brittle heuristics, both adding complexity against an undemonstrated problem.

**What this means concretely:**
- Round counts are a per-mode configuration field in team YAML, set at authoring time by a human.
- The orchestrator runs exactly the configured number of rounds, then proceeds to synthesis.
- No LLM calls are made to judge discussion quality mid-session.
- No round is skipped or added based on runtime analysis.

### Secondary Decision: Instrument Output Quality Post-Hoc

Ship per-round novelty logging to determine whether fixed rounds consistently waste final rounds or produce diminishing returns. This is observational instrumentation in the output pipeline, not a runtime control mechanism.

**Rationale:** The system already has an evaluation pipeline. The right place to detect whether stagnation is a real problem is in post-session analysis of output files, not in a runtime classifier. If the data eventually shows that fixed rounds produce measurably worse output in predictable patterns, that evidence justifies revisiting dynamic termination.

**What to instrument:**
- Per-round word/proposal/objection counts (cheap structural metrics, no LLM scoring).
- Evaluation scores correlated with round number to identify diminishing-return patterns.
- Session-level output quality compared across different round count configurations.

### Tertiary Decision: If Evidence Warrants Revisiting, Start With Early Termination — Not Intervention

If instrumentation data demonstrates that fixed rounds consistently waste final rounds, the first response is early termination (ending the round sequence and running synthesis on what exists). The system does not resurface dropped threads, inject constraints, or steer discussion content.

**Rationale:** The Adversarial Critic correctly identified that termination is itself a content judgment. That reality is unavoidable in any dynamic system. But termination is the *least* intrusive content judgment — it says "enough" without saying "talk about this instead." Thread resurfacing and constraint injection put the orchestrator in a content-generation role, which distorts discussion dynamics and couples orchestration reliability to LLM output quality.

---

## What the System Must Not Do

- **No LLM calls in the control plane to judge discussion quality.** Transformation tracking, semantic novelty scoring, and LLM-based stagnation detection are all rejected. Using the unreliable substrate to judge the unreliable substrate adds failure modes without proven benefit.
- **No orchestrator-generated content during discussion.** The orchestrator sequences and terminates. It does not resurface threads, inject constraints, add commentary, or steer agent attention. The moment it takes a position, it distorts the dynamics it exists to facilitate.
- **No runtime detection thresholds, tuning parameters, or stagnation classifiers.** These add configuration burden, edge cases, and user confusion when sessions end unexpectedly. One YAML field (round count) replaces all of it.

## What the System Should Do

- **Configure round counts per mode in team YAML.** Each mode already defines its round structure (propose, critique, evaluate). The count is part of that structure. If a mode needs a different number of rounds, change the config.
- **Log structural metrics per round as part of normal output.** Round transcript length, number of distinct positions, number of cross-references to other agents. These are cheap to extract from existing output format and accumulate evidence for or against the fixed-round approach.
- **Rely on the existing evaluation pipeline for quality signals.** Eval scores already capture output quality. Correlating eval scores with round count and mode configuration tells you whether stagnation is a real problem without adding runtime machinery.
- **Treat premature termination as more expensive than over-running.** The Adversarial Critic's asymmetry observation is valid even under fixed rounds: when choosing default round counts for new modes, err toward one more round rather than one fewer. A wasted round costs tokens; a missing round loses output permanently.

## Key Reasoning That Drove Consensus

**The Cognitive Architect** proposed transformation tracking — measuring whether agents incorporate each other's reasoning. The mechanism was intellectually rigorous but required per-agent LLM calls on the critical path, coupling control-plane reliability to the same unpredictable substrate being orchestrated. The core insight (measure engagement, not repetition) is preserved in the post-hoc instrumentation approach.

**The Flow Orchestrator** correctly rejected LLM-based detection but proposed artifact counting, which still requires runtime output parsing (either brittle string matching or another LLM call). The stronger contribution was the principle that the orchestrator sequences and terminates, never generates content.

**The Adversarial Critic** landed the sharpest critique: termination is a content judgment, and pretending otherwise is intellectual dishonesty. Both the Architect and Orchestrator claimed the orchestrator should be "content-free" while proposing termination decisions. Fixed round counts absorb this critique by making the content judgment once, at config time, by a human.

**The Systems Pragmatist** identified the foundational problem: zero ground truth for stagnation. No labeled data, no validation signal, no way to tune any classifier. Every detection mechanism is speculative engineering against an unmeasured failure mode. Ship the simplest thing and measure whether it breaks.

**The Product Oracle** and **Context Surgeon** reinforced from user-experience and token-economics perspectives respectively. The user reads design docs, not stagnation metrics. Tokens spent on runtime introspection are stolen from agent reasoning in an already constrained system.

## Open Considerations

- **Default round counts for new modes** should be informed by accumulating instrumentation data. Current three-round structures (propose-critique-evaluate) are the baseline; evidence may suggest some modes benefit from a fourth round.
- **If a future mode explicitly requires dynamic length** (e.g., a freeform brainstorming mode), that mode can implement its own termination logic as a mode-specific behavior, not a general orchestrator capability. The burden of proof is on the mode to justify the complexity.
- **The instrumentation data may never show a problem.** That outcome is fine. Not every anticipated failure mode materializes, and the system is better for not having built machinery against a phantom.
<!-- complete -->
