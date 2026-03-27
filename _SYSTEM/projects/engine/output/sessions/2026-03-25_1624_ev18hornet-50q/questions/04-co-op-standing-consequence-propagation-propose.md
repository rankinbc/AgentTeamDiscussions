### Max (atmospheric flight advocate)

Here's what I care about in this question: raid spawn vectors.

We've already decided the atmosphere above a split-commitment settlement is contested airspace from two distinct directions — Confederation intercepts on P1's vector, Rebel patrols on P2's. That geometry only works if standings stay independent. The moment P1's actions bleed into P2's track automatically, you've collapsed two distinct spawn axes into a muddled shared heat value — exactly what we rejected last round.

So from where I sit: **no automatic propagation**. P1 destroys a Confederation freighter, P1 eats the standing loss, P2's Confederation track doesn't move. The atmosphere above their settlement responds to each player's own choices. That's the EV feedback principle and it's also what makes the airspace feel *authored by the players* rather than handed to them.

The agenda I want to set:

**First** — confirm the no-propagation answer is architecturally clean for M5. Single active player, single read, no bleed. Done.

**Second** — the interesting question is what happens when players take *joint actions* like a co-op boarding or a shared escort mission. Does the mission outcome distribute standing to both players? That's not the same as propagation — that's *shared authorship of an action*. That might need a flag or a split-credit mechanic.

**Third** — does this require any M5 API surface, or does the M8 co-op extension contract already cover it?

I want to lock the propagation question and open the joint-action credit question cleanly. Who's got the faction systems read on this?

### Ren (emergence systems theorist)

Max's propagation rejection is correct and the emergence chain confirms it. The standing → raid → intercept vector chain only produces authored-feeling airspace if each player's track is a clean causal input. Bleed corrupts the signal.

But joint-action credit is a different mechanism and it has emergence implications worth flagging now.

Consider the pathological case: P1 is Confederate-aligned (standing 70), P2 is Rebel-aligned (standing 70). They co-board a Confederation freighter. If both receive standing changes independently based on their faction state — P1 loses Confederate standing, P2 gains Rebel standing — you get a situation the designer didn't author: the same ship kill simultaneously pressures the Confederation intercept vector and rewards the Rebel patrol vector. One joint action shifts *both* spawn axes. That's not a bug. That's the emergence chain working correctly.

The architectural flag is this: if the standing mutation function at M5 only accepts `(player, faction, delta)`, joint actions can be dispatched as two separate calls with no new API. The M8 co-op extension contract already requires the function accept a player reference. Joint credit is just calling it twice with appropriate deltas — which means the faction standing API Max wants to lock for M5 already supports this pattern, no additions needed.

What M5 does need: clear documentation that joint actions are resolved as N independent standing mutations (one per participating player), not as a single aggregated event. That's a content design rule, not a code constraint — but if it's not written down now, someone will implement a "split credit" flag at M8 that adds complexity for no gain.

Lock propagation. Document joint-action dispatch convention. No new API surface required.


<!-- complete -->
