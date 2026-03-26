### Max (atmospheric flight advocate)

The atmospheric layer is the answer to this question, not the galaxy map.

Here's what I mean: faction count doesn't matter as an abstract number. What matters is how many *geometrically distinct* factions can simultaneously occupy your airspace. Because that's the experience — you're at altitude over your settlement, banking through a turn, and what you SEE below and around you tells the story of every political decision you've made since session one.

Two factions already gives you the two-spawn-axis contested geometry that's been deferred to M8. That's the minimum for interesting airspace. The question is whether additional factions add *new intercept geometry* or just add more bars to fill in the standing menu.

My agenda for this round: **faction count should be bounded by atmospheric legibility at 500 meters, not by galaxy map topology.**

If a faction can be visually distinguished from Confederation and Rebel ships — different silhouette, different patrol vector, different approach angle — it earns its place in the faction graph. If it's just another colored icon on the standing screen, it's stealing scope from flight depth.

Practically: I'd argue for three factions maximum in M8 contested airspace. Confederation, Rebels, and one wild-card — Raiders being the obvious candidate, enemy of both, spawning from unpredictable vectors because they don't care about your alliance state. 

That third axis creates genuinely novel atmospheric situations without requiring the standing system to track political relationships it doesn't have architecture for yet.

What's the alliance model doing for *flight geometry*? That's my question.

### Ren (emergence systems theorist)

Max is right about atmospheric legibility as the constraint, but I want to push on the underlying mechanism.

The standing system is a ledger. What matters for emergence isn't faction count — it's how many *independent standing axes* can simultaneously produce conflicting pressures on the player's airspace. Two factions with symmetric mutual rivalry gives you one axis of conflict. The player optimizes toward one pole or the other. That's rich, but it's a single dimension.

Raiders as a third faction is interesting specifically because they *break the optimization*. If Raiders spawn regardless of standing with either major faction, you've introduced an uncontrollable variable that disrupts the player's sense of total airspace control. That's good. It means even a fully committed Confederation player has a threat vector they can't standing-manage away. The emergence comes from that interaction: Raiders pressure the player toward aerial response regardless of political alignment, while the major faction threat scales with standing choices.

The alliance model question is the one I'd focus on: can smaller factions be allied with Confederation or Rebels, and does that alliance *propagate standing effects*? If Confederation-aligned faction missions move Rebel standing via `FACTION_STANDING_LOSS_MULTIPLIER`, the alliance model creates emergent standing pressure the player may not have anticipated. That's more interesting than raw faction count.

The flag I'll plant: the alliance structure should be expressible in the config architecture we already have — per-faction rivalry heat values, carried open since Q3. A Confederation ally just has `rivalry_heat` pointing toward Rebel-aligned factions. We don't need a new system. We need authored values.

Three factions maximum for M8 airspace. Alliance relationships as config. Faction count bounded by the standing architecture we've already built.


<!-- complete -->
