### Soren (solo dev scope warden)

**Soren:**

The design logic from all four is sound. My job is to tell you what it costs to build.

Good news first: Max's "visible gap" framing is the flat-poly advantage in full effect. Destruction in this aesthetic isn't a destroyed mesh — it's *absence*. You remove the geometry. The scar is the absence. That's cheaper than any other art style on the planet. Don't let anyone frame visual destruction as a scope concern here. It isn't.

The scope concern is **state persistence**.

Targeted destruction means every building has an exists/destroyed state per settlement, and that state has to survive session boundaries, co-op sync, raid resolution during atmospheric absence, and the recovery rebuild flow. That's not a rendering problem — it's a data model problem. How many buildings per settlement at Colony tier? Multiply by the number of active settlements. Multiply by co-op edge cases where one player is in space and the other is on foot when a raid resolves. That's the actual work.

The recovery path question Vera raised is also an implementation question. Standing-as-primary-currency requires the faction system to gate rebuild actions — not just flavor the experience. That's a dependency chain. The faction system has to be *queryable* by the settlement rebuild flow before that works.

My recommendation: **yes to permanent destruction, yes to tier regression, but define the minimum building vocabulary first.** How many distinct building types exist at each tier? That number drives every other estimate. Without it, "settlements you fight to protect" is a vision statement, not a scope.

What's the building type count at Outpost tier?


<!-- complete -->
