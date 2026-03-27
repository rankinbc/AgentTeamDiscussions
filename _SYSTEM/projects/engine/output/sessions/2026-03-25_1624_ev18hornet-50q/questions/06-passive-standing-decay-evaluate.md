### Soren (solo dev scope warden)

**Build cost audit, then a position.**

Event-only standing as currently architected: `mutate_standing(player, faction, delta)` called at discrete events. The system exists. The signal surface (tooltip at 40) exists. Build cost for M5: near-zero marginal work.

Passive decay — any model — requires at minimum:

- A decay tick or offer-refusal counter running persistently per player per faction
- Logic distinguishing "player declined" from "player wasn't present" from "player hasn't reached the Bar yet"
- A notification surface so decay isn't invisible (Nadia's failure mode is real and the solution costs build time)
- A `DECAY_FLOOR` constant that has no defensible value until standing movement rates are playtested

That's a new subsystem. Call it 2–4 weeks of focused solo dev time to implement correctly, including the legibility surface. More if the edge cases bite.

**Position:** Event-only for M5. Not because of EV faithfulness. Because the problem passive decay is meant to solve — "airspace feels like a diorama" — is an M8 problem (patrol density, atmospheric texture). Solving an M8 problem with an M5 faction system addition is premature coupling and it costs build time on a system whose parameters can't be tuned until you've played the event-only version enough to know what rates feel like.

Ren's refusal-tracking model is the least wrong decay design if decay ships. But "least wrong" is not a M5 argument.

The specific M5 failure mode that requires decay has not been named. Until it is, the complexity is not justified.


<!-- complete -->
