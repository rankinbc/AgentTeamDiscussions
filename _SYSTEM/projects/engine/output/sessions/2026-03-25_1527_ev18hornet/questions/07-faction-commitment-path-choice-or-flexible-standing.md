# Faction Commitment: Path Choice or Flexible Standing?

*Generated: 2026-03-25 15:50 | Question 7 | 179s | Mode: ev18hornet*

## Decisions

**Faction commitment uses a hybrid model: inverse standing math as the ongoing pressure system, authored bar mission as the point-of-no-return gate.**

Pure inverse-axis emergence is correct for everything after commitment. Gaining standing with one major faction costs standing with the other on a shared axis — this is arithmetic, not authored content, and it makes greedy optimization self-defeating without requiring a cutscene. But the point of no return is not a numerical threshold crossing silently in the background. It is a mission accepted in the bar, from a named NPC, whose dialogue explicitly names the cost before the player confirms. The math handles the consequence. The mission handles the moment.

This is not a menu lock. It is not a dialog box saying "you've made your choice." It is a mission record with a flag and a standing-check that closes the opposing faction's string when accepted. The bar NPC surfaces the cost. The player makes a conscious decision. Everything after is the standing system doing its work.

**Standing must be legible before the commitment moment, not discovered retroactively.**

A new player who does not know the standing tracks share an inverse axis will optimize greedily — accepting missions from both faction bars because nothing has yet told them that is self-defeating. The authored mission gate is not EV nostalgia. It is onboarding. The bar NPC who says "if you take this contract, the Rebels stop talking to you" is doing work the math cannot do alone. This is the same rule already applied to raid escalation: standing must move visibly before it becomes consequential. The commitment gate is the legibility moment for the faction exclusivity system.

**Simultaneous allied standing with both major factions is possible up to the commitment threshold; it is arithmetically self-defeating past it; it is architecturally closed by the authored mission gate.**

Three zones: before the gate, dual-faction play is possible but the inverse relationship creates natural friction. After the commitment mission is accepted, the opposing string closes. "Playing both sides" is not prohibited by rule — it is made impossible by narrative state and made costly by math before that state is reached. The player who tries to maintain both tracks experiences escalating raid pressure from both factions simultaneously before the gate ever fires. That pressure is the system communicating that a choice is coming.

**Two raid fleets on the nav edge simultaneously is a designed situation, not a punishment.**

If a player delays commitment long enough that both faction standing tracks are degraded, overlapping raid windows are the emergent consequence. This is not a trap. It is the faction system producing a crisis the player authored through their own choices. The rule — standing must be legible before it becomes consequential — means the player has already seen both standing tracks move, seen faction contacts on the nav edge, and made intercept choices before this situation resolves. The double raid window is not a surprise. It is the conclusion of a readable escalation sequence.

**Mutual exclusivity is enforced by mission state, not standing value alone.**

Standing math creates pressure. The authored mission creates the irrevocable state. A player at negative standing with the Confederation but who has not yet accepted the Rebel commitment mission is not locked out — they are in a degraded but recoverable position. A player who has accepted the commitment mission is locked. The distinction matters for implementation: the faction string closure is a boolean flag on a mission record, not a standing threshold check. The standing threshold triggers the NPC's availability. The mission acceptance triggers the closure.

**Player faction formation is not current scope.**

The concept is correct: a late-game player whose settlement reaches City tier could become a nav entity — a faction with its own standing tracks, its own raid calculation inputs, its own skyline identity readable from altitude. The emergence reversal Ren described (early game: player is a variable in their simulation; late game: they are a variable in yours) is the right design destination. The bar acknowledging player faction status before the nav map does is the right sequencing within that destination.

But player faction formation requires: a new entity type in the nav simulation, bidirectional standing tracks pointing at the player faction, raid calculation logic reading player faction strength as an input, settlement geometry readable as a distinct silhouette, and bar NPC dialogue that acknowledges the player's changed status. These span four implementation domains. City tier is not yet proven reachable or fun. There is no milestone slot for this work. Player faction formation is flagged as a post-City-tier design target, not a current build commitment. It is not designed further until City tier is validated and a milestone can absorb it explicitly.

---

## Open Questions

**Commitment threshold standing value:** At what standing value with each faction does the commitment NPC become available? This is the parameter that sets how long dual-faction play is viable before the gate opens. Must be defined before M5 faction standing API is specified.

**Inverse axis ratio:** Is the inverse relationship 1:1 (every point gained with Confederation costs exactly one point with Rebels) or asymmetric? Asymmetric ratios create factions that are easier to join than to leave. The ratio is a tuning decision but it must be a named decision before M5 implementation.

**Commitment mission count per faction:** Each major faction needs at least one authored commitment mission. Is there one gate per faction or a multi-mission string leading to an irrevocable final mission? The answer affects bar content scope at M5.

**Faction string state persistence in co-op:** If Player 1 accepts the Confederation commitment mission, does Player 2's Rebel string close? Or do per-player standing tracks mean Player 2 remains uncommitted? This branches from the already-open cross-player standing trigger question and must be resolved before M5 faction standing API is specified.

**Recovery from degraded-but-uncommitted standing:** If a player has badly degraded standing with one faction but has not yet accepted the commitment mission, is recovery possible? If yes, what does it cost and is it standing-gated like settlement rebuild? The tempo answer here should be consistent with the tier regression rebuild path decision already flagged as open.
<!-- complete -->
