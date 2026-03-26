# Minimum Building Type Count at Outpost

*Generated: 2026-03-25 17:04 | Question 12 | 237s | Mode: ev18hornet*

## Decisions

**Minimum Building Type Count at Outpost Tier Is Three:** Three building types ship at Outpost: shelter, power node, and storage unit. A fourth type — the defense emplacement — does not earn its slot at Outpost because its strategic role depends on a power-emplacement dependency that is not buildable within M7 scope. A standalone defense emplacement without the dependency is an additional silhouette, not a system node. Silhouettes do not justify the asset commitment; system roles do. The minimum defensible count that creates meaningful raid triage without requiring raid AI structural awareness is three.

**Three-Type Triage Hierarchy Is Asymmetric by Recovery Cost:** Shelter, power node, and storage unit create a legible triage hierarchy without authored guidance because their recovery costs are asymmetric. Storage lost is trade capacity deferred; a player can rebuild it. Power lost has cascading session-level consequences; a player cannot undo time without power. Shelter lost is a living-space setback with mid-range recovery. The hierarchy emerges from the recovery cost differential — the designer does not need to label it. This is the correct minimum-viable-differentiation structure: each type creates a distinct decision, not merely a distinct silhouette.

**Defense Emplacement Earns Scope Only Through the Power Dependency:** The defense emplacement is confirmed as a future building type. It earns its slot in the tier system at the milestone when the power-emplacement dependency ships. Without that dependency, the emplacement is the fifth silhouette — the player is choosing which building to protect, identical in kind to protecting any other passive target. With the dependency, the emplacement is an autonomous actor that covers a raid vector, and the triage calculus changes: the player chooses which vector to cover knowing the emplacement covers another, unless power is down, in which case both tasks fall to the player. That inversion is the emergent situation. It requires the dependency to exist.

**Power-Emplacement Dependency Is Not a Config Flag:** Implementing the power-offline → emplacement-offline dependency requires three discrete systems that do not exist in M7: a building state propagation system defining which buildings affect which; a read path from power state into emplacement active/inactive status; and raid AI that performs a priority pass over live building states before selecting a target vector. The third item is the scope-determining element. Rational targeting in assault-scale raids — where the spawn system queries structural state and sequences attack accordingly — is a weeks-level build item, not a days-level item. It pulls in architectural surface that is not present in M7 as scoped. The dependency does not ship in M7.

**Asset Count at Outpost Is Six:** Three building types at two geometry states each yields six flat-poly models for the Outpost building set. Each model covers silhouette design, ArrayMesh construction, and a degraded variant. This is the asset floor that M8 visual regression estimates must accept as the minimum. If additional building types are added at Settlement, Colony, or City tiers, the asset multiplier grows accordingly — each type added at any tier must carry its degraded geometry state at the time the type is authored, not deferred to a later asset pass.

**Degraded Geometry States Must Communicate Strategic Consequences at Altitude:** The degraded state of a building is not only a damage indicator — it is the primary teaching surface for new players before they have experienced a failed raid. A damaged power node must visually communicate that something else has gone wrong, not merely that the power node itself is damaged. This requirement applies to all three Outpost building types. The visual signal must be legible in flat-poly at 500 meters. This is a communication design constraint on each degraded model, not solely an art direction decision. It is a named requirement for the asset pass, not an implementation detail to be resolved during production.

**Three Is the Triage-Legible Count, Not a Provisional Minimum:** The choice of three is not a compromise pending more design. Three types is the minimum that satisfies all three conditions simultaneously: each type creates a distinct decision; the set is readable from altitude in the flat-poly aesthetic; and the degraded geometry states are buildable before M8 requires them. Adding a fourth type before the power-emplacement dependency exists would add visual complexity to the assault triage window without adding a new triage decision. That trades legibility for an apparent of complexity.

---

## Open Questions

- **Defense emplacement milestone placement:** At which milestone does the power-emplacement dependency earn M7 scope? The dependency requires building state propagation, a power→emplacement read path, and assault raid AI structural awareness. No milestone has been assigned. This question is blocking for any scope estimate that includes the defense emplacement.

- **Power-emplacement dependency raid AI design:** What does "rational targeting" mean for assault-scale raid AI? The spawn system would need to query live building states and sequence attack vectors accordingly. The architecture for that query path — what it reads, when it reads it, how it affects spawn vector selection — is not yet specified. This is a separate open question from the building type count decision.

- **Power node degraded state visual signal:** What visual element on the degraded power node communicates "systems affected" at 500 meters in flat-poly? This is a named asset requirement, not an implementation detail. It must be resolved before the degraded model is built, not after. Currently unspecified.

