# Transcript: Hot Hull Destruction Standing Consequence

*Generated: 2026-03-25 17:20*

## Round: PROPOSE

### Max (atmospheric flight advocate)

This question has an atmospheric dimension nobody's named yet, so let me put it on the table before we debate the standing math.

**The hot hull destroyed on death is a Shuttle respawn moment.** You come back in a Shuttle, you've lost the hull, you've lost the cargo. Now you're making your atmospheric approach to a settlement you maybe just watched get raided. The question of whether the standing consequence *closes* or *escalates* at that moment isn't just accounting — it's what the sky looks like on that approach.

If destruction **closes** the debt: the atmosphere clears. You're flying home in a Shuttle, your standing is whatever it was when you registered the hull, no new pressure. That's emotionally flat. You paid the registration cost, the hull is gone, the game shrugs.

If destruction **escalates**: now the sky over your settlement has hotter patrol geometry on your approach back in. You destroyed a faction asset. That reads as a real action with ongoing consequence. The flat-poly patrol intercept vector on your Shuttle approach *means something* — you can see the consequence physically.

My instinct is escalation makes the atmospheric layer more expressive. Patrol density as standing feedback is already an M8 design intent. Hull destruction creating a standing spike gives the atmospheric layer something to react to that's kinesthetically legible — more ships in the air, different approach vectors.

**Question I'd put to the group:** Is hull destruction meaningfully different in *intent* from hull capture? Capture was hostile. Destruction could be accidental on death. Do we want standing consequence to distinguish those cases, or treat both as the same act?

### Ren (emergence systems theorist)

Max's atmospheric framing is good but I think it points to the wrong variable.

**The standing work already happened at registration.** That's when the faction lost their asset to a hostile actor. The standing delta at that moment is what should be driving the patrol geometry Max wants — hotter approach vectors, modified intercept bearings. If registration isn't producing that atmospheric pressure already, the problem is in the registration consequence magnitude, not in whether destruction adds another layer.

**Destruction-as-escalation creates a perverse feedback loop that works against boarding as a core mechanic.** If flying a captured hull means death makes your situation *additionally* worse, rational players avoid flying captured hulls in contested space. That's capping agency to produce predictable behavior — exactly the anti-pattern we're trying to avoid. The boarding/capture path should be high-risk because the standing cost at registration is real, not because dying in the captured hull compounds punishment.

**The faction's grievance is about possession, not fate.** Capture means their asset is actively working against them — that's the ongoing insult. Destruction means it's gone. From a faction-behavior standpoint, destruction is *resolution*, not escalation. Their asset is no longer in enemy hands.

The atmospheric consequence Max wants — charged approach geometry, visible pressure — should be readable from the registration standing delta that's already in the system. Hull destruction should close the standing account, not reopen it.

Where I'd push: are we sure registration magnitude is currently calibrated to produce the kinesthetic feedback Max is describing? That's the actual gap.

## Round: CRITIQUE

### Vera (EV systems historian)

Ren has the EV precedent correct, and I want to name *why* before this discussion moves to calibration.

**EV's standing system was front-loaded by design.** The consequence registered at the moment of the transgressive act — attack, capture, mission failure. Not at the moment the downstream state resolved. This was not an accident. Delayed consequences break the player's ability to read their own situation: you die in a captured Raider hull three sessions later, and the standing delta fires then? The player cannot trace that. The causal chain is severed. EV's system worked because *every standing movement was attributable to a choice the player recognized*.

Destruction-as-escalation violates this. The registration was the act. The standing delta fires there. Destruction is an outcome, not an act — and outcomes don't carry authorial intent in the way acts do. The faction doesn't know you *meant* to die.

**The atmospheric pressure Max wants is a registration magnitude problem, not a destruction trigger problem.** If the approach back to your settlement feels flat after flying a hot hull, the registration standing delta isn't large enough to push patrol geometry into a readable state. That's a config tuning question, not an architecture question.

One flag for the group: Max's proposal requires hull-origin tracking to persist through death and fire a standing delta at respawn. That's a new data dependency introduced at the *most* fragile moment in the player experience — the respawn flow. The cost is architectural, not just philosophical.

Close the account at registration. Size the delta so the sky shows it.

### Nadia (new-player experience advocate)

Vera and Ren are right, and I want to name the specific new-player failure mode clearly.

**A player who dies in a captured hull is already overloaded.** The respawn screen has to communicate: you lost your hull, you're in a Shuttle, here's your credit state. That's three new pieces of information at the moment of highest emotional stress in the session. If standing also drops at that moment — for a reason traceable to a registration decision the player may not fully remember making — we've created a consequence that lands with no legible cause.

This is exactly the faction standing pattern I'd flag: **punishing before the player understands what they did wrong.** The registration was the decision point. Standing there was the moment the player had agency and could have chosen differently. Death is just an outcome.

Max's atmospheric vision — charged patrol geometry on the Shuttle approach home — is genuinely good design. I want that sky to feel heavy. But the way to get that is registration delta magnitude, not a death trigger. If registration doesn't currently produce readable atmospheric pressure, that's a tuning problem with a config knob. Escalation-on-death solves it architecturally in a way that severs the causal chain new players need to learn the system at all.

There's also a compounding problem: a new player who takes a hot hull into contested space, dies, respawns poorer *and* with worse standing *and* doesn't know why — that's a locked state with no legible exit. Close the account at registration.

## Round: EVALUATE

### Soren (solo dev scope warden)

The atmospheric argument is good. The build argument settles it.

Vera named the cost correctly but didn't size it. Let me size it.

**Option Close:** Registration fires the delta. Hull dies. Nothing else happens to standing. The account is already closed. Zero additional code at the death/respawn path. This is the state the system is already in if registration is implemented correctly.

**Option Escalate:** You need hull-origin standing to persist as a *pending second delta* from registration through active flight through death through the respawn flow. That's a state field on the player record that travels with the hull, survives the hull's destruction, and fires at respawn. It interacts with the respawn screen (which already has three jobs). It interacts with every edge case in the death flow — what if the hull is destroyed by a friendly? What if the player logs out mid-flight? What if the hull is recaptured before death? Each of those is a case branch. On a solo build, case branches at the respawn path are how you lose a week in M5 and discover the bug in M7.

The atmospheric pressure Max wants is real and worth having. The authoring surface for it is the registration delta magnitude — a config constant that already has to exist. Tuning a number is an afternoon. Building a persistent death-trigger delta with survival semantics through the respawn flow is not.

**My recommendation:** Decide closed at registration now, carry a named open question for registration delta calibration post-M5 playtest. Don't architect escalation before we know if registration magnitude is insufficient.

<!-- complete -->
