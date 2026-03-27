# How could the research process be smarter about finding data?

*Generated: 2026-03-26 19:05 | Q7 | 206s | Mode: compete*

## Decisions

### 1. `verification_method` Is Added to Every UNKNOWN Tag

Every UNKNOWN tag written by a research agent must include a `verification_method` field at creation time. The researcher who surfaces an unknown knows what would resolve it — that knowledge must not be discarded.

**Required format at creation:**
```
[UNKNOWN: est 12-18] verification_method: ROM_MEMORY_WATCH | TAS_ARCHIVE | COMMUNITY_CONTACT | PLAYTHROUGH_OBSERVATION | DISASSEMBLY | GUIDE_SOURCED
```

If the researcher cannot identify a verification method, the tag must include `verification_method: UNKNOWN_METHOD` — which is itself a signal that the gap is structurally blocked, not merely unresolved.

**Rule:** UNKNOWN tags written without a `verification_method` field are considered malformed. The organizer pass treats them as conflicts requiring resolution, not as valid unknowns.

---

### 2. The Claim-Queue Architecture Is Rejected

The proposal to build a prioritized claim queue — with producers, routing logic, and method-selection heuristics — is rejected.

**Reason:** The queue requires a production layer with undefined producers and prioritization rules, and the primary verification mechanisms it proposes (emulator memory-watching, TAS archive querying) presuppose tooling infrastructure that does not exist. Agents cannot watch emulator memory or access ROM addresses. Methodology improvements that require non-existent tools are not improvements.

The wave-gate pipeline is the correct orchestration structure. It does not need a new tier.

---

### 3. TAS and Disassembly Are Source Hints, Not Pipeline Stages

TAS archives, ROM disassembly, and community Discord content are valid *hints* about where precise data might exist. They belong in the Conventions Document as researcher guidance, not as pipeline stages with defined access patterns.

**Reason:** TAS play optimizes for frame minimization and systematically subverts intended mechanics. It is a precision source for glitch behavior, not normal mechanics. Disassembly is useful for structural unknowns (does a system exist?) but requires knowing address maps — which is part of the research problem, not a precondition to it. Community Discord access is non-deterministic; servers are private, archived, or require human judgment about which rooms to read.

Researchers may consult any of these sources. None of them are mandatory verification paths.

---

### 4. `verification_method` Is the Research Blockers Instrument

The `verification_method` field is the primary mechanism by which the system surfaces research blockers for user decision-making. The Morning Brief must include a **Research Blockers** section that aggregates all open UNKNOWNs by their `verification_method` value.

**Format:**
```
Research Blockers (12 open unknowns)
  ROM_MEMORY_WATCH:          5 unknowns
  TAS_ARCHIVE:               3 unknowns
  COMMUNITY_CONTACT:         2 unknowns
  PLAYTHROUGH_OBSERVATION:   1 unknown
  UNKNOWN_METHOD:            1 unknown
```

This surfaces the user's decision clearly: whether to build tooling, contact a community, run their own observations, or defer. The `verification_method` field is the measurement wave — it does not require a separate audit pass.

---

### 5. `verification_method` Is a Context-Scoping Mechanism for Future Waves

When Wave N+1 launches an agent to resolve a specific UNKNOWN, that agent's context must be bounded by the `verification_method` hint. The task prompt includes:

- The specific UNKNOWN being resolved
- The `verification_method` tag
- The minimal system context required to recognize a valid answer

Agents do not receive the full game spec for single-unknown resolution tasks. They receive scoped context. The `verification_method` field is the mechanism that makes scoping deterministic rather than a judgment call at prompt-writing time.

**Rule:** Research tasks without a `verification_method` in scope default to full-system context, which is the expensive path. This creates a structural incentive to tag properly at creation time.

---

### 6. Prompt Deduplication Is a Template Debt Item

The "What's Already Decided" block in the current session format contains Q1–Q6 listed twice. This duplication compounds across every agent, every round, and every wave in production prompts. It is not addressed here, but it is recorded as a known template-level debt item requiring a fix before Wave 2 scaling begins.

---

### 7. What Is Not Decided Here

- Whether ROM memory-watching tooling will be built, and at what priority
- How TAS archive data should be accessed if tooling is eventually added
- The Conventions Document content (source hints, naming rules, provenance propagation rules — these were adopted in prior decisions and are not re-litigated here)
- Address map construction methodology for disassembly-based verification
- How `verification_method` values are validated at write time (linting, CI check, or convention only)
<!-- complete -->
