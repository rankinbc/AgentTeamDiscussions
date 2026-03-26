### Soren (solo dev scope warden)

The cap mechanism debate is downstream of a question nobody has answered yet: **how many ships need functioning AI at each milestone?**

Fighter bays are the right architecture — Vera is correct, and it eliminates an abstraction layer. But whether the cap is "hull slots" or "command rating," every ship in your fleet needs pathfinding, formation behavior, target acquisition, and atmospheric layer handling. That cost is identical either way. The cap mechanism is two hours of design work. The AI for each fleet slot is weeks.

My scope flag: **fleet escort AI is a full feature, not a progression modifier.** A shuttle with one escort and a capital ship with eight escorts isn't a scaling multiplier. It's eight separately-validated AI agents that must hold formation in 2D space, execute the atmosphere dive, navigate flat-poly terrain, and re-emerge. Each capability is a milestone-sized task the first time you build it.

The captured-ship-as-standing-trigger is genuinely good emergence design. It's also a second feature hiding inside what looks like a fleet question. The port run, the faction provenance signal, the standing event — that's a session of work minimum, and it requires the faction standing API from M5 to exist first.

My recommendation for this discussion: **separate the mechanism decision from the fleet AI scope decision.** Fighter bays — fine, decide that now. Then answer: at which milestone does the *first* escort ship have working AI? That answer will tell you whether fleet is M6 content or M8 content. The mechanism doesn't matter if you don't know when you can afford to build it.


<!-- complete -->
