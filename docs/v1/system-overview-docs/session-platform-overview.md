# Session Platform

## What It Is

The Session Platform manages the lifecycle of a discussion from start to finish. It handles persistence, crash recovery, artifact collection, decision tracking, and the production of the final deliverable — the Morning Brief. It's the system's memory and its contract with the user: "You will get useful output, even if things go wrong along the way."

## Why It Exists

An 8-hour unattended discussion generates enormous amounts of intermediate output. Without a persistence layer, a crash at hour 7 loses everything. Without structured artifact collection, the user wakes up to a wall of raw transcript instead of actionable specifications.

The Session Platform exists to make overnight operation reliable and the output useful. It's the difference between "the AI talked to itself all night" and "here's your spec, here are the decisions, here's what still needs your input."

## How It Fits the System

The Session Platform wraps around the entire discussion lifecycle:

- **Receives events from Conversation Engine**: Turn completions, round completions, phase transitions
- **Persists Discussion Agent output**: Every agent response is written to disk immediately
- **Accumulates the Decision Ledger**: Append-only log of all decisions extracted from synthesis rounds
- **Produces the Morning Brief**: The user-facing summary document generated after all questions are processed
- **Enables crash recovery**: On restart, scans the session folder to determine progress and resumes from the next incomplete question
- **Snapshots configuration**: Saves team configs and brief with each session for reproducibility

## Core Responsibilities

### Session Lifecycle
A session follows this flow:
1. **Initialize**: Create timestamped session folder, snapshot config, parse brief
2. **Execute**: For each question — run rounds, synthesize, extract decisions, persist
3. **Accumulate**: Append decisions to the ledger, chain context forward
4. **Finalize**: Generate Morning Brief from accumulated decisions and open questions
5. **Close**: Write final status, mark session complete

### Persistence
Every successful LLM call is written to disk immediately. The session folder structure:
```
sessions/{session-id}/
  summary.md              # Morning Brief
  decisions_ledger.md     # Append-only decision log
  session_status.json     # Progress tracking
  config_snapshot/        # Frozen team + brief configs
  q01/
    design-doc.md         # Synthesized specification
    transcript.md         # Raw agent conversation
    decisions.json        # Extracted decisions
    open_questions.json   # Unresolved items
  q02/
    ...
```

Files end with a `<!-- complete -->` marker. Files without this marker are treated as incomplete and discarded on recovery.

### Decision Ledger
An append-only constraint log that accumulates across all questions in a session:
- Format: `### Q{N}: {topic}` with `- DECIDED:` and `- OPEN:` entries
- Never summarized, never truncated — it grows linearly and chains forward as context
- At question 10, the ledger is roughly 2,500 characters — well within token budgets
- This is the authoritative record of what the discussion concluded

### Decision Extraction
After each synthesis round, a separate LLM call extracts structured decisions:
- **Decision fields**: ID, statement, commitment level (firm/recommendation/suggestion), confidence (high/medium/low), supporting evidence, dissent, source round
- **Open question fields**: ID, statement, blocking flag, source round
- Validated with JSON parsing + field validation, with retry on failure

### Morning Brief
The final user-facing deliverable, generated from accumulated decisions and open questions:
- **Decisions Made**: What was concluded, with confidence levels
- **Risk Flags**: Items that need attention
- **Open Questions**: What the agents couldn't resolve — needs human input
- **Recommended Reading Order**: Which design docs to read first

All entries are scannable one-liners. No prose, no fluff — respect the user's time.

### Crash Recovery
Recovery is file-based, not checkpoint-based:
- On startup, scan the session folder
- Count completed design docs (those with `<!-- complete -->` markers)
- Resume from the next question
- Incomplete questions are discarded and re-run from scratch (cheaper than diagnosing partial state)

### Failure Cascade
Graceful degradation when individual LLM calls fail:
- Propose fails: Skip entire question
- Critique fails: Save proposal only
- Evaluate fails: Save proposal + critique
- Synthesis fails: Save all rounds as raw artifacts
- Synthesis retry: Strip propose round (~40% token reduction) and retry

## Key Design Constraints

- **Write-only output**: Session folders are never edited after creation — only reviewed
- **Immediate persistence**: No buffering. Every completed turn hits disk before the next one starts
- **No database**: Everything is file-based. Session folders are portable and human-readable
- **Linear context growth**: The decision ledger grows slowly enough that it never threatens token budgets
- **Reproducible**: Config snapshots mean any session can be re-run with identical parameters

## Interactions

| Component | Relationship |
|---|---|
| Conversation Engine | Emits lifecycle events (turn/round/phase complete) that Session Platform persists |
| Discussion Agents | Every agent response is persisted immediately |
| Context Management | Decision ledger feeds back as context for subsequent questions |

## Current State

V1 implements the full session lifecycle: folder creation, per-question persistence, decision extraction with validation, append-only ledger, Morning Brief generation, and file-based crash recovery. 14 experiment sessions have been run successfully. The `<!-- complete -->` marker system and failure cascade logic are production-tested.
