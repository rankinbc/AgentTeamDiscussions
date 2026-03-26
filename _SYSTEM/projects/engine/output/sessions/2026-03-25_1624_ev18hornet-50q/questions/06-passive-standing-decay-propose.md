### Max (atmospheric flight advocate)

Passive decay is an atmospheric layer question dressed in faction clothing, and I want to name that before we start arguing numbers.

Here's the design truth: the payoff moment — banking over your settlement at altitude, watching your City tier layout from 800m — only *hits* if the airspace has texture. Patrol density is M8, yes. But the *precondition* for patrol density meaning anything is that standing moves without you. If standing only shifts on explicit events, the sky above your settlement is static until you poke it. That's a screensaver. That's not SimCopter, that's a diorama.

Passive decay is the engine that makes airspace *alive*.

But here's my flag before anyone proposes a simple timer: **decay should feel like neglect, not taxation.** The experience design question is — does the player feel *drifting away* from a faction, or does it feel like the game is taking something? Those are completely different feelings. Drifting is atmospheric (literally). Taxation is administrative.

So my agenda for this round is two questions:

1. **Is decay continuous (time-ticker) or event-paced (mission-drought)?** A mission-drought model — standing starts dropping after N days with no faction contact — maps to the atmospheric loop naturally. You've been out of the sky, the faction forgot you exist.

2. **Does decay have a floor above the Hostile threshold?** Passive decay should never cascade you into Hostile. That band requires authored intent, not a clock.

Set those two, and we have something buildable.

### Ren (emergence systems theorist)

Max has correctly identified the design question but I want to push on the *systems interaction* implication before we answer it.

Standing decay is only interesting if it **feeds the raid chain**. Decay → Degraded → increased raid probability → atmospheric intercept → on-foot aftermath. If decay is just a number-reduction mechanic that sits in the faction layer and doesn't pull on anything else, it's administrative regardless of how it *feels*. The texture question Max is asking about is real, but the answer has to come from system coupling, not from choosing the right decay curve.

**On the event-paced vs. timer question:** Mission-drought is correct, but the trigger shouldn't be calendar days — it should be *mission opportunities declined or ignored*. The faction offered contact through the Bar and the player didn't take it. That maps naturally to the existing Bar interaction model and doesn't introduce a new time-tracking surface. The system already knows when missions were offered. Neglect is measured in refusals, not seconds.

**On the Hostile floor:** Fully agree. Passive decay must have a hard floor above the Hostile threshold — call it `DECAY_FLOOR`, a named config constant, set above `HOSTILE_THRESHOLD`. Decay can erode you to Degraded. Getting to Hostile requires an explicit negative action. Those are different player choices and should produce different system states.

This also means decay *rate* and `DECAY_FLOOR` are the two new config constants. Both require playtest data. Both deferred in value, decided in architecture.


<!-- complete -->
