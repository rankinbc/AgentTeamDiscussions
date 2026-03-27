# Return Log Milestone

*Generated: 2026-03-25 17:24 | Question 17 | 222s | Mode: ev18hornet*

## Decisions

**The return log as a full system is M8 scope, not M7.** An event timeline, scrollable combat history, UI dashboard, or any surface with "log" as its primary design contract does not ship at M7 Settlement. The data required to populate it correctly — per-faction raid attribution, structural damage sequence, session timestamps — is a co-op legibility problem that earns its full design surface in M8 when the co-op session layer ships.

**The player-legibility gap at first offline raid contact is real and must be addressed in M7.** Three systems already in scope — degraded geometry states, standing tooltip, and the Q10 comms intercept pattern — address different dimensions of consequence legibility. Geometry communicates state (what was hit and what stopped working). Tooltip communicates standing position (current value and what band it implies). Comms intercept communicates causal attribution (which faction's activity explains the damage). None of the three answer the slope question: how far is the player from repair-eligible, and how deep did offline activity cut the standing trajectory. That gap produces the anti-pattern Nadia identifies: a player who runs one escort mission and returns will feel punished for correct play if the standing gap is larger than one mission and no surface communicated that before touchdown.

**The M7 minimum legibility surface is a `raids_since_last_docking` counter plus one formatted string routed through the existing Q10 comms intercept.** This is not a return log. `raids_since_last_docking` is a single integer written at raid spawn time and read at atmospheric layer entry. At layer entry, if the value is nonzero, the comms intercept already firing for faction attribution appends or is joined by one additional string communicating raid count since the player's last docking event. The string gives the player the slope signal before touchdown. The geometry gives them the current state when they arrive. Together they answer the question the standing gate requires the player to be able to ask.

**`raids_since_last_docking` resets on successful docking write.** It uses the same docking-write event as the respawn anchor field decided in Q14. A successful dock — standing ≥ Engaged with the owning faction at landing — writes the anchor and resets the counter to zero. A failed dock attempt (standing insufficient) does not reset the counter.

**This addition must be scoped and specified as an extension of the Q10 comms intercept, not as a new system.** The moment it receives its own spec entry with "log" in the title it will grow. Scope language for M7 planning must read: "extend comms intercept with `raids_since_last_docking` counter." The architectural pattern, the read path at atmospheric entry, and the string emission behavior are already established in Q10. This addition is a counter field and one string substitution on the existing surface.

**The M7 estimate for this extension is conditioned on M5 comms intercept infrastructure shipping as decided.** The Q10 comms intercept pattern — atmospheric entry triggers a faction-attributed string — was decided as M5 scope. If that infrastructure ships in M5, the M7 extension is a counter write, a counter read, and a string format. If M5 slipped the comms intercept, M7 builds surface and content simultaneously and the estimate changes materially. This dependency must be confirmed before M7 scope is locked.

---

## Open Questions

- **Whether M5 ships the comms intercept infrastructure as decided in Q10:** This is a blocking dependency for the M7 extension estimate. If the comms intercept pattern slipped in M5, the M7 work expands from one counter and one string to include the full atmospheric entry emission surface. Must be confirmed before M7 scope is locked.

- **Counter scope — per-faction or aggregate:** Does `raids_since_last_docking` count all raid spawns regardless of faction origin, or does it maintain a per-faction count? Per-faction tracking increases precision and aligns with the per-player per-faction standing architecture, but adds field count. Aggregate is simpler and may be sufficient for the slope signal. Resolution required before implementation begins.

- **`raids_since_last_docking` reset behavior on non-owned pads:** The counter resets on successful docking at a player-owned settlement pad. It was not decided whether docking at a faction port also resets the counter. If the player docks at a neutral faction port between sessions, the counter should arguably not reset — the settlement's offline situation has not been observed. Must be specified before M7 builds the docking write.

- **Exact string content for the counter output at atmospheric entry:** One line per comms intercept event, formatted around the counter value. Exact wording is content design out of scope for this discussion. Must be authored before M7 ships the comms intercept extension.

- **[Carried from Q16] Pad destruction and anchor invalidation:** Option A (degraded pad remains valid anchor) vs. Option B (pad below damage threshold invalidates anchor with fallback chain). The `raids_since_last_docking` reset condition is coupled to whichever option ships — if Option B invalidates the pad as an anchor, a reset at that pad is not a valid docking event. Must resolve before the docking write logic is built.

- **[Carried from Q16] Standing re-check at respawn time vs. docking write time:** Simpler rule (anchor set at docking, not re-evaluated) vs. stricter rule (re-check at respawn, fallback if standing degraded). The counter reset shares the docking write event — if the write rule changes, the reset rule changes.

- **[Carried from Q13] Tier regression rebuild cost mechanism:** What specific form — resource quantity, time, or step-count reduction — and what named config constant governs it.

- **[Carried from Q13] Which in-world surface carries the rebuild gate explanation:** Comms intercept string or Bar cold dialogue at the moment of regression.

- **[Carried from Q13] Scaffolding third geometry state asset estimate:** Per-building-type day count required; estimate floor is 2–4 days per type. Cannot be approved without that number.

- **[Carried from Q12] Defense emplacement milestone placement:** Blocking for any scope estimate including the emplacement.

- **[Carried from Q12] Power-emplacement dependency raid AI design:** Query path architecture for rational targeting unspecified.

- **[Carried from Q12] Power node degraded state visual signal:** What communicates "systems affected" at 500 meters in flat-poly. Must resolve before the degraded model is built.

- **[Carried from Q12] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value:** Deferred pending M7 building type count and structural damage accumulation rates.

- **[Carried from Q12] Building type count at Settlement, Colony, and City tiers:** Required for M8 visual regression asset estimate.

- **[Carried from Q12] Tier regression milestone placement:** Stat-only regression could ship earlier; geometry regression requires asset pass acknowledgment first.

- **[Carried from Q11] Assault-scale split-vector spawn bearing offsets for M7 solo:** Two approach bearings must be named config constants.

- **[Carried from Q11] First-raid protection window co-op edge case:** Whether `player_has_had_clean_atmospheric_view` requires both players or only the triggering player.

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
