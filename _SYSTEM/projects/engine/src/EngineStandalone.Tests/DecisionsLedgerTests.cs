using EngineStandalone.Session;
using Xunit;

namespace EngineStandalone.Tests;

public class DecisionsLedgerTests : IDisposable
{
    private readonly string _tempDir;

    public DecisionsLedgerTests()
    {
        _tempDir = Path.Combine(Path.GetTempPath(), $"engine-test-{Guid.NewGuid():N}");
        Directory.CreateDirectory(_tempDir);
    }

    public void Dispose()
    {
        if (Directory.Exists(_tempDir))
            Directory.Delete(_tempDir, recursive: true);
    }

    // --- T11: ExtractLedgerSection extracts ## Ledger from design doc ---

    [Fact]
    public void ExtractLedgerSection_ExtractsLedgerFromDesignDoc()
    {
        var designDoc = @"## Decisions

Some decisions here.

## Ledger

### Q1: Feature Ranking
- DECIDED: Use priority queue
- DECIDED: Limit to 10 items

## Open Questions

- How to handle overflow?
";

        var section = DecisionsLedger.ExtractLedgerSection(designDoc);

        Assert.NotNull(section);
        Assert.Contains("### Q1: Feature Ranking", section);
        Assert.Contains("- DECIDED: Use priority queue", section);
        Assert.Contains("- DECIDED: Limit to 10 items", section);
    }

    // --- T12: ExtractLedgerSection returns null when no ## Ledger header ---

    [Fact]
    public void ExtractLedgerSection_ReturnsNullWhenNoLedgerHeader()
    {
        var designDoc = @"## Decisions

Some decisions here.

## Implementation

Details here.
";

        var section = DecisionsLedger.ExtractLedgerSection(designDoc);

        Assert.Null(section);
    }

    // --- T13: HallucinationCheck passes at balanced ratio ---

    [Fact]
    public void HallucinationCheck_PassesAtBalancedRatio()
    {
        // 2 doc decisions (### headers), 2 ledger decisions → ratio 1.0
        var designDoc = "### Decision A\nDetails\n### Decision B\nDetails";
        var ledger = "- DECIDED: First thing\n- DECIDED: Second thing";

        Assert.True(DecisionsLedger.HallucinationCheck(designDoc, ledger));
    }

    // --- T14: HallucinationCheck rejects extreme ratios ---

    [Fact]
    public void HallucinationCheck_RejectsTooManyLedgerDecisions()
    {
        // 1 doc decision, 5 ledger decisions → ratio 5.0 > 4.0
        var designDoc = "### Single Decision\nDetails";
        var ledger = "- DECIDED: A\n- DECIDED: B\n- DECIDED: C\n- DECIDED: D\n- DECIDED: E";

        Assert.False(DecisionsLedger.HallucinationCheck(designDoc, ledger));
    }

    [Fact]
    public void HallucinationCheck_RejectsTooFewLedgerDecisions()
    {
        // 10 doc decisions, 1 ledger decision → ratio 0.1 < 0.2
        var designDoc = string.Join("\n",
            Enumerable.Range(1, 10).Select(i => $"### Decision {i}\nDetails"));
        var ledger = "- DECIDED: Only one";

        Assert.False(DecisionsLedger.HallucinationCheck(designDoc, ledger));
    }

    [Fact]
    public void HallucinationCheck_PassesWhenZeroDocDecisions()
    {
        // Edge: no doc decisions → returns true (can't compute ratio)
        var designDoc = "No headers here, just text.";
        var ledger = "- DECIDED: Something";

        Assert.True(DecisionsLedger.HallucinationCheck(designDoc, ledger));
    }

    // --- T15: AppendToLedger is idempotent ---

    [Fact]
    public void AppendToLedger_IdempotentSameQuestionTwice()
    {
        var sessionDir = Path.Combine(_tempDir, "session");
        Directory.CreateDirectory(sessionDir);

        var section = "### Q1: Feature Ranking\n- DECIDED: Use priority queue\n";

        DecisionsLedger.AppendToLedger(sessionDir, section, 1);
        DecisionsLedger.AppendToLedger(sessionDir, section, 1);

        var ledger = DecisionsLedger.ReadLedger(sessionDir);
        var count = ledger.Split("### Q1:").Length - 1;
        Assert.Equal(1, count);
    }

    // --- T29: ReadLedger returns empty string for missing file ---

    [Fact]
    public void ReadLedger_ReturnsEmptyForMissingFile()
    {
        var sessionDir = Path.Combine(_tempDir, "no-ledger");
        Directory.CreateDirectory(sessionDir);

        var result = DecisionsLedger.ReadLedger(sessionDir);

        Assert.Equal("", result);
    }

    // --- T30: AppendToLedger creates file on first append ---

    [Fact]
    public void AppendToLedger_CreatesFileOnFirstAppend()
    {
        var sessionDir = Path.Combine(_tempDir, "new-session");
        Directory.CreateDirectory(sessionDir);

        var section = "### Q1: Auth Flow\n- DECIDED: Use JWT\n";
        DecisionsLedger.AppendToLedger(sessionDir, section, 1);

        Assert.True(File.Exists(DecisionsLedger.GetLedgerPath(sessionDir)));
        var content = DecisionsLedger.ReadLedger(sessionDir);
        Assert.Contains("### Q1: Auth Flow", content);
        Assert.Contains("- DECIDED: Use JWT", content);
    }

    // --- T31: CreateFallbackEntry produces valid entry ---

    [Fact]
    public void CreateFallbackEntry_ProducesValidEntry()
    {
        var entry = DecisionsLedger.CreateFallbackEntry(5, "Database Sharding Strategy");

        Assert.Contains("### Q5:", entry);
        Assert.Contains("Database Sharding Strategy", entry);
        Assert.Contains("- DECIDED:", entry);
    }

    // --- T38: HallucinationCheck edge case with zero ledger decisions ---

    [Fact]
    public void HallucinationCheck_ZeroLedgerDecisionsWithDocDecisions()
    {
        // 3 doc decisions, 0 ledger decisions → ratio 0.0 < 0.2
        var designDoc = "### Decision A\n### Decision B\n### Decision C\n";
        var ledger = "No decisions here";

        Assert.False(DecisionsLedger.HallucinationCheck(designDoc, ledger));
    }

    // --- Bonus: Multiple questions all present ---

    [Fact]
    public void AppendToLedger_MultipleQuestionsAllPresent()
    {
        var sessionDir = Path.Combine(_tempDir, "multi-q");
        Directory.CreateDirectory(sessionDir);

        DecisionsLedger.AppendToLedger(sessionDir,
            "### Q1: Auth\n- DECIDED: JWT\n", 1);
        DecisionsLedger.AppendToLedger(sessionDir,
            "### Q2: Database\n- DECIDED: Postgres\n", 2);
        DecisionsLedger.AppendToLedger(sessionDir,
            "### Q3: Caching\n- DECIDED: Redis\n", 3);

        var ledger = DecisionsLedger.ReadLedger(sessionDir);
        Assert.Contains("### Q1: Auth", ledger);
        Assert.Contains("### Q2: Database", ledger);
        Assert.Contains("### Q3: Caching", ledger);
    }
}
