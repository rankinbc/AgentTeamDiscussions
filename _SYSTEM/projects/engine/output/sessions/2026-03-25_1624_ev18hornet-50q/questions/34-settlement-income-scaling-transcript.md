# Transcript: Settlement Income Scaling

*Generated: 2026-03-25 18:38*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

Before endorsing the cascade Max and Ren are describing, I want to check what we're actually inheriting from EV.

EV's economy was simple by design. Freight pays flat. Mission pays flat. You understand it in one session. The complexity wasn't in the income model — it was in *where you could go* to earn, which was gated by standing. The economy and the faction system talked to each other through geography, not through production coefficients.

What's being proposed here is something different: a real-time building operational status system where income rates shift based on damage state, with per-type degradation coefficients and multiplier interactions across building categories. That's not EV economy. That's closer to Factorio with guns.

The risk I'm flagging is substitution. If managing building income becomes the dominant loop, the player optimizes settlement health for income reasons, not faction reasons. Faction standing becomes one input into a production system rather than the central axis that every system orbits. That's a different game.

What EV's standing system actually delivered was *consequence legibility*. Every standing change traced to a specific choice. Building-derived income adds a second consequence chain that doesn't trace to a choice — it traces to raid outcome, which traces to standing. That's two hops. Two hops is manageable if the income signal is simple. It becomes noise if we add per-type coefficients, multiplier interactions, and differential degradation behaviors before we've measured what standing deltas actually look like in play.

The agenda question I'd put: is building income a *signal* or a *system*? Because those require different architectures and different amounts of player attention.

### Nadia (new-player experience advocate)

Vera's signal-vs-system question is the right frame, and I want to apply it specifically to session one.

A new player lands their Shuttle for the first time. They see flat-poly buildings in different states. If building income is tied to operational status, that player needs to simultaneously understand: what buildings do, what degraded means, that income is building-derived, and that the power node's multiplier relationship affects storage output differently than shelter. That's not discovery — that's a manual they haven't read.

The SimCopter payoff Max describes is real, but it's a session-five payoff. The player who reads their settlement from 500 meters and sees economic state in the silhouettes is someone who already understands the system. First-session players see polygons in two colors and don't know what the difference means yet.

Here's where I'd land: Max is right that operational-status income is the *eventual* correct design. Ren is right that reduced-not-zero preserves agency. But Vera is right that the architecture needs to be simple enough that the degradation feedback arrives before the consequence does.

The practical answer: flat passive income in M5 with building-presence as the modifier (you have a shelter, you earn shelter income; it's present or it's not). Operational-status degradation earns scope when the degraded geometry state is already teaching players what each building *does* intact. You can't read degraded-power-node-means-income-drop if you don't already know what intact power node means.

Signal first. System second. That's the onboarding contract.

## Round: EVALUATE

### Soren (solo dev scope warden)

The group has correctly identified the design tension. Let me put the build cost on the table before the architecture gets decided.

**What Nadia proposed (presence-modifier, flat rate) costs:**
- Income constant per building type — config, one afternoon
- Building presence check at income tick — trivial read against existing building list
- Total estimate: 1–2 days including tests

**What Max and Ren proposed (operational-status, per-type degradation coefficients) costs:**
- Damage state exposed as a queryable value per building instance — requires damage model to exist and emit readable state
- Per-type degradation coefficients — config is cheap; the multiplier relationship between power and other types is not
- Power-as-output-multiplier means the income calculation has a dependency graph: power state affects storage output rate affects trade income — that's not a coefficient, that's a runtime query chain
- Estimate for the dependency graph alone: 1–2 weeks, higher if building count grows

The dependency graph is the flag. "Named config constants per building type" describes the tuning surface, not the architecture. The architecture is a directed graph of building states feeding into an income calculation. That's a new system, not a new config file.

**The sequencing implication:**
Operational-status income cannot ship before the building damage model exposes live queryable state. That model doesn't exist. Presence-modifier income can ship the day buildings can be placed.

Vera's "signal vs. system" question is the agenda question. My answer: signal first, because the system requires infrastructure that isn't built yet. Presence-modifier in M7. Operational-status earns scope when the damage model is live and we have playtest data on raid frequency.

<!-- complete -->
