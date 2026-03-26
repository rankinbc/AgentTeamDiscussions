### Vera (EV systems historian)

**[PROPOSE - Vera (EV systems historian)]**

Both positions are directionally correct on mission-gating. Neither has asked the EV-critical question: **what does the floor actually mean?**

In Nova, standing wasn't a continuous gradient with smooth recovery available everywhere. Below certain thresholds, factions wouldn't let you dock. That's not a mission gate — it's a physical access gate. You couldn't begin recovery missions because you couldn't land to take them. The floor had teeth.

This game has The Bar as the mission acquisition layer. If degraded standing means the faction's Bar contacts won't speak to you, recovery missions don't exist in the UI — there's nothing to take. Max's "available at any positive value" proposal collapses that distinction. Positive standing doesn't mean relationship intact. It means you haven't fully antagonized them yet. Those are different states.

I'd separate standing into three behavioral bands:
- **Engaged** (above ~40): missions available, normal NPC behavior
- **Degraded** (below 40, above some floor): faction contacts cold, recovery missions sparse or absent, airspace hotter
- **Hostile** (below floor): faction shoots on sight, no docking, recovery requires an intermediary or a specific authored string — not just grinding missions

Max's patrol density feedback is compelling but it's M8 geometry. Don't let the visual design of atmospheric consequences drive the M5 standing logic.

**My question for this round:** Does the hostile floor exist, and if so, is recovery from it player-initiated or does it require a specific authored trigger to unlock the recovery path?

### Nadia (new-player experience advocate)

**[PROPOSE - Nadia (new-player experience advocate)]**

Vera's three-band model is the right structure. My concern is the Degraded band, not the Hostile floor.

The Hostile floor is legible. Faction shoots on sight — players understand they've crossed a line even without knowing why. The consequence is immediate, physical, and unmistakable. That band can require an authored unlock because the player *knows* something broke.

The Degraded band is where new players get quietly punished without feedback. Bar contacts going cold, missions becoming sparse — these are invisible to someone who doesn't have a prior session's mission density to compare against. They'll think the content dried up, not that they degraded a relationship. That's systems-legibility failure happening below the threshold where the standing tooltip even fires.

My proposal: the standing tooltip should fire **downward through 40**, not just upward. Specifically, it should read differently — not "here's what standing affects" but "your standing with [Faction] is slipping — this is what's starting to close." That one-time downward trigger is the signal that makes the Degraded band legible before it becomes the Hostile floor.

For recovery access: I agree with Vera that "any positive value" is too loose. But the gate shouldn't be invisible. If a Bar contact won't offer recovery missions below a certain value, there needs to be a single cold line of dialogue telling the player what's happening: *"Come back when we're on better terms."* Not a UI tooltip. A person in a bar saying something true.

Recovery should be hard. It shouldn't be silent.


<!-- complete -->
