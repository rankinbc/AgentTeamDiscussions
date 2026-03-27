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


<!-- complete -->
