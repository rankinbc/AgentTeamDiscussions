# Should `_SYSTEM/projects/engine/config/teams/` be deleted?

*Generated: 2026-03-26 01:22 | Question 4 | 131s | Mode: default*

## Decisions

**The diff and grep run in parallel before any deletion decision is made.** Neither operation is a prerequisite for the other. Both are required. Neither substitutes for the other.

**Operation 1 — Grep.** Pattern: `config/teams` across `*.py`, `*.yaml`, `*.j2`, `*.json` in `_SYSTEM/projects/engine/`. Extend to isolated `"teams"` token in path-construction contexts to catch dynamic segment assembly (`Path(...) / "teams"`). Zero hits clears this gate. Any hit outside a comment is a hard stop: fix the loader before deletion proceeds. This is not a deletion question; it is a code fix question.

**Operation 2 — Diff.** Byte-level comparison of `_SYSTEM/projects/engine/config/teams/` against `_SYSTEM/data/teams/`. The CLAUDE.md label "stale duplicate pending removal" is an assertion, not a diff. Labels do not update when files are edited directly. The diff is the only output that answers which copy is authoritative by content, not by declaration.

**Deletion is authorized only when both operations return clean.** "Clean" means: grep returns zero hits outside comments, and diff returns identical content. Under that condition, deletion executes as a single commit containing only the directory removal and a CLAUDE.md pointer update removing the "pending removal" note. No other changes are bundled.

**If the diff reveals divergence, stop.** Do not proceed with deletion. Surface the diff for human review. The divergent content in `config/teams/` may represent a persona or configuration change made directly and never propagated to `data/teams/`. Persona drift does not crash sessions — it silently degrades Morning Brief output quality over time with no observable failure signal. The Morning Brief acceptance criterion (writes and is non-empty) does not catch this failure mode. Any divergent content must be explicitly reviewed and, if intentional, propagated to `data/teams/` before the stale copy is deleted.

**If the grep reveals active loaders, stop.** The engine CLAUDE.md hard rule prohibiting use of `config/teams/` as a source of truth does not enforce itself in code. An active loader that violates the rule has a runtime consequence on deletion regardless of content parity. Fix the loader to point at `data/teams/`, confirm the session runner resolves correctly, then re-run both operations to re-establish clean baseline before deletion proceeds.

**The "out of scope" classification from prior decisions does not protect this directory.** The prior scoping decision excluded `config/teams/` cleanup from the `lib/` deletion work to bound that change's scope. It did not defer deletion indefinitely. This question is the correct place to close it.

**Post-deletion acceptance criterion.** A completed `--no-session` run with no import errors or path resolution failures clears the smoke test. The Morning Brief acceptance criterion (full session, writes non-empty) applies if any doubt remains after the smoke test.
<!-- complete -->
