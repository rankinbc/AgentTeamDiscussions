# EV18Hornet — 50 Open Design Questions Brief

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

1. **Faction Standing Commitment Threshold** At what standing value does the commitment NPC become available? This is a concrete number that must be decided before M5 faction standing API work can begin — it gates both content placement and the code path that unlocks the mission string.

2. **Faction Standing Inverse Axis Symmetry** Is the faction inverse axis 1:1, or asymmetric — does 1 point gained with Confederation cost exactly 1 with Rebels, or more? This asymmetry (or lack of it) shapes how costly it is to explore both factions before committing, and must be a named decision before M5 implementation.

3. **Co-op Faction Commitment Independence** If Player 1 accepts the Confederation commitment mission, does it close Player 2's Rebel string — or do co-op players have independent commitment paths? This is a foundational co-op question that blocks M5 faction standing API design.

4. **Co-op Standing Consequence Propagation** If Player 1's action causes a standing consequence with a faction that is also pressuring Player 2, does Player 2's track move automatically, or does it require an explicit shared-action mechanic? This blocks M5 faction standing API.

5. **Standing Recovery Mechanics** Is recovery from degraded-but-uncommitted standing possible, and what does it cost — is it standing-gated, credits-gated, or mission-gated? The answer must be consistent with the tier regression rebuild decision.

6. **Passive Standing Decay** Does standing decay passively over time with no player action, or does it only move through explicit events? Passive decay creates urgency and ongoing faction pressure; event-only decay is simpler but may reduce faction tension.

7. **Escort Formation AI Milestone** At which milestone does the first escort ship have working 2D formation AI — M6 architecture or M6 functional AI? This milestone assignment determines what M5 can ship without and blocks escort scope estimation.

8. **Escort Atmosphere Dive Milestone** At which milestone do escorts execute the atmosphere dive — same milestone as 2D escort AI, or deferred? Co-locating these tasks saves context switching; deferring keeps M6 scope tight.

9. **Hot Hull Port Registration** Is the port run registration for a captured hull a fixed standing cost, or does the player get choices — bribe official, flag as salvage, accept standing penalty? The number and nature of choices here determines how much the boarding mechanic feeds into faction standing emergence.

10. **Hot Hull Interdiction Trigger** During the hot-hull window, if the player is interdicted, is the hull itself the hostility trigger or only the standing value? This determines whether a stolen ship is dangerous to own regardless of your standing, or only dangerous if you've already burned your faction relationship.

11. **Raid Scale Definitions** What are the concrete definitions of "harassment-scale" vs. "assault-scale" raid — ship count ceiling, building damage cap, tier regression eligibility? These definitions block offline raid logic and M8 co-op scope estimation.

12. **Minimum Building Type Count at Outpost** What is the minimum building type count at Outpost tier? This single number drives all state persistence estimates, co-op sync scope, and raid targeting logic — it must be defined before settlement scope can be estimated.

13. **Tier Regression Rebuild Path** Is the tier regression rebuild path the same founding investment as original construction, or is there a faster recovery path? Standing must remain the primary gate for advancement regardless of which path is chosen.

14. **Death Respawn Port Definition** What is the precise definition of "nearest" and "friendly" port for 2D space death? The edge cases — contested systems, faction-owned ports you have bad standing with, ports that have been destroyed — must be resolved before the death flow is implemented.

15. **Starter Ship at Respawn** How is the starter ship acquired at respawn — given free, loaned against future earnings, or purchased? What is the credit floor guarantee the player always retains? This shapes the risk profile of the entire game.

16. **Hot Hull Destruction Standing Consequence** When the hot hull is destroyed on death, does the owning faction's standing consequence close (hull is gone, matter resolved) or escalate (destruction of their asset is an additional offense)?

17. **Return Log Milestone** Does the return log ship with M7 Settlement, or M8 Co-op? If M7 proceeds without it, first offline damage events will be unreadable and the co-op experience degrades significantly.

18. **Offline Session State Model** What is the canonical session state when both host and client go offline simultaneously — last committed save, or elapsed-time reconstruction? The answer determines how complex the offline simulation system needs to be.

19. **Host Role Assignment** Is the host role fixed to one player, or negotiable session-by-session, and how does asymmetric hosting affect asymmetric faction pressure accumulation? This has implications for whose standing matters most when a shared event fires.

20. **Minimum Altitude Range** What is the minimum altitude range — the vertical delta between entry point and lowest flyable altitude? This is a concrete number needed before atmospheric layer geometry can be scoped.

21. **Atmosphere Exit Transition** Does exiting the atmosphere trigger a symmetric cinematic beat, and what is the player's position and orientation in 2D space on re-emergence? The re-emergence position affects tactical play — can you use atmosphere dives as evasion?

22. **Raid Approach Signaling from Space** How does the 2D nav layer signal raiding fleet approach time to a player who has never experienced an atmospheric raid? The answer determines whether the inter-layer threat model is legible to new players.

23. **Raid Defense Weapon Type** What is the specific weapon type for raid breach defense? The answer determines what the on-foot combat system needs to handle at M7.

24. **On-Foot AI Range Thresholds** What are the exact alert and attack range thresholds for on-foot enemy AI? These numbers are required before on-foot AI can be implemented.

