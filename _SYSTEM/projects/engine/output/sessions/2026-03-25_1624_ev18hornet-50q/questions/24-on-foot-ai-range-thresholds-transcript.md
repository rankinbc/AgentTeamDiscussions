# Transcript: On-Foot AI Range Thresholds

*Generated: 2026-03-25 17:53*

## Round: PROPOSE

### Ren (emergence systems theorist)

Range thresholds are downstream questions. The blocking constraint is building interior dimensions, which aren't specified anywhere in the decision ledger.

Here's the interaction chain that matters: sidearm effective range (open, needs config constant) × building interior depth × alert range = the corridor geometry that delivers the "you failed at airspace management" message. Author those three numbers independently and you get a fight that either never happens (alert range exceeds approach distance) or collapses into a melee the sidearm can't handle.

Two specific concerns from an emergence standpoint:

**Static thresholds ignore settlement tier entirely.** A raider alerting at the same distance inside a Claim Stake shelter and a Colony building is a system working in isolation. Building scale changes across tiers — the same threshold that produces desperate close-quarters defense in an Outpost produces a shooting gallery in a Colony corridor. If thresholds don't scale with geometry, the failure-state message changes character across tiers without anyone intending that.

**Alert range relative to chokepoints determines whether the player has a decision.** If alert fires before the player reaches a defensible position, breach combat becomes reactive. If alert fires after, it becomes a scramble. Both are valid — but neither is authored right now because we don't know where the chokepoints are in building geometry.

Before numeric thresholds: what are the interior dimensions of the three confirmed Outpost building types? That's the load-bearing question. Range values follow from geometry, not the reverse.

### Max (atmospheric flight advocate)

Ren's right that geometry precedes thresholds — but the geometry constraint is already partially answered by decisions we've made for a different reason.

The degraded state legibility requirement at 500m altitude means every building silhouette has to read as distinct flat-poly geometry from that altitude. That's not just an art note — it caps building footprint. A structure that's legible from 500m at Hornet speeds is not a large building. The Outpost shelter, power node, and storage unit all have to communicate their damage state as readable silhouettes. That's a small silhouette. Which means small interiors.

What I'd flag as the atmospheric layer concern here: if breach combat becomes mechanically interesting, you've created a competing draw. Players will learn that staying dirtside during a raid is viable strategy — maybe even preferable if the sidearm fight feels good. The SimCopter payoff, the whole reason the atmospheric layer matters, depends on the player *wanting* to be up there watching their settlement from altitude. The moment dirtside defense becomes the optimal play, the atmospheric layer becomes a commute.

So Ren's geometry-first approach is correct, but the geometry is bounded above by atmospheric readability requirements already in the ledger. Small buildings, tight corridors, no room to maneuver. That constraint doesn't need to be authored separately — it drops out of the 500m legibility requirement we've already committed to.

The range thresholds follow from that, and they should be authored to make the sidearm fight feel like a last resort, not a tactical option.

## Round: CRITIQUE

### Vera (EV systems historian)

The question is premature, and answering it now produces false precision.

EV's failure states worked because the consequence was legible at the moment it landed. You understood *why* you were being shot at — your standing was visible, the patrol geometry told you the story. The breach combat is supposed to carry that same legibility: "you failed at airspace management." But a number like "alert range: 8 meters" is not legible. It's a tuning parameter that means nothing without reference geometry.

Both Ren and Max are correct on the geometry-first point, but I want to name what's actually blocking here. It's not building dimensions. It's that we've decided breach combat is a failure state, and failure states in EV were designed *after* the success condition was working. You can't calibrate how bad the sidearm fight feels until you know what "successfully intercepted the raid" feels like from the atmospheric layer. The comparison is what produces the message.

Asking for alert and attack thresholds before M7 has a single playable breach is the same error as authoring a specific hostile floor value before M5 standing movement rates exist. We've deferred that correctly every time. The same principle applies here.

What the ledger should record: sidearm effective range and enemy alert range are named config constants, values deferred pending building geometry authoring and at least one playable atmospheric intercept for baseline comparison. The thresholds must produce a fight that reads *worse* than successful airspace management — and you can't author that relationship without both endpoints.

The question to answer before this one is building interior dimensions. Ren named it. That's the correct next question.

### Nadia (new-player experience advocate)

Vera's framing lands correctly for me, and I want to add the new-player dimension that's missing from this round.

The first breach encounter is not just a failure state — it's a teaching moment. It's the moment the game explains, in mechanical terms, why the atmospheric layer matters. That explanation only works if the player has something to compare it to. A new player who gets breached before they've had a clean atmospheric intercept isn't receiving the message "you failed at airspace management." They're receiving "enemies appeared inside my building and I died." Those are completely different lessons.

The first-raid protection window suppresses damage specifically to give new players a clean atmospheric view before consequence lands. The same logic applies here. Authoring alert and attack range thresholds before a player has experienced the thing those thresholds are punishing them for skipping — that's designing around the symptom.

Max's point about small buildings from the 500m legibility constraint is useful, but I'd push back slightly on one implication: tight corridors don't automatically produce legible failure states. A corridor that's mechanically "last resort" still needs to *read* as last resort to a player who's never been in it before. The sidearm's visual language (improvised, flat-poly, desperate) carries some of that. But the fight's pacing — how fast enemies close, whether the player has a breath before contact — that's what communicates the message.

Vera is right: building geometry first, playable atmospheric intercept for baseline, then thresholds. Same discipline we've applied to every other config constant in this ledger.

## Round: EVALUATE

### Soren (solo dev scope warden)

Building dimensions aren't specified, atmospheric intercept has zero playable data, and we're being asked for exact numbers.

Every config constant in this ledger that got deferred correctly — hostile floor, raid thresholds, standing deltas — got deferred because the same logic applied: you can't author a defensible value without the data that makes it defensible. Alert and attack range thresholds are the same category of question.

The team has already named the dependency chain correctly:

1. Building interior dimensions (currently unspecified for all three Outpost types)
2. At least one playable atmospheric intercept (M7 has no baseline yet)
3. Thresholds that produce a fight reading *worse* than successful intercept

You can't reach step 3 without steps 1 and 2. Authoring numbers now produces false precision that someone will tune against the wrong baseline.

What the ledger should record from this round:

- `ENEMY_ALERT_RANGE` and `ENEMY_ATTACK_RANGE` are named config constants, required from day one, values deferred
- Values are blocked on building interior dimension authoring and at least one playable atmospheric intercept session
- Thresholds must satisfy the constraint: breach fight feels demonstrably worse than successful airspace management — this is a behavioral contract, not a tuning preference
- Building interior dimensions for the three confirmed Outpost types (shelter, power node, storage unit) are the next blocking question

One additional flag: the 500m silhouette legibility requirement already caps building footprint. The interior dimensions follow from that constraint. That's not a new question — it's a consequence of a decision already in the ledger.

<!-- complete -->
