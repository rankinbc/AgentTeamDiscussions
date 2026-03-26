# Transcript: Atmosphere Exit Transition

*Generated: 2026-03-25 17:40*

## Round: PROPOSE

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

## Round: CRITIQUE

### Vera (EV systems historian)

The positional re-emergence argument has a problem that neither Max nor Ren have named yet: legibility.

EV's spatial design worked because consequences were readable before you committed. You could see the jump point. You knew where you'd arrive. The overhead view made orbital relationships legible at a glance — who's where, how far, which vector matters. That readability was load-bearing. Remove it and the "traceable consequence" contract breaks, even if the underlying system is technically sound.

Positional re-emergence requires the player to reason about 3D atmospheric exit heading and translate it into 2D orbital position — in real-time, under pressure, during a dive. That translation is not obvious. A player banking at 030° in atmosphere needs to know what that maps to on the galaxy layer orbital shell *before* they commit to the maneuver. If they can't, the evasion isn't tactical depth. It's chaos with emergent aesthetics.

EV's faction consequence worked because every delta traced to a visible choice. The standing number moved, you saw why. If atmospheric exit vector produces orbital emergence position the player couldn't predict, the raid-at-emergence situation Ren describes isn't "the player chose a bad exit vector." It's "the player got surprised by a system they couldn't read."

Before this group commits to positional re-emergence, I want one answer: what is the in-flight legibility surface for exit vector → orbital emergence mapping? If that surface isn't specified before the exit mechanic ships, you've built tactically interesting emergence by EV standards, but tactically illegible by EV standards.

Name the display surface first.

### Nadia (new-player experience advocate)

Vera named the right problem, but I want to sharpen where it bites hardest: **not for experienced players, for first-session players who don't know what they're reasoning about yet.**

The exit vector → orbital position translation assumes the player has already built a mental model of the orbital shell. That model takes time to form. In the first 10 minutes of atmosphere, players are learning bank angles, managing altitude, reading the flat-poly terrain. They are not simultaneously constructing a 3D-to-2D coordinate mapping.

Positional re-emergence is correct design — I'm not arguing against it. But it has a **temporal dependency**: it only works as tactical depth once the player can predict it. Before that threshold, it's just surprising death.

The solution isn't to make re-emergence non-positional. It's to make the orbital shell *visible from inside atmosphere* during exit climb. Not a UI overlay. Something diegetic — the flat-poly sky shows orbital reference markers, sparse geometry that communicates "you're climbing toward *here*." The player learns the mapping by flying it, not by reading a tooltip.

That also solves Vera's legibility surface question: the display is the sky itself during exit. You see your emergence point before you commit to the climb angle.

One concrete ask before this ships: **the first atmospheric exit must be tutorialized** — not scripted, but the HUD or a single comms line needs to confirm "you emerged at [bearing]" so players can close the loop between choice and consequence. Without that, the first three dives feel random even if they aren't.

## Round: EVALUATE

### Soren (solo dev scope warden)

Three separable build items. Conflating them inflates the estimate.

**Asymmetric exit feel.** Correct call, low cost. Don't implement the symmetric beat. Hull-dependent climb rate comes for free if ship stats already exist. Bank angle cost is a flight model tuning variable. This is a day of polish work, not a feature.

**Positional re-emergence.** Correct design. Not free. This requires a coordinate transform: 3D atmospheric exit vector → 2D orbital shell position. That's a non-trivial mapping function, plus the galaxy layer needs to know *where* to spawn the player rather than at a fixed insertion point. Call it 3–5 days to do right, including edge cases (what if the player corkscrews out at an oblique angle — what's the canonical exit vector?). The exit vector must be a named value, not implicit in whatever direction the player happens to be flying at the moment the altitude threshold triggers.

**Nadia's diegetic sky markers.** This is the one I want the group to sit with before approving. "Sparse geometry in the sky showing orbital reference points" is an asset problem. How many markers? What silhouette reads correctly at speed in flat-poly at varying altitudes? This is novel art work — it doesn't inherit from any existing building type. Flat-poly advantage only applies if you're not inventing new geometry categories. Get a per-marker day estimate before this earns scope.

**The escort hold point issue Ren raised is the real blocker.** Entry vector ≠ exit vector means M6 layer-transition contract needs amendment before it ships. That's not deferred. That's a dependency.

<!-- complete -->
