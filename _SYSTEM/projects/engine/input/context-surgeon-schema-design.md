# Stop Extracting, Start Emitting — Schema Design for Structured Synthesis Output

## What's Already Decided

- Micro-brief input is extracted decisions OR last-500-token fallback
- The fallback exists because extraction wasn't implemented
- `extraction_failed: true` flag plus skip marker in brief for garbage handling
- Post-hoc extraction on free-form synthesis prose creates a second failure surface with no upside if the synthesis prompt is controlled
- The synthesis prompt is editable — this is a precondition, not a debate

## Open Questions

1. **Schema for decisions.json** The micro-brief template already implies: decision text, why-it-won, unresolved risk. Confidence score adds complexity — is it load-bearing or decorative? What fields does decisions.json actually need?

2. **Firm vs. recommendation vs. suggestion — is three-tier premature?** This distinction is only meaningful if something downstream consumes it differently. Does anything in V1 branch on confidence? If not, the three-tier classification is premature schema complexity. Should we collapse to two tiers: `decided` and `open`?

3. **Structured synthesis output vs. standalone extractor** If we instrument the synthesis prompt to emit a structured `## Decisions` block, questions 1 and 2 collapse into "parse that block." Question 3 becomes "what if the block is malformed or absent." Should we design a parser for structured synthesis output instead of an extractor? What's the failure mode when the block is malformed?