25. **Hit Feedback Model** What does hit feedback look like — screen shake, directional indicator, sound cue, or combination? This is a concrete UX decision required before on-foot combat feel can be evaluated.

26. **Galaxy Map Standing Gate Visualization** How does the galaxy map visually communicate a standing-gated system to a player who has never encountered one? This affects player onboarding and must be solved before M3 launch.

27. **Starting System Faction and Geography** Which faction owns the starting system, and what is its geographic relationship to the two contested chokepoints the player reaches in sessions 2–3? This shapes the opening hours of the game.

28. **Settlement Building System Introduction** How does the player first learn the settlement building system — is it mission-gated, triggered by landing, or open from session one? The discovery method shapes how much tutorial scaffolding is needed.

29. **Atmosphere Boundary Visual Signature** What is the audiovisual signature of the atmosphere boundary that reads as an intentional surface using only geometry and color — no haze, no bloom? The constraint is the flat-poly aesthetic, which means standard atmospheric rendering tricks are off the table.

30. **Hostile vs. Friendly Atmosphere Signal** How does the player distinguish whether an atmosphere is friendly or hostile before committing to the dive — what signals faction ownership from 2D space? This is both a design and UX question: what information does the layer transition UI surface?

31. **Core Tradeable Commodities** What are the core tradeable commodities — ore, food, fuel, tech goods, weapons, medicine — and which ones can player settlements produce? The commodity list determines the economy's surface area before M5 content scope can be estimated.

32. **Settlement Tier Advancement Trigger** How does settlement tier advancement work — what is the trigger that promotes an Outpost to the next tier? Is it population, investment, time, mission completion, or a combination?

33. **NPC Settler Arrival Model** Do NPC settlers arrive organically once the settlement reaches a threshold, or does the player always place and manage personnel explicitly? Organic arrival reduces micromanagement; explicit management increases attachment to the settlement.

34. **Settlement Income Scaling** How does settlement income scale — flat passive rate, or derived from the specific buildings present and their operational status? The latter creates build strategy depth; the former is simpler to balance.

35. **Credit Floor and Failure State** What is the failure state if the player runs out of credits entirely — is there a floor, or can the game become unwinnable? A floor is more forgiving but reduces stakes; no floor requires careful economy balancing.

36. **NPC Settlement Tribute / Piracy Model** Can the player collect tribute or tax from NPC settlements they have dominated, mirroring EV's piracy model? This determines whether economic dominance is a viable playstyle.

37. **Total Faction Count and Alliance Model** How many total factions exist beyond Confederation and Rebels, and can smaller factions be allied with either major faction, neutral, or enemies of both? The faction graph complexity determines how rich the standing system's emergent situations can be.

38. **Conflict Introduction Mechanism** What is the inciting incident that introduces the Confederation vs. Rebels conflict from the player's perspective — mission-triggered, proximity event, or background lore on session start?

39. **Mission String Count at Full Scope** How many mission strings exist at full scope — Confed path, Rebel path, and how many smaller faction arcs? This is the content scope ceiling for the story layer.

40. **Post-Story Galaxy State** What does completing the main story unlock or change about the galaxy — does faction war resolve, does territory shift, does a new mode open? The answer determines whether the game has a satisfying arc or is purely sandbox.

41. **Settlement Fate on Faction Commitment** What happens to the player's settlements in Confederation space when they commit to the Rebels, and vice versa? This is one of the highest-stakes consequences in the game and must be explicitly designed.

42. **Divergent Co-op Faction Commitment and Settlements** If co-op Player 1 commits to Confederation and Player 2 commits to Rebels, are their settlement deterrence profiles still shared, or do they bifurcate? This is one of the hardest co-op design problems in the game.

43. **Capital Ship Atmosphere Access** Can capital ships enter the atmosphere layer, or are they space-only assets? The answer affects fleet strategy, raid counterplay, and atmospheric layer scope significantly.

44. **Ship Repair Model** Is ship repair automatic at port, credits-cost only, or does it require materials sourced from your settlements? The repair model determines how tightly the economy and combat are coupled.

45. **Space Stations as Dockable Structures** Are there space stations in addition to planets as dockable and landable structures in the galaxy? Stations expand the space layer's complexity and create potential settlement-layer outposts in deep space.

46. **Co-op Escort Destruction Budget** If a co-op player's escort ship is destroyed, does it come out of their fleet budget or is it a shared fleet resource? The answer determines how much escort losses affect the other player.

47. **Maximum Fleet Size at Full Scope** What is the maximum practical fleet size at full game scope — the physical bay cap on the largest available hull? This sets the ceiling for the fleet system's complexity.

48. **Win Condition vs. Sandbox** Is there a win condition, or is the game a sandbox with story beats as optional milestones? The answer shapes the entire late-game design philosophy.

49. **Post-Story Save State** What happens to a player's save after completing the main story — does the galaxy persist for continued play, or is a new game implied?

50. **Modding Support as a Long-Term Goal** Is modding support — EV-style plugin architecture with replaceable content packs — a long-term design goal, and does that constrain any data format decisions made before City tier?
