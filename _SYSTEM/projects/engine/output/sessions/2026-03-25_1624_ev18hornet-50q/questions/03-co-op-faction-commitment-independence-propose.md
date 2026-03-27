### Ren (emergence systems theorist)

The question underneath this question is: *what does the settlement's faction alignment become when two players have divergent commitments?*

Independent paths are obviously correct from a player agency standpoint. Linking them collapses the design space before any interesting situations can emerge. But independence doesn't resolve the harder problem — the raid system needs a single faction-heat value per settlement to determine who shows up in your atmosphere. Two players with opposing commitments create a standing input that the raid trigger can't currently interpret.

Here's what I want to map before we decide API shape:

**The emergence chain at stake:**
Faction standing → settlement raid frequency/intensity → atmospheric defense engagement → on-foot combat aftermath

If Player 1 is Confederation-committed and Player 2 is Rebel-committed, both raid pools are simultaneously hot. That's not a problem — that's the most interesting situation this game can generate. A settlement under pressure from two opposing factions, where both players have different atmospheric intercept priorities, creates *exactly* the kind of player situation the designer didn't author.

The API question then becomes: does the raid system read individual player standing or a *settlement alignment value* that aggregates from both?

I'd push toward a settlement-level faction heat derived from *both* players' standing combined — not averaged, combined, so high commitment on both sides means maximum raid pressure from all directions. That's the emergent output that matters.

What I need from this discussion: how raid targeting currently reads faction data, and whether the commitment NPC trigger creates any settlement-level flag we can build on.

### Max (atmospheric flight advocate)

Ren nailed the emergence chain and I want to pull on one thread hard: **if both raid pools are simultaneously hot, the atmospheric layer becomes the most loaded space in the game.**

That's not a side effect. That's the payoff.

Picture it: you've built your settlement to Colony tier. You fly up to altitude and bank a long turn over your own build — the SimCopter moment, earned. And then you're getting Confederation intercepts from the north AND Rebel patrols sweeping from the south because your co-op partner went the other way. The atmosphere above your settlement is *contested airspace*. That's not a problem to solve in the API design. That's the reason the atmospheric layer exists.

So yes — independent commitment paths, full stop. Don't link them.

On Ren's settlement-level faction heat question: I'd implement it as two separate heat values per faction pool, not aggregated. Let the raid system read them independently. Why? Because combined heat collapses into a single number that loses the directional information the atmospheric spawn system needs. You want to know *which vector* the Confederation fighters come from versus the Rebel patrol route. Combined heat tells you "lots of raids." Independent heat values tell you "flanked from both sides" — which is a completely different atmospheric intercept geometry.

The bank-and-roll defense engagement has to reflect that geometry or the flight layer becomes random. Two heat values. Two spawn axes. The player reads the sky and knows what's coming.

That's the atmospheric layer earning its place as primary gameplay space, not a transition corridor.


<!-- complete -->
