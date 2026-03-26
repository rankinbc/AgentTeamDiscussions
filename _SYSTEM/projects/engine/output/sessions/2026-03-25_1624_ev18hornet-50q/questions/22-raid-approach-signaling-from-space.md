# Raid Approach Signaling from Space

*Generated: 2026-03-25 17:44 | Question 22 | 227s | Mode: ev18hornet*

## Decisions

- DECIDED: The approach signal question is a galaxy-layer visibility problem, not a notification design problem; designing a purpose-built approach warning before establishing what the galaxy map currently shows is rejected as designing around the symptom rather than the cause
- DECIDED: The three-layer architecture creates an information gap that did not exist in EV Nova; the galaxy map must be evaluated as the primary signal surface before any substitute system is specified
- DECIDED: Soren's three-option taxonomy is the correct gateway framing: Option A (faction ship presence already visible on galaxy map, repurposable), Option B (presence exists in simulation but not surfaced, requires read path and icon state), Option C (presence not modeled until atmospheric entry, requires new system); the answer determines build cost and gates all signal design below it
- DECIDED: The answer to the galaxy map question must precede any signal architecture specification; approach signal design, pull mechanics, and first-raid teaching moment design are all downstream of that answer
- DECIDED: A purpose-built raid approach notification that resolves entirely in the galaxy layer without requiring atmospheric entry is rejected as authored content substituting for emergent information the standing system should already be communicating
- DECIDED: Max's pull problem is a real design constraint: the approach signal must be designed to invite atmospheric descent, not to enable the player to manage threat anxiety from the galaxy layer as a spectator
- DECIDED: Ren's no-new-system position is correct for players who have had a clean atmospheric descent and have built the mental model; it is not sufficient for players who have not yet descended and cannot interpret the signal
- DECIDED: The first-raid protection window suppresses damage, not the approach signal; new players should be able to see the threat approach and choose to respond before they have experienced loss; this is a behavioral contract, not a tuning question
- DECIDED: The first atmospheric descent is the teaching moment that makes all subsequent approach signals legible; signal design must account for the pre-descent state as distinct from post-descent standing
- DECIDED: Vagueness that rewards descent is a design tool: if precise approach time requires atmospheric entry to resolve, that information gradient is intentional, not a deficiency to correct with a more accurate galaxy-layer display
- DECIDED: Hostile band patrol density as raid warning is an M8 atmospheric texture problem per prior decisions; it is not accessible from the galaxy layer and does not serve as the galaxy-layer approach signal

## Open Questions

