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


<!-- complete -->
