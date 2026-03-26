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
