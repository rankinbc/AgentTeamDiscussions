using EngineStandalone.Agents;
using EngineStandalone.Brief;
using EngineStandalone.Discussion;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Abstraction over multi-round discussion orchestration and synthesis.
/// </summary>
public interface IDiscussionEngine
{
    List<string> ComputeSpeakingOrder(List<string> agents, TeamConfig team);

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
        int questionNumber = 0);

    Task<string> SynthesizeAsync(
        Question question,
        Dictionary<string, Dictionary<string, string>> roundResponses,
        List<string> roundLabels,
        string decisions,
        string priorSpecs,
        string openQuestions,
        int timeout);

    string FormatTranscript(Question question, Dictionary<string, Dictionary<string, string>> roundResponses);
    List<string> ExtractOpenQuestions(string designDoc);

    Task<QuestionResult> RunQuestionAsync(
        Question question,
        TeamConfig team,
        Dictionary<string, string> systemPrompts,
        string decisions,
        string priorSpecs,
        string openQuestions,
        int timeout,
        TeamMode? mode = null);
}
