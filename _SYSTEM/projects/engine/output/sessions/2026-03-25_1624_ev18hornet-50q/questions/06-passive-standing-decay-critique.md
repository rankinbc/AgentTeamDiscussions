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


<!-- complete -->
