# Standing Recovery Mechanics

*Generated: 2026-03-25 16:39 | Question 5 | 188s | Mode: ev18hornet*

## Decisions

**Standing Recovery Is Mission-Gated, Not Credits-Gated or Standing-Gated:** Recovery from degraded faction standing requires completing faction missions. Credits may be attached to those missions as a secondary cost, but credits alone cannot purchase standing improvement. A faction that accepts payment in lieu of demonstrated loyalty has no ideological identity; a faction that requires proof does. This asymmetry is how faction character is expressed through mechanics rather than lore text.

**Recovery Missions Draw From the Existing Mission Pool:** No distinct recovery mission type ships in M5. Recovery missions are ordinary faction missions that happen to move standing in a positive direction. Separate authored recovery strings are content scope that requires playtest data on standing movement rates before the cadence is defensible. Distinct recovery mission types are M6+ at earliest.

**Recovery From a Degraded Faction Structurally Costs Rival Faction Standing:** Completing faction missions to repair one relationship applies the standard `FACTION_STANDING_LOSS_MULTIPLIER` to rival factions. This is not a special recovery penalty — it is the ordinary mission consequence operating in a degraded context. The emergent result is that the geometry of recovery differs depending on how standing was lost: passive neglect produces a different recovery path than active antagonism, because the rival standing consequences have accumulated differently.

**Standing Operates in Three Behavioral Bands:**
- **Engaged** (standing ≥ 40): missions available normally, NPC contacts speak, full equipment access
- **Degraded** (standing < 40, above the hostile floor): faction contacts cold, mission availability sparse, Bar contacts may decline mission offers
- **Hostile** (standing below the hostile floor): faction shoots on sight; recovery from this band is not player-initiated in M5

The threshold between Engaged and Degraded is 40, consistent with the prior commitment NPC and tooltip decisions.

**The Hostile Floor Exists and Its Value Is Deferred:** A standing floor below which faction forces engage on sight is a confirmed design element. The exact numeric value is not set in M5 — it requires playtest data on how quickly standing moves under normal play. The floor must be implemented as a named config constant from day one to support authoring without code changes.

**Recovery From Hostile Standing Is Not Player-Initiated in M5:** Recovery from the Hostile band requires an authored trigger — an intermediary NPC, a specific mission string, or a narrative unlock — to re-open the recovery path. This is content work with no ceiling. It is M6 scope or later. M5 implements the Hostile band as a behavioral state (faction attacks on sight, Bar contacts absent) but does not ship a recovery path out of it.

**The Standing Tooltip Fires Downward Through 40:** The prior open question on tooltip direction is closed. The standing tooltip fires the first time any faction standing crosses 40 in either direction. The downward crossing uses distinct text: it names the faction, shows the current value, and states what is starting to close — not a general orientation tooltip but a warning that a relationship is slipping. The upward crossing retains its prior behavior: names the system, shows the value, describes what standing affects. Each direction fires once per faction, independently. A player who crosses 40 upward and then downward sees both tooltips.

**Bar Contacts Surface a Cold Dialogue Line in the Degraded Band:** When a player's standing with a faction has crossed into the Degraded band and a Bar contact from that faction would otherwise offer a mission, the contact delivers a single cold dialogue line rather than a mission offer. The line communicates that missions are unavailable at the current standing level. This is one string per faction contact, not a branching tree. It is the legibility signal that makes the Degraded band readable before it becomes the Hostile floor. The exact text is content design work; the behavioral trigger is an M5 implementation point.

**M5 Implements the Three Bands as Thresholds Only:** In M5, the behavioral distinction between Engaged and Degraded is expressed through mission availability and the cold Bar dialogue line. Atmospheric patrol density as a standing feedback signal is M8 geometry. The visual and kinesthetic recovery loop — airspace clearing as standing improves — is a confirmed design intent for M8 but has no M5 implementation surface.

**Recovery Is Available From the Degraded Band Without an Authored Unlock:** A player in the Degraded band can begin recovery by accepting and completing faction missions from whatever sparse pool is available. No special unlock, intermediary, or authored trigger is required to enter the recovery path from the Degraded band. The cost is the missions themselves and the rival standing they consume — not access to the path.

---

## Behavioral Rules

**Standing Thresholds Drive NPC Behavioral State:** Bar contact behavior — mission offer or cold line — is a read against faction standing at the time of interaction. No state flag is set on the NPC; the standing value is the source of truth. A contact that was cold becomes warm the moment standing crosses back above 40.

**Recovery Missions Are Indistinguishable From Ordinary Missions:** The mission pool does not tag missions as "recovery missions." Mission authors assign standing deltas per the existing content design rules. The emergent property that completing missions repairs standing is a consequence of the standing system, not a distinct mission category.

**The Hostile Band Has No Recovery Path in M5:** A player in the Hostile band has no in-game mechanism to initiate standing repair. The system correctly represents a relationship that has collapsed past the point of informal repair. The authored recovery trigger that would unlock a path out of Hostile is explicitly out of M5 scope.

---

## Open Questions

- **Hostile floor numeric value:** What standing value marks the boundary between Degraded and Hostile? Must be a named config constant. Requires playtest data on standing movement rates before a defensible value can be authored.
- **Authored Hostile recovery trigger:** What form does the M6+ authored trigger take — intermediary NPC, specific mission string, or faction-unique narrative unlock? Design is deferred pending playtest data on how often players reach Hostile standing under normal play.
- **Mission pool sparsity in the Degraded band:** What defines "sparse" — is it a probability filter on available missions, a reduced mission count at Bar contacts, or a subset of mission types? Implementation rule for the Degraded band mission availability is not yet specified.
- **Per-faction rivalry heat values:** Which faction pairs have hotter relationships than others. Out of M5 scope. Config architecture must support per-faction overrides from day one even with no authored values.
- **Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases once a player has triggered the commitment NPC and later acts for the opposing faction. Deferred. Applies post-commitment only.
- **Commitment NPC dialogue content:** Exact dialogue across settlement tier contexts. Content system for reading settlement tier and raid history variables into NPC dialogue is not yet designed.
- **Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Deferred to M8.
- **Joint action delta magnitude:** Whether each participating player receives the full standing consequence or a fractional share. Must be resolved before M8 mission resolution code ships.
- **Standing change cause attribution:** Notification surface for co-op participation. Deferred to M8.
<!-- complete -->
