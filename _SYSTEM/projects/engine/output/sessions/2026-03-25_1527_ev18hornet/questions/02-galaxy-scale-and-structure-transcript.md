# Transcript: Galaxy Scale and Structure

*Generated: 2026-03-25 15:34*

## Round: PROPOSE

### Max (atmospheric flight advocate)

## Max — Atmospheric Layer Advocate

Here's the thing everyone misses when they argue procedural vs. authored: **galaxy scale directly determines how rare atmosphere entry feels.**

If you've got 200 randomly generated systems, planets become waypoints. You skip over them. The atmospheric layer becomes a loading screen you tolerate between jump points. That's the death condition for everything we're building.

EV's ~50 systems worked because **every planet had a personality.** You knew Rebels owned the frontier systems. You knew certain planets had the gear. That knowledge was earned through play. When you finally had reason to land somewhere new, it mattered.

My position: **start authored, small, and dense.**

12–15 hand-crafted systems. Each system has 1–3 planets with distinct atmospheric identities — a gas giant you can't land on (pure vista), an arid colony world with visible settlement grids from altitude, a frozen outpost where the terrain geometry shifts color zones. Players will visit these dozens of times. They need to feel like *places*.

The SimCopter payoff only works if the world below is *yours* and *recognizable*. You can't get attached to a procedurally shuffled hex tile.

**Procedural can come later** — after the authored template proves the loop works. Then you're generating variations on a proven structure, not gambling on emergence.

The galaxy map isn't the game. It's the strategic layer that **earns** atmosphere entry. Keep it tight, authored, and legible — so every jump toward a contested planet feels like a decision with weight.

How many systems feels right to the room?

### Ren (emergence systems theorist)

## Ren — Systems Interaction Mapping

Max is right about authored density, but I want to reframe *why*.

The case for 12–15 authored systems isn't about attachment to pretty planets. It's about **faction geography as an interaction substrate**. The emergence chain — standing → raids → atmospheric defense → on-foot — only generates novel situations if the geography creates contested zones where multiple factions have competing claims. Procedural systems don't guarantee that. You can generate 200 systems and end up with clean territorial partitions where factions never actually collide. That's worse than small and authored.

What you need structurally: 3–4 faction territories with **deliberate overlap zones** — systems where two factions both want to be, where trade routes cross, where the player's settlement location puts them in the middle of something. The authored choice isn't "what does this planet look like" — it's "where do faction interests intersect in ways that create player situations the designer didn't script."

On map visibility: show the full galaxy map from session one. Hidden systems are a scripted reveal mechanic dressed as exploration. Emergent exploration happens when the player *knows* what's out there but has to *earn* access — standing gates, faction passage, jump point control. That's agency operating on a known state, not discovery as authored content drip.

So: 12–15 systems, fully visible, designed around 2–3 contested chokepoints where faction territories overlap. The map isn't small — it's *loaded*.

The procedural question reopens when you're generating *variants* of that proven contested-zone structure, not before.

## Round: CRITIQUE

### Vera (EV systems historian)

## Vera — EV Systems Historian

Both proposals land near 12–15 systems and treat that as conservative. I want to challenge the framing before the number hardens.

**EV didn't feel infinite because of system count. It felt infinite because standing gates meant the map was visible but not accessible.** You could see Auroran space from session one. You couldn't reach it meaningfully until you'd earned passage or built a ship that could survive the encounter. That's a different mechanism than "more systems = more exploration."

The dangerous assumption in both proposals: that authored *geography* is what made EV planets feel like places. It wasn't. EV's planets were functionally identical visually. What gave them identity was **which missions were strung there, which factions' equipment they sold, and what standing you needed to land safely.** Disable the mission strings and faction economy and EV's planet art tells you nothing.

So the real authored investment isn't terrain variety. It's **faction logic and mission string placement.** That scales differently. You can support 30 systems if each system's authored content is "which faction owns this chokepoint and what mission string threads through it" — that's YAML and graph structure. You cannot support 30 systems if each requires distinct atmospheric terrain art.

My flag on Ren's "fully visible from session one": correct for EV, but needs a corollary. Visible ≠ accessible. The map shows everything. Standing gates everything worth having.

**Question I'd put to the room:** What's the minimum number of systems needed for two simultaneous contested chokepoints that don't overlap on the same trade route?

### Nadia (new-player experience advocate)

## Nadia — New-Player Experience Advocate

Vera nailed the mechanism, but I want to pull it toward the player side of the table.

**Standing gates are only meaningful if the player understands what they're gating.** EV veterans read a red-faction system and know the cost/benefit calculation. A new player reads it as "I got shot for no reason." That's not an emergence situation — that's a punishment with invisible rules.

The 12–15 authored system count feels right to me, but the **first system needs a different design contract than the rest of the map.** It has to teach the faction legibility language before the player enters a contested chokepoint. If they jump into a collision zone in session one without knowing what faction colors mean, what standing is, or why the raids are coming — the emergence chain Ren described reads as chaos, not strategy.

My specific concern with "full map visible from session one": I love the philosophy, but the player's eye needs somewhere to land. A dense map of 12–15 systems shown simultaneously to someone who doesn't know EV is a wall of noise. The map isn't small — it's loaded, as Ren says — but **loaded for who?** The starting system needs to be a legible tutorial in faction geography before the stakes of the contested zones matter.

**Concrete ask:** Does any proposal include what the player's first jump feels like? Not the third — the first. That's where the flat-poly aesthetic, the standing system, and the atmospheric layer all make their first impression simultaneously.

That's the session-one design question I'd put to the room.

## Round: EVALUATE

### Soren (solo dev scope warden)

## Soren — Scope Sequencing

Vera made the build argument without naming it as one. Let me name it.

**"Authored" has two completely different cost structures in this game.**

Authored *faction geography* — which faction controls what system, which chokepoints overlap, what trade routes thread through — that's YAML and graph design. A week of careful work. Scales to 30 systems without breaking the budget.

Authored *atmospheric identity* — distinct terrain geometry, color zones, settlement grid reads from altitude, the frozen outpost that feels different from the arid colony — that's mesh work, test passes, and tuning per planet. At flat-poly speeds, call it 2–4 days per planet you want to feel distinct. Three planets per system across 12–15 systems is 36–45 planets. That's 3–4 months of asset work before a single mission string ships.

The room is accidentally conflating these two things. Every proposal says "12–15 authored systems" and means something different by "authored."

**My sequencing recommendation:**

Milestone 3 (Galaxy Layer): 4–6 systems. Faction geography authored in YAML. Atmospheric identities are placeholders — one terrain mesh per planet, color-swapped. The loop works or it doesn't.

Expand atmospheric variety *after* the EV Core Loop milestone tells you which planets players actually care about. You're not building 45 planets. You're building the 8 planets that earn repeat visits.

Nadia's "first jump" question is the right one. The answer is: it should exist at milestone 3. Everything else is milestone 5 or later.

How many systems do you actually need at milestone 3 for the faction-collision scenario to be testable?

<!-- complete -->
