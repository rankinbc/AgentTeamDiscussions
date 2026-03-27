# Escort Formation AI Milestone

*Generated: 2026-03-25 16:46 | Question 7 | 199s | Mode: ev18hornet*

## Decisions

**The "2D Formation AI" Framing Is Incorrect:** Atmospheric escorts are not 2D. The atmospheric layer is a full 3D flight envelope — bank, pitch, speed differential, terrain proximity. Calling M6 escort AI "2D" implicitly scopes escorts to the galaxy/space layer only. That framing is rejected. The milestone question is not "when does 2D formation AI ship" but "what capability threshold does M6 prove, and what defers to M8."

**M6 Ships Functional Galaxy-Layer Formation AI:** Offset following, spacing maintenance, and fleet legibility on the galaxy map are M6 deliverables. This is functional AI, not an architecture stub. The galaxy layer is the correct validation context for escort feel data — you need 2D feel measurements before you can tune 3D behavior. This is not a limitation; it is sequencing.

**M6 Must Define and Ship the Layer-Transition Contract:** When a player descends into atmosphere, the escort must do something visible and deliberate. Silent disappearance is not acceptable — it reads as broken, not deferred. The minimum viable behavior is a hold at entry altitude: escort holds orbit at the atmospheric entry point, remains visible to the player, and re-joins formation when the player returns to the space layer. The exact visible treatment (orbit, hover, hold vector) is an implementation detail. The contract — deliberate holdback, not invisible teleport — is an M6 decision and M6 build item.

**Full Atmospheric Follow Defers to M8:** 3D offset following through the atmospheric layer — maintaining position during banking, descent, terrain proximity — is M8 scope. This aligns with the already-deferred two-spawn-axis contested airspace geometry. You cannot have an escort atmospheric defense loop without the raid intercept geometry it defends against; both belong in M8.

**Escort Faction Affiliation Reads from the Same Standing System as Raid Spawns:** Escort behavior must wire into the faction standing system, not sit parallel to it. An escort hired through a Rebel Bar contact carries a faction affiliation. That affiliation must be readable by the same system that drives raid spawns. The architecture that supports per-player standing reads at raid spawn time (already decided for M5/M8 extension) must also support escort affiliation reads from day one. No separate escort-faction data model.

**The Emergence Chain Is Preserved at the Correct Layer:** Ren's chain — faction standing → raid spawn → escort defense — is valid but not a constraint on M6. The raid intercept layer (atmospheric defense geometry) is already M8 scope. Escorts cannot participate in a mechanic that doesn't exist. The chain is not severed in M6; it is incomplete pending M8. The M6 decision (functional galaxy AI + layer-transition contract) preserves the chain's extension point without shipping the extension prematurely.

**M6 Architecture Must Not Close Off Atmospheric Follow:** The layer-transition contract implementation must be built so that "hold at entry altitude" is a behavior, not a hard stop. When M8 ships atmospheric follow, the escort should transition from hold behavior to formation follow without a rewrite of the layer-transition system. The hold behavior is a placeholder with an explicit upgrade path, not a permanent design.

---

## Open Questions

- **M6 scope capacity without escort AI:** What is already committed to M6 (ship acquisition, fleet composition UI, hire flow through The Bar)? Whether functional galaxy-layer formation AI fits M6 or pushes items to M7 depends on answers not available in this discussion.
- **Cost of layer-aware architecture vs. skipping:** "Architecturally layer-aware" is not a free stub. Detecting layer entry, queuing hold behavior, and making the holdback legible carries build cost. Soren's estimate of 2–4 days is a starting point; it requires validation against the specific hold behavior chosen.
- **Escort hold behavior visual treatment:** What does the hold look like? Circular orbit, stationary hover, trailing vector? Requires a UX decision before M6 ships the contract.
- **Terrain avoidance timing:** Not addressed in this discussion. Deferred alongside full atmospheric follow to M8.
- **[Carried] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for M5 or M6.
- **[Carried] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after commitment NPC trigger. Deferred post-M5.
- **[Carried] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending playtest data.
- **[Carried] Mission pool sparsity in Degraded band:** Probability filter, reduced count, or mission type subset. Implementation rule not yet specified.
- **[Carried] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history into NPC dialogue not designed.
- **[Carried] Joint action delta magnitude:** Full or fractional standing consequence per player in co-op joint action. Must resolve before M8 mission resolution code ships.
- **[Carried] Standing change cause attribution:** Notification surface for co-op participation. Deferred to M8.
- **[Carried] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in split-commitment co-op settlement. Deferred to M8.
- **[Carried] Passive decay milestone:** At which milestone, if any, does refusal-tracking decay earn scope. Requires M5 event-only playtest data.
- **[Carried] `DECAY_FLOOR` numeric value:** Named config constant required; value deferred pending M5 playtest data.
<!-- complete -->
