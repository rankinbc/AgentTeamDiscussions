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


<!-- complete -->
