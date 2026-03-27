# Minimum Altitude Range

*Generated: 2026-03-25 17:36 | Question 20 | 225s | Mode: ev18hornet*

## Decisions

**The atmospheric floor must be below building roofline.** This is a day-one build requirement, not a feel-state preference or an M8 concern. Building height determines terrain geometry, collision surfaces, and low-pass camera behavior. If the deck is authored above roofline height, those systems cannot be retroactively lowered without touching every building mesh already built. The constraint exists before the first shelter model is authored, not after.

**The floor constraint is geometrically binding, not atmospherically binding.** The reason to set deck below roofline is not the SimCopter payoff moment — though that payoff is real — and not faction standing expression through spatial depth. It is that building height is a terrain authoring input. The deck value gates the collision model. It must be specified as a named config constant `ATMOSPHERIC_FLOOR_ALTITUDE`, constrained to be less than `BUILDING_ROOFLINE_HEIGHT`, before building geometry ships.

**Entry altitude and floor altitude are config constants.** Both are single floats. Specifying numeric values for either before the Hornet Layer milestone is played commits to numbers that cannot be defended without flight model data. The correct approach is the same one applied to `HOSTILE_THRESHOLD`, `RAID_HARASSMENT_THRESHOLD`, and `RAID_ASSAULT_THRESHOLD`: name the constants, constrain the relationship between them, defer the values.

**At Hornet Layer, the column proves one thing: the flight model is fun between two altitude bounds.** The three feel-state architecture — high overview, mid intercept, low kinesthetic — is correct eventual design. It is not a Hornet Layer requirement. Faction pressure expressing as spatial depth, standing reads keyed to altitude band, convergent patrol geometry scaled to intercept band depth — those are M8 integration problems. Wiring them to specific altitudes before the flight model has been playtested is the same error as specifying standing thresholds before mission reward rates are measured.

**The minimum altitude range is the vertical delta between `ATMOSPHERIC_ENTRY_ALTITUDE` and `ATMOSPHERIC_FLOOR_ALTITUDE`.** The range must be large enough that descent takes perceivable time and the view transforms — this is a pacing requirement, not a faction system requirement, and it applies at session one. The range must not be so large that it creates scope obligations for LOD transitions, terrain streaming, or band-keyed system activations before those systems are scoped.

**The faction standing → spatial pressure architecture does not constrain the column at Hornet Layer.** Ren's argument that the intercept band needs reaction depth for converging patrol geometry to register is correct design intent. It is an M8 constraint on intercept band depth, not a Hornet Layer constraint on entry altitude. The entry altitude must not be set *to satisfy M8 intercept geometry* before M8 intercept geometry has been specified.

---

## Open Questions

- **`ATMOSPHERIC_ENTRY_ALTITUDE` numeric value** — config constant required before Hornet Layer ships; value deferred pending flight model playtest data on what altitude makes approach feel like arrival rather than teleportation.

- **`ATMOSPHERIC_FLOOR_ALTITUDE` numeric value** — config constant required before first building mesh is authored; value must satisfy `ATMOSPHERIC_FLOOR_ALTITUDE < BUILDING_ROOFLINE_HEIGHT`; numeric value deferred pending building height authoring decisions.

- **`BUILDING_ROOFLINE_HEIGHT` as a named constant** — whether roofline height is a single authored constant or a per-building-type value affects the floor constraint implementation; must be resolved before the pad damage model and collision surfaces are built.

- **Minimum range depth for pacing** — what vertical separation between entry and floor produces perceivable descent time at Hornet flight speeds; requires Hornet Layer playtest data on approach velocity and bank angle envelope.

- **Three feel-state band boundaries** — high overview, mid intercept, and low kinesthetic band thresholds are confirmed correct eventual design; numeric boundaries deferred to post-Hornet-Layer playtest and M8 faction system integration scope.

- **LOD transition altitude triggers** — whether terrain and building geometry require LOD changes keyed to altitude bands; deferred pending terrain complexity decisions and Hornet Layer performance profiling.

- **[Carried from Q19] Attribution path selection: Path A vs Path B** — must be answered before M7 or M8 attribution scope is locked.

- **[Carried from Q19] Exact co-op comms intercept string content for `max()` conditions** — what P2 reads at atmospheric entry when P1's standing is driving hostile airspace geometry.

- **[Carried from Q17–Q19] Whether M5 shipped comms intercept infrastructure as decided in Q10** — blocking dependency for M7 and M8 extension estimates.

- **[Carried from Q17–Q19] Counter scope for `raids_since_last_docking`** — per-faction or aggregate.

- **[Carried from Q17–Q19] `raids_since_last_docking` reset behavior on docking at non-owned neutral faction port.**

- **[Carried from Q17–Q19] Exact string content for counter output at atmospheric entry.**

- **[Carried from Q14–Q19] Pad destruction and anchor invalidation** — Option A (degraded pad remains valid anchor) vs. Option B (pad below threshold invalidates anchor with fallback chain).

- **[Carried from Q14–Q19] Standing re-check at respawn time vs. docking write time.**

- **[Carried from Q13–Q19] Tier regression rebuild cost mechanism** — resource quantity, time, or step-count reduction, and named config constant.

- **[Carried from Q13–Q19] Which in-world surface carries the rebuild gate explanation** — comms intercept string or Bar cold dialogue at moment of regression.

