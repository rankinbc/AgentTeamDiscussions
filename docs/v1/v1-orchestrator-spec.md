# V1 Orchestrator Spec

*Distilled from agent-generated design docs, design specs, and adversarial review gap analysis. Scoped to what's needed for a working V1.*

## What V1 Does

A solo builder submits an idea brief at night. The orchestrator runs a structured multi-agent discussion. The builder wakes up to a session folder containing design docs, transcripts, a decision log, and a summary brief.

## What V1 Does NOT Do

- No MCP server (agents communicate through the orchestrator directly)
- No two-team separation (single team of agents, different roles)
- No BackgroundAgents (no angels, no planted ideas, no stat manipulation)
- No magnitude system (no numeric idea tracking, no drift mechanics)
- No intra-team talk between rounds
- No random/dream events
- No phase transitions (single discussion flow, not brainstorm->refine->specify->review)
- No AgentMind schema

These are all designed and documented for later versions. V1 validates the core loop.

---

## Architecture

### What We Already Have (from beta)

The beta experiment system (`run_discussion.py`) proves the core pattern works:
- `claude -p` subprocess calls with system prompts built from YAML agent configs
- Structured rounds (propose, critique, evaluate) with parallel agent execution
- Synthesis step that merges rounds into a design doc
- Agent personality configs that produce distinguishable output
- Prompt assembly from personality/position/technique/voice/anti-slop config

### What V1 Adds

1. **Session persistence** -- structured output folder per run with completion markers
2. **Decisions ledger** -- append-only constraint log that chains context across questions
3. **Decision extraction** -- structured JSON extraction from synthesized docs
4. **Error handling** -- per-round disk writes, retry policy, failure cascading
5. **Session recovery** -- resume from last completed question on restart
6. **Morning Brief** -- scannable summary assembled from structured data (zero LLM calls)
7. **Evaluation** -- per-dimension scoring with static rubrics
8. **Cognitive Action System** -- orchestrator-injected Task directives with YAML-defined triggers
9. **Consensus Detection** -- detect agent agreement, advance to synthesis early or inject disruption
10. **GUID-based Agent Identity** -- UUID4 per agent, stable across renames and version history
11. **Agent Workshop** -- optional FastAPI + htmx web UI for agent creation, tuning, and group composition

---

## Session Lifecycle

### Input

A brief file (markdown) with:
- `## What's Already Decided` -- context the agents should respect
- `## Open Questions` -- numbered questions to discuss

### Execution

For each question in the brief:

1. **Round-start assembly** (per agent, parallel)
   - Load agent identity from YAML config (static, ~2k tokens)
   - Build situation context: decisions ledger + previous design doc (~3-5k tokens)
   - Build task: the question + round instruction + "250 words max, stay in character" (~500 tokens)

2. **Run rounds** (sequential rounds, parallel agents within each round)
   - Round 1 (propose): proposer agents generate solutions
   - Round 2 (critique): critic agents find problems
   - Round 3 (evaluate): evaluator agents assess feasibility and user impact
   - Each round's output becomes context for the next round
   - **Each completed round writes to disk immediately** (crash-safe)

3. **Synthesize** -- moderator call merges all rounds into one design doc AND produces ledger entries for this question

4. **Extract** -- single `claude -p` call extracts structured decisions and open questions from the synthesis section

5. **Persist** -- write design doc, transcript, decisions.json, open_questions.json to session folder. Append to decisions ledger. All files end with `<!-- complete -->` marker.

After all questions:

6. **Generate Morning Brief** -- assembled from structured session data (zero LLM calls)

### Output (Session Folder)

```
sessions/{session-id}/
  morning-brief.md            # Morning Brief -- what to read first
  decisions_ledger.md         # Append-only constraint log
  session_status.json         # Per-round completion status
  config-snapshot.yaml        # Copy of team config used
  eval/                       # Evaluation scores (if run)
    eval_dimensions.yaml      # Rubric version used
    scores.json               # Per-dimension scores
    suggested_followups.md    # Low-score-driven follow-up questions
  q01-{topic}/
    design-doc.md             # Synthesized design document
    transcript-r1.md          # Round 1 (propose) transcript
    transcript-r2.md          # Round 2 (critique) transcript
    transcript-r3.md          # Round 3 (evaluate) transcript
    decisions.json            # Extracted decisions
    open_questions.json       # Extracted open questions
  q02-{topic}/
    ...
```

