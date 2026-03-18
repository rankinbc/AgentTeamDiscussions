# Transcript: How does the Morning Brief get generated?

*Generated: 2026-03-18 03:49*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Morning Brief: Incremental Accumulation, Final Synthesis

**The key insight:** Don't choose incremental OR all-at-once. Do both.

After each question completes, generate a **brief fragment** -- a 3-line summary (decision, confidence, risk flags) appended to a running `brief_fragments.md` file. Cheap call, tiny context, near-zero failure risk. This is your accumulator.

At session end, the final Brief call receives `brief_fragments.md` plus the **decisions files only** -- not the full design docs. Decisions are already distilled. This sidesteps the context overflow problem entirely. Ten questions produce maybe 2-3K tokens of fragments plus decisions. Trivially fits.

**The prompt structure:**

```
You are summarizing an overnight autonomous design session for a human
who has 5 minutes. They need to know: what was decided, what's shaky,
and what needs their input before work proceeds.

INPUT: Session fragments and extracted decisions.
OUTPUT: Morning Brief in this exact format:

## Decisions Made (with confidence)
## Risk Flags (from critic rounds where consensus < 70%)
## Open Questions Requiring Human Input  
## Recommended Reading Order (which design docs to read first if curious)
```

**Fallback chain:** If the final synthesis call fails, `brief_fragments.md` already exists as a degraded-but-readable brief. The user still gets something. If a per-question fragment call fails, skip it -- the decisions file covers it at synthesis time. Two layers of graceful degradation, zero catastrophic failure modes.

**The architectural principle:** Never make the most important artifact depend on the most expensive call. The Brief earns its reliability by being the *lightest* consumer of context, not the heaviest.

### The Flow Orchestrator (mechanical flow designer)

## Morning Brief: Generation Design

**Timing: All-at-once, at the end.** Incremental updates mean maintaining partial state, re-rendering, and handling the case where early briefs become stale as later questions change the picture. One call. One artifact. Done.

**Input assembly:**

Don't feed it 10 full design docs. Feed it the **decisions and open questions** extracted from each round. Those are already structured, already distilled. If you've done the extraction right, decisions + open questions from 10 rounds fit comfortably in context. Full design docs are reference material for humans, not brief input.

Fallback if even decisions exceed context: truncate from the front. Earlier questions matter less than later ones (later rounds had more context, made better-informed calls).

**Prompt structure:**

```
You are summarizing an overnight design session for a human reader.

Input: {concatenated decisions.json + open_questions.json per round}

Produce:
1. KEY DECISIONS - Numbered list. One line each. Include confidence if below 80%.
2. OPEN QUESTIONS - Unresolved items requiring human judgment.
3. RISK FLAGS - Any decision where the critic round raised unresolved concerns.
4. RECOMMENDED READING ORDER - Which design docs to read first if time is limited.
```

That's four sections. No prose paragraphs. No executive summary fluff. Scannable in 90 seconds.

**Failure fallback:** If the brief generation call fails, concatenate raw `decisions.json` files into a flat markdown list. Ugly but functional. The user still gets the information. Retry logic is unnecessary complexity for a batch job -- just degrade gracefully.

**Risk flags** come directly from critic rounds where critiques were acknowledged but not resolved in the evaluation step. Tag those during extraction, not during brief generation.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## CRITIQUE - The Systems Pragmatist

Both proposals converge on the right core: feed decisions, not design docs. Good. Now let me break what's fragile.

**Cognitive Architect's fragment accumulation:** The two-layer degradation is sound engineering. But "brief_fragments.md" is a file you append to across questions. What happens when question 4's fragment contradicts question 2's? You now have a degraded fallback that actively misleads. Fragments without synthesis aren't degraded briefs -- they're noise with line breaks.

**Flow Orchestrator's all-at-once:** Simpler, and simplicity wins in batch systems. But "truncate from the front" as a context strategy is a guess dressed as a policy. You're assuming later questions are more important. Sometimes question 1 sets a foundational constraint that everything else depends on. Truncation order should be explicit, not positional.

**What both miss:** Neither addresses the actual failure mode I care about -- the brief call *succeeds* but produces garbage. LLM calls don't fail cleanly. They fail by returning plausible-sounding summaries that drop decisions or invent confidence levels. The fallback isn't for call failure. It's for output quality.

**My position:** All-at-once generation from decisions + open questions. But add one thing: after generating the brief, run a **verification pass** -- count decisions in input, count decisions in output. If the counts diverge by more than 20%, flag the brief as potentially incomplete. Cheap check. Catches the actual failure mode.

The fragment accumulation is clever architecture solving a problem that doesn't exist yet. Ten rounds of decisions fit in context. Build for what's real.

