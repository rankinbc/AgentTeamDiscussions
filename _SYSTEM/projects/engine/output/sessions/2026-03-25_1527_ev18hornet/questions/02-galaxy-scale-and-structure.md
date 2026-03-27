# Galaxy Scale and Structure

*Generated: 2026-03-25 15:34 | Question 2 | 155s | Mode: ev18hornet*

## Decisions

**Galaxy scale at Milestone 3 is 4–6 systems, authored in YAML, with placeholder atmospheric meshes.**
**The full galaxy map is visible from session one. Standing gates access, not visibility.**
**Authored investment at this stage is faction geography and mission string placement — not atmospheric terrain variety.**
**Atmospheric identity expansion is deferred until the EV Core Loop milestone identifies which planets earn repeat visits.**

---

## Galaxy Scale and Structure: Design Specification

### Governing Decisions

The galaxy uses a small, fully hand-authored system graph. Procedural generation is not a current build target. The authored investment is faction logic, chokepoint placement, and mission string structure — not per-planet terrain art. These are different cost curves and must not be conflated in scope estimation.

Scale expands in two phases:

- **Milestone 3 (Galaxy Layer):** 4–6 systems. Faction geography defined in YAML. Atmospheric terrain is one placeholder mesh per planet, color-swapped for biome identity. The core loop either works or it doesn't.
- **Post-EV Core Loop:** Atmospheric identity is built out for the planets that real player data shows earn repeat visits. You are not building 45 planets. You are building the 8 that matter.

Procedural generation reopens only after the authored template proves the loop works. At that point, procedural generation produces *variants of a proven contested-zone structure*, not a substitute for one.

---

### Map Visibility

The full galaxy map is visible from session one.

Hidden systems are a scripted reveal mechanic dressed as exploration. Emergent exploration operates on a known state: the player can see what exists, but earning access requires standing, faction passage, or jump point control. This is agency over a legible board — not authored content drip.

Standing gates what is worth having. The map shows everything. Those two rules are not in tension.

---

### System Count and Faction Geography

**Minimum viable structure for testable faction collision: 4–6 systems.**

This requires:
- 3–4 faction territories with deliberate overlap — systems where two factions both have a stake
- 1–2 contested chokepoints where trade routes cross and faction interests collide
- The player's settlement zone placed such that expansion puts them into the contested area naturally

Clean territorial partitions — factions with non-overlapping domains — are worse than a small authored map. Two hundred procedurally generated systems can produce clean partitions. Six hand-placed systems can guarantee collision zones. The authored choice is *where faction interests intersect*, not what the planet looks like.

Faction geography is defined in YAML as graph structure: which faction controls which systems, which systems are contested, which jump routes pass through chokepoints. This is a week of design work. It scales to 30 systems without breaking budget.

---

### Planet Identity

Planet identity comes from faction logic and mission string placement — not terrain art.

EV's planets were functionally identical visually. Their sense of place came from which missions threaded through them, which faction's equipment they sold, and what standing you needed to land safely. Terrain art tells the player almost nothing without that layer active.

At Milestone 3, each planet has:
- A faction owner or contested status
- A role in at least one mission string thread
- A standing threshold for safe approach
- One placeholder atmospheric mesh, color-coded to biome type

Distinct atmospheric terrain geometry is built after the core loop milestone, targeting only the planets that demonstrably earn repeat visits.

---

### First Jump Design Contract

The starting system has a different design contract from the rest of the map.

The faction legibility language must be taught before the player enters a contested chokepoint. Faction colors, standing feedback, and raid telegraphing all make their first impression simultaneously — alongside the flat-poly aesthetic and the atmospheric layer transition. Dumping a new player into a collision zone before they understand what faction indicators mean produces chaos that reads as punishment, not strategy.

The starting system must contain:
- One dominant faction with legible color and behavior
- A clear standing feedback moment — a positive interaction and a negative consequence visible within the first session
- No contested chokepoint pressure until the player has made at least one voluntary jump

The first jump is the moment the galaxy map, the standing system, and the atmospheric layer first cohere as a single game. That moment must exist at Milestone 3. Everything else is Milestone 5 or later.

---

### Scope Rules

| Authored element | Cost structure | Milestone |
|---|---|---|
| Faction territory graph (YAML) | ~1 week | M3 |
| Chokepoint placement and trade routes | ~1 week | M3 |
| Mission string scaffolding (per system) | ~2–3 days per system | M3–M5 |
| Placeholder atmospheric mesh (color-swapped) | ~1 day per planet | M3 |
| Distinct atmospheric terrain per planet | 2–4 days per planet | Post-core-loop |
| Procedural variant generation | Unestimated | Post-core-loop |

Building 45 distinct atmospheric planets before the core loop is validated is out of scope. The sequencing rule: prove the loop first on placeholder terrain, then build atmosphere for the planets that earn it.

---

### Open Questions

- **Contested chokepoint minimum:** What is the minimum number of systems needed to support two simultaneous contested chokepoints that do not share a trade route? (Vera's question — answer drives final system count at M3.)
- **Standing gate UX:** How does the map communicate a standing-gated system to a player who has never encountered one? (Visual language question, not architecture.)
- **Starting system faction:** Which faction owns the starting system, and what is their relationship to the two contested chokepoints the player will encounter in the first 2–3 sessions?
<!-- complete -->
