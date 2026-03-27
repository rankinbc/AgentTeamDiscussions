# Transcript: Is the provenance tagging system well-designed?

*Generated: 2026-03-26 18:51*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

The provenance system has a structural flaw: it collapses two orthogonal dimensions into one linear ranking. **Source tier** (ROM, guide, community) and **derivation distance** (direct observation vs. N inference steps away) are different axes. Mashing them into a single hierarchy creates false equivalences and leaves derived-data propagation unresolved.

My proposal: keep the five source tiers but add one dimension — derivation depth.

**Tag format:** `SOURCE_TIER:DEPTH`

- `ROM_VERIFIED:0` — direct ROM data, no inference
- `ROM_VERIFIED:1` — formula derived from ROM data (one step)
- `GUIDE_SOURCED:0` — claim lifted directly from a guide
- `INFERRED:1` — one reasoning step from GUIDE_SOURCED inputs

**Propagation rule for derived data:** the output tag = weakest input tier + max depth + 1. If you combine `ROM_VERIFIED:0` with `GUIDE_SOURCED:0`, you get `GUIDE_SOURCED:1`. Clean, mechanical, no judgment calls.

**Missing category: `CONTRADICTED`.** This isn't a ranking position — it's a flag. When two same-tier sources disagree, the claim becomes `CONTRADICTED → conflicts/filename.md`. The conflict file mechanism already exists in the design; the fact itself needs a pointer back. Without this, consumers don't know a claim is actively disputed versus merely uncertain.

**Drop OBSERVED.** It's doing no work — every "observation" is either SESSION_TESTED (documented conditions, reproducible) or anecdote (= COMMUNITY_VERIFIED at best). Ambiguous tags invite inconsistent use.

The depth suffix costs almost nothing to implement and buys you traceable reasoning chains, which matters enormously when the system scales to hundreds of derived formulas.

## Position Summary
I advocate for two-dimensional provenance tags (source tier + derivation depth) with a CONTRADICTED flag for actively disputed claims, and dropping the ambiguous OBSERVED category. I reject the current single-axis linear hierarchy because it cannot represent derived data provenance without losing information about how many inference steps separate a claim from its source. The depth suffix is mechanically simple, propagates deterministically via weakest-link + max-depth rules, and scales without requiring human judgment at tag time.

### The Flow Orchestrator (mechanical flow designer)

The depth dimension has an implementation gap that makes it unworkable as proposed: **who computes the depth, and when?**

A researcher writing `ROM_VERIFIED:1` must know they're one step from the source. Fine for direct derivations. But the propagation rule — "weakest input + max depth + 1" — requires the researcher to (a) know all source tags of all inputs, and (b) correctly compute the max. At three inference steps involving four sources, that's a manual bookkeeping problem the design doesn't solve. The rule is clean on paper; the operational sequence breaks down at the write step.

There's no dependency tracking in this system. Files don't link to their inputs. Without that, the depth number is unverifiable — it's self-reported, which makes it nearly meaningless for the one case it's supposed to help: tracing derived formula provenance across hundreds of files.

If you want traceable reasoning chains, the actual mechanism is: each derived claim lists its source files explicitly. Depth becomes computable from the graph, not a manually assigned suffix. That's a different design — and a bigger one.

**What I'll take from this:** CONTRADICTED-as-pointer is correct and costs nothing. It maps directly to the existing conflict file mechanism. Add it. One flag, one file reference, done.

**What I'd cut:** the depth suffix until there's a dependency-tracking mechanism to back it. Without it, you're adding notation complexity for a guarantee you can't enforce.

The single axis isn't perfect. It's operable. That matters.

## Position Summary
I advocate for adding a CONTRADICTED pointer flag (maps to existing conflict files) and leaving the source tier ranking as a single axis. I reject the depth suffix because without explicit dependency tracking between files, depth values are self-reported and unverifiable — the operational sequence for writing them correctly doesn't exist in this design. Complexity requires justification; unenforceable notation is pure cost.

## Round: CRITIQUE

