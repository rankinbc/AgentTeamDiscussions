# Escort Atmosphere Dive Milestone

*Generated: 2026-03-25 16:49 | Question 8 | 181s | Mode: ev18hornet*

## Decisions

**Atmosphere Dive Milestone Is M8:** Escort atmospheric follow — 3D offset following through banking, descent, and terrain proximity — is M8 scope. This is not a deferral under pressure; it is correct sequencing. Galaxy-layer feel data must precede atmospheric behavior tuning. You cannot tune a 3D flight envelope escort without solo atmospheric feel measurements to tune against. This decision is carried from Q7 and confirmed without dissent.

**M6 Ships Functional Galaxy-Layer Formation AI:** Offset following, spacing maintenance, and fleet legibility on the galaxy map are M6 deliverables. The atmospheric escort problem is different in kind, not in degree — bank angle anticipation, speed differential management, and terrain proximity response are not extensions of flat-space formation logic. M6 proves the formation system works. M8 proves it works in atmosphere.

**M6 Must Define and Ship the Layer-Transition Contract:** Silent escort disappearance on atmospheric entry is not acceptable. It reads as broken regardless of whether it is intentional. The minimum viable behavior is a hold at entry altitude: escort holds position at the atmospheric entry point, remains visible, and re-joins formation when the player returns to the space layer.

**Hold Behavior Must Be a State, Not a Pose:** The entry-altitude hold must be implemented as an interruptible AI state, not a frozen animation or static position. A pose cannot respond to changed conditions. A state can. The distinction is not cosmetic — it determines whether M8 can extend the hold into atmospheric follow without rewriting the layer-transition system. "Hold at entry altitude" must be a named, interruptible state in the escort AI graph.

**Hold State Must Be Threat-Aware from Day One:** The atmospheric entry point is geometrically the same chokepoint where faction raid intercepts arrive. An escort holding at entry altitude occupies the intercept vector. That is not incidental — it is the faction standing → raid spawn → escort defense emergence chain showing its structure before the atmospheric layer is complete. The hold state must read faction standing data using the same read path that drives raid spawns. An escort that ignores a raid spawning around it while the player is in atmosphere breaks the standing system's consequence traceability at the layer boundary. That breakage discovered at M8 is expensive. The threat-aware read costs less in M6 than a rewrite costs in M8.

**Hold State Requires a Player-Facing Communication Surface:** New players have no prior context for why an escort would hold at altitude. They will read a correctly-implemented hold as a broken AI. A single legible signal before the player crosses the entry boundary — a comms line, a brief acknowledgment — converts "the AI froze" into "they are waiting for me." This is not a tutorial. It is the minimum authored signal that protects the atmospheric dive as a positive first-impression moment. A static string on layer entry ("Holding at altitude, standing by") is low build cost and eliminates the first-impression problem.

**Threat-Aware Hold State Requires a Build Estimate Before M6 Commitment:** "Hold state that reads faction standing and interrupts on raid threat" is not the same build cost as "hold pose." The threat-aware requirement touches raid spawn logic, faction standing reads, and AI state interruption in a milestone scoped to validate galaxy-layer formation feel. If the estimate for the threat-aware hold exceeds approximately three days, it belongs in M7 as a named scope item rather than as an implicit M6 requirement that grows in place. The communication surface (comms line) is confirmed as a cheap ship item regardless of the threat-aware estimate.

**Escort Faction Affiliation Reads from the Standing System:** No separate escort-faction data model. Escort affiliation is carried through the same per-player standing reads that drive raid spawns. The M5/M8 architecture extension (raid spawn accepts a player reference, not a global) must also support escort affiliation reads from day one.

**M6 Architecture Must Not Close Off Atmospheric Follow:** The hold behavior is an upgradeable placeholder. M8 must be able to transition the escort from hold state to atmospheric formation follow without a layer-transition system rewrite. This is an architectural contract, not a feature commitment.

---

## Open Questions

- **M6 scope capacity:** What is already committed to M6 (ship acquisition, fleet composition UI, hire flow through The Bar)? Whether functional galaxy-layer formation AI and the threat-aware hold state both fit M6 or whether the hold state pushes items to M7 cannot be determined without the current committed scope list.

- **Build cost of threat-aware hold state:** Soren's estimate requires validation. Detecting layer entry, reading faction standing from inside the hold state, and implementing raid threat interruption are discrete build items. The estimate gates the M6 vs. M7 placement of the threat-aware requirement.

- **Escort hold visual treatment:** What does the hold look like from the cockpit? Circular orbit, stationary hover, and trailing vector read differently in flight than on a map. A UX decision is required before M6 ships the contract. This decision was not reached in this discussion.

- **Mechanical resolution when a raid spawns during escort hold:** If a raid exits FTL into the entry altitude space while the escort is holding and the player is underground — does the escort engage? Can it be destroyed? Does the player surface to a changed tactical situation? The threat-aware hold state enables this resolution to be authored; the authored rule itself is not yet specified.

- **[Carried from Q7] Terrain avoidance timing:** Deferred alongside full atmospheric follow to M8.

- **[Carried from Q3–Q7] Per-faction rivalry heat values:** Config architecture must support per-faction overrides from day one; no authored values for M5, M6, or M7.

- **[Carried from Q3–Q7] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after commitment NPC trigger. Deferred; applies post-commitment only.

- **[Carried from Q5–Q7] Hostile floor numeric value:** Named config constant required from day one; numeric value deferred pending M5 playtest data.

- **[Carried from Q5–Q7] Mission pool sparsity in Degraded band:** Probability filter, reduced count, or mission type subset. Implementation rule not yet specified.

- **[Carried from Q3–Q7] Commitment NPC dialogue content and content system:** Exact dialogue across settlement tier contexts; content system for reading settlement tier and raid history into NPC dialogue not designed.

- **[Carried from Q4–Q7] Joint action delta magnitude:** Full or fractional standing consequence per player in co-op joint action. Must resolve before M8 mission resolution code ships.

- **[Carried from Q4–Q7] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8.

- **[Carried from Q3–Q7] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in split-commitment co-op settlement. Deferred to M8.

- **[Carried from Q6–Q7] Passive decay milestone:** At which milestone, if any, does refusal-tracking decay earn scope. Requires M5 event-only playtest data.

- **[Carried from Q6–Q7] `DECAY_FLOOR` numeric value:** Named config constant required; value deferred pending M5 playtest data.

- **[Carried from Q3–Q7] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

- **[Carried from Q5–Q7] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Deferred pending playtest data on Hostile band frequency under normal play.
<!-- complete -->
