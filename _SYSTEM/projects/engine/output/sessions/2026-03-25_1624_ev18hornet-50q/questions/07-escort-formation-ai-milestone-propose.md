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


<!-- complete -->
