### The Cognitive Architect (creativity engine designer)

## Role-Differentiated History Compression

The question assumes all agents should see the same history. That assumption is wrong — and correcting it gives you a mechanism with real behavioral teeth.

In group creativity research (Nijstad & Stroebe, 2006), *information asymmetry* between members drives divergent thinking. When everyone holds identical priors, groups converge prematurely. The fix isn't giving everyone more history — it's giving different agents *structurally different* history based on their cognitive role.

**The proposal:** Each agent type gets a truncation strategy matched to what it actually needs to perform its function:

- **Synthesizer agents** receive a compressed arc of the full discussion — key position shifts, not raw exchanges. They need trajectory, not recency.
- **Challenger agents** receive only the last N turns, uncompressed. Their job is local contradiction-finding; full history creates anchoring bias that softens critique.
- **Domain specialists** receive the original framing prompt + latest technical claims, with middle discussion stripped. They catch drift from the original question that other agents normalize over time.

This isn't cosmetic. Challengers literally *cannot* have been convinced by arguments they haven't seen. That structural ignorance forces genuine pushback rather than performed disagreement.

**How to implement:** Tag agents with a `history_mode: [arc | window | bookends]` in their YAML config. Compression is pre-processing, not in-context instruction.

**Testable prediction:** Role-differentiated history produces higher variance in agent positions and more explicit contradiction-surfacing than uniform sliding windows given identical total token budgets.

Commit to asymmetry. Identical context is the enemy of genuine diversity.

### The Flow Orchestrator (mechanical flow designer)

## The Cognitive Architect is right about asymmetry, wrong about implementation complexity.

Three history modes sounds minimal. It isn't. Trace the sequence:

**For `arc` mode:** Discussion ends turn N → something compresses it into a "key position shifts" summary → agent receives that summary. Who does that compression? Another LLM call. That call can fail, hallucinate the arc, or add latency to every turn. You've introduced a new agent — the compressor — and called it "pre-processing."

**Cut it.** Two modes, zero summarization:

- `window`: last N turns
- `bookends`: first turn (original framing) + last M turns

Both are pure string operations. No LLM call. No failure mode beyond slicing.

The Cognitive Architect's core insight — that challengers shouldn't see the full persuasion arc — is valid and worth keeping. A challenger on `window` genuinely hasn't been convinced by arguments outside their window. That's structural ignorance by design, achieved cheaply.

The domain specialist's need (catch drift from original framing) is solved by `bookends`. The synthesizer's need for "trajectory" is the only one that requires arc summarization — and that's a deferred feature, not a v1 requirement.

**Proposed YAML field:** `history_mode: window | bookends` with configurable `window_turns` and `bookend_tail_turns`.

**Decision point that needs answering:** Truncation happens where in the sequence? My answer: at message construction time, per-agent, before the CLI call is made. The stored session file stays untruncated. That's the invariant.

Don't build the compressor until you've proven the simple version fails.


<!-- complete -->
