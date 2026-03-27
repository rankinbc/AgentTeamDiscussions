# Transcript: Core Tradeable Commodities

*Generated: 2026-03-25 18:25*

## Round: PROPOSE

### Max (atmospheric flight advocate)

Here's the real question underneath this question: **which commodities make the player want to be in the atmospheric layer?**

Every commodity on the list is either a reason to descend or a reason to stay in space. That's the filter I'm bringing.

Ore, fuel, food — three production commodities that make sense at settlement level. A Colony-tier mine should be visible from 500m as a hole in the terrain with geometry around it. The player should be able to look down and *see* what their settlement produces. That's the SimCopter payoff. If a commodity's production infrastructure has no visual footprint, it doesn't belong in the first content pass.

The axis I want to put on the table: **production visibility from altitude vs. production that lives in menus**. Tech goods and medicine feel like menu commodities — they're numbers moving between systems. Ore and food have physical infrastructure — mines, grow-domes, storage silos. That infrastructure is what makes the atmospheric layer feel alive rather than decorative.

Weapons as a tradeable commodity is interesting because it directly feeds the standing system — selling weapons to Raiders creates a different faction consequence than selling to Confederation, and that consequence *manifests atmospherically* as patrol density and intercept vectors. That's the kind of commodity feedback loop I want to argue for.

My agenda push: **decide the commodity list by asking which ones produce buildings, and which produce standing consequences that show up in airspace.** Everything else is galaxy-layer spreadsheet content. The atmospheric layer needs commodities that have bodies.

What produces infrastructure? What produces heat?

### Ren (emergence systems theorist)

Max's production-visibility filter is correct and incomplete. It identifies which commodities have bodies — but not which commodities have *read paths into the standing system*.

That's the filter I'd add: **what does the commodity do to faction heat, and does that heat manifest in the atmospheric layer?**

Weapons is the only commodity on the list that directly mutates standing as a trade consequence. Selling to Raiders degrades Confederation standing; selling to Confederation degrades Raider standing. That mutation feeds directly into patrol density, raid composition, and intercept vectors. Weapons isn't just a commodity — it's a standing manipulation tool with airspace consequences. It belongs in the first pass for that reason alone.

Ore, fuel, and food pass Max's visual test and they pass mine — but only if production volume creates a read path. If the raid AI eventually queries live building states for rational targeting (still open from Q12), then a working mine produces more ore, which means more stored value, which means the mine becomes a priority assault target. That's the designer-unintended situation this system lives for: a productive Colony attracts worse raids than a struggling Outpost.

Tech goods and medicine: Max is right, these are menu numbers. No building footprint, no standing consequence, no atmospheric manifestation. They can exist as trade commodities but they don't belong in the first content pass.

One flag: if fuel production is settlement-based and fuel consumption is a real constraint on atmospheric flight time, fuel becomes load-bearing infrastructure with an airspace consequence. That's worth scoping intentionally rather than discovering late.

## Round: CRITIQUE

### Nadia (new-player experience advocate)

Max and Ren have given us two filters: bodies and heat. I want to add a third: **legibility to someone who has never played EV.**

My concern with weapons isn't that it's wrong — it's that it's a standing trap with no warning label. A new player who sells weapons to Raiders because the price is good doesn't know they've degraded Confederation standing until patrols start tightening. That's faction standing punishing a player before they understand what they're doing. Weapons belongs in the game. It doesn't belong in session one without a Bar rumor or tooltip that teaches the consequence *before* the player pulls the trigger.

Ore, food, fuel pass both prior filters. I'd add: these three also pass the **new-player self-explanation test**. A mine looks like extraction. A grow-dome looks like food. A fuel depot has a shape. Players don't need to know EV to read infrastructure.

My flag for fuel: if atmospheric flight has a real fuel constraint, fuel crosses from "tradeable commodity" into "airspace mechanic." That's load-bearing for the descent loop in a way ore and food aren't. Scope it intentionally or don't scope it — but don't leave it ambiguous when someone's designing the first Bar mission.

My agenda push: **rank the first-pass commodities by how much EV knowledge they require to understand.** Ore, food, fuel are self-explaining. Weapons requires faction literacy. Tech goods and medicine require economic context that doesn't exist in session one.

Start with what teaches itself.

### Vera (EV systems historian)

Three filters on the table. One missing: **galaxy size**.

EV Nova shipped six commodity types across a galaxy of ~50 authored systems. You're discussing this same list for a galaxy confirmed at six to eight systems. That's not a commodity economy — that's a price lookup table with standing consequences attached.

EV's economy worked because the player could *see the whole board*. Sigma Shipyards needed metal ore; Palshife exported food; you built trade routes from that. Legibility came from small galaxy size, not from commodity design. Double the commodity types in one-eighth the galaxy and you don't double the depth — you halve the legibility.

My specific flag: **fuel as an airspace mechanic is a trap**. EV never had fuel constraints outside edge-case plugins, for good reason. Fuel scarcity is an invisible wall on player freedom. If fuel is a settlement production commodity but *also* a real constraint on flight time, you've created a system where running low on fuel punishes the player for exploring — which is the exact experience EV was designed to avoid. Scope it as a tradeable commodity with no flight constraint, or scope it as a flight mechanic and accept you've fundamentally changed the freedom loop. The ambiguity Nadia flagged isn't a minor content question.

Weapons needs contraband status signaling before it ships — EV taught consequence through the legal overlay, not through experience. That's the missing piece in Nadia's legibility concern.

First pass: ore, food. Two commodities. Prove the loop.

## Round: EVALUATE

### Soren (solo dev scope warden)

Vera's galaxy-size flag is the most important thing said in this discussion. I want to extend it.

Every commodity type you author has a minimum build cost that doesn't scale down because your galaxy is small. Ore needs: mine building geometry (intact + degraded), storage geometry, a price variable per system, a supply/demand curve or fixed differential, and a mission hook that moves it. That's approximately the same work whether your galaxy has 8 systems or 80.

Here's my agenda question: **what is the minimum commodity count that proves the trade loop is fun before M5 ships?**

One commodity — ore — gives you: production building, storage, inter-system price differential, hauling missions, and faction standing consequences if you sell to the wrong buyer. That's a complete economy proof-of-concept. Two commodities with different production footprints (ore = mine, food = grow-dome) give you triage: which building do I protect first?

Weapons is the standing-manipulation commodity Ren correctly identifies as load-bearing — but it requires contraband status signaling (Vera), Bar rumor surface (already open from Q9), and new-player legibility work (Nadia). That's a second-pass commodity, not a first-pass one.

Fuel with a flight constraint is a different game than this one. Fuel without a flight constraint is ore with a different skin. Don't build two commodities that do the same thing.

My scope question: **can the core loop — fly, find price differential, haul, earn standing consequence — be proven with one commodity type before the list expands?**

If yes, start there. Everything else is debt.

<!-- complete -->
