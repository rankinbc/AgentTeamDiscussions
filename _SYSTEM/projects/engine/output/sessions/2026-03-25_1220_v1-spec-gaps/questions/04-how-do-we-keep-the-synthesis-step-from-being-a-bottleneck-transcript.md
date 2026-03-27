# Transcript: How do we keep the synthesis step from being a bottleneck?

*Generated: 2026-03-25 12:32*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

The framing is slightly wrong, and fixing it resolves most of the problem.

**The synthesis bottleneck is in the design doc write, not the brief generation.** The brief is already protected — it consumes only extracted structured fields plus prior brief. That's lean by design. The real 9000-word problem is the design doc step, where all three round outputs get passed to produce the per-question artifact.

**My proposal: The evaluate round is the compression point. Use it.**

The evaluate round already reads propose and critique and produces a synthesized assessment. Passing all three rounds to the design doc writer is redundant — you're asking for synthesis of a document that already contains synthesis. The evaluate output *is* the natural compression boundary.

**Concrete mechanism:**
- Design doc writer receives: evaluate round output + extracted fields (decisions, open questions, sharpest objection)
- Propose and critique round outputs go to transcript only
- This cuts input to the design doc call from ~9000 words to ~2000-3000 words

**Why this holds:**
- Evaluate was explicitly designed to judge and integrate the prior rounds — it's not a summary, it's a synthesis
- Extracted fields capture the three most forward-relevant signals
- No information loss for the brief chain (brief never touched propose/critique directly)
- Design doc quality may *improve* — less noise from redundant competing proposals

**On the retry question:** Accept degraded output over no output, but degraded means "evaluate output forwarded as design doc verbatim" — not a blank file. The evaluate round already exists on disk. Use it.

Two-pass outline-then-fill adds latency without addressing the root cause. Fix the input size first.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect's diagnosis is correct. I'll confirm the sequence implication and flag the one remaining decision point.

**Confirmed routing:**
1. Propose round → transcript only
2. Critique round → transcript only  
3. Evaluate round → transcript + design doc input
4. Extract fields from evaluate output → structured fields
5. Design doc write: `evaluate_output + extracted_fields` → `design_doc_{n}.md`
6. Synthesize: `extracted_fields + previous_brief` → `brief.md`

Steps 5 and 6 already have separate, bounded inputs. The bottleneck was never architectural — it was an uncontrolled input to step 5. Constraining step 5 to evaluate output alone fixes it without adding any new moving parts.

**One decision still open:** What is the size bound on evaluate output? If evaluate output itself grows unbounded (agents are verbose; no truncation exists today), step 5 inherits the same problem one round later. The fix is a hard word truncation on evaluate output before it enters step 5 — not a retry policy, not a two-pass approach. One truncation threshold, applied at the boundary.

**On "accept degraded output":** The Cognitive Architect proposes forwarding evaluate output verbatim as the design doc on failure. I'd sharpen the trigger: this fallback activates only on step 5 API failure or timeout, not on output quality. The verbatim evaluate output is already a valid artifact — it's on disk, it's structured, it's forward-usable. Name it `design_doc_{n}_fallback.md` to match the existing fallback convention.

No chunking. No two-pass. Fix the input boundary and set one truncation limit.

## Round: CRITIQUE

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

## Round: EVALUATE

### The Product Oracle (user advocate)

**The critics are right. Close the false debate and ship the two actual decisions.**

Synthesis was solved three questions ago. The Morning Brief has a bounded, structured input: extracted fields plus prior brief. That chain is clean. Everything being argued about "synthesis reliability" belongs to step 5 — the design doc write — which has no input contract at all. That's the live problem.

**Here's what users actually experience:** They wake up to a Morning Brief. They don't read design docs. Design docs exist to feed the context chain — their quality matters only insofar as they produce better decisions for the next question and, ultimately, a better brief. That means the design doc write needs to be reliable and bounded, but it doesn't need to be beautiful.

**Two decisions need to land:**

1. **Truncation threshold for evaluate output entering step 5.** The Systems Pragmatist said 1500 words. That's a reasonable conservative bound — take it. Don't measure it against beta output first; that's a V2 refinement. Pick the number, log it in `defaults.yaml`, and move on.

2. **Fallback doc inheritance.** `design_doc_{n}_fallback.md` is inherited by Q(n+1) identically to a primary doc. No detection logic. No branching. The fallback *is* the design doc for that question. Name it consistently, treat it uniformly.

Everything else in this discussion — two-pass, chunking, retry-with-simplified-input — is complexity in search of a validated problem. The user needs a brief that arrives. These two decisions get us there.

### The Context Surgeon (context efficiency evaluator)

**The question is wrong. That's the first problem.**

"How do we keep synthesis from being a bottleneck" — synthesis has a bounded, structured input. That was decided. The question is still pointing at the solved problem. Two rounds of discussion followed the wrong pointer. The evaluator should flag this as a session-level failure mode: stale question framing propagates wasted compute.

**What the discussion actually resolved — and what's still open:**

The Product Oracle and Systems Pragmatist converged correctly. Accept both decisions:

1. **Evaluate output truncated at 1500 words before step 5.** Rationale: conservative bound, covers dense discussions, revision deferred to V2 with empirical data. Log in `defaults.yaml`. Done.

2. **Fallback design docs are inherited identically.** No detection branch. `design_doc_{n}_fallback.md` is the doc for Q(n). Q(n+1) inherits it without special handling. Simpler state machine, no implicit branching.

**What nobody said that needs saying:**

The truncation happens *before* the LLM call, not inside it. That means the orchestrator does the word-count and slices the string — not the prompt. If you leave truncation to the model's judgment, you've added a failure surface. Hard truncation in Python on the input string. One line of code. The contract is enforced before the token is spent.

**Cover the open question this closes:** First-call behavior on empty `previous_brief` — omit `## What Got Built`. Confirmed.

Ship the two decisions. Move to the next question.

<!-- complete -->
