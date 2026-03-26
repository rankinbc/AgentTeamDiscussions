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


<!-- complete -->
