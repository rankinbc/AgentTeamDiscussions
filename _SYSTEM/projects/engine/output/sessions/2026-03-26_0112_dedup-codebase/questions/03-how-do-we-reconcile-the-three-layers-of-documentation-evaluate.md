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
