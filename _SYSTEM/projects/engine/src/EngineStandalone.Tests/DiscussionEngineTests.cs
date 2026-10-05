using EngineStandalone.Discussion;
using Xunit;

namespace EngineStandalone.Tests;

public class DiscussionEngineTests
{
    private const string Template = @"## Ledger

### Q{{ question_number }}: {{ topic_tag }}
- DECIDED: {terse constraint, max {{ max_ledger_words | default(50) }} words}
Keep each entry under {{ max_ledger_words | default(50) }} words.";

    [Fact]
    public void FillSynthesisTemplate_ReplacesAllPlaceholders()
    {
        var filled = DiscussionEngine.FillSynthesisTemplate(Template, 3, "Token storage", 40);

        Assert.Contains("### Q3: Token storage", filled);
        Assert.Contains("max 40 words", filled);
        Assert.Contains("under 40 words", filled);
        Assert.DoesNotContain("{{", filled);
        Assert.DoesNotContain("}}", filled);
    }

    [Fact]
    public void FillSynthesisTemplate_TruncatesTopicTagLikeLedgerHeader()
    {
        var title = new string('x', 80);

        var filled = DiscussionEngine.FillSynthesisTemplate(Template, 1, title, 50);

        Assert.Contains($"### Q1: {new string('x', 60)}\n", filled.Replace("\r\n", "\n"));
    }

    [Fact]
    public void FillSynthesisTemplate_HandlesPlaceholdersWithoutDefaultFilter()
    {
        var filled = DiscussionEngine.FillSynthesisTemplate("{{question_number}} {{topic_tag}} {{ max_ledger_words }}", 7, "T$1", 12);

        Assert.Equal("7 T$1 12", filled);
    }

    [Fact]
    public void FillSynthesisTemplate_RealTemplateHasNoJinjaLeft()
    {
        var baseDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", ".."));
        var path = Path.Combine(baseDir, "templates", "prompts", "synthesis.md.j2");
        if (!File.Exists(path))
            return;

        var filled = DiscussionEngine.FillSynthesisTemplate(File.ReadAllText(path), 2, "Design question", 50);

        Assert.DoesNotContain("{{", filled);
        Assert.Contains("### Q2: Design question", filled);
    }
}
