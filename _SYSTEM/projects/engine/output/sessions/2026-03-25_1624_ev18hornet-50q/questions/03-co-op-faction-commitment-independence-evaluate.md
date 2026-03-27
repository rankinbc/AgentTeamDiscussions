### Soren (solo dev scope warden)

**The discussion has converged correctly on the architecture. What nobody has priced is the build sequence.**

Vera's proposal — raid spawn reads each player's standing directly, no settlement aggregation layer — is the right answer *and* the cheaper answer. That's unusual. Lock it.

But here's the scope problem underneath this question: **co-op is Milestone 8. Faction standing is Milestone 5.** The API you're designing today needs to work for a single player first, then extend cleanly to two players three milestones later without a rewrite.

That means M5 should ship with:
- Per-player faction standing (single player, fully functional)
- Commitment NPC trigger: standing ≥ 60 AND mission completed (already decided)
- Raid spawn reads the *active player's* standing — singular, not plural

The co-op extension point is: at M8, raid spawn queries each connected player's standing independently. No new data concept required. No settlement aggregation layer. The architecture Vera described is already the correct M8 shape — you just don't build the two-player read path until M8.

**What I want to flag before Max's two-spawn-axis geometry gets designed:** directional spawn axes tied to faction heat are a non-trivial atmospheric system. That's M2 atmospheric layer work intersecting with M5 faction data intersecting with M8 co-op state. Building that intersection point now is how scope compounds.

The question to answer today: does M5 require *any* co-op faction API, or is M5 strictly single-player standing with a clean extension contract documented for M8?

That's the agenda.


<!-- complete -->
