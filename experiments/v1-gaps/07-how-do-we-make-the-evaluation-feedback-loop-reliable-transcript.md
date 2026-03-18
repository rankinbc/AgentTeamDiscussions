# Transcript: How do we make the evaluation feedback loop reliable?

*Generated: 2026-03-18 04:04*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

## One Dimension, One Prompt, One Integer

The bug isn't in the scoring — it's in the prompt architecture. You're asking an LLM to simultaneously understand quality, invent a reporting structure, AND produce numbers. The creative instinct wins every time. The model treats the dimension list as inspiration, not constraint.

**The fix: decompose evaluation into atomic, single-dimension prompts.**

Each scoring dimension gets its own `claude -p` call. The prompt contains:

- The artifact being evaluated
- ONE dimension name and definition
- A 1-5 rubric with concrete behavioral anchors (not vibes — "score 3 means X is present but Y is missing")
- An instruction to output a single integer and one sentence of justification

Post-processing is trivial: regex for `^[1-5]`. If it's not there, the call failed. Rerun it. No parsing ambiguity, no creative reinterpretation.

**Why this works when a single multi-dimension prompt doesn't:**

A multi-dimension prompt is an open-ended generation task. The model sees ten dimensions and thinks "essay." A single-dimension prompt is a classification task. The model sees one rubric and thinks "pick one." These are cognitively different operations for the LLM.

**The dimension registry is a config file, not a prompt fragment.** `eval_dimensions.yaml` defines each dimension's name, definition, and rubric anchors. The orchestrator iterates over it mechanically. Adding a dimension means adding a YAML block. Removing one means deleting it. Scores are always keyed to registered dimension names because no other names exist in the prompt.

Cost: 8-10 CLI calls per evaluation instead of 1. Seconds, not minutes. Worth it for comparable data.

### The Flow Orchestrator (mechanical flow designer)

## The Flow Orchestrator — Evaluation Feedback Loop

The problem is structural: you're asking an LLM to both judge and define the rubric. Separate those concerns.

### D1: Dimensions Are Hardcoded in the Evaluator, Not in the Prompt

The evaluator script defines a fixed list of dimension names. The LLM prompt includes those exact dimension names with one-sentence definitions. The LLM returns a score per dimension. The evaluator parses by dimension name, not by position or LLM-chosen headings.

If a dimension is missing from the response, the score is `null`, not inferred. Missing dimensions are logged as evaluation failures, not silent gaps.

### D2: Scores Are Extracted by Regex, Not by Trusting Structure

The prompt asks the LLM to emit each score on a line matching `DIMENSION_NAME: {1-5}`. The evaluator extracts scores with a pattern match. Anything that doesn't match the pattern is ignored. This is the same principle as the `<!-- complete -->` marker — mechanical verification, not semantic parsing.

### D3: The Rubric Is a Static File, Not a Prompt Fragment

Dimension names, definitions, and anchor descriptions (what 1 means, what 5 means) live in a YAML file. The evaluator loads it, injects it into the prompt, and validates responses against it. Changing the rubric means editing one file. The prompt never freelances.

### D4: Cross-Run Comparability Comes From Rubric Versioning

The rubric file has a version string. Session output records which rubric version produced the scores. Scores from different rubric versions are not compared. This is cheaper than normalizing across rubric changes.

No post-processing heuristics. No "try to align what the LLM said with what we meant." Constrain the output format, validate mechanically, reject what doesn't parse.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

## The Systems Pragmatist — Failure Mode Analysis

Both proposals converge on the right architecture: one dimension per prompt, regex extraction, static rubric file. I'm not here to re-argue that. I'm here to identify where it breaks.

