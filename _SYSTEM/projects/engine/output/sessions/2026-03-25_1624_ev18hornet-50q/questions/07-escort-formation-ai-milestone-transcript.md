# Transcript: Escort Formation AI Milestone

*Generated: 2026-03-25 16:46*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The question contains an assumption worth surfacing before we answer it: *2D* formation AI.

Escorts in the atmospheric layer aren't 2D. They're flying alongside you in a full 3D flight envelope — banking, pitching, maintaining offset while you thread a canyon or make a landing approach over your settlement. If we scope M6 formation AI as "2D" and call it done, we've implicitly decided that escorts only work in the galaxy/space layer. The atmospheric escort experience — a wingman holding position off your left wing as you descend through cloud cover toward your Colony — gets deferred indefinitely.

That's the scoping trap I want to flag before milestone assignment locks in.

On the actual question: I'd argue M6 should ship **functional AI**, not architecture stubs. Here's why. Formation AI that only lives in a galaxy map context — essentially 2D waypoint following with spacing — is nearly useless as a test bed for whether escorts *feel good*. The feel question only becomes answerable when they're flying alongside you in the atmospheric layer, where bank angles, speed differentials, and terrain avoidance create the actual challenge.

Architecture-first in M6 means M8 ships formation AI that's never been tested against the experience it most needs to serve.

So my agenda items:

1. **Define "escort scope" as atmospheric-inclusive from M6**, not galaxy-only
2. **Functional AI in M6** — simple offset following, no terrain avoidance yet, but 3D-capable
3. Terrain avoidance and contested airspace formation behavior defer to M8

What's the counter-argument for architecture-first?

### Ren (emergence systems theorist)

Max is right about the 3D capability requirement, but I want to reframe *why* it matters — because the argument from "feel" undersells it.

The emergence chain this game lives or dies by is: faction standing → raids → atmospheric defense → on-foot combat. Escorts aren't a comfort feature. They're the player's defensive response to faction pressure at the atmospheric layer. If escort AI is galaxy-only in M6, then when a Confederation raid spawns over your settlement, your escorts can't follow you in. The raid defense collapses to a solo on-foot problem. The faction standing system — which we've spent six rounds carefully designing — loses one of its major consequence branches.

That's not a feel problem. That's a system that works in isolation. Faction standing → raid → escorts-can't-participate is an emergence chain with a severed link.

So: **3D-capable escort AI in M6, even if minimal.** Simple offset following, no terrain avoidance, no contested airspace formation behavior. The capability threshold that matters is "can enter atmospheric layer and maintain loose formation" — not "flies elegantly through canyons."

One constraint I'd add to Max's framing: the escort AI must also respond to the same faction standing reads that drive raid spawns. An escort hired from a Rebel contact should not hold formation if Confederation raiders are the ones spawning — unless your standing with both factions creates that tension deliberately. The escort's faction affiliation needs to wire into the same standing system, not sit parallel to it.

Otherwise we've built two isolated systems that happen to occupy the same airspace.

## Round: CRITIQUE

### Vera (EV systems historian)

**The EV precedent is being used selectively here, and I want to name that.**

In EV, escorts were a 2D fleet-layer feature. They followed you through hyperspace, held formation in space combat, and died in space. The atmospheric layer — as a distinct geometry — did not exist. The escort feel that made EV's fleet composition satisfying came entirely from the galaxy map: you could see your ships, count them, lose them visibly. That legibility was the feature.

What Max and Ren are designing isn't "EV escorts." It's a new problem: 3D formation AI that transitions layers. That's a harder scope item than anything EV shipped, and wrapping it in EV nostalgia doesn't compress the implementation cost.

Now — Ren's emergence argument deserves scrutiny rather than deference. The chain proposed is: faction standing → raid spawn → escort defense. But the raid intercept layer was already decided as M8 scope (two-spawn-axis geometry, contested airspace). If atmospheric raid defense is M8, then the question of whether escorts participate in atmospheric defense is also an M8 question. You cannot have a severed emergence chain link in M6 if the link it connects to doesn't exist until M8.

**My read:** M6 ships formation AI that is architecturally layer-aware — capable of being called into atmosphere — but with functional behavior validated in the galaxy/space layer first. You need playtest data on escort feel in 2D before you know what "good enough" means in 3D. EV knew this. The galaxy map was the test bed. It wasn't a limitation. It was sequencing.

What does M6 need to *prove*, not just implement?

### Nadia (new-player experience advocate)

Vera's question is the right one, and I want to answer it from the hire moment outward.

When a new player hires their first escort from The Bar — that handshake is a promise. *You paid for a wingman. Here is your wingman.* The question is: where does the game redeem that promise?

On the galaxy map, it's abstract. A little dot follows your little dot. Players won't read that as "escort working" — they'll read it as "UI thing." The moment the escort becomes *real* is when they're visible off your left wing as you drop into atmosphere. That's when the hire means something felt.

So here's my concern with galaxy-first sequencing: if escorts disappear when the player descends, the first atmospheric descent after hiring reads as *broken*, not deferred. Players don't know M6 scoped escorts to galaxy-only. They know they have a wingman who just vanished.

Vera's sequencing logic is sound — you need 2D feel data before you tune 3D. I'm not arguing against that. I'm arguing that the player's experience of "layer transition with escort" needs to be decided before M6 ships, even if the answer is a graceful holding-orbit behavior rather than full atmospheric follow.

**My position:** M6 ships functional galaxy-layer formation AI. But M6 must also decide the layer-transition contract — what the escort visibly does when the player enters atmosphere. Even if that's "holds at entry altitude" rather than full follow, the player needs to see it happen. A deliberate holdback beats an invisible teleport.

What does "escort stays legible across the transition" require architecturally? That's the real M6 scope question.

## Round: EVALUATE

### Soren (solo dev scope warden)

[PROPOSE - Soren (scope estimator)]

Before we answer the milestone question, I want to put build cost on the table, because this discussion has been expanding scope without acknowledging what that costs.

Formation AI is not one feature. It is at minimum:

1. **Offset following** — simple, 3–5 days in 2D, doubles in 3D because you're managing pitch and bank, not just heading
2. **Layer-transition contract** — Nadia correctly identified this; "holds at entry altitude" sounds cheap but requires detecting layer entry, queuing a hold behavior, and making it legible to the player. Call it 2–4 days.
3. **Faction affiliation wiring** — Ren's correct that escort standing must read from the same system. But this is also a non-zero item if it hasn't been built yet.
4. **Galaxy-layer feel validation** — Vera's sequencing argument is right and is also free: you get this data by shipping 2D first.

M6 is the Fleet milestone. That milestone already carries ship acquisition, fleet composition UI, and escort hire flow through The Bar. The plate is not empty.

**My agenda for this round:**

1. What is M6's current estimated scope *without* escort AI? Is there room for even 2D functional formation AI, or does that push M7?
2. "Architecturally layer-aware" is not a free stub — what does it actually cost to build versus skipping it?
3. Nadia's layer-transition contract is the correct minimum viable decision. Can we scope that independently of full atmospheric follow?

The emergence chain argument is real. But "real" doesn't compress build time. What's already on M6's plate?

<!-- complete -->
