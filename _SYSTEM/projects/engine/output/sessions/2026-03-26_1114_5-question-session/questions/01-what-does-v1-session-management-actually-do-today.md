# What does V1 session management actually do today?

*Generated: 2026-03-26 11:22 | Q1 | 481s | Mode: compete*

## Decisions

### D1: Atomic writes for session.json (V1 blocker)

`session.json` and `session_status.json` use `File.WriteAllText` with no crash protection. A process kill mid-write produces truncated JSON that cannot be deserialized. Recovery returns null, and the session state map -- which questions were partial, skipped, or failed -- is lost. Filesystem scanning cannot reconstruct this metadata.

**Decision:** Protect all JSON manifest writes with temp-file-plus-rename. Write to `session.json.tmp`, flush, then rename to `session.json`. This is atomic on NTFS and ext4. One-line fix, not an architecture change.

**Rationale:** This is the only failure mode in V1 that is both silent and unrecoverable. Every other persistence path (round files, design docs, ledger) has completion markers. The manifest does not.

### D2: Quarantine suspicious ledger extractions with visible surfacing

The engine extracts decisions from LLM responses and appends them to the decisions ledger. The current hallucination check warns in logs but does not block or exclude suspicious extractions. Downstream consumers (Morning Brief, context chaining) use them without qualification.

**Decision:** Suspicious extractions are quarantined: excluded from downstream context and logged. The Morning Brief must surface quarantined items as a visible warning line (e.g., "Note: N decisions could not be verified and were excluded from this summary"). Users judge trustworthiness; the system does not silently degrade or silently halt.

**Rationale:** Hard-fail kills multi-hour sessions on a single bad LLM response. Silent pass-through produces unexplainably incomplete summaries. Quarantine-with-surfacing is the only option that preserves both session continuity and user trust.

### D3: Completion marker pattern is adequate for V1

The `<!-- complete -->` marker written as a separate flush after content is the backbone of crash recovery for round files, design docs, and transcripts. Concerns were raised about marker collision with LLM-generated content and lack of checksumming.

**Decision:** Retain the current marker pattern for V1 without modification. The collision scenario requires three independent failures to align (LLM produces exact byte sequence as final content, process crashes between content flush and marker flush, stale marker survives stripping). This is not a V1-blocking risk.

**Backlog:** V2 should evaluate adding a content hash to the marker (e.g., `<!-- complete:sha256:abc123 -->`) to close the integrity gap.

### D4: Ledger-to-brief desync is a known gap, not a V1 blocker

If the process crashes after writing a question's design doc but before appending its ledger entry, the design doc has a completion marker but the ledger does not reference it. The Morning Brief omits that question's decisions. The idempotency guard (checking for existing `### Q{n}:` headers) does not help because the header was never written.

**Decision:** Accept this gap for V1. The failure is detectable by comparing question output files against ledger entries. Document it as a known limitation. The fix (a ledger completion marker per question) is straightforward but not blocking because the design doc itself survives and the user can read it directly.

### D5: Discussion coherence after crash recovery is a synthesis quality problem

Recovered sessions reconstruct file state, not discussion state. Agents resumed after a crash receive reconstructed context that may diverge from the pre-crash discussion trajectory. This can produce responses that are technically valid but disconnected from what was actually discussed.

**Decision:** Accept this for V1. Context chaining already compresses prior docs to decision headings and open questions -- it is lossy by design. The question is whether "lossy but consistent" produces useful output, and V1's answer is yes. Coherence validation belongs to the synthesis layer and prompt engineering, not session management.

### D6: Unbounded round queueing is operational, not architectural

If Claude CLI responses are slow, rounds queue without backpressure. No timeout enforcement exists beyond the per-call timeout in `defaults.yaml`.

**Decision:** This is a configuration concern, not a session management concern. The existing timeout in `defaults.yaml` is the control surface. If sessions hang, users notice and intervene. Silent failures (D1, D2) take priority over visible ones.

---

## Session Lifecycle (Current Behavior)

### Creation

Three entry paths converge on a single `SessionConfig` object:

1. **Brief file** -- parse markdown, extract decided items and open questions, compute SHA256 question hashes
2. **Interactive CLI** -- prompt for topic, team, agents, mode; build config programmatically
3. **CLI args** -- `--topic`, `--team`, `--agents` flags skip interactive prompts

Question hashes serve as tamper seals. If the brief is edited between crash and resume, hash mismatch rejects the resume. This is sound.

### Execution

`SessionRunner` orchestrates the cascade:

- For each question: run propose, critique, evaluate rounds via `DiscussionEngine`
- Each round: `RoundRunner` executes agents with speaking-order control
- After all rounds: `DiscussionEngine` runs synthesis to produce the design doc
- After each question: append to decisions ledger, update session.json state
- After all questions: generate Morning Brief from ledger

Cascade error handling: propose failure skips the question entirely; critique failure saves partial results; consecutive failures across questions trigger a circuit breaker that halts the session.

### Persistence

Every output file follows the completion marker protocol:

1. Write content to file, flush
2. Append `<!-- complete -->` marker, flush separately
3. On recovery: files without markers are treated as incomplete and overwritten

Exception: `session.json` and `session_status.json` lack markers (see D1).

The decisions ledger uses append-only writes with an idempotency guard that checks for existing `### Q{n}:` headers before appending.

### Crash Recovery

On `--resume`:

1. Load `session.json` -- if corrupt or missing, fall back to filesystem scan
2. Scan question output directory for completion markers
3. Skip completed questions, restart incomplete ones from the failed round
4. Context chaining rebuilds discussion state from completed design docs (lossy)

### Output Structure

```
output/sessions/{timestamp}_{slug}/
  session.json              -- manifest (config + runtime state)
  session_status.json       -- legacy compatibility
  decisions_ledger.md       -- append-only decisions
  summary.md                -- Morning Brief
  questions/
    01-{slug}.md            -- design doc
    01-{slug}-transcript.md -- full agent transcript
    01-{slug}-propose.md    -- round responses
    01-{slug}-critique.md
    01-{slug}-evaluate.md
```

---

## Reliability Summary

| Component | Status | Notes |
|---|---|---|
| Per-file completion markers | Reliable | Sound for V1 scope |
| Question hash tamper detection | Reliable | SHA256-based, deterministic |
| Cascade error handling | Reliable | Propose/critique/evaluate failure modes are distinct and handled |
| Circuit breaker | Reliable | Consecutive failures halt session cleanly |
| Ledger idempotency guard | Reliable | Header check prevents duplicate appends |
| session.json write safety | Fragile | No crash protection; V1 blocker (D1) |
| Ledger extraction trust | Fragile | Suspicious extractions propagate silently; fix via quarantine (D2) |
| Ledger-to-brief sync | Known gap | Design doc can exist without ledger entry (D4) |
| Post-crash discussion coherence | Accepted limitation | Lossy context reconstruction by design (D5) |
<!-- complete -->
