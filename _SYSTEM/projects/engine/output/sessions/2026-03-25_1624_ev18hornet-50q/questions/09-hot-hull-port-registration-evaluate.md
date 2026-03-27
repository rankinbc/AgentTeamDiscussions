### Soren (solo dev scope warden)

Vera and Nadia are right. Let me put build numbers on why.

**Fixed cost path:** Hull captured → query faction ownership → call `mutate_standing(player, faction, delta)` with a faction-specific constant. One day. Integrates with the standing system that already exists. Feedback loop is complete and legible.

**Choice architecture with real consequences:** The bribe path requires deferred state that has to live somewhere, be read somewhere, and fire somewhere. "Informant contacts at the Bar" is a Bar content system. "Patrol density reads flagging a known-stolen hull" is an atmospheric spawn modifier. "Intel-triggered raids" is a new raid spawn causal path. That's three systems that don't exist in M5. You can build the choice UI in two days. You cannot build the consequence surfaces in the same milestone.

What actually ships if you build choice architecture in M5: a three-option screen where bribe and salvage routes into the same `mutate_standing` call with a smaller delta, because nothing else exists to receive the deferred state. That's not emergence. That's a UI lying about what the system does.

The flat-poly advantage is asset time, not system time. Every new causal chain costs weeks regardless of art style.

**My position:** Fixed cost, faction-specific, implemented as named config constants. The architecture doesn't prevent choice paths — `mutate_standing` is already player-scoped and faction-scoped. When the Bar rumor system ships, the bribe path earns scope. Not before.

What standing delta magnitude per faction is the actual open question here.


<!-- complete -->
