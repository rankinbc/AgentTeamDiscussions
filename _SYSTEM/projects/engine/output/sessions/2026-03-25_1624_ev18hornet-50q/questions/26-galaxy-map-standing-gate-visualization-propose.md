### Max (atmospheric flight advocate)

Here's the thing we need not to get backwards: the galaxy map visualization isn't primarily a *legibility* problem. It's a *desire* problem.

A new player staring at the galaxy map has never felt 300 knots of flat-poly airspace over their own buildings. They don't know what they're missing. The standing gate visualization has to make them *want to go down there* — not just understand abstractly that a system exists.

So I'd reframe the agenda question: **what does the galaxy map show that makes a player's hand drift toward the atmospheric entry key?**

My candidate: the galaxy map shouldn't explain standing gates at all. It should show *consequences*. A faction icon pulsing amber near your claimed system. No tooltip explaining the standing mechanic. Just ambient threat color. The explanation comes *after* descent, in the comms intercept, when the system has their full attention and they've already felt the airspace change under them.

This connects directly to Q22's open question about Option A/B/C. If faction presence is already in the simulation but not surfaced (Option B), we can key the ambient threat color to standing band crossings — Engaged band is clean, Degraded band adds the amber pulse, Hostile adds the red. That's a one-to-three day read path addition, not a new system.

What I want to flag as a risk: any design that lets the player *resolve* standing anxiety from the galaxy map without descending. Spectator mode kills the atmospheric layer. The galaxy map should be uncomfortable enough to make descent feel like the obvious move.

That's the agenda I'd set. What does Option B actually cost?

### Ren (emergence systems theorist)

Max is right that this is a desire problem first. But I want to push on something structural underneath his proposal.

The amber pulse only works as an emergent signal if it's derived from the same standing read path that drives raid spawn selection — not a separate UI flag. If the galaxy map reads `player.standing[faction]` and maps it to threat band color using the same `RAID_HARASSMENT_THRESHOLD` and `RAID_ASSAULT_THRESHOLD` constants already decided, then the visual isn't a notification system. It's the standing system's state made legible at the galaxy layer. One source of truth propagates to both behaviors simultaneously.

That's the interaction test. Does the galaxy map visualization share mechanical state with raid composition, or does it duplicate it? If it duplicates it, you've built two systems that will drift. If it reads the same constants, you've built zero additional systems — you've just surfaced an already-live state.

The patrol spawn point question from Q21 is load-bearing here. If patrols distribute across the orbital shell rather than anchoring to a single insertion point, the threat visualization could reflect spawn geometry — not just "threat exists" but something about the distribution. A single converging vector reads differently from split vectors. A player who learns to read that distinction on the galaxy map is learning raid composition before descent. That's the mental model forming through play, not through tutorial.

The isolation risk is the galaxy map becoming a threat dashboard you manage remotely. Max's point about discomfort-as-invitation is correct. Vague enough to demand descent, precise enough to register as signal.

Option B. Same read path. No new system.


<!-- complete -->
