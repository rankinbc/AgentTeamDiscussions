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


<!-- complete -->
