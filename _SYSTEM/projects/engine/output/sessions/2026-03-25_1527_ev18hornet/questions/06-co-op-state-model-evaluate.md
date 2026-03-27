### Soren (solo dev scope warden)

**[SCOPE — Soren (scope estimator)]**

Before the design work lands, there's an architecture question nobody has asked that determines whether Option B is actually buildable by a solo dev.

**Who runs the simulation when one player is offline?**

Option B requires a live faction simulation advancing without both players present. In a 2-player Godot 4 co-op, that means one of three things: Player 1's machine is the host and runs the sim while Player 2 is gone; there's a dedicated server; or offline progression is simulated on next-login rather than real-time.

Option 1 is the only realistic solo-dev answer. But it means the host going offline pauses the galaxy regardless of design intent. Option B becomes Option A the moment the hosting player sleeps.

This isn't a design flaw — it's a deployment constraint. Name it now, because it shapes every feature the table just added:

Nadia's return-log is real scope. Event logging, legible diff, attribution display — that's not a print statement, it's a feature with its own milestone slot.

Vera's standing attribution problem is a data model decision. Shared standing ledger vs. per-player tracks isn't a design preference — it's a schema choice that must be made before M5 faction code is written.

My recommendation: **Option B with host-authoritative simulation, explicitly named.** The offline player's state advances only when the host is running. Document that constraint. Then cost the return-log and standing attribution as discrete features, because "Option B is correct" is not a scope estimate.

What is the host model?


<!-- complete -->
