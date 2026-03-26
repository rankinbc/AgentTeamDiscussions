# Transcript: How does the Morning Brief get generated?

*Generated: 2026-03-25 12:11*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Morning Brief: Incremental Assembly with Critic-Extracted Risk Flags

**Core commitment: generate incrementally, assemble at the end.**

After each question completes, generate a micro-brief (3-5 bullets) while the context is narrow and fresh. This sidesteps the 10-doc overflow problem entirely — you never feed everything at once. At session end, a lightweight assembly pass synthesizes micro-briefs into the final document.

**Per-question micro-brief prompt (fed immediately after synthesis):**
```
Given this question: {question}
Design decision reached: {design_doc excerpt, ~500 tokens}
Critic challenges that were NOT resolved: {unresolved_flags}

Generate 3-5 bullets covering:
- What was decided and why it beat alternatives
- The strongest unresolved objection (if any)
- What this decision constrains downstream
```

**Risk flag extraction** happens during critique rounds, not retrospectively. The orchestrator tags any critic turn containing uncertainty markers (`"but what if"`, `"this assumes"`, `"unresolved"`, `"depends on"`) as a candidate flag. The micro-brief prompt receives only those tagged excerpts — not full transcripts.

**Final assembly prompt** receives only the micro-briefs (trivially small) plus session metadata:
```
Synthesize these per-question briefs into one Morning Brief.
Lead with: what surprised us. End with: what's still unresolved.
```

**Fallback**: If final assembly fails, concatenate micro-briefs directly. They're readable as-is. Graceful degradation, not silent failure.

**Why incremental beats all-at-once:** Recency bias works *for* you here. The micro-brief captures the critique energy while it's hot. All-at-once flattens that signal.

### The Flow Orchestrator (mechanical flow designer)

## Flow Orchestrator Response: Cut the Assembly Pass

The incremental approach is correct. The fallback reveals the real answer.

**The Cognitive Architect's own fallback — concatenate micro-briefs directly — is the design.** If micro-briefs are "readable as-is," the final assembly LLM call is pure overhead. It adds a failure mode, a latency spike at session end, and another prompt to maintain. Cut it.

**Exact sequence I'd commit to:**

1. Question N completes → synthesis output written to disk
2. Immediately: feed `{question}` + `{synthesis excerpt, 500 tokens}` to micro-brief prompt
3. Append 3-5 bullet output to `morning_brief.md`
4. Repeat for N+1
5. Session ends → `morning_brief.md` is complete. No assembly step.

**Flag on the risk extraction:** "The orchestrator tags critic turns containing uncertainty markers" is hand-waving. What triggers the scan — after every critic turn? After all critique rounds complete? What's the data structure? I'd simplify: the micro-brief prompt already asks "strongest unresolved objection" — that pulls it forward without regex fragility. Drop the tagging mechanism entirely.

**What this gives you:** Two LLM calls per question (synthesis + micro-brief), zero end-of-session call, graceful degradation built-in, no context overflow ever. The brief is assembled continuously, not retrospectively.

**One open question worth flagging:** If a micro-brief call fails mid-session, do we block or skip? The sequence needs a defined answer before implementation.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

## Adversarial Critic: The Proposal Has a Structural Hole

The Flow Orchestrator's incremental append model sounds clean. It isn't.

**Five problems before anyone ships this:**

**1. Garbage in, garbage out — compounded.** The micro-brief prompt feeds on synthesis output. If synthesis round 3 is weak (rushed, truncated, low-signal), the micro-brief inherits that weakness. There's no quality gate. You're automating the transcription of mediocre output into the one artifact the user actually reads.

**2. "500-token excerpt" is unspecified.** First 500 tokens? Last 500? A summary? This detail determines whether the micro-brief captures the real decision or the preamble. Nobody has defined the selection logic.

**3. Appended bullets ≠ coherent brief.** Ten questions × 3-5 bullets = an unstructured list. The user opens it at 8am and reads... what, exactly? No narrative thread, no priority ordering, no signal about which questions matter most. The assembly step was doing real work — synthesizing *across* questions — and it just got silently dropped.

**4. The "fail: block or skip?" question was raised and left open.** That's not a flag, that's a blocker. If you skip, the brief has silent gaps. If you block, a transient API failure corrupts the session. Neither answer is in the design.

**5. Ordering dependency is baked in.** Question 1's micro-brief is written without knowing what questions 2-10 will surface. A critical risk that only emerges in question 7 won't appear in earlier bullets. The brief is structurally biased toward early-session concerns.

The incremental model solves context overflow. It doesn't solve coherence.

### The Systems Pragmatist (infrastructure realist)

## Systems Pragmatist: The Critic Is Right, But Drawing the Wrong Conclusion

The Adversarial Critic landed real hits. But the conclusion should be "fix the incremental model," not "resurrect the assembly step."

**The assembly-at-end call is the worst possible failure mode.** Session runs for 4 hours overnight. User goes to sleep. Final call fails — API timeout, context overflow, rate limit. Morning Brief: null. That's not a degraded experience, that's a broken promise at the exact moment the user most needs the artifact.

**Incremental with a defined answer to each critique:**

**On "500 tokens unspecified":** Last 500 tokens of synthesis output. Not first, not summarized — the tail of the synthesis is where convergence lands. One-line implementation decision, commit to it.

**On "appended bullets ≠ coherent brief":** Correct. So the micro-brief prompt does light framing work: `[Question N: {title}] decision: X. risk: Y.` The brief reads as a structured list per question, not free bullets. Coherence across questions is a V2 concern — don't let perfect kill shipped.

**On "block or skip":** Skip with a visible marker. `[Q3 brief generation failed — see transcript]`. Silent gaps are worse than honest gaps.

**On ordering dependency:** This is real and unsolvable incrementally. Accept it. Questions are ordered by the user's brief — earlier questions are structurally more important. If question 7 surfaces a critical risk, the transcript exists.

**The assembly step solves coherence at the cost of catastrophic tail failure. That's the wrong trade.**

## Round: EVALUATE

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
