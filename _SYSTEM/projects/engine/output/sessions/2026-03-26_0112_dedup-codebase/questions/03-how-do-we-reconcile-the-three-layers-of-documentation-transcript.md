# Transcript: How do we reconcile the three layers of documentation?

*Generated: 2026-03-26 01:20*

## Round: PROPOSE

### The Flow Orchestrator (mechanical flow designer)

Three layers, three distinct consumers, three different update triggers. The reconciliation question collapses if we trace the read path for each.

**`_SYSTEM/docs/`** — consumed by humans and AI working on design changes. Update trigger: architectural decision changes. Owner: engineers making deliberate design choices. This layer should remain stable between sessions.

**`/docs/` (project root)** — consumed by AI context injection at session start. Update trigger: codebase structure changes. Owner: generation tooling, not humans. If this was generated today, it has a generation timestamp and a staleness window. The critical question is: what regenerates it, and what invalidates it? If nothing enforces regeneration, this layer drifts and becomes a liability.

**`.planning/codebase/`** — consumed during planning phases only. Update trigger: planning invocation. Owner: planning tools. These are point-in-time snapshots. CONCERNS.md is already referenced in `_SYSTEM/CLAUDE.md` as a required read before touching fragile areas — that's a live dependency, not an archive.

**The sequencing problem:** right now, there's no defined read order when layers conflict. If `/docs/ARCHITECTURE.md` contradicts `_SYSTEM/docs/concepts/`, which wins? The answer must be explicit before any merge decision.

**What I need the group to resolve:**
1. Is CONCERNS.md a live gate or a historical snapshot? If live, it belongs in `_SYSTEM/docs/`, not `.planning/`.
2. What is the declared staleness policy for `/docs/`? If there isn't one, that layer is unreliable and should be scoped out of AI context injection until it has one.

Proposals without answers to both questions are premature.

### The Cognitive Architect (creativity engine designer)

The Flow Orchestrator's read-path decomposition is correct, but there's a sharper cut available.

**The real fault line isn't ownership — it's consumption mode.** Documents consumed by humans at deliberate read-time can tolerate staleness and contradiction; the human reconciles. Documents injected into AI context at session start cannot tolerate contradiction — the model has no reconciliation signal, it just uses whatever arrives first or weights by recency heuristics we don't control.

That's why `/docs/` isn't just an organizational problem. It's a behavioral reliability problem. If `/docs/ARCHITECTURE.md` and `_SYSTEM/docs/concepts/` contradict each other and both land in context, you get confident wrong answers about your own system. This isn't theoretical — it's the documented failure mode for RAG systems with stale indices.

**My position on the three questions raised:**

CONCERNS.md is a live gate. The CLAUDE.md reference makes it load-bearing — it's cited as required reading before touching fragile areas. That's not archival, that's operational. Move it to `_SYSTEM/docs/` or make `.planning/codebase/` an explicit first-class read source. Leaving it stranded in `.planning/` means the next AI context injection either misses it or double-loads it without knowing which copy is canonical.

On staleness policy for `/docs/`: the minimum viable policy is a generation timestamp plus a declared invalidation trigger (e.g., "regenerate after any merge to `agentteam/`"). Without that, the layer should be excluded from automated context injection entirely and treated as a human-reference artifact only.

Merge `.planning/codebase/CONCERNS.md` into `_SYSTEM/docs/`. Archive the rest of `.planning/codebase/` as point-in-time snapshots with an explicit `generated:` header.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

The Cognitive Architect's consumption-mode framing is elegant and wrong enough to be dangerous.

**Five problems before we design anything:**

**1. The "AI reconciles at read-time" assumption is false for humans too.** Developers under pressure grab the first answer. The human-tolerance argument is a just-so story that lets us defer the staleness problem indefinitely.

**2. CONCERNS.md isn't a live gate because CLAUDE.md says it is.** A citation is not enforcement. Who verifies the file was read? Nobody. It's aspirational documentation dressed as operational gating. Calling it "load-bearing" doesn't make it load-bearing.

**3. Moving CONCERNS.md to `_SYSTEM/docs/` doesn't fix staleness — it relocates it.** If the content is drifting from reality now, it will drift from reality in the new location at the same rate. Location is not the problem.

**4. The three-layer framing misses the actual fourth layer: the CLAUDE.md files themselves.** There are at minimum four CLAUDE.md files with overlapping scope. Any reconciliation policy that ignores intra-CLAUDE.md contradiction is incomplete before it starts.