---

## Prior Context Management

Two layers of prior context enter each question's agent prompts:

### 1. Decisions Ledger (append-only)

A single file that accumulates extracted decisions from every completed question. Never edited, never truncated, never summarized.

Format per question:
```
### Q{n}: {topic tag}
- DECIDED: {terse constraint statement, max 50 words}
- DECIDED: {terse constraint statement}
- OPEN: {unresolved question or tension}
```

Expected budget: ~250 chars per question. At question 10, ~2500 chars total.

Rules:
- Decisions stated as constraints, not rationale
- If a later question supersedes an earlier decision, the later block contains the new decision; the earlier entry remains (agents infer chronological precedence)
- Ledger append is guarded against duplicates on rerun

### 2. Previous Design Doc

The full, uncompressed design doc from the immediately prior question only. Not a window of multiple docs. Not all prior docs truncated.

Total context at question 8: ~4000 chars (2500 ledger + 1500 previous doc). Well under any context limit.

---

## Decision Extraction

One `claude -p` call per question. Input: the synthesis section of the design doc only. Output: two JSON files.

### decisions.json schema

```json
[
  {
    "id": "q3-d1",
    "decision": "Use WebSocket transport, not polling",
    "commitment": "firm | recommendation | suggestion",
    "confidence": "high | medium | low",
    "resolution_status": "resolved | partially_resolved | unresolved",
    "supporting_evidence": "Quote from synthesis grounding the classification",
    "dissent": "Quote from critic round, or null",
    "source_round": "q3"
  }
]
```

### open_questions.json schema

```json
[
  {
    "id": "q3-oq1",
    "statement": "Whether to support multi-region deployment",
    "blocking": true,
    "source_round": "q3"
  }
]
```

### Commitment classification

Based on linguistic markers in the synthesis:
- **firm**: Declarative, no hedging ("we will", "the system uses")
- **recommendation**: Advisory or conditional ("should", "preferred approach")
- **suggestion**: Exploratory or deferred ("could", "worth considering")

Default on ambiguity: `suggestion` with `confidence: low`.

### Garbage handling

**Gate 1:** `json.loads()` on CLI output. If parse fails, retry once with nudge: "Your previous response was not valid JSON. Return only the JSON array." Second failure writes stub (`[]`).

**Gate 2:** Field validation. Strip entries missing required fields or with out-of-enum values. Don't fail the session over one malformed entry.

---

## Error Handling

### Core Principle: Immediate Disk Writes

Every successful LLM call writes its output to disk the moment it completes. If the process crashes after round 2 of question 4, rounds 1 and 2 are intact files on disk.

### session_status.json

Updated after each round completes. Reflects what is actually on disk:

```json
{
  "session_id": "2026-03-18_overnight",
  "questions": {
    "q3": {
      "status": "complete",
      "rounds": {
        "propose": {"status": "complete"},
        "critique": {"status": "complete"},
        "evaluate": {"status": "complete"},
        "synthesis": {"status": "complete"}
      },
      "extraction": {"status": "complete"}
    }
  }
}
```

### Timeout and Retry Policy

- **120-second wall-clock timeout** per CLI call. Hung calls are killed.
- **One retry per call** (two attempts total).
  - Rate limit (429): wait 30 seconds, retry.
  - Any other failure: retry immediately.
- No special retry counts for synthesis or any other step.

### Output Validation

A CLI call that returns but produces unparseable or off-schema output counts as a failure:
- **JSON outputs**: validate against schema, required fields, allowed enums
- **Markdown outputs**: validate non-empty and contains expected structural markers

### Failure Cascade Rules

