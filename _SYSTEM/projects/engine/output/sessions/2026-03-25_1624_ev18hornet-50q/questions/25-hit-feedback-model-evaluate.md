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
