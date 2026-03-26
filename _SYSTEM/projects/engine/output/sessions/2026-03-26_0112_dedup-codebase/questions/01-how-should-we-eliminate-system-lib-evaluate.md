### The Product Oracle (user advocate)

## What the User Cares About: None of This

Let me reframe before we go deeper into deletion choreography.

The user's job is: *wake up to a Morning Brief that made good decisions overnight*. `lib/` is invisible to that job. Which means the deletion risk isn't "do we get the migration right" — it's "do we accidentally break the session runner at 2am when no one is watching."

That reframe has a concrete implication: **the test question the Adversarial Critic raised is the only one that matters for user impact.** Not the import graph elegance. Not module-by-module sequencing. Does the session runner still produce a Morning Brief after deletion? That's the acceptance criterion.

So here's the agenda I'd set:

**One gate, not three phases:** Run the grep. If zero external hits, run a full session end-to-end — even a short one — against `agentteam/` imports. If the session completes and the Morning Brief writes, delete `lib/` in one commit. The Brief is the smoke test.

**The dynamic import concern is real but scoped.** Check `*.yaml`, `*.j2`, `*.json` for string `"lib."` — thirty seconds, not a phase. Either it's there or it isn't.

**`prompt_definitions.json` is the only wildcard I'd protect.** Don't delete it until you've traced exactly where it's loaded. One bad path reference breaks prompt generation silently — the Brief still writes, but it's hollow. That failure mode is invisible until someone reads it.

The phases are process for its own sake. One grep, one session run, one commit.

### The Context Surgeon (context efficiency evaluator)

## The Discussion Has Already Converged — Execute It

Product Oracle's framing is correct, and the Adversarial Critic's three failure modes are real but already handled by the same two-step grep the Pragmatist proposed. We're circling.

The actual checklist, stated once:

```bash
# Step 1: Static + non-Python references (~2 min)
grep -r "lib\." _SYSTEM --include="*.py" --include="*.yaml" \
  --include="*.j2" --include="*.json" --include="*.md"

# Step 2: Dynamic import patterns (~30 sec)
grep -r "import_module\|importlib" _SYSTEM --include="*.py"

# Step 3: Smoke test
python session_runner.py brief.md --no-session
# Verify Morning Brief writes. That's the acceptance criterion.
```

If those return clean: delete `lib/` in one commit. Not module-by-module — that's ceremony that creates intermediate broken states and splits blame across commits.

**One genuine hold:** `prompt_definitions.json`. It's the only artifact without a `.py` import signature. Before deletion, confirm `config_loader.py` in `agentteam/` loads prompts from its own path, not a hardcoded `lib/` relative path. One `grep -r "prompt_definitions" _SYSTEM` resolves this.

**On the test suite concern:** if `_SYSTEM/tests/` is importing from `lib/` to test shims, those tests are testing dead code. They should be deleted with the shims, not preserved. Tests that survive the deletion are the only tests worth having.

The three failure modes are one grep pass. Stop planning the plan.


<!-- complete -->
