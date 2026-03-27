# Starter Ship at Respawn

*Generated: 2026-03-25 17:16 | Question 15 | 217s | Mode: ev18hornet*

## Decisions

**Free Shuttle is the respawn ship model.** On death, the player receives a Shuttle regardless of what hull they were flying. The loaner-against-future-earnings framing is explicitly rejected. Debt requires a state on the player record, a repayment trigger on every credit-earning event, and a UI surface at respawn, at the Bar, and at payoff — approximately one week of build time that metastasizes into every credit-earning feature added in later milestones. The "insurance" framing is real design space (EV Nova shipped it as a purchasable upgrade) but earns scope only when the economy is mature enough to price it and playtest data exists on how often death occurs and how much it costs.

**Consequence from hull loss is reset by design; consequence from cargo and mission failure is the weight-bearing mechanism.** This maps directly to EV's actual design. The boarding mechanic's risk calculus derives from the investment in the captured hull's cargo and the mission failure standing hit — not from the possibility of permanent hull loss. Free Shuttle respawn does not undercut boarding; it correctly locates the consequence in the cargo and standing systems, which already exist.

**Credit floor is defined by capability, not by a number.** The floor must always guarantee enough credits to fly to the nearest Bar and accept one mission. This is the minimum viable re-entry point into the economy. Any credit state below this floor is a locked state; locked states in the first session are fatal. The floor is implemented as a single named config constant: `RESPAWN_SHUTTLE_CREDIT_FLOOR`. Numeric value is deferred pending playtest data on mission reward rates and travel costs.

**`RESPAWN_SHUTTLE_CREDIT_FLOOR` must be authored as a named config constant from day one.** The implementation is a constant and a starting value — an afternoon of build time. No debt tracking, no repayment surface, no mission-reward interception required.

**The flight-feel argument does not change the respawn ship.** The atmospheric approach to a damaged settlement is a Shuttle flight-model tuning problem, not a respawn ship selection problem. If the Shuttle's bank-and-yaw response is insufficient for the approach to land emotionally, the fix is in the atmospheric flight model, which is already in scope. Respawn ship tier is not the authoring surface for approach feel.

**Purchasable ship insurance is confirmed design intent, deferred.** EV Nova's model — optional, purchasable insurance that restores the lost hull class — is the correct post-EV-core-loop answer. It earns scope at the milestone when the economy is mature enough to price it, which requires playtest data on death frequency and hull replacement costs. It does not ship in M5.

**The first-death experience must be immediately legible without tooltips.** The respawn screen must communicate — at the moment of respawn, without requiring menu navigation — that the player is in a Shuttle, their previous hull is gone, and their credit state is visible. This is a UI surface requirement, not a design decision about the model. Content and layout of the respawn screen are not specified here.

---

## Open Questions

**`RESPAWN_SHUTTLE_CREDIT_FLOOR` numeric value:** Named config constant required from day one; numeric value deferred. Requires authored mission reward rates and inter-system travel cost data before a defensible floor can be set. The capability definition (enough to reach nearest Bar and accept one mission) is the authoring target.

**Insurance milestone placement:** At which milestone does purchasable ship insurance earn scope? Requires playtest data on death frequency under normal play and hull replacement cost data from the economy. Cannot be scoped before M5 event-only playtest data is available.

**Cargo loss on death:** EV's consequence model locates boarding risk in cargo loss, not hull loss. Whether this game confirms cargo is lost on death — and at what scope — is not addressed in this discussion. Must be resolved before the boarding mechanic's risk calculation can be specified.

**Shuttle flight model tuning for atmospheric approach:** The emotional requirement for the settlement approach (bank angles, roll response, low-pass behavior) must be specified as a tuning target before the atmospheric layer ships. Not a respawn design question — a flight-model design question for the Hornet Layer milestone.

**Tier-mismatch edge case — distant respawn in hostile space:** The last-docked anchor decision places the player at their own pad or most recent docked port. The edge case where a player's last docked anchor is far from their settlement and they respawn in a Shuttle in contested space is an unresolved tactical situation. Not blocked, but should be acknowledged before M5 death-flow implementation begins.

