# Discussion Brief: Game Data Pipeline -- Next Steps and Analysis Strategy

## Project Summary

We are building a game information gathering system that extracts structured JSON data from games for comparative analysis. The end goal: build a rich, cross-game dataset that helps inform design decisions for creating our own game in the future.

The pipeline currently has three stages:

1. **Initial Research** -- A 21-task iterative process (via ClaudeContainer's ralph loop) where an AI researcher builds a comprehensive prose game-spec.md covering every aspect of a game's design: mechanics, stats, history, technical implementation. Completed for 11 games.

2. **Entity Extraction** -- Reads the completed game-spec.md in a single pass to identify all entity types (ships, weapons, factions, etc.), their schemas, and relationships. Outputs a game-entities.json. Completed for 2 games (Escape Velocity and TMOS).

3. **Entity Deep-Dive** -- Takes discovered entity types and extracts complete data for every instance using research agents with web search (critical for accuracy -- general-purpose agents fabricate game data). Done for Escape Velocity (11 of 13 entity types, though 10 need redoing because only ships.json used proper web-verified research; the rest used general-purpose agents that hallucinated data).

## What We Know Works

- The 21-task research loop produces comprehensive prose specs reliably
- Entity extraction from prose works in a single pass when the spec is thorough
- Research agents with web search produce dramatically more accurate entity data than general-purpose agents (the EV ships.json vs everything else proves this conclusively)
- The pipeline scales -- 11 games researched, 2 extracted, pattern is repeatable

## What We Know Is Broken or Missing

- 10 of 11 EV entity deep-dives need to be redone with research agents (data quality is garbage without web verification)
- No validation layer -- we cannot programmatically tell good data from hallucinated data
- No cross-game schema normalization -- each game's entities.json is self-contained with game-specific schemas
- No analysis tooling exists yet -- we have raw JSON but no way to query across games
- No relationship data between entities (e.g., which ships use which weapons, which factions control which systems)
- The pipeline captures WHAT exists in a game but not WHY it was designed that way

## Games Researched (11 total, game-spec.md complete)

Escape Velocity (1996, space trading/combat), TMOS / The Magic of Scheherazade (1989, NES action-RPG), StarCraft + Brood War (1998, RTS), Warcraft 2 (1996, RTS), Cities: Skylines (2015, city builder), Guardian Legend (1988, NES action/shmup), Stranded Deep (2015, survival), SimCopter (1996, helicopter sim), RPGWO (2004, online RPG), FA-18 Hornet 2 (1994, flight sim), Counter-Strike 1.6 (2000, FPS)

Note: This is a diverse set -- not all space games. The dataset spans RTS, survival, city builder, flight sim, FPS, and action-RPG alongside the space titles. This affects what cross-game analyses are meaningful.

## Open Questions for This Session

### Part 1: Pipeline Next Steps

1. **What pipeline stages are missing between "entity deep-dive" and "ready for analysis"?** We have raw per-game JSON. What processing, normalization, validation, or enrichment steps need to happen before the data is useful for cross-game comparison? Name specific stages with their inputs and outputs.

2. **How should we handle cross-game schema normalization?** Each game has different entity types (EV has "stellar objects," Stellaris has "star systems," Elite has "station types"). Some map to each other, some don't. What is the right approach -- a universal schema, a mapping layer, game-specific schemas with crosswalks, or something else?

3. **What data should we be capturing that we are NOT currently capturing?** Beyond entity stats and attributes, what information about a game's design would be valuable for analysis but is not in our current pipeline? Think about relationships, design intent, balancing philosophy, progression curves, player experience data, historical context.

4. **What validation and quality assurance steps should exist in the pipeline?** Given that LLM-extracted data has known hallucination problems (the EV lesson), what verification, cross-referencing, or confidence-scoring mechanisms should be built into each stage?

### Part 2: Analysis and Artifacts

5. **What comparative analyses become possible with 11+ games of structured data?** Not obvious things like "compare weapon damage across games" -- what non-trivial patterns, design insights, or structural comparisons could you surface that a game designer would actually use?

6. **What artifacts should the analysis produce?** Think deliverables a game creator would actually reference during design work. Not reports that get read once -- reference materials, comparison tools, design pattern libraries, decision frameworks. Name the format and how it gets used.

7. **What analyses would help specifically with creating a new game?** The dataset spans multiple genres (space sim, RTS, survival, city builder, FPS, action-RPG, flight sim). What cross-genre design patterns could the data reveal? And for the space/sci-fi subset specifically (EV, StarCraft, FA-18), what design decisions could the data directly inform? Think economy design, combat balance, progression pacing, faction design, unit/ship classification, resource systems.

8. **What interactive or generative tools could sit on top of this dataset?** Beyond static analysis reports, what tools could use this structured game data as a knowledge base? Think query tools, generators, comparison engines, design assistants, balance simulators.

## Expected Output

- For each question: concrete, specific answers with named mechanisms and artifacts
- Distinguish between "next logical step" and "aspirational but not urgent"
- When proposing analyses, name the specific artifact produced and how a game creator uses it
- When proposing pipeline stages, name inputs, outputs, and what can go wrong
- No code -- describe behavior, data flow, and decisions
- Stay practical: what is achievable with 11 games of JSON data and a solo builder's time

## Constraints

- 250 words max per response
- The user is a solo builder -- everything must be automatable or at least scriptable
- The pipeline runs via ClaudeContainer (Docker + Claude CLI) -- assume that infrastructure
- Research agents with web search are available but expensive in time (each entity type takes ~5 minutes)
- The long-term goal is game creation, not building a game database product

---

## Appendix: Pipeline Context (Real Data)

This appendix shows what the pipeline actually produces at each stage. These are trimmed real examples from completed runs. Use this to understand the current data shapes when proposing next steps.

### Current Status Across All Games

| Game | Year | Genre | Stage 1 (Spec) | Stage 2 (Entities) | Stage 3 (Deep-Dive) |
|------|------|-------|-----------------|--------------------|--------------------|
| Escape Velocity | 1996 | Space trading/combat | Done (290K) | Done (13 types, 73 entities) | 11/13 types done (10 need redo) |
| TMOS (Magic of Scheherazade) | 1989 | Action-RPG hybrid | Done (307K) | Done (17 types, 120 entities) | Not started |
| StarCraft + Brood War | 1998 | RTS | Done (457K) | Not started | -- |
| Warcraft 2 | 1996 | RTS | Done (359K) | Not started | -- |
| Cities: Skylines | 2015 | City builder | Done (368K) | Not started | -- |
| Guardian Legend | 1988 | Action/shmup hybrid | Done (314K) | Not started | -- |
| Stranded Deep | 2015 | Survival | Done (314K) | Not started | -- |
| SimCopter | 1996 | Helicopter sim | Done (322K) | Not started | -- |
| RPGWO | 2004 | Online RPG | Done (147K) | Not started | -- |
| FA-18 Hornet 2 | 1994 | Flight sim | Done (43K) | Not started | -- |
| Counter-Strike 1.6 | 2000 | FPS | Done (65K) | Not started | -- |

### Stage 1 Output: game-spec.md (prose, ~3000-4000 lines)

A 20-section prose document written from a game designer's perspective. Sections 1-2 and 15-21 are universal; sections 3-14 are customized per game genre. Includes specific stats, tables, design rationale, and cross-references between systems.

Example section topics for a space sim: Universe & Star Map, Factions, Ships, Weapons & Outfits, Combat System, Trading & Economy, Mission System, Main Storylines, Planet Interactions, Piracy & Domination, Escort & Fleet System, Difficulty & Progression.

These are large (43K-457K) and comprehensive but are prose -- not machine-readable.

### Stage 2 Output: game-entities.json (schema discovery)

Identifies entity types, their properties, approximate counts, 2-3 examples, and relationships between types. This is a discovery pass, not a completeness pass.

Trimmed real example (Escape Velocity -- showing 1 of 13 entity types):

```json
{
  "metadata": {
    "game_title": "Escape Velocity",
    "game_year": 1996,
    "entity_type_count": 13,
    "total_entity_count": 73
  },
  "entity_types": {
    "Ship": {
      "description": "Player-purchasable or capturable vessel classes",
      "count": 14,
      "common_properties": ["shields", "armor", "max_speed", "turn_rate",
                            "cargo", "weapon_slots", "turret_slots",
                            "purchase_price", "role", "tier"],
      "entities": [
        {
          "name": "Shuttle",
          "properties": {
            "shields": "~100", "armor": "~100",
            "max_speed": "Moderate", "cargo": "~30 tons",
            "weapon_slots": 1, "purchase_price": "~20,000 cr",
            "role": "Starting vessel / early trader"
          },
          "notes": "Deliberately underwhelming to create urgency to upgrade."
        }
      ]
    }
  },
  "relationships": [
    {
      "type": "requires",
      "from_type": "Ship",
      "to_type": "ForwardWeapon",
      "description": "Ships equip forward weapons using weapon_slots"
    }
  ]
}
```

Note the approximate values ("~100", "Moderate") -- this stage captures schema shape and rough data, not exact numbers. The TMOS extraction found 17 entity types and 120 entities from a very different game genre.

### Stage 3 Output: entities/<type>.json (complete data, research-verified)

One file per entity type with every instance and exact property values. This is the GOOD example (ships.json, extracted with research agents using web search):

```json
{
  "entity_type": "Ship",
  "game": "Escape Velocity",
  "description": "All 22 vessels in original EV 1.0.5",
  "count": 22,
  "sources": [
    "https://gamefaqs.gamespot.com/mac/575197-escape-velocity-1996/faqs/2600",
    "https://docs.google.com/spreadsheets/d/1osUivKYxZzszNmVoYIBMUX-fBhJ4hfpDQwvByYdbbFw/edit"
  ],
  "property_definitions": {
    "shields": { "type": "number", "unit": "points", "description": "Shield hit points" },
    "armor": { "type": "number", "unit": "points", "description": "Armor hit points" },
    "shield_recharge": { "type": "number", "unit": "points/sec", "description": "Recharge rate" },
    "max_speed": { "type": "number", "unit": "raw", "description": "Maximum velocity" },
    "cargo_capacity": { "type": "number", "unit": "tons", "description": "Base cargo hold" },
    "weapon_slots": { "type": "number", "unit": "count", "description": "Fixed gun mounts" },
    "purchase_price": { "type": "number", "unit": "credits", "description": "Base shipyard price" },
    "purchasable": { "type": "string", "unit": null, "description": "shipyard, capture, or npc_only" },
    "faction": { "type": "string", "unit": null, "description": "civilian, confederation, rebellion, alien" }
  },
  "entities": [
    {
      "name": "Shuttlecraft",
      "properties": {
        "shields": 18, "armor": 10, "shield_recharge": 2.4,
        "max_speed": 275, "cargo_capacity": 20,
        "weapon_slots": 3, "purchase_price": 9400,
        "purchasable": "shipyard", "faction": "civilian"
      },
      "notes": "Starting ship; cheapest vessel in the game"
    }
  ]
}
```

Key differences from Stage 2: exact numeric values (18, not "~100"), self-documenting property_definitions, source URLs for verification, and complete entity list (22 ships, not 2-3 examples). The other 10 EV entity types were extracted WITHOUT research agents and contain fabricated data -- this is the core quality lesson.

### What the Pipeline Does NOT Currently Capture

- No cross-entity relationships at the instance level (which specific ships carry which specific weapons)
- No design intent or rationale (WHY a ship costs 9400 credits)
- No progression curves (how stats scale across tiers)
- No balance analysis (damage-per-cost ratios, time-to-kill estimates)
- No cross-game mapping (EV's "Ship" vs Stellaris's "Ship" have different property sets)
- No metadata about extraction quality or confidence per field
- No community/reception data (player rankings, meta analysis)
