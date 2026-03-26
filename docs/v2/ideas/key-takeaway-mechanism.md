# Key Takeaway Mechanism

*Findings from live agent conversations (2026-03-25) + design direction from Brian*

## Context

A 25-turn live conversation with 5 custom agents (game data pipeline team) produced genuinely productive debate but no visible conclusions. At least 5-6 convergence moments were buried in prose, never formalized. An agent conceded a key point around turn 8 but nobody recorded it. By turn 20, agents were re-deriving conclusions they had already reached because those conclusions were not in context. A human post-hoc analysis was required to extract 7 confirmed takeaways, 3 unresolved disagreements, and a prioritized action list.

The rolling synthesis feature failed to parse in all 3 attempts, producing no usable output. Even if it had worked, it would have produced a summary, not a set of confirmed decisions with agent buy-in.

Brian proposed a Key Takeaway mechanism: agents propose conclusions, all agents vote, confirmed takeaways enter shared state and compress the conversation that produced them. A second conversation with the beta agents (7 agents, designed to improve this system) debated the mechanism design across two 25-turn sessions.

---

## The Problem

The conversation engine has no mechanism for recognizing, recording, or acting on productive conclusions as they happen. Conclusions are invisible until post-hoc analysis. This causes three failures:

1. **Re-derivation waste** -- Agents re-argue settled points because the conclusion is not in context
2. **Context bloat** -- History that should be compressible remains in full because there is no structured replacement for it
3. **Invisible output** -- A human cannot tell what was decided without reading the full transcript or commissioning an AI summary

---

## Design Decisions

### Takeaway Lifecycle

A Key Takeaway moves through five states: **proposed**, **voting**, **confirmed**, **challenged**, **dead**. The orchestrator manages all state transitions. Agents never see vote arithmetic or internal mechanism state -- they see only resolved outcomes.

#### 1. Proposal

An agent proposes a Key Takeaway alongside their regular conversation message. The proposal is a concise statement of what was concluded. Proposals are a free action -- they do not consume a turn.

The proposal trigger is in the agent's instructions, not a background process. The agent recognizes convergence and formalizes it. This respects the "thermostat vs diary" principle from agent-behavior-mechanisms.md: agents act on instructions, not on introspection about their internal state.

**Open question:** What prevents premature proposals (before genuine debate) or performative proposals (obvious statements proposed to "win" confirmation)? The anti-slop mechanisms (agreement tax, perspective enforcement) apply to proposals the same way they apply to conversation messages -- an agent whose personality resists premature consensus should resist premature proposals.

#### 2. Voting

All other agents vote on the proposal: 0-10 scale plus a brief reason. This happens as a **lightweight side-channel** -- separate `claude -p` calls with abbreviated context. The voter receives:

- The takeaway statement
- The 2-3 most recent messages that produced it (not full history)
- Their perspective reminder

Voting is not a conversation turn. Agents do not see each other's votes. The orchestrator collects all votes and resolves the outcome.

**Vote reason constraint:** The vote reason must address the takeaway's content. A vote of 8+ must include substantive reasoning (agreement tax applies). A vote of 3 or below must state the specific objection -- this text becomes the candidate killing blow for the tombstone if the takeaway is rejected.

**Cost:** One `claude -p` call per voter per proposal. With 5 agents voting on 1 proposal, that is 5 calls. This is acceptable if proposals are infrequent (estimated 3-5 per 25-turn session based on observed convergence patterns).

#### 3. Confirmation or Rejection

The orchestrator reads the vote tally and resolves:

- **Confirmed:** Threshold met (see Confirmation Threshold below). Takeaway enters shared state.
- **Rejected:** Threshold not met. Takeaway receives a tombstone and is marked dead.
- **There is no "pending" or "unresolved" state.** Split votes are rejected. Rationale: unresolved takeaways in shared state cost tokens every turn they persist and produce the false consensus problem the mechanism exists to prevent.

Agents never see the vote distribution. They see only the resolved outcome.

#### 4. What Happens on Confirmation

Three things happen when a takeaway is confirmed:

**a) Takeaway enters shared state** with two fields:
- The takeaway statement (text)
- A contestation scalar (computed from vote distribution -- see Contestation Scalar below)

