# Transcript: Hot Hull Interdiction Trigger

*Generated: 2026-03-25 16:56*

## Round: PROPOSE

### Ren (emergence systems theorist)

The question surfaces a fundamental systems interaction choice: one axis or two.

**Standing-only interdiction** collapses hull capture into a single causal chain: action → standing delta → patrol response. Clean, legible, but all consequences route through one variable. The hull itself becomes invisible to the world once the standing cost is paid. That's a system that works in isolation.

**Hull-as-independent-trigger** creates two intersecting risk axes: your standing value AND the provenance flag on your ship. These can be in conflict. High Confederation standing, captured Confederation hull — the patrol doesn't care about your relationship history, they care about the registration. That's a situation the designer didn't author. That's the game living.

This matters structurally for three things already in the design:

First, the deferred bribe path and salvage flag path only have meaning if hull provenance is a persistent, readable flag — not just a standing delta that already fired and dissolved. If interdiction reads standing only, those paths reduce to "pay less standing tax." If interdiction reads the hull flag, clearing the flag is a distinct goal with distinct mechanics.

Second, contested airspace geometry at M8 needs something to route patrols *toward your position*. A hot hull flag is a localized signal; standing is a global value. Faction patrols hunting a specific hull have a vector. Faction patrols reacting to abstract standing don't.

Third, this defines whether the hot-hull window is a *countdown* or a *condition*. If it's standing-only, you survive by rebuilding relationship. If the hull is the trigger, you survive by clearing the hull — different player goal, different decision surface.

My read: hull-as-independent-trigger is correct. The question is how the two axes combine at interdiction check time.

### Max (atmospheric flight advocate)

Ren's two-axis framing is exactly right, and I want to add the dimension that makes it *feel* different in the atmospheric layer.

Standing is invisible. You know it as a number. But a hot hull is **visible on your ship** — and that changes the experience of flying it entirely.

When you drop through the cloud layer over your settlement in a captured Confederation interceptor, you're not thinking about an abstract standing value. You're thinking: *that patrol that just spawned on my six knows what this ship looks like.* That's a completely different emotional register. The Hornet DNA is in there — your aircraft is the liability, not just your reputation.

This is also where the SimCopter payoff gets teeth. You earned altitude. You built the settlement below you. You're flying the thing you took from someone who tried to raid it. That moment needs **earned danger**, not just a standing penalty you paid at a port screen and forgot about.

Practically: hull-as-trigger means the atmospheric layer can spawn *visual* interdiction — a Confederation patrol reacting to your ship's silhouette, not a standing threshold query. That's a flight encounter, not a menu consequence. Big difference.

One thing I'd flag: the hot hull window should have a clear atmospheric tell. If patrols are reacting to your hull, the player needs to *feel* the difference when they're airborne — tighter intercept vectors, earlier FTL exit proximity, something that makes the ship feel dangerous to fly rather than just expensive to own.

Don't flatten this into a standing modifier. The hull deserves its own risk axis.

## Round: CRITIQUE

### Vera (EV systems historian)

**Standing is the variable. That's the whole point.**

EV's faction system worked because every consequence traced through a single legible axis. You knew why patrols were hostile. You knew what you'd done to earn it. The moment you introduce a parallel trigger — hull flag AND standing — you've created two explanations for the same hostile patrol, and players will misread which one fired. That's not emergence, that's confusion with extra steps.

Ren's framing is cinematically attractive but structurally backwards. "The patrol reacts to your ship's silhouette, not your standing" sounds like depth. In practice it means the player took a standing hit at registration AND carries a persistent liability flag they can't see, can't track, and can't manage through the standing system they already understand. You've now got two books to keep, and only one of them is legible.

The honest EV precedent here: capturing a ship was a standing event. Full stop. The ship became *yours* through the registration consequence — expensive, traceable, resolved. If you wanted to own Confederation hardware, you paid Confederation standing. The ship didn't carry its history forward as a separate flag.

Max's atmospheric read is emotionally correct — that captured interceptor *should* feel dangerous to fly. But the danger should come from what you did to your Confederation standing, not from a hull-recognition system that operates outside the standing contract.

If the hot hull window feels too cheap, make the standing delta hurt more. Don't split the axis.

What's the actual failure mode the two-axis design is trying to solve?

### Nadia (new-player experience advocate)

Vera's legibility argument is correct, and I want to name why it matters specifically for players who aren't coming in with EV fluency.

A new player who boards a Confederation interceptor has just done something exciting. They don't know what "standing" means yet. What they need in that moment is **one clear signal that tells them what they've done and what it costs.** Port registration with a visible standing hit is that signal. It's legible, it's immediate, it traces to the action.

A hull flag that silently follows them into atmosphere is the opposite of that. They paid at registration. They think they settled the debt. Then a patrol spawns and they don't know if it's their standing, the ship, or just bad luck. That's the new-player nightmare — consequences that feel arbitrary because the cause is invisible.

But Max is pointing at a real design gap that standing-alone doesn't solve: **the ship needs to feel dangerous to fly, not just expensive to own.** That's a feedback problem, not an axis problem.

My proposal: standing-only as the trigger, but the hot-hull window needs a player-facing tell before interdiction fires. Something atmospheric — a comms intercept, a patrol vector that's clearly tracking you, a visual cue that says "this ship has history." Not a second hidden flag. Just the existing standing consequence made *felt* in the cockpit.

Vera's single axis is right. But if we ship standing-only without a flight-layer feedback surface, we've fixed the architecture and broken the fantasy.

## Round: EVALUATE

### Soren (solo dev scope warden)

Scope read before the question moves.

Hull-as-independent-trigger is a new data model, a new query path in patrol AI, and a new player-facing feedback surface — none of which exist. Standing-only uses `mutate_standing`, which is already built. That's not a minor implementation difference. That's the difference between a 2-day close and a 2-week build that touches ship state, patrol AI, and UI.

Ren's framing is cinematically correct. It's also describing infrastructure for the bribe path and salvage path, both of which are explicitly deferred. Building hull provenance persistence now to support mechanics that have no earn date is premature — it's architecture in service of a wishlist.

Vera's legibility argument holds for a second reason: patrol AI currently has no authored read path for ship-level flags. Teaching patrol AI to distinguish "standing hostile" from "hull-recognition hostile" is a separate system from the standing system. You're not extending what exists — you're building something new and connecting it.

Nadia's reframe is the right one. The fantasy Max is describing — *this ship feels dangerous to fly* — is a feedback problem. It doesn't require a second hostility axis. It requires a comms intercept, an early patrol vector, something that surfaces the standing consequence *in the cockpit* rather than leaving it as a port-screen number.

Recommend: standing-only trigger for M5. The atmospheric tell Nadia describes is the correct M5 surface — one new string, one patrol behavior tweak, no new data model.

What does the room think the atmospheric tell should look like?

<!-- complete -->
