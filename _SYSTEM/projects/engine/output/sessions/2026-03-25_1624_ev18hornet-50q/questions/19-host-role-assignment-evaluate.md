### Soren (solo dev scope warden)

**Host role:** Network topology, session-negotiable, no standing implications. That's decided. Four speakers said the same thing; I won't add a fifth.

The scope question this round is Nadia's claim: the attribution surface "can't wait until M8 if co-op ships in M8." That's a dependency inversion worth stress-testing before it becomes a scope addition.

Two distinct implementation paths are hiding inside "P2 needs to understand why the airspace is hostile":

**Path A — Content change.** The existing comms intercept string from Q10 gets authored differently for co-op sessions. Same emission surface, same trigger, different wording that includes a partner-reference. This is a content design problem, not a code problem. Build cost: one conditional branch on session type in the string formatter, authoring time for co-op variants. Estimate: 1 day code, content out of scope.

**Path B — New read surface.** The system compares P1 and P2 standing at comms intercept time, determines who drove `max()`, and names that player in the string. This requires real-time cross-player standing comparison at atmospheric entry, a new data path, and UI surface. Estimate: 3–5 days minimum, with co-op session state dependencies that don't exist in M7.

Before attributing M7 scope to this, the question needs an answer: is this Path A or Path B? If it's Path A, it's cheap and should ship with co-op. If it's Path B, it competes with everything else already queued.

Name the path. Then estimate. Then decide whether it fits M7 or M8.


<!-- complete -->
