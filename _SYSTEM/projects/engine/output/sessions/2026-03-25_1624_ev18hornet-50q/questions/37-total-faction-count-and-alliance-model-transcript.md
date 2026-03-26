# Transcript: Total Faction Count and Alliance Model

*Generated: 2026-03-25 18:51*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

EV Nova shipped with eight named factions. Four of them mattered to airspace. The other four were interesting because of what they *didn't* do to your standing with the factions that did matter.

That distinction is where I'd push back on Ren's alliance propagation framing.

If Confederation-aligned smaller factions pass standing consequences through `FACTION_STANDING_LOSS_MULTIPLIER` to Rebel standing, you've made the player responsible for diplomatic consequences they may not have seen coming. That sounds like emergence. It's actually opacity. In EV Nova, the faction graph was legible because the rivalry relationships were *explicit and expected* — attacking a Confederation ship cost you Confederation standing, full stop. The causal chain was one step long. Players could trace it.

Alliance propagation makes the chain two steps long, minimum. "I ran missions for the Trade Consortium and now the Rebels are raiding me" requires the player to know that the Trade Consortium is Confederation-aligned and that alignment propagates through the multiplier. That's not emergent complexity — that's hidden consequence, which is the opposite of what this standing system was designed to produce.

Raiders work as a third faction specifically because they are *orthogonal* to the standing graph, not because they add a third standing axis. They spawn regardless of your political position. No multiplier propagation, no alliance table. The player cannot standing-manage them away.

My agenda: **faction count should be three maximum, and alliance relationships should produce no automatic standing propagation in M8.** Alliance is a content signal — flavor text, mission framing, NPC dialogue — not a mechanical relay. Keep the causal chain one step long.

### Nadia (new-player experience advocate)

Vera's one-step causal chain argument is the new player argument, and I want to name it clearly: alliance propagation doesn't produce emergent complexity for new players, it produces invisible punishment.

The player who runs three Confederation missions in session one and then discovers their Rebel standing has also been degraded by some Trade Consortium relay they never saw — that player doesn't read "emergence." They read "broken." They haven't built the mental model that makes two-step consequences feel like their own choices coming back to haunt them. They built nothing. The system just moved.

The standing tooltip fires at 40. That's the designated legibility surface. It can explain one thing: *this faction, this value, this consequence.* It cannot explain "this faction's ally's missions also moved this other faction's value." That's a different system requiring a different teaching surface we haven't designed.

Raiders as orthogonal threat is the right framing precisely because new players don't have to understand it. The Raiders don't care about your choices — and the player doesn't need to understand *why* to respond correctly. Fly up, intercept, defend. The motivation is irrelevant to the action.

My position: three factions maximum, Raiders as third, zero alliance propagation in M8. 

But I want to add something nobody's said: the first contested chokepoint is where this question actually lives. If the player arrives at session two or three with Rebel standing already in Degraded band from passive Confederation mission completion — without the tooltip having fired clearly — we've already lost them before faction count even matters.

## Round: EVALUATE

### Soren (solo dev scope warden)

The discussion has landed on three factions and no alliance propagation. Those are the right answers. I want to put build costs on them so "three factions" doesn't become a number that surprises anyone mid-M8.

**Per-faction content cost is not a standing track. It's everything a faction needs to exist.**

For each faction beyond two, the minimum viable content set is: one distinct ship silhouette (flat-poly mesh, intact and damaged geometry states), one patrol behavior variant with authored spawn parameters, Bar NPC presence in at least one system (model, dialogue strings), a mission pool with authored entries, and faction-specific comms intercept strings. That's not a config entry. That's roughly two to four weeks of work per faction, depending on how many systems they appear in.

Raiders at three factions is the right call because they're *cheaper* than a third political faction. No standing track to balance. No Bar missions to author. No commitment NPC. No Degraded band cold dialogue. Their complexity is in spawn behavior and ship silhouette, which is bounded.

Flag on alliance propagation: every time "alliance relationships as config" appears in this discussion, it sounds like a named constant. It isn't. Alliance propagation requires a rivalry graph, authoring pass across all faction pairs, testing the emergent combinations, and a new teaching surface. That's a system. Vera and Nadia closed it correctly.

My agenda for this round: **Confirm Raiders as structurally distinct from major factions — no standing track, no Bar presence — and scope that distinction as the cost reduction that makes a third faction viable.**

What does a Raider ship cost to build? That's the question that unlocks the decision.

<!-- complete -->
