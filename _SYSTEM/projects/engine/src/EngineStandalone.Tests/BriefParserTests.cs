using EngineStandalone.Brief;
using Xunit;

namespace EngineStandalone.Tests;

public class BriefParserTests
{
    private readonly string _testDataDir;

    public BriefParserTests()
    {
        _testDataDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "TestData");
    }

    [Fact]
    public void ParseBrief_WithValidBrief_ReturnsDecisionsAndQuestions()
    {
        // Arrange
        var parser = new BriefParser();
        var briefPath = Path.Combine(_testDataDir, "sample-brief.md");

        // Act
        var (decisions, questions) = parser.ParseBrief(briefPath);

        // Assert
        Assert.NotEmpty(decisions);
        Assert.Contains("async processing", decisions);
        Assert.Equal(3, questions.Count);
    }

    [Fact]
    public void ParseBrief_QuestionsHaveCorrectStructure()
    {
        // Arrange
        var parser = new BriefParser();
        var briefPath = Path.Combine(_testDataDir, "sample-brief.md");

        // Act
        var (_, questions) = parser.ParseBrief(briefPath);

        // Assert
        var firstQuestion = questions[0];
        Assert.Equal(1, firstQuestion.Number);
        Assert.Equal("How should timeouts be handled?", firstQuestion.Title);
        Assert.Contains("retry automatically", firstQuestion.Body);
    }

    [Fact]
    public void ParseBriefStructured_ExtractsConstraints()
    {
        // Arrange
        var parser = new BriefParser();
        var briefPath = Path.Combine(_testDataDir, "sample-brief.md");

        // Act
        var brief = parser.ParseBriefStructured(briefPath);

        // Assert
        Assert.NotEmpty(brief.Constraints);
        Assert.Contains(brief.Constraints, c => c.Contains("async processing"));
        Assert.Contains(brief.Constraints, c => c.Contains("markdown files"));
    }

    [Fact]
    public void Slugify_WithSimpleTitle_ReturnsLowercaseSlug()
    {
        // Act
        var slug = BriefParser.Slugify("How should timeouts be handled?");

        // Assert
        Assert.Equal("how-should-timeouts-be-handled", slug);
    }

    [Fact]
    public void Slugify_WithSpecialCharacters_ReplacesWithHyphens()
    {
        // Act
        var slug = BriefParser.Slugify("What's the best approach (option A vs B)?");

        // Assert
        Assert.DoesNotContain("'", slug);
        Assert.DoesNotContain("(", slug);
        Assert.DoesNotContain(")", slug);
    }

    [Fact]
    public void Slugify_WithLongTitle_TruncatesToMaxLength()
    {
        // Arrange
        var longTitle = "This is a very long title that exceeds the maximum length limit and should be truncated";

        // Act
        var slug = BriefParser.Slugify(longTitle, maxLength: 30);

        // Assert
        Assert.True(slug.Length <= 30);
        Assert.DoesNotMatch(@"-$", slug); // Should not end with hyphen
    }

    [Fact]
    public void Slugify_WithEmptyString_ReturnsUntitled()
    {
        // Act
        var slug = BriefParser.Slugify("");

        // Assert
        Assert.Equal("untitled", slug);
    }
}
