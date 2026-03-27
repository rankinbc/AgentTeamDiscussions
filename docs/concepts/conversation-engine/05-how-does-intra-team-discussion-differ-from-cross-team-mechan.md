# How does intra-team discussion differ from cross-team mechanically?

*Generated: 2026-03-17 21:46 | Question 5 | 174s*

The spec is ready to write -- just needs your file write permission. Here's what I synthesized from all six panel voices:

**Spec: Intra-Team vs. Cross-Team Discussion Mechanics** -- reconciled into one authoritative document.

**The core split:**
- **Cross-team** is the main event -- full curated context (~25-30k tokens), natural language appended to transcript, permanent record. The expensive path.
- **Intra-team** is a between-round processing step -- simplified context from teammate save files only (~4-6k tokens), structured magnitude deltas as output, no transcript. One LLM call per agent, 80% cheaper.

**Key decisions locked down from the panel debate:**

- **Write semantics resolved** (Adversarial Critic's demand): Deltas are additive, but each agent writes to *their own* magnitude values. Agent A finding teammate B's idea compelling bumps it in A's state, not B's. No race condition.
- **Output schema specified** (Systems Pragmatist's demand): Structured JSON -- agent ID, target idea/stance, delta value, source tag, one-sentence rationale. Parseable without a second LLM call. The schema doubles as the audit ledger entry.
- **Magnitude source tagging required** (both Pragmatist and Critic): Six valid sources (initial, discussion, background_agent, intra_team, thinking_routine, decay). Every mutation carries provenance.
- **Audit ledger added** (Product Oracle's framing): Structured log of all magnitude mutations per session. Not part of agent context -- purely for operator observability. The difference between a trustworthy tool and an abandoned black box.
- **Step 3/4 conflict acknowledged**: Thinking routines *can* override intra-team effects. This is correct behavior -- an agent reflecting may legitimately disagree with teammates. Source tags preserve the history for debugging.
- **Team size capped at 6 for V1** (Context Surgeon's scaling concern).

**Six open items flagged:** intra-team token budget per call, magnitude delta bounds, decay formula (still unresolved), save file size budget, failure handling, and V2 structured logs for team composition analysis.

File destination: `output/spec_intra_vs_cross_team_mechanics.md`