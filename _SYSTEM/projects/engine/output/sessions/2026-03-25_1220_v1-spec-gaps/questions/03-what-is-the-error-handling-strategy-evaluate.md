### The Product Oracle (user advocate)

## Evaluate: The User Wakes Up to a Brief, Not a Status Page

The three-layer policy is correct and should be decided as-is. The debate worth resolving is what the Morning Brief says about failure — because that's the only failure artifact the user actually reads.

**Resolve first-call behavior now: DECIDED — omit `## What Got Built` when `previous_brief` is empty.** Both proposers agreed. Empty structural scaffolding is noise. Close it.

**On the brief and failed questions:** The Pragmatist says don't touch `brief.md`. The Architect says write a tombstone to `## Still In Play`. The Pragmatist wins on mechanism — direct append violates the write contract. But the Architect wins on intent — a user reading the brief shouldn't believe Q6 was answered when it wasn't. 

Resolution: tombstone is **transcript-only** for V1. The brief stays at last valid state. The user who wants to understand gaps reads the transcript. The brief remains clean and contractually intact. This is acceptable for a solo builder running overnight experiments — they'll check the transcript when something looks thin.

**Context chain gap:** Inherit last successful design doc. The Pragmatist named the simplest correct mechanism. Decide it.

**Retry budget:** One retry, no delay. The Pragmatist is right — we're catching blips, not building SLAs.

**Session abort:** Three consecutive failures. Reasonable signal that something systemic is wrong.

**Synthesis failure after successful rounds:** The existing fallback (`brief_fallback.md`) covers this. Say so explicitly and close the open question.

Five decisions ready to land. No new complexity introduced.

### The Context Surgeon (context efficiency evaluator)

## Evaluate: Five Decisions Land. One Context Efficiency Note.

The Oracle correctly enumerated five ready decisions. The Pragmatist named the right mechanisms. I'll validate and add one efficiency point, then close.

**DECIDED: Omit `## What Got Built` when `previous_brief` is empty.** Empty scaffolding is structural noise and wastes synthesis tokens. Both proposers agreed. Closed.

**DECIDED: On question failure, `brief.md` is not touched.** Tombstone is transcript-only. The brief stays at last valid state. The append-to-brief path violates the write contract and — critically — injects failure noise into the synthesis context chain. Every token spent on tombstone language in `previous_brief` is a token displaced from substantive decisions. The brief is a forward-looking compression artifact, not a status log.

**DECIDED: On question failure, Q(n+1) inherits Q(n-1)'s design doc.** Skip the gap in context. Simplest correct mechanism.

**DECIDED: One retry, no delay.** Transient blip recovery only.

**DECIDED: Abort after 3 consecutive failures.** Systemic failure signal.

**DECIDED: Synthesis failure after successful rounds is covered by the existing `brief_fallback.md` mechanism.** No new path needed. Close the open question.

**One context note:** When Q6 fails, the evaluator's scoring will incorrectly treat Q6 as absent rather than failed. Log the failure to `session.log` with question index and failure reason. This costs zero tokens in the brief chain and gives the evaluator the signal it needs. Not a new mechanism — just an explicit log write.

Six decisions. No open questions remaining on this topic.


<!-- complete -->
