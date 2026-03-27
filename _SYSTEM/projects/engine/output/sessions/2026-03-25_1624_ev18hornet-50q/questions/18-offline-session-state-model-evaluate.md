### Soren (solo dev scope warden)

The model is already decided. Elapsed-time reconstruction is not a design tradeoff — it's a project-ending scope item. A faithful offline simulator requires tick-accurate standing tracking, timestamped event queues, and a replay engine you'd build instead of the game. Last committed save is not a compromise. It's the only model a solo dev can ship.

What's not settled is implementation sequencing, and that's where scope risk lives.

**Sequential compounding** is correct and cheap in single-player. One loop: for each offline raid, calculate composition from current standing, apply damage, apply standing delta, advance. Three raids in, maybe 2 days of implementation. Ren's point about compounding assault composition is a loop variable, not a new system.

**The co-op authoritative state problem** is where this discussion needs to land before M8 touches the reconnect path. Nadia's "higher threat standing" rule is the right answer — not because it's elegant, but because it's *implementable without new data*. It resolves to a `max()` call on two standing values at raid spawn time. No attribution surface required, no new fields. The comms intercept already fires; it names raid count, not whose standing drove composition. That's sufficient legibility for M7.

What I'd flag as a pending scope decision: does the comms intercept string need to attribute fault to a player in co-op? That's a content design and notification surface question that Nadia raised. If yes, it belongs on the M8 standing change cause attribution work, which is already open. If no, the "higher threat" rule ships in M7 with no additional surface.

That's the remaining decision. Everything else is implementation.


<!-- complete -->
