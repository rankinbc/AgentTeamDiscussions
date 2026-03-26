# Transcript: Fleet Architecture: Hard Cap or Soft Cap?

*Generated: 2026-03-25 15:44*

## Round: PROPOSE

### Max (atmospheric flight advocate)

Fleet cap is a flight feel question wearing an economy hat. Don't let it get answered purely by the systems team.

Here's why it matters to me: your ship is the thing you *fly*. Command rating as soft cap means ship tier = atmospheric capability = the shuttle handles like a drunk seagull and the heavy fighter carves. That's not balance flavor — that's the reason to upgrade. If command rating gates fleet size, then flying a better ship *feels* like more power in two directions: tighter rolls in atmosphere *and* more hulls backing you up. That's a clean design signal.

Hard cap collapses that. It says "five ships is five ships regardless of what you're flying." Less interesting in the spreadsheet, and it kills the progressive feel of arriving over your settlement in a capital ship with a real wing versus a shuttle with a buddy.

On captured ships needing a port run: yes, and I'd argue that port run should go *through atmosphere* if the ship is atmosphere-capable. Capturing a faction heavy fighter in 2D space and then having to fly it down yourself — in an unfamiliar hull with different mouse response — that's earned content. Different mass, different roll rate, different altitude behavior. The capture *becomes* a flight experience, not just an inventory transaction.

My agenda item: before we finalize fleet architecture, we need to define whether ship tier produces distinct atmospheric flight profiles. If it doesn't, the command rating soft cap loses half its meaning.

### Ren (emergence systems theorist)

Max is right that flight feel and fleet architecture are entangled, and that's exactly the systems interaction I want to flag.

Soft cap via command rating creates a dependency chain: **ship tier → command rating → fleet ceiling → settlement defense density → raid survival probability**. That chain runs all the way through the emergence loop we've already committed to. A hard cap severs it. You arrive over your settlement in a capital ship with the same fleet you had in a shuttle — the progression signal collapses exactly at the moment it should peak.

But here's what I want to add: fleet size needs to interact with the **raid response calculation**, not just exist as a prestige metric. If a faction's decision to send 3 raiders vs 7 raiders is partially derived from your visible fleet strength at the planet — what's docked, what's in system — then fleet size becomes active intelligence, not passive accumulation. Players who park escorts at their settlement aren't just showing off. They're communicating deterrence to the faction system. That's an emergent situation the designer didn't author.

On captured ships: port-run-required is correct, and not just for flight feel reasons. An unregistered capture sitting in your fleet is a faction standing event waiting to happen. The faction that owned that ship *knows it's missing*. If the port run takes time, and factions track ship loss, you create a window where the player is flying a hot hull. That's pressure the system generates. Immediate capture turns piracy into inventory management.

The standing interaction for captured ships: has anyone flagged this as a faction standing trigger? It should be.

## Round: CRITIQUE

### Vera (EV systems historian)

**[COUNTER - Vera (EV systems historian)]**

Before this discussion bakes in "command rating" as the soft cap mechanism, someone should note that EV didn't have a command rating. It had **fighter bays** and **economics**.

Your carrier-class ship had physical bay capacity. Fighters docked in those bays. You hired freelance escorts with credits and kept them with credits. Fleet size was capped by what your hull could physically carry plus what your income could sustain — not a hidden stat. Both constraints were legible without opening a menu.

That distinction matters. Fighter bays are *visible geometry*. A command rating is an abstraction layer. When EV's economy was "simple enough to understand in one session but deep enough to optimize for 100 hours," it was because the constraints were physical and traceable, not statistical.

Max is describing the right outcome — ship tier producing real progression signals in fleet capability — but the EV mechanism that delivered it was hull architecture, not a rating. A shuttle has no bays. A heavy freighter has two. A carrier has eight. The progression is the ship, not a number attached to the pilot.

My flag: if command rating is introduced as a named pilot stat, you're adding a layer EV didn't need. If it's shorthand for "ships with more bay slots allow larger fleets," that's just EV's actual system, and you should call it that.

On capture: EV let you fly captures immediately with sufficient crew. The port-run is a new mechanic. It may be correct. But be honest that it's a departure, and make sure the faction standing trigger Ren described justifies the friction before it's committed.

What did EV's fighter bay capacity actually look like per ship class? That's the reference that should anchor this decision.

### Nadia (new-player experience advocate)

Vera just made my argument for me and I want to put a name on why it matters for first-session players.

**Fighter bays are a tutorial you don't have to write.** A new player looks at their shuttle, sees no docking bay, and understands the constraint. They don't need a tooltip. They don't need a mentor NPC. The hull *is* the explanation. Command rating is the opposite — it's a number that requires a system reveal before it communicates anything. I've watched players bounce off abstraction layers like that in the first fifteen minutes. They don't know what they don't know, so they don't know to look.

Max's outcome is right: ship upgrade should feel like fleet power expanding. But Vera's mechanism delivers it more cleanly for a player who hasn't read the design doc.

On capture: I'm less worried about the port run friction than I am about whether the *consequence* is legible when it hits. Ren's "hot hull" framing is genuinely exciting — but only if the player understands *why* their standing is moving. If a captured ship triggers a faction standing event the player didn't anticipate, that's not earned pressure. That's the exact standing-punishes-before-you-understand-what-you-did-wrong pattern we've already flagged as a hard no.

The port run is fine. What needs to land alongside it: a clear signal that the captured ship has a faction provenance and what that means for you right now. One line of bar dialogue. One nav contact. Something the player can point to later and say "I knew that was coming."

## Round: EVALUATE

### Soren (solo dev scope warden)

The cap mechanism debate is downstream of a question nobody has answered yet: **how many ships need functioning AI at each milestone?**

Fighter bays are the right architecture — Vera is correct, and it eliminates an abstraction layer. But whether the cap is "hull slots" or "command rating," every ship in your fleet needs pathfinding, formation behavior, target acquisition, and atmospheric layer handling. That cost is identical either way. The cap mechanism is two hours of design work. The AI for each fleet slot is weeks.

My scope flag: **fleet escort AI is a full feature, not a progression modifier.** A shuttle with one escort and a capital ship with eight escorts isn't a scaling multiplier. It's eight separately-validated AI agents that must hold formation in 2D space, execute the atmosphere dive, navigate flat-poly terrain, and re-emerge. Each capability is a milestone-sized task the first time you build it.

The captured-ship-as-standing-trigger is genuinely good emergence design. It's also a second feature hiding inside what looks like a fleet question. The port run, the faction provenance signal, the standing event — that's a session of work minimum, and it requires the faction standing API from M5 to exist first.

My recommendation for this discussion: **separate the mechanism decision from the fleet AI scope decision.** Fighter bays — fine, decide that now. Then answer: at which milestone does the *first* escort ship have working AI? That answer will tell you whether fleet is M6 content or M8 content. The mechanism doesn't matter if you don't know when you can afford to build it.

<!-- complete -->
