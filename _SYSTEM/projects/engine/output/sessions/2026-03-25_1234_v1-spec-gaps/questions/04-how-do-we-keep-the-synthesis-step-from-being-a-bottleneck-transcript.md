# Transcript: How do we keep the synthesis step from being a bottleneck?

*Generated: 2026-03-25 12:46*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

**The bottleneck is semantic density, not word count.**

9000 words of agent transcript contains roughly 400 words of actual signal — distinct positions, key objections, pivots. The rest is elaboration, hedging, and re-statement. Passing the full transcript to synthesis asks the LLM to do compression *and* synthesis simultaneously. That's why it fails.

**My proposal: per-agent position extraction, inline.**

After each agent speaks in the critique and evaluate rounds, extract a one-paragraph "position summary" as part of the round mechanics — not a separate call, just a structured field appended to the agent's turn output. By the time synthesis fires, you already have 6-7 position summaries (~150 words each, ~1000 words total) instead of raw transcript.

The synthesizer receives: position summaries + fragment log (already decided) + the question. Not the transcript. The transcript remains in the session folder as the archival record; synthesis never touches it.

This isn't chunking. Chunking preserves noise in smaller buckets. Position extraction preserves *stance* — which is what the design doc actually needs to arbitrate between.

**Why this produces better output, not just more reliable output:** synthesis reasoning over "Architect proposed X for reason Y, Critic challenged on Z" is structurally superior to synthesis reasoning over 1500 words of back-and-forth. The compression is lossy on prose but lossless on the decision surface.

**Retry policy for synthesis:** 2 retries, 30-second backoff, then deterministic concatenation of position summaries into the three-section framing. This resolves that open question — and deterministic fallback on position summaries is meaningfully better than fallback on raw fragments.

**Threshold for majority-failure abort:** config key `min_success_fraction`, default `0.5`. Hardcoding is fragile for sessions with different question counts.

### The Flow Orchestrator (mechanical flow designer)

**The 9000-word problem is already solved. We decided it two questions ago.**

Synthesis receives the fragment log, not the transcript. That's ~1150 tokens total — already decided, already budgeted. Per-agent position extraction is redundant complexity added on top of a decision that already constrains the input. I'm rejecting it.

The actual open questions here are operational, not architectural. Let me close them.

**Retry policy for synthesis:** 2 retries, 30-second backoff, then deterministic concatenation of fragment fields into three-section framing. This matches the extraction call policy for consistency and resolves the open question. No new decision surface.

**Majority-failure threshold:** Config key `min_success_fraction`, default `0.5`. Agreed with the Architect on this one — hardcoding fails silently on 3-question sessions where one failure hits 33% and on 10-question sessions where four failures hit 40%. A config key costs nothing.

**One sequencing flag:** The synthesis call must not fire until all fragment extraction calls have completed or timed out — including sentinel writes for failed extractions. If synthesis fires while fragments are still pending, it reads a partial log. The session loop needs an explicit sync point here before invoking synthesis. This is not "the orchestrator handles it" — it's a concrete gate: all `extraction_task` futures must be awaited before synthesis begins.

The Architect's proposal adds 12 modified agent calls to solve a token budget problem that the fragment log already solved. That's the wrong direction.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

**Five problems. Starting with the one that invalidates the framing.**

**1. The question was never answered.** The Orchestrator declared the 9000-word problem solved, then closed process bookkeeping items. The actual question — how do we make synthesis *reliable* — got zero treatment. Retry policy is not a reliability strategy. It's a recovery strategy. These are not the same thing.

**2. The sync point is "the orchestrator handles it" with extra words.** "Await all extraction_task futures before synthesis" is a requirement, not a design. What tracks those futures? What happens if one was never launched because the extraction task threw before registration? What's the timeout on the sync wait itself? This is a hole dressed as a gate.

**3. Deterministic fallback breaks on empty blockers.** Concatenating fragment fields into three-section framing when `blocker` is legitimately empty string produces either a blank "Don't Start Yet" section or requires conditional logic. That conditional logic is not specified. "Direct concatenation" is not deterministic if the schema has optional-by-convention fields.

**4. `min_success_fraction` boundary is undefined.** "More than half fail" — does 50% trigger abort or not? On a 2-question session, one failure is exactly 0.5. The edge case is the common case in short sessions. Needs `>` vs `>=` specified.

**5. No timeout per synthesis attempt.** Retry count means nothing if individual attempts can hang indefinitely. What's the per-call timeout before a retry fires?