**b) Conversation history is compressed.** The turns that produced the takeaway are replaced by the takeaway statement in the context window. This is the core benefit: 5-8 turns of argument become one sentence plus a scalar.

**Compression safety rule:** Compression is only performed on confirmed takeaways that pass threshold cleanly. The compressed history is replaced by the takeaway + scalar, not silently deleted. If a takeaway is later overturned, the compression is not reversible -- but the overturn itself becomes a new event in the transcript.

**c) Topic steering.** After confirmation, the orchestrator can prompt agents to propose the next sub-topic. This provides natural conversation flow rather than circular re-hashing of settled points.

#### 5. What Happens on Rejection

Three things happen when a takeaway is rejected:

**a) Two-field tombstone entry.** The tombstone carries two fields, written atomically at rejection time:

- **Agent-facing field:** The sharpest objection from the lowest-scoring voter, recorded verbatim from their vote reason. This is the "extinction record" -- the argument that landed the killing blow. Agents read this to avoid re-deriving the same proposal.
- **User-facing field:** A plain-language override prompt generated by the orchestrator from a fill-in-the-blank template: "Rejected because: [killing blow]. Override if: [takeaway text] applies to your idea despite this objection." This is for the Morning Brief reader who has no session context.

The two-field approach follows the "86 Protocol" pattern: the technical reason (for agents) and the table-side reason (for the user) are different translations of the same event. Neither degrades the other.

**Legibility gate (Mad Libs Test):** The killing blow must drop verbatim into the user-facing template slot and produce a coherent sentence. If the orchestrator would need to rewrite a word to make it fit, the rejection does not confirm. This is extraction, not inference -- a mechanical check with no LLM call. The template is defined by the user in config before their first run.

**Stuck-state timeout:** If a rejection fails the legibility gate and does not re-confirm within N turns (configurable, default 3), the takeaway is force-rejected. The timeout tombstone uses the highest-scored unresolved objection from the vote reasons as its killing blow, bypassing the legibility gate. Rationale: a stuck rejection sitting in shared state costs tokens every turn; force-rejection with an imperfect tombstone is cheaper than indefinite limbo.

**b) Re-raise allowed.** Any agent can re-propose the takeaway in a later turn if subsequent discussion changes the conditions. The tombstone stays visible so the re-proposal must address the killing objection.

**c) Tombstone lifecycle.** Tombstones are promoted into the phase briefing as a one-line rejection reason at phase close, then released. The tombstone does not survive phase transition -- the briefing carries the rejection forward. No pinned transcript segments, no unbounded exception lists. The briefing is the permanent record.

---

### Confirmation Threshold

**Not yet specified.** This is the most load-bearing design parameter and should be tuned empirically.

Starting point for experimentation:
- **Confirmed:** Average vote >= 7.0, no single vote below 3
- **Rejected:** Everything else

The "no single vote below 3" rule prevents false consensus where 4 agents vote 9 and 1 votes 2 -- that is a live disagreement, not a conclusion.

The threshold should be a YAML-configurable parameter, not hardcoded.

---

### Contestation Scalar

A number from 0.0 (unanimous agreement) to 1.0 (barely passed threshold) computed from the vote distribution. Lives on every confirmed takeaway in shared state.

Purpose:
- Agents see at a glance which takeaways are rock-solid versus narrowly confirmed
- The Morning Brief sorts contested takeaways first
- Drives challenge behavior (see Challenge Integration below)

Computation: standard deviation of votes, normalized to 0-1 range. High variance = high contestation.

---

### Shared State: What Agents See Each Turn

Every turn, each agent's context includes a **Takeaway Block** injected by the orchestrator:

```
=== Confirmed Takeaways ===
[1] "Citation verification should be a named pipeline stage" (contestation: 0.2)
[2] "Progression topology is the missing data layer" (contestation: 0.5)
[3] "Ship scalar-only, defer dissent fetch" (contestation: 0.7)

=== Rejected (tombstones) ===
[X] "Design pattern density should drive extraction priority"
    Killed by: "Design pattern density is a post-extraction judgment -- you cannot
    use it to prioritize extraction without already having the data."
=== End Takeaways ===
```

