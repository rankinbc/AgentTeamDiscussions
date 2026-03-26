# What is the minimum viable V2?

*Generated: 2026-03-26 12:53 | Q10 | 213s | Mode: compete*

## Decisions

### DECIDED: Round-Type Prompt Differentiation Is the Highest-Priority V2 Change

Every agent converged on this unanimously. Propose rounds, critique rounds, and evaluate rounds currently receive the same cognitive framing. V2 ships three distinct prompt templates keyed to round type:

- **Propose**: Expansive, generative framing. The agent's task is to produce an original position with supporting reasoning.
- **Critique**: Adversarial, gap-finding framing. The agent's task is to stress-test proposals, identify unstated assumptions, and find failure modes.
- **Evaluate**: Integrative, trade-off framing. The agent's task is to weigh competing positions, identify where they agree beneath surface disagreement, and recommend resolution.

Round type is already known by the round runner. PromptBuilder already assembles prompts per-agent-per-round. The implementation is a template selector on `round_type`. No new subsystems. No new configuration surfaces. The round-type templates live alongside existing prompt templates.

This is the only V2 change with unanimous support, minimal structural risk, and directly measurable impact via paired human comparison against V1 output using the same agents and topics.

### DECIDED: Blind Proposals Ship as a Real PromptBuilder Change, Not a Prompt-Instruction Test

The Critic raised a valid concern: nobody has measured actual proposal divergence in V1. The Oracle proposed a "zero-cost" prompt-only test where agents are instructed to generate positions independently while still receiving prior responses in context.

The Code Surgeon killed that proposal on methodological grounds: telling an LLM to ignore context it can see is not a controlled test. Positional context dominates instructions. The only valid test of whether removing prior proposals changes behavior is to actually remove prior proposals.

The PromptBuilder change is small: during propose rounds, withhold prior agent responses from the assembled prompt. Agents receive their identity layer, the question context, and the round-type template — but not other agents' proposals from the same round. Critique and evaluate rounds continue to receive all prior responses.

This is the second V2 change. It addresses the single largest structural flaw in V1 discussion dynamics: anchoring bias from sequential proposal visibility. The architectural cost is a conditional in PromptBuilder, not a new subsystem.

### DECIDED: Overnight Completion Report Is the Third Minimum-Viable Change

The Flow Orchestrator identified this and no other agent contested it. Currently, a completed overnight session produces output files that require individual inspection. A failed session produces a crash log. Neither tells the user what happened at a glance.

The completion report is a single structured artifact written by SessionRunner at session end (success or failure). It contains:

- Session title and timestamp
- Questions attempted and their completion status
- Wall-clock duration
- Retry events (count and which questions triggered them)
- Final status (complete, failed with location of failure, timed out)

No LLM generation. No quality assessment. Mechanical facts only. This was already decided as the only new artifact for overnight operation. It ships as part of minimum viable V2 because it transforms overnight runs from "forensic reconstruction" to "read one file."

### DECIDED: Tiered Summarization Is Not Minimum-Viable

The Systems Pragmatist raised the fatal objection: tiered summarization asks an LLM to compress prior rounds while preserving the specific technical nuances agents need to critique effectively. Lossy compression of argument structure — with no detection mechanism for when compression has corrupted the discussion state — risks silently degrading output quality.

Tiered summarization remains on the V2 roadmap. The eviction order and trigger mechanism are already decided. But it does not ship in the minimum viable set because the project has no way to detect when summarization has destroyed information that matters.

### DECIDED: BIT System and Personality Transition Are Not in the Minimum-Viable Set

Both were already excluded from the critical path by prior decisions. The swap test has not been run. Whether personality is load-bearing is unknown. These are independent workstreams that layer on after the structural changes ship.

### DECIDED: Prompt Output Snapshots Remain the Prerequisite for All V2 Validation

Already decided. Reiterated here because all three minimum-viable changes require paired comparison against V1 output. You cannot validate round-type differentiation or blind proposals without before/after prompt snapshots.

---

## The Minimum Viable V2

Three changes. Two touch PromptBuilder. One touches SessionRunner. No new subsystems, no new configuration surfaces, no new runtime infrastructure.

| Priority | Change | Touches | Validates Against |
|----------|--------|---------|-------------------|
| 1 | Round-type prompt differentiation | PromptBuilder, templates | Paired comparison: do round-specific prompts produce more focused agent output than undifferentiated prompts? |
| 2 | Blind proposals | PromptBuilder | Paired comparison: do isolated proposals surface perspectives that sequential proposals miss? |
| 3 | Overnight completion report | SessionRunner | Operational: can the user determine session outcome from one file? |

Ship in this order. Validate each with five paired runs before proceeding to the next. If round-type differentiation shows no measurable improvement in paired comparison, stop and diagnose before shipping blind proposals — the problem may be upstream of what these mechanisms address.

---

## What Was Rejected and Why

| Proposal | Raised By | Rejected Because |
|----------|-----------|-----------------|
| Tiered summarization as minimum-viable | Cognitive Architect | Lossy compression with no quality detection mechanism risks silent degradation (Pragmatist) |
| Prompt-only anchoring test as gate for blind proposals | Adversarial Critic, Product Oracle | Methodologically unsound — instructing an LLM to ignore visible context does not test the effect of removing that context (Code Surgeon) |
| Counting tiered summarization as separate from blind proposals | Cognitive Architect | Inflates feature count; summarization is plumbing that ships as part of context assembly, not an independent feature (Orchestrator) |
| Instrumentation as the minimum viable V2 | Adversarial Critic | Produces data for developers, not better output for users (Oracle) |

---

## Open Risks

**Blind proposals create a cold-start problem for critique rounds.** Proposals generated in isolation may address different facets of the question, making cross-proposal critique difficult. The critique round template must account for potentially non-overlapping proposals.

**Round-type templates have no empirical basis yet.** What constitutes a good "critique framing" versus a good "propose framing" is hypothesis, not evidence. The five paired runs are the evidence-generation mechanism.

**Halt-on-failure still kills overnight sessions.** The completion report tells you where the session died. It does not prevent the death. For sessions longer than four questions, the expected overnight output remains partial given observed Claude CLI timeout rates. This is a known limitation, not a V2 problem — but it bounds how much the completion report actually improves the overnight experience.
<!-- complete -->
