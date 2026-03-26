### Soren (solo dev scope warden)

Scope read before the question moves.

Hull-as-independent-trigger is a new data model, a new query path in patrol AI, and a new player-facing feedback surface — none of which exist. Standing-only uses `mutate_standing`, which is already built. That's not a minor implementation difference. That's the difference between a 2-day close and a 2-week build that touches ship state, patrol AI, and UI.

Ren's framing is cinematically correct. It's also describing infrastructure for the bribe path and salvage path, both of which are explicitly deferred. Building hull provenance persistence now to support mechanics that have no earn date is premature — it's architecture in service of a wishlist.

Vera's legibility argument holds for a second reason: patrol AI currently has no authored read path for ship-level flags. Teaching patrol AI to distinguish "standing hostile" from "hull-recognition hostile" is a separate system from the standing system. You're not extending what exists — you're building something new and connecting it.

Nadia's reframe is the right one. The fantasy Max is describing — *this ship feels dangerous to fly* — is a feedback problem. It doesn't require a second hostility axis. It requires a comms intercept, an early patrol vector, something that surfaces the standing consequence *in the cockpit* rather than leaving it as a port-screen number.

Recommend: standing-only trigger for M5. The atmospheric tell Nadia describes is the correct M5 surface — one new string, one patrol behavior tweak, no new data model.

What does the room think the atmospheric tell should look like?


<!-- complete -->
