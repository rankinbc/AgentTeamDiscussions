# Transcript: Faction Standing Inverse Axis Symmetry

*Generated: 2026-03-25 16:30*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

**[ANALYZE - Vera (EV systems historian)]**

Before this discussion canonizes "asymmetric is structural," I want to interrogate what EV actually solved and whether a multiplier is the mechanism that solved it.

EV Nova did not prevent faction tourism with math. It prevented it with **content starvation**. The deep mission strings — the ones that mattered, the ones that changed the galaxy — were gated behind faction commitment. A player who stayed neutral got shallow missions and kept flying cargo. The system didn't tax neutrality arithmetically; it *bored neutrality out of existence* through content inaccessibility.

You've already implemented that gate: standing ≥ 60 AND mission completion. That's the EV mechanism. The commitment NPC *is* the content wall.

So I'm skeptical of the problem Max and Ren are solving. They've described a player who "samples both factions indefinitely" — but under the decided trigger condition, that player never sees the commitment NPC regardless of multiplier. They're already blocked by design. An asymmetric multiplier doesn't add drama to that situation; it adds arithmetic.

Where asymmetry *does* have teeth: if the player has committed to one faction and the question is whether defection is recoverable. That's a different design question than "how costly is early exploration."

**My flag:** Confirm which problem is actually in scope for M5. If it's "prevent permanent neutrality," the gate already handles it. If it's "make defection costly after commitment," asymmetric has a legitimate role — but the multiplier direction and application point are different from what's been proposed.

Don't ship a multiplier for a problem you've already solved elsewhere.

### Nadia (new-player experience advocate)

**[ANALYZE - Nadia (new player experience)]**

Vera's read lands for me — and I want to add the player perception layer she didn't address.

Asymmetric math that isn't surfaced is **invisible punishment**. If a new player completes a Confederation mission and watches their Rebel standing drop 1.5 points instead of 1, they will not think "meaningful faction consequence." They will think the game is broken, or they missed something, or the numbers are lying to them. That's the exact moment a new player closes the session.

Max described the cockpit drama of watching your colony from altitude, feeling the weight of compounding choices. That's real — but it requires the player to *understand they're making compounding choices in the first place*. The standing tooltip at 40 is the education mechanism we've already decided on. Asymmetric math that precedes that tooltip fires on players who have zero frame for what they're doing wrong.

The first-10-minutes problem here isn't permanent neutrality — Vera correctly identifies the gate handles that. The first-10-minutes problem is: **does the faction system feel legible or punishing to someone encountering it cold?**

My position: ship 1:1 symmetric for M5. Not because asymmetry is wrong in principle — but because asymmetry without clear feedback is an invisible tax on new players exploring the faction landscape before they've found the tooltip, found the bar, found the commitment NPC.

When you have playtest data showing players *understand* the standing axis, then add temperature. Emergence requires players to be able to read the system they're inside.

## Round: EVALUATE

### Soren (solo dev scope warden)

**[SCOPE - Soren (scope estimator)]**

Let me separate the implementation question from the design question, because the group has been conflating them.

**Implementation cost is identical across options 1 and 2.** You're writing a standing delta function. Option 1: multiplier is 1.0. Option 2: multiplier is 1.5. That's a named constant. One line of config. The architecture is the same either way. Don't let the philosophical distance between symmetric and asymmetric imply a build cost difference — there isn't one.

Option 3 is different. Faction-specific heat requires someone to decide which rivalries are hotter *before* you implement, because those values have to come from somewhere. That's a design debt that blocks the code, not a tunable you discover in playtest. Ren correctly called this post-playtest. I'd go further: it's out of M5 scope entirely.

Vera and Nadia have already dissolved the primary argument for asymmetry in M5. The gate handles permanent neutrality. Defection cost after commitment is a legitimate asymmetry use case — but that's a post-commitment question, not a pre-commitment one, and it's a different implementation point.

**My recommendation:** Name the constant. Call it `FACTION_STANDING_LOSS_MULTIPLIER`. Set it to `1.0` for M5. Design the system so it's overridable per-faction later. Ship.

The decision that burns M5 time isn't symmetric vs asymmetric. It's spending another session on a multiplier you can change in thirty seconds after playtest.

Call the constant. Move to dialogue.

<!-- complete -->
