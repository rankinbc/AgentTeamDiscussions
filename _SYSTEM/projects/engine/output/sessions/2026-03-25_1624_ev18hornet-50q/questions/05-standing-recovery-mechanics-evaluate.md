### Soren (solo dev scope warden)

**[PROPOSE — Soren (scope estimator)]**

Before this round adds another design layer, I want to sequence what's actually being decided versus what's being designed.

Vera's three-band model is the right frame. The question is what each band *costs to implement*, because the bands aren't equal:

**Engaged → Degraded** is a read against a threshold. One conditional. Already implied by the 40-threshold tooltip work. Build cost: negligible.

**Degraded band behavior** — Bar contacts cold, missions sparse — requires NPC state reads against faction standing. Every NPC contact that changes behavior based on standing is a separate implementation point. "Sparse" missions means a filter pass on the mission pool. This is real work. Not enormous, but not free.

**Hostile floor recovery** — Vera's intermediary or authored string — is content work that has no ceiling. "An authored trigger to unlock the recovery path" is a quest. That's M6 or later, not M5.

My recommendation for M5 scope:

1. Implement the three bands as standing thresholds only — no behavioral differences in M5 beyond what's already decided (tooltip, commitment NPC, patrol density is M8)
2. Nadia's cold dialogue line is the right call and it's one string per faction contact — that's manageable if it's a single state, not a branching tree
3. Recovery mechanics in M5 = mission-gated, drawing from existing pool, no separate authored recovery type. Distinct recovery missions are content scope that belongs post-playtest.

The downward tooltip is the only open question I'd close today. Everything else is M6+ until the core loop has run.


<!-- complete -->
