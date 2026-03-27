# Morning Brief: 2026-03-26_0112_dedup-codebase

*Generated: 2026-03-26 01:26*

## Overnight Design Session Summary
**Date:** 2026-03-26 | **Project:** AgentTeamDiscussions

---

### Overview

Four distinct cleanup tracks were deliberated. Three tracks reached full decision closure with clear execution plans. One track is **blocked on a mandatory code read** before any action is authorized.

---

### Track 1 — `_SYSTEM/lib/` Deletion

**Status: ✅ Fully decided, execution-ready (pending gate clearance)**

The `agentteam/` package is the canonical library; `_SYSTEM/lib/` is deprecated and will be deleted in a single commit. The acceptance criterion is a completed session where the Morning Brief writes and is non-empty — not import graph cleanliness.

**Five gates must clear before deletion:**

| Gate | Condition |
|---|---|
| Gate 1 | Grep across `.py`, `.yaml`, `.j2`, `.json`, `.md` — zero external references to `lib.*` outside `lib/` itself |
| Gate 2 | No `importlib`/`import_module` dynamic references to `lib.*` paths |
| Gate 3 | Explicit confirmation that `agentteam/config_loader.py` loads `prompt_definitions.json` from its own package path |
| Gate 4 | Conditional — only required if Gate 1 finds external imports from `lib/types/`; skipped if zero hits |
| Gate 5 | Smoke test: `python session_runner.py brief.md --no-session` passes cleanly |

**Key rulings:**
- `speak_to_agent.py` and `prompt_builder.py` are **migration targets, not confirmed duplicates** — diff against `agentteam/` counterparts only if Gate 1 reveals external callers; if no external callers, delete with the rest
- Tests that import from `lib/` are testing dead code and are deleted alongside the shims
- Tests that import from `agentteam/` and pass are preserved
- `__init__.py` re-export is explicitly rejected as a valid resolution path
- No `agentteam/` package structure changes permitted

---

### Track 2 — Engine Root-Level Wrapper Cleanup

**Status: ✅ Fully decided, execution-ready (pending classification)**

Scope covers seven engine root-level wrapper files. `_SYSTEM/lib/` deletion, `config/teams/` cleanup, and any outside-engine-root reorganization are **explicitly out of scope** for this track.

**Classification rule:** Confirmed shim (re-exports only, no logic) → deletion list. File with unmigrated logic → migrate to canonical submodule first, then delete.

**Execution rules:**
- Four unconfirmed files (`interact.py`, `conversation.py`, `multi_agent.py`, `evaluate_experiment.py`) must be read and classified before any deletion sequence is designed
- Caller scan runs after classification, covers `.py`, `.yaml`, `.j2`, `.json` across full project scope
- Hits within `_SYSTEM/projects/engine/` itself are excluded from the external caller set
- If zero external callers → delete all confirmed shims in one commit alongside internal call site updates
- If external callers exist → re-point each call site to canonical path and delete shims in the **same** commit (not separate commits)
- External caller defined as any call site outside `_SYSTEM/projects/engine/`, including `_SYSTEM/tests/`, `temp/`, `agentteam/`, and any tooling or config outside the engine directory

---

### Track 3 — Documentation Consolidation

**Status: ✅ Fully decided, implementation sequence locked**

**Canonical authority:** `_SYSTEM/docs/` is the sole authoritative location for operational and design documentation. CLAUDE.md files are the sole injection control plane.

**Implementation sequence (ordered):**
1. Archive headers on six `.planning/codebase/` files (ARCHITECTURE.md, CONVENTIONS.md, INTEGRATIONS.md, STACK.md, STRUCTURE.md, TESTING.md) — `generated: 2026-03-25` header + SNAPSHOT warning block, no content changes, no moves
2. Snapshot headers on all `/docs/` files — `GENERATED SNAPSHOT` header dated 2026-03-26 with pointer to `_SYSTEM/docs/`
3. Move CONCERNS.md to `_SYSTEM/docs/CONCERNS.md` without content modification; vacates `.planning/codebase/CONCERNS.md`
4. Update `_SYSTEM/CLAUDE.md` reference to CONCERNS.md
5. Audit all CLAUDE.md files for stale references to `.planning/codebase/` or `/docs/` as authoritative
6. Grep and remove/redirect any session bootstrap or hook pulling from `/docs/` or `.planning/codebase/`

