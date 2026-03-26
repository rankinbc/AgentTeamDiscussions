# Evaluation & Improvement

## What It Is

The Evaluation & Improvement system is how you close the loop between "the agents ran overnight" and "the agents got better." It provides tools to review session output, identify where the discussion succeeded or failed, and feed those insights back into the system — whether that means tuning agent configurations, adjusting round structure, or changing how synthesis works.

## Why It Exists

Without evaluation, the system is a black box. You get output, but you don't know:
- Did the agents actually disagree, or did anti-slop mechanisms fail silently?
- Did the critique round catch real problems, or just generate noise?
- Did synthesis produce an implementable spec, or a summary of opinions?
- Where did the conversation go off the rails — and why?

The system generates hours of discussion across dozens of agent turns. Reading raw transcripts is impractical. The Evaluation & Improvement system needs to make it possible to quickly identify what worked, what didn't, and what to change — without reading every word.

This is also the primary mechanism for iterating on the hard problems (like artifact quality). You can't solve "synthesis doesn't produce good enough specs" in the abstract — you solve it by reviewing real output, identifying specific failure patterns, and adjusting.

## How It Fits the System

Evaluation & Improvement sits downstream of everything else — it consumes session output and feeds insights back upstream:

- **Reads from Session Platform**: Session transcripts, decision ledgers, synthesized specs, Morning Briefs
- **Informs agent configuration**: Evaluation findings lead to tuning personality traits, anti-slop settings, voice constraints
- **Informs Conversation Engine**: Round structure, phase gates, and synthesis prompts get adjusted based on what evaluation reveals
- **Informs Creativity Engine**: Anti-slop effectiveness, convergence patterns, and perspective diversity are measurable
- **Feeds Context Management**: If evaluation reveals context assembly problems (agents losing thread, missing decisions), truncation strategies get adjusted

## Core Responsibilities

### Session Review (the unsolved UX problem)

The fundamental challenge: how does a human efficiently review a multi-hour, multi-agent discussion?

**What needs to be reviewable:**
- Per-agent contributions — did each agent stay in character and add value?
- Per-round quality — did propose/critique/evaluate each do their job?
- Synthesis quality — does the design doc actually capture what was debated?
- Decision quality — are extracted decisions accurate, complete, and well-scoped?
- Conversation dynamics — where did the discussion stall, loop, or go off-topic?
- Artifact quality — is the final spec implementable, or just a summary of opinions?

**Possible approaches (not yet decided):**
- Annotated transcript viewer — highlight key moments, flag problems, collapse noise
- Per-question scorecards — rate each question's output on dimensions (creativity, rigor, completeness, actionability)
- Diff view — show what each round added to the evolving spec
- Signal dashboard — visualize agent stance, confidence, and convergence over time
- AI-assisted review — use a separate LLM call to evaluate discussion quality and flag concerns
- Side-by-side comparison — compare output from different agent configurations on the same input

### Quality Metrics

Things that could be measured (some automatically, some requiring human judgment):

**Automatically measurable:**
- Agent stance diversity per round (are agents actually disagreeing?)
- Convergence speed (are they agreeing too quickly?)
- Anti-slop trigger frequency (are the mechanisms firing?)
- Spec section completeness (did synthesis fill all template sections?)
- Decision extraction accuracy (do extracted decisions match synthesis content?)

**Requires human judgment:**
- Are the decisions actually good?
- Is the spec implementable as written?
- Did the agents miss obvious concerns?
- Would a real team have caught things the agents didn't?

### Feedback Loop

How evaluation insights get back into the system:

- **Configuration tuning**: Adjust agent personality traits, anti-slop thresholds, voice rules based on observed behavior
- **Prompt iteration**: Refine round directives, synthesis instructions, and forcing functions based on output quality
- **Structural changes**: Add/remove rounds, change agent assignments, modify phase gates based on what evaluation reveals
- **Regression tracking**: Keep a library of "known good" and "known bad" outputs to test changes against

### Experiment Framework

The system already has experiment modes (default, counter, lean, competitive, etc.) that tested different configurations. Evaluation & Improvement formalizes this:

- Run the same input through different configurations
- Compare outputs on quality dimensions
- Identify which configuration choices improve which aspects
- Build evidence for design decisions rather than guessing

## Open Questions

This concept has more unknowns than the others. Key questions to resolve:

1. **What's the primary review interface?** CLI tool? Web dashboard? Annotated markdown? The answer depends on who's reviewing and how often
2. **How much can be automated?** AI-assisted evaluation is tempting but risks circularity — using LLMs to evaluate LLM output. Where is human judgment irreplaceable?
3. **What's the feedback granularity?** Do you tune per-agent, per-round, per-phase, or per-session? Finer granularity gives more control but costs more review time
4. **How do you track improvement over time?** Need some kind of baseline comparison — is version N+1 of the config actually better than version N?
5. **What does "good output" even look like?** Before you can evaluate, you need a definition of success. This may vary by use case

## Key Design Constraints

- **Must be practical**: If reviewing takes longer than the discussion, nobody will do it. The 80/20 rule applies — surface the most important signals first
- **Must support iteration**: The system will get better over many cycles, not one. The evaluation harness needs to support rapid experimentation
- **Must not require reading everything**: Transcripts are the raw material, not the review surface. Summaries, highlights, and scores should guide attention
- **Must handle subjectivity**: "Good spec" is partly subjective. The system should capture human judgment, not try to replace it entirely

## Interactions

| Component | Relationship |
|---|---|
| Session Platform | Primary data source — all session output feeds evaluation |
| Conversation Engine | Evaluation findings inform round structure and synthesis prompt changes |
| Creativity Engine | Anti-slop effectiveness and perspective diversity are key evaluation dimensions |
| Context Management | Context assembly problems surface as "agents losing thread" in evaluation |
| Discussion Agents | Per-agent contribution quality is a core evaluation metric |

## Current State

V1 has a basic experiment evaluation framework (`evaluate_experiment.py`) that scores discussion output against rubrics and compares across experiment modes. This is a starting point but not yet a practical review workflow. The primary gap is a usable way to review overnight session output and decide what to change — the "morning after" experience beyond just reading the Morning Brief.
