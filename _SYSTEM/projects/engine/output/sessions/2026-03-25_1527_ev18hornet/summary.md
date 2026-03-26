# Morning Brief: 2026-03-25_1527_ev18hornet

*Generated: 2026-03-25 16:01*

## Overnight Design Session Summary — 2026-03-25

Based solely on the provided ledger. No stub entries were detected; all entries are substantive and reportable.

---

### What Was Resolved

The session covered ten major design areas and produced a large number of binding decisions.

---

#### Space Layer & Navigation
The space layer is locked as **2D top-down** for the EV Core Loop milestone. Shallow 3D is deferred, not rejected, and reopens only after the core loop is validated with real player data. Navigation uses point-and-click or directional input with no camera rotation, no altitude axis, and no vertical targeting. Within-system travel flies on the 2D plane; system-to-system travel uses a hyperspace jump via galaxy map selection. Combat resolves fully on the 2D plane. Readability standards are explicit: the space layer must be parseable in 60 seconds by a player with zero EV context, the player ship is always the most visually prominent element, hostile contacts use a distinct color from faction palette, jump points are visually distinct landmarks, and each entity class must have a distinct silhouette at minimum nav-map scale.

---

#### Galaxy & Map Scale
Milestone 3 scope is defined as **4–6 hand-authored systems in YAML**, no procedural generation. The full galaxy map is visible from session one; access is gated by standing, faction passage, or jump point control — not map visibility. Hidden systems are rejected. Atmospheric terrain at Milestone 3 is one placeholder mesh per planet, color-swapped for biome identity. Authored investment at this milestone is faction geography and mission string placement only. Minimum faction structure requires 3–4 faction territories with 1–2 contested chokepoints, the player starting zone placed to lead naturally into contested space, and each planet carrying a faction owner/contested status, a mission string role, a standing threshold, and one placeholder mesh.

---

#### Atmospheric Entry
Entry is a **gated, irrevocable transition** — no abort once initiated. All entities follow identical transition logic. The first atmospheric entry in a session always plays the full ~3-second cinematic beat (external camera, ship crossing boundary, 3D layer loading behind it) with no skip option; subsequent entries use the same beat unless the player opts out. Control returns in mouse-flight mode, at altitude, oriented downward. Entry altitude derives from dive angle — steep dive produces low entry, shallow arc produces high entry. Escorts emerge behind the player in physics-derived formation order, not scripted timing. Raiding fleets that breach the 2D intercept window initiate their own dive on their own timeline. The atmosphere boundary must read as a distinct intentional surface via geometry and color alone — no haze, blur, or atmospheric scattering.

---

#### Raids & Destruction
Enemy factions can **permanently destroy buildings**. Loss condition is tier regression, not total destruction — settlement continues but loses tier-unlocked functions. Raid damage is targeted (infrastructure serving competing factions or threatening raiding interests), not random. Standing is the primary recovery currency; rebuild flow is standing-gated. Altitude-visible structures (e.g., docking towers) rebuild deliberately slower to create skyline absence as a meaningful scar. Destruction visual is removed geometry — the gap is the scar, not a particle effect. The emergence loop is defined: faction standing mismanagement → escalating raid scale → atmospheric defense failure → tier loss → economy contraction → standing re-engagement → faction re-pressure. Standing must be legible before it becomes consequential.

---

#### Fleet & Escorts
Fleet size is **capped by physical fighter bay slots** on the hull — no command rating pilot stat. Fleet composition docked at or patrolling a settlement contributes to deterrence. Raid scale is partially derived from demonstrated fleet strength at location; deterrence is emergent cause-and-effect, not a designer buff. A captured ship requires a port run before joining the fleet. The owning faction registers the loss at capture, opening a hot-hull window of earned risk. Capturing a faction ship is a standing trigger event, and that consequence must be legible at or immediately after capture. Faction provenance must be surfaced before the player commits to the port run. Fighter bay AI scope is a separate decision per milestone.

---

#### Co-op State Model
**Option B adopted**: the galaxy advances when the hosting player's instance is running. Option A (paused galaxy) rejected as a scheduling dependency. Option C (independent merging instances) rejected as untraceable artifacts. The hosting player's machine is the authoritative simulation host. Offline settlements attract harassment-scale raids only (deterrence math applied consistently, not a protection rule). A docked fleet contributes deterrence regardless of owning player's online status. Standing uses per-player tracks with shared settlement physical state. The return-log is required scope (not a print statement) and must include: which faction acted, what was destroyed, what standing moved and on whose track, and what intercept opportunity existed or was taken. It must be assigned a milestone slot before M8 co-op work begins.

---

