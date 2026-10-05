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
    public void LoadAgent_ParsesAllergies()
    {
        var path = Path.Combine(Path.GetTempPath(), $"agent-{Guid.NewGuid():N}.yaml");
        File.WriteAllText(path, @"name: Test Agent
position:
  role: tester
  intensity: 0.5
  drives:
    - find bugs
  allergies:
    - deferred decisions
    - hand-waving
");
        try
        {
            var agent = new AgentLoader(Path.GetTempPath()).LoadAgent(path);

            Assert.Equal(new List<string> { "deferred decisions", "hand-waving" }, agent.Position.Allergies);
            Assert.Contains("allergic", new PromptBuilder().BuildSystemPrompt(agent));
        }
        finally
        {
            File.Delete(path);
        }
    }

    [Fact]
    public void ResolveTeamPath_PointsIntoTeamsDir()
    {
        var loader = new AgentLoader(Path.Combine("some", "data"));

        var path = loader.ResolveTeamPath("beta-agents");

        Assert.EndsWith(Path.Combine("some", "data", "teams", "beta-agents.yaml"), path);
        Assert.True(Path.IsPathRooted(path));
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
