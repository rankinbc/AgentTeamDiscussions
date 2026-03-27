# Atmosphere Exit Transition

*Generated: 2026-03-25 17:40 | Question 21 | 231s | Mode: ev18hornet*

## Decisions

**Exit transition is asymmetric.** A symmetric cinematic beat on exit is rejected. Entry and exit are different in kind — entry is gravity-assisted commitment with view transformation, exit is powered climb under hull-specific cost. Treating them identically reads as a loading screen. The asymmetry is a design feature, not a gap to fill.

**Hull-dependent climb rate on exit is correct and low-cost.** If ship stats already govern thrust and hull mass, climb rate variation during atmospheric exit is a tuning variable, not a feature. Heavy Freighter punching out feels different from a Light Fighter. No new systems required. This is a day of polish work contingent on ship stat existence.

**Bank angle cost during exit is a flight model tuning variable.** Not a new mechanic. Belongs in Hornet Layer tuning pass, not in this discussion's scope.

**Re-emergence is positional.** Player emerges on the orbital shell at the position and bearing corresponding to their atmospheric exit vector. A fixed orbital insertion point is rejected. Fixed insertion makes atmosphere a panic button — players learn "dive, come back safe" regardless of what they do underground. Positional re-emergence makes atmosphere a navigation space: evasion through atmosphere requires the player to fly to a useful exit vector, which requires actually flying the atmospheric layer. The evasion question resolves as yes, atmosphere dives work as evasion, but only if the player can execute the exit vector that makes emergence tactically viable.

**The exit vector must be a named canonical value.** The vector is not implicitly whatever direction the player happens to be facing at the altitude threshold. A canonical exit vector must be computed and stored before the layer transition fires — the rule for what constitutes that vector (heading at threshold crossing, average over final N meters of climb, or another formulation) is an implementation decision that must be specified before the coordinate transform is built. This is an open question requiring resolution before positional re-emergence ships.

**Positional re-emergence requires a 3D-to-2D coordinate transform.** Atmospheric exit vector maps to orbital shell position. This is a non-trivial mapping function. The galaxy layer must spawn the player at a computed position rather than a fixed insertion point. Build estimate: 3–5 days including edge case handling. This is not Hornet Layer scope — it is a dependency that must be placed on the milestone where positional re-emergence ships.

**A single comms line on first atmospheric exit confirming emergence bearing is confirmed.** Low build cost, ships regardless of diegetic sky marker scope decision. "Emerged at [bearing]" closes the first loop between exit choice and orbital consequence. This satisfies the tutorial requirement without scripting. Exact wording is content design out of scope.

**Diegetic sky markers for orbital reference are not approved pending asset estimate.** The proposal — sparse flat-poly geometry visible from inside atmosphere during exit climb, communicating the orbital shell and emergence point — is correct design intent and solves Vera's legibility surface requirement and Nadia's first-session mental model problem. It is not approved. Flat-poly advantages do not apply to novel geometry categories being invented from scratch. A per-marker day estimate is required before this earns scope. The estimate floor is unspecified; the group needs a number per marker silhouette type before the work can be evaluated. This is a blocking open question.

**The escort hold point issue is a real dependency, not a deferred concern.** Prior discussions specified escorts hold at atmospheric entry altitude. Positional re-emergence means entry vector and exit vector are potentially different points on the orbital shell. An escort holding at the entry point does not cover a player who exits on a different bearing after a lateral atmospheric transit. This is a correct and interesting design consequence — a straight plunge-and-return is protected, a lateral transit that exits on a different bearing leaves the player unescorted at emergence. The M6 layer-transition contract must be amended to account for entry vector ≠ exit vector before M6 ships. This is not deferred. It is a named dependency against the M6 escort hold decision.

**Patrol spawn anchor points must not be fixed to a single orbital insertion point.** If patrol spawns are anchored to a single insertion point, positional re-emergence loses its tactical consequences — the raid-at-emergence situation that makes the evasion question interesting collapses. This must be confirmed before positional re-emergence ships. It is an open question requiring verification against the patrol spawn implementation.

---

## Open Questions

- **Canonical exit vector computation rule:** What constitutes the exit vector — heading at threshold crossing, average over final N meters of climb, or another formulation? Must be specified before the 3D-to-2D coordinate transform is implemented. Blocks positional re-emergence build.

- **Diegetic sky marker asset estimate:** Per-marker day estimate required for flat-poly orbital reference geometry visible from inside atmosphere during exit climb. No authored count or silhouette type specified. Cannot be approved without that number. Design intent is confirmed; scope is blocked on estimate.

- **Patrol spawn point architecture:** Are patrol spawns anchored to a single orbital insertion point or distributed across the orbital shell? Must be confirmed before positional re-emergence ships. If anchored, positional re-emergence loses tactical teeth and the patrol spawn system requires amendment.

- **Positional re-emergence milestone placement:** The coordinate transform (3–5 day estimate) and the galaxy layer spawn refactor are not Hornet Layer scope. Which milestone carries positional re-emergence as a named build item must be specified.

- **M6 escort hold contract amendment:** Entry vector ≠ exit vector under positional re-emergence. The M6 escort hold behavior must be specified in terms of both vectors — what the escort covers, what it does not cover, and whether the asymmetric coverage is the authored behavior or a gap to address. Required before M6 ships the layer-transition contract.

- **Oblique and corkscrewing exit edge cases:** If a player exits at an oblique angle or loses directional control during climb, what is the canonical exit vector? The computation rule must handle degenerate cases before the transform is built.

- **[Carried from Q20] `ATMOSPHERIC_ENTRY_ALTITUDE` numeric value** — config constant required before Hornet Layer ships; value deferred pending flight model playtest data.

- **[Carried from Q20] `ATMOSPHERIC_FLOOR_ALTITUDE` numeric value** — config constant required before first building mesh is authored; must satisfy `ATMOSPHERIC_FLOOR_ALTITUDE < BUILDING_ROOFLINE_HEIGHT`; value deferred pending building height authoring decisions.

- **[Carried from Q20] `BUILDING_ROOFLINE_HEIGHT` as named constant** — whether single authored constant or per-building-type value; must resolve before pad damage model and collision surfaces are built.

- **[Carried from Q20] Minimum range depth for pacing** — vertical separation producing perceivable descent time at Hornet flight speeds; requires Hornet Layer playtest data.

- **[Carried from Q20] Three feel-state band boundaries** — numeric boundaries deferred to post-Hornet-Layer playtest and M8 faction system integration.

- **[Carried from Q20] LOD transition altitude triggers** — deferred pending terrain complexity decisions and Hornet Layer performance profiling.

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

- **[Carried from Q4–Q19] Standing change cause attribution for co-op** — notification surface for attributing triggering action and player role; deferred to M8; coupled to Path A / Path B selection.

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
