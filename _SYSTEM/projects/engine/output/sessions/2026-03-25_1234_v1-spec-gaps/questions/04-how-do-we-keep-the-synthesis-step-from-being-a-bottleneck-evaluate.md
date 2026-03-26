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
