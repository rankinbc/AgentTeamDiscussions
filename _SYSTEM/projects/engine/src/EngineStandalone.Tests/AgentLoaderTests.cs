using EngineStandalone.Agents;
using Xunit;

namespace EngineStandalone.Tests;

public class AgentLoaderTests
{
    private readonly string _dataDir;

    public AgentLoaderTests()
    {
        // Use the actual data from the engine_standalone directory
        var baseDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", ".."));
        _dataDir = Path.Combine(baseDir, "data");
    }

    [Fact]
    public void LoadTeamByName_LoadsBetaAgents()
    {
        // Skip if data not available
        if (!Directory.Exists(_dataDir))
        {
            return;
        }

        // Arrange
        var loader = new AgentLoader(_dataDir);

        // Act
        var team = loader.LoadTeamByName("beta-agents");

        // Assert
        Assert.NotEmpty(team.Agents);
        Assert.True(team.Agents.ContainsKey("cognitive_architect") ||
                    team.Agents.Keys.Any(k => k.Contains("architect")));
    }

    [Fact]
    public void LoadTeamByName_AgentsHaveNames()
    {
        // Skip if data not available
        if (!Directory.Exists(_dataDir))
        {
            return;
        }

        // Arrange
        var loader = new AgentLoader(_dataDir);

        // Act
        var team = loader.LoadTeamByName("beta-agents");

        // Assert
        foreach (var agent in team.Agents.Values)
        {
            Assert.NotEmpty(agent.Name);
        }
    }

    [Fact]
    public void LoadTeamByName_AgentsHavePersonality()
    {
        // Skip if data not available
        if (!Directory.Exists(_dataDir))
        {
            return;
        }

        // Arrange
        var loader = new AgentLoader(_dataDir);

        // Act
        var team = loader.LoadTeamByName("beta-agents");

        // Assert
        foreach (var agent in team.Agents.Values)
        {
            Assert.NotNull(agent.Personality);
            Assert.InRange(agent.Personality.Assertiveness, 0, 1);
            Assert.InRange(agent.Personality.CreativityTemp, 0, 1);
        }
    }

    [Fact]
    public void LoadTeamByName_AgentsHavePosition()
    {
        // Skip if data not available
        if (!Directory.Exists(_dataDir))
        {
            return;
        }

        // Arrange
        var loader = new AgentLoader(_dataDir);

        // Act
        var team = loader.LoadTeamByName("beta-agents");

        // Assert
        foreach (var agent in team.Agents.Values)
        {
            Assert.NotNull(agent.Position);
            Assert.NotEmpty(agent.Position.Role);
        }
    }

    [Fact]
    public void ListTeams_ReturnsTeamInfo()
    {
        // Skip if data not available
        if (!Directory.Exists(_dataDir))
        {
            return;
        }

        // Arrange
        var loader = new AgentLoader(_dataDir);

        // Act
        var teams = loader.ListTeams();

        // Assert
        Assert.NotEmpty(teams);
        var (name, file, count) = teams[0];
        Assert.NotEmpty(name);
        Assert.NotEmpty(file);
        Assert.True(count > 0);
    }

    [Fact]
    public void ListAgents_ReturnsAgentInfo()
    {
        // Skip if data not available
        if (!Directory.Exists(_dataDir))
        {
            return;
        }

        // Arrange
        var loader = new AgentLoader(_dataDir);

        // Act
        var agents = loader.ListAgents();

        // Assert
        Assert.NotEmpty(agents);
        var (id, name, key, file) = agents[0];
        Assert.NotEmpty(name);
        Assert.NotEmpty(key);
        Assert.NotEmpty(file);
    }
}

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
}
