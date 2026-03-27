### Soren (solo dev scope warden)

Vera closed the routing problem before it opened. Accept it.

"Nearest navigable friendly" is not a lookup — it's a graph traversal against live port state, contested boundary flags, and standing reads across multiple factions simultaneously. For a respawn mechanic. That's weeks of infrastructure to answer a question EV answered with one variable.

Last-docked is a single write on successful landing. One field. The standing check at respawn time is already built — you're reading the same band data that gates mission availability and Bar access. No new read path. No routing topology. No contested-system geometry.

**What actually needs to be decided:**

1. **Docked definition.** Does landing at your own settlement pad count as docking for last-docked purposes? It should. That's Max's scenario working correctly — last anchor was your home pad, you wake up there post-raid, you fly toward the damage. Nothing extra to build.

2. **Pad destruction.** If the pad is in degraded state, does it still count as a valid respawn anchor? Two options: (a) degraded pad is still dockable, just damaged — simplest, no new logic; (b) destroyed pad invalidates the anchor, requires fallback chain. Option (b) adds a fallback chain. Scope that explicitly before choosing it.

3. **Starting port fallback.** Nadia's right. Hardcode it as always-accessible. One constant. Done.

The only open question with real build cost is pad destruction invalidating the anchor. Everything else is already in the system.

How deep does tier regression cut the pad's functionality?


<!-- complete -->
