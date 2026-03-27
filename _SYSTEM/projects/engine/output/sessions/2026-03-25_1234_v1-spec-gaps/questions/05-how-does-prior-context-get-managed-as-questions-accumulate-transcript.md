# Transcript: How does prior context get managed as questions accumulate?

*Generated: 2026-03-25 12:49*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

The 6000-char truncation is a blunt instrument solving the wrong problem. Truncating raw design docs is like summarizing a conversation by cutting off the last speaker mid-sentence — you preserve volume, not signal.

Here's the actual problem: **prior context serves one function** — preventing question N from contradicting or re-litigating what question N-3 already resolved. It is not a reference library. Agents don't need the full reasoning chain; they need the binding constraints.

**My proposal: sliding window of 3, verbatim.**

Pass the three most recent design docs forward, unmodified. Archive everything older. No summarization.

Why not summarization? Because summarization adds a lossy LLM call to every question transition, compounds errors across 10 questions, and solves a problem that doesn't exist at the scale we're building for. A 10-question session has at most 3 docs in the window — roughly 1,800 words of prior context. That's well within budget without any compression.

Why 3, not 2 or 5? Three captures the local coherence arc — setup, elaboration, consequence — without carrying stale early-session constraints that no longer bind. The first two questions are often framing questions whose decisions are already embedded in the decisions.json artifact. The window doesn't need to reach them; the decisions list does.

The fragment log already solves the long-range coherence problem. Prior docs solve short-range elaboration continuity. These are different jobs. Don't conflate them.

**Sliding window of 3, no summarization, decisions.json for long-range binding.** That's the architecture.

### The Flow Orchestrator (mechanical flow designer)

This is already decided. Sliding window of 3, verbatim, earlier docs archived. The Cognitive Architect is proposing the conclusion we landed on two questions ago. We are covering old ground.

The unresolved operational question is the assembly sequence, not the policy.

**Concrete sequence for question N context assembly:**

1. Session start: question IDs registered in order.
2. Question N begins: collect the three most recent *written* design docs by slot position — including tombstones.
3. Pass those three docs as prior context. No filtering, no modification.

The tombstone case is the only decision point here. A tombstone occupies a slot in the chain. If questions 5, 6, and 7 are in the window and question 6 tombstoned, does the window skip it and pull question 4? **No.** Tombstones stay in the chain. The tombstone's one-sentence content explicitly signals the gap. Skipping it silently re-introduces the invisible-failure problem we already solved at the session level.

So: window is the last 3 slots by position, tombstones included, no exceptions.

**What this resolves:** Prior docs pass tombstones forward as context-chain entries. Downstream agents see the gap explicitly rather than inferring from missing reasoning.

**What remains open:** The exact format the window docs are injected into the propose prompt — whether they're labeled by question ID, separated by headers, or appended raw. That's a prompt template detail, not an architecture decision, but it needs to be specified before implementation.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

The sliding window of 3 is decided. Stop re-proposing it.

Here are the actual failure modes nobody has addressed:

**1. Tombstones poison the window disproportionately.**
Window slots are 3. If questions 5, 6, 7 all tombstone, the window for question 8 contains three one-sentence failure notices and zero substantive context. The agent proceeds with effectively no prior context. This isn't a gap — it's a silent context collapse that looks identical to a healthy window. The downstream agent has no way to distinguish "prior questions resolved cleanly" from "prior questions all failed."

**2. Window position 3 is an unvalidated assumption.**
Why 3? The prior doc says it "caps prior-doc contribution at roughly 1,800 words." That calculation assumes average design doc length. What's the actual distribution? A question that resolves in one round produces a short doc. A question that hits retry limits and partial rounds produces a tombstone. The 1,800-word estimate could be off by 3x in either direction. This has never been measured against the beta system's actual outputs.

**3. The inject format is unspecified and consequential.**
The Flow Orchestrator correctly flags this as unresolved. Unlabeled raw concatenation of three docs will cause the proposing agent to lose track of which context belongs to which question. This isn't a prompt template detail — it's a context corruption risk.

**4. "Written design docs by slot position" has a race condition.**
Async extraction means a design doc could be written but its fragment not yet appended. The window reads the doc; the fragment log lags. These diverge silently.

