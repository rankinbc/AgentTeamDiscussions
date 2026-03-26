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


<!-- complete -->
