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
    List<(string Name, string File, int AgentCount)> ListTeams();
    List<(string Id, string Name, string Key, string File)> ListAgents();
}