### The Adversarial Critic (adversarial reviewer)

Both proposals are debating notation complexity while ignoring the foundational failure: **provenance tags are self-reported by the same agents whose output they're rating.** An LLM researcher that found something on a GameFAQs wiki will tag it ROM_VERIFIED if the text sounds authoritative. There is no verification step, no auditor, no challenge mechanism. The entire trust hierarchy collapses to "whatever the agent felt like writing."

**Specific failures:**

1. **ROM_VERIFIED is a method claim, not a truth claim.** Wrong ROM version, emulator bug, decompiler artifact — all can produce confidently wrong ROM_VERIFIED data. The tag implies a false ceiling of certainty.

2. **INFERRED and OBSERVED are indistinguishable without process enforcement.** Both mean "I think this is true." The researcher picks the label. No mechanism exists to challenge the choice.

3. **The weakest-link propagation rule (Architect) is destructive at scale.** One INFERRED source among fifty ROM_VERIFIED sources drags the entire derived claim to INFERRED. Researchers will simply omit low-tier sources to protect their tag — hiding the contamination rather than surfacing it.

4. **CONTRADICTED pointers (Orchestrator) create stale dependency chains.** Conflict file gets resolved, renamed, or deleted. Pointer rots. Now you have a CONTRADICTED tag pointing nowhere, and no one knows if the contradiction was resolved or abandoned.

5. **Neither proposal addresses ROM version dimensionality.** NTSC vs PAL, different dumps. A claim ROM_VERIFIED for one version is actively wrong for another. The tag has no version axis.

The shared assumption — that tags reflect reality — is the design's foundation and its fatal flaw.

## Position Summary
I reject both proposals because they optimize notation while leaving the fundamental integrity problem unsolved: agents self-report their own provenance without any verification or challenge mechanism, making the entire tier hierarchy aspirational rather than enforceable. I reject the depth suffix for the Orchestrator's reasons and also reject CONTRADICTED pointers without a lifecycle model for conflict resolution. The design needs a mandatory second-agent challenge pass for any ROM_VERIFIED claim before it enters the hierarchy, or the tags are decorative.

### The Systems Pragmatist (infrastructure realist)

The Critic correctly identifies the self-reporting problem but their solution — mandatory second-agent challenge pass — just moves the hallucination one level up. Two LLMs agreeing on ROM_VERIFIED doesn't produce truth; it produces consensus. That's a more expensive failure with a better story attached.

**The shared assumption both proposals miss:** provenance tags exist to change user behavior. The question is: what decision does a user make differently based on ROM_VERIFIED vs GUIDE_SOURCED? If the answer is "they trust it more," then the system's value is proportional to tag accuracy. But at scale — 18 systems, hundreds of claims — users stop reading tags and trust the document. The tagging system creates an illusion of rigor that gets abandoned in practice, leaving the infrastructure cost without the trust benefit.

**The simpler intervention that actually works:** require citation URLs instead of tier labels. A URL is checkable. It's human-readable. It doesn't require an agent to self-assess its own methodology. GUIDE_SOURCED with no URL is unfalsifiable. GUIDE_SOURCED with `https://gamefaqs.com/nes/587803/faqs/12345` is auditable. The tier label adds nothing a citation doesn't already encode.

The Critic's ROM version dimensionality point is the most operationally concrete failure here — it's not a notation problem, it's a structural gap. A claim that's ROM_VERIFIED for a Japanese ROM is actively wrong for NTSC. Neither proposal has a field for this.

Both proposals are solving the wrong problem. The notation isn't the bottleneck; missing source references are.

## Position Summary
I advocate for replacing tier labels with mandatory citation URLs as the primary provenance mechanism, because citations are auditable where tier labels are self-assessed. I reject both the depth-suffix and CONTRADICTED-pointer proposals because they add notation complexity without fixing the underlying verification gap. I reject the Critic's second-agent challenge pass because LLM consensus is not verification — it's expensive hallucination with better paperwork.

## Round: EVALUATE

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
