# Co-op Faction Commitment Independence

*Generated: 2026-03-25 16:33 | Question 3 | 156s | Mode: ev18hornet*

## Decisions

**Co-op Commitment Independence:** Player 1 accepting a Confederation commitment mission does NOT close Player 2's Rebel string. Faction commitment paths are fully independent per player. One player's faction choice imposes no mechanical constraint on their co-op partner's faction options.

**No Settlement-Level Faction Heat Aggregation:** The raid system does NOT maintain a settlement-level faction heat value derived from both players' standing. Combined or averaged settlement alignment is explicitly rejected. A settlement is not an agent with its own standing; its raid pressure is derived from its players' standing at query time.

**Raid Spawn Reads Player Standing Directly:** At raid spawn, the system queries each player's faction standing independently. No intermediate aggregation layer sits between player standing and raid spawn logic. This preserves EV's core feedback principle: every raid a player sees is traceable to their own choices.

**Two Independent Faction Heat Values in Co-op:** When both players are present, the raid system maintains two independent faction heat reads — one per committed player — rather than collapsing them into a single value. This preserves directional information required by the atmospheric spawn system. Confederation intercepts spawn on a vector derived from Player 1's Confederation standing. Rebel patrols spawn on a vector derived from Player 2's Rebel standing. The atmosphere above a split-commitment settlement is contested airspace from two distinct directions.

**M5 Ships Single-Player Standing Only:** Milestone 5 implements per-player faction standing for a single player. The raid spawn path at M5 reads the active player's standing — singular. No co-op faction API ships in M5.

**M8 Co-op Extension Contract:** At Milestone 8, raid spawn is extended to query each connected player's standing independently. This requires no new data concept and no architectural revision — it is a read-path extension on the existing per-player standing model. The M5 architecture must be written to accommodate this extension without rewrite. Specifically: the raid spawn query must be written as a function that accepts a player reference, not a function that assumes a single global active player, so that M8 can pass multiple players into the same logic path.

**No Directional Spawn Axis Design in M5:** Two-spawn-axis atmospheric geometry (faction-directional intercept vectors) is deferred to M8. M5 faction standing does not define spawn axes. Designing that intersection now would compound scope across M2 (atmospheric layer), M5 (faction standing), and M8 (co-op state) simultaneously.

---

## Behavioral Rules

**The Commitment NPC is Per-Player:** The commitment NPC appears in The Bar for a given player if and only if that player individually meets the trigger condition: `faction_standing >= 60` AND `faction_mission_completed == true`. Player 2's standing has no effect on whether Player 1's NPC appears, and vice versa.

**Faction Standing Remains Per-Pilot:** Standing is recorded and read per player, not per settlement, per session, or per faction affiliation of the settlement location. This is the EV pilot model applied to co-op without modification.

**Inverse Axis Applies Per-Player:** When Player 1 gains standing with the Confederation, only Player 1's Rebel standing decreases by `FACTION_STANDING_LOSS_MULTIPLIER`. Player 2's standing is unaffected by Player 1's actions.

**Experiential Gate (Implementation Note, Not API):** The commitment NPC trigger condition (standing ≥ 60, mission completed) is mechanically sufficient. The design intent behind the threshold is that the path to 60 must have delivered enough faction-flavored encounters for the commitment to feel like a real choice, not a gate passed without context. This is not an additional code condition — it is a content design constraint on what faction missions must accomplish before standing reaches 60.

---

## Open Questions

- **Per-faction rivalry heat values:** Which faction pairs have hotter relationships than others. Out of M5 scope. Requires playtest data before values are defensible. Config architecture must support per-faction overrides from day one even with no authored values.

- **Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases once a player has triggered the commitment NPC and later acts for the opposing faction. Deferred. Asymmetric defection cost is a legitimate design tool for post-commitment pressure, but it is a different question from pre-commitment exploration cost and a different implementation point.

- **Standing floor behavior:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

- **Commitment NPC dialogue content:** Exact dialogue across settlement tier contexts (Claim Stake through City). Settlement tier and raid history inform dialogue context only, not the unlock check. Content system for reading those variables into NPC dialogue is not yet designed.

- **Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions (upward and downward) or only upward. The trigger threshold of 40 is decided; the directional trigger is open.

- **Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Full design deferred to M8. Requires atmospheric layer work, faction standing data, and co-op session state to intersect — that intersection is an M8 design problem.
<!-- complete -->