The prompt template for context injection needs to be decided now, not deferred again.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic's point 1 is real but the response to it is wrong.

**Consecutive tombstone scenario:** Three tombstones in the window is a symptom, not a failure mode. The actual failure mode is that the session didn't abort when it should have. `min_success_fraction` exists precisely for this. If questions 5, 6, and 7 all fail, you're already at or below the abort threshold for most session lengths. The session shouldn't reach question 8. If it does, that's a config miscalibration, not a window design flaw.

**The race condition (point 4) is the real issue.** Async fragment extraction means "doc written to disk" and "fragment appended to log" are not atomic. The window reads the doc. The prior-doc chain and the fragment log can diverge. This isn't theoretical — it's a predictable interleaving failure. The fix is straightforward: context assembly for question N reads docs from disk directly, not from the fragment log. The fragment log feeds synthesis only. These are different consumers. Don't conflate them.

**The inject format cannot be deferred again.** Raw concatenation is a context corruption vector. Minimum viable spec: each doc prefixed with a labeled header (`## Prior Context: Question {id} — {title or FAILED}`), newline-separated. That's it. One line per doc, deterministic, no LLM involvement. This is an implementation detail that becomes a debugging nightmare if left unspecified.

**Window size of 3:** The 1,800-word estimate is untested. Instrument the beta system. Measure actual doc lengths across 10 runs before assuming the window holds.

Prompt template is still open. That's the blocker.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The user never sees the window. They see the Morning Brief.**

That reframe matters. Every word spent on window architecture is justified only if it protects coherence in the output the builder reads at 8am. So let me evaluate against that standard.

**What's resolved and should stop being debated:**
Sliding window of 3, tombstones included, no summarization. Decided. The Cognitive Architect re-proposed a conclusion we already own. The Flow Orchestrator is correct — stop.

**What's actually at risk for the user:**

The Systems Pragmatist has the race condition right: context assembly reads docs from disk; fragment log feeds synthesis only. These are different consumers. That's a clean separation and protects the Morning Brief from divergence.

The inject format is the remaining gap that directly affects user-perceived output. Raw concatenation means later questions produce muddier reasoning, which produces muddier fragments, which produces a weaker Morning Brief. The Systems Pragmatist's one-line fix — labeled header per doc, `## Prior Context: Question {id} — {title or FAILED}` — is sufficient. It's deterministic, debuggable, and costs nothing. **Adopt it.**

**What I'd push back on:**

Instrumenting doc lengths across 10 beta runs before proceeding is the right instinct eventually, but not a blocker now. The window of 3 is a reasonable default. Ship it, observe it, tune it. The config key exists precisely so the builder can adjust without code changes.

**The one remaining open item that genuinely blocks implementation:**

The fragment extractor prompt template. That's what produces the fragments that feed the Morning Brief. Everything else is downstream of it. Decide the template.

### The Context Surgeon (context efficiency evaluator)

**The window count is decided. The window budget is not.**

Three docs, no per-doc size cap, is not a token budget — it's a count cap that still allows unbounded accumulation. If average doc length is 800 words (~1,067 tokens), three docs contribute ~3,200 tokens to every downstream question call. At question 8, that's consistent, which is the point. But "consistent" and "affordable" are different properties. The 1,800-word estimate from the prior doc addresses synthesis input. Agent call context is a different budget line and nobody has put a number on it.

**Flag the conflation:** The prior doc window serves two consumers with different tolerances. Synthesis input is bounded by fragment log design (~1,150 tokens). Agent call context is bounded by... the window count alone, which is insufficient. These need separate budget ceilings or the window-of-3 decision is half-specified.

**Minimum addition to close this:** Add a per-doc token cap — call it `prior_doc_max_tokens`, default 500. Truncate from the bottom of each doc (conclusions first, rationale last — invert the truncation direction from naive head-truncation). The labeled header format the Systems Pragmatist specified survives this; the header is 10 tokens, not subject to the cap.

**On the fragment extractor prompt:** Every round notes it's open. Nobody is drafting it. The template needs exactly four extraction targets with one-sentence constraints each. That's a 15-line prompt. The deferral is the waste. Draft it or assign it — carrying it as "open" is pure context overhead at this point.

<!-- complete -->
