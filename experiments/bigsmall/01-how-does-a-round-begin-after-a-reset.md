# How does a round begin after a reset?

*Generated: 2026-03-17 23:22 | Question 1 | 110s | Mode: bigsmall*

## Decisions

### D1: Canonical Round Initialization Sequence

**Status:** Agreed

The round initialization follows a fixed five-step sequence. This order is non-negotiable because each step depends on the output of the previous one.

1. **Load save file** -- Read each agent's persisted state: ideas with magnitudes, stances with magnitudes, committed decisions, and personal narrative summary.
2. **Run BackgroundAgents** -- Angels analyze history and mutate the save file directly: bump/drop idea magnitudes, plant new ideas, shift stances. Agents never see or interact with BackgroundAgents.
3. **Run intra-team talk** -- Teammates compare notes asynchronously. High-magnitude ideas get reinforced, low-magnitude ideas get challenged. Further magnitude shifts occur.
4. **Curate context** -- Deterministic pass first (drop ideas below persona-dependent archival threshold, drop resolved decisions, drop stale references), then LLM curator call compresses surviving state into the ~8-15k situation block.
5. **Assemble prompt** -- Identity block (static, ~2k) + curated situation block + task block.

**Rationale:** BackgroundAgents and intra-team talk must precede curation because the curator needs final magnitudes to decide what survives the archival threshold. Running them after curation produces stale context on arrival.

**Source:** All participants converged on this order. The Flow Orchestrator's original three-step model was correct as a skeleton but incomplete -- it collapsed steps 2 and 3 into step 1, hiding the state mutations that drive overnight drift.

---

### D2: Round-Start Task Prompt is Split from Reflection

**Status:** Agreed (with refinement)

The opening prompt does NOT combine reflection and agenda declaration in a single call. Instead:

- **Pre-pass reflection:** A cheap call where the agent runs Reflect (review ideas/stances against what happened, adjust magnitudes). Output updates the save file. This output is not included in the main conversation context.
- **Opening prompt:** "Given your current state, what matters most to you right now? What will you push for? Open the discussion."

The agent initiates rather than reacts. It looks at its post-manipulation magnitudes and decides its own agenda.

**Rationale:** Combining reflection and agenda declaration produces shallow reflection as agents rush to their agenda statement. Reflection output that nobody reads burns response tokens. Making reflection a pre-pass that updates state keeps the main prompt focused on actionable agenda.

**Source:** Product Oracle and Context Surgeon aligned on splitting. Adversarial Critic flagged the double-duty problem.

---

### D3: Mid-Round Turns Differ Structurally from Round-Start

**Status:** Agreed

| Dimension | Round-Start | Mid-Round |
|---|---|---|
| Curation | Full hybrid (deterministic + LLM curator) | None (append raw messages) |
| BackgroundAgents | Run before prompt | Do not run |
| Intra-team talk | Runs before prompt | Does not run |
| Task block | "What matters? What will you push for?" | "Here's what was just said. Respond." |
| Identity + Situation | Freshly assembled | Already in context window |
| Cost | Expensive (~12-19k tokens per agent before thinking) | Cheap (append and prompt) |

**Caveat:** The cheap/expensive asymmetry erodes over long rounds. After 6-8 verbose exchanges, context window pressure may require mid-round compression, which is effectively a mini-curation pass. This is a mid-round problem to solve separately; it does not change the round-start design.

**Source:** Flow Orchestrator defined the asymmetry. Systems Pragmatist flagged the erosion. Context Surgeon confirmed separation of concerns.

---

### D4: Failure Modes and Degraded Operation

**Status:** Agreed

Each step in the initialization sequence has a defined fallback:

| Step | Failure | Fallback |
|---|---|---|
| Load save file | Corrupt or missing | Agent restarts from base persona with no accumulated state. Harsh but recoverable. |
| BackgroundAgents | Agent errors or times out | No-op. The agent simply does not get nudged this round. Round continues. |
| Intra-team talk | Fails for one or more agents | Skip for affected agents. They enter the round with pre-team-talk magnitudes. |
| LLM curator call | Timeout, hallucination, or garbage output | Fall back to deterministic-only filtering. Agent loses the surprise/unexpectedness factor but the round still starts. |
| Prompt assembly | N/A (deterministic concatenation) | No realistic failure mode beyond OOM. |

**Rule:** Never stall the round. Every failure degrades gracefully to a less-intelligent but functional state. Log all fallback activations for post-run review.

**Source:** Systems Pragmatist raised the gaps. Product Oracle and Context Surgeon converged on the specific fallbacks.

---

### D5: Observability of State Mutations

**Status:** Agreed

BackgroundAgent manipulations and intra-team talk magnitude shifts must be logged and visible in session output. These steps are where overnight drift happens. If they are invisible, the user who wakes up to a stale or surprising discussion cannot diagnose why.

Each round's session output should include:
- Pre-BackgroundAgent magnitudes vs. post-BackgroundAgent magnitudes (delta log)
- Ideas planted by BackgroundAgents (with source attribution)
- Pre-team-talk magnitudes vs. post-team-talk magnitudes (delta log)
- What the curator dropped (items that fell below archival threshold)
- What the curator surfaced as unexpected/non-obvious

**Source:** Product Oracle: "Sequence matters. Observability matters more."

---

## Open Questions

### O1: Mid-Round Compression Trigger

When context window pressure forces mid-round compression, what triggers it and what gets compressed? This is acknowledged as a real concern but explicitly deferred as a mid-round problem, not a round-start problem.

### O2: Reflection Pre-Pass Token Budget

The split reflection call needs a token budget. How much thinking does the agent get for reflection before it becomes wasteful? This interacts with the three thinking routines (Reflect, Research, Strategize) -- does the pre-pass run all three or only Reflect?

### O3: BackgroundAgent Contradiction Handling

What happens when a BackgroundAgent plants an idea that contradicts a committed decision? Committed decisions are presumably immutable, but the planted idea would enter the agent's state alongside the contradictory decision. Does the curator catch this? Does the agent? Does validation happen at plant time?