**Key rulings:**
- `/docs/` (project root) excluded from all automated AI context injection immediately
- `/docs/` is **not deleted** at this time; retained as short-term human reference
- Generated content is never written to `_SYSTEM/docs/` without human review and promotion
- If codebase analysis tooling runs again, output goes to a timestamped directory (e.g., `.planning/snapshots/2026-03-26/`) and is explicitly excluded from context injection at creation time
- When subject matter overlaps, `_SYSTEM/docs/` is authoritative over archived snapshots regardless of recency
- No Python changes, no session runner changes, no package changes — scope is documentation and CLAUDE.md pointer surgery only

**One open question remains:** Whether `/docs/` should eventually be deleted, and what the trigger for that decision should be.

---

### Track 4 — `config/teams/` Stale Duplicate Cleanup

**Status: ✅ Fully decided, gates defined**

**Two gates, both required:**

| Gate | Condition |
|---|---|
| Grep gate | Pattern `config/teams` (and isolated `"teams"` token in path-construction contexts) across `*.py`, `*.yaml`, `*.j2`, `*.json` in `_SYSTEM/projects/engine/` — zero hits outside comments |
| Diff gate | Byte-level diff of `_SYSTEM/projects/engine/config/teams/` against `_SYSTEM/data/teams/` — identical content |

**Hard stops:**
- Any grep hit outside a comment → fix loader to point at `data/teams/` first; confirm session runner resolves correctly; re-run both gates
- Any diff divergence → stop and surface diff for human review; divergent content may represent persona drift never propagated to `data/teams/`, which silently degrades Morning Brief output with **no observable failure signal** (the Morning Brief acceptance criterion does not catch this)
- Any divergent content must be explicitly reviewed and, if intentional, propagated to `data/teams/` before deletion

**When both gates clear:** Delete in a single commit containing only the directory removal and a CLAUDE.md pointer update. No other changes bundled.

**Post-deletion smoke test:** Completed `--no-session` run with no import errors or path resolution failures.

---

### Track 5 — `conversation/state.py` Consolidation

**Status: 🔴 BLOCKED — mandatory read not yet completed**

**The blocking read:** `agentteam/conversation/state.py` must be read before any action is authorized. The engine copy is **not a shim** — it contains real logic, and delete-and-redirect without reading the library counterpart is unsafe.

**Two questions that must be answered from the library file:**
1. Does it contain `should_trigger_uncomfortable_idea()` or equivalent anti-slop quota logic?
2. Does its `_truncated_history()` use the same config keys (`multi_history_truncation_threshold`, `multi_history_keep_first`, `multi_history_keep_last`) via the same `defaults()["conversation"]` call pattern?

**Consolidation path decision tree (locked, pending read results):**

| Library state | Action |
|---|---|
| Has both behaviors, identical config keys | Redirect imports, delete engine copy, single commit |
| Has both behaviors, different config keys | Align config keys first, then redirect and delete |
| Missing `should_trigger_uncomfortable_idea()` | Migrate anti-slop logic to library first; engine copy remains until confirmed |
| Hardcoded truncation thresholds / no config pull | Promote config-driven truncation to library before consolidation |
| Drift with no clear ownership | Hard stop, human review |

**Key risk rulings:**
- A config key mismatch produces **silent truncation behavior drift** not caught by the Morning Brief acceptance criterion
- Missing anti-slop logic causes **silent loss of uncomfortable idea injection** — sessions complete normally, output degrades without error
- "Thin subclass" is explicitly rejected as a consolidation option
- Field-level identity is not semantic identity — shared field names are not a consolidation signal
- **No changes authorized until the blocking read is complete**

---

### Cross-Track Constraints

- The Morning Brief acceptance criterion (full session, writes non-empty) is the primary acceptance signal across all tracks
- No file reorganization outside each track's explicit scope is permitted
- All deletion commits are single-purpose — no bundling of unrelated changes
- This cleanup does not proceed ahead of any work that directly affects the Morning Brief pipeline
<!-- complete -->
