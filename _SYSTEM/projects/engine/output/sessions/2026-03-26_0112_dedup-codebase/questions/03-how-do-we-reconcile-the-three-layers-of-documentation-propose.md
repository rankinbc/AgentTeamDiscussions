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


<!-- complete -->