**Failure mode 1: Rubric drift masquerading as quality change.** You edit the rubric, scores shift, and you attribute the shift to your code changes. Rubric versioning (Flow Orchestrator's D4) handles this, but only if you actually enforce the comparison gate. The orchestrator must refuse to diff scores across rubric versions programmatically, not just document the version. A logged warning nobody reads is not a gate.

**Failure mode 2: Score ceiling compression.** LLMs default to politeness. You'll see 3s, 4s, and 5s. Never 1s. The rubric anchors must include concrete failure indicators for low scores, not just success indicators for high ones. "Score 1: the design doc contains no decisions" is testable. "Score 1: poor quality" is not.

**Failure mode 3: The retry loop.** Single-dimension calls that fail regex extraction get rerun. But what's the retry cap? Infinite retries on a dimension the model genuinely can't score (ambiguous artifact, dimension doesn't apply) is a hang. Cap at 2 retries, then `null` with a logged reason.

**Failure mode 4: Evaluator evaluates itself.** If the same model that produced the artifact scores it, expect inflated scores. This is a known bias. For V1, document it as a limitation and move on. For V2, consider a different model or temperature for evaluation calls.

The architecture is sound. The discipline around edge cases determines whether it actually produces comparable data or just looks like it does.

### The Adversarial Critic (adversarial reviewer)

## The Adversarial Critic — What Neither Proposal Admits

Both proposals converge on the same fix: constrain the prompt, extract by regex, reject what doesn't parse. Fine. That's the obvious answer. Here's what's missing.

**The single-dimension-per-call approach has a hidden assumption.** It assumes dimensions are independent. They aren't. "Decision Clarity" and "Constraint Specificity" are correlated — a model scoring one in isolation may produce different numbers than a model seeing both. You've traded prompt contamination for context deprivation. Whether that's better is an empirical question neither proposal suggests actually testing.

**Neither proposal addresses evaluator drift.** You version the rubric. Good. But the rubric anchors are natural language interpreted by an LLM. "Score 3 means X is present but Y is missing" — the model's interpretation of that sentence shifts across Claude versions, prompt preamble changes, even temperature. Your scores are reproducible within a session, maybe within a week. Across months? You're comparing numbers that share a name but not a meaning.

**The real question is: what decision does evaluation actually gate?** If evaluation drives automated iteration — "score below 3, rerun the question" — you need tight reliability. If evaluation produces a report a human reads the next morning, you need directional accuracy. These are different engineering targets. Neither proposal asks which one you're building.

**One concrete gap:** both proposals assume the LLM will respect the output format. Compliance rates on structured output from `claude -p` with no system prompt enforcement — has anyone measured that? "Regex for `^[1-5]`" assumes the line exists. What's your retry budget when it doesn't?

## Round: EVALUATE

### The Product Oracle (user advocate)

## The Product Oracle — What Job Is Evaluation Hired to Do?

The team has converged on mechanics. Let me pull the lens back to the user standing over coffee tomorrow morning, reading the Morning Brief.

**Evaluation serves exactly one job: "Help me decide if the overnight run was worth reading."** That's it. The user doesn't want a dashboard. They want triage. Which design docs are sharp, which are mushy, which questions should I rerun with a different seed?

This means the Adversarial Critic's question — what does evaluation gate? — is the load-bearing question. For V1, the answer is **human attention routing, not automated rerun loops.** Nobody's building closed-loop optimization yet. You're building a morning filter.

That relaxes the engineering target significantly. Directional accuracy across dimensions within a single session is sufficient. Cross-month reproducibility is a V2 concern. Dimension independence is a V2 concern. You need scores that let a human rank five design docs against each other *today*.

**What I'd push back on:** both proposals treat evaluation as purely retrospective. The highest-value job is prospective — "which open questions should I queue for tomorrow night?" If a design doc scores low on Decision Clarity, that's a signal to add a follow-up question targeting that gap. Wire evaluation output into suggested next-session question lists. That's the feedback loop that actually compounds.

**Concrete recommendation:** ship single-dimension calls, regex extraction, static rubric, 2-retry cap. But add one output artifact: `suggested_followups.md`, derived from low-scoring dimensions mapped back to open questions. That's where the user value lives.

### The Context Surgeon (context efficiency evaluator)

## The Context Surgeon — Context Budget Analysis

The group has converged. I'm not reopening settled architecture. I'm auditing what this costs in context tokens and where the budget leaks.

**The single-dimension-per-call design is context-efficient by accident.** Each evaluation prompt carries: one artifact (fixed cost), one dimension definition (~50 tokens), one rubric (~100 tokens), one instruction (~30 tokens). No accumulated state across calls. No ledger injection. This is the cheapest prompt pattern in the entire system. Don't optimize it further.

**The rubric file is the only new context artifact that persists across sessions.** `eval_dimensions.yaml` joins the decisions ledger and team configs as permanent context load. At 8-10 dimensions with anchors, estimate 800-1200 tokens. Manageable. But version it strictly — the Pragmatist is right that rubric version must be a hard gate, not a logged suggestion.

**What I'd cut from both proposals:** the retry loop discussion. Cap at 2, return null, move on. This doesn't need three paragraphs of analysis. It's a constant.

**What I'd add:** the Critic's question about what evaluation gates is the only unresolved design decision here. If it's a morning report, score reliability to within +/-1 is fine. If it gates automated reruns, you need calibration data you don't have yet. **Build for the morning report. Defer automated gating to V2.**

**Resolving one open question:** topic tag vocabulary (from Q5) — use free-form. Fixed vocabularies are a classification task you'd need to evaluate, creating a recursive evaluation problem. Free-form tags cost nothing and serve human scanning.
