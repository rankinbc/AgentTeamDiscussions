### Soren (solo dev scope warden)

**[SCOPE - Soren (scope estimator)]**

Let me separate the implementation question from the design question, because the group has been conflating them.

**Implementation cost is identical across options 1 and 2.** You're writing a standing delta function. Option 1: multiplier is 1.0. Option 2: multiplier is 1.5. That's a named constant. One line of config. The architecture is the same either way. Don't let the philosophical distance between symmetric and asymmetric imply a build cost difference — there isn't one.

Option 3 is different. Faction-specific heat requires someone to decide which rivalries are hotter *before* you implement, because those values have to come from somewhere. That's a design debt that blocks the code, not a tunable you discover in playtest. Ren correctly called this post-playtest. I'd go further: it's out of M5 scope entirely.

Vera and Nadia have already dissolved the primary argument for asymmetry in M5. The gate handles permanent neutrality. Defection cost after commitment is a legitimate asymmetry use case — but that's a post-commitment question, not a pre-commitment one, and it's a different implementation point.

**My recommendation:** Name the constant. Call it `FACTION_STANDING_LOSS_MULTIPLIER`. Set it to `1.0` for M5. Design the system so it's overridable per-faction later. Ship.

The decision that burns M5 time isn't symmetric vs asymmetric. It's spending another session on a multiplier you can change in thirty seconds after playtest.

Call the constant. Move to dialogue.


<!-- complete -->
