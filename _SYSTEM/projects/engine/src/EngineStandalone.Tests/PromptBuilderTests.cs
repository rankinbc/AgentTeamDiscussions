using EngineStandalone.Agents;
using Xunit;

namespace EngineStandalone.Tests;

public class PromptBuilderTests
{
    private readonly string _dataDir;

    public PromptBuilderTests()
    {
        var baseDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", ".."));
        _dataDir = Path.Combine(baseDir, "data");
    }

    [Fact]
    public void BuildSystemPrompt_IncludesAgentName()
    {
        // Arrange
        var agent = new AgentConfig
        {
            Name = "Test Agent",
            Description = "A test agent for unit testing",
            Position = new PositionConfig { Role = "tester" }
        };
        var builder = new PromptBuilder();

        // Act
        var prompt = builder.BuildSystemPrompt(agent);

        // Assert
        Assert.Contains("Test Agent", prompt);
    }

    [Fact]
    public void BuildSystemPrompt_IncludesRole()
    {
        // Arrange
        var agent = new AgentConfig
        {
            Name = "Test Agent",
            Description = "A test agent",
            Position = new PositionConfig { Role = "critic" }
        };
        var builder = new PromptBuilder();

        // Act
        var prompt = builder.BuildSystemPrompt(agent);

        // Assert
        Assert.Contains("Critic", prompt);
    }

    [Fact]
    public void BuildPerspectiveReminder_IncludesNameAndRole()
    {
        // Arrange
        var agent = new AgentConfig
        {
            Name = "Test Agent",
            Position = new PositionConfig { Role = "proposer" },
            Technique = new TechniqueConfig { Primary = "cross_pollination" }
        };
        var builder = new PromptBuilder();

        // Act
        var reminder = builder.BuildPerspectiveReminder(agent);

        // Assert
        Assert.Contains("Test Agent", reminder);
        Assert.Contains("proposer", reminder);
        Assert.Contains("cross pollination", reminder);
    }

    [Fact]
    public void BuildContextLens_IncludesDrives()
    {
        // Arrange
        var agent = new AgentConfig
        {
            Position = new PositionConfig
            {
                Drives = new List<string> { "Drive 1", "Drive 2", "Drive 3" }
            }
        };
        var builder = new PromptBuilder();

        // Act
        var lens = builder.BuildContextLens(agent);

        // Assert
        Assert.Contains("Drive 1", lens);
        Assert.Contains("focus on", lens.ToLower());
    }

    [Fact]
    public void BuildContextLens_IncludesPushbacks()
    {
        // Arrange
        var agent = new AgentConfig
        {
            Position = new PositionConfig
            {
                PushbackOn = new List<string> { "Bad pattern 1", "Bad pattern 2" }
            }
        };
        var builder = new PromptBuilder();

        // Act
        var lens = builder.BuildContextLens(agent);

        // Assert
        Assert.Contains("Bad pattern 1", lens);
        Assert.Contains("flag", lens.ToLower());
    }

    [Fact]
    public void FilterPriorRounds_ReturnsUnchangedForHighReceptivity()
    {
        // Arrange
        var agent = new AgentConfig
        {
            Personality = new PersonalityConfig
            {
                IdeaReceptivity = 0.8,
                Patience = 0.7
            }
        };
        var builder = new PromptBuilder();
        var priorRounds = "Some prior discussion content";

        // Act
        var filtered = builder.FilterPriorRounds(priorRounds, agent);

        // Assert
        Assert.Equal(priorRounds, filtered);
    }

    [Fact]
    public void FilterPriorRounds_TruncatesForLowPatience()
    {
        // Arrange
        var agent = new AgentConfig
        {
            Personality = new PersonalityConfig
            {
                IdeaReceptivity = 0.3,
                Patience = 0.2
            }
        };
        var builder = new PromptBuilder();
        var priorRounds = new string('x', 5000); // Long prior rounds

        // Act
        var filtered = builder.FilterPriorRounds(priorRounds, agent);

        // Assert
        Assert.True(filtered.Length < priorRounds.Length);
        Assert.Contains("truncated", filtered.ToLower());
    }

    // FilterPriorRounds: when no \n[ boundary exists in trimmed text,
    // the truncated string should still start with the header and "..."
    [Fact]
    public void FilterPriorRounds_NoBoundaryFound_StartsWithHeaderAndEllipsis()
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig
        {
            Name = "TestAgent",
            Personality = new PersonalityConfig
            {
                Patience = 0.1,
                IdeaReceptivity = 0.4
            }
        };

