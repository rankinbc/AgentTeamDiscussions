### The Systems Pragmatist (infrastructure realist)

## Three Distinct Failure Scenarios. Only Two Need Recovery.

Before designing a checkpoint strategy, name what you're actually recovering from. There are three distinct crash points with different recovery costs:

**Scenario A: Crash between questions.** Question 5 completed, design doc on disk, extraction returned (or timed out). `session.json` shows slot 5 as `completed`. Resume reads state, starts question 6. This is trivial — it already works by the established design.

**Scenario B: Crash mid-question, propose/critique/evaluate not complete.** Slot 5 is `in_progress`. The Flow Orchestrator's resume sequence handles this: tombstone slot 5, advance to slot 6. Work is lost but session continues. Acceptable — already decided.

**Scenario C: Crash mid-write to `session.json`.** This is the one nobody's named yet. If the process dies while writing state, you get a corrupted or stale `session.json`. Resume reads wrong state. You either re-run a completed question or skip a pending one.

**The fix for Scenario C is atomic writes.** Write to `session.json.tmp`, then rename. On POSIX systems, rename is atomic. This is one line of code and eliminates an entire class of corruption.

**Morning Brief for incomplete sessions:** An interrupted session that gets resumed and completes should produce a normal Morning Brief with sentinels for the tombstoned question. An interrupted session the user *never* resumes produces no brief — that's fine. Don't design for that case; it's abandoned work.

**What I need resolved:** Is `--resume` manual (user passes session ID) or automatic (detect `in_progress` on startup)? This affects whether we need a "sessions index" file or just scan the sessions directory.

### The Adversarial Critic (adversarial reviewer)

## Four Problems Nobody Has Named

**The atomic write assumption is wrong for this codebase.** The project root is `C:\claude-workspace\`. POSIX rename atomicity doesn't apply on Windows. `os.replace()` in Python *is* atomic on Windows for same-drive operations — but you need to say that explicitly or the implementer uses `shutil.copy` + delete and introduces the exact corruption you're solving.

**"Completed = doc written to disk" doesn't close the partial-write case.** If the process dies mid-write of the design doc, the file exists but is truncated. The slot shows `in_progress`, resume tombstones it — but the tombstone says "failure type." What failure type? "Round failed" is wrong; rounds completed. "Session crashed" is a new category the tombstone format wasn't designed for. The tombstone spec was written for round-level failures. Resume-triggered tombstones are structurally different. Nobody has addressed this.

**The 4-state machine omits extraction state, and that matters for resume.** Crash while extraction is running: slot is `completed`, no fragment exists. Resume starts question 6 normally. Prior-doc window reads from disk — fine. But synthesis hits a sentinel for the previous question. The user sees a gap in the Morning Brief for a question that *did* complete. That's misleading. The sync-gate handles it mechanically, but the user experience is wrong.

**Multiple interrupted sessions — what happens?** Automatic resume detects `in_progress`. There are two interrupted sessions from last week. Which one resumes? This needs a policy, not a punted question.

The Pragmatist correctly names Scenario C. The rest needs tighter spec before implementation.


<!-- complete -->
