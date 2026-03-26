# Passive Standing Decay

*Generated: 2026-03-25 16:42 | Question 6 | 174s | Mode: ev18hornet*

## Decisions

**Standing Does Not Decay Passively in M5:** Faction standing moves only through explicit player-attributable events — mission completion, mission failure, combat outcomes, and trade actions with standing consequences. No time-ticker, no mission-drought counter, no refusal-tracking surface ships in M5. The event-only model is not a compromise; it is the EV-faithful baseline, and no M5 failure mode has been identified that requires departing from it.

**The "Static Airspace" Problem Is an M8 Problem:** The motivation for passive decay — that faction airspace feels like a diorama without standing movement — is correctly diagnosed as an atmospheric layer concern. Patrol density as standing feedback is already decided as M8 scope. Routing an M8 atmospheric texture problem through an M5 faction standing addition is premature coupling. The airspace texture problem will be addressed in M8 with its own design surface, not by modifying the standing system in advance of that work.

**Event-Only Standing Is Correct for Legibility, Not Only for EV Faithfulness:** Every standing movement must be traceable to a player action the player understood as a choice at the moment they made it. The existing tooltip system (fires at crossing 40 in either direction, per prior decision) is the standing feedback surface. Passive decay — any model — produces standing loss without a recognized player choice, and the tooltip fires too late to serve as a satisfying causal signal for loss that began silently. The new-player case makes this load-bearing: a player building a Claim Stake across their first sessions, having done no faction-negative action they recognized, must not walk into the Bar to find a cold contact. Silent standing loss before the player has a mental model of the standing system produces confusion, not tension.

**Refusal-Tracking Is the Least-Wrong Decay Model If Decay Ships Post-M5:** If passive decay earns its scope in a later milestone through demonstrated gameplay need, the mission-drought model should use declined or ignored mission offers as the decay trigger — not calendar time. The faction offered contact through the Bar; the player did not take it. Neglect is measured in refusals, not seconds. This maps to the existing Bar interaction model without introducing a new time-tracking surface. However, the implementation must resolve the attribution edge case (offered-while-player-was-elsewhere vs. deliberately declined) before shipping, and that resolution has not been designed. This is a post-M5 design problem.

**A Decay Floor Above the Hostile Threshold Is a Required Architectural Constraint If Decay Ships:** Any future passive decay implementation must include a hard floor — named `DECAY_FLOOR` — set above `HOSTILE_THRESHOLD` in config. Passive decay may erode standing into the Degraded band. It may not cascade a player into Hostile. Reaching the Hostile band requires an explicit negative player action. These are different player choices and must produce different system states. The separation is not merely a tuning question; it is a behavioral contract. `DECAY_FLOOR` has no authored value in M5 because standing movement rates under event-only play have not been measured. The constant must exist in config architecture regardless so that future authoring requires no code change.

**No New Config Constants or Data Model Entries Required for M5 Standing Decay:** `DECAY_FLOOR` is a future-scoped constant that belongs in the config architecture design for whatever milestone ships decay, not in M5. M5 ships event-only standing with the existing `mutate_standing(player, faction, delta)` call signature, the existing behavioral band thresholds, and the existing tooltip trigger. No decay-related constants, counters, or tracking surfaces are added.

---

## Open Questions

- **Passive decay milestone:** At which milestone, if any, does mission-drought refusal-tracking decay earn its way into scope? Requires solo standing movement playtest data from M5 event-only play before the design problem (neglect signal vs. administrative taxation) is answerable with evidence.

- **Refusal-tracking attribution rule:** If decay ships, how does the system distinguish "player declined a mission offer" from "player was not present when the offer was available" from "player has not yet reached a Bar on a faction-associated planet"? The edge case is real and unresolved.

- **`DECAY_FLOOR` numeric value:** Must be a named config constant set above `HOSTILE_THRESHOLD`. No defensible value until standing movement rates under event-only play are measured. Deferred pending M5 playtest data.

- **[Carried from Q5] Hostile floor numeric value:** What standing value marks the Degraded/Hostile boundary? Named config constant required from day one. Requires playtest data.

- **[Carried from Q5] Authored Hostile recovery trigger form:** Intermediary NPC, specific mission string, or faction-unique narrative unlock. Design deferred pending playtest data on how often players reach Hostile under normal play.

- **[Carried from Q5] Mission pool sparsity definition in Degraded band:** Probability filter, reduced mission count at Bar contacts, or mission type subset. Implementation rule not yet specified.

- **[Carried from Q3–Q5] Per-faction rivalry heat values:** Which faction pairs have hotter relationships. Out of M5 scope. Config architecture must support per-faction overrides from day one.

- **[Carried from Q3–Q5] Defection multiplier post-commitment:** Whether `FACTION_STANDING_LOSS_MULTIPLIER` increases after a player triggers the commitment NPC and acts for the opposing faction. Deferred; applies post-commitment only.

- **[Carried from Q3–Q5] Standing floor behavior post-commitment:** Whether standing can fall below a threshold with an allied faction after commitment. Undefined for M5.

- **[Carried from Q3–Q5] Commitment NPC dialogue content:** Exact dialogue across settlement tier contexts. Content system for reading settlement tier and raid history variables into NPC dialogue not yet designed.

- **[Carried from Q4–Q5] Joint action delta magnitude:** Full or fractional standing consequence per participating player in a co-op joint action. Must be resolved before M8 mission resolution code ships.

- **[Carried from Q4–Q5] Standing change cause attribution for co-op:** Notification surface for attributing triggering action and player role. Deferred to M8.

- **[Carried from Q3–Q5] Contested airspace spawn geometry:** Two-spawn-axis design for opposing faction intercepts in a split-commitment co-op settlement. Deferred to M8.
<!-- complete -->
