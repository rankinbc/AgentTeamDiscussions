using EngineStandalone.Agents;
using EngineStandalone.Config;
using EngineStandalone.Session;
using EngineStandalone.Types;
using Xunit;

namespace EngineStandalone.Tests;

public class SessionPreparerTests
{
    // --- ParseTopicIntoQuestions (static, no DI needed) ---

    [Fact]
    public void ParseTopic_SingleParagraph_BecomesOneQuestion()
    {
        var questions = SessionPreparer.ParseTopicIntoQuestions(
            "How should we handle authentication in the API?");

        Assert.Single(questions);
        Assert.Equal(1, questions[0].Number);
        Assert.Contains("authentication", questions[0].Title.ToLower());
    }

    [Fact]
    public void ParseTopic_NumberedList_SplitsIntoMultipleQuestions()
    {
        var text = @"1. How should tokens be stored?
Token storage is critical for security.

2. What about refresh token rotation?
We need to decide on rotation strategy.

3. Should we support OAuth2?
Third-party auth is a common requirement.";

        var questions = SessionPreparer.ParseTopicIntoQuestions(text);

        Assert.Equal(3, questions.Count);
        Assert.Equal(1, questions[0].Number);
        Assert.Equal(2, questions[1].Number);
        Assert.Equal(3, questions[2].Number);
    }

    [Fact]
    public void ParseTopic_NumberedWithParens_Splits()
    {
        var text = @"1) First question about design
2) Second question about testing";

        var questions = SessionPreparer.ParseTopicIntoQuestions(text);
        Assert.Equal(2, questions.Count);
    }

    [Fact]
    public void ParseTopic_BoldTitles_ExtractsTitle()
    {
        var text = @"1. **Token Storage** How should tokens be stored securely?
2. **Refresh Strategy** What rotation approach should we use?";

        var questions = SessionPreparer.ParseTopicIntoQuestions(text);

        Assert.Equal(2, questions.Count);
        Assert.Equal("Token Storage", questions[0].Title);
        Assert.Equal("Refresh Strategy", questions[1].Title);
    }

    // --- ExtractTitle (static, no DI needed) ---

    [Fact]
    public void ExtractTitle_BoldMarkdown_ExtractsBoldText()
    {
        var title = SessionPreparer.ExtractTitle("**Feature Ranking** How should features be prioritized?");
        Assert.Equal("Feature Ranking", title);
    }

    [Fact]
    public void ExtractTitle_FirstSentence_ExtractsUpToPeriod()
    {
        var title = SessionPreparer.ExtractTitle("How should we handle auth. There are many options to consider.");
        Assert.Equal("How should we handle auth.", title);
    }

    [Fact]
    public void ExtractTitle_QuestionMark_ExtractsUpToQuestionMark()
    {
        var title = SessionPreparer.ExtractTitle("How should tokens work? We need to decide on format and storage.");
        Assert.Equal("How should tokens work?", title);
    }

    [Fact]
    public void ExtractTitle_LongText_Truncates()
    {
        var longText = new string('a', 200);
        var title = SessionPreparer.ExtractTitle(longText);
        Assert.True(title.Length <= 80);
        Assert.EndsWith("...", title);
    }

    [Fact]
    public void ExtractTitle_ShortText_ReturnsAsIs()
    {
        var title = SessionPreparer.ExtractTitle("Short title");
        Assert.Equal("Short title", title);
    }

    // --- PrepareFromBrief (needs real config/data dirs) ---

    private static SessionPreparer? TryCreatePreparer()
    {
        var baseDir = AppDomain.CurrentDomain.BaseDirectory;
        var dataDir = Path.Combine(baseDir, "data");
        var configDir = Path.Combine(baseDir, "config");
        var templateDir = Path.Combine(baseDir, "templates");

        if (!Directory.Exists(dataDir) || !Directory.Exists(configDir))
            return null;

        var agentLoader = new AgentLoader(dataDir);
        var configLoader = new ConfigLoader(configDir, templateDir);
        return new SessionPreparer(agentLoader, configLoader);
    }

    [Fact]
    public void PrepareFromBrief_ParsesSampleBrief()
    {
        var briefPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "TestData", "sample-brief.md");
        if (!File.Exists(briefPath)) return;

        var preparer = TryCreatePreparer();
        if (preparer == null) return;

        var config = preparer.PrepareFromBrief(briefPath, team: "beta-agents", mode: "compete", timeout: 60);

        Assert.Equal("sample-brief", config.Title);
        Assert.Equal("beta-agents", config.Team);
        Assert.Equal("compete", config.Mode);
        Assert.Equal(60, config.Timeout);
        Assert.Equal(briefPath, config.Source);
        Assert.NotEmpty(config.Questions);
        Assert.NotNull(config.QuestionHash);
        Assert.Equal(SessionRunStatus.Ready, config.State.Status);
    }

    [Fact]
    public void PrepareFromArgs_SingleTopic_CreatesOneQuestion()
    {
        var preparer = TryCreatePreparer();
        if (preparer == null) return;

        var config = preparer.PrepareFromArgs(
            "Design the auth system",
            team: "beta-agents",
            mode: "default",
            timeout: 90);

        Assert.Single(config.Questions);
        Assert.Equal("beta-agents", config.Team);
        Assert.Equal("default", config.Mode);
        Assert.Equal(90, config.Timeout);
        Assert.Equal("cli-args", config.Source);
        Assert.NotNull(config.QuestionHash);
    }

    [Fact]
    public void PrepareFromArgs_NumberedTopic_SplitsQuestions()
    {
        var preparer = TryCreatePreparer();
        if (preparer == null) return;

        var config = preparer.PrepareFromArgs(
            "1. How to handle auth?\n2. How to handle sessions?",
            team: "beta-agents");

        Assert.Equal(2, config.Questions.Count);
        Assert.Equal(1, config.Questions[0].Number);
        Assert.Equal(2, config.Questions[1].Number);
    }

    [Fact]
    public void PrepareFromArgs_DefaultsApplied()
    {
        var preparer = TryCreatePreparer();
        if (preparer == null) return;

        var config = preparer.PrepareFromArgs("Some topic");

        Assert.Equal("beta-agents", config.Team);
        Assert.Equal("compete", config.Mode);
        Assert.Equal(120, config.Timeout);
    }
}
