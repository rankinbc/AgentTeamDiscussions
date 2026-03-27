# Transcript: NPC Settler Arrival Model

*Generated: 2026-03-25 18:34*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

Both Max and Ren are describing visible agents as the high-fidelity option. I want to register skepticism about that framing before the group anchors on it.

EV never rendered individual colonists. Spöbeck didn't have visible farmers walking between buildings. What made those planets feel inhabited was *proxy signal density* — ship traffic in the system, Bar contact count, mission pool depth, equipment availability. You read population as consequence, not as agent. The aerial legibility of "this place is alive" came from ship density on the galaxy map and Bar occupancy on landing, not from figures moving at 500 meters.

The relevant authenticity question is: **what does EV's design heritage say about population representation?** The answer is that EV abstracted population completely and produced 100 hours of optimization depth anyway. The standing system that's been built over Q3 through Q29 follows that same principle — faction attention scales with a counter, not with visible agent count.

Ren's raid targeting concern is the real flag. The moment settlers become visible agents who can be killed, the assault raid AI needs a new read path — population targeting versus infrastructure targeting. Q12 explicitly deferred rational targeting. Visible agents reopen that question with higher stakes and no playtest data to calibrate against.

My agenda item: **establish whether "feels inhabited from altitude" requires visible agents or whether proxy signals already in the design can carry that weight.** Specifically — does the flat-poly ring geometry, patrol density at the galaxy layer, and ship traffic already produce aerial legibility? If yes, visible agents are scope cost without design gain.

The SimCopter payoff Max describes is real. The question is whether it requires rendering settlers or rendering *evidence of settlers*.

### Nadia (new-player experience advocate)

Vera's proxy signal argument is persuasive for someone who already knows how to read EV's vocabulary. A new player doesn't. Ship traffic density and Bar contact count are legible *after* you've learned what they mean. For someone in session one, those signals are noise.

This is the first-session test: a new player descends to their settlement and it feels empty. Why? They don't know. When does that change? They don't know. The population counter is invisible by definition — it's a system that exists but cannot be perceived. That violates the principle we've been building toward across every standing tooltip and comms intercept decision: consequence must be traceable to player-recognized action.

Max's SimCopter moment is real and it matters specifically *because* it's the first legible proof that something they built persists and lives. But I want to separate the payoff from the mechanism.

The question isn't visible agents vs. counter. It's: **what's the smallest legible change that communicates "threshold crossed" from altitude?**

Individual moving figures may be unreadable at `ATMOSPHERIC_FLOOR_ALTITUDE` in flat-poly. But a new building type appearing — a trade post, an antenna, something structurally distinct — could read from altitude as evidence of settler presence without requiring NPC pathfinding.

Organic arrival via visible *geometry change* rather than visible *agent* preserves the discovery moment, stays within the established aesthetic, and avoids reopening Q12's deferred raid targeting question.

Ren's emergence chain works either way. The threshold event produces faction attention escalation regardless of whether it's expressed as agents or structures.

## Round: EVALUATE

### Soren (solo dev scope warden)

Four options are on the table. I want to put build costs next to each before anyone anchors.

**Population counter only.** One integer field, one threshold check. Faction attention scales with it. No aerial legibility. Build cost: one day. EV ran on this model and produced deep play.

**Visible settler agents.** Flat-poly character meshes, patrol paths inside settlement geometry, some form of idle/movement state, collision with buildings. Raid interaction TBD — can they be killed? Do they flee? If yes, that's a health model, a flee state, and a new read path for assault AI that Q12 explicitly deferred. Build cost: **4–8 weeks minimum** for a functional NPC agent system in a new layer. This is a separate game feature, not a settlement extension.

**Geometry change at threshold.** A new structure appears — trade post, antenna, communal structure — when population crosses the unlock value. Flat-poly mesh, authored once, placed at settlement time. Reads from altitude. No pathfinding. Doesn't reopen Q12. Build cost: 2–4 days per new building type, which is already in the per-type authoring budget.

**Explicit placement.** Player places personnel slots as buildings. Population is building count. No separate counter, no new system. Arrival is a player action. Build cost: folds into existing building placement.

The geometry change option does what Nadia described — legible threshold signal from altitude, no agents, no Q12 regression risk.

**Decision-forcing question:** Does the SimCopter payoff require *movement*, or does it require *evidence of change*? Answer that and the scope follows directly.

<!-- complete -->
