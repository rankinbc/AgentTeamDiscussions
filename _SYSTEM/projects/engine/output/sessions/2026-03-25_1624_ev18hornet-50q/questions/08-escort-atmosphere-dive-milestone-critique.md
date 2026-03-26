### Vera (EV systems historian)

EV didn't have atmospheric layer transitions. That's not an oversight — it's why escorts in EV *worked*. Every escort stayed in the same 2D envelope as the player, faction affiliation was always legible, and the relationship between standing and escort behavior was traceable at a glance. The system had no seams because there was only one space.

This game is introducing a seam EV never had. That's not a problem — the three-layer architecture is a deliberate extension. But when you extend a system that worked because of its flatness, you need to be precise about which properties you're preserving and which you're deliberately discarding.

What EV gave you with escorts: **consequence legibility**. You knew whose ship was flying with you, you knew what it meant for your standing if they died or defected, and you knew the faction had eyes on you. That chain was readable.

Ren's threat-aware hold point is the only thing in this discussion that actually protects that legibility at the seam. A frozen escort at entry altitude that ignores a raid spawning around it breaks the standing chain — the player surfaces to debris and has no authored way to understand what happened to their consequence structure.

M8 for the dive is correct and already decided. I'm not relitigating that.

What I'm flagging: the hold behavior cannot be implemented as a pose. It must be a state that reads faction standing data. If it doesn't, you're not deferring atmospheric escorts to M8 — you're silently breaking the standing system's traceability at the layer boundary and discovering that breakage at M8 when it's expensive to fix.

### Nadia (new-player experience advocate)

Max named the feeling problem. Ren named the mechanical one. Vera named the EV precedent. I want to name what happens to a first-time player at that moment.

The atmospheric dive is going to be one of the most memorable moments in the first session. Player descends, the horizon bends, the flat-poly terrain rushes up — that's the fantasy payoff the whole early game is building toward. If the escort does something that reads as *broken* at exactly that moment, you've poisoned the memory of your best feature.

But here's what concerns me more than the visual treatment of the hold: **new players have no prior context for why an escort would wait at altitude.** EV players will infer it. First-timers won't. They'll think it's a bug, finish the dive, surface to either a waiting escort or a debris field, and have no authored explanation for either outcome.

That means the hold behavior needs *a single legible moment* — not a tutorial, not a tooltip wall — just one thing that signals "your escort is holding position" before the player crosses the entry boundary. A comms line. A brief visual acknowledgment. Something that converts "AI froze" into "they're waiting for me."

Ren's threat-aware state requirement is correct. I'm adding: that state needs a communication surface toward the player, however minimal. A frozen hold that silently gets destroyed by a raid while the player is underground is not just an M8 problem — it's a first-impression problem that will read as jank to anyone who didn't already trust the system.

M8 for the dive. M6 hold needs a voice.


<!-- complete -->
