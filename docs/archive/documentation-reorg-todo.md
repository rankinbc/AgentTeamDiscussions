# Immediate Documentation Reorganization

This file describes a set of documentation cleanup and reorganization tasks for the AgentTeamDiscussions project. The goal is to improve discoverability, reduce redundancy, and surface implementation status -- without losing any valuable information.

## Context

This project is a multi-agent AI discussion platform where two AI teams communicate through an MCP message broker to convert product ideas into implementation-ready specs. The design documentation is extensive (~550KB across 23+ files) but has organizational issues: redundancy, empty directories, untracked implementation status, and a large unexplained `_bmad/` directory.

---

## Task 1: Add a Root README

**What:** Create `README.md` at the project root.

**Why:** There is no entry point explaining what this project is, its current status, or how to run it. Only `CLAUDE.md` (governance rules) and `docs/index.md` (design spec reading guide) exist.

**Content to include:**
- One-paragraph project description (multi-agent discussion platform, MCP broker, overnight spec generation)
- Current status: design-phase, beta code exists in `projects/beta-agent-interaction/`, MCP server not yet implemented
- Directory map explaining the purpose of each top-level folder
- How to run the beta system (reference `projects/beta-agent-interaction/` scripts)
- Pointer to `docs/index.md` for design documentation

**Sources to pull from:**
- `CLAUDE.md` for project rules and directory conventions
- `docs/design_specs/prd.md` for project description and goals
- `docs/index.md` for documentation structure

---

## Task 2: Consolidate proposed_design_docs/

**What:** Merge the 10 design summary files in `proposed_design_docs/` into a single synthesized document. Archive the raw transcripts.

**Why:** Currently 21 files (~200KB) exist as 10 question pairs (a `*-design.md` summary + a `*-transcript.md` raw discussion). The transcripts are bulky and the summaries overlap. A single consolidated doc would be far more useful.

**Steps:**
1. Read all 10 `*-design.md` files in `proposed_design_docs/`
2. Create a single `proposed_design_docs/consolidated-design-decisions.md` that synthesizes the key decisions, organized by topic rather than by question number
3. Move all `*-transcript.md` files into `proposed_design_docs/archived-transcripts/`
4. After consolidation, the original `*-design.md` files can also be moved to an archive subfolder (e.g., `proposed_design_docs/archived-originals/`)
5. Update `proposed_design_docs/index.md` to point to the new consolidated doc and note the archive locations
6. Do NOT delete any files -- archive only

---

## Task 3: Document or Isolate _bmad/

**What:** Determine the purpose of the `_bmad/` directory (1,654 files, 15.1MB) and document it, or flag it for removal.

**Why:** This appears to be a full copy of the BMAD (Brian Multi-Agent Development) skill/agent system. It is not referenced in any project documentation and its relationship to the project is unclear. It may be tooling that was committed alongside the project, or it may be an integral part of the system.

**Steps:**
1. Check if any project code in `projects/` imports from or references `_bmad/`
2. Check if `CLAUDE.md` or any config references it
3. If it is tooling/infrastructure not specific to this project:
   - Add a one-paragraph `_bmad/README.md` explaining it is external tooling, what it provides, and that it should not be edited within this project
4. If it is project-specific:
   - Add a `_bmad/README.md` explaining which parts are active and how they relate to the discussion platform
5. Either way, add `_bmad/` to the root README directory map (Task 1)

---

## Task 4: Clean Up Empty Directories

**What:** Handle `design-artifacts/`, `temp/`, and `projects/mcp-server/src/`.

**Steps:**
- `design-artifacts/` -- If no planned use, remove it. If it has a future purpose, add a `.gitkeep` with a comment in the root README about its intent.
- `temp/` -- Same treatment. CLAUDE.md mentions temp files should be prefixed with `temp_`, but this directory is empty and may be vestigial.
- `projects/mcp-server/src/` -- This is the planned TypeScript MCP server that has not been implemented. Add a brief `projects/mcp-server/README.md` noting it is not yet implemented and pointing to the relevant design specs (`docs/design_specs/v1-orchestrator-spec.md`, `docs/design_specs/session-platform-and-agent-management.md`).

---

## Task 5: Index the experiments/ Directory

**What:** Create `experiments/index.md` cataloging all 72 files with status tags.

**Why:** The experiments directory has substantial content but no index or explanation of what each experiment tested, whether results were useful, or if any are still active.

**Steps:**
1. Read through the files in `experiments/`
2. Create `experiments/index.md` with a table: filename, one-line description, date, status (active/archived/superseded)
3. Group by topic if patterns emerge

---

## Task 6: Create Implementation Status Tracker

**What:** Create `docs/IMPLEMENTATION_STATUS.md` that reconciles what is designed vs. what is built.

**Why:** Implementation status is currently scattered:
- `ideas/discussion-productivity-mechanisms.md` tracks 40+ mechanisms as "Not implemented"
- `docs/beta-agent-output/known-issues.txt` lists 8 critical unfixed problems
- Design specs describe features that don't exist in code yet
- No single view of what works today

**Steps:**
1. Read `ideas/discussion-productivity-mechanisms.md` for the mechanism status list
2. Read `docs/beta-agent-output/known-issues.txt` for known problems
3. Scan `projects/beta-agent-interaction/` to understand what code actually exists
4. Scan `projects/orchestrator/` for its current state
5. Create `docs/IMPLEMENTATION_STATUS.md` with sections:
   - **Working Today** -- what the beta system can actually do
   - **Designed but Not Implemented** -- summarize the 40+ mechanisms and major spec features not yet in code
   - **Known Issues** -- incorporate and update the 8 items from known-issues.txt with any resolution notes
   - **Not Started** -- MCP server, production orchestrator, team configuration system
6. Cross-reference design spec files for each item so a developer can find the relevant spec

---

## Task 7: Reconcile Overlapping Design Specs

**What:** Designate canonical locations for concepts that are currently defined in multiple files, and replace duplicates with cross-references.

**Why:** Several core concepts are repeated across multiple docs:

| Concept | Appears In |
|---------|-----------|
| Entity/data model | `entity-model.md`, `session-platform-and-agent-management.md`, conversation-engine docs |
| Phase system | `prd.md`, `design-decisions.md`, `phase-dynamics.md` |
| Turn model | `turn-anatomy.md`, `design-decisions.md`, `rebuttal-priority.md` |
| Anti-slop mechanisms | `anti-slop-mechanisms.md`, `design-decisions.md`, `research-applied.md` |

**Steps:**
1. For each concept in the table above, read all the files where it appears
2. Determine which file has the most complete/authoritative definition -- that becomes the canonical source
3. In the other files, replace the duplicated content with a brief summary and a cross-reference: "See [canonical-file.md] for the full definition of X"
4. Preserve any unique details from non-canonical files by moving them into the canonical file
5. Update `docs/index.md` to note which file is canonical for each major concept
6. Do NOT delete content -- only consolidate into one location and replace duplicates with references

---

## Execution Notes

- **Do not delete any files** -- archive or consolidate only. This project has no redundant backups and losing information is worse than having it in two places.
- **Preserve git history** -- use `git mv` when moving files to archives.
- **Follow CLAUDE.md conventions** -- no emojis in markdown, descriptive file names, output files in `output/<name>_<date>/` if generating artifacts.
- **Tasks are independent** -- they can be done in any order, though Task 1 (README) benefits from having Tasks 3-6 done first so it can reference the results.
- **Estimated scope** -- primarily reading and reorganizing existing content, minimal new writing required. The largest effort is Task 2 (consolidation) and Task 6 (status tracker) which require synthesizing across multiple files.