- **[Carried from Q13–Q19] Scaffolding third geometry state asset estimate** — per-building-type day count required; floor is 2–4 days per type.

- **[Carried from Q12–Q19] Defense emplacement milestone placement** — blocking for any scope estimate including the emplacement.

- **[Carried from Q12–Q19] Power-emplacement dependency raid AI design** — query path architecture for rational targeting unspecified.

- **[Carried from Q12–Q19] Power node degraded state visual signal** — what communicates "systems affected" at 500 meters in flat-poly; must resolve before degraded model is built.

- **[Carried from Q12–Q19] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value** — deferred pending M7 building type count and structural damage accumulation rates.

- **[Carried from Q12–Q19] Building type count at Settlement, Colony, and City tiers** — required for M8 visual regression asset estimate; Outpost floor confirmed at three.

- **[Carried from Q12–Q19] Tier regression milestone placement** — stat-only regression could ship earlier; geometry regression requires asset pass acknowledgment first.

- **[Carried from Q11–Q19] Assault-scale split-vector spawn bearing offsets for M7 solo** — two approach bearings must be named config constants.

- **[Carried from Q11–Q19] First-raid protection window co-op edge case** — whether `player_has_had_clean_atmospheric_view` requires both players or only the triggering player.

- **[Carried from Q3–Q19] Per-faction rivalry heat values** — config architecture must support per-faction overrides from day one; no authored values for any milestone.

- **[Carried from Q3–Q19] Defection multiplier post-commitment** — whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after commitment NPC trigger; deferred, applies post-commitment only.

- **[Carried from Q5–Q19] Hostile floor numeric value** — named config constant required; value deferred pending M5 playtest data.

- **[Carried from Q5–Q19] Authored Hostile recovery trigger form** — intermediary NPC, specific mission string, or faction-unique narrative unlock.

- **[Carried from Q5–Q19] Mission pool sparsity definition in Degraded band** — probability filter, reduced count, or mission type subset.

- **[Carried from Q3–Q19] Commitment NPC dialogue content and content system** — exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables not yet designed.

- **[Carried from Q3–Q19] Standing floor behavior post-commitment** — whether standing can fall below a threshold with an allied faction after commitment.

- **[Carried from Q3–Q19] Standing tooltip direction** — whether tooltip fires at crossing 40 in both directions or only upward; threshold decided, directional trigger open.

- **[Carried from Q4–Q19] Joint action delta magnitude for co-op** — full or fractional standing consequence per participating player; must resolve before M8 mission resolution code ships.

- **[Carried from Q4–Q19] Standing change cause attribution for co-op** — notification surface for attributing triggering action and player role; deferred to M8; now coupled to Path A / Path B selection.

- **[Carried from Q3–Q19] Contested airspace spawn geometry** — two-spawn-axis design for opposing faction intercepts in split-commitment co-op settlement; deferred to M8.

- **[Carried from Q6–Q19] Passive decay milestone** — at which milestone refusal-tracking decay earns scope; requires M5 event-only playtest data.

- **[Carried from Q6–Q19] Refusal-tracking attribution rule** — distinguishing deliberate decline from absence from never having reached a faction Bar.

- **[Carried from Q6–Q19] `DECAY_FLOOR` numeric value** — named config constant required, set above `HOSTILE_THRESHOLD`; value deferred pending M5 playtest data.

- **[Carried from Q9–Q19] Hull capture standing delta magnitude per faction** — named config constants required; numeric values deferred pending M5 playtest data.

- **[Carried from Q9–Q19] Relative magnitude of hull capture versus mission failure standing consequence** — unspecified.

- **[Carried from Q10–Q19] Comms intercept string content per faction** — one line per faction contact; exact wording is content design out of scope.

- **[Carried from Q10–Q19] Patrol vector modifier numeric values** — spawn timing offset and approach angle adjustment must be named config constants; values deferred pending M5 playtesting.

- **[Carried from Q9–Q19] Bribe path design** — fully deferred pending Bar rumor/informant surface and deferred-state store for hull provenance.

- **[Carried from Q9–Q19] Salvage flag path design** — fully deferred pending faction-specific grievance tracking.

- **[Carried from Q7–Q19] M6 scope capacity** — full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7.

- **[Carried from Q7–Q19] Build cost of threat-aware hold state** — estimate gates M6 vs. M7 placement.

- **[Carried from Q7–Q19] Escort hold visual treatment** — circular orbit, stationary hover, or trailing vector; UX decision required before M6 ships the layer-transition contract.

- **[Carried from Q8–Q19] Mechanical resolution when a raid spawns during escort hold** — escort engagement rules, destruction possibility, and player surface state unspecified.

- **[Carried from Q7–Q19] Terrain avoidance timing** — deferred alongside full atmospheric escort follow to M8.

- **[Carried from Q11–Q19] `RAID_HARASSMENT_THRESHOLD` numeric value** — named config constant required; value deferred pending M5 playtest data.

- **[Carried from Q11–Q19] `RAID_ASSAULT_THRESHOLD` numeric value** — named config constant required; value deferred pending M5 playtest data.

- **[Carried from Q16–Q19] Registration delta calibration** — whether standing cost at hot-hull registration is large enough to produce readable atmospheric pressure on Shuttle approach; cannot be answered before M5 playtest data; named config constants required from day one.
<!-- complete -->
