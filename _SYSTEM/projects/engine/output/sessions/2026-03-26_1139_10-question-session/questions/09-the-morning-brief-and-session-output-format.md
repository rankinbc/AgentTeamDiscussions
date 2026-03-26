# The Morning Brief and session output format.

*Generated: 2026-03-26 12:13 | Q9 | 205s | Mode: compete*

## Decisions

### Primary Decision: Single Structured-Prompt Synthesis, No Verification Pass

The Morning Brief is produced by one LLM synthesis call per session using a structured prompt template that demands consistent output fields per question. No verification pass, no post-hoc extraction, no parallel structured artifacts.

**Rationale:** The discussion converged on a clear consensus: the current regex-based extraction from prose is fragile and must be replaced, but the proposed alternatives (structured decision records, tension maps, verification passes) all optimize fidelity for an output format that has never been validated with a real consumer. The cheapest reliable mechanism for consistent output is prompt structure, not pipeline complexity.

**Who agreed:** The Pragmatist, Oracle, and Context Surgeon aligned on shipping the simplest viable output. The Architect's core insight — that structure should be generated at synthesis time, not extracted after — was preserved in the structured prompt approach. The Orchestrator's principle of deterministic assembly was partially adopted (consistent template-driven prompts) without the full YAML pipeline.

**Who dissented:** The Adversarial Critic argued that single-pass synthesis is just as fragile as regex extraction with better cosmetics, and that silent failures (well-formed but fabricated output) are strictly worse than loud regex failures. This concern was acknowledged but not acted on — the counterargument (from the Pragmatist and Oracle) is that the human reader is a more effective verifier than an additional LLM pass, and the cost of verification doubles token spend for an unvalidated deliverable.

### Secondary Decision: No Dropped-Thread Detection

The Morning Brief does not attempt to surface ideas that were raised but never resolved. Transcript links serve this purpose.

**Rationale:** The Orchestrator and Oracle agreed that detecting absence — reasoning about what was *not* said — is an unreliable LLM operation. The Critic argued that omitting dropped threads creates a confirmation bias machine (only surfacing explicit conclusions). The resolution: transcripts already capture everything. The Morning Brief is a navigation aid, not a comprehensive record. If a dropped thread matters, it surfaces naturally in subsequent sessions.

### Tertiary Decision: Defer Structured Decision Records and Reading Instrumentation

Structured decision records (YAML per question), tension maps, and reading-behavior analytics are all rejected as premature. They may be revisited once the simple Morning Brief has been consumed across multiple real sessions.

**Rationale:** The Architect proposed full structured decision records as synthesis output. The Oracle and Pragmatist countered that this builds a parallel structure alongside the existing decisions ledger with no evidence that anyone consumes either programmatically. The Surgeon dismissed reading-behavior instrumentation as impractical for a CLI tool writing markdown files — the real feedback loop is Brian running sessions and identifying when output fails him.

---

## Morning Brief Specification

### What It Is

A single markdown document produced once per session, after all questions have completed synthesis. It is the entry point for anyone reviewing session results.

### How It Is Produced

One LLM synthesis call per session. The prompt template is structured — not free-form summarization. The synthesis agent receives all round outputs across all questions and produces markdown conforming to the template below.

The prompt template must demand, for each question:

| Field | Description |
|---|---|
| **Recommendation** | The dominant position that emerged. One sentence. |
| **Dissent** | The strongest counterargument and who made it. One sentence. |
| **Confidence** | How settled this feels: `settled`, `leaning`, or `contested`. |
| **Transcript link** | Relative path to the full question transcript. |

This is not the Architect's full YAML decision-record pipeline. It is a structured prompt that produces consistent markdown output — prompt discipline, not output parsing.

### What It Looks Like

```markdown
# Morning Brief: {Session Title}
{Date} | {Team} | {Mode} | {Agent Count} agents

## {Question 1 Title}
**Recommendation:** {one sentence}
**Dissent:** {agent name} argued {one sentence}
**Confidence:** {settled|leaning|contested}
[Full transcript]({relative path})

## {Question 2 Title}
...

## Session Notes
- Total questions discussed: {n}
- Session duration: {if available}
```

### What It Is Not

- Not a structured data artifact. It is prose with consistent headings.
- Not a replacement for the decisions ledger. The ledger continues as the append-only record of decisions across sessions.
- Not comprehensive. It is a navigation aid that points to transcripts for depth.

---

## What Does Not Change

- **Decisions ledger** continues as-is. It is the cross-session decision record.
- **Transcripts** continue as-is. Full round-by-round output per question.
- **Round output files** (propose, critique, evaluate) continue as-is.
- **session.json** manifest continues as-is.

---

## What Changes

| Current Behavior | New Behavior |
|---|---|
| Morning Brief generated by MorningBriefGenerator reading the decisions ledger with fragile regex extraction | Morning Brief generated by a single synthesis call with a structured prompt template reading round outputs directly |
| Synthesis output is free-form prose | Synthesis prompt demands consistent fields per question (recommendation, dissent, confidence) |
| Two LLM passes (synthesis + brief generation) | One LLM pass produces the brief directly |

---

## What Was Explicitly Rejected

| Proposal | Origin | Reason for Rejection |
|---|---|---|
| YAML decision records as synthesis output | Cognitive Architect | Premature structured artifact with no programmatic consumer. Prompt structure achieves consistency without a parallel data format. |
| Tension maps (prose on unresolved fault lines) | Cognitive Architect | Valuable concept but unvalidated. Transcripts serve this purpose today. Revisit if consumers request it. |
| Verification pass (LLM cross-checks synthesis against transcripts) | Adversarial Critic | Doubles token cost and latency. Human reader catches errors faster than automated verifier for a document of this length. |
| Dropped-thread detection | Cognitive Architect | Requires reasoning about absence, which is unreliable. Transcripts capture everything; dropped threads resurface naturally in future sessions. |
| Role-selective context in synthesis prompt | (preemptive) | Rejected in Q8 decisions. Synthesis receives all round outputs for its question without filtering. |
| Reading-behavior instrumentation | Product Oracle | Impractical for a CLI tool. The feedback loop is the user running sessions and identifying failures directly. |
| One synthesis call per question with template assembly | Flow Orchestrator | Unnecessarily complex. One call per session is simpler and the context window can handle typical session sizes. Revisit if sessions grow beyond current agent/question counts. |

---

## The Reopening Gate

Revisit this design if any of the following occur:

1. **The user reports that Morning Briefs misrepresent discussion outcomes.** This would validate the Critic's concern about silent synthesis failures and reopen the verification-pass question.
2. **Session size exceeds synthesis context capacity.** If agent counts or question counts grow such that all round outputs cannot fit in one synthesis call, the Orchestrator's per-question synthesis with template assembly becomes necessary.
3. **A downstream system needs to consume decisions programmatically.** This would justify the Architect's structured decision records as a real consumer exists.
4. **The user stops reading Morning Briefs.** This would indicate the format needs fundamental rethinking, not incremental improvement.
<!-- complete -->
