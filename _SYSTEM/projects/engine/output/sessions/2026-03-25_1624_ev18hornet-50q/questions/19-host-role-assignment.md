# Host Role Assignment

*Generated: 2026-03-25 17:31 | Question 19 | 211s | Mode: ev18hornet*

## Decisions

**Host role is network topology only.** The host designation governs session connectivity and save authority. It has no effect on faction standing reads, raid spawn logic, patrol density calculations, or any other standing-consequential system. A player's faction standing is not privileged, discounted, or overridden based on whether they are the session host or client. This is permanent and not revisited at any milestone.

**Host role is session-negotiable with no standing implications.** Either player may host without affecting the faction pressure each player accumulates or the airspace conditions above their shared settlement. Routing session setup to avoid standing consequences is not possible under this architecture.

**All shared events query both players' standing independently.** No shared event — raid spawn, patrol density calculation, atmospheric intercept geometry, escort hold-state threat evaluation — collapses to a single privileged standing read. The faction system has no concept of host standing. Every standing-consequential calculation in a co-op session receives two per-player standing reads.

**The `max()` operator governs shared event resolution for hostile pressure.** When a shared event requires a single standing reference to resolve — raid composition selection, patrol density band, atmospheric intercept vector geometry — the system uses the higher-threat (worse) standing value across the two players. The player in the more hostile faction relationship drives the composition. This is consistent with the offline co-op raid resolution rule established in Q18 and requires no new data fields.

**`max()` produces correct emergence.** If P1 has degraded Confederation standing through boarding actions while P2 maintained positive standing through trade, the airspace above their shared settlement reflects P1's choices. This is intentional: the settlement's airspace reads like the game that was actually played. The SimCopter payoff moment — flying over what you built — includes flying through the faction pressure your shared history created.

**Escort hire is not a shared event.** Bar interactions are single-player and dirtside. The hiring player's standing gates escort availability with no aggregation. The co-op complexity enters later: when an escort holds at atmospheric entry altitude and a raid spawns during the hold, raid composition uses `max()` across both players' standing. The escort's threat-aware hold state reads both players' faction values before evaluating whether to break hold.

**The standing change cause attribution surface is load-bearing for co-op legibility under `max()`.** Because the more hostile player's standing drives shared airspace conditions, the less hostile player experiences faction pressure without a causal read path. The comms intercept string from Q10 — one line per faction at atmospheric entry — is not sufficient to explain to P2 why the airspace is hostile when P2 did not cause it. Attribution is not optional post-M8; it is the mechanism that makes emergent pressure legible to the player who did not earn it.

**Two implementation paths exist for the attribution surface and must be distinguished before scope is assigned.**

- **Path A — Content change.** The existing Q10 comms intercept string is authored differently for co-op sessions. Same emission surface, same trigger, different wording that includes a partner-reference when session type is co-op. This is a content design problem, not a code problem. The string formatter requires one conditional branch on session type. Build cost: approximately one day of code work; string content is authored separately and out of scope for this discussion.

- **Path B — New read surface.** The system compares both players' standing at comms intercept time, identifies which player drove `max()`, and names that player in the string. This requires real-time cross-player standing comparison at atmospheric entry, a new data path, and a UI surface. This path has co-op session state dependencies that do not exist in M7.

Path A ships with co-op if co-op ships in M8. Path B competes with queued M8 work and requires scoping against committed M8 capacity. The path must be named before scope is assigned.

---

## Open Questions

**[NEW, Q19] Attribution path selection — Path A or Path B:** Is the co-op attribution surface a content change to the existing comms intercept string (Path A: one conditional branch, authored co-op string variant) or a new cross-player standing comparison surface that identifies the `max()` driver by name (Path B: new data path, new UI surface, co-op session state dependencies)? This must be answered before M7 or M8 attribution scope is locked. Path A ships cheaply with co-op; Path B requires a separate scope estimate against M8 capacity.

**[NEW, Q19] Co-op comms intercept string content for `max()` conditions:** What does P2 read at atmospheric entry when P1's standing is driving hostile airspace geometry? The string must provide enough causal information for P2 to identify their partner as the source. "Confederation patrols are active" is insufficient. Exact wording is content design and out of scope for this discussion, but the information requirement — partner-reference at minimum — is a named content constraint that must be authored before co-op ships.

**[Carried from Q18] Whether the comms intercept string needs to attribute fault to a named player in co-op:** Resolution required before M8 builds the reconnect path. This question is now coupled to the Path A / Path B decision above.

**[Carried from Q18] Whether M5 shipped the comms intercept infrastructure as decided in Q10:** Blocking dependency for M7 and M8 extension estimates. If the comms intercept pattern slipped in M5, M7 work expands to include the full atmospheric entry emission surface before any co-op string variant can be added.

**[Carried from Q17] Counter scope — per-faction or aggregate for `raids_since_last_docking`:** Per-faction aligns with the per-player per-faction standing architecture but adds field count. Aggregate is simpler. Resolution required before M7 implementation begins.

**[Carried from Q17] `raids_since_last_docking` reset behavior on non-owned faction port docking:** Whether docking at a neutral faction port resets the counter. Must be specified before M7 builds the docking write.

**[Carried from Q17] Exact string content for the counter output at atmospheric entry:** Must be authored before M7 ships the comms intercept extension.

