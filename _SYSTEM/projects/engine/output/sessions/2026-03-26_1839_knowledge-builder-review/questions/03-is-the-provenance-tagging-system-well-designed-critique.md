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


<!-- complete -->
