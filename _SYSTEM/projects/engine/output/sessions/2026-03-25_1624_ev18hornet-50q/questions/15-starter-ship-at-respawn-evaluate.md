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
