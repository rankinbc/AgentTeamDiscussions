# Starting System Faction and Geography

*Generated: 2026-03-25 18:06 | Question 27 | 262s | Mode: ev18hornet*

## Decisions

- DECIDED: The starting system is Confederation-owned; the player begins with Confederation patrol presence, Confederation Bar contacts, and Confederation missions as the default available content
- DECIDED: Confederation patrol presence in the starting system satisfies Option A of the Q22 galaxy map visibility question — faction ship presence is base-layer on the galaxy map from session one at authoring cost only; no new read path or icon state system is required
- DECIDED: The starting system's Confederation ownership is the structural answer to the Q22 galaxy map blocking question; no separate galaxy map signal architecture decision is needed for the early-game threat legibility problem
- DECIDED: One neutral buffer system separates the starting system from the first contested chokepoint; the player crosses into contested space as a consequential act, not by proximity drift
- DECIDED: Confederation mission availability from session one means the player accumulates Confederation standing — and by the symmetric multiplier, incurs Rebel standing degradation — before the standing system is visible to them
- DECIDED: The legibility contract is tooltip-before-hostile-consequence: a standing tooltip must have fired (crossing 40 in either direction) and at least one faction mission must have been completed before hostile-band behavior is architecturally permitted to manifest against that player in the starting system
- DECIDED: The tooltip-before-consequence contract is a behavioral rule governing the starting system only; once the player crosses into the neutral buffer or the contested chokepoint, normal band thresholds apply regardless of tooltip history
- DECIDED: The starting system's Bar contacts are Confederation-affiliated from session one; this determines the initial commitment NPC unlock trajectory and is not separable from the geography decision
- DECIDED: The first contested chokepoint is the system immediately beyond the neutral buffer (galaxy position three from start); "sessions 2–3" is a pacing description, not an authored gate, and is subject to revision against M5 playtest standing delta data

---

## Open Questions

