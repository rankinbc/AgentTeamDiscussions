// RoundRunner.cs — Executes a single discussion round (propose, critique, or evaluate).
// Each round runs agents in a computed speaking order. In sequential mode, later speakers
// see what earlier speakers said, enabling incremental debate within a single round.

using System.Text;
using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Brief;
using EngineStandalone.Config;
using EngineStandalone.Runner;
using EngineStandalone.Telemetry;

namespace EngineStandalone.Discussion;

/// <summary>
/// Event hooks for the live SSE server. OnAgentStart fires when an agent begins,
/// OnAgentContext delivers the assembled prompt, OnAgentDone fires with the response and timing,
/// OnAgentContextStats delivers the structured context snapshot for each turn.
/// </summary>
public class RoundCallbacks
{
    public Action<string>? OnAgentStart { get; set; }
    public Action<string, string, string>? OnAgentContext { get; set; }
    public Action<string, string, double>? OnAgentDone { get; set; }
    public Action<ContextSnapshot>? OnAgentContextStats { get; set; }
}

/// <summary>
/// Executes a single round of agent discussion.
/// </summary>
public class RoundRunner : IRoundRunner
{
    private readonly IClaudeRunner _claudeRunner;
    private readonly IPromptBuilder _promptBuilder;
    private readonly IConfigLoader _configLoader;
    private readonly IContextTelemetry _telemetry;
    private readonly IContextBudgetEnforcer _enforcer;

    public RoundRunner(
        IClaudeRunner claudeRunner,
        IPromptBuilder promptBuilder,
        IConfigLoader configLoader,
        IContextTelemetry telemetry,
        IContextBudgetEnforcer enforcer)
    {
        _claudeRunner = claudeRunner;
        _promptBuilder = promptBuilder;
        _configLoader = configLoader;
        _telemetry = telemetry;
        _enforcer = enforcer;
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
    /// Builds named sections for one agent's prompt. Returns a structured list that
    /// BuildAgentPayload() measures, optionally enforces, then concatenates.
    /// </summary>
    public List<ContextSection> BuildAgentSections(
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
        string context = "")
    {
        if (!team.Agents.TryGetValue(agentKey, out var agent))
        {
            throw new ArgumentException($"Agent '{agentKey}' not found in team");
        }

        var sections = new List<ContextSection>();

        // Perspective reminder (protected — always included)
        var reminder = _promptBuilder.BuildPerspectiveReminder(agent);
        sections.Add(new ContextSection("perspective_reminder", reminder, IsProtected: true));

        // Agent-specific context lens
        var contextLens = _promptBuilder.BuildContextLens(agent);
        if (!string.IsNullOrEmpty(contextLens))
            sections.Add(new ContextSection("context_lens", contextLens));

        // Per-agent role overlay
        if (agentRoles != null && agentRoles.TryGetValue(agentKey, out var roleKey))
        {
            var roleText = _configLoader.OverlayInstruction(roleKey);
            if (!string.IsNullOrEmpty(roleText))
            {
                var roleContent = $"=== Your Approach ===\n{roleText}\n=== End Approach ===";
                sections.Add(new ContextSection("role_overlay", roleContent));
            }
        }

        // Reference material from the brief's ## Context section (protected — every agent
        // must see all of it, so the budget enforcer never trims it)
        if (!string.IsNullOrWhiteSpace(context))
        {
            var contextContent = $"=== Context (reference material for this discussion) ===\n{context}\n=== End Context ===";
            sections.Add(new ContextSection("context", contextContent, IsProtected: true));
        }

        // Decisions from brief
        if (!string.IsNullOrEmpty(decisions))
        {
            var decisionsContent = $"=== What's Already Decided ===\n{decisions}\n=== End Decisions ===";
            sections.Add(new ContextSection("decisions", decisionsContent));
        }

        // Prior design docs
        if (!string.IsNullOrEmpty(priorSpecs))
        {
            var specsContent = $"=== Prior Design Docs (reference, don't contradict) ===\n{priorSpecs}\n=== End Prior Docs ===";
            sections.Add(new ContextSection("prior_specs", specsContent));
        }

        // Unresolved open questions
        if (!string.IsNullOrEmpty(openQuestions))
        {
            var oqContent = $"=== Unresolved Open Questions from Prior Docs ===\n{openQuestions}\n=== End Open Questions ===\n\nIf this question can resolve any of the above, do so.";
            sections.Add(new ContextSection("open_questions", oqContent));
        }

        // Prior rounds (filtered by agent patience/receptivity)
        var filteredPriorRounds = _promptBuilder.FilterPriorRounds(priorRounds, agent);
        if (!string.IsNullOrEmpty(filteredPriorRounds))
            sections.Add(new ContextSection("prior_rounds", filteredPriorRounds));

        // What's been said this round so far (only in sequential mode, after first speaker)
        if (!string.IsNullOrEmpty(thisRoundSoFar))
            sections.Add(new ContextSection("this_round_so_far", thisRoundSoFar));

        // The question itself (protected)
        var questionContent = $"## Question: {question.Title}\n\n{question.Body}";
        sections.Add(new ContextSection("question", questionContent, IsProtected: true));

        // Round instruction (protected)
        if (!string.IsNullOrEmpty(roundInstruction))
            sections.Add(new ContextSection("round_instruction", roundInstruction, IsProtected: true));

        // Speaking position (protected)
        var speakingPosition = !string.IsNullOrEmpty(thisRoundSoFar)
            ? "Other agents have already spoken this round. Respond to their points directly -- disagree where you see a flaw, and be specific about why. Do not agree unless you have genuinely new evidence. 250 words max (excluding Position Summary)."
            : "You are speaking first this round. Set the agenda. 250 words max (excluding Position Summary).";
        sections.Add(new ContextSection("speaking_position", speakingPosition, IsProtected: true));

        // Position summary format (protected)
        const string summaryFormat = "IMPORTANT: End your response with exactly this format:\n## Position Summary\n[3 sentences: what you advocate, what you reject, and why.]";
        sections.Add(new ContextSection("position_summary_format", summaryFormat, IsProtected: true));

        return sections;
    }

    /// <summary>
    /// Assembles the Situation Layer + Task Layer for one agent's prompt.
    /// Calls BuildAgentSections(), optionally enforces budget, measures via telemetry,
    /// then concatenates into the final string.
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
        string thisRoundSoFar = "",
        string roundName = "",
        int questionNumber = 0,
        RoundCallbacks? callbacks = null,
        string context = "")
    {
        var sections = BuildAgentSections(
            agentKey, team, systemPrompts, question, decisions,
            priorRounds, priorSpecs, openQuestions, roundInstruction,
            agentRoles, thisRoundSoFar, context);

        var budgetSettings = _configLoader.Defaults().ContextBudget;
        var rescueActions = new List<string>();

        if (budgetSettings.Enabled)
        {
            var preSnapshot = new ContextSnapshot
            {
                AgentKey = agentKey,
                RoundName = roundName,
                QuestionNumber = questionNumber,
                Sections = sections,
                BudgetTokens = budgetSettings.MaxPayloadTokens
            };
            var diagnosis = _enforcer.Diagnose(preSnapshot);
            if (diagnosis.IsOverBudget || diagnosis.IsImbalanced)
            {
                (sections, rescueActions) = _enforcer.Enforce(sections, diagnosis);
            }
        }

        var snapshot = new ContextSnapshot
        {
            AgentKey = agentKey,
            RoundName = roundName,
            QuestionNumber = questionNumber,
            Sections = sections,
            BudgetTokens = budgetSettings.MaxPayloadTokens,
            RescueActions = rescueActions
        };

        _telemetry.Record(snapshot);
        _telemetry.LogToConsole(snapshot);
        callbacks?.OnAgentContextStats?.Invoke(snapshot);

        return ConcatenateSections(sections);
    }

