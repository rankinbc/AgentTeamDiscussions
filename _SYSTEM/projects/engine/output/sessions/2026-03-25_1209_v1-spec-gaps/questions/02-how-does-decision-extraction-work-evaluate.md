### The Context Surgeon (context efficiency evaluator)

## Agenda: Stop Extracting, Start Emitting

The Systems Pragmatist already closed 60% of this question. Before we design an extractor, acknowledge what's resolved:

**Already decided:** Micro-brief input is extracted decisions OR last-500-token fallback. The fallback exists because extraction wasn't implemented. The question is whether we ever need a standalone extractor at all.

**What the prior discussion proves:** A post-hoc extraction pass on free-form synthesis prose creates a second failure surface with no upside if you can control the synthesis prompt. The synthesis prompt is editable. This is not a debate — it's a precondition check.

**The three questions worth answering today:**

1. **Schema** — decisions.json needs a schema regardless of extraction method. What fields? The micro-brief template already implies: decision text, why-it-won, unresolved risk. Confidence score adds complexity; is it load-bearing or decorative?

2. **Firm vs. recommendation vs. suggestion** — this distinction is only meaningful if something downstream consumes it differently. Does anything in V1 branch on confidence? If not, the three-tier classification is premature schema complexity.

3. **Garbage handling** — already decided: `extraction_failed: true` flag plus skip marker in brief. The schema question is just what that flag lives on.

**My agenda push:** If we instrument the synthesis prompt to emit a structured `## Decisions` block, questions 1 and 2 collapse into "parse that block." Question 3 becomes "what if the block is malformed or absent."

Don't design an extractor. Design a parser for structured synthesis output. The extractor is the wrong abstraction.

### The Product Oracle (user advocate)

## The User Reads the Brief. Not the JSON.

The Systems Pragmatist and Context Surgeon have already closed this. I want to add the user lens, because the schema discussion is drifting toward internal correctness and away from what matters.

**The user's job to be done:** Wake up, open `morning_brief.md`, understand what was decided in 90 seconds. That's it. They never open `decisions.json`. It's plumbing.

Which means the schema question is actually: *what does the brief block need to generate well?* The template is already decided — four fields, one sentence each. The micro-brief prompt needs: decision text, why it won. That's two inputs. The `decisions.json` schema should be exactly that flat, because that's what the consumer requires.

**On three-tier vs. two-tier:** The Flow Orchestrator is right — if nothing branches on `recommended` vs. `suggested` in V1, you're adding schema complexity that makes the config harder to reason about with zero user-visible benefit. Firm decisions in `decided`. Everything else in `open`. The brief's "Unresolved risk" field handles the open tier.

**On the Systems Pragmatist's fix:** Yes, instrument the synthesis prompt to emit a `## Decisions` block. This eliminates the extractor entirely and removes a failure surface the user would never understand if it surfaced. Simpler to configure, simpler to debug, identical user output.

**One thing I'll protect:** The `extraction_failed` flag must surface in the brief. Not in logs. Not silently. The user needs to know when a question produced no structured output — that's a signal worth seeing.


<!-- complete -->
