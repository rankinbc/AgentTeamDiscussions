# Space Layer: 2D or 3D?

*Generated: 2026-03-25 15:31 | Question 1 | 160s | Mode: ev18hornet*

## Decisions

**The Space Layer is 2D (top-down, EV-faithful) at Milestone 3 (Galaxy Layer). Shallow 3D is a deferred option, not a current build target.**

---

## Space Layer: Design Specification

### Governing Decision

The Space Layer uses a 2D top-down representation consistent with Escape Velocity's galaxy map and system-travel screen. This is a deliberate design choice, not a scope concession. The decision is binding through the EV Core Loop milestone and subject to review after the core loop is validated as fun.

Shallow 3D space is not rejected permanently. It is deferred because it is unestimated scope on a solo project — an architecture no shipped game has cleanly solved — and because the emergence problem it solves does not yet exist at milestone three. The dive-toward-atmosphere scenario requires 20+ hours of player context; it cannot be built toward before that context exists.

---

### Space Layer Behavior

**Representation**
- Top-down 2D. Stars, planets, stations, and ships occupy a flat plane.
- The player navigates using point-and-click or directional input on the map plane.
- No camera rotation. No altitude axis. No vertical targeting.

**Navigation**
- System-to-system travel via hyperspace jump: select destination on galaxy map, confirm, transition.
- Within-system travel: direct flight toward target on the 2D plane with arrival proximity trigger.
- Planets, stations, and jump points are fixed landmarks visible at all times.

**Threat and Combat**
- Hostile ships appear on the nav plane as standard sprites or flat-poly shapes.
- Threat geometry is always fully visible — no camera rotation required to locate enemies.
- Combat is resolved on the 2D plane: approach vectors, firing arcs, and intercept geometry all read from a single overhead view.
- Faction fleet raids appear as incoming contacts on the nav edge, giving the player time to intercept or evade before the fleet reaches the planet.

**Layer Transition**
- Entering a planet's atmosphere is a deliberate player action: fly to planet, trigger landing/entry.
- The transition from 2D space to 3D atmosphere is the dimensional payoff. Space is strategic and flat; atmosphere is tactile and deep. The shift is the design, not a seam to paper over.
- This contrast protects the Atmospheric Layer's identity. The mouse-flight, bank-and-roll, and SimCopter moment over the player's settlement are earned by arriving from a flatter world.

**Raid Handoff**
- When a hostile fleet reaches a planet, the game transitions to the Atmospheric Layer for the defense engagement.
- The raid is not a notification — it is an intercept opportunity in 2D space first, then an atmospheric engagement if the player fails to stop it or chooses not to.
- This preserves a meaningful faction standing → raid → defense chain without requiring 3D spatial geometry in the space layer.

---

### Legibility Rules (First Session)

The space layer must be readable within 60 seconds by a player with zero EV context.

- **Player ship** is always the most visually prominent element on screen.
- **Planets and stations** have persistent labels. Size indicates rough importance.
- **Hostile contacts** use a distinct color from the faction palette — no ambiguity between neutral traffic and threat.
- **Jump points** are visually distinct landmarks, not unmarked edges.
- **Nav map zoom** defaults to showing the player's current system fully, not the galaxy. Galaxy view is a deliberate zoom-out.

Flat-poly in space means geometry does the legibility work that textures and normal maps do elsewhere. Each entity class (ship, planet, station, asteroid, jump point) must have a distinct silhouette at minimum nav-map scale.

---

### What 2D Space Is Not

- It is not a loading screen. The space layer has its own gameplay: interception, faction patrol avoidance, escort timing, and resource transit decisions.
- It is not a lesser version of EV's space. EV's space layer worked because it was solved and readable. This is the same solution.
- It is not permanent. After the core loop is fun and the faction/standing system is validated, the shallow-3D question reopens with real player data and scoped build estimates.

---

### Deferred: Shallow 3D Space (Post-Core-Loop Review)

The emergence scenario Ren describes — hostile fleet drops out of warp above the planet, player dives toward atmosphere using terrain as cover — is a valid and exciting design target. It is not the current build target.

If shallow 3D is revisited, the following must be answered before scoping begins:

1. **Vertical range:** What is the minimum and maximum altitude delta between space and the atmosphere boundary? This sets the extent of the "shallow" constraint.
2. **Camera system:** Does the camera pitch to follow vertical movement, or does vertical position express as an on-screen indicator? Either answer creates UI work.
3. **Targeting in 3D:** How does the targeting reticle communicate that an enemy is above or below the player's current flight plane in a flat-poly, texture-free environment?
4. **Altitude readability:** What visual language tells a new player their elevation relative to the planet without textures, lighting, or atmospheric haze?

These are not rhetorical questions. They are the design debt that shallow 3D incurs. Answer them with prototypes, not proposals, before committing scope.

---

### Milestone Binding

| Milestone | Space Layer State |
|---|---|
| Tech Spike | Not built |
| Hornet Layer | Not built |
| Galaxy Layer | **2D space, EV-faithful — build target** |
| EV Core Loop | 2D space, fully integrated with faction/standing |
| Faction & Standing | 2D space, raid intercept loop validated |
| Post-Core-Loop Review | Shallow 3D reopens as scoped decision |
<!-- complete -->
