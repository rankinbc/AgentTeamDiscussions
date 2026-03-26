# On-Foot Combat Depth

*Generated: 2026-03-25 15:53 | Question 8 | 170s | Mode: ev18hornet*

## Decisions

**On-foot combat is walking sim first, minimal raid defense second, and abstracted boarding permanently.**

The on-foot layer has three distinct contexts — bar and exploration, raid breach defense, and boarding — and each gets a different answer. Treating them as a single "on-foot combat depth" question produces scope drift. They are separated here by function.

---

**The bar and exploration are walking sim. This is where on-foot investment goes.**

Bar NPCs occupy physical space. The player walks through a door, sees characters at tables, approaches to trigger dialogue, sits to accept a mission. This is not ambient dressing — it is the first thing on-foot does in session one, before any settlement is built and before any raid is possible. The bar's atmosphere is the on-foot hook. Everything else in the on-foot layer earns its cost only after the bar feels like a real place.

Walking sim scope: movement, collision, interaction triggers, NPC proximity. No combat mechanics required. The bar is never hostile territory.

---

**Boarding is abstracted permanently. It is not a candidate for FPS expansion.**

Boarding resolves as a crew check after shields are depleted — a stats comparison, not a corridor. The earned difficulty is already designed: the hot-hull window, the faction standing trigger at the moment of capture, the port run required before the ship joins the fleet. That cost structure lands without an FPS layer. Adding a boarding FPS system would duplicate risk that already exists in the approach, impose 10–16 weeks of solo dev time, and overload new players who are simultaneously processing 2D space combat, standing consequences they may not yet fully understand, and a hot hull they need to survive to port.

EV resolved boarding as a stats check. The tension was positional and economic. That abstraction was the design, not a limitation. It is not reopened here.

If boarding is ever revisited as a physical FPS experience, it is a separate milestone with a separate scope estimate — not a feature added inside an existing milestone.

---

**Raid breach defense is the one on-foot combat justification. It gets one scope slot.**

When raiders survive the atmospheric layer and land, an on-foot defense option is the only mechanic that does work abstraction cannot: the player is physically present, has chosen to land, and the building they are defending is one they have flown over from altitude and watched be constructed. The SimCopter aerial view loads the stakes before the player ever touches down. Abstracted resolution cannot replicate that presence.

On-foot raid defense is: one weapon type, raycast or simple projectile, basic enemy AI (idle / alert / attack / dead), hit feedback, death state. Flat-poly assets apply. No cover geometry. No melee. No full animation rig. The player decision is binary — fight for this building or absorb the tier regression — and the system is sized to support that decision, not to expand beyond it.

On-foot combat scope is explicitly capped at the Settlement milestone (M7). It does not grow to absorb atmospheric layer polish time.

---

**What on-foot combat is for: atmosphere in session one, defense stakes in later sessions.**

The sequence that makes raid defense meaningful — fly over the skyline you built, recognize structures you placed, dive in to defend them — is a later-session payoff, not a first-session hook. The on-foot layer cannot be designed around that payoff as its entry point.

Session one on-foot is: walk into the bar, take a mission, place a building, explore the terrain. The combat mechanic earns its development cost only after the space feels worth defending.

---

**Scope boundary summary**

| Context | Treatment | Rationale |
|---|---|---|
| Bar and exploration | Walking sim — full investment | Session one hook; bar atmosphere is the on-foot entry point |
| Boarding | Abstracted permanently — stats check | EV precedent; cost already designed in standing/hot-hull/port-run chain |
| Raid breach defense | Minimal FPS — one scope slot, capped at M7 | Only context where physical presence does work abstraction cannot |
| Melee | Out of scope | Does not feed the emergence chain; no justification for cost |
| Cover geometry | Out of scope | Scope threat to atmospheric layer polish time |

---

**Rule: on-foot combat cannot expand into hours that belong to atmospheric layer polish.**

The differentiator in this project is flight feel — mouse-rate control, bank-and-roll, low-altitude terrain reads, settlement legibility from altitude. Any on-foot investment beyond the scope boundary above comes directly out of that time. The on-foot layer is the landing of the atmospheric arc, not a second arc running parallel to it.
<!-- complete -->
