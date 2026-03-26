# Scope Target: How Small is the Fun Version?

*Generated: 2026-03-25 16:00 | Question 10 | 183s | Mode: ev18hornet*

## Decisions

**DECIDED: Minimum ship count at EV Core Loop milestone is 3.**
Shuttle (respawn regression vessel), Light Fighter (first consequence-bearing hull), and one faction patrol class (capture target and hot-hull seed). The Shuttle must handle and bank perceptibly worse than the Light Fighter. If the flight feel is identical, ship loss carries no regression signal. The three-ship set is sufficient to run the full death → regression → re-engagement loop and seed the capture flow without requiring authored hull variety before the loop is validated.

**DECIDED: Minimum system count at EV Core Loop milestone is 4.**
Starting system, two faction-territory systems with distinct faction ownership, and one contested chokepoint. Three systems collapses contested space into a binary; five adds variety before the loop is validated. The contested chokepoint is the geographic location where the two faction territories overlap — it must exist in the authored YAML graph before Milestone 3 ships.

**DECIDED: Minimum building count at Outpost tier is 4.**
Generator, Landing Pad, Comm Tower, Defense Turret. These are not four assets — they are four systems, each requiring per-settlement exists/destroyed state, co-op sync, raid targeting motivation, and standing-gated rebuild flow. The count is the floor. No building is added to the Outpost vocabulary before the loop is validated with these four.

**DECIDED: Each building must have a distinct silhouette readable from 400 meters altitude in flat-poly.**
Generator is squat and wide. Comm Tower is vertical. Landing Pad is a horizontal plane with a high-contrast color circle. Defense Turret rotates. Silhouette distinctiveness at nav altitude is a design contract on every Outpost building, not an art preference. A building that reads as a gray box from altitude fails its primary function in the atmospheric layer.

**DECIDED: Each building must map to a raider motivation or it is not on the Outpost list.**
Generator: destroys competing economic infrastructure. Landing Pad: disrupts fleet replenishment logistics. Comm Tower: destroys player standing visibility. Defense Turret: removed first to enable targeting of the others. Raid targeting logic must be able to articulate why it selected a building. Destruction without traceable faction motivation is not emergence — it is random damage with faction paint. If a building type cannot be given a raider motivation, it is deferred until post-loop-validation.

**DECIDED: Each of the four systems must have faction disposition authored before session one.**
A system without faction logic baked in before the player arrives is not a playable system — it is placeholder geography that breaks the emergence chain at step one. The authored investment at Milestone 3 is faction ownership, standing threshold, and mission string role per system. A system with geometry but no faction disposition does not count toward the four-system minimum.

**DECIDED: The starting system is a distinct design artifact from the other three systems.**
It is not system number one in a list. It carries the full onboarding load: it must teach what faction standing is through observable behavior before the player makes their first voluntary jump. The starting system requires at least one standing-feedback moment the player did not cause — a faction patrol that ignores the player at neutral standing, notices them after a standing-relevant action, and changes behavior visibly. Not a tooltip. A readable behavior shift in the world.

**DECIDED: The Landing Pad is the first building placed in the first playable session.**
It is the most legible "I made a thing" moment from altitude and the immediate reward for looking down during atmospheric flight. Generator and Comm Tower are functionally invisible until absent. The first building placement must reward the player for the atmospheric layer's core promise — you fly over what you built and you recognize it. Landing Pad earns that moment. It is scoped and built first.

**DECIDED: The first testable loop is one ship, one system, two buildings.**
Shuttle in the starting system. Generator and Landing Pad placed. One faction patrol with standing-responsive behavior. One bar mission. Atmospheric dive loads a placeholder mesh. The player flies over what they placed, lands, takes a mission, and flies back out. This is not Milestone 3 shipped — this is the first moment the question "is this fun?" is answerable. If this loop is not engaging, no content added at Milestone 7 recovers it.

**DECIDED: Build sequence is testable loop first, complete scope second.**
The minimum complete set (3 ships, 4 systems, 4 buildings) is the completion target for the EV Core Loop milestone. The minimum testable set (1 ship, 1 system, 2 buildings) is the first internal validation gate. Development sequences from testable to complete — not by building all four buildings in parallel and integrating at end. Scope estimates must treat each building as a system with state persistence, sync, targeting logic, and rebuild flow. Four buildings is not four asset-weeks.

---

## Open Questions Resolved by This Discussion

**[from Q4] Building type count at Outpost tier:** 4. Generator, Landing Pad, Comm Tower, Defense Turret. This is the floor. Each must have raid targeting motivation and altitude-readable silhouette before it ships.

**[from Q2] Contested chokepoint minimum:** 4 systems support the required geography — two faction territories with one contested overlap and one starting system. Two simultaneous contested chokepoints sharing no trade route is a post-validation scope question; the minimum validated loop requires one chokepoint.

---

## Open Questions Not Resolved — Still Pending

- **[from Q2] Standing gate UX:** How does the map communicate a standing-gated system to a player who has never encountered one? Visual language question unaddressed in this discussion.
- **[from Q2] Starting system faction:** Which faction owns the starting system, and what is their relationship to the two contested chokepoints the player encounters in sessions 2–3?
- **[from Q4] Tier regression rebuild path:** Same founding investment as original construction, or faster recovery path? Standing as primary gate is confirmed; tempo is unresolved.
- **[from Q4] Faction system queryability milestone:** Must be flagged in M5 acceptance criteria before M7 standing-gated rebuild flow is implemented.
- **[from Q5] Fleet AI milestone scope:** At which milestone does the first escort ship have working 2D formation AI?
- **[from Q5] Atmospheric escort behavior:** Separate milestone from 2D AI; timing unresolved.
- **[from Q5] Port run registration options:** Fixed standing cost or player-choice branching at port?
- **[from Q5] Hot-hull faction response:** Hull as hostility trigger vs. standing value — unresolved.
- **[from Q6] Harassment vs. assault raid definitions:** Concrete parameters (ship count ceiling, building damage cap, tier regression eligibility) unresolved.
- **[from Q6] Dual-offline resumption:** Canonical state on next host boot — last committed save vs. elapsed-time reconstruction.
- **[from Q6] Cross-player standing triggers:** Whether Player 1's action moves Player 2's standing track — must resolve before M5 faction API is specified.
- **[from Q6] Return-log milestone slot:** M7 or M8; sequencing dependency, not optional.
- **[from Q6] Host selection protocol:** Fixed or negotiable; asymmetric hosting creates asymmetric faction pressure accumulation.
- **[from Q7] Commitment threshold standing value:** At what standing value does the commitment NPC become available?
- **[from Q7] Inverse axis ratio:** 1:1 or asymmetric — must be a named decision before M5 implementation.
- **[from Q7] Commitment mission count per faction:** One gate or multi-mission string?
- **[from Q7] Faction string state persistence in co-op:** Does Player 1's commitment close Player 2's string?
- **[from Q7] Recovery from degraded-but-uncommitted standing:** Cost and gate must be consistent with tier regression rebuild path.
- **[from Q8] Specific weapon type for raid breach defense:** Not yet selected.
- **[from Q8] Enemy AI behavior thresholds:** Alert range and attack range not specified.
- **[from Q9] Respawn location rules:** Definition of "nearest" and "friendly" port for 2D death.
- **[from Q9] Starter ship acquisition at respawn:** Given, loaned, or purchased; credit floor guarantee required.
- **[from Q9] Hot-hull fate on death:** Whether hull destruction closes or escalates owning faction standing consequence.
<!-- complete -->
