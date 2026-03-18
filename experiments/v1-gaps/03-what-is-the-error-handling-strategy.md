# What is the error handling strategy?

*Generated: 2026-03-18 03:54 | Question 3 | 154s | Mode: compete*

## Decisions

### D1: Immediate Disk Writes After Every Completed Round

Every successful LLM call writes its output to disk the moment it completes. Not buffered until question completion, not batched at session end. If the process crashes after round 2 of question 4, rounds 1 and 2 are intact files on disk.

This is the foundation. Every other decision assumes it.

### D2: Per-Round Status Tracking

The orchestrator writes `session_status.json` after each round completes, not after each question. The file reflects what is actually on disk at any point in time.

Schema:

```json
{
  "session_id": "2026-03-18_overnight",
  "questions": {
    "q3": {
      "status": "complete",
      "rounds": {
        "propose": {"status": "complete", "file": "q3_propose.md"},
        "critique": {"status": "complete", "file": "q3_critique.md"},
        "evaluate": {"status": "complete", "file": "q3_evaluate.md"},
        "synthesis": {"status": "complete", "file": "q3_design_doc.md"}
      },
      "extraction": {"status": "complete"}
    },
    "q6": {
      "status": "partial",
      "rounds": {
        "propose": {"status": "complete", "file": "q6_propose.md"},
        "critique": {"status": "failed"},
        "evaluate": {"status": "skipped"},
        "synthesis": {"status": "skipped"}
      },
      "extraction": {"status": "skipped"}
    }
  }
}
```

If the process crashes, the last-written state of this file tells the human (or a future recovery tool) exactly what exists on disk.

### D3: 120-Second Timeout Per CLI Call

Every `claude -p` invocation gets a 120-second wall-clock timeout. If the process has not returned by then, kill it. A hung call counts as a failed call and enters the retry path.

Without this, a single stuck process can consume the entire overnight window. A timeout failure is operationally worse than a fast failure because it is silent.

### D4: One Retry With Exit-Code-Aware Backoff

Each CLI call gets exactly one retry. Two attempts total, no exceptions. The backoff depends on why the call failed:

- **Rate limit (429 or equivalent exit code):** Wait 30 seconds, then retry. The most common failure mode at 70+ calls. Retrying immediately guarantees the same result.
- **Any other failure (timeout, malformed output, model error):** Retry immediately with no backoff. If the problem is not transient load, waiting changes nothing.

No special retry counts for synthesis or any other step. Uniform policy across all call types. The sunk-cost argument for extra synthesis retries does not change success probability on a third attempt with the same input.

### D5: Output Validation Before Accepting a Response

A CLI call that returns HTTP 200 but produces unparseable or off-schema output is a failure, not a success. Before writing output to disk as "complete":

- **JSON outputs** (decisions.json, open_questions.json): Validate against the defined schema. Required fields must be present and correctly typed.
- **Markdown outputs** (design docs, round outputs): Validate that the response is non-empty and contains expected structural markers (headers, sections).

Failed validation counts as a failed call and enters the retry path. This prevents garbage data from propagating into downstream steps (synthesis, extraction, Morning Brief).

### D6: Failure Cascading Rules

When a round fails after both attempts:

| Failed Step | Consequence |
|---|---|
| **Propose fails** | Skip the entire question. Critique and evaluate have no input. Mark question as `skipped`. |
| **Critique fails** | Mark question as `partial`. Save the proposal. Do not run evaluate. Do not attempt synthesis. The proposal stands alone as a raw artifact. |
| **Evaluate fails** | Mark question as `partial`. Save proposal and critique. Do not attempt synthesis. |
| **Synthesis fails** | Save all completed rounds as `raw_rounds.md`. Mark question as `partial`. The human gets the ingredients. |
| **Extraction fails** | The design doc exists and is complete. The Morning Brief proceeds without this question's decisions and open questions. |

The rejected path: running evaluate without critique input. The evaluate prompt expects critique as input. Feeding it nothing produces hallucinated or confused output. If critique fails, stop the chain for that question.

### D7: Context Chaining Across Partial Questions

Prior design docs chain forward as context for subsequent questions. When a question produces only partial output (no synthesis, no design doc):

- The raw rounds from the partial question do not chain forward. Only completed design docs enter the context chain.
- The subsequent question proceeds with the last successfully completed design doc as its most recent context.
- The gap is noted in `session_status.json` but does not block forward progress.

### D8: Morning Brief Gap Reporting

When all questions complete successfully, the Morning Brief contains exactly the four standard sections (Decisions Made, Risk Flags, Open Questions Requiring Human Input, Recommended Reading Order). No gaps section. No success banner. Its absence is the signal.

When any question failed or produced partial output, the brief adds one section:

```
## Session Gaps
Questions where failures prevented full processing.
- Q6: Skipped. Propose failed on both attempts. No output.
- Q8: Partial. Critique failed. Proposal saved as q8_propose.md.
- Q9: Extraction failed. Design doc complete -- read q9_design_doc.md directly.
```

The brief generator reads `session_status.json` to build this section. It does not infer gaps from missing files.

### D9: Extraction Skips Incomplete Questions

Decision extraction (producing `decisions.json` and `open_questions.json`) only runs on questions that completed synthesis. No extraction attempt on partial questions -- the extraction prompt operates on the synthesis section of a design doc. Without synthesis, there is nothing to extract.

Missing extractions reduce the Morning Brief's coverage but do not prevent brief generation. The brief proceeds with whatever extractions succeeded.

## Open Questions

### OQ1: Exit Code Mapping for CLI Failures

The retry policy depends on distinguishing rate limits from other failures. What specific exit codes or stderr patterns does `claude -p` produce for rate limiting vs. model errors vs. timeouts? This mapping must be determined empirically before implementation. If the CLI does not expose failure type through exit codes, the backoff strategy falls back to a fixed 15-second wait on all retries (splitting the difference without the conditional).

**Blocking:** Yes. The retry implementation depends on this.

### OQ2: Timeout Duration Calibration

The 120-second timeout is a starting point. Synthesis calls may legitimately take longer than propose calls due to larger input context. Should the timeout vary by step type, or is a uniform 120 seconds sufficient based on observed call durations from beta runs?

**Blocking:** No. 120 seconds is a safe default. Can be tuned after observing real session timing data.

### OQ3: Session-Level Abort Threshold

If 5 of 10 questions fail at the propose step, the session is likely hitting a systemic issue (auth failure, service outage). Should the orchestrator abort the session after N consecutive or total failures rather than grinding through all 10 questions? Neither proposal addressed session-level circuit breaking.

**Blocking:** No, but worth deciding before V1 ships. Wasting 10 questions worth of timeout cycles on a dead API is a poor overnight experience.