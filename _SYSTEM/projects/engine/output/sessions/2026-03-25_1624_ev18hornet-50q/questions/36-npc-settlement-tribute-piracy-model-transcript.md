# Transcript: NPC Settlement Tribute / Piracy Model

*Generated: 2026-03-25 18:47*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The question buried in this is: where does tribute collection happen?

If the answer is "click the system on the galaxy map and credits arrive" — that's atmosphere-bypass and I'm against it on principle. The whole point of this architecture is that consequences live in the layer where they're earned. You want dominance money? You descend. You show up. The settlement sees your hull at low altitude.

That's not a constraint — that's the SimCopter payoff running in reverse. Instead of watching your own city from above with pride, you're rolling in over someone else's with intent. Same kinesthetic reward, different emotional register. That moment — the long banking approach over a settlement you've claimed — needs to exist in 3D space at flight speed, not as a menu interaction.

So my position before we debate economic model details: tribute collection must require an atmospheric presence event. The player has to descend to the planet, fly over or land at the settlement. That presence event is the collection trigger. Not a timer, not a galaxy-layer transaction.

Two things I want the group to resolve before we go further:

One — does NPC settlement tribute require a new spawn type for the settlement, or can it ride the existing landing pad infrastructure? Because if we're authoring NPC settlements they need geometry legible from 500 meters, same constraints as player settlements.

Two — what does a dominated NPC settlement look like from altitude? That visual read is load-bearing for whether dominance feels real. If it's indistinguishable from a neutral settlement, the whole fantasy collapses.

Those are my blocking questions.

### Ren (emergence systems theorist)

Max is right that atmosphere-bypass breaks the three-layer contract. But I want to name *why* it breaks it, because that sharpens what we actually need.

The tribute collection trigger should be atmospheric flyover at low altitude — not landing, not a menu. Landing routes through the respawn anchor and docking infrastructure. Flyover is a separate event we already need for the SimCopter read. That's not a new system. That's using the existing atmospheric entry + altitude band to fire a settlement interaction event.

On Max's two blocking questions:

**Spawn type vs landing pad:** Tribute doesn't require a new spawn type if we treat NPC settlement geometry as the same two-state minimum already decided for player settlements — intact and degraded. The pad is optional. The flyover trigger is keyed to settlement presence at low altitude, not pad presence.

**Visual read from altitude:** I'd argue patrol *absence* is the primary legible signal that you've dominated a settlement. No faction escorts in the airspace, no intercept vector on approach — that silence communicates dominance emergently, without authored geometry. But a dominated settlement should probably carry one additional marker, something flat-poly and small, a flag or antenna state. One extra geometry variant per settlement type.

The chain I want to name explicitly: dominated settlement → patrol vacuum → rival faction now has a standing-neutral reason to raid and re-establish control → which generates standing movement for everyone involved. That's the emergence this system lives or dies on. Tribute collection isn't an economy feature. It's a raid provocation timer.

What standing condition gates dominance in the first place — is it Hostile band with the owning faction, or something else? That's the next question.

## Round: CRITIQUE

### Vera (EV systems historian)

Two things in EV's piracy model the discussion has already romanticized past the point of accuracy.

**First: EV's tribute was fleet-strength gated, not standing gated.** You demanded tribute by having enough firepower in-system to make the threat credible. Standing was the *consequence* of tribute, not the precondition. This design has inverted that relationship across every prior decision — standing as primary gate, fleet as secondary. That's not wrong, but it's a divergence that needs naming before the domination condition is specified. "Hostile band with the owning faction" is a standing answer to what was originally a capability question in EV.

**Second: Patrol absence is not a legible dominance signal.** In EV, you knew you'd dominated a planet because it said so on the planet card — discrete state, explicit display. Ren's "silence communicates dominance emergently" is seductive but breaks for new players and probably for veteran players on systems they haven't visited recently. Absence reads as "nothing happening" before it reads as "I did something." EV's legibility came from explicit state, not emergent negative space.

What Ren gets exactly right: tribute collection is a raid provocation timer. That's authentic. The income is the bait; the defense cost is the constraint; the standing movement from both sides is the drama. That chain is correct.

What Max gets exactly right: atmosphere-bypass breaks the layer contract.

The question I want answered before anything else: is domination a *discrete authored state* per NPC settlement, or does it emerge from standing values alone? That determines whether this system is buildable.

### Nadia (new-player experience advocate)

Vera's patrol-absence point is the one I care most about, and I want to push harder on it.

Absence as a signal only works if the player has a baseline to compare against. A new player descending on their first dominated settlement has no learned expectation of patrol presence — so the silence reads as nothing, not as "I did this." That's not emergence, that's legibility debt we've deferred to hour ten.

The discrete authored state question is the right question. But I'd frame it slightly differently: **the player needs a visual confirmation that something changed because of them.** Not because it teaches them EV's piracy model — they don't know that model. Because it closes the feedback loop on the action they took.

That visual marker Ren mentions — flag state, antenna variant — is load-bearing for new players in a way it isn't for veterans. One flat-poly geometry swap that says "this is yours now" is actually the minimum viable fantasy delivery. Without it, the economic dominance playstyle is invisible until the credit ticker runs, and invisible systems aren't features.

So my position: discrete authored state, expressed geometrically, readable from 500 meters. Not just patrol vacuum.

On the domination condition itself — Vera's point about fleet-strength versus standing being an inversion is important context, but I'm less worried about EV authenticity than about whether a new player can understand *why* a settlement is dominated when they first encounter one. Standing-gated is actually more legible. Fleet-gated requires knowing what fleet strength means.

## Round: EVALUATE

### Soren (solo dev scope warden)

Before the group debates tribute mechanics, I need to name the asset cost nobody has priced.

NPC settlements don't exist yet. The discussion is treating them as a configuration option on existing infrastructure. They're not. Each NPC settlement is a new authored object requiring:

- Geometry readable from 500 meters (established constraint)
- Minimum two states already decided: intact and degraded
- Nadia and Ren are now proposing a third state: dominated

That's the scaffolding problem from Q13, applied to a new asset class before the player settlement asset pass is complete.

**The blocking question before any tribute design:** How many NPC settlements are in the authored galaxy? Six to eight systems is the cap from Q27. NPC settlements aren't systems — they could be multiple per system. Each one is 3 geometry states × authoring time. At flat-poly rates, call it 3–5 days per settlement type for three states. Two settlement types at three systems is already 6–10 days of geometry work that doesn't appear in any milestone.

**Second scope flag:** The raid provocation timer Ren correctly identifies requires the raid system to distinguish NPC-settlement-origin raids from player-standing-origin raids. That's a new input to the spawn logic. Not expensive in isolation — but it's new, and it's not in any milestone.

**My agenda question:** Is dominance a playstyle available at M7 or M8? Because the asset and system cost is different depending on the answer, and neither milestone has room for a surprise.

What's the NPC settlement count?

<!-- complete -->
