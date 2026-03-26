### Soren (solo dev scope warden)

The design framing in this room is sound. I'm not going to argue with it. What I'm going to do is name the build cost that's sitting underneath this conversation unremarked.

**On-foot combat is a separate gameplay system.** It requires: first-person movement in a constrained space, a weapon with a fire state and hit detection, enemy units with pathfinding inside building geometry, a health or damage model, and a death/fail state. None of these exist yet. The weapon type choice is the smallest item on that list.

Flat-poly helps with art. It does not help with AI pathfinding, collision detection, or the fire/hit loop. Those are code problems.

Rough estimate for minimum viable on-foot breach combat — sidearm, limited ammo, enemies enter and move toward player, player can kill or die:

**3–5 weeks, solo.**

That's before supply chain integration (Ren's fork), before the comms line Nadia is asking for, before the teaching surface that makes the loop legible.

The question I'd put before weapon type: **Is M7 on-foot combat a named M7 build item, or is it M8?**

If it's M7, the milestone needs to absorb 3–5 weeks of new system work on top of everything else already scoped there. That has to be acknowledged explicitly before weapon type is decided.

If the answer is "yes, M7, we've budgeted for it" — then short-range energy sidearm is the right call. Vera and Max are aligned, the constraint is correct. Author it as a last-resort item and move.

But the milestone placement question comes first.


<!-- complete -->
