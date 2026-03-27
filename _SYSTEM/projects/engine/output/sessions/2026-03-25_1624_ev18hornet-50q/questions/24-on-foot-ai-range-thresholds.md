# On-Foot AI Range Thresholds

*Generated: 2026-03-25 17:53 | Question 24 | 205s | Mode: ev18hornet*

## Decisions

- DECIDED: `ENEMY_ALERT_RANGE` and `ENEMY_ATTACK_RANGE` are named config constants required from day one; numeric values are deferred pending building interior dimension authoring and at least one playable atmospheric intercept session
- DECIDED: Numeric threshold authoring is blocked until two prerequisites are satisfied: (1) building interior dimensions for all three confirmed Outpost types are specified, and (2) at least one playable atmospheric intercept session provides a baseline comparison
- DECIDED: Alert and attack range thresholds must satisfy a behavioral contract: the breach fight must read demonstrably worse than successful airspace management; this is a behavioral contract, not a tuning preference
- DECIDED: Building interior dimensions are not independent of prior decisions — the 500m silhouette legibility requirement already caps building footprint, and interior dimensions follow from that constraint as a consequence of the committed degraded-state legibility requirement, not as a new authoring question
- DECIDED: Authoring numeric threshold values before the dependency chain is satisfied produces false precision calibrated against the wrong baseline; the same deferral discipline applied to hostile floor, raid thresholds, and standing deltas applies here
- DECIDED: Alert and attack range thresholds are in the same category as other deferred config constants: name now, value after data exists
- DECIDED: The behavioral contract governing threshold authoring is: ammo scarcity, range punishment, and no survival guarantee must produce a fight that reads as a consequence of airspace management failure, not as a viable tactical alternative to aerial intercept; if dirtside defense becomes the optimal play, the atmospheric layer's strategic value is lost
- DECIDED: Static thresholds that ignore settlement tier are a named risk; a threshold that produces desperate close-quarters defense in an Outpost shelter may produce a shooting gallery in a Colony corridor as building scale increases across tiers; threshold scaling relative to building geometry must be considered at authoring time
- DECIDED: Alert range relative to chokepoints determines whether the player has a decision before contact; this is a design constraint on threshold authoring, not a tuning variable; chokepoint positions cannot be specified until building interior dimensions are authored
- DECIDED: The first breach encounter is a teaching moment; a player who is breached before experiencing a clean atmospheric intercept receives the wrong lesson; threshold authoring must account for the pre-intercept new-player state as distinct from the post-intercept experienced-player state

## Open Questions

