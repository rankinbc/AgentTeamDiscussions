### Max (atmospheric flight advocate)

The question that matters to me isn't micromanagement load — it's what the settlement looks like from 500 meters.

Organic arrival wins on the aerial payoff. Here's why: if settlers arrive at a threshold, their presence is *news you discover by flying over*. You come in on approach, and there are figures moving between buildings. That's the SimCopter moment. You built something, you left, you came back from altitude, and it's alive. Explicit placement means you already know exactly what's there — the discovery is gone before you ever descend.

That said, the organic model has a scope question that matters architecturally: what does "settler" actually represent in a flat-poly game? If it's a visible NPC agent with a patrol path inside your settlement boundary, that's a different build than if "settlers" is just a population counter that affects building unlocks and faction attention. The aerial legibility question depends on which of those is true.

My agenda item: **decide what a settler IS before deciding how they arrive.**

Specifically — does settler presence produce visible geometry or movement that reads from `ATMOSPHERIC_FLOOR_ALTITUDE` upward? If yes, organic arrival is the correct model and the threshold event creates a genuinely discoverable moment from the air. If settlers are abstracted population counters with no 3D representation, the organic/explicit distinction is an economy design question and I don't have a strong opinion either way.

The atmospheric layer needs the settlement to read as inhabited. How we get there matters.

### Ren (emergence systems theorist)

Max identified the right dependency. I'll extend it into the emergence chain.

The settler model isn't just an economy question — it's a **raid targeting question**. If settlers have 3D representation, they become potential raid targets, which creates a new read path for assault-scale AI: attack population vs. attack infrastructure. That's a different tactical problem than what Q12 decided. Q12 deferred rational targeting because the query path architecture wasn't specified. If settlers are visible agents, that question resurfaces with higher stakes.

The emergent systems flag here: **organic threshold arrival creates a signal the player doesn't control**. Population crosses threshold → faction attention escalates → raid frequency increases → standing pressure mounts. That's the chain producing situations the designer didn't author. Explicit placement gives the player a throttle on faction attention escalation, which caps emergent pressure.

My position: organic arrival is correct for the emergence chain, but Max's question about representation is load-bearing. The decision branches:

**Population counter:** Organic arrival is a stat change. Faction attention scales with the counter. No new geometry, no raid targeting complexity. Low scope cost, functional emergence chain.

**Visible agents:** Organic arrival creates the SimCopter aerial moment Max describes. But now settlers can be killed, can flee, can be absent after a raid. Raid consequences become readable from altitude without checking a UI. Settlement feels genuinely damaged, not just statistically degraded.

The visible agent version produces emergent situations the counter version cannot. But it also requires the building interior dimensions question from Q24 to be resolved first — pathfinding scope inside settlement geometry applies to settlers too.

Decide what a settler IS. Then the arrival model follows.


<!-- complete -->
