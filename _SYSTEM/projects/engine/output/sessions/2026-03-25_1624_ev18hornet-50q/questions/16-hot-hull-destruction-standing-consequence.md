# Hot Hull Destruction Standing Consequence

*Generated: 2026-03-25 17:20 | Question 16 | 207s | Mode: ev18hornet*

## Decisions

**Hull destruction closes the standing account; it does not escalate it.** When the hot hull is destroyed on death, no additional standing delta fires. The owning faction's standing consequence was paid in full at registration. Destruction is an outcome, not a transgressive act — the faction's grievance was the capture and the active use of their asset against them, not the fate of the hull. Resolution of that asset, including destruction, is not a new offense.

**Standing consequences are front-loaded to the moment of transgressive choice, not to downstream resolution.** Every standing movement must be attributable to a player-recognized decision. Registration was the decision point; the player had agency there and could have chosen differently. Death is an outcome with no authorial intent. Firing a standing delta at respawn for a registration decision made sessions earlier severs the causal chain players need to read their own situation. This is a behavioral contract, not a tuning question.

**The atmospheric pressure on the Shuttle approach home derives from the registration delta, not from a destruction trigger.** If the approach back to a settlement after flying a hot hull does not feel charged — if patrol geometry is not readable as consequence — the problem is registration delta magnitude, which is a named config constant already required by prior decisions. Tuning that constant is an afternoon. Building a persistent death-trigger delta with survival semantics through the respawn flow is not.

**Escalation-on-death is explicitly rejected for M5.** The implementation cost is architectural: hull-origin standing would need to persist as a pending second delta from registration through active flight through death through the respawn flow. That state field travels with the hull, survives the hull's destruction, and fires at respawn — which already carries three jobs (hull lost, Shuttle assigned, credit state). Every edge case in the death flow (friendly-fire destruction, logout mid-flight, hull recaptured before death) becomes a case branch. Case branches at the respawn path on a solo build are deferred bug surface, not deferred design space.

**The respawn screen does not carry standing consequence from hull loss.** The respawn screen communicates hull loss, Shuttle assignment, and credit state. No standing change notification appears there for hull origin. Standing was communicated at registration. The respawn screen is not the teaching surface for hot-hull standing consequence.

**Registration delta magnitude is the correct authoring surface for kinesthetic atmospheric feedback.** Patrol geometry, approach vectors, and intercept pressure after flying a captured hull are downstream effects of the standing delta paid at registration. If that delta is insufficiently large to push patrol behavior into a readable state, the fix is in the config constant governing registration cost, which is already a named open question. Hull destruction does not require its own trigger to produce atmospheric legibility.

---

## Open Questions

- **Registration delta calibration:** Is the standing cost at hot-hull registration currently large enough to produce readable atmospheric pressure — modified patrol approach vectors, denser intercept geometry — on a subsequent Shuttle approach to the settlement? This cannot be answered before M5 playtest data on standing movement rates exists. Named config constants required from day one; numeric values deferred.
- **[Carried from Q14] Pad destruction and anchor invalidation:** Option A (degraded pad remains valid anchor) vs. Option B (pad below damage threshold invalidates anchor with fallback chain). Not resolved.
- **[Carried from Q14] Tier regression depth and pad functionality:** How far does tier regression cut pad functionality across Colony→Settlement→Outpost steps? Blocking for Option B scope estimate.
- **[Carried from Q14] Landing on degraded pad and anchor write behavior:** Whether landing on a degraded-but-present pad still writes the last-docked anchor under Option A. Must confirm before M7 builds the pad damage model.
- **[Carried from Q14] Standing re-check at respawn time vs. docking write time:** Simpler rule (anchor set at docking, not re-evaluated) vs. stricter rule (re-check at respawn, fallback if standing degraded). Must resolve before death-flow implementation begins.
- **[Carried from Q13] Tier regression rebuild cost mechanism:** What specific form — resource quantity reduction, time reduction, or step-count reduction — and what named config constant governs it.
- **[Carried from Q13] Which in-world surface carries the rebuild gate explanation:** Comms intercept string or Bar cold dialogue at the moment of regression.
- **[Carried from Q13] Scaffolding third geometry state asset estimate:** Per-building-type day count required; estimate floor is 2–4 days per type. Cannot be approved without that number.
- **[Carried from Q12] Defense emplacement milestone placement:** Blocking for any scope estimate including the emplacement.
- **[Carried from Q12] Power-emplacement dependency raid AI design:** Query path architecture for rational targeting unspecified.
- **[Carried from Q12] Power node degraded state visual signal:** What communicates "systems affected" at 500 meters in flat-poly. Must resolve before the degraded model is built.
- **[Carried from Q12] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value:** Deferred pending M7 building type count and structural damage accumulation rates.
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
<!-- complete -->
