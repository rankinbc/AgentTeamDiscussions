# System Review: Hierarchical Game Knowledge Builder

A system for building comprehensive, structured knowledge bases about retro video games. Contains enough mechanical detail — exact formulas, stat tables, algorithms, ROM-verified values — that an AI developer could generate requirements documents and write code to mechanically clone the game (excluding assets). Think of it as a complete "implementation specification" derived from research rather than source code access.

## What's Already Decided

- Each game lives in `analysis_games/<GameName>/` with a `game_specs/` folder containing all knowledge
- Knowledge is organized hierarchically: depth = precision (top = prose overviews, leaves = exact formulas/tables)
- Flexible depth per system — combat may have 4+ levels, save system may only need 2
- Two-role pipeline: research agents (find data, output raw files) and organizer agents (slot data into hierarchy, dedup, cross-reference, resolve conflicts)
- This separation exists because parallel researchers create overlapping/misplaced data when they each try to organize findings into a shared structure
- Provenance tagging on every factual claim: ROM_VERIFIED > COMMUNITY_VERIFIED > GUIDE_SOURCED > INFERRED > OBSERVED
- [UNKNOWN: est X-Y] tags for unfindable data with plausible estimated ranges
- Recursive research pipeline: Level 0 bootstraps from existing specs, Level 1+ waves investigate specific unknowns with user approval between waves
- First consumer: The Magic of Scheherazade (NES, 1989) — Level 0 complete (18 system READMEs, ~71KB), Level 1 in progress (4 research agents active, 12 proposals prioritized)

### Folder Structure Example

```
game_specs/
  README.md                    # Level 0: Game overview, system index
  systems/
    combat/
      README.md                # Level 1: How combat works conceptually
      action_combat/
        README.md              # Level 2: Detailed action combat mechanics
        damage_formulas.md     # Level 3: Exact formulas, pseudocode
        enemy_stats.json       # Level 3: Exact numeric tables
```

## Open Questions

1. **Is the hierarchical folder structure the right format for AI consumption?** The knowledge is organized as a file tree where depth = precision. Would a database, single large structured document, or graph be better for downstream AI consumption (generating requirements docs, writing clone code)? What are the tradeoffs for each format at the point where an AI developer agent needs to actually USE this data?

2. **Is the researcher/organizer split the right pipeline architecture?** Research agents find data and output raw files. Organizer agents trail behind and slot findings into the hierarchy. Is this separation optimal, or is there a better way to prevent overlap and gaps? What happens when two researchers find conflicting data about the same mechanic?

3. **Is the provenance tagging system well-designed?** Every claim is tagged (ROM_VERIFIED, GUIDE_SOURCED, COMMUNITY_VERIFIED, INFERRED, OBSERVED, UNKNOWN). The hierarchy resolves conflicts. Is this sufficient? Too complex? Are there missing categories? How should provenance propagate when derived data combines multiple sources?

4. **What problems will emerge at scale?** Consider 10+ games, 1000+ files, multiple research waves per game. What breaks in the folder structure, the research pipeline, the organizer workflow, or the provenance system? Where are the bottlenecks?

5. **Is the UNKNOWN estimation approach viable for game generation?** When data can't be found, it's tagged as [UNKNOWN: est X-Y] with a plausible range so a downstream game generator could fill in a reasonable value. Is this the right strategy, or will estimated ranges create cascading inaccuracies when multiple unknowns interact in the generated game?

6. **What's missing for the "generate a clone from this data" step?** Assume the knowledge base is complete. What additional information, structure, or metadata would an AI developer agent need to actually produce a working game clone? What's the gap between "we know all the mechanics" and "we can generate code"?

7. **How could the research process be smarter about finding data?** Better sources, better search strategies, ROM analysis automation, community engagement patterns — what would make the research agents more effective at extracting precise mechanical data from retro games?