- OPEN: Building interior dimensions for the three confirmed Outpost types — shelter, power node, and storage unit — are the immediate blocking question for all threshold authoring; dimensions are not yet specified and are required before `ENEMY_ALERT_RANGE` and `ENEMY_ATTACK_RANGE` can receive defensible values
- OPEN: Whether a single authored interior dimension per building type is sufficient, or whether interior dimensions vary by tier as building scale increases from Outpost through Colony and City; if thresholds must scale with geometry, the relationship between building scale and threshold values must be authored as a rule, not a per-tier constant
- OPEN: `ENEMY_ALERT_RANGE` numeric value — named config constant required; value deferred pending Outpost interior dimension authoring and playable atmospheric intercept baseline data
- OPEN: `ENEMY_ATTACK_RANGE` numeric value — named config constant required; value deferred pending Outpost interior dimension authoring and playable atmospheric intercept baseline data
- OPEN: Sidearm effective range numeric value — named config constant required from day one per Q23 decisions; value deferred pending Hornet Layer floor altitude and building geometry authoring; must be specified in relation to `ENEMY_ALERT_RANGE` and building interior depth to ensure the player has a weapon response window after alert fires
- OPEN: M7 on-foot combat milestone placement — is minimum viable breach combat a named M7 build item or does it belong in M8? Requires explicit acknowledgment that 3–5 weeks of new system work fits M7 capacity before threshold authoring has a target milestone
- OPEN: Enemy pathfinding scope inside building geometry — full pathfinding versus converging-vector movement toward player position; must resolve before AI build begins and before alert range is meaningful (alert range at which converging-vector enemies are triggered is a different number from alert range at which pathfinding enemies are triggered)
- OPEN: Death/fail state for on-foot breach — whether this connects to the Q14/Q15 respawn anchor and Shuttle assignment flow or resolves separately; must resolve before breach combat implementation begins
- OPEN: Comms line exact wording at breach — one line communicating the aerial alternative that was unavailable; exact wording is content design out of scope; must be authored before M7 ships the breach combat surface
- OPEN: Supply chain integration milestone — at which milestone faction-sourced ammo or standing-gated sidearm acquisition earns scope; requires M5 event-only playtest data confirming authored equipment does not make dirtside defense dominant
- OPEN: [Carried from Q22] Galaxy map threat visibility option — Option A (repurposable at authoring cost), Option B (requires read path and icon state), or Option C (new system); blocking question for all signal architecture
- OPEN: [Carried from Q22] Galaxy map build cost per option
- OPEN: [Carried from Q22] Minimum galaxy-layer signal that creates urgency without enabling spectator behavior
- OPEN: [Carried from Q22] Whether approach time precision should require atmospheric entry to resolve
- OPEN: [Carried from Q22] First-raid protection window and approach signal interaction
- OPEN: [Carried from Q22] What pulls a new player into the atmospheric layer before they understand why the threat matters
- OPEN: [Carried from Q21] Canonical exit vector computation rule — heading at threshold crossing, average over final N meters, or other formulation
- OPEN: [Carried from Q21] Diegetic sky marker asset estimate — per-marker day count for flat-poly orbital reference geometry
- OPEN: [Carried from Q21] Patrol spawn point architecture — single orbital insertion anchor or distributed across orbital shell
- OPEN: [Carried from Q21] Positional re-emergence milestone placement
- OPEN: [Carried from Q21] M6 escort hold contract amendment — escort coverage must be specified for both entry and exit vectors before M6 ships the layer-transition contract
- OPEN: [Carried from Q21] Oblique and corkscrewing exit edge cases
- OPEN: [Carried from Q20] `ATMOSPHERIC_ENTRY_ALTITUDE` numeric value
- OPEN: [Carried from Q20] `ATMOSPHERIC_FLOOR_ALTITUDE` numeric value — must satisfy `ATMOSPHERIC_FLOOR_ALTITUDE < BUILDING_ROOFLINE_HEIGHT`
- OPEN: [Carried from Q20] `BUILDING_ROOFLINE_HEIGHT` as named constant — single authored constant or per-building-type value
- OPEN: [Carried from Q20] Minimum range depth for pacing — requires Hornet Layer playtest data
- OPEN: [Carried from Q20] Three feel-state band boundaries — deferred to post-Hornet-Layer playtest and M8 faction system integration
- OPEN: [Carried from Q20] LOD transition altitude triggers — deferred pending terrain complexity decisions and Hornet Layer performance profiling
- OPEN: [Carried from Q19] Attribution path selection — Path A (content change, one conditional branch) vs Path B (new cross-player standing comparison surface); must resolve before M7 or M8 attribution scope is locked
- OPEN: [Carried from Q19] Exact co-op comms intercept string content for `max()` conditions
- OPEN: [Carried from Q17–Q19] Whether M5 shipped comms intercept infrastructure as decided in Q10 — blocking dependency for M7 and M8 extension estimates
- OPEN: [Carried from Q17–Q19] Counter scope for `raids_since_last_docking` — per-faction or aggregate
- OPEN: [Carried from Q17–Q19] `raids_since_last_docking` reset behavior on docking at non-owned neutral faction port
- OPEN: [Carried from Q17–Q19] Exact string content for counter output at atmospheric entry
- OPEN: [Carried from Q14–Q19] Pad destruction and anchor invalidation — Option A (degraded pad remains valid anchor) vs Option B (pad below threshold invalidates anchor with fallback chain)
- OPEN: [Carried from Q14–Q19] Standing re-check at respawn time vs docking write time
- OPEN: [Carried from Q13–Q19] Tier regression rebuild cost mechanism — resource quantity, time, or step-count reduction, and named config constant
- OPEN: [Carried from Q13–Q19] Which in-world surface carries the rebuild gate explanation — comms intercept string or Bar cold dialogue at moment of regression
- OPEN: [Carried from Q13–Q19] Scaffolding third geometry state asset estimate — per-building-type day count required; floor is 2–4 days per type
- OPEN: [Carried from Q12–Q19] Defense emplacement milestone placement — blocking for any scope estimate including the emplacement
- OPEN: [Carried from Q12–Q19] Power-emplacement dependency raid AI design — query path architecture for rational targeting unspecified
- OPEN: [Carried from Q12–Q19] Power node degraded state visual signal — what communicates "systems affected" at 500 meters in flat-poly; must resolve before degraded model is built
- OPEN: [Carried from Q12–Q19] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value — deferred pending M7 building type count and structural damage accumulation rates
- OPEN: [Carried from Q12–Q19] Building type count at Settlement, Colony, and City tiers — required for M8 visual regression asset estimate; Outpost floor confirmed at three
- OPEN: [Carried from Q12–Q19] Tier regression milestone placement — stat-only regression could ship earlier; geometry regression requires asset pass acknowledgment first
- OPEN: [Carried from Q11–Q19] Assault-scale split-vector spawn bearing offsets for M7 solo — two approach bearings must be named config constants
- OPEN: [Carried from Q11–Q19] First-raid protection window co-op edge case — whether `player_has_had_clean_atmospheric_view` requires both players or only the triggering player
- OPEN: [Carried from Q3–Q22] Per-faction rivalry heat values — config architecture must support per-faction overrides from day one; no authored values for any milestone
- OPEN: [Carried from Q3–Q22] Defection multiplier post-commitment — whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after commitment NPC trigger; deferred, applies post-commitment only
- OPEN: [Carried from Q5–Q22] Hostile floor numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried from Q5–Q22] Authored Hostile recovery trigger form — intermediary NPC, specific mission string, or faction-unique narrative unlock
- OPEN: [Carried from Q5–Q22] Mission pool sparsity definition in Degraded band — probability filter, reduced count, or mission type subset
- OPEN: [Carried from Q3–Q22] Commitment NPC dialogue content and content system — exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables not yet designed
- OPEN: [Carried from Q3–Q22] Standing floor behavior post-commitment — whether standing can fall below a threshold with an allied faction after commitment
- OPEN: [Carried from Q3–Q22] Standing tooltip direction — whether tooltip fires at crossing 40 in both directions or only upward; threshold decided, directional trigger open
- OPEN: [Carried from Q4–Q22] Joint action delta magnitude for co-op — full or fractional standing consequence per participating player; must resolve before M8 mission resolution code ships
- OPEN: [Carried from Q4–Q22] Standing change cause attribution for co-op — notification surface for attributing triggering action and player role; deferred to M8; coupled to Path A / Path B selection
- OPEN: [Carried from Q3–Q22] Contested airspace spawn geometry — two-spawn-axis design for opposing faction intercepts in split-commitment co-op settlement; deferred to M8
- OPEN: [Carried from Q6–Q22] Passive decay milestone — at which milestone refusal-tracking decay earns scope; requires M5 event-only playtest data
- OPEN: [Carried from Q6–Q22] Refusal-tracking attribution rule — distinguishing deliberate decline from absence from never having reached a faction Bar
- OPEN: [Carried from Q6–Q22] `DECAY_FLOOR` numeric value — named config constant required, set above `HOSTILE_THRESHOLD`; value deferred pending M5 playtest data
- OPEN: [Carried from Q9–Q22] Hull capture standing delta magnitude per faction — named config constants required; numeric values deferred pending M5 playtest data
- OPEN: [Carried from Q9–Q22] Relative magnitude of hull capture versus mission failure standing consequence — unspecified
- OPEN: [Carried from Q10–Q22] Comms intercept string content per faction — one line per faction contact; exact wording is content design out of scope
- OPEN: [Carried from Q10–Q22] Patrol vector modifier numeric values — spawn timing offset and approach angle adjustment must be named config constants; values deferred pending M5 playtesting
- OPEN: [Carried from Q9–Q22] Bribe path design — fully deferred pending Bar rumor/informant surface and deferred-state store for hull provenance
- OPEN: [Carried from Q9–Q22] Salvage flag path design — fully deferred pending faction-specific grievance tracking
- OPEN: [Carried from Q7–Q22] M6 scope capacity — full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7
- OPEN: [Carried from Q7–Q22] Build cost of threat-aware hold state — estimate gates M6 vs M7 placement
- OPEN: [Carried from Q7–Q22] Escort hold visual treatment — circular orbit, stationary hover, or trailing vector; UX decision required before M6 ships the layer-transition contract
- OPEN: [Carried from Q8–Q22] Mechanical resolution when a raid spawns during escort hold — escort engagement rules, destruction possibility, and player surface state unspecified
- OPEN: [Carried from Q7–Q22] Terrain avoidance timing — deferred alongside full atmospheric escort follow to M8
- OPEN: [Carried from Q11–Q22] `RAID_HARASSMENT_THRESHOLD` numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried from Q11–Q22] `RAID_ASSAULT_THRESHOLD` numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried from Q16–Q22] Registration delta calibration — whether standing cost at hot-hull registration is large enough to produce readable atmospheric pressure on Shuttle approach; cannot be answered before M5 playtest data; named config constants required from day one
<!-- complete -->