- OPEN: Total system count in the authored galaxy — Soren's blocking question; a solo dev can author approximately six to eight systems with full faction content (patrol presence, Bar contacts, mission pool, landing pad, faction affiliation, NPC dialogue); the starting system + neutral buffer + contested chokepoint structure accounts for three; remaining system budget must be specified before galaxy topology is final
- OPEN: Whether one contested chokepoint or two serves sessions 2–3; Ren asked this and it was not answered; affects system count and pacing geometry
- OPEN: What happens to Rebel standing during the starting-system phase — whether passive Rebel degradation through Confederation mission completion crosses 40 before the player reaches the neutral buffer, and whether that degradation is legible or silent; if Rebel standing can reach Degraded band before the tooltip fires, the tooltip-before-consequence contract has a gap
- OPEN: How many sessions at expected mission pacing until standing tooltip fires at 40 in either direction — requires M5 playtest data on standing delta rates; "sessions 2–3" for chokepoint arrival is a design assumption, not a measured value; geography may need to be revisited against real pacing once M5 ships
- OPEN: Whether the neutral buffer system has authored Confederation presence, authored Rebel presence, or is genuinely faction-neutral — affects whether standing movement continues in the buffer or pauses, and whether the buffer is a teaching space or a transition
- OPEN: What Rebel standing value the player arrives at the first contested chokepoint with under normal play — requires M5 standing delta data; this determines whether the contested system reads as immediately hostile or as a place where standing continues to move
- OPEN: Whether the "sessions 2–3 chokepoint" timing assumption holds once actual mission pacing, standing delta rates, and Bar contact density are authored; the geography decision is conditional on this assumption and must be confirmed against playtest data before M4 Galaxy Layer scope is locked
- OPEN: [Carried from Q22] First-raid protection window and approach signal interaction — the protection window suppresses damage; whether it modifies approach signal fidelity for pre-first-descent players is unspecified; starting system geography does not resolve this
- OPEN: [Carried Q22] What pulls a new player into the atmospheric layer before they understand why the threat matters — Max's "settlement worth defending" framing addresses this but the galaxy map signal fidelity question (vague threat vs. precise intercept timing requiring atmospheric entry) is not yet specified
- OPEN: [Carried from prior] Canonical exit vector computation rule
- OPEN: [Carried from prior] Diegetic sky marker asset estimate
- OPEN: [Carried from prior] Patrol spawn point architecture — single orbital insertion anchor or distributed across orbital shell
- OPEN: [Carried from prior] Positional re-emergence milestone placement
- OPEN: [Carried from prior] M6 escort hold contract amendment — escort coverage must be specified for both entry and exit vectors before M6 ships the layer-transition contract
- OPEN: [Carried from prior] Oblique and corkscrewing exit edge cases
- OPEN: [Carried from prior] `ATMOSPHERIC_ENTRY_ALTITUDE` numeric value
- OPEN: [Carried from prior] `ATMOSPHERIC_FLOOR_ALTITUDE` numeric value — must satisfy `ATMOSPHERIC_FLOOR_ALTITUDE < BUILDING_ROOFLINE_HEIGHT`
- OPEN: [Carried from prior] `BUILDING_ROOFLINE_HEIGHT` as named constant — single authored constant or per-building-type value
- OPEN: [Carried from prior] Minimum range depth for pacing — requires Hornet Layer playtest data
- OPEN: [Carried from prior] Three feel-state band boundaries — deferred to post-Hornet-Layer playtest and M8 faction system integration
- OPEN: [Carried from prior] LOD transition altitude triggers — deferred pending terrain complexity decisions and Hornet Layer performance profiling
- OPEN: [Carried from prior] Attribution path selection — Path A vs Path B; must resolve before M7 or M8 attribution scope is locked
- OPEN: [Carried from prior] Exact co-op comms intercept string content for `max()` conditions
- OPEN: [Carried from prior] Whether M5 shipped comms intercept infrastructure as decided in Q10 — blocking dependency for M7 and M8 extension estimates
- OPEN: [Carried from prior] Counter scope for `raids_since_last_docking` — per-faction or aggregate
- OPEN: [Carried from prior] `raids_since_last_docking` reset behavior on docking at non-owned neutral faction port
- OPEN: [Carried from prior] Exact string content for counter output at atmospheric entry
- OPEN: [Carried from prior] Pad destruction and anchor invalidation — Option A vs Option B
- OPEN: [Carried from prior] Standing re-check at respawn time vs docking write time
- OPEN: [Carried from prior] Tier regression rebuild cost mechanism — resource quantity, time, or step-count reduction, and named config constant
- OPEN: [Carried from prior] Which in-world surface carries the rebuild gate explanation — comms intercept string or Bar cold dialogue at moment of regression
- OPEN: [Carried from prior] Scaffolding third geometry state asset estimate — per-building-type day count required; floor is 2–4 days per type
- OPEN: [Carried from prior] Defense emplacement milestone placement — blocking for any scope estimate including the emplacement
- OPEN: [Carried from prior] Power-emplacement dependency raid AI design — query path architecture for rational targeting unspecified
- OPEN: [Carried from prior] Power node degraded state visual signal — what communicates "systems affected" at 500 meters in flat-poly
- OPEN: [Carried from prior] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value — deferred pending M7 building type count and structural damage accumulation rates
- OPEN: [Carried from prior] Building type count at Settlement, Colony, and City tiers — required for M8 visual regression asset estimate; Outpost floor confirmed at three
- OPEN: [Carried from prior] Tier regression milestone placement — stat-only regression could ship earlier; geometry regression requires asset pass acknowledgment first
- OPEN: [Carried from prior] Assault-scale split-vector spawn bearing offsets for M7 solo — two approach bearings must be named config constants
- OPEN: [Carried from prior] First-raid protection window co-op edge case — whether `player_has_had_clean_atmospheric_view` requires both players or only the triggering player
- OPEN: [Carried from prior] Per-faction rivalry heat values — config architecture must support per-faction overrides from day one; no authored values for any milestone
- OPEN: [Carried from prior] Defection multiplier post-commitment — whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after commitment NPC trigger; deferred, applies post-commitment only
- OPEN: [Carried from prior] Hostile floor numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried from prior] Authored Hostile recovery trigger form — intermediary NPC, specific mission string, or faction-unique narrative unlock
- OPEN: [Carried from prior] Mission pool sparsity definition in Degraded band — probability filter, reduced count, or mission type subset
- OPEN: [Carried from prior] Commitment NPC dialogue content and content system — exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables not yet designed
- OPEN: [Carried from prior] Standing floor behavior post-commitment — whether standing can fall below a threshold with an allied faction after commitment
- OPEN: [Carried from prior] Standing tooltip direction — whether tooltip fires at crossing 40 in both directions or only upward; threshold decided, directional trigger open
- OPEN: [Carried from prior] Joint action delta magnitude for co-op — full or fractional standing consequence per participating player; must resolve before M8 mission resolution code ships
- OPEN: [Carried from prior] Standing change cause attribution for co-op — notification surface for attributing triggering action and player role; deferred to M8; coupled to Path A / Path B selection
- OPEN: [Carried from prior] Contested airspace spawn geometry — two-spawn-axis design for opposing faction intercepts in split-commitment co-op settlement; deferred to M8
- OPEN: [Carried from prior] Passive decay milestone — at which milestone refusal-tracking decay earns scope; requires M5 event-only playtest data
- OPEN: [Carried from prior] Refusal-tracking attribution rule — distinguishing deliberate decline from absence from never having reached a faction Bar
- OPEN: [Carried from prior] `DECAY_FLOOR` numeric value — named config constant required, set above `HOSTILE_THRESHOLD`; value deferred pending M5 playtest data
- OPEN: [Carried from prior] Hull capture standing delta magnitude per faction — named config constants required; numeric values deferred pending M5 playtest data
- OPEN: [Carried from prior] Relative magnitude of hull capture versus mission failure standing consequence — unspecified
- OPEN: [Carried from prior] Comms intercept string content per faction — one line per faction contact; exact wording is content design out of scope
- OPEN: [Carried from prior] Patrol vector modifier numeric values — spawn timing offset and approach angle adjustment must be named config constants; values deferred pending M5 playtesting
- OPEN: [Carried from prior] Bribe path design — fully deferred pending Bar rumor/informant surface and deferred-state store for hull provenance
- OPEN: [Carried from prior] Salvage flag path design — fully deferred pending faction-specific grievance tracking
- OPEN: [Carried from prior] M6 scope capacity — full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7
- OPEN: [Carried from prior] Build cost of threat-aware hold state — estimate gates M6 vs M7 placement
- OPEN: [Carried from prior] Escort hold visual treatment — circular orbit, stationary hover, or trailing vector; UX decision required before M6 ships the layer-transition contract
- OPEN: [Carried from prior] Mechanical resolution when a raid spawns during escort hold — escort engagement rules, destruction possibility, and player surface state unspecified
- OPEN: [Carried from prior] Terrain avoidance timing — deferred alongside full atmospheric escort follow to M8
- OPEN: [Carried from prior] `RAID_HARASSMENT_THRESHOLD` numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried from prior] `RAID_ASSAULT_THRESHOLD` numeric value — named config constant required; value deferred pending M5 playtest data
- OPEN: [Carried from prior] Registration delta calibration — whether standing cost at hot-hull registration is large enough to produce readable atmospheric pressure on Shuttle approach; cannot be answered before M5 playtest data; named config constants required from day one
- OPEN: [Carried from prior] Patrol-tier audio dependency — whether raid composition tier is readable at breach combat spawn point at M7 build time
- OPEN: [Carried from prior] Exact alarm audio asset — one asset or two (harassment vs. assault); must be authored before M7 ships breach combat surface
- OPEN: [Carried from prior] `HIT_DESATURATION_DURATION` numeric value — named config constant required; value deferred pending M7 breach combat playtest
- OPEN: [Carried from prior] `HIT_DESATURATION_INTENSITY` numeric value — named config constant required; value deferred pending M7 breach combat playtest
- OPEN: [Carried from prior] Damage-state desaturation depth modulation milestone — at which milestone building damage model exposes live state query at render time
- OPEN: [Carried from prior] M7 on-foot combat milestone placement — minimum viable breach combat in M7 or M8
- OPEN: [Carried from prior] Comms line exact wording at breach — one line communicating the aerial alternative that was unavailable
- OPEN: [Carried from prior] Enemy pathfinding scope inside building geometry — full pathfinding versus converging-vector movement toward player position
- OPEN: [Carried from prior] Death/fail state for on-foot breach — connection to Q14/Q15 respawn anchor and Shuttle assignment flow
- OPEN: [Carried from prior] Supply chain integration milestone — when faction-sourced ammo or standing-gated sidearm acquisition earns scope
- OPEN: [Carried from prior] Building interior dimensions for shelter, power node, and storage unit — blocking for `ENEMY_ALERT_RANGE` and `ENEMY_ATTACK_RANGE` authoring
- OPEN: [Carried from prior] Whether interior dimensions vary by tier or use a single authored value per type
- OPEN: [Carried from prior] `ENEMY_ALERT_RANGE` numeric value — deferred pending Outpost interior dimension authoring and playable atmospheric intercept baseline
- OPEN: [Carried from prior] `ENEMY_ATTACK_RANGE` numeric value — deferred pending Outpost interior dimension authoring and playable atmospheric intercept baseline
- OPEN: [Carried from prior] Sidearm effective range numeric value — deferred pending Hornet Layer floor altitude and building geometry authoring; must be specified in relation to `ENEMY_ALERT_RANGE` and building interior depth
<!-- complete -->
