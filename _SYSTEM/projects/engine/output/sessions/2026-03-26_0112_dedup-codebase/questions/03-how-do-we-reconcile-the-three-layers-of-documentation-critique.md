### The Adversarial Critic (adversarial reviewer)

The Cognitive Architect's consumption-mode framing is elegant and wrong enough to be dangerous.

**Five problems before we design anything:**

**1. The "AI reconciles at read-time" assumption is false for humans too.** Developers under pressure grab the first answer. The human-tolerance argument is a just-so story that lets us defer the staleness problem indefinitely.

**2. CONCERNS.md isn't a live gate because CLAUDE.md says it is.** A citation is not enforcement. Who verifies the file was read? Nobody. It's aspirational documentation dressed as operational gating. Calling it "load-bearing" doesn't make it load-bearing.

**3. Moving CONCERNS.md to `_SYSTEM/docs/` doesn't fix staleness — it relocates it.** If the content is drifting from reality now, it will drift from reality in the new location at the same rate. Location is not the problem.

**4. The three-layer framing misses the actual fourth layer: the CLAUDE.md files themselves.** There are at minimum four CLAUDE.md files with overlapping scope. Any reconciliation policy that ignores intra-CLAUDE.md contradiction is incomplete before it starts.

**5. "Generation timestamp plus invalidation trigger" is a policy that requires someone to execute it.** Who? On what schedule? Triggered by what event detection? This is "the system will handle it" wearing a timestamp hat.

**My agenda for this round:** Before we assign ownership, we need to answer: what breaks first when these layers contradict, and who is actually maintaining each layer today? Ownership without maintenance accountability is fiction.

### The Systems Pragmatist (infrastructure realist)

The Adversarial Critic's point 2 is the load-bearing one and everything else should be sequenced behind it: **a citation is not enforcement**. The entire CLAUDE.md instruction chain is aspirational. It works when AI context loads happen to include the right files in the right order. It fails silently when they don't. You have no observability into which failure mode you're actually in on any given session.

So the reconciliation question is secondary. The primary question is: **which of these three layers is actually being read by anything, verified, and acted on?** Before designing ownership, run that audit. My guess is `.planning/codebase/` is read occasionally by humans, never reliably injected into AI context, and drifts freely. `/docs/` was generated today so it's accurate today and will be wrong in six weeks. `_SYSTEM/docs/concepts/` is the closest thing to ground truth but has no freshness signal.

**The simplest version that validates the hypothesis:** collapse to one layer. Pick `_SYSTEM/docs/` as the single authoritative location. Move CONCERNS.md there. Delete or clearly archive `.planning/codebase/` with a `generated: <date>` header and a warning that it's a point-in-time snapshot. Delete `/docs/` or redirect it with an explicit "last generated" timestamp and exclusion from any automated context injection.

The failure mode of three layers isn't contradiction — it's that nobody knows which one to trust, so everyone trusts the one they happened to open first. That's not a policy problem. That's a count problem. Reduce the count.


<!-- complete -->