This replaces the conversation history that produced each takeaway. Token cost: approximately 50-100 tokens per takeaway versus 500-2000 tokens for the argument that produced it. Net savings increase as more takeaways are confirmed.

**Scaling rule:** If confirmed takeaways accumulate beyond a configurable limit, older low-contestation takeaways (scalar below 0.2) can be further compressed into a summary block. Tombstones are released at phase close (see Tombstone Lifecycle above).

---

### Re-Derivation Protection

Agents may organically re-derive a rejected takeaway without realizing it was already debated and killed -- especially after compression removes the original argument from context. This is the hardest problem the mechanism must solve.

#### Two-layer defense

**Layer 1 -- Prevention (gate check at vote stage):** When any new takeaway is proposed, the orchestrator checks the proposal text against existing tombstone summaries before opening the vote. This is a text comparison against stored tombstone fields -- no mid-run LLM call, no phrase extraction. If a match is detected, the orchestrator injects the matching tombstone into the proposer's next turn context, forcing them to either withdraw or defend the re-proposal against the killing argument.

This is imperfect. It catches direct re-proposals but may miss significantly rephrased versions of the same idea. This is an accepted tradeoff -- perfect semantic matching was evaluated and rejected as unsolvable cheaply (see Deferred: Tripwire Phrase Extraction below).

**Layer 2 -- Detection (Morning Brief flag):** The Morning Brief flags instances where agents re-debated something already settled. The orchestrator can detect this when a rejected proposal's vote reasoning matches an existing tombstone's killing blow. This costs nothing to log -- the comparison data already exists.

The Morning Brief shows: "Agents re-debated [takeaway X] which was previously rejected because [killing blow]. [N] turns were spent on this re-derivation."

This is a post-run signal, not a mid-run intervention. The user uses it to tune team configs and anti-slop settings for future runs.

#### Why cheap re-rejection beats duplicate detection

The group evaluated and rejected elaborate duplicate detection mechanisms (tripwire phrases, semantic similarity, full tombstone list injection). The pragmatic conclusion: the briefing line already arms every agent with the rejection reason, so re-proposals die in 2 turns instead of 25. The vote mechanism handles repeats without any semantic overhead. Perfect prevention is not worth the complexity cost when fast re-rejection is free.

#### Known tension

The Adversarial Critic raised a standing objection: shipping detection-after-the-fact for a mechanism whose entire value proposition is prevention is contradictory. The gate check at vote stage partially addresses this, but organic re-derivation that uses different language will bypass the gate. This is an accepted limitation of v1. If instrumentation shows re-derivation burning significant overnight turns, invest in mid-run phrase extraction (see Deferred section).

---

### Challenge Integration

The Key Takeaway mechanism interacts with the existing challenge/urgency system:

**Scalar-driven fetch.** When an agent's turn begins and any confirmed takeaway has a contestation scalar above a configurable threshold (e.g., 0.6), the orchestrator fetches the dissent vote reasons for that takeaway and includes them in that agent's context for that turn only.

This is a **named step in the turn protocol**, not implicit behavior. The orchestrator decides deterministically based on the scalar, not by parsing agent intent:

1. Turn begins
2. Orchestrator checks: any takeaway scalar > threshold?
3. If yes: fetch dissent reasons, inject into context for this turn only
4. Build rest of turn context normally
5. Agent responds

**Cost:** Dissent text is fetched on-demand (lazy loading), not stored in shared state. The cost is paid once per challenge turn, not per turn per agent. With bounded session parameters (max agents, max contested takeaways, max turns -- all YAML-configurable), the fetch count is bounded.

**Deferred for v1:** Ship scalar-only initially. If challenge quality degrades without dissent text, add the lazy-loading fetch. Instrument overturn rates by phase to detect degradation (see Instrumentation).

**Challenge via conversation.** An agent who disagrees with a confirmed takeaway can challenge it in their regular message. This triggers the existing challenge detection and urgency system -- the takeaway's proponent gets rebuttal priority.

**Citing takeaways in defense.** An agent can cite a confirmed takeaway to support their position. This is a natural conversational behavior, not a mechanism -- agents see the Takeaway Block in context and can reference it.

---

### Morning Brief Integration

