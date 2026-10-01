using EngineStandalone.Agents;
using EngineStandalone.Brief;
using EngineStandalone.Config;
using EngineStandalone.Discussion;
using EngineStandalone.Runner;
using EngineStandalone.Telemetry;
using Xunit;

namespace EngineStandalone.Tests;

/// <summary>
/// The brief's "## Context" section: parsed verbatim, kept out of decisions/questions,
/// and rendered as a protected prompt section the budget enforcer never trims.
/// </summary>
public class BriefContextTests
{
    private const string Brief = """
        # Resume Review

        ## What's Already Decided

        - Targeting AI-heavy roles

        ## Context

        ### Resume
        Senior engineer, 11 years.
        1. Not a question, just a numbered line in the resume
        2. Another numbered line

        ## Open Questions

        1. **Positioning** Which lane fits best?
        2. **Bullets** Which bullets are weakest?
        """;

    [Fact]
    public void ExtractContext_CapturesSectionIncludingSubheadings()
    {
        var context = BriefParser.ExtractContext(Brief);

        Assert.StartsWith("### Resume", context);
        Assert.Contains("Another numbered line", context);
        Assert.DoesNotContain("Open Questions", context);
    }

    [Fact]
    public void ExtractContext_NoSection_ReturnsEmpty()
    {
        Assert.Equal("", BriefParser.ExtractContext("# T\n\n## Open Questions\n\n1. **Q** body"));
    }

    [Fact]
    public void ParseBriefText_NumberedLinesInContext_AreNotQuestions()
    {
        var (decisions, questions) = new BriefParser().ParseBriefText(Brief);

        Assert.Equal(2, questions.Count);
        Assert.Equal("Positioning", questions[0].Title);
        Assert.DoesNotContain("Senior engineer", decisions);
    }

    [Fact]
    public void LooksLikeBrief_DetectsOpenQuestionsHeading()
    {
        Assert.True(BriefParser.LooksLikeBrief(Brief));
        Assert.False(BriefParser.LooksLikeBrief("1. How to handle auth?\n2. Sessions?"));
    }

    [Fact]
    public void BuildAgentSections_ContextIsProtectedAndSurvivesBudgetEnforcement()
    {
        var engineDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", ".."));
        var configDir = Path.Combine(engineDir, "config");
        if (!Directory.Exists(configDir)) return;

        var runner = new RoundRunner(
            new ClaudeRunner(),
            new PromptBuilder(),
            new ConfigLoader(configDir, Path.Combine(engineDir, "templates")),
            new ContextTelemetry(),
            new ContextBudgetEnforcer(4000));
        var team = new TeamConfig { Agents = { ["critic"] = new AgentConfig { Name = "Critic" } } };
        var question = new Question { Number = 1, Title = "Q", Body = "Body" };
        var bigContext = string.Join("\n", Enumerable.Repeat("resume line with plenty of detail", 600));

        var sections = runner.BuildAgentSections(
            "critic", team, new Dictionary<string, string>(), question,
            decisions: "- decided", priorRounds: new string('x', 8000), priorSpecs: "",
            openQuestions: "", roundInstruction: "", agentRoles: null, context: bigContext);

        var contextSection = Assert.Single(sections, s => s.Name == "context");
        Assert.True(contextSection.IsProtected);

        var enforcer = new ContextBudgetEnforcer(100);
        var (trimmed, _) = enforcer.Enforce(sections, enforcer.Diagnose(new ContextSnapshot { AgentKey = "critic", RoundName = "critique", QuestionNumber = 1, Sections = sections, BudgetTokens = 100 }));
        Assert.Equal(contextSection.Content, trimmed.Single(s => s.Name == "context").Content);
    }
}
