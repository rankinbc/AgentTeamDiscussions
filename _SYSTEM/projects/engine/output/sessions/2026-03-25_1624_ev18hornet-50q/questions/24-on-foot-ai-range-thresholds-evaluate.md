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
