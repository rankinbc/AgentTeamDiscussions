// RoundRunner.cs — Executes a single discussion round (propose, critique, or evaluate).
// Each round runs agents in a computed speaking order. In sequential mode, later speakers
// see what earlier speakers said, enabling incremental debate within a single round.

using System.Text;
using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Brief;
using EngineStandalone.Config;
using EngineStandalone.Runner;

namespace EngineStandalone.Discussion;

/// <summary>
/// Event hooks for the live SSE server. OnAgentStart fires when an agent begins,
/// OnAgentContext delivers the assembled prompt, OnAgentDone fires with the response and timing.
/// </summary>
public class RoundCallbacks
{
    public Action<string>? OnAgentStart { get; set; }
    public Action<string, string, string>? OnAgentContext { get; set; }
    public Action<string, string, double>? OnAgentDone { get; set; }
}

/// <summary>
/// Executes a single round of agent discussion.
/// </summary>
public class RoundRunner : IRoundRunner
{
    private readonly IClaudeRunner _claudeRunner;
    private readonly IPromptBuilder _promptBuilder;
    private readonly IConfigLoader _configLoader;

    public RoundRunner(IClaudeRunner claudeRunner, IPromptBuilder promptBuilder, IConfigLoader configLoader)
    {
        _claudeRunner = claudeRunner;
        _promptBuilder = promptBuilder;
        _configLoader = configLoader;
    }

    /// <summary>
    /// Determines who speaks first. Formula: assertiveness*0.5 + intensity*0.3 + stubbornness*0.2 + jitter.
    /// Higher-scoring agents set the agenda; later agents respond to what's been said.
    /// </summary>
    public List<string> ComputeSpeakingOrder(List<string> agents, TeamConfig team)
    {
        var random = new Random();
        var scored = new List<(string Key, double Score)>();

        foreach (var key in agents)
        {
            if (!team.Agents.TryGetValue(key, out var agent))
            {
                scored.Add((key, 0.5 + random.NextDouble() * 0.2 - 0.1));
                continue;
            }

            var p = agent.Personality;
            // Speaking priority: assertiveness * intensity, weighted by stubbornness
            var score = p.Assertiveness * 0.5 + agent.Position.Intensity * 0.3 + p.Stubbornness * 0.2;
            // Add small random jitter (+-0.1) so it's not perfectly deterministic
            score += random.NextDouble() * 0.2 - 0.1;
            scored.Add((key, score));
        }

        return scored.OrderByDescending(x => x.Score).Select(x => x.Key).ToList();
    }