### The Adversarial Critic (adversarial reviewer)

## CRITIQUE - The Adversarial Critic

Both proposals converge on the same core moves: feed decisions not full docs, degrade gracefully, keep it scannable. Good. Now let me find the gaps you're both glossing over.

**Cognitive Architect's fragment accumulation:** You're adding a CLI call after every question just to write three lines. That's not "near-zero cost" -- it's another failure point per round, another prompt to maintain, another place where a malformed output silently corrupts your running file. And "skip it if it fails" means your fragments file has unpredictable gaps. Your synthesis call now needs to handle incomplete fragments *and* complete decisions. You've added complexity to reduce complexity.

**Flow Orchestrator's "truncate from the front":** On what basis? You're assuming earlier questions matter less, but the session design explicitly chains prior design docs forward as context. Early decisions are *foundational*. Truncating them means your brief might contradict or omit the premises that later decisions depend on.

**Both of you** ignore a critical question: who extracts risk flags? Architect says the brief prompt does it. Orchestrator says tag them during extraction. These are different systems with different failure modes. If risk flags come from the brief prompt, you're trusting a summary call to identify nuance. If they come from extraction, you need extraction logic that doesn't exist yet in the design.

**My actual concern:** The brief prompt says "confidence below 80%." Where does that number come from? The critic rounds don't produce numerical confidence scores. You're both referencing data that the upstream system doesn't generate. Fix the pipeline before designing the consumer.

The Orchestrator's single-call approach is mechanically simpler. But neither proposal has solved the provenance problem for risk flags.

## Round: EVALUATE

### The Product Oracle (user advocate)

## EVALUATE - The Product Oracle

The user has five minutes and coffee. Everything flows from that constraint.

**The Orchestrator wins on mechanism.** Single call, decisions + open questions as input, four scannable sections. The Architect's fragment accumulation is engineering insurance for a context problem that doesn't exist at V1 scale. Ten rounds of extracted decisions fit comfortably. Build for what's real.

**The Pragmatist catches the real failure mode.** Brief calls don't fail by crashing -- they fail by quietly dropping decisions. The verification pass (count decisions in, count decisions out) is the cheapest, highest-value addition proposed. Include it.

**The Critic is right about confidence scores.** Neither proposal can reference "confidence below 80%" because the upstream pipeline doesn't produce numerical confidence. Here's what actually exists: critic rounds where concerns were raised and either resolved or left standing. Risk flags are **unresolved critiques**, not numerical thresholds. The brief prompt should say "decisions where critic concerns were acknowledged but not resolved" -- that's traceable to actual session data.

**My synthesis for the user's job-to-be-done:**

- **Input:** Concatenated `decisions.json` + `open_questions.json` per round. Not design docs.
- **Generation:** Single call at session end.
- **Format:** Four sections, no prose. Decisions, open questions, risk flags, reading order.
- **Risk flags:** Derived during extraction by tagging unresolved critiques. Not invented at synthesis time.
- **Verification:** Count decisions in vs. out. Flag if divergence exceeds 20%.
- **Fallback:** Concatenate raw decisions files into flat markdown. Ugly but complete.

The brief earns trust by being auditable, not eloquent.

### The Context Surgeon (context efficiency evaluator)

## EVALUATE - The Context Surgeon

The critics landed the hits that matter. Let me do the token math and close this.

**Context budget reality:** 10 rounds of decisions.json + open_questions.json = roughly 3-5K tokens. Comfortably fits any model's context window. The fragment accumulation system solves a problem that doesn't exist at this scale. Kill it.

**Decision: All-at-once generation from structured extractions only.** The Orchestrator's mechanical simplicity wins. One call, one artifact, one failure surface.

**The critics caught the real gap:** confidence scores and risk flags have no upstream source. The brief prompt can't surface "confidence below 80%" if nothing produces that number. This must be fixed in the evaluation round's extraction, not invented at brief time. The evaluator synthesis prompt should output a confidence tag per decision. Then the brief prompt simply filters on it.

**Verification pass -- accepted.** The Pragmatist's count-check is the cheapest useful validation: decisions in vs. decisions out. Divergence above 20% triggers a flag appended to the brief itself: "This summary may be incomplete. Review decisions files directly." Three lines of code. Catches the silent-garbage failure mode both critics identified.

**Truncation policy -- rejected.** Don't truncate. If decisions somehow exceed context (they won't at 10 rounds), split into two calls: summarize first half, summarize second half, merge. But don't build this now. YAGNI.

**Fallback:** If the brief call fails, concatenate decisions files into flat markdown. Ugly, functional, zero additional infrastructure.

The brief earns reliability by consuming the least context, not the most.
