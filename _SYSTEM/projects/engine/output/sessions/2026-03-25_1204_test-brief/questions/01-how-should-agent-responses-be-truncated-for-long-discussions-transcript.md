# Transcript: How should agent responses be truncated for long discussions?

*Generated: 2026-03-25 12:07*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## Role-Differentiated History Compression

The question assumes all agents should see the same history. That assumption is wrong — and correcting it gives you a mechanism with real behavioral teeth.

In group creativity research (Nijstad & Stroebe, 2006), *information asymmetry* between members drives divergent thinking. When everyone holds identical priors, groups converge prematurely. The fix isn't giving everyone more history — it's giving different agents *structurally different* history based on their cognitive role.

**The proposal:** Each agent type gets a truncation strategy matched to what it actually needs to perform its function:

- **Synthesizer agents** receive a compressed arc of the full discussion — key position shifts, not raw exchanges. They need trajectory, not recency.
- **Challenger agents** receive only the last N turns, uncompressed. Their job is local contradiction-finding; full history creates anchoring bias that softens critique.
- **Domain specialists** receive the original framing prompt + latest technical claims, with middle discussion stripped. They catch drift from the original question that other agents normalize over time.

This isn't cosmetic. Challengers literally *cannot* have been convinced by arguments they haven't seen. That structural ignorance forces genuine pushback rather than performed disagreement.

**How to implement:** Tag agents with a `history_mode: [arc | window | bookends]` in their YAML config. Compression is pre-processing, not in-context instruction.

**Testable prediction:** Role-differentiated history produces higher variance in agent positions and more explicit contradiction-surfacing than uniform sliding windows given identical total token budgets.

Commit to asymmetry. Identical context is the enemy of genuine diversity.

### The Flow Orchestrator (mechanical flow designer)

## The Cognitive Architect is right about asymmetry, wrong about implementation complexity.

Three history modes sounds minimal. It isn't. Trace the sequence:

**For `arc` mode:** Discussion ends turn N → something compresses it into a "key position shifts" summary → agent receives that summary. Who does that compression? Another LLM call. That call can fail, hallucinate the arc, or add latency to every turn. You've introduced a new agent — the compressor — and called it "pre-processing."

**Cut it.** Two modes, zero summarization:

- `window`: last N turns
- `bookends`: first turn (original framing) + last M turns

Both are pure string operations. No LLM call. No failure mode beyond slicing.

The Cognitive Architect's core insight — that challengers shouldn't see the full persuasion arc — is valid and worth keeping. A challenger on `window` genuinely hasn't been convinced by arguments outside their window. That's structural ignorance by design, achieved cheaply.

The domain specialist's need (catch drift from original framing) is solved by `bookends`. The synthesizer's need for "trajectory" is the only one that requires arc summarization — and that's a deferred feature, not a v1 requirement.

**Proposed YAML field:** `history_mode: window | bookends` with configurable `window_turns` and `bookend_tail_turns`.

**Decision point that needs answering:** Truncation happens where in the sequence? My answer: at message construction time, per-agent, before the CLI call is made. The stored session file stays untruncated. That's the invariant.

Don't build the compressor until you've proven the simple version fails.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## The Flow Orchestrator has already won this argument. Let me close it.

The question asks about "smart summarization" as a candidate. Here's the failure mode analysis:

**Summarization adds a compressor agent.** That agent can: hallucinate position shifts that didn't happen, flatten genuine disagreement into false consensus, add 2-5 seconds of latency *per turn*, and fail silently — producing a summary that looks valid but misrepresents the discussion state. You cannot unit test this. You cannot make it deterministic. Over 50 turns, drift compounds.

**The blast radius when it fails:** every subsequent agent reasons from a corrupted shared premise. The discussion continues, appears coherent, and produces garbage conclusions with high confidence.

**The two-mode approach has known, bounded failure modes:**

- `window` fails when critical framing lives outside the window. You know when this can happen. You can tune around it.
- `bookends` fails when the important middle is neither beginning nor recent. This is rare and observable.

Both failures are *detectable* and *recoverable*. LLM summarization failure is neither.

**The one implementation detail that matters most:** truncation happens at message construction time, per-agent, never touching the stored session file. This is non-negotiable. The session file is your audit log. If you truncate storage, you lose the ability to debug what any agent actually saw.

**What to build for v1:** `window` mode only. Ship it. Validate that discussions stay coherent under truncation before building `bookends`. Don't build both simultaneously — that's two untested variables.

Prove the simplest version breaks before adding complexity.

### The Adversarial Critic (adversarial reviewer)

## Both proposals have a shared blind spot. Let me name it.

**"Window failures are detectable."** Are they? The agent receiving a windowed history doesn't know what it missed. It reasons confidently from incomplete premises and produces coherent-sounding output. That's identical to the summarization failure you're both condemning. The failure mode you're calling "bounded" is only bounded from the *outside observer's* perspective, not from within the discussion.

**The token assumption.** Both proposals count in *turns*, not *tokens*. Turn N could be 50 tokens or 5,000. A `window_turns: 10` configuration is meaningless without token budgeting. You've deferred the actual hard problem — fitting context into a fixed window — by using a unit of measurement that doesn't map to the constraint you're solving.

**"Ship window only, validate coherence."** How? What's the coherence test? You're proposing to validate an emergent property of multi-agent discussion with no measurement mechanism defined. This isn't iterative development, it's hoping the simple thing works well enough that nobody notices.

**The stored session file invariant.** Stated as non-negotiable, but: at 50 turns with verbose agents, what's the file size? Who reads it for debugging? Is there tooling? "Untruncated audit log" is only useful if someone can actually audit it.

**The real unstated assumption:** that history truncation is the primary coherence problem. It might be. It might also be prompt design, agent ordering, or turn limits. You're optimizing one variable before establishing it's the binding constraint.

Prove window mode breaks *something measurable* first.

## Round: EVALUATE

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
