# Transcript: How does prior context get managed as questions accumulate?

*Generated: 2026-03-18 04:00*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

**The Living Spine.**

Forget sliding windows. Forget summaries. Both treat prior context as a *corpus to compress* when it's actually a *structure to maintain*.

After each question resolves, extract exactly three things into a single evolving document — the **Design Spine**:

1. **Decisions** — what was decided, stated as constraints (not rationale)
2. **Dependencies** — which decisions reference or require other decisions
3. **Open tensions** — unresolved contradictions between decisions

That's it. Not summaries of design docs. Not truncated prose. A dependency graph in markdown. Fifty words per decision, max.

Here's why this beats the alternatives:

**Summarization** preserves the shape of each document but loses the *connections between them*. By question 8, you have 7 independent summaries that don't talk to each other. Agents treat them as background reading, not as binding constraints.

**Sliding windows** are worse — they literally forget. Question 8 can contradict Question 2 because Question 2 fell off the window.

**The Spine** is different. It's a single document that *grows denser, not longer*. When Question 5's decision supersedes Question 2's, you update the entry — don't append. When Question 6 creates a tension with Question 3, you mark it explicitly so Question 7's agents can address it.

The Spine stays under 2000 chars even at question 10 because decisions are terse and superseded ones get replaced.

The full design docs still exist in the session folder. The Spine is what enters the prompt. It's the difference between handing someone a stack of meeting notes and handing them the current blueprint.

### The Flow Orchestrator (mechanical flow designer)

Three layers. Nothing more.

**Layer 1: Decisions ledger (always included, never truncated)**

A single running file. Each question appends its extracted decisions and open questions -- maybe 200-300 chars per question. By question 10, that's ~2500 chars. This is the backbone. It's what prevents drift. It's cheap.

**Layer 2: Previous design doc (full, uncompressed)**

Only the immediately prior doc. Question 8 gets the full doc from question 7. This gives the agents local continuity -- they know what was just discussed. One doc, not seven.

**Layer 3: Nothing else.**

The beta system's 6000-char truncation of all prior docs is the wrong shape. It gives you a little bit of everything, which means agents get fragments they can't act on. Fragments cause hallucinated continuity -- agents pretend they remember more than they do.

The decisions ledger solves the "coherent arc" problem. The previous doc solves the "local context" problem. Together they're maybe 4000 chars at question 8. Well under budget, and every token is load-bearing.

**What about summaries?** Don't. Summarization is lossy and adds a processing step. The decisions ledger already *is* the summary -- it's the structured output you're already extracting. Use what you have.

**What about sliding windows of 2-3 docs?** Unjustified complexity. If question 8 actually needs something from question 3, the decisions ledger carries it. If the ledger doesn't carry it, it wasn't a decision -- it was color commentary. Let it go.

Two files in context. Done.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

**CRITIQUE — The Systems Pragmatist**

Both proposals converge on the right instinct: structured extraction over lossy compression. Good. But neither addresses the failure modes that actually kill multi-question sessions.

**On the Spine:** The dependency graph idea is elegant on paper. In practice, who maintains it? The synthesizer agent after each question? That's asking an LLM to perform graph surgery on a document it didn't create. Merge conflicts are inevitable — decision D3 gets restated slightly differently, and now you have two entries that are almost-but-not-quite duplicates. By question 6, the Spine is subtly corrupted and nobody notices because it *looks* structured.

The "update, don't append" rule is particularly fragile. How does the agent know Question 5 *supersedes* Question 2 versus *extends* it? That's a judgment call that requires understanding both decisions deeply — exactly the context you're trying to avoid loading.

**On the Two-Layer approach:** More honest about what LLMs can reliably do. Append-only is mechanically sound. But "previous doc only" has a real gap: Question 8 discusses API design, Question 7 discussed testing strategy, and the relevant prior is actually Question 4 (data model). You'll get coherent *adjacent* questions and incoherent *thematic* ones.

**What I'd actually build:** The Flow Orchestrator's decisions ledger (append-only, no graph surgery) plus the full previous doc. But tag each decision with its question number and topic. When constructing context, include the ledger always and pull the previous doc. Simple, predictable, debuggable.

The Spine is a v2 optimization. Ship the dumb thing first.

### The Adversarial Critic (adversarial reviewer)

**Both proposals solve the same problem and pretend the other doesn't exist.**

