# How do we reconcile the three layers of documentation?

*Generated: 2026-03-26 01:20 | Question 3 | 136s | Mode: default*

## Decisions

**Single authoritative documentation layer.** `_SYSTEM/docs/` is the sole canonical location for operational and design documentation. All other layers are either archived snapshots or deleted. There is no valid state in which multiple layers carry equal authority over the same subject matter.

**CONCERNS.md is an operational artifact, not a planning snapshot.** Its citation in `_SYSTEM/CLAUDE.md` as required reading before touching fragile areas makes it load-bearing by function, regardless of its current location. It moves to `_SYSTEM/docs/` without content modification. Its location in `.planning/codebase/` is vacated.

**The remaining six `.planning/codebase/` files are archived in place.** ARCHITECTURE.md, CONVENTIONS.md, INTEGRATIONS.md, STACK.md, STRUCTURE.md, and TESTING.md each receive a `generated: 2026-03-25` header and a warning block:

```
> SNAPSHOT — point-in-time analysis. Not maintained. Do not inject into AI context.
> Authoritative sources: _SYSTEM/docs/ and the codebase itself.
```

No file is deleted. No file is moved. The headers are the archive signal.

**`/docs/` (project root) is excluded from all automated AI context injection immediately.** The layer was generated on 2026-03-26 and has no human owner, no invalidation trigger, and no freshness signal. It is accurate today and will silently become wrong. Each file in `/docs/` receives a visible header:

```
> GENERATED SNAPSHOT — 2026-03-26. Not maintained. Do not use as authoritative reference.
> See _SYSTEM/docs/ for current design documentation.
```

The directory is not deleted at this time. It may be useful as a human reference in the short term. Automated context injection — including any `Read` instructions in CLAUDE.md files, session bootstrap hooks, or AI context generation tooling — must not pull from `/docs/`.

**The CLAUDE.md files are the injection control plane.** Any file that currently references `.planning/codebase/` files other than CONCERNS.md must be updated to remove or redirect those references. Any file that references `/docs/` for authoritative content must be updated to reference `_SYSTEM/docs/` instead. CLAUDE.md files are the only place where "read this before proceeding" instructions live — they are not supplemented by undeclared injection from other layers.

**Staleness policy for `_SYSTEM/docs/`.** Files in `_SYSTEM/docs/` are human-maintained. There is no automated regeneration. The update trigger for any file in this layer is: a deliberate architectural decision changes the behavior, structure, or constraints it describes. Cosmetic edits do not require updates. Generated content is never written to this layer.

**No new generated documentation layers are created.** If codebase analysis tooling runs again, its output is written to a timestamped directory (e.g., `.planning/snapshots/2026-03-26/`) and explicitly excluded from context injection at the point of creation. It is never written into `_SYSTEM/docs/` or `/docs/` without human review and promotion.

**Read order when subject matter overlaps.** If two documents address the same subject, the one in `_SYSTEM/docs/` is authoritative. Archived snapshots in `.planning/codebase/` and generated files in `/docs/` are never authoritative, regardless of recency.

**Morning Brief risk.** The acute failure mode is: session bootstrap injects a stale `/docs/` layer, agents receive a wrong codebase map, and Morning Brief output reflects those errors without warning. The exclusion of `/docs/` from automated injection is the direct mitigation. The migration of CONCERNS.md to `_SYSTEM/docs/` is the direct mitigation for missing operational constraints at session start.

---

## Implementation Sequence

1. Add archive headers to all six non-CONCERNS files in `.planning/codebase/`.
2. Add snapshot headers to all files in `/docs/`.
3. Move CONCERNS.md to `_SYSTEM/docs/CONCERNS.md`.
4. Update `_SYSTEM/CLAUDE.md` reference from `.planning/codebase/CONCERNS.md` to `_SYSTEM/docs/CONCERNS.md`.
5. Audit all CLAUDE.md files for references to `.planning/codebase/` (excluding the now-archived snapshots) and `/docs/` as authoritative sources; update or remove each reference found.
6. Verify: grep for any session bootstrap or hook configuration that pulls from `/docs/` or `.planning/codebase/`; remove or redirect.

No Python changes. No session runner changes. No package changes. This is documentation and CLAUDE.md pointer surgery only.
<!-- complete -->
