### Soren (solo dev scope warden)

**"Minimal FPS" is not a scope category. It's a wish.**

Let me put numbers on what the table has been calling minimal. Walking sim — movement, collision, interaction triggers, bar NPC proximity — is 3–5 weeks in Godot 4 with flat-poly assets. You get the bar, exploration, building placement. That's real.

The moment you add combat — even "minimal" — you've added: weapon model, projectile or raycast system, enemy AI state machine (idle/alert/attack/dead), hit feedback, death state, sound design for weapon fire, damage tuning, at least one balance pass. That's 10–16 weeks minimum, solo. Flat-poly helps with enemy art. It does not help with AI, hit detection, or balance.

So the actual decision is: walking sim (3–5 weeks) or FPS (10–16 weeks). There is no third option.

Given that framing, I'd resolve the open debate this way:

**Boarding: abstracted. Permanently.** Vera is right. The standing cost, hot-hull window, and port run are already the danger. Adding 10–16 weeks of FPS to make boarding feel "earned" when EV proved a stats check works is sunk cost before you've shipped a core loop.

**Raid defense: the one FPS justification.** It does work the abstraction can't — you're present, you chose to land, the building matters. But it gets one scope slot, not a system that expands.

**Bar and exploration: walking sim. Full investment here.**

Flag for the record: if boarding ever gets reopened as FPS, that's a milestone in its own right, not a feature added to an existing milestone.


<!-- complete -->