**5. "Generation timestamp plus invalidation trigger" is a policy that requires someone to execute it.** Who? On what schedule? Triggered by what event detection? This is "the system will handle it" wearing a timestamp hat.

**My agenda for this round:** Before we assign ownership, we need to answer: what breaks first when these layers contradict, and who is actually maintaining each layer today? Ownership without maintenance accountability is fiction.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic's point 2 is the load-bearing one and everything else should be sequenced behind it: **a citation is not enforcement**. The entire CLAUDE.md instruction chain is aspirational. It works when AI context loads happen to include the right files in the right order. It fails silently when they don't. You have no observability into which failure mode you're actually in on any given session.

So the reconciliation question is secondary. The primary question is: **which of these three layers is actually being read by anything, verified, and acted on?** Before designing ownership, run that audit. My guess is `.planning/codebase/` is read occasionally by humans, never reliably injected into AI context, and drifts freely. `/docs/` was generated today so it's accurate today and will be wrong in six weeks. `_SYSTEM/docs/concepts/` is the closest thing to ground truth but has no freshness signal.

**The simplest version that validates the hypothesis:** collapse to one layer. Pick `_SYSTEM/docs/` as the single authoritative location. Move CONCERNS.md there. Delete or clearly archive `.planning/codebase/` with a `generated: <date>` header and a warning that it's a point-in-time snapshot. Delete `/docs/` or redirect it with an explicit "last generated" timestamp and exclusion from any automated context injection.

The failure mode of three layers isn't contradiction — it's that nobody knows which one to trust, so everyone trusts the one they happened to open first. That's not a policy problem. That's a count problem. Reduce the count.

## Round: EVALUATE

### The Product Oracle (user advocate)

The technical framing here is good. The product question is simpler: **what does the person running this system actually need to look up, and when?**

There are exactly two use cases:
1. "I'm about to touch something fragile — what do I need to know?" → operational reference
2. "I'm orienting a new AI session to this codebase" → context injection

Every documentation layer should serve one of those jobs. If it serves neither, it's archive material.

By that test:
- `_SYSTEM/docs/concepts/` does job 1 today
- CONCERNS.md does job 1 — it's operational, not historical, regardless of where it lives
- `.planning/codebase/` was generated for job 2 but has no freshness signal, making it unreliable for both
- `/docs/` was generated today for job 2 and will quietly become a liability

**The agenda I'm setting:** don't debate ownership. Debate which layer the solo builder will actually trust six weeks from now — and make that the only layer.

My read: `_SYSTEM/docs/` is the only layer with human intent baked in. Everything else is generated or aspirational. Fold CONCERNS.md there. Timestamp and exclude `.planning/codebase/` from AI context injection. Make `/docs/` clearly labeled "generated on X, not authoritative" or delete it.

**The Morning Brief risk is real:** if AI context injection pulls from a stale `/docs/` layer, the session starts with a wrong map. That's not a documentation problem — it's an output quality problem.

One authoritative layer. Everything else is clearly labeled snapshot or deleted.

### The Context Surgeon (context efficiency evaluator)

The Systems Pragmatist and Product Oracle have converged on the correct answer. I'll add the context engineering dimension they've left implicit.

**The token budget framing matters here.** Three documentation layers means three potential injection candidates competing for context window space. The failure mode isn't just "humans trust the wrong one" — it's that any automated context injection system (CLAUDE.md `Read` instructions, hooks, session bootstrap) has to make a bet on which layer to pull. If it pulls all three, you're burning ~15-25k tokens on overlapping material before a single agent has said anything. If it picks one, the selection logic becomes a hidden policy decision with no owner.

**CONCERNS.md is the highest-density artifact in that `.planning/codebase/` set.** It's operational, specific, and directly affects Morning Brief output quality. The other six files (ARCHITECTURE, CONVENTIONS, INTEGRATIONS, STACK, STRUCTURE, TESTING) are point-in-time snapshots — useful when generated, liability when stale. They should get a `generated: <date>` header and be excluded from any automated injection path.

**The `/docs/` layer is the acute risk.** Generated today means accurate today. But it has no staleness signal and no human owner. If session bootstrap pulls from it in six weeks, agents get a wrong map with no warning. Either timestamp it visibly in the filename (`/docs/codebase-snapshot-2026-03-26/`) or delete it.

**Concrete resolution:** CONCERNS.md → `_SYSTEM/docs/`. Everything else in `.planning/codebase/` → archived with timestamps. `/docs/` → renamed with date or deleted. One injection target. Zero ambiguity.

<!-- complete -->
