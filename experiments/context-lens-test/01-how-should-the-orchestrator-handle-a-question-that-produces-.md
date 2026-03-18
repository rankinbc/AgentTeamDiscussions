# How should the orchestrator handle a question that produces contradictory proposals?

*Generated: 2026-03-18 13:02 | Question 1 | 126s | Mode: compete*

## Decisions

### Decision 1: Never Merge Contradictory Proposals

The synthesizer never produces a hybrid design from incompatible proposals. Merged LLM output obscures the sharp edges that made each proposal valuable and produces incoherent designs that are harder to debug than either original. The system preserves the fork explicitly.

**Rationale:** Unanimous agreement across all participants. Merging contradictory positions produces the median of two extremes, losing the distinct value each proposal was optimizing for. Two clean proposals with a tagged fork are debuggable. A hybrid is not.

---

### Decision 2: Synthesis Produces a Structured Comparison, Not a Winner

The synthesis step outputs a **Comparison Report** containing:

1. **Agreement summary** -- what both proposals share (typically small).
2. **Divergence list** -- specific points where proposals contradict, stated as pairs: "Proposal A says X. Proposal B says Y."
3. **Scored recommendation per divergence** -- each side evaluated against three pass/fail criteria.
4. **Provisional resolution** -- the synthesizer picks a default winner for each divergence and flags it as overridable.

The report is a single markdown artifact written to the session output folder.

---

### Decision 3: Three Pass/Fail Scoring Criteria

Each side of a contradiction is scored against exactly three questions:

| Criterion | Test |
|---|---|
| **Overnight survival** | Can this run unattended for 8 hours without human intervention? |
| **Fewer moving parts** | Does this option introduce fewer components, interfaces, or failure points than the alternative? |
| **Observable via config** | Can a user understand and tune this behavior by reading or editing YAML files? |

Each criterion is binary pass/fail. No weighted scoring, no rubrics, no nuance. The synthesizer must commit to a yes or no for each.

**Why these three:** They directly encode the project's V1 constraints (overnight autonomy, simplicity, YAML-driven configuration). They are blunt by design -- at 3 AM the system needs a clear signal, not a spreadsheet.

**Acknowledged weakness:** These criteria are somewhat subjective when applied by an LLM to prose descriptions. This is acceptable for V1 because the output is a recommendation, not an automated decision. The human retains override authority.

---

### Decision 4: Synthesizer Extracts Decision Points from Prose

Proposers write naturally. The synthesizer extracts decision points as a separate reasoning step before scoring.

The system does not force proposers to emit decisions in a rigid tagged format. Doing so would constrain the divergent thinking the propose step exists to produce. Instead, the synthesizer's prompt includes an explicit instruction: "Before comparing, extract the key structural decisions each proposal makes. List them as pairs."

**Acknowledged risk:** Extraction will miss some conflicts. Silent agreement on a point that was actually contested is the failure mode. This is tolerable in V1 because:
- The Morning Brief invites the human to review the full proposals, not just the summary.
- Missed conflicts surface during implementation and can be caught in later sessions.
- Building a structured decision-point schema to prevent this is premature complexity for a system that doesn't exist yet.

---

### Decision 5: Maximum Two Tiebreakers Reach the Morning Brief

When both proposals pass all three criteria on a divergence, it escalates as a tiebreaker. The synthesizer ranks tiebreakers by estimated downstream impact and escalates only the top two.

All remaining tiebreakers are auto-resolved using the "fewer moving parts" criterion as the default heuristic. If that criterion is also tied, proposal A (first listed) wins by convention.

**Rationale:** If the system escalates eight conflicts, the user deletes the email. The user's job is "decide what to build," not "resolve architectural contradictions." Two tiebreakers is a manageable homework assignment. Sensible defaults handle the rest.

**Override mechanism:** The Morning Brief marks auto-resolved conflicts with a "resolved by default" tag. The user can reopen any of them. No configuration knob for the cap -- ship the default.

---

### Decision 6: Unresolved Conflicts Do Not Block Progress

When a conflict escalates or is auto-resolved, the system picks a provisional winner and continues. The next round proceeds using the provisional resolution as assumed context.

The session artifact records:
- Which resolution was provisional.
- What the alternative was.
- That downstream artifacts may need revision if the human overrides.

**Rationale:** A frozen session waiting for human input defeats the overnight autonomy goal. The system must always produce a complete, reviewable draft. "We went with A. You might prefer B. Here's why they differ." is more useful than "We stopped because we couldn't agree."

---

### Decision 7: Synthesis Is an LLM Call, Not Mechanical Diffing

Despite the context cost, V1 retains an LLM-powered synthesis step rather than a mechanical section-level diff.

**Why not cut it:** A mechanical diff requires proposals to follow a template with identical section headers. Enforcing that template constrains the propose step. More importantly, contradiction detection often requires semantic understanding -- two proposals can use different vocabulary for the same structural decision, or agree on surface wording while diverging on intent. An LLM catches these; a diff tool does not.

**Context budget management:** The synthesizer prompt includes both proposals in full, the original question, and the scoring instructions. This is the most context-hungry step in the pipeline. To keep it manageable:
- Proposals have a soft length target (set in the proposer's system prompt, not enforced mechanically).
- The synthesizer prompt uses a fixed template with clear sections to minimize instruction overhead.
- If prompt size becomes a problem in practice, the first mitigation is summarizing each proposal before comparison, not cutting the synthesis step.

---

### Decision 8: Comparison Report Format

The synthesis step writes a single markdown file to `{session}/artifacts/comparison-report.md` with this structure:

```
# Comparison Report
## Question
{the original design question}

## Agreement
{what both proposals share}

## Divergences
### Divergence 1: {named decision}
- **Proposal A:** {position}
- **Proposal B:** {position}
- **Scoring:** A [pass/fail, pass/fail, pass/fail] | B [pass/fail, pass/fail, pass/fail]
- **Resolution:** {A or B} (provisional | tiebreaker)
- **Reasoning:** {one sentence}

### Divergence 2: ...

## Tiebreakers for Morning Brief
{top 2 unresolved conflicts, if any, with enough context for the human to decide}

## Provisional Design
{the complete design assuming all provisional resolutions hold}
```

The **Provisional Design** section is the key output. It is a coherent, usable design document that incorporates all resolutions (both auto-resolved and provisionally picked). The user can review just this section if they trust the defaults, or audit the divergences above if they want to understand the tradeoffs.

---

## Behavior Summary

1. Proposers write freely. No structured decision-point tagging required.
2. The synthesizer extracts decision points from prose as its first reasoning step.
3. It identifies contradictions by comparing extracted decisions.
4. Each contradiction is scored pass/fail on three criteria: overnight survival, fewer moving parts, observable via config.
5. If one side wins on score, it becomes the provisional resolution.
6. If tied, the conflict is ranked by impact. Top two escalate as tiebreakers. The rest auto-resolve via "fewer moving parts wins" (or position-order tiebreak).
7. The system always produces a complete provisional design. Nothing blocks on human input.
8. The Morning Brief surfaces at most two tiebreakers with enough context to decide.
9. All provisional resolutions are tagged so the human can override and trigger re-derivation of downstream artifacts.