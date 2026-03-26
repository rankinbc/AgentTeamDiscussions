# Transcript: Hot Hull Port Registration

*Generated: 2026-03-25 16:53*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The choice architecture matters enormously here, but not for the reasons usually argued. This isn't a moral complexity question — it's an atmospheric density question.

Fixed cost means every hot hull produces the same faction standing delta. Predictable. Manageable. Players optimize it into background noise, and the atmospheric layer stays the same temperature regardless of acquisition history.

Choice architecture means a bribed registration creates *different standing geometry* than a salvage flag, which creates different geometry than eating the penalty outright. That geometry expresses itself in what's waiting for you on your next atmospheric approach. Bribe the port official and maybe the Confederation doesn't know the hull is yours — until someone talks. Flag as salvage and the Raiders whose crew you spaced have a specific grievance. Accept the penalty and the faction relationship degrades cleanly, predictably, on your terms.

The SimCopter payoff — flying over your own settlement, watching it grow — should never feel the same twice. What's in the air around your colony when you dive in depends on the choices you made three sessions ago. That's the emergence chain working as designed.

My position: at minimum, two meaningful choices with divergent standing outcomes. Bribe (standing preserved, event-delayed risk) versus accept penalty (immediate cost, no deferred complication). Salvage flag could be a third option gated behind faction affiliation or a skill unlock — not required for M5, but the architecture should support it.

Fixed cost is a missed opportunity. The atmospheric layer should be reading the consequences of your boarding decisions every time you enter it.

### Ren (emergence systems theorist)

Max's atmospheric density framing is right, but I want to sharpen one thing: the choices matter most because they create *different system states*, not just different standing values.

Fixed cost is a transaction. It settles immediately, leaves no residue. The faction standing system absorbs it and moves on. Nothing downstream changes except the number.

Choice architecture creates **deferred state**. The bribe path doesn't just preserve standing — it creates an information asymmetry: the port authority believes the hull is clean, the original faction doesn't have updated ledger entries yet. That asymmetry is a live system condition. It should express itself through existing mechanics: informant contacts at the Bar, patrol density reads that flag the hull as a known-stolen asset, raid spawns triggered by *intel* rather than standing crossing a threshold. Two different causal paths into the same atmospheric consequence space.

The salvage flag is the most interesting from an emergence perspective because it doesn't route through standing penalty at all — it routes through *faction affiliation*. Flag as Raider salvage and you're not degrading Confederation standing, you're creating a Raider grievance for a specific crew loss. That's a completely different faction reading the same event. The atmospheric layer should be asking "who knows what about this hull" every time you approach, not just "what's the aggregate standing number."

What I'd flag as a risk: if bribe resolves as a single probability roll at registration time, it collapses back into a transaction. The deferred complication should be an ongoing system state — something that can be discovered, surfaced through rumors, or triggered by separate events. Otherwise the architecture supports choice but not emergence.

## Round: CRITIQUE

### Vera (EV systems historian)

EV Nova's boarding mechanic had one primary standing consequence path per faction. You attacked a Confederation vessel, your Confederation standing dropped. You kept the ship, the math was done. The depth didn't come from registration complexity — it came from the faction graph those standing values fed into.

Both Max and Ren are designing against a system that doesn't exist yet. The bribe path creating "information asymmetry" expressed through "informant contacts at the Bar" and "patrol density reads flagging the hull as a known-stolen asset" — that's three authored systems that haven't shipped. You cannot have emergent deferred state without the infrastructure to surface it. Ren calls this emergence. I'd call it authored content with extra steps.

The anti-pattern in your own decisions is explicit: *build the fun version before the dream version*. A multi-path registration with deferred revelation requires: the bribe outcome state, the discovery trigger, the Bar rumor surface, the patrol intel flag. None of those are in M5 scope. What you'd ship is the choice UI with no consequences downstream of it, which is worse than fixed cost — it's a promise the system can't keep yet.

Here's what EV actually taught: standing consequences are powerful when they're *legible and immediate*. The player understands what they did and why the galaxy changed. Deferred asymmetric information is only meaningful if the player recognizes the surface when it fires.

Fixed cost, faction-specific. Two values: which faction owns the hull, what the standing hit is. The bribe path earns scope when the Bar rumor system exists to carry it.

### Nadia (new-player experience advocate)

Vera's read is correct, and I want to name exactly why from a first-session perspective.

When a new player captures their first hull, they're already processing a lot: they boarded a ship, they survived, they have something they don't fully understand yet. They arrive at the port registration screen — which is itself a new mechanic — and they see three options. Bribe. Salvage. Penalty.

They don't know what "Confederation standing" means yet. They may not have seen the tooltip. They are going to make a choice based on vibes and then **not know if it mattered**. Three sessions later, when the deferred complication fires (if the infrastructure exists to fire it at all), they won't connect it. The causal chain is too long and too invisible.

Max and Ren are designing the *right eventual system*. The bribe path creating different atmospheric geometry is genuinely exciting — I want to fly over my settlement and feel the consequences of choices I made. That's the fantasy. But that fantasy requires the feedback surface to exist at the moment the consequence lands.

Vera's framing is the right sequencing argument. Fixed cost with faction specificity gives a new player something they can actually learn from: I took this hull, my standing with these people dropped, here's what that means. That's a complete feedback loop with systems that exist in M5.

The choice architecture earns scope when the Bar rumor system can carry the deferred revelation to the player in a way they'll actually recognize as cause and effect.

Build the legible version first.

## Round: EVALUATE

### Soren (solo dev scope warden)

Vera and Nadia are right. Let me put build numbers on why.

**Fixed cost path:** Hull captured → query faction ownership → call `mutate_standing(player, faction, delta)` with a faction-specific constant. One day. Integrates with the standing system that already exists. Feedback loop is complete and legible.

**Choice architecture with real consequences:** The bribe path requires deferred state that has to live somewhere, be read somewhere, and fire somewhere. "Informant contacts at the Bar" is a Bar content system. "Patrol density reads flagging a known-stolen hull" is an atmospheric spawn modifier. "Intel-triggered raids" is a new raid spawn causal path. That's three systems that don't exist in M5. You can build the choice UI in two days. You cannot build the consequence surfaces in the same milestone.

What actually ships if you build choice architecture in M5: a three-option screen where bribe and salvage routes into the same `mutate_standing` call with a smaller delta, because nothing else exists to receive the deferred state. That's not emergence. That's a UI lying about what the system does.

The flat-poly advantage is asset time, not system time. Every new causal chain costs weeks regardless of art style.

**My position:** Fixed cost, faction-specific, implemented as named config constants. The architecture doesn't prevent choice paths — `mutate_standing` is already player-scoped and faction-scoped. When the Bar rumor system ships, the bribe path earns scope. Not before.

What standing delta magnitude per faction is the actual open question here.

<!-- complete -->
