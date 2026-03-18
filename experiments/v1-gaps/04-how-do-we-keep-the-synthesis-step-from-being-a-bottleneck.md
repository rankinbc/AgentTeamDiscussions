# How do we keep the synthesis step from being a bottleneck?

*Generated: 2026-03-18 03:56 | Question 4 | 134s | Mode: compete*

## Decisions

### D1: Truncated Input on Synthesis Retry

When synthesis fails its first attempt, the retry sends a reduced payload. The retry uses the same prompt template and produces the same output format. No alternate prompt, no skeleton documents, no second output contract.

The truncation rules:

- **Strip the propose round entirely.** Critique and evaluate subsume the propose round's content in the common case. Critique captures disagreements; evaluate captures consensus. The propose round has the highest token count and lowest marginal signal density of any input section.
- **Trim prior design doc context to the immediately preceding question only.** Earlier design docs provided cross-question continuity but are not load-bearing for synthesizing the current question's rounds.

This reduces input token count by approximately 40%. The orchestrator builds the truncated payload from round files already on disk. String concatenation on existing files, not a new subsystem.

### D2: Pre-Build the Truncated Payload

The orchestrator constructs both the full payload and the truncated fallback payload before the first synthesis attempt. If synthesis succeeds, discard the fallback. If it fails, the fallback is ready immediately with no string manipulation inside the error handler.

The cost is trivial: one extra string concatenation per synthesis call. The benefit is keeping retry-path code simple and testable. Error handlers that build prompts on the fly are where silent bugs accumulate.

### D3: No Degraded Output Mode

If synthesis fails both attempts (original + truncated retry), the question is marked `partial` in `session_status.json` and the orchestrator advances to the next question. No skeleton document, no bullet-point summary, no file that approximates a design doc.

The rationale:

- Individual round files (propose, critique, evaluate) are already on disk per the immediate-write policy. A human can read them and synthesize manually.
- A `partial` status is an honest, machine-readable signal. The Morning Brief can flag it. Downstream consumers can skip it.
- A degraded synthesis file that looks authoritative but was generated from incomplete context is worse than a gap. It passes visual inspection but may contain misclassified commitments or fabricated consensus. The extraction pipeline would process it as if it were full-fidelity output, propagating errors into `decisions.json`.

### D4: Same Retry Policy as All Other Calls

Synthesis does not get special retry counts, special timeouts, or special backoff. It follows D4 from the error handling design doc exactly: one retry, exit-code-aware backoff (30 seconds for rate limits, immediate for everything else), 120-second wall-clock timeout per attempt.

The sunk-cost argument -- "we already ran three rounds for this question, so synthesis deserves extra retries" -- does not change the probability that a third attempt succeeds with the same input. The truncated payload on retry is the only concession to synthesis's higher stakes, and it operates within the existing retry budget.

### D5: Log Failure Mode on Every Synthesis Failure

Every synthesis failure (first attempt or retry) logs the failure category:

- **timeout**: The 120-second wall-clock limit was reached.
- **rate_limit**: Exit code or HTTP status indicates 429 or equivalent.
- **malformed_output**: The call returned but output failed validation (missing required sections, unparseable structure).
- **model_error**: Any other non-zero exit code.

This data goes into `session_status.json` alongside the round status:

```json
"synthesis": {
  "status": "failed",
  "attempts": [
    {"input": "full", "failure_mode": "timeout", "duration_seconds": 120},
    {"input": "truncated", "failure_mode": "malformed_output", "duration_seconds": 34}
  ]
}
```

This is the instrumentation requirement that makes future targeted interventions possible. Without failure mode distribution data, any V2 synthesis reliability work is guesswork. V1 ships with the cheapest viable intervention (truncated retry) and collects the data needed to design the next one.

### D6: No Two-Pass Synthesis

Synthesis remains a single `claude -p` call producing the complete design doc. No outline-then-fill approach.

Two-pass doubles the call count for synthesis on every question, including the majority that succeed on the first single-pass attempt. It doubles the failure surface: the outline pass can fail, the fill pass can fail, and now coordination between them can fail. It optimizes for the failure case at the expense of the common case.

### D7: No Chunked Input

Synthesis input is not split across multiple calls. The purpose of synthesis is to reconcile contradictions between agents across all rounds. Chunking produces parallel summaries, not integrated synthesis. A merge step after chunking recreates the original problem at a different layer.

---

## Open Questions

### OQ1: Propose Round Stripping May Drop Load-Bearing Content

When all agents agree during propose and the critic raises only marginal objections, the core position may exist only in the propose round. Stripping it removes the substance that critique and evaluate reference but do not restate. This is a known edge case accepted for V1 on the basis that it is uncommon and the alternative (analyzing propose for unique content before stripping) adds complexity disproportionate to the risk. Monitor truncated-retry output quality in early runs.

**Blocking:** No. Accepted risk for V1.

### OQ2: Actual Synthesis Failure Rate Is Unknown

All design decisions in this document are hedged against an unknown failure distribution. If synthesis fails less than 5% of the time, this entire mechanism activates rarely and the real reliability work is elsewhere (prompt quality, input structure). If it fails more than 20%, truncated retry alone is insufficient and V2 needs targeted interventions informed by the failure mode logs from D5.

**Blocking:** No. D5 instrumentation collects the data. Revisit after first production runs.

### OQ3: Upstream Prompt Quality as the Higher-Leverage Intervention

Tighter round prompts that produce more structured output reduce synthesis reconciliation work. This is a prompt tuning task, not an architecture decision, but it likely delivers more reliability improvement per unit effort than retry-path engineering. Not addressed in this design doc because it falls outside the synthesis retry scope.

**Blocking:** No. Independent improvement track.