### The Product Oracle (user advocate)

## The Product Oracle: What Does 8am Actually Feel Like?

Everyone's been arguing about architecture. Let me argue about the user.

The person opening this brief ran a session overnight. They remember their questions — they wrote them. What they *don't* know is: which answers held up, which ones have a hidden time bomb, and what they should think about before their first meeting.

That's three things. The brief should deliver exactly those three things, per question, in under 2 minutes of reading.

**The Systems Pragmatist is right on the architecture.** Incremental wins. Catastrophic tail failure at the one moment the artifact matters most is disqualifying. Ship the incremental model.

**But the format question is underdecided.** "Appended bullets" isn't good enough. The micro-brief template needs to be opinionated:

```
### [Question title]
**Decided:** [one sentence]
**Why this beat alternatives:** [one sentence]  
**Unresolved risk:** [one sentence, or "none surfaced"]
```

That's scannable in 10 seconds per question. No narrative needed. Structure *is* the coherence.

**One flag nobody raised:** The "what surprised us" framing from the Cognitive Architect is the most valuable prompt instruction here. Surprise is the signal. If the answer was obvious before the session, it's not worth the brief's real estate. The micro-brief prompt should explicitly ask: *did this answer challenge any assumptions?*

**My verdict:** Incremental append, structured template, skip-with-marker on failure, surprise-flag baked into prompt. That's V1. Assembly pass is V2 if users ask for it.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon: The Input Assembly Problem Is the Whole Problem

Everyone aligned on incremental. Good. But nobody has solved *what goes into each micro-brief call*, and that's where this breaks.

**The incremental model accidentally solves the context overflow problem.** Each micro-brief call takes one question's synthesis — call it 1-2K tokens. Not 10 design docs. Not the full transcript. That's the strongest argument for incremental that hasn't been named explicitly. Lock it in: micro-brief input = synthesis output for that question only, nothing else.

**The Product Oracle's template is correct. Add one field:**

```
### [Question title]
**Decided:** [one sentence]
**Why this beat alternatives:** [one sentence]
**Unresolved risk:** [one sentence, or "none surfaced"]
**Assumption challenged:** [one sentence, or "none"]
```

That last field is doing signal extraction, not summarization. The prompt instruction matters: *"If the discussion reached the same conclusion the brief writer would have predicted, write 'none.'"* Forces the model to actually check.

**The context waste I'm flagging:** passing synthesis *output* when you could pass extracted decisions directly. The synthesis is human-readable prose optimized for a reader, not token-efficient input for the next call. If decision extraction is already happening per-question, pass those structured decisions to the micro-brief prompt, not the synthesis narrative. Half the tokens, same signal.

**On fallback:** skip-with-marker is correct. But the marker should include the question title so the gap is scannable at 8am. `[Q3 — "Error recovery strategy" — brief failed, see transcript]`. Silence is not a fallback.


<!-- complete -->
