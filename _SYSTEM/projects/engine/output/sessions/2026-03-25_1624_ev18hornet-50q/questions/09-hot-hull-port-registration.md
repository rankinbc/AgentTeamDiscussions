# Hot Hull Port Registration

*Generated: 2026-03-25 16:53 | Question 9 | 195s | Mode: ev18hornet*

## Decisions

**Hot Hull Port Registration Uses Fixed Standing Cost in M5:** Port registration for a captured hull applies a single, immediate standing consequence with no player choice at the registration screen. The cost is fixed, faction-specific, and legible. This is not a permanent design constraint — it is the correct M5 form of the mechanic given what systems exist to receive downstream consequences.

**Standing Cost Is Faction-Specific:** The standing delta applied at registration is determined by which faction owned the captured hull. Capturing a Confederation vessel costs Confederation standing. Capturing a Raider vessel costs Raider standing. The magnitude is a named config constant per faction, not a shared value. This aligns with the existing faction-specific config architecture required by per-faction rivalry heat values.

**Delta Magnitude Implemented as Named Config Constants:** Standing loss on hull capture must be authored as named constants in the faction config, not hardcoded. This follows the pattern established for `FACTION_STANDING_LOSS_MULTIPLIER` and the hostile floor threshold. No defensible numeric value is specified here; that is a tuning question requiring M5 playtest data on standing movement rates under normal boarding play.

**Choice Architecture (Bribe / Salvage Flag / Accept Penalty) Is Explicitly Deferred:** The multi-path registration design requires downstream infrastructure that does not exist in M5: Bar informant contacts to surface deferred revelation, patrol spawn modifiers that read hull provenance as a standing-independent flag, and an intel-triggered raid causal path separate from threshold crossing. None of these systems are M5 scope. Building the choice UI without the consequence surfaces produces a screen that lies about what the system does — all paths would resolve to a `mutate_standing` call with a modified delta, indistinguishable from fixed cost with extra player friction. That outcome is strictly worse than fixed cost alone.

**Choice UI Without Consequence Infrastructure Is Rejected:** A three-option registration screen where bribe and salvage internally route to `mutate_standing(player, faction, delta * reduction)` is not choice architecture — it is a discount mechanic with false framing. The bribe path is only meaningful if the information asymmetry it creates can be discovered, surfaced, and recognized as cause and effect when it fires. That recognition requires the Bar rumor surface to exist and for the player to encounter it at a moment when the connection to their earlier decision is traceable. Neither condition holds in M5.

**Existing Architecture Already Supports Future Choice Paths:** The current `mutate_standing(player, faction, delta)` signature is player-scoped and faction-scoped. When the Bar rumor system ships, the bribe path can route to a deferred-state store rather than an immediate standing mutation without requiring changes to the core standing architecture. The M5 fixed-cost implementation does not close off multi-path registration — it defers it correctly.

**Choice Architecture Earns Scope When the Bar Rumor System Exists:** The bribe path becomes implementable when: (1) the Bar has a rumor or informant contact surface that can surface a deferred event to the player, and (2) the player can plausibly connect that surface event to a registration decision made in a prior session. The salvage flag path earns scope when faction-specific grievance tracking (distinct from aggregate standing) is a live system, because the salvage route does not degrade standing — it creates a named crew-loss event against a specific faction, which is a different causal chain entirely.

---

## Open Questions

- **Hull capture standing delta magnitude per faction:** What is the specific standing cost for registering a captured hull from each faction? Named config constants are required from day one; numeric values require M5 playtest data on standing movement rates before they are defensible.

- **Relative magnitude of hull capture versus mission failure:** Is capturing a hull a heavier standing event than failing a faction mission, or comparable? The boarding mechanic may represent a more deliberate hostile act than mission failure; whether that registers as a larger standing consequence is unspecified.

- **Bribe path design:** Fully deferred. Requires Bar rumor/informant contact surface, a deferred-state store for hull provenance, and a discovery trigger. Earns scope when Bar rumor system ships. Intended behavior: standing preserved at registration time, information asymmetry created, consequence fires when hull provenance is surfaced through Bar contacts or patrol-read events.

- **Salvage flag path design:** Fully deferred. Routes through faction-specific grievance tracking rather than aggregate standing mutation. Capturing a Raider hull and flagging it as salvage does not degrade Raider standing — it creates a named crew-loss grievance against the specific Raider faction or cell. That causal path requires a grievance data model that does not exist in M5.

- **[Carried from Q8] M6 scope capacity:** What is already committed to M6 (ship acquisition, fleet composition UI, hire flow through The Bar)? Whether functional galaxy-layer formation AI and the threat-aware hold state both fit M6 or whether the hold state pushes items to M7 cannot be determined without the current committed scope list.

- **[Carried from Q8] Build cost of threat-aware hold state:** Detecting layer entry, reading faction standing from inside the hold state, and implementing raid threat interruption are discrete build items. The estimate gates M6 vs. M7 placement of the threat-aware requirement.

- **[Carried from Q8] Escort hold visual treatment:** Circular orbit, stationary hover, or trailing vector. A UX decision is required before M6 ships the layer-transition contract.

- **[Carried from Q8] Mechanical resolution when a raid spawns during escort hold:** Does the escort engage? Can it be destroyed? Does the player surface to a changed tactical situation? The authored rule is not yet specified.

- **[Carried from Q3–Q8] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for M5, M6, M7, or M8 yet.

- **[Carried from Q3–Q8] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after a player triggers the commitment NPC and acts for the opposing faction. Deferred; applies post-commitment only.

- **[Carried from Q5–Q8] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending M5 playtest data on standing movement rates.

- **[Carried from Q5–Q8] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Deferred pending playtest data on Hostile band frequency under normal play.

- **[Carried from Q5–Q8] Mission pool sparsity definition in Degraded band:** Probability filter, reduced mission count at Bar contacts, or mission type subset. Implementation rule not yet specified.

- **[Carried from Q3–Q8] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts (Claim Stake through City); content system for reading settlement tier and raid history variables into NPC dialogue not yet designed.

- **[Carried from Q3–Q8] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

- **[Carried from Q3–Q8] Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions or only upward. Threshold of 40 is decided; directional trigger is open.

- **[Carried from Q4–Q8] Joint action delta magnitude:** Full or fractional standing consequence per participating player in a co-op joint action. Must resolve before M8 mission resolution code ships.

- **[Carried from Q4–Q8] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8.

- **[Carried from Q3–Q8] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Deferred to M8.

- **[Carried from Q6–Q8] Passive decay milestone:** At which milestone, if any, does refusal-tracking decay earn scope. Requires M5 event-only playtest data.

- **[Carried from Q6–Q8] Refusal-tracking attribution rule:** How to distinguish deliberate decline from player absence from player never having reached a faction Bar. Edge case unresolved.

- **[Carried from Q6–Q8] `DECAY_FLOOR` numeric value:** Named config constant required, set above `HOSTILE_THRESHOLD`. Value deferred pending M5 playtest data.

- **[Carried from Q7–Q8] Terrain avoidance timing:** Deferred alongside full atmospheric escort follow to M8.
<!-- complete -->