- OPEN: Galaxy map threat visibility option — which of Soren's three options applies: (A) faction ship presence already visible on galaxy map as part of base layer, repurposable at authoring cost only; (B) presence exists in simulation but not surfaced on the map, requires read path and icon state; (C) presence not modeled until atmospheric entry, constitutes a new system; this is the blocking question for all signal architecture below it
- OPEN: Galaxy map build cost per option — Option A approximately two days authoring; Option B one to three days depending on data proximity; Option C unknown scope; cost estimate required before any signal design is committed
- OPEN: Minimum galaxy-layer signal that creates urgency without enabling spectator behavior — what information the galaxy map shows, at what fidelity, and whether vagueness below that threshold is authored or incidental
- OPEN: Whether approach time precision should require atmospheric entry to resolve — whether the galaxy map shows "threat approaching" without ETA, and descent is the act that converts vague threat into precise intercept timing
- OPEN: First-raid protection window and approach signal interaction — the protection window suppresses damage; whether it also modifies the fidelity or presentation of the approach signal for pre-first-descent players is unspecified
- OPEN: What pulls a new player into the atmospheric layer before they understand why the threat matters — if the approach signal is legible only to players who have already built the mental model, what invites the first descent without authored scripting
- OPEN: [Carried Q21] Canonical exit vector computation rule — heading at threshold crossing, average over final N meters, or other formulation; blocks 3D-to-2D coordinate transform build
- OPEN: [Carried Q21] Diegetic sky marker asset estimate — per-marker day count for flat-poly orbital reference geometry; cannot be approved without that number
- OPEN: [Carried Q21] Patrol spawn point architecture — single orbital insertion anchor or distributed across orbital shell; must confirm before positional re-emergence ships
- OPEN: [Carried Q21] Positional re-emergence milestone placement — coordinate transform and galaxy layer spawn refactor must be assigned to a named milestone
- OPEN: [Carried Q21] M6 escort hold contract amendment — escort coverage must be specified for both entry and exit vectors before M6 ships the layer-transition contract
- OPEN: [Carried Q21] Oblique and corkscrewing exit edge cases — computation rule must handle degenerate cases before transform is built
- OPEN: [Carried Q20] `ATMOSPHERIC_ENTRY_ALTITUDE` numeric value — config constant required before Hornet Layer ships; value deferred pending flight model playtest data
- OPEN: [Carried Q20] `ATMOSPHERIC_FLOOR_ALTITUDE` numeric value — config constant required before first building mesh is authored; must satisfy `ATMOSPHERIC_FLOOR_ALTITUDE < BUILDING_ROOFLINE_HEIGHT`; value deferred pending building height authoring decisions
- OPEN: [Carried Q20] `BUILDING_ROOFLINE_HEIGHT` as named constant — whether single authored constant or per-building-type value; must resolve before pad damage model and collision surfaces are built
- OPEN: [Carried Q20] Minimum range depth for pacing — vertical separation producing perceivable descent time at Hornet flight speeds; requires Hornet Layer playtest data
- OPEN: [Carried Q20] Three feel-state band boundaries — numeric boundaries deferred to post-Hornet-Layer playtest and M8 faction system integration
- OPEN: [Carried Q20] LOD transition altitude triggers — deferred pending terrain complexity decisions and Hornet Layer performance profiling
- OPEN: [Carried Q19] Attribution path selection — Path A (content change, one conditional branch) vs Path B (new cross-player standing comparison surface naming the `max()` driver); must resolve before M7 or M8 attribution scope is locked
- OPEN: [Carried Q19] Exact co-op comms intercept string content for `max()` conditions — what P2 reads at atmospheric entry when P1's standing is driving hostile airspace geometry
- OPEN: [Carried Q17–Q19] Whether M5 shipped comms intercept infrastructure as decided in Q10 — blocking dependency for M7 and M8 extension estimates
- OPEN: [Carried Q17–Q19] Counter scope for `raids_since_last_docking` — per-faction or aggregate
- OPEN: [Carried Q17–Q19] `raids_since_last_docking` reset behavior on docking at non-owned neutral faction port
- OPEN: [Carried Q17–Q19] Exact string content for counter output at atmospheric entry
- OPEN: [Carried Q14–Q19] Pad destruction and anchor invalidation — Option A (degraded pad remains valid anchor) vs Option B (pad below threshold invalidates anchor with fallback chain)
- OPEN: [Carried Q14–Q19] Standing re-check at respawn time vs docking write time
- OPEN: [Carried Q13–Q19] Tier regression rebuild cost mechanism — resource quantity, time, or step-count reduction, and named config constant
- OPEN: [Carried Q13–Q19] Which in-world surface carries the rebuild gate explanation — comms intercept string or Bar cold dialogue at moment of regression
- OPEN: [Carried Q13–Q19] Scaffolding third geometry state asset estimate — per-building-type day count required; floor is 2–4 days per type
- OPEN: [Carried Q12–Q19] Defense emplacement milestone placement — blocking for any scope estimate including the emplacement
- OPEN: [Carried Q12–Q19] Power-emplacement dependency raid AI design — query path architecture for rational targeting unspecified
- OPEN: [Carried Q12–Q19] Power node degraded state visual signal — what communicates "systems affected" at 500 meters in flat-poly; must resolve before degraded model is built
- OPEN: [Carried Q12–Q19] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value — deferred pending M7 building type count and structural damage accumulation rates
- OPEN: [Carried Q12–Q19] Building type count at Settlement, Colony, and City tiers — required for M8 visual regression asset estimate; Outpost floor confirmed at three
- OPEN: [Carried Q12–Q19] Tier regression milestone placement — stat-only regression could ship earlier; geometry regression requires asset pass acknowledgment first
- OPEN: [Carried Q11–Q19] Assault-scale split-vector spawn bearing offsets for M7 solo — two approach bearings must be named config constants
- OPEN: [Carried Q11–Q19] First-raid protection window co-op edge case — whether `player_has_had_clean_atmospheric_view` requires both players or only the triggering player
- OPEN: [Carried Q3–Q19] Per-faction rivalry heat values — config architecture must support per-faction overrides from day one; no authored values for any milestone
- OPEN: [Carried Q3–Q19] Defection multiplier post-commitment — whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after commitment NPC trigger; deferred, applies post-commitment only
- OPEN: [Carried Q5–Q19] Hostile floor numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried Q5–Q19] Authored Hostile recovery trigger form — intermediary NPC, specific mission string, or faction-unique narrative unlock
- OPEN: [Carried Q5–Q19] Mission pool sparsity definition in Degraded band — probability filter, reduced count, or mission type subset
- OPEN: [Carried Q3–Q19] Commitment NPC dialogue content and content system — exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables not yet designed
- OPEN: [Carried Q3–Q19] Standing floor behavior post-commitment — whether standing can fall below a threshold with an allied faction after commitment
- OPEN: [Carried Q3–Q19] Standing tooltip direction — whether tooltip fires at crossing 40 in both directions or only upward; threshold decided, directional trigger open
- OPEN: [Carried Q4–Q19] Joint action delta magnitude for co-op — full or fractional standing consequence per participating player; must resolve before M8 mission resolution code ships
- OPEN: [Carried Q4–Q19] Standing change cause attribution for co-op — notification surface for attributing triggering action and player role; deferred to M8; coupled to Path A / Path B selection
- OPEN: [Carried Q3–Q19] Contested airspace spawn geometry — two-spawn-axis design for opposing faction intercepts in split-commitment co-op settlement; deferred to M8
- OPEN: [Carried Q6–Q19] Passive decay milestone — at which milestone refusal-tracking decay earns scope; requires M5 event-only playtest data
- OPEN: [Carried Q6–Q19] Refusal-tracking attribution rule — distinguishing deliberate decline from absence from never having reached a faction Bar
- OPEN: [Carried Q6–Q19] `DECAY_FLOOR` numeric value — named config constant required, set above `HOSTILE_THRESHOLD`; value deferred pending M5 playtest data
- OPEN: [Carried Q9–Q19] Hull capture standing delta magnitude per faction — named config constants required; numeric values deferred pending M5 playtest data
- OPEN: [Carried Q9–Q19] Relative magnitude of hull capture versus mission failure standing consequence — unspecified
- OPEN: [Carried Q10–Q19] Comms intercept string content per faction — one line per faction contact; exact wording is content design out of scope
- OPEN: [Carried Q10–Q19] Patrol vector modifier numeric values — spawn timing offset and approach angle adjustment must be named config constants; values deferred pending M5 playtesting
- OPEN: [Carried Q9–Q19] Bribe path design — fully deferred pending Bar rumor/informant surface and deferred-state store for hull provenance
- OPEN: [Carried Q9–Q19] Salvage flag path design — fully deferred pending faction-specific grievance tracking
- OPEN: [Carried Q7–Q19] M6 scope capacity — full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7
- OPEN: [Carried Q7–Q19] Build cost of threat-aware hold state — estimate gates M6 vs M7 placement
- OPEN: [Carried Q7–Q19] Escort hold visual treatment — circular orbit, stationary hover, or trailing vector; UX decision required before M6 ships the layer-transition contract
- OPEN: [Carried Q8–Q19] Mechanical resolution when a raid spawns during escort hold — escort engagement rules, destruction possibility, and player surface state unspecified
- OPEN: [Carried Q7–Q19] Terrain avoidance timing — deferred alongside full atmospheric escort follow to M8
- OPEN: [Carried Q11–Q19] `RAID_HARASSMENT_THRESHOLD` numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried Q11–Q19] `RAID_ASSAULT_THRESHOLD` numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried Q16–Q19] Registration delta calibration — whether standing cost at hot-hull registration is large enough to produce readable atmospheric pressure on Shuttle approach; cannot be answered before M5 playtest data; named config constants required from day one
<!-- complete -->
