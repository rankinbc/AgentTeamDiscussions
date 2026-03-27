# Death and Progression Setback

*Generated: 2026-03-25 15:57 | Question 9 | 180s | Mode: ev18hornet*

## Decisions

**The adopted model is Option B with world-state propagation. Ship loss is the consequence. Standing is not lost. The world registers the death.**

---

**Option B is the death model.** On death, the player respawns at the nearest friendly port in a starter ship. The destroyed ship is gone. Standing is unaffected. Credits are unaffected. Ship loss is already a session-length consequence because replacement — through purchase or capture — costs time, faction access, and economic opportunity. The penalty is built into the progression system that already exists. No second consequence layer is required.

**Option A is rejected.** Zero penalty severs the emotional wire. The SimCopter payoff requires accumulated attachment — the player has flown over the settlement, watched it grow, seen the buildings from altitude. Nothing at stake means nothing earned when the defense holds. The first death is a tutorial; Option A teaches nothing.

**Option C is rejected.** Losing unbanked credits stacks a second consequence on top of ship replacement without adding signal. Credits are already embedded in ship loss — the player who lost a Heavy Fighter and respawns in a Shuttle is already absorbing an economic hit. Adding a separate credit drain is noise on the correct signal and requires its own UI, legibility, and edge-case handling. It is scope that does not earn its cost.

**Option D (permadeath) is rejected for the default experience.** Permadeath ends the emergence chain rather than letting it continue. It is a different game and should not be the default. If pursued, it is a mode with its own milestone slot and scope estimate — not a toggle on the existing death model.

---

**Death is a world-state event, not a player-state reset.**

The standing system, deterrence calculation, and raid schedule all read the event. A player who dies does not simply respawn — the world has registered what happened.

- **Deterrence profile drops immediately.** The destroyed ship is no longer part of the settlement's hull count. The raid calculation reads hull count at location, not session status. Death is hull count going to zero. This is the existing deterrence system doing its job, not new code.
- **The faction that killed the player registers a combat outcome.** That outcome is standing-relevant. If the player was flying a hot hull at time of death, the owning faction's response to hull-confirmed-destroyed is a distinct state from hull-at-large.
- **Raid window advances.** A faction that destroyed the defending patrol knows the patrol is gone. The contested space near the player's settlement is now less defended. The raid calculation updates accordingly.

These effects require no new system. The deterrence model and standing event triggers are already required by prior decisions. Death is an input to systems already being built.

---

**The death screen must surface one sentence of faction consequence before respawn.**

Not a log. One sentence. The format is: which faction acted, what the consequence is, what changed in the world. Example: *"The Confederation registered the patrol loss. Your settlement's defense window has advanced."* The player must understand why the world changed before they re-enter it. This is the standing-before-consequence rule applied to the death moment. Hidden consequences at the death screen are ruled out by the same principle that ruled out hidden standing penalties throughout.

---

**Atmospheric death has a distinct return geometry.**

Death in the atmospheric layer — over your own settlement, during a raid defense, having watched the building from altitude — carries specific emotional weight that deep-space death does not. The respawn location reflects this:

- **Atmospheric death respawns the player at distance in 2D space**, not at port. The player arrives at altitude above the system, not inside the station dock.
- **The player must make a second dive decision.** Do you go back in? The settlement is still contested. The faction that killed you is still present. The re-entry choice is the grief mechanic. The player decides whether to return knowing what is at stake.
- **Entry altitude on re-entry follows the existing rule:** dive angle determines entry point. There is no designer override for atmospheric return after death. Steep dive, low entry. Shallow arc, high entry.

This applies only to atmospheric deaths. Death in 2D space respawns at nearest friendly port under the standard Option B flow.

---

**The replacement ship experience must be designed to communicate regression.**

Arriving in a starter ship after losing a Light Fighter or Freighter should feel like loss. This is not ambient — it is the lesson the death is teaching. The dock looks different in a smaller hull. Faction contacts the player earned remember them. The settlement the player built is still there, but defending it is now harder. That delta between what the player had and what they have is the consequence. It must be perceptible, not merely arithmetic.

The replacement ship flow is already required by progression (purchase path, capture path). The death path is a third entry into the same flow. No new system — but the experience of arriving via death must be distinct from arriving by choice.

---

**Standing survives death. It is relational, not material.**

Standing is the long-form record of who the player is in the faction system. It accumulates across sessions, survives material loss, and reflects history. A player who dies does not lose faction relationships they have built. They return to a world that still knows them — and now also knows their patrol was destroyed. That combination (standing intact, world updated) is what allows death to be a setback rather than a reset.

---

## Open Questions

**Spatial model flag (unresolved, not a death mechanics question):**
Multiple agents flagged a possible reversal of the fourteen decided space layer bullets — specifically that the PROPOSE round appeared to treat space as 3D rather than the decided 2D top-down plane. This document does not adjudicate that flag. If the space layer model has changed, the death mechanics above apply correctly to either model, but every readability, targeting, and legibility decision made for the 2D layer reopens. This flag must be resolved before M3 milestone estimates proceed.

**Specific respawn location rules for 2D space death:**
"Nearest friendly port" requires a definition of nearest (nav distance? faction standing threshold? jump graph proximity?) and a definition of friendly (standing > neutral? explicit ally? open port?). Must be defined before death flow is implemented.

**Starter ship acquisition at respawn:**
Is the starter ship given, loaned, or purchased at respawn? If purchased, what credit floor exists to guarantee the player can always afford it? The economy must guarantee the player cannot be stranded without a replacement path. This is a floor-setting question for the economy, not a death mechanics question — but it must be answered before death flow is built.

**Hot-hull confirmation at death:**
If the player dies while flying a captured hull before port registration, the owning faction receives confirmation the hull is destroyed. Whether this closes the hot-hull standing consequence (the hull is gone, no further risk) or escalates it (destruction of a faction asset is a worse outcome than return) must be defined. The capture flow decision log flagged this as open and it remains open.
<!-- complete -->
