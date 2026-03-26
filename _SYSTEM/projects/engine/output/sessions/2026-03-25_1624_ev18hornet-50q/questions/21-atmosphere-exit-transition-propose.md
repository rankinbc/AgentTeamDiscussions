### Max (atmospheric flight advocate)

The exit transition question is doing more work than it looks like. Let me name the two things it's actually asking and why they matter differently.

**Exit feel** is a flight model question. Entry is gravity-assisted — you're committing, the view transforms, altitude matters. Exit is the opposite: you're climbing out under power, burning to escape. Symmetric *cinematic treatment* would be a mistake. Same duration, same beat, same camera — that reads as a loading screen, not flight. The exit should feel like work. Bank angle costs. Climb rate varies by hull. Heavy Freighter punching out feels different from a Light Fighter. That's atmospheric layer identity, not polish.

**Re-emergence position** is where I want everyone paying attention, because it's the question that decides whether atmosphere is a primary space or a tactical corridor.

If re-emergence maps to your atmospheric exit vector — you punch out heading 030° at 15km altitude, you emerge at the corresponding orbital point — then atmosphere dives become genuine navigation choices. Evasion through atmosphere requires you to actually *fly* your way to a useful exit vector. That's Hornet Layer depth. That's the SimCopter payoff earning its keep.

If re-emergence is always at the same orbital insertion point regardless of atmospheric exit vector, then atmosphere becomes a panic button. Players learn "dive atmosphere, come back safe." That's a corridor.

My position: re-emergence should track atmospheric exit position and heading. The tactical evasion question answers itself — yes, atmosphere dives work as evasion, but only if you can *fly* to a useful exit vector first.

What are the dependencies against making re-emergence positional?

### Ren (emergence systems theorist)

Max's positional re-emergence argument is correct, and I want to name exactly why it matters for layer integration rather than just tactical depth.

Re-emergence position is the mechanism that makes atmosphere a navigation space rather than a loading zone. Without it, the three layers don't interact — they sequence. The faction standing → raid spawn → atmospheric defense chain I care about requires that *where* you exit atmosphere has consequences in space. If exit vector maps to orbital emergence point, then a player who dove atmosphere to break a pursuit now has to ask: where am I coming out, and who's waiting?

That question is not authored. The raid AI didn't script that ambush. The player's choice of exit vector, combined with patrol spawn logic reading faction standing, produces the situation. That's the emergence chain working.

On the escort hold: this is where I'd push back on an assumption baked into the prior discussions. We've specified escorts hold at atmospheric entry altitude. If re-emergence is positional, the entry vector and exit vector are potentially *different points on the orbital shell*. An escort holding at your entry point is not covering your exit point unless you exit where you entered. That's a correct design consequence — a straight plunge and return is safe, a lateral atmospheric transit that exits on a different bearing leaves you unescorted at emergence. That asymmetry is emergent and interesting.

Flag: we need to confirm patrol spawn points aren't anchored to a single orbital insertion point before the exit vector design ships. If they are, positional re-emergence loses its teeth.


<!-- complete -->
