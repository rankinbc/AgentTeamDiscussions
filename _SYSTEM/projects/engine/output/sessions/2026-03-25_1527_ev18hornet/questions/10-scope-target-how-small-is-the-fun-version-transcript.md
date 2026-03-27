# Transcript: Scope Target: How Small is the Fun Version?

*Generated: 2026-03-25 16:00*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

**Both proposals are correct on numbers and wrong on justification.**

Ren's 4 buildings and 4 systems survive scrutiny. Max's silhouette contract is right. But neither of them has stated *why EV felt infinite with 50 systems*, and without that answer you cannot know whether 4 systems is enough.

EV felt infinite because **every system had a faction logic that preceded the player's arrival.** The Confederation didn't materialize when you jumped in. It was already there, already in conflict, already with opinions about your hull. The player was reading a world with history. That's what created depth, not system count.

Four systems is enough *only if* each system has a faction disposition baked before session one. If two of the four systems are placeholder geography waiting for authored content — world geometry without faction logic — you do not have a 4-system game. You have a 2-system game that crashes the emergence chain at step one.

The building count question Ren answered correctly, but incompletely. The number is 4. The missing constraint: **each building must be destructible by a faction with a legible reason.** Raiders who destroy a Generator are protecting a competing economic interest. If the raid targeting logic cannot articulate *why* it chose that building, the player cannot read the consequence. Arbitrary destruction is not emergence — it is random damage with faction paint on it.

EV's economy was readable in one session because every action had an attribution chain. That's the test: can the player trace *why* after every consequence? That's what the minimum scope must preserve.

### Nadia (new-player experience advocate)

Vera is right but she's framing it for an EV veteran. Let me translate it for someone who has never heard of Escape Velocity.

The reason 4 systems works isn't system count — it's that the **starting system has to do all the onboarding in one session**. The player doesn't experience "the galaxy." They experience one system, one faction with a color and a behavior they can observe, and one bar. If that first system doesn't teach what faction standing *is* through visible consequence before the player jumps, then session two drops them into contested space without a conceptual model for what's happening to them.

This is my actual scope stake: **the starting system is a separate design artifact from the other three systems.** It needs at least one standing-feedback moment that the player didn't cause — a faction patrol that ignores you, then notices you, then changes behavior. Not a tutorial tooltip. A readable behavior shift.

On buildings: I'd reverse Ren's priority order for a new player. Build the Landing Pad first — it's the most legible "I made a thing" moment from altitude. Generator and Comm Tower are invisible until they're gone. The first building has to *reward the player for looking down.* That's the SimCopter hook. If the first thing they place reads as a gray box from 400 meters, the flat-poly aesthetic just failed its biggest audition.

Four buildings. Four systems. Three ships. But the starting system is doing 70% of the work, and it needs to be designed as such — not as system #1 in a list of four.

## Round: EVALUATE

### Soren (solo dev scope warden)

The numbers in this discussion are right. The sequencing argument is wrong.

Three ships, four systems, four buildings — that's not a scope target. That's a *completion target*. The question Ren, Max, Vera, and Nadia haven't answered is: **what is the first moment the loop is testable?** Because you cannot validate all four buildings against all four systems against all three ships simultaneously. You build in sequence. The question is which sequence.

Here's what I'm putting on the table:

**One ship. One system. Two buildings.** That's the first playable test. Not the first shipped milestone — the first moment you can ask "is this fun?" Shuttle in a starting system with a Generator and a Landing Pad. No raid targeting logic yet. No contested chokepoint. One faction patrol that changes behavior based on standing. The atmospheric dive loads a placeholder mesh. You fly over what you built. You land. You take a mission. You fly back out.

If that loop isn't fun, nothing Milestone 7 adds will save it.

The agenda I'm proposing: stop counting the minimum complete set and start sequencing the minimum *testable* set. Because every build estimate I've seen for "minimum viable" games that listed features instead of sequences ran 3x long. Four buildings sounds like four weeks. It's four weeks times four — state persistence, co-op sync, raid targeting, rebuild flow. Each building is a system, not an asset.

One question drives the rest: **what is the first day someone plays this and says yes?**

That's the real minimum.

<!-- complete -->
