# Transcript: Faction Standing Commitment Threshold

*Generated: 2026-03-25 16:27*

## Round: PROPOSE

### Max (atmospheric flight advocate)

**Standing threshold: 65 out of 100. Here's why that number matters atmospherically.**

The commitment NPC shouldn't appear until the player has *flown contested airspace over their own settlement* at least once. That's the SimCopter payoff — banking over your Outpost at altitude, seeing the polygon rooftops you placed, watching a faction patrol cut through the clouds below you. That moment needs to exist *before* you commit, because commitment should feel like choosing to defend something you already love.

At 65, you've done real work. You're not neutral anymore. Factions are watching your flight paths. You've probably taken fire defending your claim stake approaches. You've *earned* the view from altitude.

My concern going into this discussion: if the threshold is set too low — say, 30 or 40 — commitment happens before the atmospheric layer has delivered its core payoff. You're locked in before you've had the bank-and-roll moment that makes the faction worth caring about. The commitment string becomes paperwork instead of punctuation.

If it's too high — 80+ — you've already got the relationship. The NPC feels redundant. The standing curve has done the emotional work the mission string was supposed to do.

**65 is the inflection point where the player knows they belong to a place but hasn't fully decided what that means.**

Two things I want the group to weigh in on:
1. Does the threshold scale with settlement tier, or is it a flat value?
2. Does the commitment NPC appear dirtside (On-Foot layer) or do they broadcast from the Atmospheric layer — intercepted mid-flight?

That second one changes everything about how this *feels*.

### Ren (emergence systems theorist)

Max's 65 is well-argued from an atmospheric pacing lens, but I want to push on something: **a flat threshold is still a scripted beat.** The NPC fires at 65 for every player, every run. That's authored content wearing emergent clothing.

What actually signals commitment isn't standing accumulation — it's whether the player has *defended something*. Two players can hit 65 with completely different relationships to the faction. One farmed trade runs. The other flew three intercept sorties against raiders targeting their Outpost. The NPC appearance means different things to each of them, but the code path treats them identically.

The emergent version: **threshold = standing ≥ 55 AND (settlement_tier ≥ 2 OR raid_repelled_count ≥ 1)**. Now the NPC appears when the player has demonstrated commitment through action, not just passive standing drift. You can reach it "early" by getting raided and fighting back. You can delay it by staying neutral and keeping your tier low. The threshold becomes a *product* of the emergence chain rather than a gate on it.

On Max's two questions directly:

1. **Scale with tier, yes** — but my compound condition handles this naturally. Higher tier creates more raid exposure which accelerates the alternate trigger path.

2. **Atmospheric intercept.** Not because it feels better — because it mechanically closes the loop. The NPC appears *in the airspace you've been defending*. That's the systems interaction. Dirtside delivery breaks the chain; the bar is for strangers, not for someone who's watched you fly.

If the API truly needs a single integer: **55, with the compound condition as the canonical trigger.**

## Round: CRITIQUE

### Vera (EV systems historian)

**EV precedent cuts through this argument cleanly. Let me state what the historical record actually shows.**

In EV Nova, faction commitment strings didn't trigger on standing alone. They triggered on standing *plus mission completion* — specifically, you had to have *done something for them* that was unambiguous. The Polaris string doesn't open because you have high Polaris standing. It opens because you completed "Nil Desperandum" and the game registered a deliberate choice. The standing was a precondition, not the trigger.

Both of you are arguing over integer values when the more important precedent is structural: **EV used compound conditions because the designers understood that standing is an artifact of behavior, not a proxy for intent.**

Ren's compound condition is closer to authentic EV architecture. But "raid_repelled_count ≥ 1" concerns me — it's a very specific authored condition that could be gamed or missed through no fault of the player's engagement. In EV, the equivalent condition was always a *discrete player choice* (accepting a flagged mission) not a combat statistic.

**My position:** The commitment NPC should require standing ≥ 60 AND at least one completed mission in the faction's string — not a raid counter, not a tier check. That's the EV model. The player chose to do faction work; the faction responds to that choice.

On the atmospheric intercept: historically wrong. Every meaningful NPC in EV was in a bar or spaceport. Intercepting players mid-flight was reserved for enemies and strangers. Your commitment contact should be dirtside, in the Bar, where EV always put the conversations that mattered.

What's the current mission string architecture for M5? That determines whether my condition is even implementable.

### Nadia (new-player experience advocate)

Vera's structural read is the one that matters for new players, and I want to explain why the number is almost beside the point.

A player who doesn't know EV cannot feel a standing score. They feel *events*. Ren's raid counter and Max's altitude moment are both events — but only one of them is something the player *chose*. Vera's completed-mission condition wins on legibility: the player did a thing, they felt the thing, and now the thing responds to them. That's a feedback loop a first-session player can actually parse.

Here's my flag: **if the commitment NPC appears without the player understanding that faction standing exists as a system, the NPC reads as a random popup.** Standing needs a tutorial surface before it gates anything — even at 60. Does the UI ever show the player their standing number? Does anything in the first session *name* the system? If the answer is no, then every threshold argument is moot because the player won't understand what they earned.

On the intercept vs. bar question: new players read mid-flight interruptions as threats. An unknown contact cutting into your airspace during the atmospheric layer will read as an enemy until proven otherwise. Put the NPC in the bar. That's where players have learned to expect consequential conversations. Don't use a new mechanic (atmospheric broadcast) to deliver the highest-stakes narrative beat.

**My position:** Vera's compound condition (≥60 standing + one completed faction mission), dirtside, in the Bar. But add one thing — a standing tooltip the first time it ticks above 40, so players know the system exists before it matters.

## Round: EVALUATE

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
