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