**[Carried from Q14] Pad destruction and anchor invalidation — Option A vs. Option B:** If a settlement pad degrades or is destroyed through raid damage, does it remain a valid respawn anchor? Option A: degraded pad remains dockable and valid. Option B: pad below damage threshold invalidates anchor, requires fallback chain. Not resolved. Option B build cost cannot be estimated until pad damage model scope is known.

**[Carried from Q14] Tier regression depth and pad functionality:** How deep does tier regression cut pad functionality across regression steps (Colony→Settlement→Outpost)? Does the pad survive intact, degrade in place, or disappear? Blocking for Option B scope estimate.

**[Carried from Q14] Landing on degraded pad and anchor write behavior under Option A:** Requires confirmation before M7 builds the pad damage model.

**[Carried from Q14] Standing re-check at respawn time vs. docking write time:** Simpler rule (anchor set at docking, not re-evaluated at respawn) vs. stricter rule (re-check at respawn, fallback if standing degraded since docking). Must resolve before death-flow implementation begins.

**[Carried from Q3–Q13] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for any milestone.

**[Carried from Q3–Q13] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after a player triggers the commitment NPC and acts for the opposing faction. Deferred; applies post-commitment only.

**[Carried from Q5–Q13] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending M5 playtest data on standing movement rates.

**[Carried from Q5–Q13] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Deferred pending playtest data on Hostile band frequency under normal play.

**[Carried from Q5–Q13] Mission pool sparsity definition in Degraded band:** Probability filter, reduced count, or mission type subset. Implementation rule not yet specified.

**[Carried from Q3–Q13] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables into NPC dialogue not yet designed.

**[Carried from Q3–Q13] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

**[Carried from Q3–Q13] Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions or only upward. Threshold of 40 decided; directional trigger open.

**[Carried from Q4–Q13] Joint action delta magnitude for co-op:** Full or fractional standing consequence per participating player. Must resolve before M8 mission resolution code ships.

**[Carried from Q4–Q13] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8.

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

**[Carried from Q11–Q13] `RAID_HARASSMENT_THRESHOLD` numeric value:** Named config constant required from day one; value deferred pending M5 playtest data.

**[Carried from Q11–Q13] `RAID_ASSAULT_THRESHOLD` numeric value:** Named config constant required from day one; value deferred pending M5 playtest data.

**[Carried from Q11–Q13] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value:** Named config constant required from day one; value deferred pending M7 building type count and structural damage accumulation rates.

**[Carried from Q11–Q13] Building type count at Settlement, Colony, and City tiers:** Required inputs for M8 visual regression asset estimate. Outpost floor confirmed at three; remaining tiers unspecified.

**[Carried from Q11–Q13] Tier regression milestone placement:** Does visual geometry regression ship in M7 or M8? Stat-only regression could ship earlier; geometry regression requires asset pass acknowledgment first.

**[Carried from Q11–Q13] Assault-scale split-vector spawn bearing offsets for M7 solo:** Two approach bearings must be named config constants. Contested airspace two-spawn-axis geometry for split-commitment co-op remains deferred to M8.

**[Carried from Q11–Q13] First-raid protection window co-op edge case:** Does `player_has_had_clean_atmospheric_view` require both players or only the triggering player to have completed an unobstructed descent?

**[Carried from Q12–Q13] Defense emplacement milestone placement:** Blocking for any scope estimate including the defense emplacement.

**[Carried from Q12–Q13] Power-emplacement dependency raid AI design:** Query path architecture for rational targeting — what it reads, when, how it affects spawn vector selection — is unspecified.

**[Carried from Q12–Q13] Power node degraded state visual signal:** What visual element communicates "systems affected" at 500 meters in flat-poly? Must be resolved before the degraded model is built.

**[Carried from Q13] Tier regression rebuild cost mechanism:** What specific form — resource quantity reduction, time reduction, or step-count reduction — and what named config constant. Not yet decided.

**[Carried from Q13] Which in-world surface carries the rebuild gate explanation:** Comms intercept string or Bar cold dialogue must name the standing gate at the moment of regression. Content design question not resolved.

**[Carried from Q13] Scaffolding third geometry state asset estimate:** Requires per-building-type day estimate before the group can evaluate. Estimate floor is 2–4 days per type for a flat-poly scaffolding mesh.
<!-- complete -->
