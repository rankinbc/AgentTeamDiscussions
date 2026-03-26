### Soren (solo dev scope warden)

The group has correctly identified the design tension. Let me put the build cost on the table before the architecture gets decided.

**What Nadia proposed (presence-modifier, flat rate) costs:**
- Income constant per building type — config, one afternoon
- Building presence check at income tick — trivial read against existing building list
- Total estimate: 1–2 days including tests

**What Max and Ren proposed (operational-status, per-type degradation coefficients) costs:**
- Damage state exposed as a queryable value per building instance — requires damage model to exist and emit readable state
- Per-type degradation coefficients — config is cheap; the multiplier relationship between power and other types is not
- Power-as-output-multiplier means the income calculation has a dependency graph: power state affects storage output rate affects trade income — that's not a coefficient, that's a runtime query chain
- Estimate for the dependency graph alone: 1–2 weeks, higher if building count grows

The dependency graph is the flag. "Named config constants per building type" describes the tuning surface, not the architecture. The architecture is a directed graph of building states feeding into an income calculation. That's a new system, not a new config file.

**The sequencing implication:**
Operational-status income cannot ship before the building damage model exposes live queryable state. That model doesn't exist. Presence-modifier income can ship the day buildings can be placed.

Vera's "signal vs. system" question is the agenda question. My answer: signal first, because the system requires infrastructure that isn't built yet. Presence-modifier in M7. Operational-status earns scope when the damage model is live and we have playtest data on raid frequency.


<!-- complete -->
