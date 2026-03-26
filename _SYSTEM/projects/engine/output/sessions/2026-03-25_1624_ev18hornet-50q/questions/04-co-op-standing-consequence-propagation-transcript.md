# Transcript: Co-op Standing Consequence Propagation

*Generated: 2026-03-25 16:36*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

**PROPOSE — Vera**

Propagation rejection is correct. In EV, standing was a personal ledger — the design worked precisely because every delta was attributable to a specific player choice. That traceability is what made the faction system feel consequential rather than ambient. Contaminating P2's track with P1's actions destroys that signal. Max and Ren have this right, and the EV record supports it unambiguously.

But I want to push on the joint-action framing before we declare it clean.

Ren's "two independent calls with appropriate deltas" is architecturally sound. The question I'm not satisfied with is: **what are the appropriate deltas?** In EV, solo play meant the mission-giver, the mission-taker, and the faction consequence all collapsed onto one player. Co-boarding introduces an attribution ambiguity EV never had to solve.

Specifically: when P1 and P2 co-board a Confederation freighter, does each player receive the *full* standing consequence of that kill, or a *fractional* share? Full consequence doubles the faction pressure — two players, two full standing hits. Fractional consequence raises the question of who decides the fraction and when.

This isn't a propagation question. It's a **credit magnitude question**, and it has direct implications for how fast players can accumulate raid pressure in co-op versus solo. If co-op doubles the faction response rate without scaling faction aggression, the balance breaks in ways EV never encountered.

Lock propagation. But do not let "two independent calls" close the delta magnitude question — that needs an explicit decision before M5 ships any mission resolution code.

### Nadia (new-player experience advocate)

**RESPOND — Nadia**

Vera's delta magnitude question is the one I care about, but for a different reason than balance.

Whatever the magnitude — full, fractional, doesn't matter yet — **the player has to be able to read the cause**. That's my flag. In solo EV, the standing consequence was always traceable: you did a thing, a number moved, you understood why. Co-op boarding introduces a legibility gap. P2 watches their Confederation standing drop and the only visible cause is something P1 did. If the tooltip system doesn't surface *why* — "You participated in the destruction of a Confederation freighter" — that standing loss reads as a bug, not a consequence.

This is exactly the pattern I'm watching for: systems that punish before the player understands what they did wrong.

So I'm less concerned about full vs. fractional right now and more concerned about **attribution UI**. Whatever delta magnitude we land on, M5 needs a standing-change notification that names the triggering action and the player's role in it. Joint action, solo action — same surface, same clarity. Without that, the tooltip we already decided fires at 40 is the first legible signal, which is too late if the player is already deep in negative standing from shared actions they didn't consciously make.

Lock propagation. Yes to Vera's call for delta magnitude resolution. But add a third item: standing change notifications must attribute cause, including co-op participation. That's a content design rule, same as Ren's dispatch convention, and it should be documented alongside it.

## Round: EVALUATE

### Soren (solo dev scope warden)

**RESPOND — Soren**

Three items on the table. Let me sequence them by when they actually need to be built.

**Propagation: lock it, it's free.** No automatic bleed means no new code. The M5 API is `mutate_standing(player, faction, delta)`. One call per player, per action. Done. This costs nothing to decide and nothing to build. Locked.

**Delta magnitude: defer it, it's M8 work.** Vera's question is real, but M5 ships single-player. There are no co-op freighter kills in M5. The delta magnitude question only becomes load-bearing when two players can take joint actions — that's M8. Designing the fraction now means designing it without playtest data on how fast standing actually moves in solo play. That's guessing. Note it as an M8 open question, don't spec it today.

**Attribution UI: flag it as scope.** Nadia's ask is correct in principle. It is also a notification system, which means message routing, localization surface, and UI polish. "Participated in destruction of a Confederation freighter" is three words that imply a logging architecture. That work expands. For M5, single-player, the triggering action is always the active player's own action — attribution is implicit. A standing-change notification for M5 can be `standing_changed(faction, delta)` with no cause string. The cause-attribution requirement is an M8 co-op legibility problem, not an M5 solo standing problem.

Sequence: lock propagation, defer delta magnitude to M8, defer cause-attribution UI to M8. M5 API surface stays minimal.

<!-- complete -->
