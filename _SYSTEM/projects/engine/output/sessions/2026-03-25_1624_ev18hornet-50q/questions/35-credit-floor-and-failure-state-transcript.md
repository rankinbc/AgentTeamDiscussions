# Transcript: Credit Floor and Failure State

*Generated: 2026-03-25 18:42*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The question sounds like an economy question. It isn't. It's a flight feel question.

Here's the through-line: the atmospheric layer only pays off if the player has something worth defending below them. The SimCopter moment — banking over your settlement at 500m, watching the polygon cluster you built — requires the player to still *have* a settlement. If a credit drought cascades into inability to repair, inability to advance, inability to defend airspace, and finally a Claim Stake that nobody raids because there's nothing left to raid — that's not a failure state. That's the player quietly exiting without a dramatic moment.

What actually matters from the atmospheric layer perspective: the player must always be able to get back into the air over *something*. Even a degraded, stripped-back settlement reads differently from altitude than nothing does. The approach vector still has emotional weight if there's geometry below you.

So my agenda question is: does the credit floor connect to flight capability, or does it just gate Bar access?

We already decided `RESPAWN_SHUTTLE_CREDIT_FLOOR` covers death recovery. But that only fires on hull loss. What fires if the player bleeds to zero through operating expenses, failed cargo runs, standing penalties — the slow grind to insolvency?

My position: a floor is correct, but it should be defined as *minimum airspace engagement capability* — enough credits to fuel a descent, intercept one raid, and return. Not enough to feel safe. Just enough to stay in the game that matters.

What's the floor keyed to?

### Ren (emergence systems theorist)

Max has the framing right. But I want to tighten the mechanical reason.

The standing → raid → response chain is a feedback loop. The credit floor isn't about comfort — it's about whether that loop can still execute. If a player can't fuel an atmospheric descent, raids land unopposed. Unopposed raids degrade the settlement. Degraded settlement reduces income further. We already ruled out zero-output degradation for exactly this reason: no exit from the spiral.

The same logic applies to credits. The floor must keep the player inside the feedback loop, not outside observing it from the galaxy map.

What I want to flag that hasn't been said: **the slow insolvency path is architecturally invisible to current systems.** `RESPAWN_SHUTTLE_CREDIT_FLOOR` fires on hull death. Nothing fires if the player bleeds to zero through operating costs, failed cargo, standing penalties. That's a soft lock that bypasses every designed consequence surface — no comms intercept, no Bar cold dialogue, no death screen. The player just loses the ability to act without receiving a signal that explains why.

This is the isolation problem I'm specifically watching for. Death and insolvency are two different failure modes. Death has architecture. Insolvency currently doesn't.

The floor should be defined as: minimum to execute one atmospheric descent and return to a dockable port. One cycle. Not recovery — just enough to re-enter the loop that creates recovery pressure.

And it needs its own trigger surface. Not the death screen. Something that fires when credits cross the floor from above.

## Round: CRITIQUE

### Vera (EV systems historian)

The insolvency trap Ren identified is real, but the framing is slightly off. EV Nova didn't solve this with a credit floor. It solved it with **mission density and zero-cost Bar access**.

In EV, you could reach zero credits. The game didn't prevent it. What prevented terminal insolvency was structural: the Bar was always free to enter, missions were always available at the starting tier, and cargo runs existed as a baseline income floor that required no standing. The economy was simple enough that zero credits was a *temporary* state, not a terminal one, because re-entry into the earning loop had no prerequisite cost.

The question I'd put to this group before defining any floor value: **does Bar entry in this game cost credits?** If yes, zero credits locks you out of missions, which locks you out of standing recovery, which makes insolvency a soft lock. That's not an EV-heritage problem — it's an anti-EV design that no floor value will fully patch.

The second question: **are cargo runs available without standing prerequisites?** In EV, you could always haul something. If every income source in this game is standing-gated or faction-dependent, the economy has no baseline fallback, and insolvency becomes structurally different from what EV players understand.

Max and Ren are correct that a floor is needed. But before defining it, confirm the mission pool has a standing-agnostic entry tier. A floor on top of a locked loop is just a slower soft lock.

What does the baseline income tier look like at Claim Stake?

### Nadia (new-player experience advocate)

Vera's question about Bar entry costs is the one I'd pin first. Before we define any floor value, we need to answer it — because from a new player's perspective, insolvency that locks out Bar access is not a *failure state*. It's an invisible wall. The player doesn't know they're in a terminal condition. They just notice that nothing is available, try a few things, and stop playing.

That's worse than a punishing failure state. At least a punishing failure state *communicates*.

Ren's insolvency-has-no-architecture problem is exactly the new-player onboarding nightmare. Death has a screen. Insolvency has silence. And silence reads as a bug, not a consequence. A player who doesn't know EV will assume something is broken before they assume they made a series of bad economic choices over three sessions.

So I'd argue the floor isn't primarily a forgiveness question — it's a *legibility* question. Whatever the floor is, it needs a surface that fires when the player crosses it from above. Not a death screen. Something in-world. A Bar contact who says something cold. A comms line. Anything that names the condition so the player understands what they're looking at.

Max is right that something worth defending below you matters. But I'd add: a player in a credit crisis needs to know they're *in* a crisis before they can respond to one. The floor only works if crossing it is legible.

What fires when credits hit the floor?

## Round: EVALUATE

### Soren (solo dev scope warden)

Before the floor value, before the trigger surface — what are the operating expenses that drain credits to zero?

Ren describes "operating costs, failed cargo, standing penalties" as the bleed path. But I don't see an operating cost system in the milestone map. Standing penalties are in M5. Cargo failure is in M5. Operating costs — fuel, maintenance, crew upkeep — are not confirmed anywhere in the build sequence.

This matters for scope in two ways.

First: if there are no operating expenses, the slow insolvency path doesn't exist. Credits only move through mission rewards, cargo margins, and settlement income. Mission failure docks standing but the question is whether it docks credits. If it doesn't, "bleeding to zero slowly" is already architecturally constrained — it requires consistent active failure, not passive attrition. That's a different design problem than Ren is describing.

Second: Nadia's legibility surface — "something that fires when credits cross the floor from above" — is new architecture if it isn't the death screen. Before this group designs what fires, someone needs to say whether that trigger is a one-line extension of an existing system or a new monitoring path. Based on Q10 precedent, I'd estimate a comms line extension at one day. A new credit-state monitoring surface with its own emission event is three to five days.

Vera's Bar entry question is the right one. But before answering it: **does the current milestone plan include operating expenses as a system, or are credits only moved by discrete events?**

That answer changes the insolvency problem significantly.

<!-- complete -->