| Failed Step | Consequence |
|---|---|
| Propose fails | Skip the entire question. Mark as `skipped`. |
| Critique fails | Save proposal. No evaluate, no synthesis. Mark as `partial`. |
| Evaluate fails | Save proposal and critique. No synthesis. Mark as `partial`. |
| Synthesis fails | Save all rounds as raw artifacts. Mark as `partial`. |
| Extraction fails | Design doc exists. Morning Brief proceeds without this question's decisions. |

### Synthesis Retry: Truncated Input

When synthesis fails its first attempt, retry with reduced payload:
- Strip the propose round entirely (critique and evaluate subsume it)
- Trim prior design doc context to immediately preceding question only
- ~40% token reduction. Pre-built before first attempt.

If both attempts fail, question is marked `partial`. No degraded output -- partial is better than fake-complete.

### Context Chaining Across Failures

Only completed design docs enter the context chain. Raw rounds from partial questions do not chain forward. The gap is noted in session_status.json but does not block forward progress.

---

## Session Recovery

### Progress Derived From Artifacts

No checkpoint file. The orchestrator scans the session folder on startup. The decisions ledger block count tells how many questions completed. Next question is `max(completed) + 1`.

### Incomplete Questions Discarded

If the process crashed mid-question, all partial output for that question is abandoned. On restart, the question runs fresh. Three `claude -p` calls plus synthesis costs seconds; diagnosing which partial artifacts are recoverable costs a state machine.

### Completion Markers

Every file ends with `<!-- complete -->`. On resume, files without this marker are treated as non-existent (truncated write from crash).

### Resume Is Normal Startup

Same command, same entry point. If the session folder exists with fewer completed questions than the brief contains: `"Session has 4/10 questions completed. Resume? [Y/n]"`. On resume, the orchestrator loads the ledger and last completed design doc as context -- identical to what the next question would have received.

---

## Morning Brief

### Generation: Assembled from Structured Data (Zero LLM Calls)

The Morning Brief is assembled programmatically from structured session artifacts — no LLM call required. Source data: `decisions_ledger.md`, all `decisions.json` and `open_questions.json` files, `session_status.json`.

### Format

```markdown
# Morning Brief — {session-id}

## Decisions Made
- [Q1] Decision text (confidence: medium)
- [Q2] Decision text
...

## Risk Flags
Decisions where dissent was recorded but not resolved. Includes the
dissent quote and source question.

## Open Questions Requiring Human Input
Unresolved items that block downstream work. Source question noted.

## Session Gaps
- Q6: Skipped. Propose failed on both attempts.
- Q8: Partial. Critique failed. Proposal saved as raw artifact.

## Recommended Reading Order
1. q03-{topic}/ — most decisions, highest confidence
2. q01-{topic}/ — foundational constraints
...
```

### Assembly Rules

- **Decisions**: pulled from all `decisions.json` files, sorted by source_round. Append `(confidence: {level})` if medium or low. Omit if high.
- **Risk Flags**: decisions where `dissent` field is non-null. Show decision + dissent excerpt.
- **Open Questions**: all items from `open_questions.json` where `blocking: true`, then non-blocking.
- **Session Gaps**: pulled from `session_status.json` where status is `skipped` or `partial`.
- **Recommended Reading Order**: sort question folders by decision count × average confidence score, descending.

### Verification Pass

Count decisions across all `decisions.json` vs decisions in morning brief. If >20% divergence, prepend: `NOTE: This summary may be incomplete. Review decisions files directly.`

### Fallback

If assembly fails (e.g. all decisions.json files are missing or malformed): concatenate raw decisions ledger entries into flat markdown. Header: `## Morning Brief (fallback -- structured assembly failed)`. Ugly but complete.

---

## Evaluation (Built-in Feedback Loop)

### One Dimension Per Eval Call

Each scoring dimension gets its own `claude -p` call. The prompt contains one artifact, one dimension definition, a 1-5 rubric with behavioral anchors, and an instruction to output `SCORE: {1-5}` with one sentence of justification.

### Static Rubric File

`eval_dimensions.yaml` defines every dimension: name, definition, five behavioral anchors (one per score level). Adding a dimension = adding a YAML block.