**[Carried from Q17] Pad destruction and anchor invalidation:** Option A (degraded pad remains valid anchor) vs. Option B (pad below damage threshold invalidates anchor with fallback chain). Coupled to `raids_since_last_docking` reset logic.

**[Carried from Q17] Standing re-check at respawn time vs. docking write time:** Simpler anchor-at-docking rule vs. stricter re-check-at-respawn rule. Must resolve before death-flow implementation.

**[Carried from Q13] Tier regression rebuild cost mechanism:** Resource quantity, time, or step-count reduction, and the named config constant governing it.

**[Carried from Q13] Which in-world surface carries the rebuild gate explanation:** Comms intercept string or Bar cold dialogue at the moment of regression.

**[Carried from Q13] Scaffolding third geometry state asset estimate:** Per-building-type day count required; estimate floor is 2–4 days per type. Cannot be approved without that number.

**[Carried from Q12] Defense emplacement milestone placement:** Blocking for any scope estimate including the emplacement.

**[Carried from Q12] Power-emplacement dependency raid AI design:** Query path architecture for rational targeting unspecified.

**[Carried from Q12] Power node degraded state visual signal:** What communicates "systems affected" at 500 meters in flat-poly. Must resolve before the degraded model is built.

**[Carried from Q12] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value:** Named config constant required; value deferred pending M7 building type count and structural damage accumulation rates.

**[Carried from Q12] Building type count at Settlement, Colony, and City tiers:** Required for M8 visual regression asset estimate. Outpost floor confirmed at three; remaining tiers unspecified.

**[Carried from Q12] Tier regression milestone placement:** Stat-only regression could ship earlier; geometry regression requires asset pass acknowledgment first.

**[Carried from Q11] Assault-scale split-vector spawn bearing offsets for M7 solo:** Two approach bearings must be named config constants.

**[Carried from Q11] First-raid protection window co-op edge case:** Whether `player_has_had_clean_atmospheric_view` requires both players or only the triggering player.

**[Carried from Q3–Q13] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for any milestone.

**[Carried from Q3–Q13] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after a player triggers the commitment NPC and acts for the opposing faction. Deferred; applies post-commitment only.

**[Carried from Q5–Q13] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending M5 playtest data.

**[Carried from Q5–Q13] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Deferred pending playtest data on Hostile band frequency.

**[Carried from Q5–Q13] Mission pool sparsity definition in Degraded band:** Probability filter, reduced count, or mission type subset. Implementation rule not yet specified.

**[Carried from Q3–Q13] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables into NPC dialogue not yet designed.

**[Carried from Q3–Q13] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

**[Carried from Q3–Q13] Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions or only upward. Threshold of 40 decided; directional trigger open.

**[Carried from Q4–Q13] Joint action delta magnitude for co-op:** Full or fractional standing consequence per participating player. Must resolve before M8 mission resolution code ships.

**[Carried from Q4–Q13] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8. Now coupled to Path A / Path B selection.

**[Carried from Q3–Q13] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Deferred to M8.

**[Carried from Q6–Q13] Passive decay milestone:** At which milestone, if any, does refusal-tracking decay earn scope. Requires M5 event-only playtest data.

**[Carried from Q6–Q13] Refusal-tracking attribution rule:** How to distinguish deliberate decline from player absence from never having reached a faction Bar. Unresolved.

**[Carried from Q6–Q13] `DECAY_FLOOR` numeric value:** Named config constant required, set above `HOSTILE_THRESHOLD`. Value deferred pending M5 playtest data.

**[Carried from Q9–Q13] Hull capture standing delta magnitude per faction:** Named config constants required; numeric values deferred pending M5 playtest data.

**[Carried from Q9–Q13] Relative magnitude of hull capture versus mission failure standing consequence:** Unspecified.

**[Carried from Q10–Q13] Comms intercept string content per faction:** One line per faction contact; exact wording is content design out of scope.

**[Carried from Q10–Q13] Patrol vector modifier numeric values:** Spawn timing offset and approach angle adjustment must be named config constants; values deferred pending M5 playtesting.

**[Carried from Q9–Q13] Bribe path design:** Fully deferred pending Bar rumor/informant surface and deferred-state store for hull provenance.

**[Carried from Q9–Q13] Salvage flag path design:** Fully deferred pending faction-specific grievance tracking.

**[Carried from Q7–Q13] M6 scope capacity:** Full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7.

**[Carried from Q7–Q13] Build cost of threat-aware hold state:** Estimate gates M6 vs. M7 placement.

**[Carried from Q7–Q13] Escort hold visual treatment:** Circular orbit, stationary hover, or trailing vector. UX decision required before M6 ships the layer-transition contract.

**[Carried from Q8–Q13] Mechanical resolution when a raid spawns during escort hold:** Escort engagement rules, destruction possibility, and player surface state unspecified.

**[Carried from Q7–Q13] Terrain avoidance timing:** Deferred alongside full atmospheric escort follow to M8.

**[Carried from Q11–Q13] `RAID_HARASSMENT_THRESHOLD` numeric value:** Named config constant required; value deferred pending M5 playtest data.

**[Carried from Q11–Q13] `RAID_ASSAULT_THRESHOLD` numeric value:** Named config constant required; value deferred pending M5 playtest data.

**[Carried from Q16] Registration delta calibration:** Is the standing cost at hot-hull registration large enough to produce readable atmospheric pressure on a subsequent Shuttle approach? Cannot be answered before M5 playtest data. Named config constants required from day one; numeric values deferred.
<!-- complete -->
