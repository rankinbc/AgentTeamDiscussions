### Soren (solo dev scope warden)

The atmospheric argument is good. The build argument settles it.

Vera named the cost correctly but didn't size it. Let me size it.

**Option Close:** Registration fires the delta. Hull dies. Nothing else happens to standing. The account is already closed. Zero additional code at the death/respawn path. This is the state the system is already in if registration is implemented correctly.

**Option Escalate:** You need hull-origin standing to persist as a *pending second delta* from registration through active flight through death through the respawn flow. That's a state field on the player record that travels with the hull, survives the hull's destruction, and fires at respawn. It interacts with the respawn screen (which already has three jobs). It interacts with every edge case in the death flow — what if the hull is destroyed by a friendly? What if the player logs out mid-flight? What if the hull is recaptured before death? Each of those is a case branch. On a solo build, case branches at the respawn path are how you lose a week in M5 and discover the bug in M7.

The atmospheric pressure Max wants is real and worth having. The authoring surface for it is the registration delta magnitude — a config constant that already has to exist. Tuning a number is an afternoon. Building a persistent death-trigger delta with survival semantics through the respawn flow is not.

**My recommendation:** Decide closed at registration now, carry a named open question for registration delta calibration post-M5 playtest. Don't architect escalation before we know if registration magnitude is insufficient.


<!-- complete -->
