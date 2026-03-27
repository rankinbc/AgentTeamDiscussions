### Soren (solo dev scope warden)

Before the group debates trigger conditions, there's a prior question that actually gates the build cost estimate: **where does the building action live in the UI?**

Option A, B, and C are trigger conditions. None of them cost much to implement as triggers. A boolean check on session start, a flag set on landing, a mission completion state — these are all cheap. The trigger is not where the build time lives.

The build time lives in the **placement interface itself**. Two distinct implementations are on the table and nobody has named them:

**Path 1 — Landing port menu item.** Player lands, port interface appears, Claim Stake is a selectable option. Dirtside. Approximately same complexity as buying cargo. Low build cost.

**Path 2 — In-world placement tool.** Player designates a site via 3D interaction — either from the air or on foot. Requires: placement preview mesh, terrain validity check, confirmation state, anchor write. Non-trivial. Estimate 1–2 weeks solo to do it without bugs.

Nadia's "designation from air while experiencing vertical relationship" and Max's altitude hold both assume Path 2 exists. If Path 2 isn't built, those suggestions are scope additions, not trigger options.

One more flag: Vera's EV framing is correct — landing port menu is the EV-native pattern. It's also the cheapest one. If the group is tempted toward aerial designation because it *feels* more elegant, that feeling costs 1–2 weeks.

Confirm the interface path before the trigger debate. Everything downstream depends on it.


<!-- complete -->
