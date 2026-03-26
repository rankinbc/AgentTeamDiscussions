# Transcript: Settlement Tier Advancement Trigger

*Generated: 2026-03-25 18:29*

## Round: PROPOSE

### Ren (emergence systems theorist)

The surface question is what triggers tier advancement. The deeper question is whether that trigger is load-bearing in the emergence chain or decorative.

Here's what I want the group to hold while we deliberate: tier advancement is the moment the settlement becomes more visible to faction systems. Every tier step increases the standing threshold at which raids escalate. That means the advancement trigger isn't just a progression gate — it's the input that modulates the whole faction pressure curve. Get the trigger wrong and tier advancement becomes a protected zone the player can manage independently of their standing choices.

Two failure modes I want to flag immediately:

**Isolation failure:** A pure resource-investment trigger lets a player advance tier while ignoring faction standing entirely. The settlement gets bigger; the raids get more dangerous; but the player's path to advancement never intersected the standing system. That's two systems running in parallel, not interacting.

**Agency cap:** A time-gated or session-gated trigger removes player decisions from advancement. The settlement grows on a clock, not from choices. That's scripted progression dressed as emergence.

What I want to explore is whether tier advancement can be a natural consequence of engaging the systems that already exist — specifically, whether the economic loop (missions → credits → investment) and the standing loop (missions → standing → faction pressure) can share the same actions as inputs to advancement, such that you cannot advance tier without also having moved on faction standing.

One concrete question for the group: should the advancement trigger be able to fire at any standing level, or should maintaining a tier require minimum Engaged standing with at least one faction?

### Max (atmospheric flight advocate)

Ren's framing is correct and I want to add something specific: the tier advancement moment is the SimCopter payoff. That's the beat where you climb to 500m and your settlement is *visibly larger* than it was. If the trigger that fires advancement doesn't pull the player through the atmospheric layer to see it, we've wasted the payoff.

So here's my concrete position: the advancement trigger should require at least one successful aerial defense — the player must have intercepted and repelled a raid from atmosphere, not survived a breach. Not as a bureaucratic gate, but because that's the action that *earns* the altitude view. You climbed out, you flew the intercept line, you came back down and landed. Now you can see what changed.

This addresses Ren's isolation failure directly. You cannot advance tier without having engaged the atmospheric layer as a defense surface. The standing system feeds raid frequency and scale, which means you cannot have had a successful intercept without your standing having been somewhere meaningful. The loops aren't parallel — they converge at the intercept event.

On the resource/investment question: I'm not opposed to a credit threshold as a *necessary* condition. Investment makes sense. But it shouldn't be *sufficient*. Credits alone shouldn't advance tier without the intercept. Otherwise the player who never descends builds the same settlement as the player who learned the airspace.

Ren's question about minimum Engaged standing as a maintenance requirement — yes, but I'd rather express that through raid dynamics than through a hard gate. If you drop below Engaged, raids escalate until regression pressure does the work.

## Round: CRITIQUE

### Vera (EV systems historian)

The aerial intercept gate concerns me. Let me name why before the group builds on it.

In EV, nothing required you to demonstrate a specific flight maneuver to advance. Progression came from investment, standing, and time — in that order. What made the faction system feel *traceable* wasn't that the game forced you through a particular action. It was that your choices moved standing, and standing moved the world around you whether you noticed it or not.

Max's intercept gate is a skill gate wearing a systems costume. "You must have flown the intercept line" is not a standing consequence — it's a behavioral requirement that happens to correlate with standing engagement. Those are different things. A player with high Confederation standing who hired escorts and let them handle every raid is making a *valid standing-system choice*. Gating their tier advancement on personal intercept denies that.

There's a precedent problem too. The decision log explicitly ruled out `raid_repelled_count` as a commitment NPC trigger because standing + mission completion was the right signal. That same logic applies here. If standing movement is the systemic record of faction engagement, it should be the primary input to advancement gates — not a derived behavioral artifact.

Ren's isolation failure is the real problem to solve. My question for the group: **is the isolation failure a trigger design problem or a delta magnitude problem?** If missions that advance standing also happen to be the most efficient credit source, parallel paths close naturally — not through a gate but through economic gravity. That's how EV did it. The systems didn't require coordination; they produced it.

What's the mission economy look like relative to credits needed for tier investment?

### Nadia (new-player experience advocate)

Vera's delta magnitude question is the right frame, and I want to add a layer to it from where I sit: **the trigger is only as good as its legibility to someone who has never played EV**.

Economic gravity closing the loops naturally is elegant — but it's invisible. A new player who does faction missions, accumulates credits, invests in their outpost, and then one day finds themselves at the next tier... did they understand *why*? Or did the settlement just quietly get bigger while they were looking elsewhere?

The SimCopter payoff Max describes — climbing to 500m and seeing something visibly larger — that's real. But the payoff only lands if the player anticipated it. If tier advancement fires silently in the background, you don't get the moment. You get a tooltip they might miss.

My concern with Max's intercept gate isn't the intent, it's the shape. A player who hired escorts and *trusted the faction system to do its job* is playing correctly. Blocking their advancement punishes them for understanding the game before the game confirms they should.

Here's what I'd push toward: **the trigger should be something the player chose visibly, not something the system observed passively.** Resource investment is a choice the player makes consciously. Standing movement — if it's legible through the tooltip system — is also visible. The combination of those two creates an advancement moment the player can anticipate.

The open question is whether the tooltip system, as currently designed, fires early enough that standing is *comprehensible* before it becomes consequential. If it isn't, tier advancement punishes players who didn't know what they were building toward.

## Round: EVALUATE

### Soren (solo dev scope warden)

**[AGENDA - Soren (scope estimator)]**

Before this group picks a trigger, I need the room to hold one number: each advancement condition is a separate build item, and they stack.

A resource investment threshold is a single integer comparison against a credits/materials ledger. One day to implement if the ledger already exists, which it should by M7. That's the baseline.

A standing gate reuses `mutate_standing` and band reads already decided. No new surface. Near-zero marginal cost against existing architecture.

Max's aerial intercept requirement is a new counter, a new event emission at intercept resolution, a new read path into the tier advancement check, and a new edge case for escort-handled intercepts that Vera correctly identified. Estimate: 2–4 days, plus the escort-attribution question that is still open from Q7-Q8. That question is not resolved. Building on an unresolved open question is how scope expands silently.

Vera's economic gravity argument is not a trigger — it's a design hope that the numbers work out. It requires no build cost but it also requires no guarantee. If mission credits don't happen to dominate the economy at Outpost tier, the loops don't close and we have no enforcement mechanism.

**The agenda question I want answered before we debate trigger philosophy:** Does the advancement trigger need to be a hard gate that the engine enforces, or a soft gravity that content design produces?

Those are different implementation targets. The group has been debating trigger design before answering that. I want it answered first.

<!-- complete -->
