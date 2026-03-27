### Ren (emergence systems theorist)

The right question isn't "what content volume feels infinite" — it's "what is the minimum surface area for the emergence chain to complete one full cycle?"

The chain is: standing mismanagement → raid → atmospheric defense → consequence → re-engagement. If a player can run that loop once and understand what happened and why, the game is fun. Everything else is depth added after proof.

My stake:

**Ships: 3.** Shuttle (respawn regression), Light Fighter (first consequence-bearing hull), one faction patrol class. The death consequence requires a visible loss gradient — Shuttle to Light Fighter is that gradient. A third ship (faction ship the player might capture) seeds the capture flow and hot-hull window without additional authored content.

**Systems: 4.** Starting system, two faction-territory systems, one contested chokepoint. This is the minimum geography that produces organic pressure — two factions with real territory that overlaps somewhere. Three systems collapses the contested space into a single binary. Five adds variety before the loop is validated.

**Buildings: 4 at Outpost tier.** Generator (economic target — destroys faction income competition), Landing Pad (logistics target — disrupts fleet replenishment), Comm Tower (intel target — destroys standing visibility), Defense Turret (the thing raiders destroy first to enable the others). Four building types gives raid targeting logic something to prioritize. Below four, targeting is effectively random. Above four before loop validation is scope that hasn't earned itself.

The open question this resolves: minimum Outpost building count is **4**, and each type must map to a raider motivation or it has no business being on the list.

### Max (atmospheric flight advocate)

Ren's 4-building Outpost is the right number **if every building has a rooftop silhouette readable from 400 meters altitude.** That's the constraint I'm adding, not a new building — it's a design contract on the ones already listed.

Here's why it matters for scope: the SimCopter payoff is flying over your own settlement and *recognizing it*. Generator, Landing Pad, Comm Tower, Defense Turret — those four have naturally distinct footprints. Generator is squat and wide. Tower is vertical. Landing Pad is a horizontal plane with a contrast color circle. Turret rotates. From altitude, in flat-poly, those four reads are actually **better** than twelve buildings that blur into terrain noise.

The scarcity is the feature. Four buildings means every absence after a raid is a named absence. You dive back in, bank left, and the Comm Tower isn't there. You know exactly what you lost. That's the SimCopter scar mechanic earning its keep.

On systems: I'm with Ren at 4, but I want one atmospheric constraint baked into the geography — the contested chokepoint planet should be the most visually distinct terrain color. Not for art reasons. Because when you're in the dive, reading geometry and color alone, you need to know you're somewhere that matters. One biome swap costs nothing in Godot ArrayMesh and does enormous work for atmospheric layer identity.

Ships at 3 is correct. The Shuttle has to *feel worse* to fly than the Light Fighter. If the bank-and-roll on the Shuttle is identical, death loses its regression signal entirely.


<!-- complete -->
