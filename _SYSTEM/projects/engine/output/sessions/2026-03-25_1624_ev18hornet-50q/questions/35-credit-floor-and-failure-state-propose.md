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


<!-- complete -->
