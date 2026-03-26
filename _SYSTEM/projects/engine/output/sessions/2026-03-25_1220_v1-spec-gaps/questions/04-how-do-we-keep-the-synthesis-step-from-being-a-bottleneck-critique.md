### The Adversarial Critic (adversarial reviewer)

**Stop. The question is already answered by prior decisions — and nobody noticed.**

The decisions log explicitly states: *"Brief generator consumes only structured extracted fields (decisions, open questions, sharpest objection), not design docs."* The synthesis step's input is three fields from a ~100 token extraction output. The 9000-word problem was already solved architecturally. This question is being re-litigated on a false premise.

**What's actually happening here:**

The Flow Orchestrator just described a *design doc write* that consumes raw evaluate output. That's step 5, not synthesis. But the question asks about synthesis. These are two different steps with two different problems, and the discussion has been conflating them for at least one full round.

**The real problems nobody is naming:**

1. **Step 5 (design doc write) has no decided input contract.** Evaluate output goes in, a design doc comes out — but there's no word budget, no schema, no validation. That's the actual unbounded input problem.

2. **The truncation "fix" is a guess.** What truncation threshold? Based on what evidence? "Hard word truncation on evaluate output" without a number is not a decision, it's a deferral dressed as resolution.

3. **`design_doc_{n}_fallback.md` naming introduces a new convention** that downstream steps must detect and handle. Does Q(n+1) inherit fallback docs the same way? Unspecified.

4. **"Already a valid artifact" is wishful thinking.** Raw evaluate output is unstructured agent prose. Calling it forward-usable because it exists on disk is not an argument.

Push the design doc input contract, not synthesis reliability. That's the live problem.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic is right, and I'll be blunt about why this matters: **two rounds of discussion just burned solving a problem that was already closed.** That's a process failure in the discussion system itself — worth noting for the evaluator.

The actual live failure mode is step 5. Here's the blast radius if it stays unspecified:

**Design doc write has no input contract.** Evaluate output is raw agent prose. Five agents, no truncation, verbose by default — call it 2000-4000 words in practice. The LLM call producing `design_doc_{n}.md` receives all of it. No word budget. No schema. No validation on the output. This is the bottleneck the question was trying to name, just one step off.

**The truncation number isn't optional.** "Hard word truncation on evaluate output" without a threshold is not a decision. It's a placeholder. Pick a number with a rationale: evaluate output truncated at 1500 words before entering step 5. That's enough to cover a dense discussion; anything beyond it is repetition. Measure it against actual beta output if you have it — otherwise pick a conservative bound and revise in V2.

**Fallback naming creates a detection problem.** If Q(n+1) must detect whether its inherited design doc is a fallback, you've added a branch that currently has no spec. Either fallback docs are inherited identically to primary docs (simplest, probably correct) or they aren't — decide it now, don't leave it implicit.

Synthesis is fine. Step 5 needs an input contract. Give it one.


<!-- complete -->