Rubric anchors must include concrete failure indicators for low scores, not only success descriptions for high ones.

### Score Extraction

Scores extracted by regex (`SCORE: {1-5}`). Failed match retried up to 2 times. After that, score recorded as `null`. No heuristic reinterpretation.

### Rubric Versioning

Rubric file carries a version string. Every session's scores record which version produced them. Cross-session comparison blocked if versions differ.

### Evaluation Output

- `scores.json` -- per-dimension scores keyed to registered dimension names
- `suggested_followups.md` -- for each dimension scoring below threshold (default: 3), emit the question topic and dimension as a follow-up target. User edits before next run.

### Known Limitation

Self-evaluation bias (same model scores its own output). Documented in session metadata. Scores useful for relative ranking within a session, not absolute quality claims.

---

## Prompt Assembly

### Round-Start Prompt

| Order | Block | Budget | Source |
|-------|-------|--------|--------|
| 1 | Identity | ~2k tokens | Built from YAML agent config |
| 2 | Situation | ~3-5k tokens | Decisions ledger + previous design doc |
| 3 | Task | ~500 tokens | Question text + round instruction + perspective reminder |

### Mid-Round Context (Round 2 and 3)

| Order | Block | Budget | Source |
|-------|-------|--------|--------|
| 1 | Identity | ~2k tokens | Same as round-start |
| 2 | Situation | ~3-5k tokens | Decisions ledger + previous design doc |
| 3 | Prior Rounds | ~2-6k tokens | What proposers/critics said |
| 4 | Task | ~500 tokens | Question text + round-specific instruction |

### Token Ceiling (FR11, FR28)

**Hard limit: 4,000 tokens for the user payload** (everything except Identity). If assembly exceeds this, apply cuts in this order:

1. Drop oldest history entries from Prior Rounds (keep first 2 messages + last 10, discard middle)
2. Compress retained history (extract agent name + first sentence per turn)
3. Truncate previous design doc to summary section only
4. Truncate decisions ledger to most recent 5 entries only

Never truncate the Task block. Never truncate Identity.

### History Windowing

For sessions with >12 prior round messages, apply windowing before inclusion:
- **Keep**: first 2 messages (anchors the question context) + last 10 messages (most recent discourse)
- **Drop**: everything in between, replaced with `[{n} earlier messages omitted]`
- Applied per-agent — each agent's view window is computed independently

---

## Agent Configuration

V1 uses the existing YAML team config format (`beta-agents.yaml`). No changes needed.

### GUID-Based Agent Identity

Each agent has a UUID4 identifier assigned at creation. The GUID is stable across renames and version history.

**Storage**: `config/agents/{guid}.yaml` — one file per agent. The `beta-agents.yaml` team file references agents by GUID.

```yaml
# config/agents/3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c.yaml
guid: 3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
name: Cognitive Architect
version: 3
# ... rest of agent config
```

**Session output** references agents by GUID in all JSON artifacts (decisions.json, scores.json). Human-readable names appear in transcripts and design docs for readability.

**Groups** (team configs) reference agents by GUID:

```yaml
# config/teams/beta-agents.yaml
agents:
  - guid: 3f7a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
  - guid: ...
```

Rename an agent → update name in their YAML file only. All historical session output remains consistent.

### Experiment Modes

- `default` -- 6 agents, 3 rounds
- `compete` -- competitive vs minimalist proposers
- `ideas` -- Idea Merchant + Cognitive Architect proposing
- `ideas_compete` -- Idea Merchant vs Flow Orchestrator (minimalist)
- Others as defined

### Agent Roles per Round

| Round | Job | Agents (default mode) |
|-------|-----|----------------------|
| Propose | Generate solutions | Cognitive Architect, Flow Orchestrator |
| Critique | Find problems | Systems Pragmatist, Adversarial Critic |
| Evaluate | Assess value/feasibility | Product Oracle, Context Surgeon |
| Synthesize | Merge into design doc + extract ledger entries | Neutral moderator |

---

## Cognitive Action System (FR23-26)

