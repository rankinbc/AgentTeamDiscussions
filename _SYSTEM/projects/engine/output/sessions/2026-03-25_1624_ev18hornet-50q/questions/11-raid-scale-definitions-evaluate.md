### Soren (solo dev scope warden)

**Soren**

Before ship counts: there's a scope bomb embedded in Max's framing that nobody's named.

"Tier regression needs to be *visible from altitude* — a physical change in the geometry you're flying over."

That's not a standing system question. That's a settlement geometry question. If a Settlement can visually revert to Outpost state, every building type needs at least two geometry states — erected and degraded — and the transition needs to be legible from 500 meters in flat-poly. Multiply that by however many building types ship at M7. That asset work can easily double the settlement art pass.

I'll flag it and set it aside, because it may be worth it. But it needs a cost acknowledgment before M8 scope estimation is meaningful.

On the actual blocking question — I'll take Nadia's position plus one constraint.

Two discrete compositions is the right call. Not for EV precedent reasons. For testability reasons. A continuous formula gives you infinite raid states to balance, none of which you can reliably reproduce during testing. Two compositions — harassment, assault — give you two test cases. You can verify each in isolation, tune each independently, and know exactly what you shipped.

The standing threshold that determines which spawns is a config value. Two numbers. Tunable from playtest data.

What I need defined before offline raid logic is scoped:

1. Does tier regression from raid damage ship in M5, M7, or M8?
2. How many building types exist at M7 settlement tier, and do they have degraded states?

Everything else follows from those two answers.


<!-- complete -->
