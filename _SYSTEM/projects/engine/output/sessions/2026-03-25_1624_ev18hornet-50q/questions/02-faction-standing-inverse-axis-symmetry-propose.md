### Max (atmospheric flight advocate)

Here's why this question matters more than it looks: the inverse axis ratio is the **drama dial for your atmospheric layer**.

Hear me out. If it's 1:1 — one point with Confederation costs exactly one with Rebels — then faction exploration is free tourism. Players dip into both, take what they want, and never feel the gravity of a choice. Clean math, flat experience.

But if it's **asymmetric** — say, 1 point gained costs 1.5 lost on the opposing axis — then faction standing has *weight*. And weight is exactly what you want when a player is flying home at altitude, watching their colony from 2000m up. Because at asymmetric cost, the question in the cockpit isn't just "which faction do I prefer" — it's "how deep am I already in, and can I afford to touch the other side?"

That's the SimCopter moment with stakes. Your settlement is down there. The faction you've been drifting away from has patrols. You made a series of small choices, and now the world reflects them from above.

Three options for the agenda:

1. **1:1 symmetric** — neutral, exploration-friendly, no penalty for sampling
2. **Fixed asymmetric** — e.g., 1 gained = 1.5 lost, constant across all factions
3. **Faction-specific asymmetric** — some rivalries are hotter than others; Confederation/Rebel might be 1:2, smaller factions 1:1.2

My read: option 3 is the richest but requires design investment. Option 2 is implementable in M5 with a single multiplier constant.

What's the group's appetite for faction-specific heat?

### Ren (emergence systems theorist)

Max framed this correctly as a drama dial. I want to map what that dial is actually controlling in the emergence chain.

Symmetric 1:1 has a specific failure mode: it enables permanent neutrality. A player who stays near standing 50 with both factions never triggers the chain we care about — standing doesn't drop enough to invite raids, raids don't happen, atmospheric intercepts don't happen, settlements never need defending. The emergence chain **requires faction pressure**, and 1:1 lets players bleed it off indefinitely by sampling both sides in equal measure.

Asymmetric forces a drift. Once you've done three Confederation missions, the cost of staying neutral with Rebels is compounding. That compounding is what makes the cockpit moment Max described feel earned — the player *made* choices that pushed them into a defined relationship, and now the world reflects it.

On option 3 (faction-specific heat): I agree it's the richest model, but I'd flag it as a post-playtest tunable rather than an M5 design input. The reason: you need to see the system run before you know which rivalries need higher temperature. Baking faction-specific multipliers in before first playtest is premature optimization.

**My recommendation:** Ship M5 with a single asymmetric multiplier — something in the 1:1.5 range — as a named constant in config. Design the system so that constant is faction-overridable later. That gives you option 2 now and option 3 when you have data.

The multiplier value itself is tunable. The decision that matters is: **asymmetric, not symmetric**. That one is structural.


<!-- complete -->