YAML-defined behaviors that the orchestrator injects into agent prompts at configured intervals. Allows tuning agent behavior without editing Python.

### Action Definition

```yaml
# In agent YAML config
cognitive_actions:
  - id: memory_consolidation
    trigger: periodic
    every_n_turns: 5
    instruction: |
      Before responding, briefly note (in brackets) the 2-3 most important
      things established so far that are relevant to your response.
  - id: position_check
    trigger: round_based
    on_rounds: [critique, evaluate]
    instruction: |
      Before your critique, explicitly state which part of the proposal
      you find strongest. Then attack what you find weakest.
  - id: opening_statement
    trigger: once_per_question
    instruction: |
      Open with a single sentence that commits your initial position.
      Do not hedge.
```

### Trigger Types

| Trigger | Fires when... |
|---------|--------------|
| `periodic` | Turn count % `every_n_turns` == 0 |
| `round_based` | Current round name matches `on_rounds` list |
| `once_per_question` | First turn of each question only |

### Injection Rules

- **Max 1 action per turn** — if multiple triggers fire, pick highest-priority (round_based > once_per_question > periodic)
- **Max 200 tokens** — truncate instruction at 200 tokens if longer
- **Placement**: injected into Task layer immediately before the base round directive
- No extra LLM call — pure prompt injection

---

## Consensus Detection & Disruption (FR15-16)

Detects when agents are converging on agreement and either advances early or injects friction.

### Detection Algorithm

After each round completes, scan all responses for agreement signals:

**Keyword matching** — count occurrences of:
- Agreement: "agree", "right", "exactly", "good point", "I think {prior agent} has it"
- Stance: extract the first declarative sentence per response

**Consensus threshold**: 2+ agents expressing agreement in the same round, for 2+ consecutive rounds = consensus detected.

No extra LLM call. String matching only.

### Response: After Minimum Rounds Threshold

If consensus detected AND minimum rounds already completed:
- Skip remaining rounds
- Advance directly to synthesis
- Log: `consensus_detected: early_synthesis at round {n}`

### Response: Before Minimum Rounds Threshold

If consensus detected AND minimum rounds not yet reached:
- Inject disruption prompt into next round's Task layer:

```
CONSENSUS ALERT: All agents appear to be converging on a single answer.
This may be premature. Before your response, identify the strongest
argument AGAINST the emerging consensus. If you genuinely agree after
considering the counterargument, state why the counterargument fails.
```

- Log: `consensus_detected: disruption_injected at round {n}`

### Configuration

```yaml
# config/defaults.yaml
consensus:
  min_rounds_before_advance: 2   # don't advance before round 2
  agreement_keyword_threshold: 2  # agreements per round to count
  consecutive_rounds_required: 2  # rounds in a row before triggering
```

---

## Agent Workshop (FR57+)

Optional web UI for agent creation, tuning, and group composition. Not required for V1 core session runner — ships as a separate entry point.

### Stack

- **Backend**: FastAPI on `localhost:8420`
- **Frontend**: htmx + Pico CSS (no build step, single HTML file per view)
- **Storage**: reads/writes to `config/agents/{guid}.yaml` and `config/teams/*.yaml` directly

### File Structure

```
projects/workshop/
  main.py               # FastAPI app entry point
  routers/
    agents.py           # Agent CRUD
    teams.py            # Team/group composition
    preview.py          # Live prompt preview
    test_run.py         # Single-turn test runner
  templates/
    index.html
    agent_edit.html
    team_edit.html
    preview.html
```

### API Surface (19 endpoints)

| Group | Endpoints |
|-------|-----------|
| Agents | GET/POST /agents, GET/PUT/DELETE /agents/{guid} |
| Teams | GET/POST /teams, GET/PUT/DELETE /teams/{name} |
| Preview | POST /preview/system-prompt, POST /preview/full-turn |
| Test Run | POST /test/single-turn, GET /test/results/{run_id} |
| Config | GET /config/defaults, PUT /config/defaults |
| Workshop | GET /workshop/health |

### Shared Components

