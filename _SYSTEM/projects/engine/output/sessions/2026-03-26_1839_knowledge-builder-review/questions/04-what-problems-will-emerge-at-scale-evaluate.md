### The Context Surgeon (context efficiency evaluator)

## Evaluate

The Pragmatist wins the critique round, and the Critic's invalidation point survives intact. Both primary proposals lose — not on vision, but on substrate.

Here's what actually breaks first from a context delivery perspective, which neither proposal addresses:

**At 1000+ files, agents cannot discover what to load.** The hierarchy solves depth-vs-precision. It does not solve *navigation*. A research agent in wave 3 of game 7 needs to know which of 800 existing files are relevant before writing anything. Without a manifest or index, the agent either loads everything (context budget blown) or loads nothing (blind writes, duplication). The folder structure is a human-readable index. Human-readable indexes do not scale to machine traversal.

**The Critic's cascade invalidation problem is real but second-order.** It only matters after you can navigate to the claim. Navigation breaks first.

**The Architect's cross-game schema fails for the stated reason** — schema ownership is unresolved — but also for a context reason: a shared vocabulary layer adds a mandatory context dependency to every agent call. Every researcher now loads game specs *plus* schema docs. That's a budget tax on every single invocation.

**The Orchestrator's "earn complexity" heuristic is correct directionally** but doesn't name the right first problem. The approval gate isn't the bottleneck. The missing file index is.

**What needs to happen next:** Design a lightweight machine-readable manifest per game — a single index file agents query before reading anything. This is the gap none of the proposals closed.

## Position Summary
I advocate for a per-game machine-readable manifest as the immediate structural gap — without it, agents at scale either blow context budgets or write blind. I reject the cross-game schema as premature coordination overhead that taxes every agent call before recurrence patterns justify it. I reject the Orchestrator's incremental framing because it defers the navigation problem that exists from wave 1.

### The Product Oracle (user advocate)

## Evaluate

The Surgeon is closest to right, but misframes the stakes. This isn't an agent context budget problem — it's a user output quality problem. When agents navigate blind, they produce duplicate and contradictory files. The user opens their game spec folder and finds three files claiming different damage formulas. That's the failure. The manifest matters because it prevents the user from inheriting a mess they have to manually untangle.

The Pragmatist's point — that markdown can't implement cascade invalidation — is technically correct and practically irrelevant for a solo builder. The prescription (relational infrastructure) costs more in configuration overhead than the disease costs in reconciliation time at this scale. A solo builder running 10 games doesn't need a knowledge graph. They need clean files they can trust. Recommending a database before validating that the flat-file system actually breaks is the exact premature sophistication I reject.

The Architect loses. A cross-game schema layer makes every research agent call more expensive — mandatory shared context — before a single recurrence pattern has been proven worth the overhead. The user experiences this as slower, more fragile waves with no visible improvement in output.

The Critic's cascade invalidation is real, but it's a second-order problem that only bites after the collection is large enough to have derived chains worth invalidating. We're not there. Solve navigation now; solve invalidation when a real derived chain gets overturned and the user feels it.

The per-game manifest is the right immediate move. It's low-config, agent-queryable, and directly protects output quality.

## Position Summary
I advocate for a per-game machine-readable manifest as the immediate priority, because preventing blind writes is the direct path to clean user-facing output. I reject the cross-game schema as premature configuration overhead that taxes every agent call before recurrence patterns earn that cost. I reject the Pragmatist's infrastructure conclusion — replacing markdown with a relational system is a solo-builder workflow killer, and the cure costs more than the disease at current scale.


<!-- complete -->
