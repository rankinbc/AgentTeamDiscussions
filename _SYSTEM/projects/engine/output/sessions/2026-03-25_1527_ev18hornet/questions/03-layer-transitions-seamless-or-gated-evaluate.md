### Soren (solo dev scope warden)

Everyone at this table is debating the *feel* of the transition. Nobody has priced it.

**Seamless — continuous flight, no cut** — means both layers are simultaneously resident in memory or you've built a streaming architecture. In Godot 4, that's a real engineering problem: terrain mesh, NPC state, settlement objects, atmospheric physics, *and* the 2D space layer with its faction contacts and nav map. You're not writing a shader. You're writing a world-state manager that keeps two distinct simulation modes coherent across a boundary. That's a milestone by itself.

**Gated** — irrevocable commit, brief transition, emerge in atmosphere — costs a cutscene and a scene swap. Two weeks, maybe three. It works on day one.

Max's cinematic beat is not seamless. It's a gated transition with a 3-second camera sequence bolted to the front. That's the right scope call and he's describing it correctly. The player experience of "seamless" is achievable without the engineering bill of actual seamless. The distinction matters.

Ren's symmetry argument is architecturally sound and I'm not disputing it — but "faction ships follow the same transition logic" in a gated model means queuing their scene entry on the same timer. That's manageable. In a true seamless model, it means their position and state must be valid in both coordinate spaces simultaneously. Different problem.

**The agenda I'm setting:** decide whether "seamless" means *feels seamless* or *is technically seamless*. One of those is in scope for a solo dev. The other is not.


<!-- complete -->
