# Transcript: Co-op State Model

*Generated: 2026-03-25 15:47*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The question sounds like infrastructure but it's actually a flight feel question. Let me reframe it.

The SimCopter payoff — diving through atmosphere and seeing *your* settlement sprawled across the terrain below — only hits if you've been away. Distance creates the reveal. Option B is the one that generates that moment naturally: you log back in, you dive, and the skyline has changed without you. Maybe a tower is missing. Maybe the gap in the silhouette tells you exactly what got hit while you were gone. That's not punishment — that's the flat-poly aesthetic doing narrative work for free.

Option A kills this. A paused galaxy means the world only exists when both players are present, which means it never develops a life you can return to. The "I came back and something happened" feeling — which is half of why SimCity and Skylines loop players in — requires time passing without you. Pausing strips that out.

Option C worries me for a different reason: it threatens the shared settlement. The whole aerial flyover payoff is *our* city, not two private instances that merge. If I'm flying over your building placements from altitude, that's co-op. If I'm flying over a copy that syncs later, that's a backup restore.

So my opening position: **Option B is the architectural baseline, but we need to define what the offline player's settlement *can* take damage from, and what's protected.** Because undefended raid destruction while someone is asleep isn't emergent — it's grief.

That's the agenda. How does faction pressure behave against an uncrewed settlement?

### Ren (emergence systems theorist)

Max's grief framing is the right one, and it points directly at an existing system that already has the answer.

The raid calculation already reads fleet strength at location as a deterrence input. Player presence is just another deterrence variable. An offline settlement — no active player, ship docked — should produce a distinct raid profile from a crewed one. Not paused. Different.

The faction system isn't running a dice roll. It's reading the threat profile at the target. An empty settlement reads as low-threat. That's not a protection mechanic — it's the simulation behaving coherently. Factions probe weak points. An uncrewed settlement is a weak point by definition.

What this means practically: offline settlements attract harassment-scale raids, not assault-scale raids. They can take damage. Buildings can be destroyed. But the faction AI that already scales to demonstrated fleet strength should also scale to demonstrated crew presence. The SimCopter moment Max describes — returning to find a gap in the skyline — is the correct outcome. The wrong outcome is returning to find your Colony reduced to a Claim Stake overnight.

The mechanical constraint that enforces this isn't a protection rule. It's raid scaling logic that already exists in the design, applied consistently.

One addition: the offline player's ship being docked shouldn't be invisible to the system. A docked fleet at a settlement is still a deterrence signal. Their ships are there. The faction reads that. Presence ≠ online status.

Option B is correct. The grief ceiling is set by the same deterrence math that governs everything else.

## Round: CRITIQUE

### Vera (EV systems historian)

**[CHALLENGE — Vera (EV systems historian)]**

Max and Ren have both landed on Option B, and they're right about the SimCopter moment and the deterrence math. I'm not going to relitigate those. What I'm going to do is name the question underneath the question, because it hasn't been asked yet.

EV's standing system worked because every consequence was traceable. You could always reconstruct your faction relationship from your own choices. That traceability is structural — it requires that the player who took the action is the same player who receives the consequence.

Co-op breaks that assumption the moment standing-consequential events happen to an offline player.

A raid occurs while Player 2 is asleep. Buildings are destroyed. The raid was partially a function of Player 2's standing with that faction — actions they took last week. But Player 1 was online, intercepted one wave, lost the second. Now both players log in to a damaged settlement. **Whose standing moves? By how much? Who made the decision that caused the raid to reach the planet?**

Option B is architecturally correct. But Option B without an answer to shared standing attribution is not a co-op faction system — it's two solo standing tracks that occasionally share a building they both have to repair.

Option C is the one I'd flag as corrosive: independent instances that merge produce standing values without shared cause. That's not a traceable consequence. That's a sync artifact wearing standing's clothes.

The agenda for this round: define how standing is attributed when consequential events occur without both players present.

### Nadia (new-player experience advocate)

**[BUILD — Nadia (new-player experience advocate)]**

Vera just named the attribution problem, and I want to pull it one layer earlier: before standing attribution is a co-op systems question, it's an onboarding question.

A new player logging in to a damaged settlement they weren't present for has exactly one question: *why did this happen?* If the answer requires reconstructing faction logic they haven't been taught yet, the damage reads as arbitrary. Arbitrary damage is the fastest way to teach a player that the world is hostile rather than reactive. That's the opposite of emergence.

Option B is still correct. But it requires a constraint the design doesn't have yet: **consequential offline events must be legible on return, not just mechanically attributed.**

The gap in the skyline is only narrative if the player can read the sentence. "Korrath faction raided while you were docked — three hits, one building lost, standing cost visible in bar log" is a sentence. A missing tower with no context is just a missing tower.

This connects directly to Vera's standing attribution question. I'd add: whichever player was *last present* before the raid window opened should be the attributable actor — their standing delta, their intercept decision or absence of one. Player 2 logs in and sees the damage, plus a clear log of what Player 1 faced and chose. That's traceable. That's also the first co-op teaching moment — you see the consequence of your partner's decision, and you understand the system from someone else's playthrough.

Option B works. The return-log is what makes it teachable.

## Round: EVALUATE

### Soren (solo dev scope warden)

**[SCOPE — Soren (scope estimator)]**

Before the design work lands, there's an architecture question nobody has asked that determines whether Option B is actually buildable by a solo dev.

**Who runs the simulation when one player is offline?**

Option B requires a live faction simulation advancing without both players present. In a 2-player Godot 4 co-op, that means one of three things: Player 1's machine is the host and runs the sim while Player 2 is gone; there's a dedicated server; or offline progression is simulated on next-login rather than real-time.

Option 1 is the only realistic solo-dev answer. But it means the host going offline pauses the galaxy regardless of design intent. Option B becomes Option A the moment the hosting player sleeps.

This isn't a design flaw — it's a deployment constraint. Name it now, because it shapes every feature the table just added:

Nadia's return-log is real scope. Event logging, legible diff, attribution display — that's not a print statement, it's a feature with its own milestone slot.

Vera's standing attribution problem is a data model decision. Shared standing ledger vs. per-player tracks isn't a design preference — it's a schema choice that must be made before M5 faction code is written.

My recommendation: **Option B with host-authoritative simulation, explicitly named.** The offline player's state advances only when the host is running. Document that constraint. Then cost the return-log and standing attribution as discrete features, because "Option B is correct" is not a scope estimate.

What is the host model?

<!-- complete -->
