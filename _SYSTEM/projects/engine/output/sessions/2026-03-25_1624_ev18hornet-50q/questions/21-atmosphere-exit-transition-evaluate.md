### Soren (solo dev scope warden)

Three separable build items. Conflating them inflates the estimate.

**Asymmetric exit feel.** Correct call, low cost. Don't implement the symmetric beat. Hull-dependent climb rate comes for free if ship stats already exist. Bank angle cost is a flight model tuning variable. This is a day of polish work, not a feature.

**Positional re-emergence.** Correct design. Not free. This requires a coordinate transform: 3D atmospheric exit vector → 2D orbital shell position. That's a non-trivial mapping function, plus the galaxy layer needs to know *where* to spawn the player rather than at a fixed insertion point. Call it 3–5 days to do right, including edge cases (what if the player corkscrews out at an oblique angle — what's the canonical exit vector?). The exit vector must be a named value, not implicit in whatever direction the player happens to be flying at the moment the altitude threshold triggers.

**Nadia's diegetic sky markers.** This is the one I want the group to sit with before approving. "Sparse geometry in the sky showing orbital reference points" is an asset problem. How many markers? What silhouette reads correctly at speed in flat-poly at varying altitudes? This is novel art work — it doesn't inherit from any existing building type. Flat-poly advantage only applies if you're not inventing new geometry categories. Get a per-marker day estimate before this earns scope.

**The escort hold point issue Ren raised is the real blocker.** Entry vector ≠ exit vector means M6 layer-transition contract needs amendment before it ships. That's not deferred. That's a dependency.


<!-- complete -->
