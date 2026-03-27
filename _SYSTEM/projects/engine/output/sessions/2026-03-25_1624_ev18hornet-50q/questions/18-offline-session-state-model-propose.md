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


<!-- complete -->
