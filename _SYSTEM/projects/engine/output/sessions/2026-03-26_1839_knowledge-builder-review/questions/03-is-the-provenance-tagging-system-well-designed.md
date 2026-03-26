# Is the provenance tagging system well-designed?

*Generated: 2026-03-26 18:51 | Q3 | 241s | Mode: compete*

## Decisions

### 1. Tier Labels Are Retained as Inline Fast-Scan Signals

The five-tier hierarchy is kept as-is: `ROM_VERIFIED > COMMUNITY_VERIFIED > GUIDE_SOURCED > INFERRED > OBSERVED`. Labels appear inline on every factual claim. Their sole function is fast-scan signal — a user or agent skimming a README or Morning Brief should be able to assess claim reliability without chasing references. Labels are not a guarantee of truth; they are a statement of sourcing method.

The hierarchy resolves conflicts by tier: a `ROM_VERIFIED` claim takes precedence over a `GUIDE_SOURCED` claim on the same fact unless the lower-tier claim is explicitly flagged `CONTRADICTED`.

### 2. OBSERVED Is Retained as a Distinct Category

`OBSERVED` is not collapsed into `INFERRED`. The distinction is operational: `OBSERVED` means an agent witnessed behavior at runtime under documented conditions. `INFERRED` means a claim was derived by reasoning from other claims or data. Collapsing them would obscure the derivation chain and make it impossible to distinguish empirical observation from logical deduction in downstream analysis.

### 3. Citations Are Mandatory for COMMUNITY_VERIFIED and Above — Structured at File Level

Any claim tagged `COMMUNITY_VERIFIED`, `GUIDE_SOURCED`, or `ROM_VERIFIED` must have a supporting citation. `INFERRED` and `OBSERVED` are exempt — you cannot cite inference or runtime observation with a URL.

Citations are **not** appended inline per-claim. Instead, each file that contains tagged claims includes a structured `sources:` block — a footer section mapping short citation keys to full URLs or reference identifiers. Inline claims reference the citation key, not the full URL.

This separates the lookup index from the lookup key: agents see the tier signal and a short key (minimal token cost); human auditors see the full source reference in the footer. Both consumers are served without penalizing the primary agent consumer with inline URL tokens.

Example structure:
```
The base damage formula applies a 1.5× multiplier for magic weapons. [ROM_VERIFIED:src-1]

...

sources:
  src-1: https://tcrf.net/The_Magic_of_Scheherazade/combat_formulas
  src-2: https://gamefaqs.com/nes/587803/faqs/12345
```

### 4. CONTRADICTED Is Added as a Pointer Flag

When two same-tier sources disagree on a claim, the claim is tagged `CONTRADICTED` with a pointer to the relevant conflict file. This costs nothing to implement — conflict files already exist as first-class artifacts in the design. The tag does not represent a position in the trust hierarchy; it is a state flag indicating active dispute.

Format: `CONTRADICTED → conflicts/combat-damage-multiplier.md`

A claim tagged `CONTRADICTED` is not usable for downstream derivation until the conflict file is resolved and the tag is updated. The conflict file is the authoritative record of dispute state; the pointer is the entry point.

**Lifecycle rule:** when a conflict file is resolved, the researcher who resolves it must update all `CONTRADICTED` pointers referencing that file in the same commit. Stale pointers are a known failure mode; the mitigation is co-located update responsibility, not a technical lock.

### 5. The Depth Suffix Is Rejected

The two-dimensional tag format (`SOURCE_TIER:DEPTH`) proposed during the design session is not adopted. The depth number is self-reported by the writing agent, cannot be verified without explicit dependency tracking between files, and adds notation complexity without an enforcement mechanism. Until a dependency graph is a first-class system artifact, depth numbers would be decorative. The decision is deferred, not closed — if file-level dependency tracking is added in a later wave, depth as a derived (not self-reported) property becomes tractable.

### 6. A Second-Agent Challenge Pass Is Rejected

Mandatory verification of `ROM_VERIFIED` claims by a second agent is not adopted. LLM consensus is not verification — it is agreement between two systems with the same capability floor and the same failure modes. A second-agent pass produces more expensive hallucination with better-looking paperwork. The citation requirement (Decision 3) provides the auditable mechanism; human spot-checking against cited sources provides the actual trust floor.

### 7. ROM Version Is an Open Structural Gap

A `ROM_VERIFIED` claim is implicitly scoped to the ROM version the researching agent accessed. A claim verified against a Japanese ROM may be actively incorrect for NTSC. Neither the tag format nor the citation structure currently captures version scope. This is a known gap. Interim mitigation: researchers must note the ROM version (dump identifier or region/revision) in the file-level `sources:` block entry for any `ROM_VERIFIED` citation. A structured version field on the tag itself is deferred to a future design pass.

### 8. Propagation Rule for Derived Claims

When a derived claim combines inputs from multiple source tiers, the output tag inherits the weakest input tier. No depth suffix is appended. The citation key in the inline tag references the sources block entries for all contributing inputs, comma-separated.

Example: a formula derived from one `ROM_VERIFIED` source and one `GUIDE_SOURCED` source is tagged `GUIDE_SOURCED` and cites both source keys.

Researchers must not omit lower-tier sources to protect an output tag. Omission of a contributing source to inflate tag tier is the primary integrity failure mode the citation requirement exists to surface.

### 9. UNKNOWN Estimates Are Unchanged

`[UNKNOWN: est X-Y]` tags for unfindable data with plausible estimated ranges are retained as specified in the brief. No changes to this mechanism are made by this design session.
<!-- complete -->
