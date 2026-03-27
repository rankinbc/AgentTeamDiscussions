# Hot Hull Interdiction Trigger

*Generated: 2026-03-25 16:56 | Question 10 | 199s | Mode: ev18hornet*

## Decisions

**Hot Hull Interdiction Trigger Is Standing-Only in M5:** Faction patrol interdiction during the hot-hull window reads from the player's faction standing value only. The captured hull does not carry a persistent provenance flag that operates as an independent hostility axis. Every hostile patrol encounter traces to a single legible cause: the standing delta applied at port registration. Two-axis interdiction (standing AND hull flag) is explicitly rejected for M5.

**Hull Provenance Flag Is Not Implemented in M5:** A ship-level flag encoding hull origin and readable by patrol AI is not built in M5. The bribe path and salvage flag path — both of which require hull provenance persistence as a precondition — are already deferred. Building provenance infrastructure before either downstream mechanic has an earn date is premature architecture. The existing `mutate_standing(player, faction, delta)` signature is the only write path for hull capture consequences in M5.

**Patrol AI Reads Standing, Not Ship Identity:** Patrol AI in M5 has no authored read path for ship-level attributes. Teaching patrol spawn and interdict logic to distinguish "standing hostile" from "hull-recognition hostile" would require a new data model and a new patrol query surface. That is not an extension of what exists — it is a separate system. It is out of M5 scope.

**The Hot-Hull Window Requires an Atmospheric Feedback Surface:** Standing-only interdiction is architecturally correct but incomplete as a player experience. A player flying a captured hull into atmosphere after paying the registration standing cost must feel the standing consequence in the cockpit — not only at the port screen. Without a flight-layer signal, the registration consequence is paid, forgotten, and then patrol interdiction reads as arbitrary. This is a feedback problem, not a second-axis problem. The atmospheric tell is the correct M5 surface.

**Atmospheric Tell Is a Single Comms Intercept String Plus Modified Patrol Vector:** The hot-hull atmospheric feedback surface ships as two elements: (1) a single comms intercept string that fires when the player enters atmosphere in a hull whose faction standing cost crossed the Degraded threshold — the string names the faction and signals recognition, not an abstract standing value; (2) an early intercept vector on the spawned patrol, making the patrol's approach angle steeper and faster than a routine standing-hostile contact. These two elements together make the ship feel dangerous to fly without introducing a second hostility axis or a new data model. Both elements read from the existing standing value at entry time.

**Comms Intercept String Fires on Atmospheric Entry, Not on Patrol Spawn:** The comms intercept fires at atmosphere entry when standing with the hull's faction of origin is in the Degraded band or below. It does not fire on every flight and does not fire in the Engaged band. It is a one-time signal per atmospheric entry session, not a recurring status indicator. The string is one line per faction, not a branching tree, consistent with the cold-dialogue constraint established for Bar contacts in the Degraded band.

**Modified Patrol Vector Is a Behavior Tweak, Not a New Patrol Type:** The early intercept vector is a modifier applied to the existing patrol spawn behavior when standing is in the Degraded band and the player is flying a hull of matching faction origin. It does not require a new patrol archetype, new AI state, or new query path. It is a numeric adjustment to spawn timing and approach angle within the existing patrol system.

**Hull Origin Stored Minimally for Feedback Purposes Only:** The comms intercept string and patrol vector modifier require knowing which faction's hull the player is flying at atmosphere entry time. This is stored as a single string field on the ship record — `hull_faction_origin` — set at registration and read at atmospheric entry. This field does not feed patrol AI as a hostility condition. It does not replace standing as the interdict trigger. It is a read-only input to the feedback surface, not a second hostility axis. This is the minimum attribution required to make the atmospheric tell faction-specific.

**`hull_faction_origin` Does Not Gate Interdiction:** Patrol interdiction in M5 fires when faction standing crosses the hostile threshold — period. `hull_faction_origin` is never queried as part of the interdiction condition. A player in a captured Confederation hull with Confederation standing in the Engaged band will not receive a hot-hull comms intercept and will not receive a modified patrol vector. The captured hull is invisible to interdiction logic once the standing delta is paid. The standing delta is the entire consequence.

