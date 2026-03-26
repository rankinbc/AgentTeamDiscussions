# Transcript: Raid Defense Weapon Type

*Generated: 2026-03-25 17:48*

## Round: PROPOSE

### Ren (emergence systems theorist)

The weapon type question is downstream of a more structurally important question we haven't settled: **does on-foot combat during a raid breach connect to any other active system, or does it resolve in isolation?**

If it resolves in isolation — player has weapon, enemies enter, player shoots — then weapon type is a feel decision. Pick what handles well in first-person and move on.

If it connects, the weapon type choice carries real design weight. Specifically:

**The supply chain connection.** If ammo or charges require faction-sourced materials — trade routes, Bar contacts, supply escort missions — then weapon type becomes part of the faction standing → raid defense loop. A Confederation embargo doesn't just change airspace; it empties your defense stockpile. That's a systems interaction. A Raider-origin weapon with scavenged ammo tells a different story than a military-grade purchase requiring Engaged standing with a government faction.

**The flag I'm raising:** If we choose a weapon type that requires no supply chain, no standing to acquire, and no cross-system dependency, we've added on-foot combat as a feature rather than as emergence. It works in isolation but doesn't feed back into anything.

The minimum question before weapon type: **does M7 on-foot combat have an acquisition path that touches the existing standing or economy systems, or does it arrive as authored equipment?**

Weapon category follows from that answer. The emergence chain lives or dies at that fork.

### Max (atmospheric flight advocate)

Ren's right that acquisition path is the structural question — but I want to flag a specific version of that question that matters from the atmospheric side.

The moment the player decides to *land and fight on foot* versus *intercept in the air* is one of the most interesting tactical decisions in this whole game. A Shuttle with a hot hull can't win an aerial intercept. But if the player has a capable weapon dirtside, going to ground becomes a real option. That decision — descend and fight, or stay in the air and try to outrun it — only works if both options feel meaningful.

What I'm watching for: **weapon type that makes on-foot defense feel like the better choice at M7 regardless of airspace conditions.** If the dirtside weapon is always the dominant answer, the atmospheric intercept path withers. Players learn to just land and deal with it. The SimCopter moment — watching your settlement from altitude, seeing the raid approach, making a real call — gets short-circuited.

So on Ren's acquisition fork: authored equipment at M7 is fine by me, as long as the weapon doesn't make dirtside the dominant strategy. A sidearm with limited range — something you'd only reach for if you couldn't get back to your ship — preserves the atmospheric choice without requiring a supply chain.

Specific weapon type: I'd vote for a short-range energy sidearm. Low ammo ceiling, high close-quarters feel. Forces the player to care that enemies actually breached the perimeter. Doesn't make the aerial layer feel redundant.

## Round: CRITIQUE

### Vera (EV systems historian)

Before weapon type, I want to name what EV actually was at the dirtside layer: **a narrative surface with no mechanical resolution**. The Bar gave you missions, rumors, and escorts. Nothing on foot ever fought anything. The on-foot layer in this design is a genuine departure — that's not a criticism, it's a scope clarity requirement.

The authenticity question I'm raising: **on-foot raid defense must feel like a failure state, not a feature**.

In EV, if you couldn't manage your standing well enough to prevent raids, the consequence was legible and consequential — buildings damaged, tier regression, standing signal that something was wrong. On-foot combat risks inverting that: the player who let their standing slip now has a *more engaging experience* than the player who managed standing correctly and watches the raid get intercepted from altitude.

That's the antipattern. If on-foot combat is mechanically interesting, standing management becomes less important. The faction loop — the thing that makes this game — weakens.

Max's framing is correct but needs sharpening: the weapon shouldn't just avoid making dirtside *dominant*. It should make dirtside feel **costly and improvised**. EV's economy worked because every resource had friction. Ammo that's scarce, range that's punishing, no guarantee you survive a breach — these aren't tuning choices, they're the mechanical message: *you should have managed your airspace*.

Specific weapon type follows from that framing. What reads as "last resort" in flat-poly first-person at Outpost scale?

That's the question I'd put to the room.

### Nadia (new-player experience advocate)

Vera's "failure state" framing is right, but I want to push on what that means for a player who doesn't yet know they should have managed their standing.

A new player's first raid breach won't feel like a consequence of their choices — it'll feel like a game event. They haven't learned the faction loop yet. So the weapon has to do double duty: communicate "this is improvised and desperate" *while they're using it*, so they understand retroactively that something went wrong.

That's a teaching surface, not just a tuning question.

A short-range energy sidearm works for me — Max's framing holds — but only if the flat-poly first-person presentation makes the limitation legible immediately. No ammo counter buried in a corner. The weapon should *look* like something grabbed off a wall, not a primary loadout. Visual design does the narrative work EV used text for.

The thing I'm flagging from a first-session standpoint: **the breach moment needs to tell the player what the aerial alternative was.** If they're fighting on foot with a sidearm and losing, they need some surface — even a single comms line — that says "your ship couldn't reach them in time." Otherwise the lesson doesn't land. They just fought a weird encounter. The standing → airspace → breach causality has to be readable *during* the failure, not explained in a menu afterward.

Vera's right that combat shouldn't be engaging enough to substitute for airspace management. But it has to be legible enough to teach the loop it's punishing you for missing.

## Round: EVALUATE

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
