# Phase separation: brainstorm vs refine vs specify vs review.

*Generated: 2026-03-26 12:02 | Q6 | 231s | Mode: compete*

## Decisions

### Primary Decision: Defer Phase Separation Until Instrumentation Data Exists

Do not build any phase separation mechanism -- neither hard phase gates, soft phase detection, constraint gradient rounds, nor context injection enums. The question is data-gated, not design-gated.

**Rationale:** Every prior decision in this series points the same direction. Fixed round counts per mode are already decided (Q5). Post-hoc instrumentation is already decided but not yet shipped (Q5). Two-phase visibility with deterministic rotation is already decided (Q3). Building phase controls on top of these unexecuted decisions is premature engineering against an undemonstrated problem. No user signal, no output data, and no measurement infrastructure currently indicates that rounds produce insufficiently varied output.

**What this means concretely:**
- No new fields on round definitions in mode YAML.
- No runtime phase detection logic.
- No in-round similarity scoring or novelty counting.
- No new abstractions (constraint profiles, phase gates, context gradients).
- Current round definitions (propose, critique, evaluate) continue to drive context injection as they already do.

### Secondary Decision: Preserve the Constraint Gradient Concept as a Design Note

The Cognitive Architect's constraint gradient idea -- varying how much prior context enters each round's prompt and what agents must do with it -- is the leading candidate mechanism if data later shows phase separation is needed. Record it. Do not build it.

**What to record:**
- Open rounds: minimal context, agent sees question and identity only, measures novelty.
- Anchored rounds: full prior responses, prompt demands engagement with specific proposals, measures reference density.
- Bound rounds: synthesized positions plus criteria, prompt requires judgment, measures decision coverage.

This is a bookmark for future work, not a commitment to the specific mechanism.

### Tertiary Decision: Define the Instrumentation Gate That Would Reopen This Question

Phase separation becomes a real work item only when post-hoc instrumentation (from Q5) demonstrates **all three** of the following:

1. **Round-over-round output similarity is high.** Agents in round 1 and round 3 produce statistically similar output structure, vocabulary, and positions despite different round labels and context.
2. **The similarity is user-visible.** The Morning Brief or design docs show redundancy, lack of progression, or absence of refinement that a reader would notice.
3. **The similarity persists across multiple sessions and question types.** A single flat session is not evidence of a systemic problem.

If all three conditions are met, revisit this question starting with the constraint gradient mechanism. If only condition 1 is met but not 2, the problem is cosmetic and may not warrant engineering. If none are met, the current round structure is sufficient and this question is closed.

---

## What Was Rejected

### Hard Phase Gates with Different Agent Configurations
Rejected as unnecessary complexity. Swapping agents between phases adds configuration surface area, creates ordering dependencies, and presupposes that different agents are needed for different cognitive modes. No evidence supports this. The same agents with different prompts are more likely to produce useful variation than different agents with the same prompt structure.

### Soft Phase Detection by the Orchestrator
Rejected as vaporware. Detecting "natural phase shifts" in LLM output requires defining what phase-appropriate behavior looks like in text -- a research problem with no established ground truth. Runtime detection also contradicts the Q5 decision for fixed round counts and deterministic structure.

### Context Injection Enum (none / prior_responses / synthesized)
Rejected as premature, not as wrong. The Flow Orchestrator's proposal is clean engineering -- a single enum field on round definitions controlling what enters the prompt. It is the simplest possible implementation of the constraint gradient idea. But adding configuration knobs that no data says we need creates maintenance cost and cognitive load for mode authors with no validated benefit.

### Define Output Criteria Before Selecting a Mechanism
Rejected as premature rigor. The Adversarial Critic's position -- define measurable criteria for "brainstorm behavior" and "refinement behavior" before choosing a mechanism -- applies good methodology at the wrong stage. You don't write acceptance criteria for a solution to an undemonstrated problem. If instrumentation later confirms the problem exists, defining criteria becomes the correct first step. Right now it's busywork.

---

## What Changes Between Phases (Answering the Original Question)

The question asked what should change between phases: agent selection, anti-slop rules, communication mode, success criteria. The answer for now: **nothing changes, because phases are not yet a validated need.**

If data later warrants phase separation, the priority order for levers to adjust is:

1. **Context injection** (what prior material enters the prompt) -- highest-impact, lowest-cost lever. Already partially implemented through round-type differences.
2. **Prompt task framing** (what the agent is asked to do with the context) -- second lever, changes the instruction not the data.
3. **Anti-slop rules** (what output patterns are penalized) -- third lever, could suppress convergent language in divergent rounds or suppress novelty-seeking in convergent rounds.
4. **Agent selection** (which agents participate in which phase) -- last resort, highest configuration complexity, most likely to produce unintended interaction effects.

Communication mode and success criteria are evaluation concerns, not orchestration concerns. They belong in post-hoc measurement, not round configuration.

---

## Dissent Record

The Adversarial Critic raised a valid structural concern: both the constraint gradient and context enum proposals assume that controlling prompt context produces meaningfully different cognitive behavior in LLMs. This assumption is untested. Less context may produce hallucination rather than divergent thinking. More context may produce parroting rather than convergent judgment. The relationship between prompt constraint density and output cognitive character is an empirical question, not an engineering axiom. This concern should inform how instrumentation data is interpreted if this question is reopened.
<!-- complete -->
