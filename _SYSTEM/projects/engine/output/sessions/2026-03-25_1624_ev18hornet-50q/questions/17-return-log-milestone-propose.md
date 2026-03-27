### Max (atmospheric flight advocate)

The return log question is actually an atmospheric layer question wearing settlement clothes.

Here's what happens without it in M7: player lands from space, banks into approach, descends through the layer, and sees their power node is dark and storage is gone. They're looking at consequence. But they can't read it. Was it last night? Three sessions ago? One raid or four? The visual tells them *something happened*. The log tells them *what their airspace cost them*.

That descent is the SimCopter payoff. That's the whole reason the atmospheric layer exists as primary gameplay space and not just a transit corridor. You fly over your own settlement from altitude and you *see* your choices reflected back at you. But "reflected back" requires legibility. A damaged settlement without a return log is atmospheric ambiance. With the log, it's consequence you can act on before you touch down.

M7 without a return log means the first time an offline assault-scale raid hits — which is *exactly* the M7 test case — the player surfaces to a state they can't interpret. They don't know whether to rebuild or run escort missions first because they can't see the causal chain.

My agenda question: what is the actual minimum surface that makes the atmospheric return readable? Not a full event timeline. Not a UI dashboard. Just enough that the player, descending through the layer, knows what they're descending *into*.

Is a single-line "last raid outcome" string scoped separately from a full log? Because if so, that's M7. The rest can wait.

### Ren (emergence systems theorist)

Max is right about the payoff moment but I think his framing inverts the causality.

If degraded geometry states are doing their job — communicating strategic consequence legibly at 500 meters in flat-poly, which we decided in Q12 they must — then *the settlement is already the return log*. The power node's silhouette tells you power is down. The shelter geometry tells you capacity dropped. You read the causal chain from the world, not from a UI string.

A return log solves for temporal dimension: *when* and *how many*. The geometry solves for state dimension: *what* and *so what*. The player descending into a darkened power node doesn't need to know it was Tuesday. They need to know to run escort missions before rebuilding, because standing is the gate. That's readable from standing alone — which is already surfaced via the tooltip system.

Where I flag a real systems isolation problem is this: if the degraded state doesn't communicate *causal chain* (raid → damage → standing requirement), the player may correctly read the damage but misattribute it to a bug. One comms intercept line on atmospheric entry — "Confederation patrol activity detected in sector" — does more causal teaching than a full event log, because it connects the damage to the system that produced it.

That's already scoped. `hull_faction_origin` comms intercept pattern is the template.

My position: return log as a separate system is M8 at earliest. What M7 actually needs is the comms entry surface already in scope, pointing at faction standing as the live repair gate. The geometry does the rest.


<!-- complete -->
