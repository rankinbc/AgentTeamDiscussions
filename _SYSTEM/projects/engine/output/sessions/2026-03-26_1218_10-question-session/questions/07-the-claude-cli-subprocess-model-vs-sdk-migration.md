# The Claude CLI subprocess model vs SDK migration.

*Generated: 2026-03-26 12:43 | Q7 | 214s | Mode: compete*

## Decisions

### DECIDED: SDK Migration Ships Last, After All V2 Prompt Features Are Validated

The SDK migration (replacing Claude CLI subprocess calls with direct SDK integration) is sequenced as the final V2 work item. All prompt-architecture features — blind proposals, phase system, tiered summarization, context window eviction — ship and validate before any SDK work begins.

**Rationale:** Every decided V2 validation criterion asks whether new perspectives surfaced in output. Streaming, token counting, and cancellation change transport mechanics, not prompt content. Engineering effort belongs on features that change what agents say, not how the message is delivered.

**Sequence:**
1. Prompt output snapshots (prerequisite, already decided)
2. Blind proposals via PromptBuilder modification
3. Phase system in round orchestration
4. Tiered summarization with static budgets
5. Five paired human comparison runs
6. SDK migration (only after validation data exists)

No parallelization of SDK work with prompt features. The bandwidth cost competes with features that actually affect output quality.

---

### DECIDED: Token Measurement Uses Character-Based Heuristics With Safety Margins, Not SDK Token Counting

All V2 features requiring token awareness — context eviction, summarization triggers, identity cap enforcement — use character-count estimation with conservative padding rather than SDK `count_tokens` API calls.

**Rationale:** Anthropic's `count_tokens` is an API call requiring authentication, network round-trips, and rate-limit handling. Introducing it into prompt assembly adds a second network dependency with different failure characteristics than the Claude CLI call itself. For a solo-builder tool running fewer than 20 validation sessions, the precision gain does not justify the reliability cost.

**Heuristic approach:**
- Character count divided by 4 (approximate tokens), plus 30% safety margin
- Over-estimation evicts conservatively (wastes some context, output slightly less informed)
- Under-estimation hits Claude's context limit (visible error, pad estimate, rerun)
- Both failure modes are recoverable in minutes and immediately visible in output

**Replacement trigger:** Heuristics are replaced with precise token counting only when paired comparison data identifies budget miscalculation as a binding constraint on output quality.

---

### DECIDED: 800-Token Agent Identity Cap Is Validated Offline, Not At Runtime

The decided 800-token agent identity cap is enforced through a one-time offline measurement script run during agent authoring, not through runtime token counting.

**Rationale:** Agent YAML files are loaded at session start and cached. Their token cost is static. A script that runs `count_tokens` (or a local tokenizer approximation) against agent definitions during authoring is sufficient. This is a pre-ship validation gate, not a runtime check.

**Process:**
1. Author or modify agent YAML
2. Run validation script against agent identity content
3. Trim if over cap
4. Commit

No runtime measurement. No SDK dependency.

---

### DECIDED: Tiered Summarization Triggers On Round Boundaries, Not Token Thresholds

Tiered summarization activates at structural boundaries — round completion — rather than when a token counter crosses a threshold.

**Rationale:** Sessions run 3-7 agents across 3 rounds (9-21 LLM calls per question). Context growth is predictable from session structure. Round 2 receives summaries of Round 1 proposals. Round 3 receives summaries of Round 2 critiques. The trigger is "a round completed," not "a byte counter hit a number."

Character heuristics with padding confirm whether the summarized content fits the available budget. At five validation runs, truncation failures surface in output before any automated counter would fire.

---

### DECIDED: Context Eviction Uses Padded Character Estimates Until Data Says Otherwise

Priority-queue eviction (decided hardcoded order, last-cut to first-cut) triggers based on character-estimated context consumption with 30% safety margins.

**Rationale:** Over-eviction is the conservative failure: agents lose some context, output is slightly less informed but complete. Under-eviction is the loud failure: Claude returns an error, the cause is immediately obvious, the estimate gets padded, the session reruns. Neither failure mode is silent. Neither requires token-level precision to diagnose or recover from.

Precise token counting becomes valuable only when operating near the context boundary in production at scale — a scenario that doesn't exist during V2 validation and may not exist until well after SDK migration for other reasons.

---

### DECIDED: Partial SDK Extraction Is Not a Valid Intermediate Step

The SDK is not split into "just token counting now, full conversation API later." Token counting via `count_tokens` is an API call, not a library function. Extracting it introduces the same authentication, networking, and error-handling concerns as full SDK integration, without the benefits of streaming or cancellation.

**Rationale:** The apparent surgical precision of "extract just the tokenizer" is misleading. It creates a new network dependency in prompt assembly — the hottest path in the system — to gain measurement precision that serves infrastructure (automated quality scoring, runtime instrumentation) that is explicitly not planned for V2.

The SDK migrates as a single unit, after validation, when the full benefit set (streaming, cancellation, token telemetry, proper timeout handling) justifies the full integration cost.

---

### DECIDED: V1 Retry Mechanism Is Sufficient For V2 Validation

ClaudeRunner's existing retry mechanism for hung or failed subprocess calls is adequate through the V2 validation phase. Proper cancellation via SDK is a production reliability improvement, not a validation requirement.

**Rationale:** At five paired validation runs, a hung agent call is a minor inconvenience (kill the process, rerun). The SDK's cancellation support prevents this, but preventing a rare annoyance during a five-run validation phase does not justify accelerating a significant rewrite.

---

## Design Principles

**Effort follows output quality.** If a change doesn't alter what appears in the Morning Brief or design documents, it waits until changes that do are validated.

**Visible failures beat precise prevention.** Character heuristics that fail loudly and recoverably are preferable to precise instrumentation that adds failure modes of its own.

**Validate before instrumenting.** The decided framework is five paired human comparisons with a spreadsheet. Build for that framework, not for automated telemetry pipelines that aren't planned.

**Defer precision until data demands it.** Every heuristic in this document has an explicit replacement trigger: paired comparison data showing the heuristic is the binding constraint. Until that data exists, the heuristic stands.
<!-- complete -->