        // 4000 chars of text with no \n[ pattern — simulates one massive agent response
        var priorRounds = new string('x', 4000);

        var result = builder.FilterPriorRounds(priorRounds, agent);

        Assert.StartsWith("[Earlier discussion truncated", result);
        Assert.Contains("...\n", result);
    }

    // FilterPriorRounds: when a \n[ boundary is at index 0 of trimmed text,
    // the seek should succeed (idx >= 0) and content should not be dropped
    [Fact]
    public void FilterPriorRounds_BoundaryAtIndexZero_IncludesContent()
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig
        {
            Name = "TestAgent",
            Personality = new PersonalityConfig
            {
                Patience = 0.1,
                IdeaReceptivity = 0.4
            }
        };

        // Build: long padding (>3000 total) so truncation fires,
        // with the last 2500 chars starting exactly with \n[
        var recentContent = "\n[Agent A]\nSome response here\n";
        var filler = new string('y', 2500 - recentContent.Length);
        var priorRounds = new string('z', 600) + filler + recentContent;

        var result = builder.FilterPriorRounds(priorRounds, agent);

        Assert.StartsWith("[Earlier discussion truncated", result);
        Assert.Contains("[Agent A]", result);
    }

    // FilterPriorRounds: header always present when truncation fires
    [Fact]
    public void FilterPriorRounds_Truncated_AlwaysHasHeader()
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig
        {
            Name = "TestAgent",
            Personality = new PersonalityConfig
            {
                Patience = 0.1,
                IdeaReceptivity = 0.4
            }
        };
        var priorRounds = "[Agent A]\nFirst response\n\n" + new string('x', 3000);

        var result = builder.FilterPriorRounds(priorRounds, agent);

        Assert.Contains("[Earlier discussion truncated", result);
    }

    // FilterPriorRounds: high patience + high receptivity agent gets full text unchanged
    [Fact]
    public void FilterPriorRounds_HighPatience_ReturnsUnchanged()
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig
        {
            Name = "HighPatience",
            Personality = new PersonalityConfig { Patience = 0.9, IdeaReceptivity = 0.8 }
        };
        var priorRounds = "Full discussion content here";

        var result = builder.FilterPriorRounds(priorRounds, agent);

        Assert.Equal(priorRounds, result);
    }

    [Theory]
    [InlineData(5, 5)]   // urgency 5 → every 5 turns
    [InlineData(1, 9)]   // urgency 1 → every 9 turns
    [InlineData(6, 5)]   // above 5 clamped to every 5 turns
    public void BuildSystemPrompt_UncomfortableIdeaQuota_IntervalMatchesFormula(int quota, int expectedInterval)
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig
        {
            Name = "TestAgent",
            AntiSlop = new AntiSlopConfig { UncomfortableIdeaQuota = quota }
        };

        var prompt = builder.BuildSystemPrompt(agent);

        Assert.Contains($"Every {expectedInterval} turns", prompt);
    }

    [Fact]
    public void BuildSystemPrompt_UncomfortableIdeaQuota_ZeroDisablesRule()
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig
        {
            Name = "TestAgent",
            AntiSlop = new AntiSlopConfig { UncomfortableIdeaQuota = 0 }
        };

        var prompt = builder.BuildSystemPrompt(agent);

        Assert.DoesNotContain("UNCOMFORTABLE IDEA QUOTA", prompt);
    }

    [Fact]
    public void BuildSystemPrompt_AlwaysContainsSelfVerification()
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig { Name = "Tester" };

        var prompt = builder.BuildSystemPrompt(agent);

        Assert.Contains("Before responding, verify", prompt);
        Assert.Contains("defaulting to generic", prompt);
    }

    [Fact]
    public void BuildSystemPrompt_WithAllergies_RendersAllergySection()
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig
        {
            Name = "Tester",
            Position = new PositionConfig
            {
                Allergies = new List<string> { "scope creep", "deferred decisions" }
            }
        };

        var prompt = builder.BuildSystemPrompt(agent);

        Assert.Contains("scope creep", prompt);
        Assert.Contains("deferred decisions", prompt);
        Assert.Contains("allergic", prompt);
    }

    [Fact]
    public void BuildSystemPrompt_EmptyAllergies_NoAllergySection()
    {
        var builder = new PromptBuilder();
        var agent = new AgentConfig { Name = "Tester" };

        var prompt = builder.BuildSystemPrompt(agent);

        Assert.DoesNotContain("allergic", prompt);
    }
}
