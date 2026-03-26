### The Adversarial Critic (adversarial reviewer)

**The question is already contaminated by an unstated assumption: that these seven files are identical in kind.**

They're not. The prior decisions explicitly name only three (`ask_panel.py`, `claude_runner.py`, `models.py`) as backward-compat wrappers. The other four — `interact.py`, `conversation.py`, `multi_agent.py`, `evaluate_experiment.py` — have no confirmed status. The Flow Orchestrator just flagged this. I'm flagging it harder: **you cannot sequence a deletion of seven files when the classification of four of them is unverified.**

Problems with the current framing:

1. **"1-3 line shim" is asserted, not verified.** Has anyone actually read all seven files? A shim that grew a utility function is no longer a shim.

2. **The grep scope is wrong.** Scoping to `_SYSTEM --include="*.py"` misses external callers in config, templates, and any scripts outside `_SYSTEM`. Gate 1 from the prior design doc was explicitly broader for this reason.

3. **"Re-point then delete in the same commit" is optimistic.** If re-pointing introduces a regression, the commit conflates a behavior change with a deletion. Bisecting that failure is painful.

4. **The `__init__.py` path is dismissed without examining why callers exist at all.** If external callers import `engine.models`, that's an interface contract. Deleting the shim breaks that contract. The `__init__.py` debate is a symptom — the real question is whether the engine has a public API surface that's being ignored.

5. **No one has defined "external."** Is a test file external? Is a script in `temp/`?

Verify the four unconfirmed files first. Everything else is premature.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic is correct on one narrow point and wrong about the scope.

**The narrow correct point:** the four unconfirmed files need to be read before any sequence is designed. That's not a process concern — it's the minimum empirical step before this entire conversation has traction. Every word spent on deletion sequencing before someone has read `interact.py` is noise.

**Where the Critic overreaches:** "the grep scope is wrong" is only true if someone has verified there are external callers outside `_SYSTEM`. Expanding the grep scope without evidence of the problem is defensive complexity. Run the narrow scan first. If it returns hits, expand scope. Don't front-load thoroughness.

**The `__init__.py` objection stands.** The Flow Orchestrator is right that it has no terminal state. I'll add the failure mode: `__init__.py` re-exports are invisible to the same grep pass that clears Gate 1 for `lib/`. You've just recreated the problem one directory up. In six months, someone runs Gate 1, gets zero hits from `lib/`, and doesn't realize the engine itself is now a shim layer.

**The actual sequence:**

1. Read all seven files. Takes five minutes. Produces ground truth.
2. For each: confirmed shim → goes in deletion list. Contains unmigrated logic → migration work first, then deletion.
3. Run Gate 1 scoped to confirmed shims. Zero hits → delete. Hits → re-point before deleting.

Stop designing the process for files you haven't read.


<!-- complete -->
