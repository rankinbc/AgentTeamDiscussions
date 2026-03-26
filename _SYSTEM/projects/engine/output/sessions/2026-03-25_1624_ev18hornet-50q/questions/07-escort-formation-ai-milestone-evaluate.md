### Soren (solo dev scope warden)

[PROPOSE - Soren (scope estimator)]

Before we answer the milestone question, I want to put build cost on the table, because this discussion has been expanding scope without acknowledging what that costs.

Formation AI is not one feature. It is at minimum:

1. **Offset following** — simple, 3–5 days in 2D, doubles in 3D because you're managing pitch and bank, not just heading
2. **Layer-transition contract** — Nadia correctly identified this; "holds at entry altitude" sounds cheap but requires detecting layer entry, queuing a hold behavior, and making it legible to the player. Call it 2–4 days.
3. **Faction affiliation wiring** — Ren's correct that escort standing must read from the same system. But this is also a non-zero item if it hasn't been built yet.
4. **Galaxy-layer feel validation** — Vera's sequencing argument is right and is also free: you get this data by shipping 2D first.

M6 is the Fleet milestone. That milestone already carries ship acquisition, fleet composition UI, and escort hire flow through The Bar. The plate is not empty.

**My agenda for this round:**

1. What is M6's current estimated scope *without* escort AI? Is there room for even 2D functional formation AI, or does that push M7?
2. "Architecturally layer-aware" is not a free stub — what does it actually cost to build versus skipping it?
3. Nadia's layer-transition contract is the correct minimum viable decision. Can we scope that independently of full atmospheric follow?

The emergence chain argument is real. But "real" doesn't compress build time. What's already on M6's plate?


<!-- complete -->
