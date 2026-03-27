# Transcript: What should happen to the engine's backward-compat wrapper files?

*Generated: 2026-03-26 01:17*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

The three options collapse into a prior question that isn't asked: **who are the callers?**

Internal callers (code inside `_SYSTEM/projects/engine/`) can be updated in one pass — those shims have no reason to exist once the internal sites are re-pointed. Delete them with the callsite changes as a single commit.

External callers (scripts, notebooks, anything outside the engine directory importing `from ask_panel import X`) are a different matter. If they exist, you can't delete without coordination. But I'd bet most don't — these look like implementation artifacts, not public API surface.

The `__init__.py` re-export path is a trap. It sounds clean but it just moves the confusion: now you have both `engine/__init__.py` and `engine/discussion/engine.py` and `engine/brainstorm/` all competing to be the "real" entry point. You've replaced zombie files with a zombie package namespace.

The cognitive science angle that matters here: **consistency of location signals.** If the rule is "real code lives in submodules," then anything at root level violates that signal and taxes every new contributor's mental model. Vestigial files don't stay neutral — they actively mislead.

**Concrete recommendation:** Gate 1 from the `lib/` deletion protocol applies here too. Run the same grep scoped to these seven filenames across the whole repo. If external call sites are zero, delete them. If call sites exist, schedule a single-commit re-point-and-delete. The `__init__.py` option only makes sense if these files represent a *deliberate public API contract* — which shims never are.

What's the actual caller distribution? That determines everything.

### The Flow Orchestrator (mechanical flow designer)

The Cognitive Architect is right on the core question. But "run Gate 1 scoped to these seven filenames" is a trigger without a sequence. Let me make it concrete.

**The operation sequence is fixed regardless of what Gate 1 returns:**

1. Run grep: `grep -r "ask_panel\|claude_runner\|models\|interact\|conversation\|multi_agent\|evaluate_experiment" _SYSTEM --include="*.py"` — exclude the shim files themselves from results
2. Triage hits into two buckets: inside `_SYSTEM/projects/engine/` vs. outside
3. **If zero external hits:** delete all seven in one commit, no re-pointing required
4. **If external hits exist:** re-point each callsite to the canonical submodule path, then delete shims in the same commit

What I won't accept: the `__init__.py` option as a resolution path. That path has no terminal state. It defers the deletion decision indefinitely and introduces a new ambiguity — does `engine` the package export these names deliberately or accidentally? There's no mechanism to force that question to be answered later. Shims that become `__init__.py` exports stay forever.

The Cognitive Architect flagged "consistency of location signals" — I'll frame that operationally: **every file at the engine root is a decision point that must be evaluated on entry.** Seven ambiguous files means seven branch points in the mental model. That's not neutral overhead, it accumulates.

**Decision point I need answered before sequencing completes:** are `interact.py`, `conversation.py`, and `multi_agent.py` confirmed as shims, or do any contain logic not yet migrated? The prior decisions call out only three files explicitly (`ask_panel.py`, `claude_runner.py`, `models.py`). The other four need explicit status before they enter the deletion sequence.

## Round: CRITIQUE

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

## Round: EVALUATE

### The Context Surgeon (context efficiency evaluator)

**The question is premature by exactly one grep.**

Before this discussion can produce a non-arbitrary answer, one data point is missing: who calls these files from *outside the engine directory*? That's the only variable that changes the answer.

If callers are exclusively internal to `_SYSTEM/projects/engine/`, the answer is mechanical: update the call sites, delete the wrappers, done. The wrapper files have no independent value — they exist only to preserve import paths that shouldn't be preserved.

If there are external callers (scripts in `temp/`, notebooks, external tooling, or the `agentteam/` library itself importing back into the engine), deletion requires coordination. That's a different problem.

**The grep:**
```
grep -r "ask_panel\|claude_runner\|models\|interact\|multi_agent\|evaluate_experiment" \
  _SYSTEM --include="*.py" --include="*.yaml" --include="*.j2"
```
Exclude hits within `_SYSTEM/projects/engine/` itself. What remains is the actual scope of work.

**On the `__init__.py` option:** reject it. The Systems Pragmatist already named the failure mode — you've recreated a shim layer that's invisible to future Gate 1 passes. Converting to `__init__.py` re-exports is the "looks clean, isn't" choice.

**Agenda for this round:**
1. Run the grep above — five minutes, produces ground truth
2. If zero external hits: delete is unambiguous, sequence is trivial
3. If external hits exist: map them, then decide

Don't spend 250 more words on sequencing until that grep runs.

### The Product Oracle (user advocate)

Every agent in this thread is doing engineering. Nobody is asking the product question: **what does this work actually unblock for the person running the system?**

The Morning Brief is the output that matters. These seven shims have zero effect on whether the Morning Brief writes correctly. The acceptance criterion from the prior design doc already said this: a completed session is the smoke test, not a clean import graph.

So here's what I need the team to answer before I'll support any sequencing work: **is there a user-reported failure mode that traces back to these files?** If the answer is no, this cleanup is pure maintenance debt — valuable, but it competes with the next feature the solo builder actually wants.

That said, I'll offer the product frame for *when* this gets done:

The `__init__.py` option fails the simplicity test. A future maintainer opening the engine directory sees a package that might or might not be a public API — that ambiguity is a cognitive tax on every future decision. Delete is the only option with a clean user story: "the directory contains exactly what the engine does, nothing vestigial."

**My recommendation:** Don't sequence this work until the four unconfirmed files are read (the Adversarial Critic is right on this, full stop) and until there's a clear answer that at least one of these shims is causing a real problem — a broken run, a confusing error message, a contributor blocked. Cleanup for its own sake is fine after the Morning Brief pipeline is solid. Not before.

What problem does this solve for the person running a session tonight?

<!-- complete -->
