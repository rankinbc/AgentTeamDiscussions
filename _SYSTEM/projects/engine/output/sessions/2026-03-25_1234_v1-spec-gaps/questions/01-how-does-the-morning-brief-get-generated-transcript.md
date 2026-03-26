# Transcript: How does the Morning Brief get generated?

*Generated: 2026-03-25 12:36*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Incremental Fragment Architecture

The fundamental error in brief generation is treating it as end-of-session compression. That's the wrong mental model. What you actually want is **progressive crystallization** — the brief *accretes* during the session, not after it.

**The mechanism:**

After each question resolves, a lightweight extractor runs on that question's transcript and design doc. It produces a **Brief Fragment**: one key decision (with confidence signal), one surviving tension that critique didn't resolve, and any risk flags that critics raised but evaluators didn't dismiss. Fragments are ~100 tokens each. Cheap. Reliable. Composable.

At session end, the Morning Brief assembles from **fragments + decisions.json**, not raw design docs. Context problem solved structurally, not by truncation heuristics.

**The prompt:**

```
You are synthesizing a product design session for a human who will 
read this over coffee. They need: what got decided, what's still 
uncertain, and what could go wrong. 

Inputs: [N fragments] + [decisions.json]
Sections: Decisions Made | Open Tensions | Risk Watch List

Be specific. Skip process. Surface the one thing they need to 
worry about first.
```

**Risk flag extraction** should happen *during* critique rounds — critics emit structured flags (`RISK: [type] [description]`), evaluators vote to dismiss or elevate. Only elevated flags reach the brief.

**Fallback:** fragments concatenated with headers. Ugly but readable. The session never returns nothing.

The insight from distributed cognition research: synthesis quality comes from *representation diversity across time*, not volume at the end.

### The Flow Orchestrator (mechanical flow designer)

## Agree on fragments. Cut the risk flag protocol.

The Cognitive Architect is right that end-of-session compression is the wrong model. Fragments solve the context problem structurally. I'll take that.

But the risk flag mechanism — critics emitting `RISK: [type]`, evaluators voting to dismiss or elevate — is a new sub-protocol bolted onto the critique round. That's scope. Cut it.

**The actual sequence, minimal:**

**After each question resolves:**
1. Fragment extractor runs on `transcript.md` + `design_doc.md` for that question
2. One LLM call. Output: `{decision: str, tension: str}` — two fields, nothing more
3. Append to `fragments.jsonl`

Risk flags are already in the design doc. They don't need a separate extraction pipeline.

**At session end:**
1. Load all fragments from `fragments.jsonl` + `decisions.json`
2. Single LLM call → `morning_brief.md`

**The prompt (lean version):**
```
Synthesize this product design session for a human reading over coffee.

Decisions: [decisions.json]
Key fragments: [N x {decision, tension}]

Output:
## What Got Decided
## What's Still Open  
## The One Thing To Watch

Be specific. 300 words max.
```

**Fallback if the call fails:** write fragments to `morning_brief.md` with section headers. User gets something readable. Session never exits empty.

**Decision point I need answered:** Does the fragment extractor run inline (blocking question N+1) or async? If questions chain forward and Q2 needs Q1's design doc, the fragment extraction can run async after the design doc is written — it doesn't block Q2's context assembly.

That ordering matters. Flag it now.

## Round: CRITIQUE

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

## Round: EVALUATE

### The Product Oracle (user advocate)

## The Brief Is a Decision Surface, Not a Summary

Stop optimizing for completeness. The user at 7am has one job: decide whether the session output is worth acting on and what to do first.

Everything the Adversarial Critic flagged is real. The Systems Pragmatist resolved most of it. I want to add one reframe that changes the prompt:

**The Morning Brief isn't a summary of what happened — it's a handoff document.**

That means the format question answers itself:

```
## Ready to Build
[Decisions with enough confidence to act on — 1 sentence each]

## Needs Your Call  
[Tensions the agents couldn't resolve — these require human judgment]

## Don't Start Yet
[Blockers. All of them. One line each. Zero if none.]
```

No "what the agents discussed." No process. The user doesn't care. They care what's unblocked and what isn't.

On the "One Thing to Watch" debate: the Systems Pragmatist is right to emit all blockers, but the framing matters. "Unresolved Blockers" sounds like a bug report. "Don't Start Yet" is a decision gate. Same data, better signal.

On fallback: structured fragment concatenation is a real fallback *only if* the sections are labeled with the right framing. A dump of tensions labeled "## Needs Your Call" is actually useful. A dump labeled "## What's Still Open" is noise.

**The fragment schema should match the brief sections:** `{decision, needs_your_call, blocker}` — not `{decision, tension, risk}`. Name things what they are in the output, not what they are internally.

One config field: `brief_word_limit`. Default 300. Nothing else.

### The Context Surgeon (context efficiency evaluator)

## The Input Assembly Problem Is Already Solved — Nobody Said So

The Pragmatist and Oracle have converged on the right structure. I'll stop the naming debate and close the one real gap.

**On fragment schema naming:** Internal names (`tension` vs `needs_your_call`) don't affect output labels. The synthesis prompt maps internal fields to output sections. Decouple them. This is not a design decision.

**The actual input assembly answer:** The fragment log *is* the complete input to the synthesis call. Design docs stay on disk. This resolves the "10 design docs exceed context" problem entirely — it was never a problem once you have fragments. State this explicitly so nobody re-litigates it.

Synthesis call budget: ~800 tokens fragments + ~200 tokens system prompt + ~150 tokens format template = ~1,150 tokens in, ~400 out. Trivial. No chunking, no summarization of summaries.

**Closing the risk flag gap:** Critics already produce prose critique. You don't need a new schema field. Add one extraction step: scan critic output for sentences matching `BLOCKER:` or `RISK:` prefix tags (convention in the prompt template). Regex-extract them into the fragment. No extra LLM call. If critics don't tag anything, the blocker list is empty — that's signal too.

**What still needs specifying:** The exact system prompt for synthesis. It should receive: (1) the fragment log, (2) the output format, (3) the word limit. Nothing else. One call, deterministic structure, no editorial judgment delegated to the LLM beyond formatting.

Draft that prompt. Everything else is resolved.

<!-- complete -->