#### Faction Commitment
A **hybrid model** is adopted: inverse standing math as ongoing pressure, authored bar mission as point-of-no-return gate. Mutual exclusivity is enforced by a boolean mission state flag, not a standing threshold value alone. The bar NPC becomes available at a standing threshold; mission acceptance triggers faction string closure. Gaining standing with one major faction costs standing with the other on a shared inverse axis (arithmetic). Simultaneous allied standing with both factions is possible before commitment; arithmetically self-defeating after; architecturally closed once mission is accepted. Two raid fleets simultaneously on the nav edge is a designed emergent situation. A player at negative standing who has not accepted the commitment mission is in a degraded but recoverable position. Player faction formation is flagged as post-City-tier.

---

#### On-Foot Combat
**Bar and exploration get full walking sim investment** as a session one hook. Boarding is permanently abstracted as a stats check. Raid breach defense gets minimal FPS treatment: one weapon type, raycast/simple projectile, basic enemy AI (idle/alert/attack/dead), hit feedback, death state, flat-poly assets — no cover geometry, no melee, no full animation rig. On-foot combat scope is explicitly capped at Settlement milestone (M7) and cannot expand into atmospheric layer polish hours.

---

#### Death & Respawn
**Option B adopted**: ship loss on death, respawn at nearest friendly port in a starter ship. Standing and credits survive death. Option A (zero penalty) rejected; Option C (unbanked credit loss) rejected; Option D (permadeath) rejected as default. Death is a world-state event — deterrence profile drops immediately, the killing faction registers a standing-relevant combat outcome, raid window advances. The death screen must surface exactly one sentence of faction consequence before respawn. Atmospheric death respawns the player at distance in 2D space above the system, facing a second dive decision. Re-entry after atmospheric death follows the existing dive angle rule.

---

#### Milestone 3 / EV Core Loop Scope
Minimum counts locked: **3 ships** (Shuttle, Light Fighter, one faction patrol class), **4 systems** (starting system, two faction-territory systems, one contested chokepoint), **4 buildings at Outpost tier** (Generator, Landing Pad, Comm Tower, Defense Turret). The first testable loop is: one ship, one system, two buildings, one faction patrol, one bar mission. Build sequence is testable loop first, complete scope second. Landing Pad is the first building placed in the first playable session. The first jump is the moment galaxy map, standing system, and atmospheric layer cohere as a single game.

---

### What Remains Open

The ledger carries **36 unresolved open questions** across all areas. The highest-dependency items are:

| Open Question | Blocks |
|---|---|
| Spatial model flag (2D vs. 3D) | M3 milestone estimates *(note: a separate DECIDED entry locks this as 2D — the OPEN entry appears to be a carry-forward artifact)* |
| Commitment threshold standing value | M5 faction standing API |
| Inverse axis ratio (1:1 or asymmetric) | M5 implementation |
| Faction string state in co-op | M5 faction standing API |
| Cross-player standing triggers | M5 faction standing API |
| Return-log milestone slot (M7 or M8) | First offline damage events unreadable if M7 proceeds without it |
| Harassment vs. assault raid definitions | Offline raid logic, M8 co-op scope estimate |
| Minimum building count at Outpost tier | State persistence estimates, co-op sync scope, raid targeting logic |
| Fleet AI milestone scope (first 2D escort AI) | M6 architecture vs. M6 functional AI |
| Tier regression rebuild tempo | Rebuild path spec |
| Respawn location rules | Death flow implementation |
| Starter ship acquisition at respawn | Death flow implementation |
| Hot-hull fate on death | Capture flow |
| Dual-offline canonical resumption state | M8 co-op spec |
| Host selection protocol | M8 co-op spec |
| Commitment mission count per faction | Bar content scope at M5 |
| Recovery cost for degraded-but-uncommitted standing | Must be consistent with tier regression rebuild decision |
| Weapon type for raid breach defense | On-foot combat implementation |
| Enemy AI behavior thresholds | On-foot combat implementation |
| Standing gate UX (how map communicates gated systems visually) | Player onboarding |
| Starting system faction ownership and chokepoint relationship | Sessions 2–3 design |

Additional open items exist for atmospheric escort behavior milestone timing, port run registration options, minimum altitude range, re-emergence behavior, raid timing communication, and shallow-3D visual language questions (deferred until review reopens).

---

### Summary

The session was highly productive: the core spatial, narrative, economic, and social loop decisions are now binding. The primary remaining risk is the cluster of M5 faction standing API dependencies — commitment threshold, inverse axis ratio, co-op faction string persistence, and cross-player standing triggers all need resolution before M5 can be specified. The return-log milestone slot is also flagged as a scheduling risk if M7 proceeds without it.
<!-- complete -->
