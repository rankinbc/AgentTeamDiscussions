### Soren (solo dev scope warden)

**RESPOND — Soren**

Three items on the table. Let me sequence them by when they actually need to be built.

**Propagation: lock it, it's free.** No automatic bleed means no new code. The M5 API is `mutate_standing(player, faction, delta)`. One call per player, per action. Done. This costs nothing to decide and nothing to build. Locked.

**Delta magnitude: defer it, it's M8 work.** Vera's question is real, but M5 ships single-player. There are no co-op freighter kills in M5. The delta magnitude question only becomes load-bearing when two players can take joint actions — that's M8. Designing the fraction now means designing it without playtest data on how fast standing actually moves in solo play. That's guessing. Note it as an M8 open question, don't spec it today.

**Attribution UI: flag it as scope.** Nadia's ask is correct in principle. It is also a notification system, which means message routing, localization surface, and UI polish. "Participated in destruction of a Confederation freighter" is three words that imply a logging architecture. That work expands. For M5, single-player, the triggering action is always the active player's own action — attribution is implicit. A standing-change notification for M5 can be `standing_changed(faction, delta)` with no cause string. The cause-attribution requirement is an M8 co-op legibility problem, not an M5 solo standing problem.

Sequence: lock propagation, defer delta magnitude to M8, defer cause-attribution UI to M8. M5 API surface stays minimal.


<!-- complete -->