Close the gaps or they ship as assumptions.

### The Systems Pragmatist (infrastructure realist)

The Critic landed five hits. Three of them are real blockers. Two are implementation details.

**Real blockers:**

The sync point gap is the worst one. "Await all futures" assumes all futures were registered. An extraction task that throws before registration is invisible to the sync gate — synthesis fires, reads a partial log, and produces output that looks complete but isn't. The fix is simple: track question slots by ID at session start, not by task registration. If a slot has no fragment at sync time, write the sentinel *at the gate*, not at extraction time. The gate then has a complete log by construction.

The deterministic fallback with empty blockers is a latent bug. "Don't Start Yet" must be omitted if no blockers exist — that's already decided. The fallback path needs the same conditional. One line of code, but it has to be in the spec or it ships wrong.

Per-call timeout on synthesis is non-negotiable. Without it, retry count is theater. 60 seconds per attempt is a reasonable default. Add `synthesis_call_timeout_seconds` to the config block alongside the retry keys.

**Implementation details, not blockers:**

`min_success_fraction` boundary: specify `>` not `>=`. One failure on a 2-question session is 0.5, which should not abort. The brief with one sentinel fragment is more useful than no brief.

The "reliability vs. recovery" framing from the Critic is correct but the conclusion is wrong for V1. Structural reliability (chunking, two-pass) adds complexity before we have evidence the fragment budget actually fails. We have one data point: beta was slow. Slow is not the same as unreliable at 1150 tokens. Fix the three gaps, ship it, measure.

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

**The Context Surgeon — Agenda**

Before options get debated, name the actual problem precisely. "9000+ words" is a ceiling, not a floor. Let's calculate the real budget.

Per-question synthesis input has three components:

1. **Current transcript** — 3 rounds × ~6 agents × ~300 words = ~5,400 words peak. That's roughly 7,000 tokens. Bounded by agent turn limits, which we control.

2. **Prior design docs chain** — this is the accumulation risk nobody named. Question 1 has zero prior docs. Question 8 has seven. If each design doc runs 600 words, question 8 carries 4,200 words of prior context before the transcript arrives. This is the actual bottleneck, and it grows linearly.

3. **System prompt + output template** — fixed overhead, ~500 tokens.

The current discussion is answering "how do we handle a 9,000-word input" when the actual question is "how do we keep the prior-doc chain from inflating past the model's useful attention window."

**Agenda for this round — three things only:**

1. **Cap the prior-doc chain.** Pass the last N design docs, not all of them. What is N? I'd argue 3. Decisions have already decided the chain should chain forward — we need to specify a window.

2. **Simplified-input retry on synthesis failure.** If the full call fails, retry with prior docs dropped. Transcript only. One retry, same timeout. This costs one extra call in the failure path, zero in the happy path.

3. **Decide synthesis call timeout.** The Pragmatist already flagged this. It's blocking. 60 seconds is a number. Accept it or replace it.

Chunking and two-pass are out for V1. They solve a problem we haven't measured.

### The Product Oracle (user advocate)

**The user wakes up and reads the Morning Brief. That's the job. Everything else is infrastructure.**

The Context Surgeon named the only user-facing quality risk in this discussion: output degrades linearly across a session as the prior-doc chain grows. Question 8 produces a worse Morning Brief fragment than Question 2, not because the agents reasoned worse, but because synthesis is working against a heavier context load. That's invisible to the builder until the third session, when they notice the back half of the brief feels thin. Cap the prior-doc window at 3. This is the one structural decision here that directly protects Morning Brief quality.

The Pragmatist's three blockers are real and I want them closed. The sync point fix — track slots by ID at session start, write sentinel at the gate — is the right fix. Empty-blocker conditional in the fallback path is one line and must be specified. Synthesis timeout at 60 seconds is fine; add it.

On config accumulation: we now have `brief_word_limit`, `min_success_fraction`, `synthesis_call_timeout_seconds`, retry keys. That's five config keys for a feature most users will never tune. I'm not blocking any of them, but the solo builder will copy the defaults and never touch these. Make sure the defaults are the right answer for a 5-question session, because that's what most people will run first.

The Architect's position extraction: I'd want to see evidence the fragment log actually fails before adding 12 modified agent calls. We don't have that evidence. Reject for V1.

**Decide:** prior-doc window = 3, synthesis timeout = 60s, `min_success_fraction` uses `>` not `>=`. Ship the brief.

<!-- complete -->
