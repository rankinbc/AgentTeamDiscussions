### Soren (solo dev scope warden)

The altitude range is a config constant. The systems that run at each altitude band are the build cost. The group is solving the wrong problem first.

Vera and Nadia are right on sequencing. But I want to add the build-cost framing they're missing.

Here's what actually costs time in the atmospheric column:

**Entry altitude:** one float. Costs nothing. Change it twelve times after playtest.

**Floor altitude:** same. One float.

**What costs time is the systems you wire to each band.** Patrol spawn logic at intercept altitude — that's a build item. Convergent approach vectors keyed to faction standing — build item. LOD transitions as altitude changes — build item depending on terrain complexity.

Vera's question ("what does the column need to prove at first ship?") is the scope sequencing question. My answer: **one thing.** At Hornet Layer, the column needs to prove the flight model is fun between two altitude bounds. That's it. No faction pressure. No standing reads. No three feel-states. Those come after you know the flight model earns its keep.

The one constraint I'll second from Nadia: **deck below roofline is a day-one build requirement**, not because of feel-states but because building height determines your terrain geometry, your collision surfaces, and your low-pass camera behavior. You cannot retrospectively lower the floor without touching those systems. That number needs to exist before the first building mesh is authored.

Everything else: config constants, sized after the Hornet Layer milestone plays.

Name the deck. Defer the rest.


<!-- complete -->
