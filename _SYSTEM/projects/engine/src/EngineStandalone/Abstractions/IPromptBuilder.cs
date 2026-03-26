using EngineStandalone.Agents;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Abstraction over system prompt assembly for agents.
/// </summary>
public interface IPromptBuilder
{
    string BuildSystemPrompt(AgentConfig agent);
    string BuildPerspectiveReminder(AgentConfig agent);
    string BuildContextLens(AgentConfig agent);
    string FilterPriorRounds(string priorRounds, AgentConfig agent);
}
