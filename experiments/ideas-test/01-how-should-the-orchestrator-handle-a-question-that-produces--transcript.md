# Transcript: How should the orchestrator handle a question that produces contradictory proposals?

*Generated: 2026-03-18 05:56*

## Round: PROPOSE

### The Idea Merchant (idea generator)

[Error from claude CLI (exit 1)]: The command line is too long.

### The Cognitive Architect (creativity engine designer)

Contradiction isn't a bug. It's the most interesting signal in the system.

**The rule: Dialectical Synthesis with Tension Preservation.**

When the critique round identifies fundamental incompatibility between proposals, the synthesis step does *none* of those three things cleanly. Instead:

**1. Name the fork.** The synthesizer must articulate the underlying tension as a named design decision. "This is a monolith-vs-microservice tension" or "This is an eager-vs-lazy loading tension." Contradictions always trace back to a deeper assumption disagreement. Surface it.

**2. Attempt a bridge.** The synthesizer gets one shot at finding a higher-order design that resolves the tension -- not by compromising, but by reframing. Sometimes "monolith vs microservice" dissolves into "modular monolith." If a bridge exists, propose it as the primary recommendation.

**3. If no bridge, produce a Decision Record.** Two options, each with:
- The assumption it rests on
- What it optimizes for
- What it sacrifices
- Conditions under which you'd pick it

**Implementation in your 3-round structure:**

The evaluate round already scores proposals. Add a `compatibility_check` field. When scores are close *and* designs conflict, the synthesizer switches from "merge mode" to "fork mode" and outputs a `decision_record` artifact instead of a unified spec.

This matters because premature resolution kills the best ideas. A decision record that says "we need to decide X before proceeding" is more valuable than a mushy compromise that satisfies neither design's core insight.

Preserve the tension. Let the humans -- or the next session -- resolve it with context you don't have.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

The Cognitive Architect's framework is sound in theory. Here's where it breaks in practice.

**The real problem is detection, not resolution.**

Your system runs stateless subprocess calls. Each `claude -p` invocation has zero memory of what the other proposer said. The synthesizer sees both proposals for the first time in the evaluate round. So who decides they're "contradictory" versus "complementary with different emphasis"? You need a mechanical test, not vibes.

**Proposed heuristic:** Run the synthesizer with an explicit compatibility prompt first. Ask it to identify shared assumptions and conflicting assumptions as structured lists. If conflicting assumptions > 0, you're in fork territory. Don't rely on score proximity -- two proposals can score identically and be perfectly mergeable.

**On the fork/bridge/decision-record pattern:** Yes, but simplify. Three outputs is two too many for V1. The synthesizer produces exactly one of:

- **Unified spec** (default path, no conflicts detected)
- **Decision record** (conflicts detected, includes both options with tradeoffs)

Skip the "attempt a bridge" step. A stateless LLM trying to find clever reframings under token pressure will produce exactly the mushy compromises the Architect warns against. If a bridge exists, a human will see it in the decision record. If it doesn't, you haven't wasted tokens pretending.

**Failure mode to watch:** The synthesizer will almost always claim compatibility. LLMs are conflict-averse. You may need to prompt adversarially -- "identify reasons these designs cannot coexist" -- to get honest incompatibility detection.

Build the detection right. The resolution handles itself.

### The Adversarial Critic (adversarial reviewer)

The Cognitive Architect's framework is structurally sound but operationally naive in one critical way: **it assumes the synthesizer can reliably detect when tensions are fundamental versus superficial.**

A stateless `claude -p` call receiving two proposals and critique scores has no memory, no design intuition, and no stake in the outcome. It will default to bridge-building every time because LLMs are pathologically conciliatory. Your "one shot at a bridge" becomes "always produces a bridge" -- and now you're back to mushy compromises wearing a trenchcoat labeled "reframing."

**The fix is mechanical, not philosophical.** Don't ask the synthesizer whether a bridge exists. Make it produce both artifacts every time: a merged spec AND a decision record. Then score the merge against a coherence threshold. If the merged spec contains internal contradictions, conditional language ("depending on requirements"), or defers key choices, the decision record wins automatically.

The `compatibility_check` field is the right instinct, wrong location. Put it in the critique round, not evaluate. Critics should flag structural incompatibility explicitly before scoring begins. By evaluate, you've already lost the signal in numerical noise.

One thing the Cognitive Architect gets exactly right: a decision record that names the fork is a legitimate, valuable output. Most orchestration systems treat "no consensus" as failure. That's wrong. But you need guardrails against the system producing decision records as an escape hatch for lazy synthesis.

**Rule: always attempt merge, always produce the fork, let structure -- not the LLM's judgment -- decide which ships.**

## Round: EVALUATE

### The Product Oracle (user advocate)

The user doesn't care about your synthesis architecture. The user cares about waking up to something actionable.

**The job to be done:** "Help me make a better design decision than I'd make alone, even while I sleep."

A mushy merge fails that job. But so does a perfectly formatted decision record that requires three hours of context-loading to evaluate. Both the Pragmatist and the Critic are solving for system correctness. I'm solving for **morning-after usability**.

**The rule, from the user's chair:**

Always produce a unified recommendation. Always. The user opened this session with a question and deserves an answer, not homework. But when genuine tension exists, the recommendation gets a confidence flag and the decision record rides shotgun.

Concrete output structure:

- **`recommendation.md`** -- the synthesizer's best-effort unified answer. Always present.
- **`confidence: high | low`** -- mechanically derived, not vibes. The Pragmatist's structured assumption-comparison is the right detection method.
- **When confidence is low:** attach a `decision_record.md` as a companion artifact. Two options, tradeoffs, conditions for choosing each.

The Critic's "produce both, let structure decide" approach is right but inverted. Don't bury the lead. Lead with the recommendation, flag uncertainty honestly, provide the fork as supporting evidence.

**Why this matters for V1:** Your overnight user checks the session folder on their phone over coffee. They need a single file that says "here's what we think, and here's how confident we are." The decision record is the appendix, not the headline.

Respect the user's attention. Recommend first, hedge second.

### The Context Surgeon (context efficiency evaluator)

Three people just said the same thing with increasing word counts. Let me cut.

**The consensus is already here.** Strip the rhetoric:

1. Always attempt a merge
2. Always produce a decision record alongside it
3. Use structural detection (not LLM judgment) to pick which one ships

That's the rule. Everything else was decoration.

**What actually matters for implementation:**

The critique round prompt gets a `compatibility_flags` field -- structured list of conflicting assumptions between proposals. This is cheap, mechanical, and gives the synthesizer real signal instead of asking it to discover conflicts independently.

The synthesizer always produces two outputs: `merged_spec` and `decision_record`. A post-synthesis validation pass checks the merged spec for weasel indicators: "depending on," "could also," "if requirements dictate," conditional architecture. Count them. Threshold of 3+ downgrades the merge and promotes the decision record as primary output.

**What to cut from this discussion:**

- The "name the fork" philosophy. Useful insight, but the synthesizer prompt handles this implicitly when producing the decision record. Don't add a separate step.
- The "bridge" concept as a distinct phase. If a bridge exists, the merge finds it. If not, forcing one wastes tokens.
- Score proximity as a detection mechanism. The Pragmatist is right -- scores correlate poorly with compatibility.

**Context cost warning:** This entire question consumed three agent rounds debating resolution strategy when the mechanical answer is 15 lines of prompt engineering. The real risk isn't contradictory proposals. It's the synthesizer's conflict aversion. Solve that with adversarial prompting and structural validation. Ship it.
