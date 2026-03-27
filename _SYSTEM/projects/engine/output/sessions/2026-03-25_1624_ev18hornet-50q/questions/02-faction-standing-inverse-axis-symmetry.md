# Faction Standing Inverse Axis Symmetry

*Generated: 2026-03-25 16:30 | Question 2 | 169s | Mode: ev18hornet*

## Decisions

**Faction Standing Loss Multiplier:** 1.0 (symmetric) for M5, implemented as a named constant `FACTION_STANDING_LOSS_MULTIPLIER` in config.

**Faction-Specific Heat:** Out of M5 scope. Post-playtest tunable only, requires playtest data before values are defensible.

**Defection Cost Asymmetry:** Deferred. Asymmetric multipliers have a legitimate role in making post-commitment defection costly — but that is a different design question from pre-commitment exploration cost, and a different implementation point. Not in M5.

---

## Faction Standing — Inverse Axis Design

### The Axis

Faction standing operates on a 0–100 scale per faction. When a player gains standing with one faction, opposing factions lose standing by an amount determined by `FACTION_STANDING_LOSS_MULTIPLIER`. For M5, that multiplier is **1.0**: one point gained with Confederation costs exactly one point with Rebels.

### Why Symmetric for M5

The primary argument for asymmetry was preventing permanent neutrality — the failure mode where a player samples both factions indefinitely and never experiences faction pressure. That failure mode is already handled by the commitment NPC trigger condition: standing ≥ 60 AND at least one completed faction mission. A player who samples both factions in equal measure does not reach 60 with either. The commitment NPC is absent. The content wall is already in place. An asymmetric multiplier does not add drama to that situation; it adds arithmetic to a problem already solved by a different mechanism.

Asymmetry without surfaced feedback is invisible punishment. The standing tooltip fires the first time any faction standing crosses 40 — that is the moment the system becomes legible to a new player. Asymmetric math that operates before the tooltip fires penalizes players who have no frame for what they are doing wrong. The emergence chain requires players to be able to read the system they are inside before that system produces meaningful pressure.

Implementation cost is identical between 1.0 and 1.5. This is a named constant. The decision is not worth the build time of further deliberation before playtest data exists.

### The Named Constant

```
FACTION_STANDING_LOSS_MULTIPLIER = 1.0
```

This constant is:
- Applied to every opposing-faction standing delta when a player gains standing through missions, trade, or actions
- Overridable per-faction rivalry in a later config extension (the architecture must support this from day one, even if no per-faction overrides are authored for M5)
- The single implementation point for all future asymmetry decisions — no hardcoded ratios elsewhere in the standing system

### Defection Asymmetry (Deferred)

Asymmetric multipliers have a legitimate design role in one specific scenario: a player has committed to a faction and later performs actions for the opposing faction. At that point, the cost of defection could reasonably exceed the cost of exploration — the player has a standing relationship to damage, not just a neutral axis to drift along.

This is a post-commitment question. It is not a pre-commitment question. The multiplier direction (does gaining rebel standing cost more confederation standing *after* commitment than before?) and the implementation point (does commitment flag change the multiplier?) are separate design decisions that require the commitment system to be running before they are meaningful to answer.

These decisions are explicitly out of M5 scope. They are recorded here so they are not re-litigated as a symmetric-vs-asymmetric question — the symmetric decision applies to the pre-commitment state only.

### What Is Not Decided Here

- **Per-faction rivalry heat** — which faction pairs have hotter relationships than others. Requires playtest data. Post-M5.
- **Defection multiplier after commitment** — whether `FACTION_STANDING_LOSS_MULTIPLIER` increases once a player has triggered the commitment NPC. Requires the commitment system to be live and observable. Post-M5.
- **Standing floor behavior** — whether standing can fall below a certain threshold with an allied faction or whether floor mechanics apply. Not addressed by this decision.

### Open Items Inherited from Prior Sessions

- Exact dialogue content for commitment NPC across different settlement tier contexts
- Whether standing tooltip appears at crossing 40 in both directions or only upward
- Content system implementation for reading settlement/raid variables into NPC dialogue
<!-- complete -->
