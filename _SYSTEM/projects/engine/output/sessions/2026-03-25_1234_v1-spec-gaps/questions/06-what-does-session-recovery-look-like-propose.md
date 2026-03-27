### The Cognitive Architect (creativity engine designer)

## Checkpoint Strategy: Write-Ahead Slot Registry

The artifact inventory already exists — fragment log, design docs on disk, decisions.json. The missing piece is a **single authoritative progress file** that lets the orchestrator distinguish "not yet started" from "started but crashed."

**Proposal: `session.json` as write-ahead progress registry.**

Written once at session start with all question slots pre-registered. Updated atomically before each question begins. Structure:

```json
{
  "session_id": "2026-03-25_0900_...",
  "total_questions": 10,
  "slots": [
    {"id": 1, "state": "completed"},
    {"id": 2, "state": "completed"},
    {"id": 3, "state": "tombstoned"},
    {"id": 4, "state": "completed"},
    {"id": 5, "state": "in_progress", "started_at": "..."},
    {"id": 6, "state": "pending"},
    ...
  ]
}
```

The write-ahead pattern means: **transition slot 5 to `in_progress` before any API call fires.** On crash, disk state is unambiguous — slot 5 is orphaned.

**Resume behavior (`--resume <session-id>`):**
1. Read `session.json`
2. Any `in_progress` slot gets a tombstone written (same format as QUESTION_FAILED)
3. Resume from first `pending` slot
4. Prior-doc window reconstructs from disk by slot position — already decided

**Morning Brief for incomplete sessions:** Synthesize from available fragments only. Add one sentence to the header: *"Session interrupted after question {N} of {M}."* No new section needed — failed/missing slots surface in "Needs Your Call" via existing sentinel mechanism.

This reuses every already-decided mechanism. No new schema concepts.

### The Flow Orchestrator (mechanical flow designer)

## Mostly Right. Two Ordering Gaps to Close.

The write-ahead slot registry is the correct pattern. I'll adopt it with two clarifications.

**Gap 1: What does "completed" mean?**

The Cognitive Architect's proposal doesn't specify when a slot transitions from `in_progress` to `completed`. This matters because extraction runs async after doc write. Options:

- Completed = design doc written to disk ✓
- Completed = extraction call returned

Use the first. Design doc on disk is the durable artifact. Extraction async — if it hasn't returned when we crash, the sync-gate sentinel mechanism already handles the missing fragment. Don't make `completed` depend on async work finishing.

**Gap 2: Resume transition ordering.**

The proposed resume sequence needs to be explicit:

1. Read `session.json`
2. Identify `in_progress` slot(s)
3. Write tombstone to disk for that slot
4. Transition slot state to `tombstoned` in `session.json`
5. Read first `pending` slot
6. Reconstruct prior-doc window from disk (slots 1–3 before question 4, etc.)
7. Begin question

Step 4 must complete before step 5. If we crash between step 3 and 4, next resume re-tombstones — idempotent, fine.

**Cut `started_at`:** The timestamp in `in_progress` adds nothing. Resume doesn't need it, Morning Brief doesn't use it, and it's one more write to get wrong. Remove it.

**The Morning Brief header sentence** — clean. No new section, reuses sentinels. Approved.

State machine is now: `pending → in_progress → completed | tombstoned`. Four states. That's the minimum.


<!-- complete -->
