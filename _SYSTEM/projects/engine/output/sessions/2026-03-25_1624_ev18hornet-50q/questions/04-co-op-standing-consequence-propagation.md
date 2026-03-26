# Co-op Standing Consequence Propagation

*Generated: 2026-03-25 16:36 | Question 4 | 164s | Mode: ev18hornet*

## Decisions

**No Automatic Standing Propagation in Co-op:** Player 1's actions never cause automatic movement on Player 2's faction standing tracks. Standing is a personal ledger. Every delta is attributable to a specific player's choice. P1 destroys a Confederation freighter — P1's Confederation standing drops, P2's Confederation standing is unaffected. This preserves the causal traceability that makes faction consequences feel authored by the player rather than ambient. The EV feedback principle holds: every raid a player sees is traceable to their own choices.

**Joint Actions Resolve as Independent Standing Mutations:** When two players participate in a joint action (co-boarding, shared escort, co-op mission completion), the action is resolved as N independent standing mutations — one per participating player — using the existing `mutate_standing(player, faction, delta)` call. There is no aggregated joint event, no split-credit flag, and no shared-action mechanic. P1 boards a Confederation freighter: `mutate_standing(player_1, confederation, delta)`. P2 boards the same freighter: `mutate_standing(player_2, confederation, delta)`. These are two calls, not one. This is a content design rule, not a code constraint, and must be documented as such. Any future implementation of a "split credit" flag at M8 would add complexity for no architectural gain.

**Joint Dispatch Requires No New M5 API Surface:** The M5 faction standing API already supports joint-action dispatch. The function signature `mutate_standing(player, faction, delta)` accepts a player reference per the M8 co-op extension contract already established. Joint actions in M8 are two calls to the same function. No additional API surface is required in M5 to support this pattern.

**Delta Magnitude for Joint Actions Is Deferred to M8:** Whether each participating player receives the full standing consequence of a joint action or a fractional share is an open question, but it is not an M5 question. M5 ships single-player. No co-op joint actions execute in M5. Specifying the fraction before playtest data exists on solo standing movement rates is premature. The question is noted as M8 scope and must be resolved before any M8 mission resolution code ships.

**M5 Standing Change Notification Carries No Cause Attribution:** M5 standing change events use the signature `standing_changed(faction, delta)` with no cause string. In single-player, the triggering action is always the active player's own action — attribution is implicit. The requirement to surface cause attribution in co-op ("You participated in the destruction of a Confederation freighter") implies message routing, a logging architecture, and a localization surface. That work is an M8 co-op legibility problem. It is not built in M5.

---

## Behavioral Rules

**Standing Mutation Is Always Player-Scoped:** No standing mutation may target a faction without also targeting a specific player. There is no settlement-scoped mutation, no session-scoped mutation, and no broadcast mutation that moves multiple players' tracks simultaneously.

**Joint Action Dispatch Convention:** Joint actions are dispatched as one `mutate_standing` call per participating player. The content designer or mission author is responsible for defining the delta applied to each player. The engine makes no assumptions about equality or symmetry of deltas across players in a joint action.

**M5 Reads Single Active Player Only:** All faction standing reads and writes in M5 reference the single active player. No co-op session state is queried. The architecture must remain compatible with M8 passing multiple player references into the same logic paths without rewrite.

---

## Open Questions

- **[from Q3, active] Per-faction rivalry heat values:** Which faction pairs have hotter relationships than others. Out of M5 scope. Config architecture must support per-faction overrides from day one even with no authored values.

- **[from Q3, active] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases once a player has triggered the commitment NPC and later acts for the opposing faction. Deferred. Asymmetric defection cost applies post-commitment only.

- **[from Q3, active] Standing floor behavior:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

- **[from Q3, active] Commitment NPC dialogue content:** Exact dialogue across settlement tier contexts (Claim Stake through City). Content system for reading settlement tier and raid history variables into NPC dialogue is not yet designed.

- **[from Q3, active] Standing tooltip direction:** Whether the tooltip fires at crossing 40 in both directions (upward and downward) or only upward. Threshold of 40 is decided; directional trigger is open.

- **[from Q3, active] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Full design deferred to M8.

- **[new, M8] Joint action delta magnitude:** Whether each participating player receives the full standing consequence of a joint action or a fractional share. Must be resolved before M8 mission resolution code ships. Requires solo standing movement playtest data before the fraction is defensible.

- **[new, M8] Standing change cause attribution:** Notification surface must attribute the triggering action and the player's role in it for co-op participation. Deferred to M8. M5 standing change events carry no cause string.
<!-- complete -->
