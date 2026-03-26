### Soren (solo dev scope warden)

The discussion has converged correctly on the conditional: four types if the power-emplacement dependency ships in M7, three otherwise. My job is to price the dependency so that conditional is answerable.

**Asset math first.** Four types × two geometry states = eight flat-poly models. At this aesthetic, each model is maybe a half-day to one day of focused work — silhouette design, ArrayMesh construction, degraded variant. Call it four to eight days of asset time for the building set alone. That's real but not blocking.

**The dependency is where scope hides.** "Power node offline → emplacement offline" is not a config flag. It is:
- A building state propagation system (which buildings affect which)
- A read path from power state into emplacement active/inactive state
- Raid AI that queries structural state before selecting a target vector

That last item is the expensive one. "Rational targeting" in assault raids means the spawn system needs a priority pass over live building states. That doesn't exist. Building it in M7 is a weeks-level item, not a days-level item, and it pulls in architectural surface that doesn't exist yet.

**My read:** The dependency does not ship in M7 as currently scoped. Therefore Vera's conditional applies: three types is the honest number at Outpost.

The question for this round is whether anyone can show the dependency is cheaper than I'm estimating — or whether four types earns its slot by another mechanism that doesn't require raid AI structural awareness.


<!-- complete -->