    /// <summary>
    /// Assembles the Situation Layer + Task Layer for one agent's prompt. Sections in order:
    /// perspective reminder, context lens, role overlay, prior decisions, prior design docs,
    /// open questions, discussion so far, the question, round instruction, speaking position.
    /// </summary>
    public string BuildAgentPayload(
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
        string thisRoundSoFar = "")
    {
        if (!team.Agents.TryGetValue(agentKey, out var agent))
        {
            throw new ArgumentException($"Agent '{agentKey}' not found in team");
        }

        var sb = new StringBuilder();

        // Perspective reminder
        var reminder = _promptBuilder.BuildPerspectiveReminder(agent);
        sb.AppendLine(reminder);
        sb.AppendLine();

        // Agent-specific context lens
        var contextLens = _promptBuilder.BuildContextLens(agent);
        if (!string.IsNullOrEmpty(contextLens))
        {
            sb.AppendLine(contextLens);
            sb.AppendLine();
        }

        // Per-agent role overlay
        if (agentRoles != null && agentRoles.TryGetValue(agentKey, out var roleKey))
        {
            var roleText = _configLoader.OverlayInstruction(roleKey);
            if (!string.IsNullOrEmpty(roleText))
            {
                sb.AppendLine("=== Your Approach ===");
                sb.AppendLine(roleText);
                sb.AppendLine("=== End Approach ===");
                sb.AppendLine();
            }
        }

        // Decisions from brief
        if (!string.IsNullOrEmpty(decisions))
        {
            sb.AppendLine("=== What's Already Decided ===");
            sb.AppendLine(decisions);
            sb.AppendLine("=== End Decisions ===");
            sb.AppendLine();
        }

        // Prior design docs
        if (!string.IsNullOrEmpty(priorSpecs))
        {
            sb.AppendLine("=== Prior Design Docs (reference, don't contradict) ===");
            sb.AppendLine(priorSpecs);
            sb.AppendLine("=== End Prior Docs ===");
            sb.AppendLine();
        }

        // Unresolved open questions
        if (!string.IsNullOrEmpty(openQuestions))
        {
            sb.AppendLine("=== Unresolved Open Questions from Prior Docs ===");
            sb.AppendLine(openQuestions);
            sb.AppendLine("=== End Open Questions ===");
            sb.AppendLine();
            sb.AppendLine("If this question can resolve any of the above, do so.");
            sb.AppendLine();
        }

        // Context: prior rounds + what's been said THIS round so far
        var agentPriorRounds = _promptBuilder.FilterPriorRounds(priorRounds, agent);
        var combinedContext = "";
        if (!string.IsNullOrEmpty(agentPriorRounds))
        {
            combinedContext += agentPriorRounds;
        }
        if (!string.IsNullOrEmpty(thisRoundSoFar))
        {
            combinedContext += $"\n\n--- This round so far ---\n{thisRoundSoFar}";
        }
        if (!string.IsNullOrEmpty(combinedContext))
        {
            sb.AppendLine("=== Discussion So Far (this question) ===");
            sb.AppendLine(combinedContext);
            sb.AppendLine("=== End Discussion ===");
            sb.AppendLine();
        }

        // The question itself
        sb.AppendLine($"## Question: {question.Title}");
        sb.AppendLine();
        sb.AppendLine(question.Body);
        sb.AppendLine();

        // Round instruction
        if (!string.IsNullOrEmpty(roundInstruction))
        {
            sb.AppendLine(roundInstruction);
            sb.AppendLine();
        }

        // Speaking order context
        if (!string.IsNullOrEmpty(thisRoundSoFar))
        {
            sb.Append("Other agents have already spoken this round. Respond to their points directly -- disagree where you see a flaw, and be specific about why. Do not agree unless you have genuinely new evidence. 250 words max (excluding Position Summary).");
        }
        else
        {
            sb.Append("You are speaking first this round. Set the agenda. 250 words max (excluding Position Summary).");
        }

        sb.AppendLine();
        sb.AppendLine();
        sb.Append("IMPORTANT: End your response with exactly this format:\n## Position Summary\n[3 sentences: what you advocate, what you reject, and why.]");

        return sb.ToString();
    }

    /// <summary>
    /// Executes one round (propose, critique, or evaluate). Sequential mode runs agents
    /// one at a time so each sees prior speakers, building incrementally. Parallel mode
    /// fires all at once (faster but less contextual).
    /// </summary>
    public async Task<Dictionary<string, string>> RunRoundAsync(
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
        RoundCallbacks? callbacks = null)
    {
        var displayNames = _configLoader.DisplayNames();

        if (!sequential)
        {
            // Parallel mode: all agents fire at once
            var tasks = agents.Select(async agentKey =>
            {
                var payload = BuildAgentPayload(
                    agentKey, team, systemPrompts, question, decisions,
                    priorRounds, priorSpecs, openQuestions, roundInstruction,
                    agentRoles);

                var response = await _claudeRunner.RunAsync(systemPrompts[agentKey], payload, timeout);
                return (agentKey, response);
            });

            var results = await Task.WhenAll(tasks);
            return results.ToDictionary(r => r.agentKey, r => r.response);
        }

        // Sequential mode: agents speak one at a time, each seeing previous speakers
        var ordered = ComputeSpeakingOrder(agents, team);
        var responses = new Dictionary<string, string>();
        var thisRoundSoFar = "";

        foreach (var agentKey in ordered)
        {
            callbacks?.OnAgentStart?.Invoke(agentKey);

            var startTime = DateTime.UtcNow;
            var payload = BuildAgentPayload(
                agentKey, team, systemPrompts, question, decisions,
                priorRounds, priorSpecs, openQuestions, roundInstruction,
                agentRoles, thisRoundSoFar);

            callbacks?.OnAgentContext?.Invoke(agentKey, systemPrompts[agentKey], payload);

            var response = await _claudeRunner.RunAsync(systemPrompts[agentKey], payload, timeout);
            var elapsed = (DateTime.UtcNow - startTime).TotalSeconds;

            responses[agentKey] = response;

            callbacks?.OnAgentDone?.Invoke(agentKey, response, elapsed);

            // Add this agent's response to the running context for the next speaker
            var name = displayNames.TryGetValue(agentKey, out var dn) ? dn : agentKey;
            thisRoundSoFar += $"[{name}]\n{response}\n\n";
        }

        return responses;
    }
}
