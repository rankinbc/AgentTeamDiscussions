# Transcript: Passive Standing Decay

*Generated: 2026-03-25 16:42*

## Round: PROPOSE

### Max (atmospheric flight advocate)

Passive decay is an atmospheric layer question dressed in faction clothing, and I want to name that before we start arguing numbers.

Here's the design truth: the payoff moment — banking over your settlement at altitude, watching your City tier layout from 800m — only *hits* if the airspace has texture. Patrol density is M8, yes. But the *precondition* for patrol density meaning anything is that standing moves without you. If standing only shifts on explicit events, the sky above your settlement is static until you poke it. That's a screensaver. That's not SimCopter, that's a diorama.

Passive decay is the engine that makes airspace *alive*.

But here's my flag before anyone proposes a simple timer: **decay should feel like neglect, not taxation.** The experience design question is — does the player feel *drifting away* from a faction, or does it feel like the game is taking something? Those are completely different feelings. Drifting is atmospheric (literally). Taxation is administrative.

So my agenda for this round is two questions:

1. **Is decay continuous (time-ticker) or event-paced (mission-drought)?** A mission-drought model — standing starts dropping after N days with no faction contact — maps to the atmospheric loop naturally. You've been out of the sky, the faction forgot you exist.

2. **Does decay have a floor above the Hostile threshold?** Passive decay should never cascade you into Hostile. That band requires authored intent, not a clock.

Set those two, and we have something buildable.

### Ren (emergence systems theorist)

Max has correctly identified the design question but I want to push on the *systems interaction* implication before we answer it.

Standing decay is only interesting if it **feeds the raid chain**. Decay → Degraded → increased raid probability → atmospheric intercept → on-foot aftermath. If decay is just a number-reduction mechanic that sits in the faction layer and doesn't pull on anything else, it's administrative regardless of how it *feels*. The texture question Max is asking about is real, but the answer has to come from system coupling, not from choosing the right decay curve.

**On the event-paced vs. timer question:** Mission-drought is correct, but the trigger shouldn't be calendar days — it should be *mission opportunities declined or ignored*. The faction offered contact through the Bar and the player didn't take it. That maps naturally to the existing Bar interaction model and doesn't introduce a new time-tracking surface. The system already knows when missions were offered. Neglect is measured in refusals, not seconds.

**On the Hostile floor:** Fully agree. Passive decay must have a hard floor above the Hostile threshold — call it `DECAY_FLOOR`, a named config constant, set above `HOSTILE_THRESHOLD`. Decay can erode you to Degraded. Getting to Hostile requires an explicit negative action. Those are different player choices and should produce different system states.

This also means decay *rate* and `DECAY_FLOOR` are the two new config constants. Both require playtest data. Both deferred in value, decided in architecture.

## Round: CRITIQUE

### Vera (EV systems historian)

**EV didn't have passive decay. That's the data point this discussion is skating past.**

In EV Nova, your standing with the Confederation at 200 hours was the same standing you earned at hour 20 unless you *did something*. That permanence was load-bearing. It meant every positive action was an investment that held. Players planned around it. The faction system felt like a *ledger*, not a leaking bucket.

So before we architect decay, I want the room to answer: **what problem are we actually solving?**

Max says static airspace feels like a diorama. That's an atmospheric layer observation, not a faction standing observation. Patrol density is M8. The "airspace has no texture" problem is an M8 problem. Routing its solution through standing decay in M5 is coupling two systems prematurely — and it means we're designing the decay curve before we have any playtest data on what standing movement rates actually look like.

Ren's refusal-tracking model is the more honest framing, but it introduces a new data surface EV never needed. The Bar already knows what was offered. That's true. But "missions declined" as a decay trigger means the system now has to distinguish *declined* from *not-yet-seen* from *offered-while-player-was-elsewhere*. That's not simple.

My position: **event-only standing is the EV-faithful baseline.** Passive decay is a scope addition that requires a demonstrated gameplay problem before it earns the complexity. What's the specific failure mode of event-only standing that makes this necessary in M5?

### Nadia (new-player experience advocate)

Vera is asking the right question and I want to amplify it from the player side: **invisible standing loss is the worst possible first-session experience.**

Here's the new-player failure mode I'm flagging: someone spends their first three sessions building a Claim Stake, does a couple of trade runs, walks into the Bar excited — and the faction contact is cold. They don't know why. Standing dropped while they were building. There was no event they recognized as a choice. The system punished them before they understood what they were doing wrong.

That's not faction tension. That's confusion followed by friction followed by "I think this game is broken."

Ren's refusal-tracking model is *more* legible than a timer, but it still has the attribution problem Vera named: "offered-while-player-was-elsewhere" is a real edge case that produces the same silent punishment. New players don't have a mental model of mission offer windows.

My position: **event-only standing is correct for M5**, and the reason is legibility, not EV faithfulness. Every standing movement should be traceable to a player action they understood as a choice at the time they made it. The tooltip system we've already decided gives us the feedback surface. Decay without a clear signal uses that surface for nothing.

If the "diorama airspace" problem is real — and Max's instinct might be right — the answer is atmospheric layer work in M8, not coupling faction standing to a clock the player can't see.

What specific M5 failure mode requires decay to be present *now*?

## Round: EVALUATE

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
