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
