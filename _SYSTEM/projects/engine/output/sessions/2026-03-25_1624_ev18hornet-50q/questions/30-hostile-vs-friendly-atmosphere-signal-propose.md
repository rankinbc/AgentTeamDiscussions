### Max (atmospheric flight advocate)

The signal problem is real, but I want to name the trap before we design into it: **if we solve this too well, we make the atmosphere optional.**

Right now the open question from Q22 — galaxy map option A/B/C for non-starting systems — is technically unresolved. But the more interesting question underneath it is: *what should the player NOT be able to know from space?*

The static ring from Q29 gives spatial confirmation — inside/outside, threshold marked. That's correct and ships cheap. But a ring that color-shifts by faction standing is a different thing: it's a dashboard. It lets you orbit at safe altitude reading threat state without committing your hull to the approach vector. That's not Hornet. That's Kerbal mission planner.

My position: **the approach is the information.** You dive, you read the intercept geometry, you feel whether the patrol spacing is loose or tight. That's the kinesthetic standing readout we decided on back in Q10 — modified patrol approach vectors as atmospheric tell. The galaxy layer should show *that something is there.* How hostile? Go find out.

The specific open question I want to set: does the galaxy map signal for non-starting systems need to be faction-identified, or is faction-neutral threat presence (ships on map, no affiliation shown) the correct fidelity ceiling? Because faction-identified from orbit is Option B+ work, and it might be solving a problem that the dive itself already solves better.

What does the descent *feel like* when you're flying into hostile space versus friendly? That's where I want to land.

### Ren (emergence systems theorist)

Max is right about the trap, but I want to sharpen the systems framing.

The issue isn't information quantity — it's information *source*. There are two possible architectures here:

**Architecture A:** The galaxy map reads atmosphere and reports faction state to the player. Standing system and galaxy signal are parallel outputs. They work independently.

**Architecture B:** The player's standing ledger IS the galaxy signal. You know your Confederation standing is 28. You know that system is Confederation. You know what you're flying into. The approach confirms what your choices already told you.

Architecture B is where cross-layer interaction actually lives. Your faction history — accumulated across The Bar, missions, hull captures, combat — becomes your atmospheric intelligence. The standing system doesn't just produce raids; it produces *knowledge*. That's the chain we want: past choices → standing → approach read → intercept geometry → dirtside consequences.

Architecture A breaks that chain. If the map tells you faction ownership independent of your standing, you're reading a HUD, not your history. The approach becomes confirmation of information you already had for free.

For non-starting systems: faction-neutral ship presence on the map is the correct ceiling. Max is right that faction-identified from orbit is solving a problem the dive solves better. But the reason it's correct isn't aesthetic — it's that faction identification from orbit would let players route around their standing history instead of confronting it.

One flag: this only works if the standing UI is readable. Players need to be able to cross-reference "my Confederation standing is X" against "I'm approaching a Confederation system." If that cross-reference requires menu diving, the elegant architecture becomes an obscure one.


<!-- complete -->
