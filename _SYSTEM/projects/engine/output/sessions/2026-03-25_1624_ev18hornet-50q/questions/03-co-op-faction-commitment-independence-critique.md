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


<!-- complete -->
