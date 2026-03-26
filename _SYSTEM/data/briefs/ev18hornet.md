# EV18Hornet — Game Design Brainstorming Brief

A 3D space opera combining Escape Velocity's proven formula (faction standing, mission strings, ship outfitting, economy) with F/A-18 Hornet 2.0's atmospheric flight model and SimCopter's "flying over something you built" fantasy. Co-op (2-player). Built in Godot 4 with flat-poly aesthetics throughout. Solo developer, personal use first.

## What's Already Decided

- Three gameplay layers that interact mechanically: Space Layer (galaxy map, fleet, faction travel), Atmospheric Layer (Hornet-style 3D mouse-flight over planets), On-Foot Layer (first-person bar, building placement, exploration)
- Flat-poly aesthetic throughout — no textures, solid color polygons like FA-18 Hornet 2.0 — this is a feature, not a constraint
- Godot 4 (GDScript primary) — handles all three layers natively, procedural terrain via ArrayMesh, mouse rate-control flight via InputEventMouseMotion
- 2-player co-op (not MMO, not competitive PvP by default)
- Escape Velocity-style faction standing system — standing with factions affects mission availability, equipment access, and whether factions raid your settlements
- Ship progression: Shuttle → Light Fighter → Freighter → Heavy Fighter → Capital Ship. Can skip tiers by boarding and capturing enemy ships
- Settlement tier system: Claim Stake → Outpost → Settlement → Colony → City. Each tier unlocks new functions and attracts faction attention
- The Bar: 3D first-person NPC hub for missions, rumors, and escorts — a pillar of the EV experience
- Eight development milestones: Tech Spike → Hornet Layer → Galaxy Layer → EV Core Loop → Faction & Standing → Fleet → Settlement → Co-op → Main Story
- Reference DNA: Escape Velocity (systems/economy/factions), FA-18 Hornet 2.0 (flight model), SimCopter (aerial view of your own build), Stranded Deep (building progression), Cities: Skylines (settlement watching)
- Core design principle: emergence over scripting. Simple rules create complex player situations without authored content
- Anti-patterns to avoid: making this an MMO, losing EV's feeling of freedom, overcomplicating systems that were elegant in EV, building the dream version before the fun version

## Open Questions

1. **Space Layer: 2D or 3D?** Is space flight top-down 2D like the original EV, or full 3D like the atmospheric layer? 2D keeps the EV feel, is simpler to build, and has proven readability for targeting and navigation. 3D is consistent with the other two layers and more immersive — but requires deciding between Newtonian (drifting, momentum) and arcade (point-and-thrust) physics. This decision shapes scope, feel, and whether space feels like a different mode or a seamless third dimension of the same world.

2. **Galaxy Scale and Structure** How many star systems? Is the galaxy procedurally generated per playthrough or hand-authored? Does the full map exist from the start or do players discover systems by jumping? Consider: EV had ~50 systems and felt infinite. Procedural risks feeling generic; authored risks scope explosion. This decision shapes the entire feel of exploration and how many unique faction territories, trade routes, and mission strings are possible.

3. **Layer Transitions: Seamless or Gated?** When you dive into a planet's atmosphere from space, is it a seamless transition (continuous flight, no loading screen) or a gated transition (black screen, then you appear in atmosphere)? Seamless is the dream — it reinforces that all three layers are one world — but requires keeping both layers loaded or streaming. Gated is fast to build and universally understood. The answer also determines: can you be attacked mid-transition? Do escorts follow you through?

4. **Settlement Destruction Stakes** Can enemy factions permanently destroy your buildings during raids? If yes: dramatic stakes, real consequences for faction standing mismanagement, genuine defense tension. If no (or if rebuilding is cheap): the settlement layer becomes a resource farm rather than something you fight to protect. What is the failure condition for a settlement — and does losing one feel like a loss worth caring about?

5. **Fleet Architecture: Hard Cap or Soft Cap?** Is there a hard numerical limit on fleet size, or a soft cap via credits/command rating (higher-rated ship = bigger fleet allowed)? EV used tonnage/crew as soft limits. A soft cap via command rating creates a progression reward for upgrading your own ship. A hard cap is simpler but less interesting. Related: when you board and capture a ship, can you add it immediately to your fleet or must you fly it to a port first?

6. **Co-op State Model** What happens to the shared galaxy when one player is offline? Option A: the galaxy pauses (both players must be online to advance time) — safe but frustrating if schedules differ. Option B: the galaxy continues without the offline player — their settlements keep running, factions keep advancing, but their ship stays docked. Option C: each player has a solo-playable game that merges when they connect. This shapes whether co-op is a shared world or a drop-in companion system.

7. **Faction Commitment: Path Choice or Flexible Standing?** Can you ever be simultaneously allied with both the Confederation and the Rebels, or is faction commitment mutually exclusive past a certain point? EV forced a choice — you couldn't finish both storylines in one playthrough. Mutual exclusivity creates replayability and meaningful choice. Flexibility creates a more sandbox feel but dilutes the narrative stakes. Also: can a player form their own faction late-game, and what does that unlock?

8. **On-Foot Combat Depth** How deep is on-foot combat — is it a simple FPS shooter, a cover system, melee-inclusive, or deliberately minimal (walking sim for bars and building placement with minimal combat)? Deeper combat means more solo dev time, more UI, more animations, more balance. Minimal combat (avoid it where possible, on-foot means exploration and building not fighting) keeps scope tight but limits the derelict/boarding experience. What is on-foot for — combat, atmosphere, or both equally?

9. **Death and Progression Setback** When you die — lose your ship in space, get killed on foot — what do you lose? Options: (A) respawn at nearest friendly port, ship fully restored, no penalty; (B) respawn but lose ship and must buy/fly a starter ship; (C) lose ship and all unbanked credits; (D) permadeath option that restarts the campaign. This decision shapes the risk/reward of taking on dangerous missions, building settlements far from safe space, and whether the game has stakes or is a pure power fantasy.

10. **Scope Target: How Small is the Fun Version?** For the first playable milestone — what is the minimum ship count, system count, and building count that makes the core loop feel rewarding? EV shipped with 12 ship types and ~50 systems and felt infinite. What is the EV18Hornet equivalent? This question forces a concrete scope stake in the ground: if you could only ship with X ships, Y systems, and Z building types, what are X, Y, and Z — and is that actually fun?
