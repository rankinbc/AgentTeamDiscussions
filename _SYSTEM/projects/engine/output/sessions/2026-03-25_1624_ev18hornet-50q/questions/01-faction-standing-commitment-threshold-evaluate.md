### Soren (solo dev scope warden)

## Soren — Scope Read

Before anyone writes API code: count the variables being proposed.

**Simple condition (standing ≥ N):** one integer comparison. Test cases: ~3. Implementation: one line.

**Vera/Nadia's compound (standing ≥ 60 AND completed_faction_mission ≥ 1):** two data points, both need to persist across sessions, both need to be queryable at trigger-check time. Test cases: ~9. Mission completion needs to be wired to faction standing before M5 faction API work even starts.

**Ren's compound (standing ≥ 55 AND tier ≥ 2 OR raids_repelled ≥ 1):** three data points, one of which — `raid_repelled_count` — doesn't exist yet. You're not picking a threshold, you're authorizing a combat statistics system as a prerequisite. That's a new thing. Name it before you build it.

**The atmospheric intercept:** Max and Ren both floated this. It's a whole mechanic — mid-flight NPC broadcast, intercept UX, voice/text delivery mid-mouse-flight. Vera and Nadia correctly killed it on feel. I'm killing it on build time. Don't build it.

**My position:**

Standing ≥ 60, mission completion flag, dirtside in the Bar. This is the Vera/Nadia condition. It's implementable now with systems you're already building. The mission completion flag is a boolean you'll need anyway for mission string progression.

The number is 60. The condition is compound. The location is the Bar.

Lock this so M5 can start. Every week this stays open is a week the faction API waits.


<!-- complete -->
