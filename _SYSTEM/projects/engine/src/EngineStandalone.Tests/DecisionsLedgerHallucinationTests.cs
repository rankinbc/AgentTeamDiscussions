using EngineStandalone.Session;
using Xunit;

namespace EngineStandalone.Tests;

public class DecisionsLedgerHallucinationTests
{
    private const string LedgerSection = @"## Ledger

### Q1: Truncation
- DECIDED: a
- DECIDED: b
- DECIDED: c
- DECIDED: d
- DECIDED: e
- DECIDED: f
- CONTESTED: g
- OPEN: h";

    [Fact]
    public void HallucinationCheck_IgnoresTheDocsOwnLedgerHeader()
    {
        // Decisions written as bold paragraphs (no ### headings): the only ### in the doc
        // is the ledger's own header, which must not count as a doc decision.
        var designDoc = "## Decisions\n\n**Full history by default.** Because.\n\n**Drop oldest round first.**\n\n"
                        + "## Open Questions\n\n- x\n\n" + LedgerSection;

        Assert.True(DecisionsLedger.HallucinationCheck(designDoc, LedgerSection));
    }

    [Fact]
    public void HallucinationCheck_StillFlagsInflatedLedger()
    {
        var designDoc = "## Decisions\n\n### 1. Only decision\n\ntext\n\n" + LedgerSection;

        // 1 doc decision vs 7 ledger entries -> ratio 7 > 4
        Assert.False(DecisionsLedger.HallucinationCheck(designDoc, LedgerSection));
    }

    [Fact]
    public void HallucinationCheck_AcceptsProportionateLedger()
    {
        var designDoc = "## Decisions\n\n### 1. A\n### 2. B\n### 3. C\n### 4. D\n\n" + LedgerSection;

        Assert.True(DecisionsLedger.HallucinationCheck(designDoc, LedgerSection));
    }
}
