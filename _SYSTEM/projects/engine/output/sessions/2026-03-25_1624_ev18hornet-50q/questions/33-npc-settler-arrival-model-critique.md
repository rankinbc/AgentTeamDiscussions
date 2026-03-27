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


<!-- complete -->