**Choice Architecture Deferral Is Preserved:** Nothing in this decision reopens the bribe path or the salvage flag path. The minimum provenance storage (`hull_faction_origin`) does not constitute the deferred-state store required by the bribe path, which requires Bar rumor surface integration and an information-asymmetry consequence chain. The salvage flag path requires faction-specific grievance tracking that does not exist in M5. Both remain deferred on their existing terms.

**Existing Architecture Requires No Revision:** The M5 implementation of hot-hull interdiction trigger and atmospheric feedback requires no changes to `mutate_standing(player, faction, delta)`, no new patrol AI state, no new player-facing UI beyond the comms string, and no data model beyond the single `hull_faction_origin` string field on the ship record. The comms intercept and patrol vector modifier are authored against existing standing band reads.

---

## Open Questions

- **Hull capture standing delta magnitude per faction:** Named config constants required from day one; numeric values deferred pending M5 playtest data on standing movement rates.
- **Relative magnitude of hull capture versus mission failure:** Whether boarding registers as a heavier standing consequence than mission failure is unspecified. May carry design intent (deliberate hostile act versus performance failure) but requires playtest data before a defensible ratio is authored.
- **Comms intercept string content per faction:** The string is one line per faction contact; exact wording is not specified here. Content design is out of scope for this decision.
- **Patrol vector modifier numeric values:** Spawn timing offset and approach angle adjustment are implementation details requiring M5 playtesting. Must be authored as named config constants, not hardcoded.
- **Bribe path design:** Fully deferred. Requires Bar rumor/informant contact surface, deferred-state store for hull provenance beyond `hull_faction_origin`, and discovery trigger. Earns scope when Bar rumor system ships.
- **Salvage flag path design:** Fully deferred. Requires faction-specific grievance tracking that does not exist in M5.
- **Hull provenance flag as independent hostility axis:** Whether `hull_faction_origin` or a richer provenance flag ever becomes an independent interdiction trigger — the two-axis design Ren and Max describe — is deferred. It is the correct design direction for M8 contested airspace geometry but requires patrol AI infrastructure, player-facing flag tracking, and the Bar rumor surface before it is buildable.
- **[Carried] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for M5, M6, M7, or M8.
- **[Carried] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after a player triggers the commitment NPC and acts for the opposing faction. Deferred; applies post-commitment only.
- **[Carried] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending M5 playtest data.
- **[Carried] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Deferred pending playtest data on Hostile band frequency.
- **[Carried] Mission pool sparsity definition in Degraded band:** Probability filter, reduced count, or mission type subset. Implementation rule not yet specified.
- **[Carried] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history variables into NPC dialogue not designed.
- **[Carried] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.
- **[Carried] Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions or only upward. Threshold decided; directional trigger open.
- **[Carried] Joint action delta magnitude for co-op:** Full or fractional standing consequence per participating player. Must resolve before M8 mission resolution code ships.
- **[Carried] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8.
- **[Carried] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Deferred to M8.
- **[Carried] Passive decay milestone:** At which milestone refusal-tracking decay earns scope. Requires M5 event-only playtest data.
- **[Carried] Refusal-tracking attribution rule:** How to distinguish deliberate decline from absence from never having reached a faction Bar. Unresolved.
- **[Carried] `DECAY_FLOOR` numeric value:** Named config constant required, set above `HOSTILE_THRESHOLD`. Value deferred pending M5 playtest data.
- **[Carried] M6 scope capacity:** Full committed M6 scope list required to determine whether galaxy-layer formation AI and threat-aware hold state both fit M6 or push to M7.
- **[Carried] Build cost of threat-aware hold state:** Estimate gates M6 vs. M7 placement.
- **[Carried] Escort hold visual treatment:** Circular orbit, stationary hover, or trailing vector. UX decision required before M6 ships the layer-transition contract.
- **[Carried] Mechanical resolution when a raid spawns during escort hold:** Escort engagement rules, destruction possibility, and player surface state unspecified.
- **[Carried] Terrain avoidance timing:** Deferred alongside full atmospheric escort follow to M8.
<!-- complete -->
