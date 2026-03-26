### Soren (solo dev scope warden)

## Soren — Scope Sequencing

Vera made the build argument without naming it as one. Let me name it.

**"Authored" has two completely different cost structures in this game.**

Authored *faction geography* — which faction controls what system, which chokepoints overlap, what trade routes thread through — that's YAML and graph design. A week of careful work. Scales to 30 systems without breaking the budget.

Authored *atmospheric identity* — distinct terrain geometry, color zones, settlement grid reads from altitude, the frozen outpost that feels different from the arid colony — that's mesh work, test passes, and tuning per planet. At flat-poly speeds, call it 2–4 days per planet you want to feel distinct. Three planets per system across 12–15 systems is 36–45 planets. That's 3–4 months of asset work before a single mission string ships.

The room is accidentally conflating these two things. Every proposal says "12–15 authored systems" and means something different by "authored."

**My sequencing recommendation:**

Milestone 3 (Galaxy Layer): 4–6 systems. Faction geography authored in YAML. Atmospheric identities are placeholders — one terrain mesh per planet, color-swapped. The loop works or it doesn't.

Expand atmospheric variety *after* the EV Core Loop milestone tells you which planets players actually care about. You're not building 45 planets. You're building the 8 planets that earn repeat visits.

Nadia's "first jump" question is the right one. The answer is: it should exist at milestone 3. Everything else is milestone 5 or later.

How many systems do you actually need at milestone 3 for the faction-collision scenario to be testable?


<!-- complete -->