The Cognitive Architect's "Design Spine" and the Flow Orchestrator's "Decisions Ledger" are the same artifact wearing different hats. Terse decisions, dependency tracking, replace-don't-append. Fine. But the Spine claims it "stays under 2000 chars at question 10" with zero evidence. Fifty words per decision, ten questions averaging three decisions each — that's 1500 words before you add dependencies and tensions. The math doesn't work unless you're aggressively pruning, which you haven't specified a mechanism for.

The Flow Orchestrator's two-layer model is cleaner mechanically but has a blind spot: **what happens when question 8 depends on question 3's design doc, not just its decisions?** "If the ledger doesn't carry it, it was color commentary" is a convenient dismissal. Design rationale isn't color commentary. When question 8's agents need to understand *why* a constraint exists to evaluate whether a new approach violates its spirit, a terse decision entry won't cut it.

Neither proposal addresses **who maintains the context artifact**. The synthesizer? A post-processing step? A dedicated extraction prompt? This isn't a minor detail — it's the failure mode. If extraction is sloppy, the whole scheme degrades silently. You won't know decisions are missing until question 9 contradicts question 4.

**What I'd actually probe:** Take your beta transcripts. Manually build both proposed artifacts for questions 1-5. Measure what gets lost. That's your answer — not architectural elegance, but empirical loss rates.

The real risk isn't the strategy. It's assuming extraction reliability you haven't tested.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The Product Oracle — Evaluate**

The job to be done isn't "manage context efficiently." It's **"ensure question 8's agents make decisions that question 2's agents would recognize as coherent."**

Frame it that way and the answer clarifies fast.

The Adversarial Critic landed the punch nobody wants to acknowledge: extraction reliability is the load-bearing wall, and nobody's tested it. Both proposals assume the decisions ledger will be accurate. If it's not, everything downstream is quietly poisoned. That's not a v2 concern — that's a ship-blocker.

But the Systems Pragmatist gave us the buildable answer: **append-only decisions ledger plus previous doc.** Not because it's theoretically optimal, but because it's the only proposal where failure is visible. A corrupted dependency graph looks correct. A missing entry in an append-only ledger is obviously missing.

My synthesis for V1:

**Ship the two-layer approach.** Decisions ledger (append-only, tagged by question number and topic) plus the immediately previous design doc. No graph surgery, no summarization, no sliding windows.

**But add one thing:** after each question, run a lightweight validation — does the new design doc reference any decision not in the ledger? If yes, the extraction missed something. Flag it. This is your empirical loss rate measurement, built into the loop instead of done manually.

The Spine is genuinely good thinking for V2, once you have data on what actually gets lost. Optimize after you can measure.

**Decision: append-only ledger + previous doc + extraction validation.**

### The Context Surgeon (context efficiency evaluator)

**EVALUATE — The Context Surgeon**

The critiques exposed the real fault line: both proposals assume reliable extraction without specifying the mechanism. Everything downstream depends on that.

**What converged:**
- Structured extraction beats summarization and sliding windows. Unanimous.
- Append-only beats graph surgery. The Pragmatist and Critic both flagged update-in-place as fragile, and they're right. LLMs performing merge operations on their own prior output is an untested dependency.
- A decisions ledger is the minimum viable context artifact. Both proposals contain one.

**What's unresolved:**
- Whether the previous doc alone provides sufficient thematic reach. The Critic's question-8-needs-question-3 scenario is legitimate but unquantified.
- Extraction reliability. Nobody proposed a validation mechanism.

**My assessment:**

Ship the Flow Orchestrator's two-layer model. Decisions ledger (append-only, tagged by question number and topic) plus the immediately prior design doc. Budget: ~4000 chars at question 8. Every token traceable to a source.

The Spine is architecturally superior but operationally premature. You can't maintain a dependency graph until you've proven your extraction is consistent enough to feed one. That's a v2 concern.

The Critic's empirical test suggestion is the highest-value action item. Run questions 1-5 from your beta transcripts through both schemes. Measure decision coverage at question 5. If the ledger-only approach drops below 80% of relevant constraints, you need the Spine's structure. If it doesn't, you've saved yourself a brittle subsystem.

**One addition neither proposed:** include the current question's topic tag when constructing context, so the ledger can be scanned for relevance even by a human reviewer debugging drift.
