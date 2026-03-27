### The Context Surgeon (context efficiency evaluator)

## The Critic landed the right punch. Build on it.

The turn-vs-token confusion is disqualifying. Any truncation strategy operating in *turns* is measuring the wrong unit. Retire that framing now.

**What actually matters: token-budgeted relevance, not recency.**

Recency bias (sliding window) assumes the last N turns are the most informative. That's false for structured discussions where foundational decisions in turn 2 outweigh procedural chatter in turns 18-22. Recency is a *proxy* for relevance — a lazy one.

**The real problem is information density decay.**

Early turns in a discussion carry high signal: constraints established, decisions locked, scope defined. Later turns carry high noise: elaboration, rephrasing, social agreement tokens. A token-budget-aware strategy should weight by *decision density*, not position.

**Concrete agenda for this round:**

1. **Define the budget first.** What's the target token ceiling for history passed to each agent? Without this number, every strategy is hand-waving.

2. **Separate audit log from agent context.** Full history lives on disk for humans. Agents get a *compressed operational summary* plus the last 2-3 turns verbatim. These are different artifacts with different consumers.

3. **Measure compression fidelity.** The critic asked for a coherence test — fair. Minimum viable test: does the receiving agent correctly identify decisions already made? Binary, checkable, not "vibes-based coherence."

**The binding constraint isn't summarization vs. windowing.** It's: *who encodes what to compress, and does that encoder know which tokens were load-bearing?*

That's the question worth answering.

### The Product Oracle (user advocate)

## Everyone is optimizing for the wrong job.

The actual job-to-be-done here isn't "preserve discussion coherence." It's **"deliver a Morning Brief the user finds valuable."** All of this infrastructure exists to serve that output. When we lose sight of that, we start solving interesting engineering problems that don't improve what lands in the user's inbox.

Here's what I'd push back on:

**The Context Surgeon's "decision density" framing is compelling but pre-mature.** You can't weight by decision density without first knowing which decisions were load-bearing — and that requires the very LLM call the Systems Pragmatist correctly banned from v1. We've reinvented the compressor agent with better vocabulary.

**The measurable test exists and it's simple:** does the Morning Brief produced with truncation get flagged by the user as missing context or feeling repetitive? That's the coherence test. It's behavioral, not synthetic. It closes the loop the Adversarial Critic correctly said was missing.

**My recommendation:**

Build `window` mode in turns as a first pass — imperfect, yes — because the token-count variation problem is real but *second-order*. If the average agent turn is roughly consistent in length (likely, given structured prompts), turns-as-proxy holds well enough to ship. Instrument it: log when truncation triggers, track brief quality signals if you can.

The Adversarial Critic is right that you haven't proven this is the binding constraint. Don't build `bookends`. Don't build token budgeting. Ship the window. Watch the briefs. **Let users tell you what broke.**


<!-- complete -->
