### The Product Oracle (user advocate)

## Evaluate Round — The Product Oracle

The Pragmatist won the critique round. Here's why: citation URLs are the only provenance mechanism that gives a *user* something actionable. A `ROM_VERIFIED` label tells you nothing if you can't find the ROM dump that verified it. A URL you can click. That's not a philosophy — it's the difference between a claim you can validate in 30 seconds and one you have to take on faith from an AI agent.

The depth suffix is eliminated. The Orchestrator proved it in two sentences: self-reported, unverifiable, pure cost. The Architect's proposal doesn't survive.

The Critic's second-agent challenge is also eliminated. The Pragmatist is right — LLM consensus isn't verification. It's expensive hallucination with better paperwork. And it creates a coordination overhead that will slow down the research pipeline before anyone has validated that users want more rigorous tags.

What survives the gauntlet: **tier labels as fast-scan signals + mandatory citation URLs as auditable backing + CONTRADICTED pointer to existing conflict files**.

Tier labels stay because the user needs a quick read signal when skimming the Morning Brief or a README — they shouldn't have to chase URLs to assess whether a combat formula is reliable. But any claim at `ROM_VERIFIED` or `COMMUNITY_VERIFIED` must have a citation. `INFERRED` and below get a pass — you can't cite inference. `CONTRADICTED` costs nothing because it maps to conflict files that already exist in the design.

This is the simplest thing that actually works for a real user.

## Position Summary
I advocate for tier labels retained as fast-scan signals, mandatory citation URLs for any claim `COMMUNITY_VERIFIED` or above, and the CONTRADICTED pointer adopted because it costs nothing — it maps to conflict files already in the design. I reject the depth suffix entirely (unenforceable, per the Orchestrator) and the second-agent challenge pass (LLM consensus is not verification, per the Pragmatist). The Pragmatist's proposal wins because citations are the only mechanism that gives a user something auditable; everything else is notation that optimizes internal legibility while leaving the trust problem unsolved.

### The Context Surgeon (context efficiency evaluator)

## Evaluate Round — The Context Surgeon

The Oracle's verdict is correct on direction but wrong on placement. Tier labels win. CONTRADICTED pointer wins. Citations win. But inline per-claim citation URLs are a token budget catastrophe that the Oracle didn't account for.

**The Oracle conflated human auditability with agent utility.** These files are consumed primarily by agents running as CLI subprocesses. An agent parsing a damage formula with an inline citation URL gets ~80 tokens of `https://tcrf.net/The_Magic_of_Scheherazade/ROM_dump/...` that it cannot visit, cannot verify, and must process to skip. Scale that across 71KB of specs and hundreds of claims — you've inflated context cost to solve a human verification problem.

**The fix is structural, not inline.** Citations belong in a `sources:` block at the file level, not appended per-claim. The tier label stays inline (3-15 tokens). The citation lives in the footer. Agents see signal; auditors see provenance. This is the standard information architecture solution: separate the lookup index from the lookup key.

The depth suffix stays eliminated — the Orchestrator's argument stands. The Critic's second-agent challenge stays eliminated — the Pragmatist's argument stands.

**The OBSERVED category question from the original prompt goes unaddressed by everyone.** The Architect proposed dropping it; nobody contested it. I'll contest it: OBSERVED is distinct from INFERRED. Observed = agent witnessed at runtime. Inferred = derived by reasoning. Collapsing them obscures derivation chain. Keep OBSERVED.

## Position Summary
I advocate for tier labels inline + CONTRADICTED pointer + citations in a structured file-level `sources:` block rather than per-claim inline URLs, because inline URLs bloat agent context without improving agent utility. I reject the Architect's depth suffix (unverifiable) and the Critic's second-agent challenge (LLM consensus ≠ verification). I reject the Oracle's inline citation framing specifically because it solves human auditability at agent context cost — the architecture must serve both consumers without penalizing the primary one.


<!-- complete -->
