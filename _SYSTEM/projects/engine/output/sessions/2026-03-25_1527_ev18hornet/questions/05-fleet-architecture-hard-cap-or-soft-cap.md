# Fleet Architecture: Hard Cap or Soft Cap?

*Generated: 2026-03-25 15:44 | Question 5 | 180s | Mode: ev18hornet*

## Decisions

**Fleet size is capped by fighter bay slots on the player's hull, not by a command rating stat.**

The cap mechanism is physical and visible. A shuttle has no fighter bays. A heavy freighter has two. A capital ship has eight. The constraint is the ship, legible from the hull before any menu is opened. Command rating as a named pilot stat is rejected — it adds an abstraction layer EV did not need and that a first-session player cannot read without a tooltip. Max's desired outcome (ship tier produces a distinct and growing fleet power signal) is fully delivered by hull architecture. The progression is in the ship class, not a number attached to the pilot.

**Fleet composition visible at a planet functions as a deterrence signal to the faction raid calculation.**

Escorts docked at or patrolling a settlement contribute to that settlement's visible threat profile. Faction raid scale — number of ships dispatched, aggression tier — is partially derived from the player's demonstrated fleet strength at that location. A player who parks escorts at their settlement is not decorating. They are communicating deterrence to the faction simulation. This is not a guaranteed deterrent, but it is legible cause-and-effect: fleet investment produces faction response reduction as an emergent outcome, not a designer-authored buff. This interaction must be part of the raid calculation from the moment fleet escorts are functional.

**A captured ship cannot be added to the player's fleet immediately. It requires a port run first.**

This is a deliberate departure from EV's immediate-capture behavior. The port run is the mechanic that creates the hot-hull window. The faction that owned the captured ship registers the loss. From capture to port registration, the player is flying a hull the faction system knows is missing. That window is pressure the system generates without designer authorship — every second in transit is earned risk.

**Capturing a faction ship is a standing trigger event for that faction.**

The standing consequence is not a hidden penalty. It must be legible at the moment of capture or immediately after: a bar contact, a nav message, a faction comm acknowledging the loss. The player must be able to point to a specific moment and say "I knew this was going to cost me standing." Standing that moves before the player understands why it moved is the exact pattern already ruled out. The faction provenance of a captured hull — which faction, what the standing cost will be, whether there is a registration option at port that reduces or redirects the penalty — must be surfaced before the player commits to the port run.

**Fighter bay AI scope is a separate decision from the cap mechanism, and must be answered per milestone.**

The cap mechanism (hull slots) is an afternoon of design work. The escort AI required to make each slot meaningful — formation behavior in 2D space, atmosphere dive execution, flat-poly terrain navigation, re-emergence sequencing — is a milestone-sized task the first time it is built, and must be re-validated for each capability added. Every ship in the fleet is a separately validated AI agent. This scope does not scale as a multiplier on the cap number.

The fleet milestone (M6) must specify: how many escort ships have working AI at ship-off, what behaviors are included, and what is deliberately deferred. A capital ship hull with eight bay slots is not eight functional escorts unless eight escorts are scoped. The milestone definition must reflect the actual AI count, not the theoretical cap.

## Open Questions

- **Fleet AI milestone scope:** At which milestone does the first escort ship have working AI with formation behavior in 2D space? This answer determines whether fleet is M6 content or whether fleet bays are M6 architecture with AI populating them later.
- **Atmospheric escort behavior:** Escorts that follow the player into atmosphere are a distinct AI capability from 2D space formation. At what milestone does escort atmosphere-dive execute, and is it in scope for the same milestone as 2D escort AI?
- **Port run registration options:** Does registering a captured ship at port offer the player choices — pay a bribe to clear the standing hit, flag it as salvage for partial mitigation, or accept the faction consequence — or is the standing cost fixed on capture?
- **Hot-hull faction response:** If the player is interdicted while flying the captured hull before port registration, is the hull itself the trigger for elevated hostility from the owning faction, or only the standing value? Behavior must be defined before capture flow is implemented.
<!-- complete -->
