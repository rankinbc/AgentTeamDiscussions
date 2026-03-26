# Transcript: On-Foot Combat Depth

*Generated: 2026-03-25 15:53*

## Round: PROPOSE

### Ren (emergence systems theorist)

**On-foot isn't a genre question. It's an emergence chain question.**

The faction standing → raids → atmospheric defense → on-foot combat chain already tells us what on-foot combat needs to DO: it's the resolution layer when the faction pressure chain reaches physical space. That constrains the answer more than scope concerns do.

Three situations where on-foot combat earns its existence:

**Boarding.** Ship capture is already decided and it's a standing trigger event. If the boarding itself is a non-event — walk through a corridor, press interact — you've removed the risk that makes capture meaningful. The cost structure (hot-hull window, faction response, port run requirement) only lands if taking the ship felt dangerous. Minimal FPS is enough here. Enough resistance to feel earned, not enough to be a separate game.

**Raid breach.** If raiders survive the atmospheric layer and land, something has to happen. Currently that's just building destruction by external actors. An on-foot defense option — small, optional, high-risk — transforms that from a spectator event into a player decision. Do I fight for this building or let it fall and absorb the tier regression?

**Exploration.** Derelicts, stations, bars — walking sim is correct here. No combat needed unless the space has faction logic attached.

**What I'd flag as dangerous:** deep cover systems, melee, and full FPS animation investment are all self-contained — they don't feed back into standing or faction pressure. They consume solo dev time without strengthening the emergence chain.

Recommendation: deliberately minimal combat, purpose-built for boarding friction and raid breach defense. Walking sim everywhere else. Scope stays tight; the chain stays intact.

### Max (atmospheric flight advocate)

**Ren's emergence chain framing is exactly right, and I'll add the atmospheric lens to it.**

The reason on-foot defense works as a concept isn't FPS depth — it's because you've already *flown over this settlement*. You know that tower. You watched it get built from altitude. The SimCopter payoff is the emotional engine behind caring whether a building stands. If on-foot combat is minimal but you've earned the aerial view, the stakes are already loaded before you land.

That's the sequence: fly over at altitude, see the skyline you built, dive in to defend it. The on-foot layer is the *landing* of that arc, not a separate arc. If boarding and raid defense are purpose-minimal — enough friction to feel earned, not a cover-shooter — the atmospheric entry is still the climax.

**What I'd flag as a scope threat:** any on-foot investment that happens *instead of* flight feel iteration. Deep melee, complex cover geometry, full animation rigs — these consume exactly the same solo dev time as mouse-flight tuning, bank-and-roll refinement, and the low-altitude terrain pass that makes settlements readable from 200 meters. If those flight feel hours go to on-foot systems, you ship a walking sim with a flight game attached instead of the other way around.

**Concrete position:** walking sim in bars and exploration, minimal FPS for boarding friction and raid breach. Cap on-foot combat scope explicitly in the settlement milestone so it cannot expand and eat atmospheric layer polish time. That's where the differentiator lives.

## Round: CRITIQUE

### Vera (EV systems historian)

**EV never had on-foot combat. That's not a limitation they worked around — it was a design choice that held.**

Boarding in EV was a stats check after you'd depleted shields. You pressed a key. Numbers resolved. The *tension* came from the hot-hull window, the faction response, the port run you had to survive. Ren's framing that boarding needs "enough resistance to feel earned" assumes FPS friction is the only mechanism for earned difficulty. EV disproves this. The danger was positional and economic, not corridor-shooter danger.

What I'd flag: both Ren and Max have accepted that on-foot combat exists for boarding. That's the assumption worth testing. If boarding resolves as an atmospheric or 2D-space event — deplete shields, dock alongside, crew check, result — you preserve the standing consequences without building an FPS boarding system. The cost of capture is already designed. You don't need another cost layer unless the existing one fails to land.

**Where I'd defend on-foot depth:** raid breach defense is the one case where on-foot combat does work the others can't. You've already seen the building from altitude. You've chosen to land. The decision to fight or absorb the tier regression requires you to be *present* in a way that abstracted resolution cannot replicate. That's worth minimal FPS investment.

**The scope boundary I'd draw:** one mechanic, two purposes — raid defense and exploration. Boarding stays abstracted. No melee. No cover geometry. The bar is never hostile territory.

Don't import FPS boarding because it *feels* more modern than a stats check. EV's abstraction was the feature.

### Nadia (new-player experience advocate)

**Vera's abstracted boarding is correct. I want to explain why from the player journey side.**

A new player's first boarding attempt is already overloaded: they've just survived a 2D space fight, they have a hot hull, they don't fully understand standing yet, and now there's an FPS corridor. That's three systems demanding simultaneous comprehension. The abstracted stats check asks one question — "did you weaken them enough?" — which a new player can answer. A boarding FPS asks a dozen questions at once with no scaffolding.

Keep boarding abstracted. The earned difficulty Ren wants is already in the approach.

**Where I push back on Max slightly:** the sequence he describes — fly over, see the skyline, dive in to defend — is a *later-session* fantasy. First session, there's no skyline. The on-foot layer in session one is the bar, building placement, and exploration. If the on-foot combat system only becomes meaningful in session five, it cannot be what we use to hook players.

**What on-foot actually does in session one:** it makes the bar feel real. Walking through a door, seeing NPCs occupy space, sitting at a table to take a mission — that's the core fantasy landing before anything is built. That's worth investment.

**My position:** walking sim first, minimal raid defense second, boarding abstracted permanently. The bar's *atmosphere* is the on-foot hook, not combat. Make the bar feel like a place. Everything else follows from that.

Don't build the defense mechanics before the space feels worth defending.

## Round: EVALUATE

### Soren (solo dev scope warden)

**"Minimal FPS" is not a scope category. It's a wish.**

Let me put numbers on what the table has been calling minimal. Walking sim — movement, collision, interaction triggers, bar NPC proximity — is 3–5 weeks in Godot 4 with flat-poly assets. You get the bar, exploration, building placement. That's real.

The moment you add combat — even "minimal" — you've added: weapon model, projectile or raycast system, enemy AI state machine (idle/alert/attack/dead), hit feedback, death state, sound design for weapon fire, damage tuning, at least one balance pass. That's 10–16 weeks minimum, solo. Flat-poly helps with enemy art. It does not help with AI, hit detection, or balance.

So the actual decision is: walking sim (3–5 weeks) or FPS (10–16 weeks). There is no third option.

Given that framing, I'd resolve the open debate this way:

**Boarding: abstracted. Permanently.** Vera is right. The standing cost, hot-hull window, and port run are already the danger. Adding 10–16 weeks of FPS to make boarding feel "earned" when EV proved a stats check works is sunk cost before you've shipped a core loop.

**Raid defense: the one FPS justification.** It does work the abstraction can't — you're present, you chose to land, the building matters. But it gets one scope slot, not a system that expands.

**Bar and exploration: walking sim. Full investment here.**

Flag for the record: if boarding ever gets reopened as FPS, that's a milestone in its own right, not a feature added to an existing milestone.

<!-- complete -->
