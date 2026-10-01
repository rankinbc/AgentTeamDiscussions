using EngineStandalone.Agents;
using EngineStandalone.Brief;
using EngineStandalone.Discussion;
using EngineStandalone.Telemetry;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Abstraction over single-round agent discussion execution.
/// </summary>
public interface IRoundRunner
{
    List<string> ComputeSpeakingOrder(List<string> agents, TeamConfig team);

    List<ContextSection> BuildAgentSections(
        string agentKey,
        TeamConfig team,
        Dictionary<string, string> systemPrompts,
        Question question,
        string decisions,
        string priorRounds,
        string priorSpecs,
        string openQuestions,
        string roundInstruction,
        Dictionary<string, string>? agentRoles,
        string thisRoundSoFar = "",
        string context = "");

    string BuildAgentPayload(
        string agentKey,
        TeamConfig team,
        Dictionary<string, string> systemPrompts,
        Question question,
        string decisions,
        string priorRounds,
        string priorSpecs,
        string openQuestions,
        string roundInstruction,
        Dictionary<string, string>? agentRoles,
        string thisRoundSoFar = "",
        string roundName = "",
        int questionNumber = 0,
        RoundCallbacks? callbacks = null,
        string context = "");

    Task<Dictionary<string, string>> RunRoundAsync(
        List<string> agents,
        Dictionary<string, string> systemPrompts,
        TeamConfig team,
        Question question,
        string decisions,
        string priorRounds,
        string priorSpecs,
        string openQuestions,
        int timeout,
        string roundInstruction = "",
        Dictionary<string, string>? agentRoles = null,
        bool sequential = true,
        RoundCallbacks? callbacks = null,
        string roundName = "",
        int questionNumber = 0,
        string context = "");
}
