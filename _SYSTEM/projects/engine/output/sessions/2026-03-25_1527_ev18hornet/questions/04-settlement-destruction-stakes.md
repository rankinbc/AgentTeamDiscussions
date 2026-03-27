# Settlement Destruction Stakes

*Generated: 2026-03-25 15:40 | Question 4 | 165s | Mode: ev18hornet*

## Decisions

**Enemy factions can permanently destroy buildings during raids.**

**The loss condition for a settlement is tier regression, not total destruction.** A raided settlement does not cease to exist. It loses the functions its current tier unlocked — docking capacity, faction-specific trade infrastructure, manufacturing chains. Tier regression is the meaningful consequence because it collapses standing investment and time, not raw materials. Losing a Colony back to Settlement is a loss worth caring about. Losing a Claim Stake is recoverable noise.

**Raid damage is targeted, not random.** Raiders systematically destroy infrastructure that services competing factions or threatens the raiding faction's interests. This is not a punishment mechanic. It is faction simulation — legible behavior with a cause. Players who understand the faction system will be able to read *why* specific buildings were hit. Arbitrary damage is rejected.

**Standing is the primary currency of recovery, not resources.** If rebuilding requires resources primarily, the settlement layer becomes a resource game with faction flavor. If rebuilding requires standing re-engagement primarily — negotiating with the same faction system that generated the raid — the game stays inside the EV contract. The faction system must be queryable by the settlement rebuild flow. This is a dependency, not flavor.

**Rebuild speed for altitude-visible structures is deliberately slower.** This is not a balance decision. It is an attachment decision. If a docking tower can be replaced in thirty seconds, the absence in the skyline meant nothing. The gap must persist long enough to hurt. The emotional payoff of flying over a settlement you recognize and seeing its silhouette has changed — before landing, from 800 meters — requires that gap to have cost something to close.

**Visible absence is the destruction visual.** In flat-poly, a destroyed building is not a smoldering ruin with particle effects. It is removed geometry. The scar is the gap. This is an aesthetic advantage, not a limitation, and it is not a scope concern. Rendering destruction in this style is cheaper than any other art direction.

**Standing must be legible before it becomes consequential.** The raid is the exam, not the lesson. A player whose first experience of the faction consequence system is watching buildings disappear without prior warning will not experience earned grief — they will experience churn. The standing feedback moment already decided for the starting system is not optional scaffolding. It is the prerequisite that makes every downstream loss readable. Players must have seen their standing move, seen a faction contact arrive on the nav edge, and made a conscious intercept choice before a raid resolves against their settlement. Loss without prior legibility is not drama.

**The emergence chain is: faction standing mismanagement → raid scale escalates → atmospheric defense fails → settlement loses tier functions → faction access and economy contract → recovery requires re-earning standing → which re-engages the faction system that generated the raid.** This loop is self-reinforcing without authored consequences. The faction that raided continues to apply pressure because standing is the variable, not a script.

---

## State Persistence Requirements

The primary implementation concern is not rendering — it is data. Targeted destruction requires every building to carry a per-settlement exists/destroyed state that survives:

- Session boundaries
- Co-op sync (one player in space, one player on foot when a raid resolves)
- Raid resolution during atmospheric absence (raids that complete while the player is not present)
- The recovery rebuild flow, which must read faction standing before permitting reconstruction

This is a data model problem. The scope of that model is directly proportional to the number of distinct building types per tier multiplied by the number of active settlements. That number is not yet defined.

---

## Open Questions

**1. Tier regression rebuild path:** Does recovering from tier regression require the same founding investment (same standing threshold, same resource prerequisite) as the original construction, or is there a faster recovery path? This answer sets the tempo of the entire defense loop. The constraint is that standing must remain the primary gate regardless of tempo.

**2. Building type count at Outpost tier:** What is the minimum building vocabulary at Outpost tier? This number drives every state persistence estimate, co-op sync scope, and raid targeting logic. It must be defined before settlement scope can be estimated.

**3. Faction system queryability:** At what milestone does the faction system become queryable by the settlement rebuild flow? If standing-gated rebuilding is required at the Settlement milestone (Milestone 7), the faction standing system (Milestone 5) must expose a standing check API before that milestone closes. This dependency should be flagged in the Milestone 5 acceptance criteria.
<!-- complete -->