    /// <summary>
    /// Reconstructs the prompt string from named sections in the correct order.
    /// prior_rounds and this_round_so_far are combined under a single Discussion So Far block.
    /// </summary>
    private static string ConcatenateSections(List<ContextSection> sections)
    {
        var sb = new StringBuilder();

        var sectionMap = sections.ToDictionary(s => s.Name);

        void Append(string name)
        {
            if (sectionMap.TryGetValue(name, out var s) && s.Chars > 0)
            {
                sb.AppendLine(s.Content);
                sb.AppendLine();
            }
        }

        Append("perspective_reminder");
        Append("context_lens");
        Append("role_overlay");
        Append("context");
        Append("decisions");
        Append("prior_specs");
        Append("open_questions");

        // prior_rounds and this_round_so_far are combined under one header
        var hasPriorRounds = sectionMap.TryGetValue("prior_rounds", out var priorRoundsSection) && priorRoundsSection.Chars > 0;
        var hasThisRound = sectionMap.TryGetValue("this_round_so_far", out var thisRoundSection) && thisRoundSection.Chars > 0;

        if (hasPriorRounds || hasThisRound)
        {
            sb.AppendLine("=== Discussion So Far (this question) ===");
            if (hasPriorRounds)
                sb.AppendLine(priorRoundsSection!.Content);
            if (hasThisRound)
            {
                if (hasPriorRounds)
                    sb.AppendLine();
                sb.AppendLine($"--- This round so far ---\n{thisRoundSection!.Content}");
            }
            sb.AppendLine("=== End Discussion ===");
            sb.AppendLine();
        }

        Append("question");
        Append("round_instruction");

        // speaking_position and position_summary_format go at the end without blank line between them
        if (sectionMap.TryGetValue("speaking_position", out var sp) && sp.Chars > 0)
        {
            sb.Append(sp.Content);
            sb.AppendLine();
            sb.AppendLine();
        }

        if (sectionMap.TryGetValue("position_summary_format", out var psf) && psf.Chars > 0)
        {
            sb.Append(psf.Content);
        }

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
        RoundCallbacks? callbacks = null,
        string roundName = "",
        int questionNumber = 0,
        string context = "")
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
                    agentRoles, roundName: roundName, questionNumber: questionNumber,
                    callbacks: callbacks, context: context);

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
                agentRoles, thisRoundSoFar, roundName, questionNumber, callbacks, context);

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
