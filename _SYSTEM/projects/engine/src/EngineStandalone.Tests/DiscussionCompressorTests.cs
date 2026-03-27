using EngineStandalone.Discussion;
using Xunit;

namespace EngineStandalone.Tests;

public class DiscussionCompressorTests
{
    [Fact]
    public void ExtractPositionSummary_WithSummaryBlock_ReturnsSummaryOnly()
    {
        var response = "Some discussion content here.\n\n## Position Summary\nThis is my position.\nAnd more detail.\n\n## Other Section\nIgnored.";

        var result = DiscussionCompressor.ExtractPositionSummary(response);

        Assert.Equal("This is my position.\nAnd more detail.", result);
    }

    [Fact]
    public void ExtractPositionSummary_NoSummaryBlock_ReturnsTail()
    {
        var response = new string('x', 400) + "Last sentence content here.";

        var result = DiscussionCompressor.ExtractPositionSummary(response);

        Assert.False(string.IsNullOrEmpty(result));
        Assert.True(result.Length <= 300);
    }

    [Fact]
    public void ExtractPositionSummary_EmptyInput_ReturnsEmpty()
    {
        Assert.Equal("", DiscussionCompressor.ExtractPositionSummary(""));
    }

    [Fact]
    public void CompressToSummaries_MultipleBlocks_ExtractsSummaryPerBlock()
    {
        var discussion =
            "[PROPOSE - Agent A]\nLong proposal text.\n\n## Position Summary\nAgent A position.\n\n" +
            "[CRITIQUE - Agent B]\nLong critique text.\n\n## Position Summary\nAgent B position.\n";

        var result = DiscussionCompressor.CompressToSummaries(discussion);

        Assert.Contains("[PROPOSE - Agent A]", result);
        Assert.Contains("Agent A position.", result);
        Assert.Contains("[CRITIQUE - Agent B]", result);
        Assert.Contains("Agent B position.", result);
        Assert.DoesNotContain("Long proposal text", result);
    }

    [Fact]
    public void CompressToSummaries_EmptyInput_ReturnsEmpty()
    {
        Assert.Equal("", DiscussionCompressor.CompressToSummaries(""));
    }
}
