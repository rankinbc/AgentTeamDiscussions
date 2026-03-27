# Transcript: Starter Ship at Respawn

*Generated: 2026-03-25 17:16*

## Round: PROPOSE

### Ren (emergence systems theorist)

The respawn ship model is a leverage point that touches three separate systems simultaneously, and those interactions need to map before we can evaluate any single option.

**Interaction 1: Ship acquisition vs. boarding economics.** If respawn ships are free, the boarding mechanic becomes a dominant strategy with no downside. Players board, capture, die intentionally if they want the starter back — the capture path loses its weight. If respawn requires purchase, boarding becomes a genuine risk calculation. The ship progression system (Shuttle → Capital) only generates meaningful decisions if losing a ship registers as a real consequence.

**Interaction 2: Credit floor vs. the recovery arc.** We already decided tier regression uses a reduced rebuild cost. If the credit floor is too generous, players recover trivially — raid consequences shrink. If it's too stingy and ship purchase is mandatory, a bad raid sequence plus a ship loss creates a compounding spiral that can lock players out entirely. The credit floor is actually a recovery *rate* control on the entire economic system.

**Interaction 3: Death location vs. respawn ship tier.** The last-docked anchor is decided. But what ship you respawn with interacts with *where* you wake up. Respawning in hostile space with a Shuttle when you died flying a Heavy Fighter means the tactical situation at respawn is authored by the ship grant, not the player's state.

My agenda: we should decide these in order — ship grant model first, then credit floor, then handle the tier-mismatch edge case. What's the group's instinct on whether losing a ship should feel like a setback or a reset?

### Max (atmospheric flight advocate)

Ren mapped the economic interactions cleanly. I want to pull one thread harder: the respawn ship determines the *quality of the atmospheric return flight*, and that flight is the SimCopter payoff moment.

You died. Your last-docked anchor is your settlement pad. You wake up in-atmosphere with a view of what the raid did. That approach is the emotional core of the whole settlement system — it needs to land. A Shuttle has floaty, slow roll response. A Heavy Fighter has the bank-and-yaw authority that makes a low pass over your damaged colony *feel* like something. If you earned a Heavy Fighter and respawn in a Shuttle, the approach to your own burning outpost is aesthetically diminished. The camera doesn't move right.

So here's my position: **free Shuttle reset is wrong, not primarily for economic reasons but for feel reasons.** The respawn ship should be your last owned hull, or a loaner at the nearest tier below it. Insurance framing works — you paid into it, you get your heavy back, minus some credits. The flight home is in *your ship*, with your bank angles.

The credit floor question is secondary but connected. Floor should be generous enough that you're never locked out of flying back to your settlement at altitude in something that handles. Doesn't have to be your best ship — but it shouldn't be the starting bus.

Ren's tier-mismatch edge case is real. Hostile respawn location in a Shuttle is a punish spiral. But if last-docked anchor is your own pad, you're already home. The ship tier question mostly bites when you're far from your settlement — which is exactly when the flight back matters most.

## Round: CRITIQUE

### Nadia (new-player experience advocate)

I want to bring this back to the moment of first death, because that's where this decision actually lives.

A new player dies before they understand the faction standing system. Before they know what the Degraded band means. Possibly before they've ever successfully docked somewhere other than the starting port. The respawn model is their first lesson about what kind of game this is — does it punish, or does it set you back up?

Max's instinct is right that the flight home matters, but I'd push further: **the first death needs to feel legible, not just survivable.** Free Shuttle reset is legible — "you lost your ship, you're back at the beginning." But it also signals that ships are disposable, which undercuts everything the boarding capture path is trying to build.

My read: **loaner against future earnings is the right framing**, but it has to be surfaced immediately and clearly. Not in a tooltip buried behind two menus — at the moment of respawn, the player needs to see: *you're in a loaner, you owe X credits, your previous hull is gone.* That's a feeling of consequence with a recovery path attached.

The credit floor question is actually asking: what's the *minimum viable ability to act*? I'd define it not as a number but as a capability: the floor should always guarantee enough credits to fly to the nearest Bar and pick up one mission. That's the recovery action. Anything below that is a locked state, and locked states in the first session kill games.

### Vera (EV systems historian)

EV didn't do loaners. Worth stating plainly before this discussion drifts further into mechanics EV never attempted.

In EV and EV Nova, death cost you your ship and cargo. You respawned at the nearest inhabited system — the game didn't try to be clever about it — with a Shuttle and enough credits to act. EV Nova added optional, purchasable ship insurance. That's the full design space the source material actually explored.

The "loaner against future earnings" framing invents a debt mechanic that EV never needed. I'm skeptical on two grounds: **legibility and scope.** Debt requires UI, debt requires tracking, debt interacts with every credit-earning surface. Nadia is right that the first death has to be immediately legible — but debt is *not* more legible than "your ship is gone, here's a Shuttle." It's less legible, and it adds a recovery arc that has to be taught on top of an already-complex system moment.

The EV insight that's being partially missed: **consequence in EV came from cargo loss and mission failure, not primarily from hull loss.** Hull was resettable. The *stuff you were carrying* was what hurt. The boarding mechanic's weight came from the risk of losing the captured hull's cargo and your own investment in the run.

Nadia's credit floor framing — enough to reach a Bar and take one mission — is exactly correct and maps directly to EV's design intent. That's the floor. Not "enough to feel good about your bank angle on approach." Enough to re-enter the economy.

Free Shuttle. Mission-access credit floor. Insurance is an earnable upgrade, not a default.

## Round: EVALUATE

### Soren (solo dev scope warden)

Vera named the scope trap correctly. I want to put numbers on it so the group has something to push against.

**Loaner against future earnings** is not a design decision, it's three implementation problems wearing a coat:

1. A debt state on the player record
2. A repayment trigger on every credit-earning event
3. A UI surface that reads and communicates that debt at respawn, at the Bar, and at the moment of payoff

That's a week of build time, conservatively, before you've written a single line of dialogue. It also touches the mission reward path, the trade path, and any other credit source. Debt systems metastasize — every new credit-earning feature you add in M7 or M8 has to be debt-aware.

**Free Shuttle with a credit floor** is a constant and a starting value. One config constant (`RESPAWN_SHUTTLE_CREDIT_FLOOR`), set to whatever guarantees Bar access. That's an afternoon.

**Purchasable insurance** — EV Nova's actual answer — earns scope when the economy is mature enough to price it. Not before.

The flight-feel argument is real but misapplied. Max is right that the approach flight matters. The answer is not to change the respawn ship — it's to make the Shuttle fly well enough that the approach lands emotionally. That's a flight-model tuning problem in the atmospheric layer, which is already in scope.

My agenda: decide the Shuttle grant model and the credit floor definition today. Defer insurance to a later milestone when you have playtest data on how often death happens and how much it stings.

<!-- complete -->
