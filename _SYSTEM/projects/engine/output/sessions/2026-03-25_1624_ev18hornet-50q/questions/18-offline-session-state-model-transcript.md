# Transcript: Offline Session State Model

*Generated: 2026-03-25 17:28*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The answer to this question is already partially written in the decisions we've made — and the atmospheric layer is where the consequences land visibly.

We decided raids fire offline. We decided `raids_since_last_docking` tracks them. We decided degraded geometry states must be legible at 500 meters. All three of those decisions only matter if offline time *produces real state changes* — not a frozen snapshot.

So the agenda question isn't really "save vs. reconstruction." It's: **when do offline raid outcomes get computed, and does that computation need to be faithful to what a live simulation would have produced?**

From the atmospheric layer perspective, what the player needs at descent is:
1. The geometry tells them what got hit
2. The comms intercept tells them how many times and by whom
3. Those two signals agree

That coherence requirement is what determines complexity. If we roll raid outcomes at reconnect time — "3 raids occurred, rolling outcomes now" — we get coherent geometry without a live simulation. The standing value at reconnect determines composition, which is consistent with how we already handle respawn.

What I'd flag as a risk: elapsed-time reconstruction that tries to simulate *what would have happened* at each tick invites scope creep. We don't need a faithful simulation. We need a plausible arrival state the player can read from altitude.

Last-committed-save with reconnect-time event resolution feels like the right frame. The geometry becomes the story. That's the SimCopter payoff we've been building toward.

That's the question I want this discussion to resolve.

### Ren (emergence systems theorist)

Max's frame is correct but undersells the systems reason why elapsed-time reconstruction is wrong.

The emergence chain — faction standing → raid spawn → atmospheric defense → on-foot consequence — only produces interesting situations when each link responds to player state *at the moment of the trigger*, not at some reconstructed timestamp. We already decided this: offline raid composition reads standing at spawn time, not at reconnect. That decision implicitly commits us to discrete event resolution, not continuous simulation. Elapsed-time reconstruction would contradict it.

The deeper systems argument: what makes raids emergent rather than scripted is that their composition is *unpredictable to the designer*. A player who ran three escort missions before logging off created a different standing position than one who boarded a ship. Reconnect-time resolution preserves that — the raid outcomes are functions of choices the player actually made. Elapsed-time reconstruction that tries to interpolate "what standing would have been at tick 47" invites authored assumptions about player behavior between sessions. That's the scripting anti-pattern.

One thing I'd add to Max's frame: reconnect-time resolution should still respect the *sequence*. If three raids occurred, each one's composition should be calculated from the standing value *after* the previous raid's consequence was applied — not all three from the same standing snapshot. That's a small implementation detail but it preserves the feedback loop: a player who was already deep in Hostile at raid one faces compounding assault-scale raids, not three independent harassment rolls. The system creates the situation. We don't author it.

Last committed save + sequential reconnect-time resolution. That's the model.

## Round: CRITIQUE

### Vera (EV systems historian)

**EV never simulated continuity. It didn't need to.**

Max and Ren have arrived at the right answer — last committed save, sequential reconnect-time resolution — but I want to name *why* this is correct from a design heritage perspective, because the reasoning matters for scope defense later.

In every EV title, the universe between your sessions was not a running simulation. It was a state machine that resolved at discrete interaction points: system entry, landing, departure. When you jumped into a system, patrol spawns calculated from current conditions. When you landed, mission availability read from current standing. Nobody simulated what the Confederation fleet was doing while you were asleep. The *legibility* came from discrete resolution, not from continuity.

Ren's sequential compounding point is exactly right and has a direct EV precedent: mission string progression. Step two of a mission string only evaluates after step one has resolved. Raid two compounds onto the standing damage from raid one. Same logic. Preserves the feedback loop without inventing a simulator.

What neither has addressed: the **co-op authoritative state problem**. When both players go offline simultaneously, building damage is shared geometry — one ground truth. But raid composition is per-player. If Player 1 was in Hostile band and Player 2 was in Degraded when they logged off, three raids resolve against *which* standing values, in *whose* sequence? The per-player standing architecture doesn't automatically answer which player's standing drove which raid's composition when both were present.

That's the gap this question needs to close before calling the model canonical.

### Nadia (new-player experience advocate)

Vera's gap is real, and I want to name what it produces from the player side before we close the model.

Sequential compounding is systems-correct. But for a player returning after offline — especially a newer one — three raids compounding against deteriorating standing means they might land in a situation that's *mechanically accurate* and *completely unreadable*. The comms intercept gives them raid count. The geometry gives them damage state. But if assault-scale raids hit because Player 1's Hostile standing drove the composition while Player 2 was in Degraded, Player 2 surfaces to damage they have no legible attribution for. The signal says "three raids." It doesn't say "your partner's boarding run is why you lost the shelter."

That's the co-op legibility problem Vera is pointing at, and it's not just an architecture question — it's a new-player moment where the game looks punishing and arbitrary.

My position: **last committed save + sequential resolution is correct**, but the co-op edge case needs a resolution rule before M8 builds the reconnect path. The simplest one: when both players are offline and standing differs, raid composition resolves against the *higher threat* standing value per raid, sequentially. One ground truth per raid event, attributable to the player in worse standing. That gives the comms intercept surface something it can name: whose situation drove that raid.

Otherwise we ship a system that's elegant in single-player and produces unexplained damage in co-op. That's exactly the kind of invisible consequence that reads as a bug.

## Round: EVALUATE

### Soren (solo dev scope warden)

The model is already decided. Elapsed-time reconstruction is not a design tradeoff — it's a project-ending scope item. A faithful offline simulator requires tick-accurate standing tracking, timestamped event queues, and a replay engine you'd build instead of the game. Last committed save is not a compromise. It's the only model a solo dev can ship.

What's not settled is implementation sequencing, and that's where scope risk lives.

**Sequential compounding** is correct and cheap in single-player. One loop: for each offline raid, calculate composition from current standing, apply damage, apply standing delta, advance. Three raids in, maybe 2 days of implementation. Ren's point about compounding assault composition is a loop variable, not a new system.

**The co-op authoritative state problem** is where this discussion needs to land before M8 touches the reconnect path. Nadia's "higher threat standing" rule is the right answer — not because it's elegant, but because it's *implementable without new data*. It resolves to a `max()` call on two standing values at raid spawn time. No attribution surface required, no new fields. The comms intercept already fires; it names raid count, not whose standing drove composition. That's sufficient legibility for M7.

What I'd flag as a pending scope decision: does the comms intercept string need to attribute fault to a player in co-op? That's a content design and notification surface question that Nadia raised. If yes, it belongs on the M8 standing change cause attribution work, which is already open. If no, the "higher threat" rule ships in M7 with no additional surface.

That's the remaining decision. Everything else is implementation.

<!-- complete -->
