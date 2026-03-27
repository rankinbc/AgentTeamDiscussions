### Soren (solo dev scope warden)

[SCOPE - Soren (solo dev realist)]

I'm going to separate two things this room is treating as one conversation, because they have different build costs by an order of magnitude.

**Faction commitment exclusivity:** Cheap to build. An inverse standing axis is a sign flip in the standing update function. Vera's authored mission gate is a flag on a mission record plus a standing-check before the NPC dialogue branches. Nadia's hybrid — math handles the tail, the mission handles the moment — is the correct call and it's not expensive. Implement the flag. Surface the cost in the bar dialogue. Done. This is M5 work.

**Player faction formation:** This is not M5 work. This is not M8 work. Enumerate what "your settlement is now a nav faction" actually requires: a new entity type in the nav simulation, standing tracks *pointing at* the player faction instead of only away from it, raid calculation logic that reads player faction strength as an input, settlement geometry that reads as a distinct silhouette from altitude, and bar NPC dialogue that acknowledges the player's faction status differently from every prior faction interaction. That's four separate implementation domains. For a solo developer, that's a milestone of its own — *after* City tier is provably reachable and provably fun.

We have eight milestones. Player faction formation isn't in any of them. Before this room designs the skyline identity moment and the nav entity reversal, someone needs to say which milestone absorbs it and what gets cut to make room.

Flag it. Don't design it yet.


<!-- complete -->
