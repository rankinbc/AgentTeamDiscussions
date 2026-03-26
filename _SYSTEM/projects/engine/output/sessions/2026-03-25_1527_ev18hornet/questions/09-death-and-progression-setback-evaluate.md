### Soren (solo dev scope warden)

[PROPOSE — Soren (scope estimator)]

Before death mechanics: the moderator directive reverses fourteen decided bullets on the space layer. 3D space is not a tweak — it's a different renderer, a different camera system, a different targeting model, and a different readability problem than the 2D plane we scoped. Every estimate downstream of that decision was built on 2D. I'm noting it as a scope event that requires its own accounting before it propagates silently into milestone estimates.

On death mechanics, the question is not what feels right — it's what each option actually costs to build correctly.

**Option A** costs almost nothing to implement and teaches the player nothing. It's technically the cheapest. It's also a design hole.

**Option B** is the right scope choice. Ship loss is already a meaningful consequence because replacement cost is baked into the economy you're building anyway. You're not adding a new system — you're letting an existing system do its job. Implementation cost: starter ship spawn logic, dock state reset. Already required for other flows.

**Option C** adds a credit-drain system on top of ship loss. That's a second consequence requiring its own UI, its own legibility work, its own edge-case handling. Nadia is right that it's noise on the correct signal. More importantly, it's scope you don't need.

**Ren's world-state propagation** is correct in principle and already partially designed — the deterrence calculation reads hull count, not session status. Death is just hull count going to zero. That's not new code. That's the existing system triggering.

Option B. Build the thing you already need.


<!-- complete -->
