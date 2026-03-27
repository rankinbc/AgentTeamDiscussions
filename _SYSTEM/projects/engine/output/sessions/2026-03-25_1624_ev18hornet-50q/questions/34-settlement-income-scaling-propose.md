### Max (atmospheric flight advocate)

Building-derived income. Not because it's more complex — because it's the only version where the atmospheric layer does real work.

Here's what I mean. If income is flat passive, then what the player sees from 500 meters is *scenery*. Pretty polygons. The settlement reads the same whether the power node is intact or smoking.

Building-derived income tied to operational status means every building silhouette is an income signal visible from the air. Raider took out your power node? You can *see* that from approach altitude — degraded geometry AND you know your income just dropped. That's the SimCopter payoff times two. You're not just admiring your city, you're reading it. The aerial view becomes a management interface.

This also directly resolves the question from Q12 — what does the degraded power node communicate at 500 meters? It communicates "your income is bleeding." The visual stakes and the economic stakes become the same thing. That's design compression, not design complexity.

The balance concern is real but it's downstream. Start with building type → income category mapping (shelter covers population, power covers output multiplier, storage covers trade capacity) and let the numbers come from M5 playtest. Named config constants from day one.

The question I'd put to the group: does income derive from *presence* of the building, or from *operational status* of the building? Because that determines whether a degraded power node still generates income at reduced rate or cuts out entirely. That's the agenda question — and it has direct consequences for how hard raids actually bite.

### Ren (emergence systems theorist)

Max is right, and I want to name precisely why from a systems interaction standpoint.

Flat passive income means the three layers don't talk to each other economically. You fly down, you build, you fly away, the income accrues. Building-derived income keyed to operational status means a raid creates a cascade the designer didn't author: standing drops → raid spawns → power node degrades → income drops → fewer resources for recovery → standing harder to recover → next raid arrives at higher composition. That's the emergence chain doing real work.

On the presence-vs-operational-status question: operational status, definitively. But with one constraint that matters for agency preservation — degraded should mean *reduced*, not *zero*.

Here's why. Zero output on degradation creates a death spiral with no player-authored exit. Reduced output preserves the signal (you can see the problem, you feel the bite) while keeping the recovery path open. The player can still earn their way out. That distinction is the difference between a system that generates situations and one that terminates them.

The second thing I'd flag: storage unit income capacity should probably have a different degradation behavior than power. Power is a multiplier — degraded power reasonably reduces all downstream output. Storage is more like a throughput cap on trade. These interact differently with faction standing and raid targeting, which matters when rational targeting eventually ships.

Name the degradation coefficients as config constants per building type. Don't assume symmetry. Playtest will tell you whether 50% degraded output bites hard enough or too hard — but the architecture needs to support per-type coefficients from day one.


<!-- complete -->
