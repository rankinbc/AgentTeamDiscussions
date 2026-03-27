# How does the Morning Brief get generated?

*Generated: 2026-03-25 12:11 | Question 1 | 175s | Mode: compete*

## Decisions

### 1. Generation Strategy: Incremental Append, No Final Assembly Pass

The Morning Brief is generated incrementally — one micro-brief block written per question immediately after that question's synthesis completes. There is no end-of-session assembly call. The brief is complete when the last question finishes.

**Rationale:** A final assembly call fails at the worst possible moment — after an overnight run, when the user most needs the artifact. The incremental model eliminates catastrophic tail failure. The fallback (concatenated micro-briefs) is readable as-is, which means the assembly pass was providing marginal coherence value at high reliability cost. Structure substitutes for narrative.

---

### 2. Micro-Brief Input: Extracted Decisions, Not Synthesis Prose

The micro-brief prompt receives **extracted decisions** from the question's synthesis round, not the full synthesis narrative. If structured decision extraction is not yet implemented, use the **last 500 tokens** of synthesis output (tail captures convergence, not preamble).

**Context budget per call:** ~1,500–2,000 tokens input. No prior questions, no full transcripts, no chained design docs. Each call is fully isolated.

**Rationale:** Synthesis prose is optimized for human reading, not token-efficient LLM input. Passing structured decisions halves token count with equivalent signal. The "last 500 tokens" fallback is a concrete, implementable rule — not a vague excerpt.

---

### 3. Micro-Brief Output Template (Opinionated and Fixed)

Each micro-brief block appended to `morning_brief.md` uses this exact structure:

```
### [Question title]
**Decided:** [one sentence]
**Why this beat alternatives:** [one sentence]
**Unresolved risk:** [one sentence, or "none surfaced"]
**Assumption challenged:** [one sentence, or "none — conclusion was predictable"]
```

The four fields are mandatory. The model must produce all four. "None" answers are valid and expected.

**Prompt instruction for "Assumption challenged":** *"If the discussion reached the same conclusion the brief writer would have predicted before running the session, write 'none — conclusion was predictable.' Only flag genuine surprises."* This forces active signal extraction rather than reflexive filler.

**Rationale:** Structure is coherence. A scannable 4-field block per question takes under 10 seconds to read. No narrative thread is needed across questions. The "assumption challenged" field operationalizes the highest-value signal — surprise — without requiring a synthesis pass.

---

### 4. Risk Flag Extraction: Prompt-Driven, No Regex Tagging

Unresolved risks are surfaced through the micro-brief prompt's "Unresolved risk" field. The orchestrator does **not** scan critic turns for uncertainty markers or maintain a tagging mechanism.

**Input to the prompt:** The extracted decisions or synthesis tail already encode what was resolved. The model identifies what was not resolved from that same input. No separate risk extraction pass, no regex fragility.

**Rationale:** The prompt field does the extraction work cleanly. A regex-based tagging system ("this assumes," "but what if") is brittle to paraphrase, adds orchestrator complexity, and solves a problem the prompt already handles.

---

### 5. Failure Behavior: Skip With Labeled Marker

If a micro-brief call fails (timeout, API error, rate limit), the orchestrator appends a visible skip marker and continues. The session does not block.

**Marker format:**
```
### [Question title] — brief generation failed, see transcript
```

The question title must be included so the gap is scannable at 8am. A blank section or silent omission is not acceptable. The transcript always exists as the ground-truth fallback.

**Rationale:** Silent gaps are worse than honest gaps. The user can locate the relevant transcript section using the question title. Blocking on a transient failure corrupts the session; skipping preserves everything else.

---

### 6. Ordering Limitation: Accepted, Not Engineered Around

The incremental model has a structural ordering dependency: question 1's micro-brief is written without knowledge of what questions 7–10 will surface. A critical risk that emerges late in the session does not retroactively update earlier blocks.

This limitation is **accepted for V1**. Questions are ordered by the user's own brief, which means earlier questions reflect the user's higher-priority concerns. Late-emerging risks appear in their own question's block and in the transcript.

A cross-question synthesis pass (assembly) that reorders by risk severity is a V2 feature, contingent on user feedback that ordering is a real problem in practice.

---

### 7. Brief Header: Session Metadata Only

`morning_brief.md` opens with a minimal header:

```
# Morning Brief — {session-id} — {date}
Questions: {N} | Completed: {n} | Failed briefs: {k}
```

No narrative introduction. The per-question blocks follow immediately. The header gives the user a status check in one line before reading any decisions.

---

### 8. Quality Gate: None in V1

There is no quality gate on synthesis output before it feeds the micro-brief prompt. Weak synthesis produces a weak micro-brief block — that signal is itself informative (it indicates a low-quality discussion round).

Automated quality scoring (via the evaluator) runs post-session as a separate pass and is not a dependency of brief generation.
<!-- complete -->
