# Transcript: Hit Feedback Model

*Generated: 2026-03-25 17:57*

## Round: PROPOSE

### Max (atmospheric flight advocate)

Okay, here's the thing that nobody's said yet: the hit feedback model for breach combat has to feel *wrong* in a specific way.

This isn't a shooter. The breach fight is the consequence of not being upstairs doing what the atmospheric layer is actually for. So the feedback model needs to communicate two things simultaneously — "you're taking damage" *and* "you shouldn't be here."

That's actually a design constraint that narrows the choices fast.

Screen shake: cheap, readable, but it makes the fight feel *good*. Juice is the enemy here. The moment screen shake starts rewarding the tactile loop, players will optimize for breach defense over airspace management. We've already decided that's the wrong lesson.

Directional indicator: this is the right instinct for a real shooter, but we're not building encounter design around breach combat. Complex directional feedback implies a game where positioning matters — which implies a game worth learning. We don't want that.

Sound cue: this is the strongest single element for our purpose. A sound design that reads as *desperate* and *wrong* — not satisfying, not punchy — keeps the emotional register where it needs to be.

My read: single-frame screen desaturation flash on hit, short disorienting audio (not satisfying impact sound — something closer to alarm), no directional indicator. Minimal. Reads as "the systems are failing" rather than "the combat is engaging."

The SimCopter payoff is up there at altitude. The feedback model down here should *remind* the player of that fact.

What's the counterargument for keeping it satisfying?

### Ren (emergence systems theorist)

Max is right on the direction. I want to push further on the *why*.

The feedback model is an information surface, not just a feel surface. Every hit you take dirtside should be communicating the current state of the system that failed — the airspace management chain. That's the emergence angle.

Screen shake as the *primary* feedback does one thing: it centers the player's attention on their body. Wrong frame. We want their attention on the settlement state they're standing inside. The building around them is the consequence they're living.

Here's what I'd add to Max's model: tie desaturation depth to settlement structural damage state. Full power, clean settlement — the flash is mild. Degraded power node — the desaturation is deeper, lingers longer. The visual feedback is now reading from the building damage model, not just the hit event. The fight literally looks worse as your settlement is worse. That's systems talking to each other.

The sound cue question is: does it feel like *your* failure or like external threat? Max's alarm framing is correct — alarm sound reads as "systems are failing" rather than "you are being attacked." That's the right attribution. But I'd key alarm intensity to patrol composition tier. Harassment raid breach sounds different from assault raid breach. Players learn what they walked into.

No directional indicator. That implies encounter design we haven't built and don't want to build. Converging vector pathfinding already communicates spatial pressure. The audio handles urgency. The desaturation handles weight.

The feedback model should make the building feel sick. Not the player.

## Round: CRITIQUE

### Vera (EV systems historian)

Both proposals are solving a real problem. But Ren's damage-state desaturation is scope creep wearing emergence clothing.

Here's what EV actually taught about consequence feedback: the consequence was already legible *before* you were in it. The faction bar told you. The patrol density told you. The comms intercept told you. By the time you're dirtside taking fire, the game has already said everything it needed to say. The breach isn't a new information surface — it's the bill arriving.

So I'd push back on Ren's desaturation-tied-to-damage-state: that requires the player, mid-breach, to be reading building damage state through visual feedback and updating their mental model of the settlement. That's not the emotional register of a failure state. That's encounter design. We explicitly rejected encounter design.

Max's single-frame desaturation flash plus alarm audio is correct. It's cheap, it's wrong-feeling, it doesn't reward the loop. The sound should be close to a klaxon — the kind of sound that means "evacuate," not "engage."

One addition I'd flag as worth considering: the sound cuts abruptly on breach repelled. Not a victory sting. Silence. EV's combat resolution was a galaxy map that just... returned to normal. You survived. The threat is gone. Nothing celebrates that. The absence of alarm is the reward.

Ren's patrol-composition-tier audio distinction is legitimate and cheap — harassment and assault should sound different before you even see the enemy count. That earns its build cost.

Directional indicator: no. Confirmed by both. Stay there.

### Nadia (new-player experience advocate)

Vera's framing clarifies the actual problem: the hit feedback model doesn't need to teach the lesson — the comms line at breach does that. The feedback model just needs to not contradict it.

That changes what I'd flag. Max and Vera are right that screen shake is the enemy here, but not primarily because it rewards the tactile loop for experienced players. It's that screen shake *centers the player in the fight*. A new player who gets breached, feels screen shake, and survives will conclude: "I can do this dirtside." The wrong lesson isn't "this combat is fun" — it's "this combat is survivable as a strategy."

The alarm-plus-desaturation model works precisely because it doesn't center the player. It centers the settlement. The building is alarming. The building is losing color. The player is incidental to that.

One thing I'd add that nobody's said: the desaturation should read as coming *from the walls*, not from the player's perspective. If it's a vignette effect — edges darkening, color draining inward — it reads as the player's health. If it's a flat color pass on the whole scene, it reads as the environment failing. The latter points players toward the thing that's actually at stake.

Ren's patrol-tier audio distinction earns its cost. Harassment sounds different from assault. New players who survive a harassment breach and later hear assault audio will know they're in worse trouble before they count enemies. That's legible without a tutorial.

Vera's silence-on-repelled is exactly right. Don't celebrate survival. The bar is upstairs.

## Round: EVALUATE

### Soren (solo dev scope warden)

The design direction is largely converged. Before this closes, I want to separate the cheap from the expensive so the milestone placement is honest.

**Free or near-free:**
- Single-frame flat desaturation pass. One shader uniform, one hit event. Half a day.
- Alarm audio, not impact audio. Asset selection, no new system. One to two days including tuning.
- Silence on repelled. Remove the win sting. That's negative work.

**Cheap with a dependency:**
- Patrol-tier audio distinction (harassment vs. assault). Requires raid composition tier to be readable at breach time. If that data is already flowing to the spawn system, this is a two-hour branch. If not, it's a read path addition. Estimate accordingly.

**Scope risk:**
Ren's damage-state desaturation depth — mild flash at full power, deep lingering at degraded node — requires the building damage model to be queryable at render time per hit event. That's not a shader change. That's a live state read from the settlement model into the visual system. That dependency doesn't exist in M7. Either the building damage model exposes that query by breach combat build time, or this feature doesn't ship with M7 combat.

Nadia's flat-pass-vs-vignette distinction is actually the correct scope question. Flat pass is one shader. Vignette that reads as player health is a different implementation with a different emotional register. Decide which before asset work begins.

**Recommendation:** Ship flat desaturation plus alarm audio. Defer damage-state depth modulation until building model exposes the read path.

<!-- complete -->
