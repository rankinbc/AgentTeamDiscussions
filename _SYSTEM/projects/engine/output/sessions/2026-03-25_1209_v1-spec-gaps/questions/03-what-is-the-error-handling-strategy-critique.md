### The Adversarial Critic (adversarial reviewer)

## The Proposal Has a Comfortable Assumption Buried in It

"Absence is self-documenting" is doing a lot of work here and it's wrong.

**Problem 1: Absence is not self-documenting — it's invisible.** If round 2 fails and we proceed to synthesis, the synthesizer sees a transcript with rounds 1 and 3. It doesn't know round 2 is missing. It synthesizes as if the discussion was complete. The resulting design doc reflects a discussion that didn't happen. The morning brief marks nothing unusual. The user reads confident decisions extracted from a half-baked deliberation.

**Problem 2: "Synthesis will handle incomplete input gracefully" is the exact phrase that breaks systems.** That's not a design decision — it's a hope. Synthesis receiving a transcript missing the critique round will produce decisions without adversarial challenge. Those decisions go into `decisions.json` as `decided` tier. Nothing flags them as under-interrogated.

**Problem 3: One retry is not a strategy — it's a number.** What failure modes does one retry address? Transient network errors: yes. Rate limiting: no — you'll hit it again in 2 seconds. Model refusal: no. Malformed output: no. The retry count needs to match the failure taxonomy.

**Problem 4: Write-before-call is agreed, but what gets written?** A placeholder? The prompt itself? If the process crashes between write and call, recovery needs to distinguish "call was never made" from "call was made and response lost."

**Problem 5: Failed question count in the header without failure type is noise.** "3 questions failed" tells the user nothing actionable.

What's the actual failure taxonomy before we design handling?

### The Systems Pragmatist (infrastructure realist)

## The Adversarial Critic Is Right. The Flow Orchestrator Is Half-Right.

"Absence is self-documenting" breaks on the synthesizer problem. The synthesizer doesn't know what it doesn't know. Incomplete transcript → confident decisions → `decided` tier → user acts on them. That's silent corruption, not graceful degradation. The skip marker pattern fails here because the failure isn't visible to downstream components, only to humans reading the morning brief after the fact.

**The actual failure taxonomy, short version:**

1. **Transient** (network blip, timeout): retry once with backoff. Covers maybe 60% of failures.
2. **Rate limit**: retry with delay. Different handling than transient.
3. **Malformed output** (synthesis missing `## Decisions`): already handled — `extraction_failed: true`. Don't retry; the model understood the call.
4. **Round failure**: mark which rounds completed *in the transcript itself*, not just absence. One line: `[ROUND 2 SKIPPED — call failed after retry]`. Then synthesizer prompt explicitly states which rounds are present.

That last point is the minimum viable fix for the invisible-absence problem. Not failure type tags in the brief — tags *in the transcript* that the synthesizer reads. One conditional write. Big blast radius prevention.

**Write-before-call:** write the prompt to disk, not a placeholder. Recovery then knows: file exists = call was attempted; response file absent = response lost. Two states, unambiguous.

**One field I'd add to the header:** `rounds_skipped_count`, not just `failed_question_count`. A skipped round producing a decision is worse than a skipped question producing nothing.

Cut the evaluate-turn fallback. Keep the transcript-level skip markers.


<!-- complete -->
