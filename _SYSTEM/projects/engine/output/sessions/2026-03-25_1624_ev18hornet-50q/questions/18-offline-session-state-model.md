# Offline Session State Model

*Generated: 2026-03-25 17:28 | Question 18 | 213s | Mode: ev18hornet*

## Decisions

**Canonical offline session state is last committed save.** When both host and client go offline simultaneously, the session state is the last successfully committed save. There is no elapsed-time reconstruction of what would have occurred between sessions.

**Elapsed-time reconstruction is explicitly rejected.** A faithful offline simulator requires tick-accurate standing tracking, timestamped event queues, and a replay engine. This is not a design tradeoff — it is a project-ending scope item. It is not revisited at any milestone.

**Offline raid outcomes resolve at reconnect time, not during the offline interval.** When a player session reconnects, the system calculates how many raids occurred during the offline period and resolves their outcomes sequentially at that point. No raid outcome is committed to the save while no session is active.

**Resolution is sequential.** Each offline raid's composition is calculated from the standing value *after* the previous raid's consequence has been applied. Raid two compounds onto the standing damage from raid one. A player who was already in Hostile band at the first offline raid faces compounding assault-scale composition through subsequent raids. The feedback loop is preserved: the system creates the situation, it is not authored.

**This model is consistent with the prior decision that raid composition reads standing at spawn time.** "Spawn time" for an offline raid is its position in the sequential reconnect-time resolution pass, not a reconstructed timestamp from the offline interval. The standing value at each step in the sequence is the operative value.

**The discrete resolution model is the correct inheritance from EV design heritage.** EV never simulated continuity between sessions. Patrol spawns, mission availability, and faction behavior all resolved at discrete interaction points — system entry, landing, departure. Offline raid resolution follows the same pattern. Legibility comes from discrete resolution, not continuity.

**In co-op, when both players are offline simultaneously, raid composition resolves against the higher-threat standing value per raid.** When two players are offline and their standing values differ, each raid in the sequential resolution pass uses `max()` across the two players' current standing values to determine composition. The player in the worse standing position drives the composition at each step. This produces one authoritative composition per raid event, resolved against a single standing reference, sequentially compounding through the offline raid sequence.

**No new data fields are required to implement the co-op higher-threat rule.** The rule resolves to a `max()` call on two per-player standing values already present in the data model. No attribution field, no intermediate aggregation layer, no new event surface.

**The comms intercept at atmospheric entry names raid count but does not attribute fault to a specific player in co-op for M7.** The `raids_since_last_docking` counter and its associated string communicate slope — how many raids occurred since last docking. They do not name which player's standing position drove composition. Attribution is not part of the M7 surface.

---

## Open Questions

- **Whether the comms intercept string needs to attribute fault to a named player in co-op:** If yes, this belongs on the M8 standing change cause attribution work already open from Q4. If no, the higher-threat rule and the existing comms intercept string ship in M7 with no additional surface. This resolution is required before M8 builds the reconnect path.

- **[Carried from Q17] Whether M5 shipped the comms intercept infrastructure as decided in Q10:** Blocking dependency for the M7 reconnect-time extension estimate. If the comms intercept pattern slipped in M5, M7 work expands to include the full atmospheric entry emission surface.

- **[Carried from Q17] Counter scope — per-faction or aggregate for `raids_since_last_docking`:** Does the counter track all raid spawns regardless of faction origin, or maintain a per-faction count? Per-faction aligns with the per-player per-faction standing architecture but adds field count. Aggregate is simpler. Resolution required before M7 implementation begins.

- **[Carried from Q17] `raids_since_last_docking` reset behavior on non-owned faction port docking:** Whether docking at a neutral faction port resets the counter. If the player docks at a faction port between sessions, the settlement's offline situation has not been observed. Must be specified before M7 builds the docking write.

- **[Carried from Q17] Exact string content for the counter output at atmospheric entry:** One line per comms intercept event, formatted around the counter value. Content design out of scope for this discussion. Must be authored before M7 ships the comms intercept extension.

- **[Carried from Q17] Pad destruction and anchor invalidation:** Option A (degraded pad remains valid anchor) vs. Option B (pad below damage threshold invalidates anchor with fallback chain). The `raids_since_last_docking` reset condition is coupled to whichever option ships — a failed dock at an invalidated pad is not a valid docking event.

- **[Carried from Q17] Standing re-check at respawn time vs. docking write time:** Simpler rule (anchor set at docking, not re-evaluated) vs. stricter rule (re-check at respawn, fallback if standing degraded). Counter reset shares the docking write event — if the write rule changes, the reset rule changes.

- **[Carried from Q13] Tier regression rebuild cost mechanism:** What specific form — resource quantity reduction, time reduction, or step-count reduction — and what named config constant governs it.

- **[Carried from Q13] Which in-world surface carries the rebuild gate explanation:** Comms intercept string or Bar cold dialogue at the moment of regression.

