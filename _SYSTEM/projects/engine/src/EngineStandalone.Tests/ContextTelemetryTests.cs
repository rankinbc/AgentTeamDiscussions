using System.Text.Json;
using EngineStandalone.Telemetry;
using Xunit;

namespace EngineStandalone.Tests;

public class ContextTelemetryTests : IDisposable
{
    private readonly string _tempDir;

    public ContextTelemetryTests()
    {
        _tempDir = Path.Combine(Path.GetTempPath(), $"telemetry-test-{Guid.NewGuid():N}");
        Directory.CreateDirectory(_tempDir);
    }

    public void Dispose()
    {
        if (Directory.Exists(_tempDir))
            Directory.Delete(_tempDir, recursive: true);
    }

    private static ContextSnapshot MakeSnapshot(string agentKey = "test_agent", string roundName = "propose", int questionNumber = 1)
    {
        return new ContextSnapshot
        {
            AgentKey = agentKey,
            RoundName = roundName,
            QuestionNumber = questionNumber,
            BudgetTokens = 4000,
            Sections =
            [
                new ContextSection("perspective_reminder", "You are Test Agent.", IsProtected: true),
                new ContextSection("prior_rounds", "Some prior discussion here."),
                new ContextSection("question", "What should we build?", IsProtected: true)
            ]
        };
    }

    [Fact]
    public void Record_AccumulatesSnapshots()
    {
        var telemetry = new ContextTelemetry();

        telemetry.Record(MakeSnapshot("agent_a"));
        telemetry.Record(MakeSnapshot("agent_b"));
        telemetry.Record(MakeSnapshot("agent_c"));

        // Verify by writing and reading back
        telemetry.WriteSessionStatsAsync(_tempDir).GetAwaiter().GetResult();
        var path = Path.Combine(_tempDir, "context_stats.json");
        var json = File.ReadAllText(path);
        var doc = JsonDocument.Parse(json);
        Assert.Equal(3, doc.RootElement.GetArrayLength());
    }

    [Fact]
    public async Task WriteSessionStatsAsync_WritesValidJson()
    {
        var telemetry = new ContextTelemetry();
        telemetry.Record(MakeSnapshot());

        await telemetry.WriteSessionStatsAsync(_tempDir);

        var path = Path.Combine(_tempDir, "context_stats.json");
        Assert.True(File.Exists(path));

        var json = await File.ReadAllTextAsync(path);
        var doc = JsonDocument.Parse(json);
        Assert.Equal(1, doc.RootElement.GetArrayLength());

        var entry = doc.RootElement[0];
        Assert.Equal("test_agent", entry.GetProperty("agent").GetString());
        Assert.Equal("propose", entry.GetProperty("round").GetString());
        Assert.Equal(1, entry.GetProperty("question").GetInt32());
        Assert.True(entry.GetProperty("total_tokens").GetInt32() > 0);
        Assert.Equal(4000, entry.GetProperty("budget_tokens").GetInt32());
    }

    [Fact]
    public async Task WriteSessionStatsAsync_ClearsAfterWrite()
    {
        var telemetry = new ContextTelemetry();
        telemetry.Record(MakeSnapshot());

        await telemetry.WriteSessionStatsAsync(_tempDir);

        // Second write to a different dir should produce empty (or no) file
        var tempDir2 = Path.Combine(Path.GetTempPath(), $"telemetry-test2-{Guid.NewGuid():N}");
        Directory.CreateDirectory(tempDir2);
        try
        {
            await telemetry.WriteSessionStatsAsync(tempDir2);
            var path2 = Path.Combine(tempDir2, "context_stats.json");
            Assert.False(File.Exists(path2));
        }
        finally
        {
            Directory.Delete(tempDir2, recursive: true);
        }
    }

    [Fact]
    public void LogToConsole_DoesNotThrow()
    {
        var telemetry = new ContextTelemetry();
        var snapshot = MakeSnapshot();

        // Just verify it doesn't throw — output goes to console
        var ex = Record.Exception(() => telemetry.LogToConsole(snapshot));
        Assert.Null(ex);
    }

    [Fact]
    public void LogToConsole_WithRescueActions_DoesNotThrow()
    {
        var telemetry = new ContextTelemetry();
        var snapshot = new ContextSnapshot
        {
            AgentKey = "agent",
            RoundName = "propose",
            QuestionNumber = 1,
            BudgetTokens = 4000,
            Sections = [new ContextSection("prior_rounds", "content")],
            RescueActions = ["prior_rounds: trimmed to 50% (1200→600 tokens)"]
        };

        var ex = Record.Exception(() => telemetry.LogToConsole(snapshot));
        Assert.Null(ex);
    }
}
