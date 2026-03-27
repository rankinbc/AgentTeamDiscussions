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


<!-- complete -->