- **[Carried from Q13] Scaffolding third geometry state asset estimate:** Per-building-type day count required; estimate floor is 2–4 days per type. Cannot be approved without that number.

- **[Carried from Q12] Defense emplacement milestone placement:** Blocking for any scope estimate including the emplacement.

- **[Carried from Q12] Power-emplacement dependency raid AI design:** Query path architecture for rational targeting unspecified.

- **[Carried from Q12] Power node degraded state visual signal:** What communicates "systems affected" at 500 meters in flat-poly. Must resolve before the degraded model is built.

- **[Carried from Q12] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value:** Named config constant required; value deferred pending M7 building type count and structural damage accumulation rates.

- **[Carried from Q12] Building type count at Settlement, Colony, and City tiers:** Required for M8 visual regression asset estimate. Outpost floor confirmed at three; remaining tiers unspecified.

- **[Carried from Q12] Tier regression milestone placement:** Stat-only regression could ship earlier; geometry regression requires asset pass acknowledgment first.

- **[Carried from Q11] Assault-scale split-vector spawn bearing offsets for M7 solo:** Two approach bearings must be named config constants.

- **[Carried from Q11] First-raid protection window co-op edge case:** Whether `player_has_had_clean_atmospheric_view` requires both players or only the triggering player to have completed an unobstructed descent.

- **[Carried from Q3–Q13] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for any milestone.

- **[Carried from Q3–Q13] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after a player triggers the commitment NPC and acts for the opposing faction. Deferred; applies post-commitment only.

- **[Carried from Q5–Q13] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending M5 playtest data.

- **[Carried from Q5–Q13] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Deferred pending playtest data on Hostile band frequency.

- **[Carried from Q5–Q13] Mission pool sparsity definition in Degraded band:** Probability filter, reduced count, or mission type subset. Implementation rule not yet specified.

- **[Carried from Q3–Q13] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables into NPC dialogue not yet designed.

- **[Carried from Q3–Q13] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

- **[Carried from Q3–Q13] Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions or only upward. Threshold of 40 decided; directional trigger open.

- **[Carried from Q4–Q13] Joint action delta magnitude for co-op:** Full or fractional standing consequence per participating player. Must resolve before M8 mission resolution code ships.

- **[Carried from Q4–Q13] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8.

- **[Carried from Q3–Q13] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Deferred to M8.

- **[Carried from Q6–Q13] Passive decay milestone:** At which milestone, if any, does refusal-tracking decay earn scope. Requires M5 event-only playtest data.

- **[Carried from Q6–Q13] Refusal-tracking attribution rule:** How to distinguish deliberate decline from player absence from never having reached a faction Bar. Unresolved.

- **[Carried from Q6–Q13] `DECAY_FLOOR` numeric value:** Named config constant required, set above `HOSTILE_THRESHOLD`. Value deferred pending M5 playtest data.

- **[Carried from Q9–Q13] Hull capture standing delta magnitude per faction:** Named config constants required; numeric values deferred pending M5 playtest data.

- **[Carried from Q9–Q13] Relative magnitude of hull capture versus mission failure standing consequence:** Unspecified.

- **[Carried from Q10–Q13] Comms intercept string content per faction:** One line per faction contact; exact wording is content design out of scope.

- **[Carried from Q10–Q13] Patrol vector modifier numeric values:** Spawn timing offset and approach angle adjustment must be named config constants; values deferred pending M5 playtesting.

- **[Carried from Q9–Q13] Bribe path design:** Fully deferred pending Bar rumor/informant surface and deferred-state store for hull provenance.

- **[Carried from Q9–Q13] Salvage flag path design:** Fully deferred pending faction-specific grievance tracking.

- **[Carried from Q7–Q13] M6 scope capacity:** Full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7.

- **[Carried from Q7–Q13] Build cost of threat-aware hold state:** Estimate gates M6 vs. M7 placement.

- **[Carried from Q7–Q13] Escort hold visual treatment:** Circular orbit, stationary hover, or trailing vector. UX decision required before M6 ships the layer-transition contract.

- **[Carried from Q8–Q13] Mechanical resolution when a raid spawns during escort hold:** Escort engagement rules, destruction possibility, and player surface state unspecified.

- **[Carried from Q7–Q13] Terrain avoidance timing:** Deferred alongside full atmospheric escort follow to M8.

- **[Carried from Q11–Q13] `RAID_HARASSMENT_THRESHOLD` numeric value:** Named config constant required; value deferred pending M5 playtest data.

- **[Carried from Q11–Q13] `RAID_ASSAULT_THRESHOLD` numeric value:** Named config constant required; value deferred pending M5 playtest data.

- **[Carried from Q16] Registration delta calibration:** Is the standing cost at hot-hull registration large enough to produce readable atmospheric pressure on a subsequent Shuttle approach? Cannot be answered before M5 playtest data. Named config constants required from day one; numeric values deferred.
<!-- complete -->
