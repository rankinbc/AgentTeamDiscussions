### Max (atmospheric flight advocate)

The atmosphere dive is not an extension of 2D escort AI. It is a completely different problem, and conflating them for "context switching" efficiency is how you get escorts that technically follow you into atmosphere and feel completely wrong doing it.

Here's what the dive actually requires: the escort needs to read your bank angle, anticipate your roll, maintain offset through a 3D flight envelope where speed, altitude, and turn radius all interact. That is not a galaxy-map formation problem. Galaxy-layer AI proves offset following works in flat space. It tells you nothing about whether an escort can stay in position when you're pulling 60 degrees of bank over a ridge at low altitude.

My position: **M8, same as already decided, and for the right reasons.**

But here's what I want the team to lock down that nobody has said clearly yet — the M6 hold behavior cannot feel like a failure state. When the player dives into atmosphere and the escort orbits at the entry point, that moment needs to read as *"my escort is waiting for me"* not *"the AI broke."* The visual treatment of the hold is a flight feel problem, not an architecture problem. A stationary hover feels wrong at altitude. A flat circle orbit looks fine on a map and looks stupid in the cockpit view. 

That's the M6 work I care about: making the holdback *legible and atmospheric*, not just functional.

The dive earns its scope when we have solo atmospheric feel data to tune against. M8 is the right gate. But M6 hold behavior needs a real UX decision before it ships.

### Ren (emergence systems theorist)

Max is right, and the reasoning holds. But I want to add a layer he didn't name.

The escort's hold position at atmospheric entry altitude is not incidentally where raids appear — it's the same geometric chokepoint. Faction intercepts arrive from orbit, push through the entry vector, and engage the settlement below. An escort holding at that altitude is already positioned at the interception point. That's not a UX detail. That's the emergence chain showing its structure before we've designed it.

This means M6 hold behavior has a hidden mechanical implication: **what happens when a raid spawns while your escort is holding orbit at entry altitude?** The player is in atmosphere. The escort is at the entry point. The raiding fleet exits FTL into the same space. Does the escort engage? Does it get destroyed before the player surfaces? Does the player return to a debris field and a different tactical situation than the one they left?

None of this requires us to ship contested airspace geometry in M6. But it means the hold behavior needs to be written as a *state*, not a *pose*. "Hold at entry altitude" must be interruptible by faction threat detection using the same standing reads that drive raid spawns. Otherwise M6 hard-codes a passive escort that M8 will have to tear out.

Max's legibility concern is valid and real. My addition: legibility is downstream of the hold being a live mechanical participant in the faction space, not a frozen animation waiting for the player to resurface.

M8 for the dive. M6 hold must be threat-aware from day one.


<!-- complete -->
