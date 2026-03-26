# Transcript: Co-op Faction Commitment Independence

*Generated: 2026-03-25 16:33*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

Independent paths are correct. That's the easy part. Here's what concerns me about where this discussion is heading.

**Ren's combined-heat proposal breaks EV's core feedback loop.**

EV's faction system worked because standing was *legible*. You attacked a Confederation ship, your Confederation number moved, you understood why. The system's depth came from that traceability — players could reason about consequences before acting. Combine two players' standing into a single settlement-heat value and you've created a number that neither player can trace back to their own choices. Standing becomes weather, not consequence.

Max is closer with independent heat values per faction pool. But I want to push harder: before we design any settlement-level faction heat API, we need to know whether the raid system *needs* a settlement value at all, or whether it should simply query each committed player's standing directly at spawn time.

In EV, the game always knew whose ship you were flying. Standing was per-pilot, not per-spaceport. The spaceport's faction affiliation was authored, fixed — it didn't aggregate anything dynamically.

What happens if raid spawn reads Player 1's Confederation standing and Player 2's Rebel standing independently, with no settlement-level aggregation layer? You get the flanked-airspace outcome Max described, without inventing a new data concept.

**The question I want answered before API shape gets decided:** is settlement-level faction heat a necessary architectural concept, or is it complexity we're adding because two-player co-op *feels* like it should require a new abstraction?

EV didn't have that abstraction. It had pilots and consequences.

### Nadia (new-player experience advocate)

Vera's question is the right question, and I want to answer it from a different angle: **the player experience test, not the architecture test.**

A new player doesn't know what "settlement-level faction heat" is. They know what they see — ships coming from the north, ships coming from the south, and their co-op partner saying "I think I made the Rebels angry." That's the read they need. That's what makes the system feel like consequence rather than weather.

So Vera's alternative — raid spawn reads each player's standing directly, no settlement aggregation — passes the legibility test that combined heat fails. Player 1 can trace the Confederation intercepts to their own choices. Player 2 can trace the Rebel patrols to theirs. Neither player is punished by math they can't see.

What I want to flag for first-session design specifically: **the commitment NPC must not appear before a player understands what they're choosing between.** Standing ≥ 60 AND mission completed is a good mechanical gate, but there's an experiential gate underneath it — has this player *felt* the difference between factions before committing? If commitment arrives before that feeling lands, the choice is hollow. The NPC trigger condition is correct; the question is whether the path to 60 has given the player enough faction-flavored encounters to make the commitment meaningful.

Independent paths are obviously right. The co-op fantasy here isn't "we chose the same side." It's "we built something together and we're each defending it from different threats." That's the first-session promise the system needs to be able to deliver.

## Round: EVALUATE

### Soren (solo dev scope warden)

**The discussion has converged correctly on the architecture. What nobody has priced is the build sequence.**

Vera's proposal — raid spawn reads each player's standing directly, no settlement aggregation layer — is the right answer *and* the cheaper answer. That's unusual. Lock it.

But here's the scope problem underneath this question: **co-op is Milestone 8. Faction standing is Milestone 5.** The API you're designing today needs to work for a single player first, then extend cleanly to two players three milestones later without a rewrite.

That means M5 should ship with:
- Per-player faction standing (single player, fully functional)
- Commitment NPC trigger: standing ≥ 60 AND mission completed (already decided)
- Raid spawn reads the *active player's* standing — singular, not plural

The co-op extension point is: at M8, raid spawn queries each connected player's standing independently. No new data concept required. No settlement aggregation layer. The architecture Vera described is already the correct M8 shape — you just don't build the two-player read path until M8.

**What I want to flag before Max's two-spawn-axis geometry gets designed:** directional spawn axes tied to faction heat are a non-trivial atmospheric system. That's M2 atmospheric layer work intersecting with M5 faction data intersecting with M8 co-op state. Building that intersection point now is how scope compounds.

The question to answer today: does M5 require *any* co-op faction API, or is M5 strictly single-player standing with a clean extension contract documented for M8?

That's the agenda.

<!-- complete -->
