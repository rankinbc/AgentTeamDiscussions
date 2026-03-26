# Co-op State Model

*Generated: 2026-03-25 15:47 | Question 6 | 189s | Mode: ev18hornet*

## Decisions

**Option B is the co-op state model. The galaxy advances when the hosting player's instance is running.**

The world does not pause when one player goes offline. Time passes, faction pressure continues, and offline settlements remain subject to raid activity. The SimCopter payoff — returning to find a changed skyline — requires that the world has lived without you. A paused galaxy strips that out and reduces co-op to a scheduling dependency. Option A is rejected.

Option C is also rejected. Independent instances that merge on reconnect produce standing values without shared cause. A standing delta that originates in a simulation branch the other player never inhabited is not a traceable consequence — it is a sync artifact. The shared settlement is the co-op premise. Two private instances that synchronize are not a shared world.

**The hosting player's machine is the authoritative simulation host.**

In a 2-player Godot 4 co-op without a dedicated server, the only realistic deployment is host-authoritative. The galaxy advances only when the host instance is running. If the hosting player goes offline, the simulation pauses regardless of design intent. This is not a flaw — it is a deployment constraint that must be named explicitly and held as a hard architectural fact. The offline player's state advances only during host-active sessions. Documents, milestone specs, and the M8 co-op implementation must reflect this.

**Offline settlements produce a distinct raid profile from crewed settlements.**

Player presence is a deterrence variable in the same raid calculation that already reads fleet strength at location. An uncrewed settlement — player docked, no active session — reads as a low-threat target. The faction simulation responds accordingly: offline settlements attract harassment-scale raids, not assault-scale raids. This is not a protection rule added to spare offline players. It is the deterrence math applied consistently. Factions probe weak points; an uncrewed settlement is a weak point by definition.

**A docked fleet at a settlement contributes deterrence regardless of the owning player's online status.**

Player presence and ship presence are distinct variables. A capital ship with escorts docked at a settlement is still a visible threat profile. The faction raid calculation reads hull count at location, not session status. An offline player with a strong fleet docked provides real deterrence. An online player with no ships at their settlement provides none. The system must not conflate "player is logged off" with "settlement is undefended."

**The last-present player is the attributable actor for standing-consequential events in their session window.**

Co-op breaks EV's standing traceability assumption the moment consequential events occur without both players present. The answer is not shared culpability — it is session-scoped attribution. Standing moves that originate from decisions made during Player 1's active session are attributed to Player 1's standing track. When Player 2 returns and finds damage, the return-log surfaces what Player 1 faced and chose: which raid contacted the nav edge, whether an intercept was attempted, which wave reached the planet. Player 2 sees the consequence of their partner's decision, in sequence, with cause visible.

This establishes the first co-op teaching moment: you understand the faction system by reading someone else's playthrough. It also means the traceability EV required — the ability to reconstruct your faction relationship from your own choices — is preserved per player rather than dissolved into shared ambiguity.

**A return-log is a required feature, not a print statement.**

Consequential offline events must be legible on return. A gap in the skyline is only narrative if the player can read the sentence. The return-log must surface: which faction acted, what was destroyed, what standing moved and on whose track, and what intercept opportunity existed or was taken. "Korrath faction raided while you were docked — three hits, one building lost, standing delta on Player 1's track, intercept attempted at nav edge" is the minimum readable sentence. The return-log is discrete scope with its own implementation cost and must be assigned a milestone slot before M8 co-op work begins.

**Standing uses per-player tracks with a shared settlement state.**

The settlement's physical state — which buildings exist, what tier it holds — is shared. Both players see the same skyline. The standing ledger that governs faction pressure and rebuild gates is per-player. This resolves Vera's attribution problem without dissolving traceability: each player's faction relationships remain reconstructable from their own decisions. The raid calculation that targets a shared settlement reads the combined deterrence profile (both players' docked fleets) but attributes the standing consequence to the player whose session window was active when the triggering decision occurred.

---

## Open Questions

- **Harassment vs. assault raid definitions:** What are the concrete parameters that distinguish a harassment-scale raid from an assault-scale raid — ship count ceiling, building damage cap, tier regression eligibility? This must be defined before offline raid logic is implemented, and before M8 co-op scope can be estimated.

- **Dual-offline resumption:** If both players go offline simultaneously (host and client both close), what is the canonical session state on next host boot? Is the last committed save state the resume point, or does the simulation reconstruct elapsed time? The host-authoritative model makes this a data durability question, not a design preference.

- **Cross-player standing triggers:** When Player 1's action causes a standing consequence that affects a faction also pressuring Player 2's settlements, does Player 2's standing track move? Or does cross-player faction spillover require an explicit shared-action mechanic that is not yet designed? This must be answered before M5 faction standing API is specified, because the data model branches here.

- **Return-log milestone slot:** The return-log is confirmed as required scope. Which milestone does it land in — M7 Settlement (where offline raid damage first becomes meaningful) or M8 Co-op (where the full attribution model is live)? If M7 proceeds without a return-log, the first offline damage events will be unreadable. This is a sequencing dependency, not a nice-to-have.

- **Host selection protocol:** In a 2-player session, is the host role fixed (whoever started the session) or negotiable (either player can host)? If the offline-player's standing track advances only during host-active time, asymmetric hosting creates asymmetric faction pressure accumulation. The constraint must be surfaced in the M8 co-op spec.
<!-- complete -->
