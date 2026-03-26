### Ren (emergence systems theorist)

The death respawn question is carrying three separate decision problems that have different dependencies. Conflating them will produce a bad answer to all three.

**Problem one: what does "friendly" mean?** This is a standing-system read. We've already decided standing gates mission availability, equipment access, and raid spawns. If "friendly" for respawn purposes ignores standing, we've created a system that works in isolation from everything we've built. A player with Hostile standing toward Confederation shouldn't be able to respawn at a Confederation port as if nothing happened. The standing bands we defined — Engaged, Degraded, Hostile — should drive port accessibility, not a separate "friendly flag" we invent for death only.

**Problem two: what does "nearest" mean?** Geometric nearest on a flat map is trivially wrong — it ignores travel graph topology, contested system boundaries, and the faction geography that makes the galaxy feel real. Nearest *navigable* port using the same routing logic the ship uses while alive is the right frame. This is a read-path question, not a definition question.

**Problem three: destroyed ports.** This is actually the most interesting one. If settlement-tier regression can drop a Colony back to Outpost, can a port disappear? If yes, death respawn becomes a live read against current port state — not a static lookup. That interaction is worth naming before we close the definition.

My proposal: resolve "friendly" first by mapping it to existing standing bands. Then "nearest" falls out of routing logic. Destroyed ports we scope explicitly.

What's the current assumption about port ownership and standing interaction?

### Max (atmospheric flight advocate)

Ren's standing-band mapping for "friendly" is exactly right — don't invent a separate flag when we already have Engaged/Degraded/Hostile doing that work. Confederation port, Hostile standing: you don't land there alive, you don't wake up there dead.

The destroyed-ports question is where this gets interesting for me, and it's not just an edge case — it's the emotional peak of the whole arc.

Your settlement has a landing pad. That landing pad is a port. Raid damage can degrade it. If tier regression pulls your Colony back to Outpost, does the landing pad survive? Because if it doesn't, your *own home port* just dropped off the respawn candidate list. You wake up somewhere else, and your first flight is back toward a settlement you can see from altitude — damaged, regressed, smaller than you left it. That's the SimCopter payoff running in reverse. It should hurt. That moment earns scope.

So I'd push the destroyed-ports question past "named edge case" into "primary design surface." The respawn location isn't just a convenience decision — it's the opening frame of your next session. Where you spawn determines your first approach vector. Distant neutral port means a long transit. Your own landing pad means you're already in atmosphere on descent.

The feel question is: should death default to pulling you *toward* your settlement or *away* from it? I'd argue toward, conditional on pad state. Nearest navigable friendly port that gets you back in the air toward home is the right frame.

Ren's routing logic handles it — we just need pad state as an input.


<!-- complete -->