The Morning Brief receives confirmed takeaways as structured input rather than mining them from transcript prose. This replaces the current ledger extraction step, which is unreliable.

Morning Brief output order:
1. **Contested takeaways first** -- sorted by contestation scalar descending. Each shows the takeaway statement and a one-line disagreement claim sourced from the lowest-scoring voter's reason.
2. **Clean takeaways** -- sorted by confirmation order.
3. **Tombstones** -- rejected ideas with the user-facing override prompt ("Rejected because X. Override if Y applies despite this objection."). Promoted from tombstone records at phase close.
4. **Re-derivation flags** -- if agents re-debated a settled/rejected topic, flag it with turn count wasted. Signal for the user to tune team config.
5. **Open threads** -- topics that were discussed but never reached a takeaway proposal.

The disagreement claim for contested takeaways and the killing blow for tombstones are both sourced from vote reasons already collected. No additional LLM call needed for the Morning Brief.

---

## What Is Explicitly Deferred

These features were discussed and intentionally cut from v1:

### Dissent Authorship Mechanism
Elaborate system for determining who writes the disagreement summary (lowest scorer, prior commitment verification, handicap principle filtering). **Cut because:** the disagreement text already exists in the vote reasons. Use the lowest scorer's reason directly. No authorship logic needed.

Prior Commitment (from prediction markets) was the most promising approach: only agents who held a diverging position *before* the takeaway was proposed qualify to author the dissent. Verification is deterministic -- check the agent's last stated position before the proposal, not their earliest. This was sound but unnecessary for v1 since raw vote reasons serve the same purpose.

### Dissent Text in Shared State
Storing full dissent vote reasons alongside every takeaway in shared state. **Cut because:** continuous runtime token cost (every agent reads it every turn). Ship scalar-only. If challenge quality degrades without dissent text, add lazy-loading fetch (scalar triggers fetch on demand).

### Per-Turn Magnitude Re-evaluation
Agents self-reporting evolving opinions on each takeaway. **Cut because:** prior finding that LLMs cannot reliably introspect on conviction across stateless calls. Feeding an agent its own previous scores produces confabulation, not introspection. If added later, compute from behavioral traces (did the agent cite the takeaway approvingly? challenge it? ignore it?) rather than self-reported scores.

### TieBreakerGhost Escalation
Using a neutral LLM call to break split votes. **Cut because:** unaccountable single call that agents cannot trace, producing false resolution of genuine disagreement. Tie-goes-to-rejection with re-raise is cheaper and more honest.

### Behavioral Residue Mining
Computing contestation from conversation behavioral traces (position reversals, hedged language) rather than vote scores. **Cut because:** the conversation history that contains the traces gets compressed after confirmation, making post-hoc mining impossible. If added, extraction must happen at compression time as a two-output operation (one takeaway, one behavioral fingerprint).

### Tripwire Phrase Extraction
Embedding 3-5 trigger phrases from each tombstone into the briefing; when any agent uses those phrases in a new proposal, the orchestrator auto-surfaces the rejection. **Cut because:** phrase extraction quality at tombstone creation determines whether the wire ever fires, with no feedback signal on silent misses. The gate check at vote stage (direct tombstone comparison) is cheaper and has no silent-miss problem, even though it catches fewer rephrased re-proposals.

Self-updating tripwires (the wire learns from its own misses) were evaluated and rejected: every miss costs the user wasted overnight turns before the wire updates, and the update requires mid-run phrase extraction which adds LLM call cost.

### Full Tombstone List Injection
Injecting all tombstones into agent context at every vote stage entry. **Cut because:** at turn 20 of an overnight run, this could be hundreds of tokens per proposal, firing on every vote regardless of relevance. Defeats the compression the takeaway mechanism was designed to provide.

---

## Failure Modes

### False Consensus Compression
**Risk:** Agents confirm a takeaway that papers over unresolved disagreement, history gets compressed, downstream phases build on false consensus nobody can trace back.
**Mitigation:** The "no single vote below 3" threshold rule. Any strong dissent blocks confirmation regardless of average score. Compressed history is replaced by takeaway + contestation scalar, not silently deleted.

