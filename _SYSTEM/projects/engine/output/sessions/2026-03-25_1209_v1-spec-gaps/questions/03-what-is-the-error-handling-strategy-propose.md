### The Cognitive Architect (creativity engine designer)

## Failure Asymmetry Is the Core Insight

Failures in this pipeline are not equal. The transcript is worth more than the synthesis. The synthesis is worth more than the micro-brief. The session is worth more than any question. The error strategy falls directly from this hierarchy: **never sacrifice the outer container for an inner component.**

**Retry policy: once, fast.** Any LLM call gets exactly one retry on timeout or API error. No exponential backoff, no queue — retry immediately. If it fails twice, move on. Retries-on-retry create session death spirals in overnight runs.

**Round failure:** If a propose/critique/evaluate round fails after retry, log the partial transcript and proceed to synthesis with whatever rounds completed. Synthesis with two rounds is degraded but not worthless. Flag which rounds are missing in the transcript header.

**Synthesis failure with rounds intact:** This is the case that deserves a real fallback. The evaluate turn is already a structured judgment call. Use the last evaluate turn as a synthesis proxy, wrapped with a `[SYNTHESIS FAILED — evaluate turn used as fallback]` header. The micro-brief then runs on that. The session continues.

**Full question failure:** Skip and continue. Never abort the session. The remaining questions have independent value.

**Morning Brief treatment:** Failed questions get the already-decided skip marker *plus* a failure type tag: `[round-failure]`, `[synthesis-failure]`, `[full-failure]`. The header count already tracks `failed_brief_count` — add `failed_question_count` as a peer field.

**Save everything, always.** Partial transcripts are saved before any call that could fail. Write-before-call, not write-after-success.

### The Flow Orchestrator (mechanical flow designer)

## Agreed on Hierarchy. Cut the Rest.

The failure asymmetry framing is correct and I won't relitigate it. But the proposed strategy adds moving parts I'd remove.

**Retry: once is right. Immediate is right.** No argument there.

**The evaluate-turn synthesis fallback is complexity I'd cut.** It requires the orchestrator to detect synthesis failure, locate the last evaluate turn, wrap it, and route it differently to the micro-brief. That's three conditional branches for a case that will happen rarely. The already-decided skip marker handles it: log it, mark it, move on. The morning brief already signals the failure. The transcript has the evaluate turn — a human can read it. Don't build machinery for human-readable fallback.

**Round failure handling: simpler.** If a round fails after one retry, mark which rounds completed in the transcript and proceed to synthesis. The synthesis prompt already receives transcript content — it will handle incomplete input gracefully or fail, and failure is already handled. No special "flag which rounds are missing in the transcript header" logic needed; the transcript simply won't have those turns. Absence is self-documenting.

**`failed_question_count` in the header: yes.** That's one field, no branching logic. Keep it.

**Write-before-call: yes, mandatory.** This is the one place I'd be strict. Append partial transcript to disk before issuing any LLM call. Crash recovery depends on it.

**The failure type tags (`[round-failure]`, `[synthesis-failure]`, `[full-failure]`) are deferred.** They add conditional tagging logic now for diagnostic value that may never be needed. A plain skip marker is enough for V1.

Minimum viable error strategy: one retry, skip on second failure, write before every call, count failures in the header.


<!-- complete -->
