### Ren (emergence systems theorist)

The framing of this question contains a structural assumption worth surfacing before we answer it: it implies some shared events collapse to a single standing read, and that host designation would govern whose standing that is. That's the real question.

The existing architecture already has an answer for the offline case: `max()` across both players' standing values drives raid composition. No host dependency — worst standing wins. That's the right pattern for emergence. If host standing were privileged, players would route session setup so the lower-standing player avoids hosting. That's not emergent play, it's a standing-evasion exploit that caps faction pressure accumulation artificially.

For the online case, the same logic applies. Every shared event that fires in-session — patrol intercepts during atmospheric flight, raid spawns while both players are on the ground — must query both players' standing independently. The faction system shouldn't know or care who is hosting. Patrol pressure reads P1 and P2. It responds to the more hostile read.

The host role is a network topology concern, not a standing architecture concern. Conflating them creates a privileged player in every faction consequence calculation, which is exactly the "combined/averaged settlement alignment" pattern we already rejected in Q3.

What I want to explore this round:

1. Whether any currently-designed shared event actually requires a single-player standing read to resolve — or whether all of them can cleanly take two reads
2. Whether the `max()` pattern is the right operator for online shared events, or whether some events should use `min()` — escort hire availability, for instance, where the more hostile player's standing might gate the mission

### Max (atmospheric flight advocate)

Ren's core point is correct and I'll reinforce it from the atmospheric layer specifically: patrol intercept geometry is the kinesthetic readout of standing. If host standing were privileged, the non-host player in atmosphere would feel a completely different pressure curve than their standing warrants. That's broken feedback — the flight tells you something false about where you stand.

The `max()` operator for raid spawns and patrol density is exactly right. In practice it means the more hostile player's standing "contaminates" the airspace for both, which is honestly *correct emergence* — if P1 has been raiding Confederation shipments while P2 ran trade routes, the sky above their shared settlement should feel like P1's choices. That's the SimCopter payoff: you fly over what you built, and the airspace *reads* like the game you played.

On Ren's `min()` question for escort hire: I'd push back on making it min(). Escort hire is a Bar interaction, single-player, dirtside. The question is simpler — which player is doing the hiring? That player's standing gates it. No aggregation needed. The atmospheric complexity comes *later* when the escort holds at entry altitude and a raid spawns during the hold. Whose standing triggers that raid? `max()` again. The escort's threat-aware hold state should read both players' faction values before deciding whether to break hold or stay.

Host role as network topology is the right frame. Keep it entirely out of the standing read paths.


<!-- complete -->
