using EngineStandalone.Agents;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Abstraction over agent and team YAML loading.
/// </summary>
public interface IAgentLoader
{
    AgentConfig LoadAgent(string configPath);
    AgentConfig LoadAgentByKey(string agentKey);
    TeamConfig LoadTeamByName(string teamName);
    TeamConfig LoadTeam(string configPath);
    /// <summary>Full path of the team YAML that LoadTeamByName would read.</summary>
    string ResolveTeamPath(string teamName);
    List<(string Name, string File, int AgentCount)> ListTeams();
    List<(string Id, string Name, string Key, string File)> ListAgents();
}
