# Layer Transitions: Seamless or Gated?

*Generated: 2026-03-25 15:38 | Question 3 | 192s | Mode: ev18hornet*

## Decisions

**Atmospheric entry is a gated transition with a designed entry sequence. It is not technically seamless and does not require simultaneous layer residency.**

**Entry is a committed, irrevocable action. Once the player initiates a dive, they are in the entry state until they emerge in atmosphere. There is no abort.**

**All entities — player ships, escort ships, faction raiders — follow identical transition logic. No entity spawns inside atmosphere by designer fiat.**

**The first atmospheric entry in a session always plays the full cinematic beat. Subsequent entries use the same beat unless the player opts out after they have demonstrated understanding.**

---

## Layer Transition: Design Specification

### What "Seamless" Actually Means Here

The word seamless describes a player experience, not an architecture. The goal is that atmospheric entry feels like arrival in a continuous world — not like a menu, not like a load screen, not like a teleport.

This does not require both layers to be simultaneously resident in memory. It requires the transition to carry spatial and narrative weight. The distinction matters for scope: true simultaneous streaming is a milestone-scale engineering problem in Godot 4. A gated transition with a designed entry sequence costs two to three weeks and achieves the same player experience.

The decision is: **feels seamless, not technically seamless.**

### The Entry Sequence

Atmospheric entry is triggered by a deliberate player action — the same action already decided for layer transition. On commit:

1. The 2D space layer suspends. Faction contacts freeze in their last known positions.
2. An external camera takes over for approximately three seconds. The player's ship is visible against the flat-poly atmosphere boundary. The ship punches through.
3. The 3D atmospheric layer loads during these three seconds behind the camera beat.
4. Control returns to the player already in mouse-flight mode, at altitude, oriented downward toward terrain.

The three-second camera sequence is not cosmetic. It is the visual grammar for "you have crossed a threshold." The flat-poly atmosphere boundary must read as an intentional surface — an edge of the world, not an artifact. This beat does the UX work of teaching the player that commitment has occurred.

### Entry Is Irrevocable

Once the dive is initiated, the player cannot abort. This is a design decision, not a technical limitation.

The raid intercept opportunity exists in 2D space, before entry. The player sees inbound faction contacts on the nav edge before they reach the planet. They choose: intercept in space, or dive now and let escorts handle the approach. Diving is a consequential spatial decision. Making entry revocable would dissolve that consequence.

The player exits atmosphere via the same committed logic in reverse — a deliberate re-emergence action that transitions back to the space layer.

### Variable Entry Altitude

Entry altitude is a function of dive angle, not a fixed designer value.

A steep dive produces a low entry point — compressed reaction time, enemies potentially already at engagement range. A shallow arc produces a high entry point — altitude buffer, time to read the terrain and settlement state before descending.

The designer does not author "player arrives to find the settlement under attack." The player's spatial decision about when and how to dive produces that situation, or prevents it. This is the emergence principle applied to layer transitions.

### Entity Symmetry

Every entity that transitions between layers follows the same ruleset.

Escorts queue through on the same vector as the player, emerging behind them in formation order. The timing is physics-derived from their position relative to the atmosphere boundary at commit time — not scripted.

Faction raiders that break through the 2D intercept opportunity initiate their own dive on their own timeline. Depending on when the player dove, the raiding fleet may arrive in atmosphere ahead of the player, concurrent, or behind. The player's dive timing determines which scenario they inherit. The designer did not write that scenario. The player's decision and the raiding fleet's approach vector produced it.

Faction ships may not bypass the transition. There is no atmospheric spawn point for enemies. If a raid is in atmosphere, it entered through the transition, and the player had a 2D intercept window before that happened.

Violating entity symmetry — spawning raiders inside atmosphere for dramatic effect — would break the faction standing system at its foundation. EV's standing worked because every consequence was traceable to a player or faction action. Scripted spawns insert a consequence with no traceable cause. Players will feel the incoherence even without identifying it.

### New Player Legibility

The first atmospheric entry always plays the full cinematic beat with no option to skip.

A new player has not yet learned that atmospheric entry is a commitment with timing consequences. The cinematic beat — external camera, ship against the atmosphere boundary, the crossing — is the moment they learn what is happening. It is not an aesthetic flourish bolted onto a physics system. It is the signal that a decision has been made and is now in motion.

After the first entry, the player has the experiential vocabulary to understand subsequent dives as spatial decisions. At that point the transition can be abbreviated if desired. Earning the raw transition means understanding what it costs.

The flat-poly atmosphere boundary itself must carry this signal. It should read as a distinct visual surface — a layer edge — not as ambient environmental detail. The aesthetic commitment (flat-poly throughout) means altitude readability and layer legibility must come from geometry and color alone, not from haze, blur, or atmospheric scattering. The boundary is a flat-poly object that the ship visibly crosses.

### What Remains Open

The following questions are not resolved by this discussion and carry forward:

- **Minimum altitude range:** What is the vertical delta between atmospheric entry point and lowest flyable altitude? This determines how much time the player has to read settlement state after a steep dive before they are at engagement range.
- **Re-emergence behavior:** Does exiting atmosphere trigger a symmetric exit sequence, and what is the player's state in 2D space on return — same position, same vector, or deterministic spawn point?
- **Raid timing communication:** How does the 2D nav layer communicate "raiding fleet is 40 seconds from atmosphere entry" in a way that is legible to a player who has not yet experienced an atmospheric raid?
<!-- complete -->