Workshop shares `agentteam.runner.claude` (subprocess runner) and `agentteam.prompts.builder` (prompt assembly) with the session runner. No duplication.

### Start Command

```bash
python -m workshop.main         # starts on localhost:8420
python -m workshop.main --port 9000
```

---

## Implementation Plan

### Reuse from beta

- `claude_runner.py` -- async subprocess wrapper (working)
- `models.py` -- Pydantic agent config models (working)
- `prompt_builder.py` -- system prompt assembly (working)
- `run_discussion.py` -- round orchestration, synthesis, transcript formatting (working, refactor into modules)
- Agent configs in `beta-agents.yaml` (working, being tuned)

### Build new

1. **Session manager** -- creates session folder, manages session_status.json, handles resume logic, completion markers
2. **Decision extractor** -- extraction prompt, JSON validation, garbage handling, ledger append
3. **Morning Brief generator** -- brief prompt, verification pass, fallback, gap reporting
4. **Evaluation engine** -- one-call-per-dimension scorer, static rubric loader, regex extraction, suggested followups
5. **CLI entry point** -- `python -m orchestrator run brief.md --mode compete --output sessions/`

### Refactor

- Extract core orchestration loop from `run_discussion.py` into reusable module
- Add immediate disk writes after each round
- Add timeout/retry/validation wrapping around all CLI calls
- Add failure cascade logic (skip/partial/complete per question)

---

## Deferred to V2+

| Feature | Why Deferred | Design Status |
|---------|-------------|---------------|
| MCP server | Not needed until two-team separation | Directory exists, no implementation |
| Two-team communication | V1 validates with one team | Designed in PRD |
| BackgroundAgents | Need core loop working first | Fully designed (7 types specified) |
| Magnitude system | Adds complexity without proven value yet | Designed in entity model + design docs |
| Phase transitions | V1 runs one discussion, not multi-phase | Designed in turn-anatomy spec |
| Intra-team talk | Needs two-team setup | Designed in conversation brief |
| AgentMind schema | Explicitly marked V1.5 in design decisions | Designed in entity model |
| Dream/random events | Enhancement after core works | Designed in conversation brief |
| Bench system | Need more agents first | Designed in design-decisions |
| Human steering | V1 is fully autonomous | Designed in PRD |
| Automated eval gating | Need calibration data first | Designed in Q7 gap analysis |
| Design Spine (dependency graph) | Need extraction reliability data first | Designed in Q5 gap analysis |
| Cross-session comparison | Need rubric stability first | Designed in Q7 gap analysis |

---

## Open Questions (from agent discussion)

- **Exit code mapping**: What exit codes does `claude -p` produce for rate limits vs model errors? Determines retry backoff strategy. Blocking for implementation.
- **Extraction loss rate**: What percentage of constraints survive extraction into the ledger? Run beta transcripts through the scheme manually before relying on it.
- **Synthesis failure rate**: If <5%, the truncated retry mechanism rarely activates. If >20%, need targeted V2 interventions. Collect data from first production runs.
- **Structured output compliance**: How reliably does `claude -p` produce `SCORE: {1-5}` format? Measure in first real eval session.

---

## Success Criteria

V1 is done when:
1. `python -m orchestrator run brief.md` produces a session folder with design docs, transcripts, decisions ledger, and a Morning Brief
2. A 7+ question brief completes without crashing (partial questions acceptable, total crash not)
3. The Morning Brief accurately reflects extracted decisions (verification pass divergence <20%)
4. Session can be stopped and resumed from the last completed question
5. The evaluator produces stable, comparable scores using the static rubric
6. Agent personalities are distinguishable in the transcripts (evaluator personality_retention > 3/5)

---

## Source Documents

This spec was distilled from:
- Agent-generated design docs: `experiments/compete/` (round-start mechanics, state model)
- Agent-generated gap analysis: `experiments/v1-gaps/` (7 design decisions filling adversarial review gaps)
- Design specs: `docs/design_specs/` (PRD, entity model, conversation engine, turn anatomy)
- Beta system: `projects/beta-agent-interaction/` (working code proving core patterns)
