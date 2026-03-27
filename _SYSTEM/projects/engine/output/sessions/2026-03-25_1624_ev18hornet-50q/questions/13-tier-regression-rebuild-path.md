# Tier Regression Rebuild Path

*Generated: 2026-03-25 17:08 | Question 13 | 217s | Mode: ev18hornet*

## Decisions

**Tier Regression Rebuild Path Operates at Reduced Cost, Not Same-Cost:** The rebuild path after tier regression is not the same founding investment as original construction. Reduced cost with a standing gate is the adopted model. Same-cost recovery is rejected. The two orthogonal clocks this creates — economic rebuild rate and standing recovery rate through missions — produce pressure the designer does not need to author. Players will feel the gap between them without explanation.

**Standing Remains the Primary Gate for Tier Advancement on the Rebuild Path:** Reduced cost does not bypass the standing gate. A player can accumulate rebuild resources faster than they recover standing; that gap is the designed tension. The standing requirement for tier advancement applies identically on the rebuild path and on original construction. There is no recovery-specific exemption.

**The Reduced Cost Mechanism Must Be Named Before Implementation:** The specific form of "reduced cost" is not decided. Three candidate forms were identified: a resource quantity reduction, a time reduction, or a step-count reduction in the tier advancement sequence. Each has different mechanical implications. The mechanism must be named and authored as a named config constant before implementation begins. Hardcoding a discount ratio is explicitly rejected.

**The Atmospheric Layer Owns the Recovery Feel, Not Only the Destruction Feel:** Recovery missions that function as the standing-recovery vehicle must pull the player into flight. Dirtside Bar pickup as the sole recovery surface makes the atmospheric layer optional to the rebuild arc — wrong. Supply escort missions are the designated standing-recovery vehicle. The player who surfaces from underground to find their tier regressed should be pulled upward: an escort request queued at the Bar, a mission that requires flying. Destruction is dirtside. Rebuilding lives in the sky.

**Recovery Path Must Be Self-Explaining at the Moment of Regression, In-World:** The standing gate on recovery creates a potential double-punishment loop for players who have not yet internalized the faction system. The recovery path must close this loop at the moment of regression, not in a tutorial panel. One of the two existing surfaces already active around the standing-drop event — the comms intercept string or the Bar cold dialogue — must name the standing gate as the advancement block explicitly. The message is not about credits; it is about standing. Which surface carries the line is a content design question; that one of them must carry it is a behavioral contract.

**Ren's Structural-Pass Proposal Is the Q12 Closed Decision, Restated:** Assault raid AI querying live building states before selecting spawn vectors is the rational targeting capability Q12 identified as "a weeks-level build item" and placed out of M7. Labeling it as emergence does not change the build cost. It does not earn scope in this discussion. The decision from Q12 stands: structural-awareness targeting does not ship in M7.

**Scaffolding as a Third Geometry State Is a Named Scope Question, Not a Decision:** The partial-construction scaffolding state — a legible intermediate between start-of-rebuild and fully intact — is a legitimate design proposal. It is not decided here. Adding a scaffolding state converts the existing two-state-per-building model (intact, degraded) to three states. At Outpost tier that is 9 assets instead of 6. The ratio holds at every higher tier. A flat-poly scaffolding state is a distinct mesh, not a color swap; the estimate floor is 2–4 days per building type. The group cannot evaluate the proposal without an explicit day count attached to it. The proposal is carried as a named open question pending that estimate.

---

## Open Questions

