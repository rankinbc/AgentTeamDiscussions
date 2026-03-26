# How should we validate that V2 mechanisms actually work?

*Generated: 2026-03-26 12:36 | Q5 | 200s | Mode: compete*

## Decisions

### DECIDED: Paired Human Comparison Is the Validation Framework

V2 validation is a prompt engineering A/B test, not a systems measurement problem. Every agent is a stateless Claude subprocess -- the only thing V2 changes is prompt text. Validation reduces to whether changed prompts produce better output. The validation framework is paired V1/V2 runs with direct human judgment of Morning Brief quality.

### DECIDED: Prompt Output Snapshots Are the Prerequisite

Before any PromptBuilder modification, snapshot the exact prompts and full outputs for at least 5 existing briefs under V1. These snapshots are the baseline. Without them, no comparison is possible and all subsequent measurement is confounded. This aligns with the already-decided "Prompt Output Snapshots Are the Non-Negotiable First Deliverable" from Q2.

### DECIDED: The Evaluation Question Is "Did V2 Surface a Perspective V1 Missed?"

After running identical briefs through V2, a human reads both Morning Briefs and answers one question: did V2 surface a perspective, trade-off, or failure mode that V1 missed? This is the only metric that maps to the system's purpose -- surfacing angles the user would not have considered alone. Internal mechanics like positional spread or embedding distance do not matter if the user-facing output is unchanged.

### DECIDED: Five Paired Runs Before Declaring Success or Failure

Run 5 identical briefs through both V1 and V2. If 3 or more show meaningful improvement in the Morning Brief, the mechanism works -- ship it and iterate. If fewer than 3 show improvement, the mechanism is cosmetic regardless of what internal metrics might suggest. This threshold is deliberately low because the goal is signal detection, not statistical proof.

### DECIDED: No Automated Divergence Scoring in V2

Decision-point extraction via LLM passes is rejected for V2. It adds 15+ uncosted LLM calls per question, creates a validator-of-the-validator problem (using Claude to judge whether Claude outputs are diverse), and rewards contrarianism identically to genuine independent reasoning. Automated divergence scoring is a candidate for a future version only after manual observation has established what "genuine diversity" looks like in this system's output.

### DECIDED: No Runtime Instrumentation for Validation

Validation is post-session and offline, not coupled to the execution path. The round loop does not change to accommodate measurement. This respects the critical path decisions: blind proposals ship first, instrumentation layers on independently. Coupling validation to execution before either is proven creates unnecessary risk.

### DECIDED: Anti-Coordination Scoring (Already Decided Always-On) Provides the Only Automated Signal

The Q4 decision to ship anti-coordination scoring as always-on instrumentation stands. It provides a lightweight automated signal without adding LLM calls to the critical path. But it is a secondary indicator, not the primary validation. A high anti-coordination score with no visible improvement in the Morning Brief means the scoring is wrong, not that the output is secretly better.

### DECIDED: Contrarianism Detection Is a Human Judgment Call, Not an Automated Check

The concern that agents might produce surface-level opposition ("Agent A says X, so I say not-X") rather than genuine independent reasoning is valid. But at current session volumes, a human reading the transcript detects this immediately -- an agent that disagrees without substance is obvious in prose. Automated contrarianism detection is not worth building until session volume exceeds what one person can read.

### DECIDED: No Formal Experimental Design at N < 20

Controlled-input evaluation, matched-pair statistical testing, and ground-truth extraction pipelines are all premature at current session volumes of a few per week. Building measurement infrastructure for a sample size of 5-10 is engineering theater. The validation framework scales to formal methods later if session volume justifies it.

### DECIDED: Measurement Infrastructure Is a Spreadsheet

Track paired run results in a simple format: brief name, V1 Morning Brief quality (notes), V2 Morning Brief quality (notes), verdict (better/worse/same), specific perspectives V2 surfaced that V1 missed. No database. No dashboard. No scoring pipeline. Sophistication comes after the data justifies it.

---

## Design

### Validation Sequence

1. **Before touching PromptBuilder:** Snapshot V1 prompts and outputs for 5 briefs covering different topic types and complexities. Store snapshots alongside session output.
2. **After shipping blind proposals:** Run the same 5 briefs through V2. Store V2 output separately.
3. **Human comparison:** Read both Morning Briefs for each pair. Record whether V2 surfaced perspectives V1 missed. Note specific examples.
4. **Threshold check:** 3 of 5 improved = mechanism works, continue shipping V2 features. Fewer than 3 = stop and investigate before building further.
5. **Ongoing:** As additional V2 features ship (phases, BITs, stale detection), repeat paired runs on the same 5 briefs to track whether each feature moves the needle.

### What Counts as "Better"

A V2 Morning Brief is better than V1 if any of the following are true:

- It identifies a trade-off or failure mode that V1's Morning Brief did not mention
- The synthesis resolves a genuine disagreement between agents rather than summarizing consensus
- The design doc contains a recommendation that contradicts another agent's recommendation, with both positions substantively argued
- A human reader says "I hadn't considered that" about something in V2 that is absent from V1

A V2 Morning Brief is **not** better merely because:

- Agents used different vocabulary or metaphors
- The word count increased
- More "perspectives" appear but all reach the same conclusion
- Agents explicitly reference disagreement without the disagreement producing a different recommendation

### Brief Selection for Paired Runs

The 5 baseline briefs should cover:

- At least one topic previously run in V1 with known weak output (establishes whether V2 fixes known problems)
- At least one topic with a clear right answer (tests whether diversity mechanisms cause agents to argue against correct positions)
- At least one open-ended design question with no clear right answer (tests whether diversity produces genuinely useful angles)
- At least one topic with many sub-questions (tests whether improvements hold across question volume)
- Vary team and mode across briefs to avoid testing only one configuration

### When to Revisit This Framework

Revisit the validation approach when any of these conditions are met:

- Session volume exceeds 20 paired runs and manual comparison becomes a bottleneck
- A pattern emerges in manual comparison that could be reliably automated (e.g., "V2 always improves on topics with 3+ sub-questions but not on single-question briefs")
- A new V2 feature (BITs, phases) changes the output structure enough that Morning Brief comparison is no longer apples-to-apples
- Someone other than the builder needs to run validation independently

Until then, the spreadsheet and human judgment are the validation system.
<!-- complete -->
