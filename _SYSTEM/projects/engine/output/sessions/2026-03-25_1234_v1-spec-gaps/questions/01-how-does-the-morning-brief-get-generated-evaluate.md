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