### Zombie Takeaways
**Risk:** A takeaway gets rejected, history is compressed, agents re-propose it because the compressed state did not carry the killing argument.
**Mitigation:** Two-field tombstone entries with the killing blow recorded verbatim. Gate check at vote stage catches direct re-proposals. Cheap re-rejection via the vote mechanism handles rephrased versions.

### Premature Closure
**Risk:** Agents propose takeaways before genuine debate, shortcutting exploration.
**Mitigation:** Anti-slop mechanisms apply to proposals. Agents with high stubbornness and low idea_receptivity should naturally resist premature proposals. The voting threshold provides a second gate.

### Performative Voting
**Risk:** Agents rubber-stamp every proposal to avoid conflict, producing uniformly high scores.
**Mitigation:** Same anti-slop rules that apply to conversation apply to vote reasons. Agreement tax: a vote of 8+ must include substantive reasoning, not just "sounds good." Perspective enforcement: an adversarial agent should vote adversarially.

### Context Bloat from Takeaways
**Risk:** Many confirmed takeaways accumulate in shared state, replacing one form of context bloat with another.
**Mitigation:** Each takeaway is ~50-100 tokens (statement + scalar). At 10 confirmed takeaways, that is 500-1000 tokens -- far less than the 5000-20000 tokens of conversation history they replaced. Scaling rule: low-contestation takeaways compress to summary block after threshold. Tombstones release at phase close.

### Stuck Rejection State
**Risk:** A rejection fails the legibility gate (Mad Libs Test) and the takeaway sits in undefined state, costing tokens every turn while agents debate how to fix the killing blow.
**Mitigation:** Timeout-to-tombstone rule. Force-reject after N turns (configurable, default 3) using the highest-scored unresolved objection, bypassing the legibility gate. An imperfect tombstone is cheaper than indefinite limbo.

### Organic Re-Derivation
**Risk:** Agents re-derive a rejected takeaway using different language, bypassing the gate check and the tombstone.
**Mitigation (v1):** Gate check at vote stage catches direct re-proposals. Morning Brief flags re-derivation for the user. Cheap re-rejection via vote mechanism limits wasted turns to ~2 per re-derivation. Accepted limitation: significantly rephrased re-proposals will bypass the gate. If instrumentation shows this burning material overnight budget, invest in tripwire phrase extraction.

---

## Instrumentation

Ship with logging to validate design assumptions:

- **Proposal frequency** -- how many takeaways proposed per session, per agent
- **Confirmation rate** -- what percentage of proposals pass threshold
- **Re-proposal rate** -- how often rejected takeaways get re-proposed (zombie detection)
- **Re-derivation flag rate** -- how often the Morning Brief flags re-debated topics (validates whether gate check is sufficient)
- **Overturn rate by phase** -- do confirmed takeaways get challenged and overturned in later phases? (baseline for evaluating whether dissent fetch is needed)
- **Context savings** -- tokens saved by compression per confirmed takeaway
- **Morning Brief click-through** -- if UI supports it, whether users expand contested takeaway details (validates whether the disagreement claim is useful)
- **Tombstone legibility pass rate** -- what percentage of killing blows pass the Mad Libs Test on first attempt (validates template design)
- **Timeout-to-tombstone frequency** -- how often the stuck-state timeout fires (signal that the legibility gate is too strict)

---

## Relationship to Existing Specs

- **turn-anatomy.md** -- The Takeaway Block becomes a new section in the Situation layer of the three-layer context model (Identity, Situation, Task). Takeaways are situation context, not task directives.
- **design-decisions.md** -- The "signals alongside content" pattern applies: takeaway proposals are a signal the agent emits alongside their prose message. The orchestrator reads the signal; other agents see only the prose.
- **agent-behavior-mechanisms.md** -- Per-turn magnitude re-evaluation is deferred based on the finding that LLMs cannot reliably introspect on conviction. If added, use behavioral scoring (track defenses vs drops) rather than self-reported scores. The Prior Commitment pattern (verify diverging position before the proposal, not just the vote) is the recommended approach if dissent authorship is ever built.
- **rebuttal-priority.md** -- Challenge detection and urgency boost apply to takeaway challenges the same way they apply to direct agent-to-agent challenges.
