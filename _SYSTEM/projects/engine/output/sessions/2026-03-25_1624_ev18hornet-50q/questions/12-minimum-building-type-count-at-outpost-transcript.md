# Transcript: Minimum Building Type Count at Outpost

*Generated: 2026-03-25 17:04*

## Round: PROPOSE

### Max (atmospheric flight advocate)

The number we pick here isn't just a persistence estimate input — it's a **raid triage design problem**, and I want to make sure we're solving it from the right altitude.

Here's the constraint that matters to me: at assault scale, the player is at 500 meters, two or more approach vectors are incoming, and they have roughly three seconds to read which buildings are threatened before committing to an intercept bearing. That's the entire design window. The number of building types at Outpost isn't an abstract data model question — it's the **legibility budget for mid-air triage**.

Too few types and the settlement doesn't read as a settlement worth protecting. The SimCopter payoff — banking over your own build and *knowing* it — requires distinct silhouettes. Too many and the flat-poly aesthetic becomes visual noise from altitude, and worse, we're committing to a degraded geometry state for every one of them before M8 ships.

So I want us to frame the minimum count around one question: **what is the smallest set of building types that creates a meaningful triage decision during an assault raid?**

My instinct is that answer is **four**. A shelter (lives here), a power node (everything runs on this), a storage unit (trade capacity), and a defense emplacement (fights back). Four distinct silhouettes. Four things that read differently from 500 meters. Four degraded geometry states that are actually buildable before M8.

Does anyone see a case for fewer? Or a fifth type that changes the triage calculus in a way the first four don't?

### Ren (emergence systems theorist)

Four is correct. But the defense emplacement is doing more work than Max's framing captures, and that work matters for the emergence chain.

The other three types — shelter, power node, storage — are passive raid targets. The defense emplacement is the first Outpost-tier building that creates a feedback loop *back into* the atmospheric layer. It's not just a silhouette from 500 meters; it's an autonomous actor in the raid. That changes the triage calculus fundamentally: the player isn't choosing which building to protect, they're choosing which vector to cover knowing the emplacement handles another.

This introduces the emergent situation I want to flag: if the power node and the defense emplacement are in a dependency relationship — emplacement goes offline when power node is destroyed — then raid AI that targets rationally will prioritize power first. The player learns this under fire, not from a tutorial. The faction AI generates a situation the designer didn't author by exploiting a structural dependency the player built.

That dependency needs to be in scope for M7 even if it's one config flag per building type. Without it, the emplacement is a fifth silhouette, not a system node.

One concern: four types times two geometry states is eight assets. That's the blocking estimate question Soren needs before M8 scope is defensible. The count itself is answerable now — four — but the asset commitment needs to be explicit, not implicit in the decision.

Four types. Power-emplacement dependency from day one. Asset count acknowledged as a named M8 dependency.

## Round: CRITIQUE

### Vera (EV systems historian)

Four is defensible, but Ren's framing exposes a scope risk that needs to be named before the number is confirmed.

EV's economy worked at three commodity types per system because each type created a *different decision*. Food, equipment, trade goods — each had a distinct routing logic. You didn't need more because three already generated distinct choices. The count wasn't minimum viable complexity; it was minimum viable *differentiation*.

Apply that lens here: shelter, power node, storage — those three already create a triage hierarchy because they have asymmetric recovery cost. You can rebuild storage. You can't undo a session of lost power. That hierarchy exists without a fourth type.

The defense emplacement earns its slot *only* through the power dependency Ren describes. A standalone emplacement is a fifth silhouette masquerading as a system. But the dependency Ren wants — power-offline triggers emplacement-offline, raid AI learns to sequence accordingly — that's not a config flag. That's authored raid AI priority behavior. "Rational targeting" in assault-scale raids is a separate system that doesn't exist in M7 scope as described.

My flag: **four building types is correct if and only if the power-emplacement dependency ships in M7**. If that dependency slips to M8, the emplacement is unearned complexity and the minimum defensible count drops to three.

The question I'd set for this round: is the power-emplacement dependency a M7 build item or an M8 build item? That answer determines whether Max's four is the minimum or whether three is the honest number.

### Nadia (new-player experience advocate)

Vera's reframe is right, and I want to add what it means for someone who's never played EV.

The power-emplacement dependency is elegant — but it's only legible to a player who has already lost their emplacement once with the power node down. First time through, a new player doesn't know the dependency exists. That's fine; emergence teaches through consequence. But the degraded geometry state is what teaches them *before they lose*. The damaged power node has to visually communicate "something else just got worse" from 500 meters, in flat-poly, to someone who didn't read a wiki.

That's a harder asset problem than "two geometry states per building type." It's a *communication design* problem on each degraded state. And I don't think we've named it as such.

So my position: Vera's conditional is correct — four types only if the dependency ships in M7. But I'd add a second condition: the power node's degraded state must carry a legible visual signal that communicates "systems affected" at altitude, not just "this building is damaged." If that signal isn't in scope, the dependency becomes invisible to new players regardless of when it ships, and Ren's emergence chain breaks at the onboarding seam.

**Three types with strong degraded-state visual language beats four types where the fourth's strategic role only surfaces after a failed raid.** The SimCopter payoff requires you to *read* your settlement, not just fly over it. Count is secondary to legibility.

## Round: EVALUATE

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
