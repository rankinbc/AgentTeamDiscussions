# Morning Brief Format

*Derived from live agent conversation (2026-03-25) + orchestrator-event-cadence.md + key-takeaway-mechanism.md*

## Design Principle

The Morning Brief is the single user-facing artifact from an overnight session. The user reads it at 7 AM, possibly on their phone. If the RED section requires them to open the session transcript to make a decision, the brief has failed.

Total length: under 300 words. 90-second read for RED-only scan.

---

## Format

```
MORNING BRIEF
[Session name] | [Date] | [N turns, N agents, N hours]

--- RED -- DECISION REQUIRED ---

[max 2 items, ~60 words each, 3 lines max per item]

1. [Topic]
   Position A: "[verbatim position]" (contestation: X.X)
   Position B: "[verbatim position]" (contestation: X.X)
   YOUR CHOICE: [one sentence framing the actual decision the user must make]

2. [Topic]
   ...

--- YELLOW -- NEEDS ATTENTION TODAY ---

[max 3 items, 1 line each]

- [Unresolved thread] -- last owned by [Agent Name]
- [Unresolved thread] -- last owned by [Agent Name]
- [Unresolved thread] -- last owned by [Agent Name]

--- GREEN -- CONFIRMED, NO ACTION ---

[all confirmed takeaways, 1 line each]

- [Takeaway text] (contestation: X.X)
- [Takeaway text] (contestation: X.X)
- ...

--- SYSTEM ALERTS ---

[only if failures occurred during session]

- Turn [N]: Agent [name] produced unparseable response. A takeaway
  proposal or challenge may have been lost. Review raw transcript.
- ...
```

---

## Section Rules

### RED -- Decision Required

**Purpose:** Items where the agents could not converge and the human must break the tie. These are the takeaways that were proposed but rejected with split votes, or confirmed with contestation above 0.7 where the dissent represents a genuine alternative rather than a minor objection.

**Content:** The two strongest competing positions, stated verbatim from agent messages (not summarized by the orchestrator). The contestation score for each position. One sentence framing the choice -- not "agents disagreed on X" but "choose whether X should be [option A] or [option B]."

**Hard cap:** Maximum 2 items. ~60 words per item. 3 lines max per item. If more than 2 items qualify, the orchestrator ranks by contestation score and promotes only the top 2. Remaining items move to YELLOW.

**The 60-word cap is structural, not stylistic.** Exceeding it causes the user to open the transcript, which means the brief failed its only job. If the two positions cannot be stated in 60 words, the orchestrator must compress them further, even at the cost of nuance. The transcript preserves nuance; the brief preserves attention.

**Source:** Confirmed takeaways with contestation > 0.7 AND rejected takeaways where the vote split was close (average 5-6). The orchestrator selects from both pools.

### YELLOW -- Needs Attention Today

**Purpose:** Threads that were discussed but never reached a takeaway proposal. The user should be aware of these and may want to steer the next session toward resolving them.

**Content:** One line per thread: what the thread was about and which agent last engaged with it. No positions, no scores -- just the topic and the owner.

**Hard cap:** Maximum 3 items. If more than 3 unresolved threads exist, the orchestrator ranks by recency (most recently discussed = most likely still relevant) and shows the top 3.

**Source:** The dropped-thread list from the orchestrator's per-turn pattern capture. Threads that were raised, discussed for 2+ turns, but never formalized as a takeaway.

### GREEN -- Confirmed, No Action

**Purpose:** The reward section. The user sees what was decided without needing to act. This is the "work got done overnight" signal that builds trust in the system.

**Content:** All confirmed takeaways, one line each, with contestation scores. Sorted by confirmation order (chronological).

**No cap.** If the session produced 12 confirmed takeaways, show all 12. This section is for reading, not acting -- length does not degrade its utility the way it does for RED.

**Source:** Confirmed takeaways from the Key Takeaway mechanism with contestation <= 0.7 (higher contestation items are candidates for RED).

### System Alerts

**Purpose:** Surface failures that occurred during the session so the user knows to check the transcript. Present only when failures occurred.

**Content:** Each alert is one line: turn number, agent name, nature of the failure.

**Source:** Terminal failure flags from the footer reliability policy (challenge-response field parse failures that survived retry). Also: synthesis parse failures, agent timeout errors, and any other orchestrator-level errors that may have affected output quality.

**This section should almost always be empty.** If it regularly has content, the footer format or the retry logic needs fixing.

---

## Generation

The Morning Brief is assembled from existing orchestrator state at session end. It does NOT require an LLM call.

| Section | Source Data | LLM Required? |
|---------|------------|---------------|
| RED | Confirmed takeaways with contestation > 0.7 + rejected takeaways with close splits | No -- positions are verbatim from agent messages, choice framing is a template fill |
| YELLOW | Dropped-thread list | No -- thread text and last-owner agent are already tracked |
| GREEN | Confirmed takeaways with contestation <= 0.7 | No -- takeaway text is already stored |
| System Alerts | Error log | No -- flags are already logged at failure time |

**Conflict note:** The orchestrator-event-cadence spec says the Morning Brief requires zero additional LLM calls. The RED section's "one sentence framing the actual choice" could be argued to require an LLM call if the choice framing is non-trivial. Resolution: the choice framing is a template: "Choose whether [takeaway topic] should be [position A summary] or [position B summary]." The position summaries are the agent's `key_claim` footer fields from the relevant turns, not LLM-generated summaries. If the key_claims are too long, truncate to first clause. Zero LLM calls.

---

## Token Budget

The Morning Brief is a post-session output artifact, not an in-context injection. It has no token budget constraint from the context assembly template. The 300-word / 90-second constraint is a readability target for the human, not a system limit.

However, if the Morning Brief is used as input to a next-session briefing (see orchestrator-event-cadence spec, phase briefing), it must fit within the ~500 token phase briefing budget. The GREEN section is the compressible portion: "[N] takeaways confirmed, see previous brief for details."

---

## Relationship to Existing Specs

- **orchestrator-event-cadence.md** -- The Morning Brief is the post-session action defined in that spec. It consumes the running summary structures (concession log, position tracker, dropped-thread list) that the orchestrator maintains via per-turn pattern capture.

- **key-takeaway-mechanism.md** -- Confirmed takeaways populate GREEN and (if high contestation) RED. Tombstones populate YELLOW if the rejected idea represents an unresolved thread. The two-field tombstone (agent-facing killing blow + user-facing override prompt) is the source for RED items that come from rejected takeaways.

- **context-assembly-template.md** -- The footer reliability policy's terminal failure flag ("unlogged decision") is the source for System Alerts. The `key_claim` footer field provides the position summaries for RED items.
