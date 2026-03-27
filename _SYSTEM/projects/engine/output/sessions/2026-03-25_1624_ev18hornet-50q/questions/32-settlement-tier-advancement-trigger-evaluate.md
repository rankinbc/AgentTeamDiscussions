### Soren (solo dev scope warden)

**[AGENDA - Soren (scope estimator)]**

Before this group picks a trigger, I need the room to hold one number: each advancement condition is a separate build item, and they stack.

A resource investment threshold is a single integer comparison against a credits/materials ledger. One day to implement if the ledger already exists, which it should by M7. That's the baseline.

A standing gate reuses `mutate_standing` and band reads already decided. No new surface. Near-zero marginal cost against existing architecture.

Max's aerial intercept requirement is a new counter, a new event emission at intercept resolution, a new read path into the tier advancement check, and a new edge case for escort-handled intercepts that Vera correctly identified. Estimate: 2–4 days, plus the escort-attribution question that is still open from Q7-Q8. That question is not resolved. Building on an unresolved open question is how scope expands silently.

Vera's economic gravity argument is not a trigger — it's a design hope that the numbers work out. It requires no build cost but it also requires no guarantee. If mission credits don't happen to dominate the economy at Outpost tier, the loops don't close and we have no enforcement mechanism.

**The agenda question I want answered before we debate trigger philosophy:** Does the advancement trigger need to be a hard gate that the engine enforces, or a soft gravity that content design produces?

Those are different implementation targets. The group has been debating trigger design before answering that. I want it answered first.


<!-- complete -->