- **Tier regression rebuild cost mechanism:** What specific form does reduced cost take — resource quantity reduction, time reduction, or step-count reduction in the tier advancement sequence? Must be named and authored as a named config constant before implementation.
- **Which in-world surface carries the rebuild gate explanation:** The comms intercept string or the Bar cold dialogue must name the standing gate as the advancement block at the moment of regression. Which surface carries that line is a content design question not resolved here.
- **Scaffolding third geometry state asset estimate:** Proposal is carried pending a per-building-type day estimate. Estimate floor is 2–4 days per type for a flat-poly scaffolding mesh. The group cannot approve the addition without that number. Requires explicit scope estimate and group decision.
- **[Carried from Q12] Defense emplacement milestone placement:** At which milestone does the power-emplacement dependency earn scope? Blocking for any scope estimate including the defense emplacement.
- **[Carried from Q12] Power-emplacement dependency raid AI design:** What does rational targeting mean for assault-scale raid AI? Query path architecture — what it reads, when, how it affects spawn vector selection — is unspecified.
- **[Carried from Q12] Power node degraded state visual signal:** What visual element communicates "systems affected" at 500 meters in flat-poly? Must be resolved before the degraded model is built.
- **[Carried from Q12] `SETTLEMENT_REGRESSION_THRESHOLD` numeric value:** Named config constant required; value deferred pending M7 building type count and structural damage accumulation rates from playtest.
- **[Carried from Q12] Building type count at Settlement, Colony, and City tiers:** Required inputs for the M8 visual regression asset estimate. Outpost floor confirmed at three; remaining tiers unspecified.
- **[Carried from Q12] Tier regression milestone placement:** Does visual geometry regression ship in M7 or M8? Stat-only regression could ship earlier; geometry regression requires the asset pass acknowledgment first.
- **[Carried from Q12] Assault-scale split-vector spawn bearing offsets for M7 solo:** Two approach bearings must be named config constants. Contested airspace two-spawn-axis geometry for split-commitment co-op remains deferred to M8.
- **[Carried from Q12] First-raid protection window co-op edge case:** Does `player_has_had_clean_atmospheric_view` require both players or only the triggering player to have completed an unobstructed descent?
- **[Carried from Q3–Q12] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for any milestone.
- **[Carried from Q3–Q12] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after a player triggers the commitment NPC and acts for the opposing faction. Deferred; applies post-commitment only.
- **[Carried from Q5–Q12] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending M5 playtest data.
- **[Carried from Q5–Q12] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Deferred pending playtest data on Hostile band frequency.
- **[Carried from Q5–Q12] Mission pool sparsity definition in Degraded band:** Probability filter, reduced count, or mission type subset. Implementation rule not yet specified.
- **[Carried from Q3–Q12] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables into NPC dialogue not yet designed.
- **[Carried from Q3–Q12] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.
- **[Carried from Q3–Q12] Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions or only upward. Threshold of 40 decided; directional trigger open.
- **[Carried from Q4–Q12] Joint action delta magnitude for co-op:** Full or fractional standing consequence per participating player. Must resolve before M8 mission resolution code ships.
- **[Carried from Q4–Q12] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8.
- **[Carried from Q3–Q12] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Deferred to M8.
- **[Carried from Q6–Q12] Passive decay milestone:** At which milestone, if any, does refusal-tracking decay earn scope. Requires M5 event-only playtest data.
- **[Carried from Q6–Q12] Refusal-tracking attribution rule:** How to distinguish deliberate decline from player absence from never having reached a faction Bar. Unresolved.
- **[Carried from Q6–Q12] `DECAY_FLOOR` numeric value:** Named config constant required, set above `HOSTILE_THRESHOLD`. Value deferred pending M5 playtest data.
- **[Carried from Q9–Q12] Hull capture standing delta magnitude per faction:** Named config constants required; numeric values deferred pending M5 playtest data.
- **[Carried from Q9–Q12] Relative magnitude of hull capture versus mission failure standing consequence:** Unspecified.
- **[Carried from Q10–Q12] Comms intercept string content per faction:** One line per faction contact; exact wording is content design out of scope.
- **[Carried from Q10–Q12] Patrol vector modifier numeric values:** Spawn timing offset and approach angle adjustment must be named config constants; values deferred pending M5 playtesting.
- **[Carried from Q9–Q12] Bribe path design:** Fully deferred pending Bar rumor/informant surface and deferred-state store for hull provenance.
- **[Carried from Q9–Q12] Salvage flag path design:** Fully deferred pending faction-specific grievance tracking.
- **[Carried from Q7–Q12] M6 scope capacity:** Full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7.
- **[Carried from Q7–Q12] Build cost of threat-aware hold state:** Estimate gates M6 vs. M7 placement.
- **[Carried from Q7–Q12] Escort hold visual treatment:** Circular orbit, stationary hover, or trailing vector. UX decision required before M6 ships the layer-transition contract.
- **[Carried from Q8–Q12] Mechanical resolution when a raid spawns during escort hold:** Escort engagement rules, destruction possibility, and player surface state unspecified.
- **[Carried from Q7–Q12] Terrain avoidance timing:** Deferred alongside full atmospheric escort follow to M8.
<!-- complete -->