- **[Carried from Q11] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value:** Named config constant required from day one; numeric value deferred pending M7 building type count and structural damage accumulation rates from playtest. Outpost count is now confirmed at three; Settlement, Colony, and City type counts remain unspecified and are required inputs for this constant.

- **[Carried from Q11] Building type count at Settlement, Colony, and City tiers:** Each tier above Outpost adds building types. The total type count across all tiers gates the M8 visual regression asset estimate. Outpost floor is now three; the remaining tiers are unspecified.

- **[Carried from Q11] Tier regression milestone placement:** Does visual tier regression — geometry change legible from altitude — ship in M7 or M8? Stat-only regression (tier value drops, no geometry change) could ship earlier; geometry regression requires the asset pass acknowledgment first. Not yet placed.

- **[Carried from Q11] Assault-scale split-vector spawn bearing offsets for M7 solo:** What are the two approach bearings for the assault composition in solo play? Bearing offsets must be named config constants. The contested airspace two-spawn-axis geometry for split-commitment co-op remains deferred to M8.

- **[Carried from Q11] First-raid protection window co-op edge case:** In a co-op session, does `player_has_had_clean_atmospheric_view` require both players to have completed an unobstructed descent, or only the player whose standing would trigger the raid? Per prior decisions, standing is per-player and raid spawn queries each player independently; protection window logic should follow the same per-player read path, but the authored rule is not yet confirmed.

- **[Carried from Q3–Q11] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for any milestone.

- **[Carried from Q3–Q11] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after a player triggers the commitment NPC and acts for the opposing faction. Deferred; applies post-commitment only.

- **[Carried from Q5–Q11] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending M5 playtest data.

- **[Carried from Q5–Q11] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Deferred pending playtest data on Hostile band frequency under normal play.

- **[Carried from Q5–Q11] Mission pool sparsity definition in Degraded band:** Probability filter, reduced count, or mission type subset. Implementation rule not yet specified.

- **[Carried from Q3–Q11] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables into NPC dialogue not yet designed.

- **[Carried from Q3–Q11] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

- **[Carried from Q3–Q11] Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions or only upward. Threshold of 40 decided; directional trigger open.

- **[Carried from Q4–Q11] Joint action delta magnitude for co-op:** Full or fractional standing consequence per participating player. Must resolve before M8 mission resolution code ships.

- **[Carried from Q4–Q11] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8.

- **[Carried from Q3–Q11] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Deferred to M8.

- **[Carried from Q6–Q11] Passive decay milestone:** At which milestone, if any, does refusal-tracking decay earn scope. Requires M5 event-only playtest data.

- **[Carried from Q6–Q11] Refusal-tracking attribution rule:** How to distinguish deliberate decline from player absence from never having reached a faction Bar. Unresolved.

- **[Carried from Q6–Q11] `DECAY_FLOOR` numeric value:** Named config constant required, set above `HOSTILE_THRESHOLD`. Value deferred pending M5 playtest data.

- **[Carried from Q9–Q11] Hull capture standing delta magnitude per faction:** Named config constants required; numeric values deferred pending M5 playtest data.

- **[Carried from Q9–Q11] Relative magnitude of hull capture versus mission failure standing consequence:** Unspecified.

- **[Carried from Q10–Q11] Comms intercept string content per faction:** One line per faction contact; exact wording is content design out of scope.

- **[Carried from Q10–Q11] Patrol vector modifier numeric values:** Spawn timing offset and approach angle adjustment must be named config constants; values deferred pending M5 playtesting.

- **[Carried from Q9–Q11] Bribe path design:** Fully deferred pending Bar rumor/informant surface and deferred-state store for hull provenance.

- **[Carried from Q9–Q11] Salvage flag path design:** Fully deferred pending faction-specific grievance tracking.

- **[Carried from Q7–Q11] M6 scope capacity:** Full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7.

- **[Carried from Q7–Q11] Build cost of threat-aware hold state:** Estimate gates M6 vs. M7 placement.

- **[Carried from Q7–Q11] Escort hold visual treatment:** Circular orbit, stationary hover, or trailing vector. UX decision required before M6 ships the layer-transition contract.

- **[Carried from Q8–Q11] Mechanical resolution when a raid spawns during escort hold:** Escort engagement rules, destruction possibility, and player surface state unspecified.

- **[Carried from Q7–Q11] Terrain avoidance timing:** Deferred alongside full atmospheric escort follow to M8.
<!-- complete -->
