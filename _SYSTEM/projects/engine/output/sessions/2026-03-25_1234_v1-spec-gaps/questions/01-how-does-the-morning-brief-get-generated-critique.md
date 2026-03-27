### The Adversarial Critic (adversarial reviewer)

## Five Problems Before We Write A Single Prompt

**1. The context overflow is unaddressed.**
The question explicitly asks: what if 10 design docs exceed context? The Flow Orchestrator's answer is "load all fragments." Fragments are derived summaries — you've already accepted information loss at extraction time. Now you're summarizing summaries. The Morning Brief is a telephone game by design. Name the fidelity tradeoff or it will surprise you in production.

**2. The fallback is theater.**
"Write fragments with section headers" is not a fallback — it's a dump with formatting. If the LLM call fails, the user gets raw `{decision, tension}` pairs labeled "## What Got Decided." That's worse than no brief because it looks like a brief. A real fallback is: what does the user actually need at 7am? Define that, then design toward it.

**3. Risk flags are buried in unstructured markdown.**
"They're already in the design doc" assumes structured extraction from prose. That's a second LLM call you're not accounting for, or it's a grep that misses implicit risks. Pick one and spec it.

**4. "The One Thing To Watch" is an editorial choice made by a stateless LLM.**
If the session had three critical blockers, the prompt collapses them to one. That's not synthesis — it's suppression. Show me the selection criteria or remove the section.

**5. Incremental vs. all-at-once isn't resolved — it's deferred.**
These have opposite failure modes. Incremental briefs are stale by question 8. All-at-once fails if the session crashes at question 7. Pick one and own the failure mode explicitly.

The prompt design is premature. Fix the input assembly problem first.

### The Systems Pragmatist (infrastructure realist)

## The Adversarial Critic Is Right. The Flow Orchestrator Is Optimizing Prematurely.

Both problems are real. Let me resolve them.

**On incremental vs. all-at-once:** Pick incremental. The failure mode of all-at-once (crash at Q7 = no brief) is worse than stale fragments. But "incremental brief" is the wrong framing — you're not updating a brief, you're **appending to a fragment log**. The brief is only generated once, at session end, from that log. Staleness isn't a problem because fragments don't become stale — they're historical records.

**On context overflow:** Fragments solve this correctly *if* you're disciplined about size. Each fragment: `{question_id, decision, tension, risk_flag}` — one sentence each, hard limit. Ten questions = ten fragments = ~800 tokens. Fits. The fidelity loss is real but it's *bounded and explicit*. Design docs stay on disk; if the user wants depth, they read the doc. The brief is navigation, not content.

**On "The One Thing To Watch":** The Adversarial Critic is correct — this is editorial suppression. Replace it with `## Unresolved Blockers` and emit *all* flagged risks from the fragment log. If there are zero, say so. If there are five, show five. The LLM doesn't choose; it formats.

**The actual fallback:** If the synthesis call fails, concatenate fragment decisions into `## What Got Decided` and fragment tensions into `## What's Still Open`. No LLM needed. That's a real fallback because it uses structured data you already have.

**What still isn't resolved:** How do critics emit structured risk flags into the fragment log? That's the one gap remaining. Everything else has a deterministic path.


<!-- complete -->
