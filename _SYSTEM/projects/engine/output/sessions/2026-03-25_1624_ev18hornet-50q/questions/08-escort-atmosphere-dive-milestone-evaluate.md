### Soren (solo dev scope warden)

The dive milestone isn't the open question. M8 is already decided and this discussion didn't move it. What this discussion *did* do is add scope to M6 hold behavior, and that's what needs a cost attached before it gets committed.

Tally what's now on M6 hold behavior:

- Layer-transition detection
- Hold state (not pose) with interruptibility
- Faction standing reads from inside the hold state
- Raid threat detection during hold
- A player-facing communication surface (comms line or equivalent)

Each of those is a discrete build item. Ren's "threat-aware from day one" is the one I'd watch — it's the right architecture call, but "threat-aware" starts touching raid spawn logic, faction standing reads, and AI state interruption in a milestone that was supposed to validate galaxy-layer formation feel. That's M6 reaching into M7 and M8 systems to do it correctly.

My read: the communication surface (Nadia's comms line) is cheap and eliminates the first-impression problem. A single string on layer entry — "holding at altitude" — is an afternoon. Ship that.

The threat-aware hold state is the right answer architecturally, but it needs a build estimate before it's committed to M6. "Hold state that reads faction standing" is not the same cost as "hold pose." If that estimate comes back at more than 3 days, it belongs in M7 as a named item, not as an implicit M6 requirement that grows in place.

What's the current M6 scope list? That's the number this conversation needs before it can close.


<!-- complete -->
