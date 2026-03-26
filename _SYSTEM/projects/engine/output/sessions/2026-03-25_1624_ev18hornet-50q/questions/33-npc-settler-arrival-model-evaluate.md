### Soren (solo dev scope warden)

Four options are on the table. I want to put build costs next to each before anyone anchors.

**Population counter only.** One integer field, one threshold check. Faction attention scales with it. No aerial legibility. Build cost: one day. EV ran on this model and produced deep play.

**Visible settler agents.** Flat-poly character meshes, patrol paths inside settlement geometry, some form of idle/movement state, collision with buildings. Raid interaction TBD — can they be killed? Do they flee? If yes, that's a health model, a flee state, and a new read path for assault AI that Q12 explicitly deferred. Build cost: **4–8 weeks minimum** for a functional NPC agent system in a new layer. This is a separate game feature, not a settlement extension.

**Geometry change at threshold.** A new structure appears — trade post, antenna, communal structure — when population crosses the unlock value. Flat-poly mesh, authored once, placed at settlement time. Reads from altitude. No pathfinding. Doesn't reopen Q12. Build cost: 2–4 days per new building type, which is already in the per-type authoring budget.

**Explicit placement.** Player places personnel slots as buildings. Population is building count. No separate counter, no new system. Arrival is a player action. Build cost: folds into existing building placement.

The geometry change option does what Nadia described — legible threshold signal from altitude, no agents, no Q12 regression risk.

**Decision-forcing question:** Does the SimCopter payoff require *movement*, or does it require *evidence of change*? Answer that and the scope follows directly.


<!-- complete -->
