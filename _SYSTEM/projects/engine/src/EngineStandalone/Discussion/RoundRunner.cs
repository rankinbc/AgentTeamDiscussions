// RoundRunner.cs — Executes a single discussion round (propose, critique, or evaluate).
// Each round runs agents in a computed speaking order. In sequential mode, later speakers
// see what earlier speakers said, enabling incremental debate within a single round.
// Context telemetry measures each section's size; budget enforcement trims when over ceiling.

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
/// OnAgentContext delivers the assembled prompt, OnAgentDone fires with the response and timing.
/// OnAgentContextStats delivers per-section telemetry for the context budget dashboard.
/// </summary>
public class RoundCallbacks
{
    public Action<string>? OnAgentStart { get; set; }
    public Action<string, string, string>? OnAgentContext { get; set; }
    public Action<string, ContextSnapshot>? OnAgentContextStats { get; set; }
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
    private readonly IContextTelemetry? _telemetry;
    private readonly IContextBudgetEnforcer? _budgetEnforcer;

    public RoundRunner(
        IClaudeRunner claudeRunner,
        IPromptBuilder promptBuilder,
        IConfigLoader configLoader,
        IContextTelemetry? telemetry = null,
        IContextBudgetEnforcer? budgetEnforcer = null)
    {
        _claudeRunner = claudeRunner;
        _promptBuilder = promptBuilder;
        _configLoader = configLoader;
        _telemetry = telemetry;
        _budgetEnforcer = budgetEnforcer;
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
            var score = p.Assertiveness * 0.5 + agent.Position.Intensity * 0.3 + p.Stubbornness * 0.2;
            score += random.NextDouble() * 0.2 - 0.1;
            scored.Add((key, score));
        }

        return scored.OrderByDescending(x => x.Score).Select(x => x.Key).ToList();
    }

    /// <summary>
    /// Assembles the Situation Layer + Task Layer as structured sections for measurement
    /// and budget enforcement. Each section is named and tagged as protected or cuttable.
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
        string thisRoundSoFar = "")
    {
        if (!team.Agents.TryGetValue(agentKey, out var agent))
        {
            throw new ArgumentException($"Agent '{agentKey}' not found in team");
        }

        var sections = new List<ContextSection>();

        // Perspective reminder (protected — identity reinforcement)
        var reminder = _promptBuilder.BuildPerspectiveReminder(agent);
        sections.Add(new ContextSection { Name = "perspective_reminder", Content = reminder + "\n", IsProtected = true });

        // Agent-specific context lens
        var contextLens = _promptBuilder.BuildContextLens(agent);
        if (!string.IsNullOrEmpty(contextLens))
        {
            sections.Add(new ContextSection { Name = "context_lens", Content = contextLens + "\n" });
        }

        // Per-agent role overlay
        if (agentRoles != null && agentRoles.TryGetValue(agentKey, out var roleKey))
        {
            var roleText = _configLoader.OverlayInstruction(roleKey);
            if (!string.IsNullOrEmpty(roleText))
            {
                sections.Add(new ContextSection
                {
                    Name = "role_overlay",
                    Content = $"=== Your Approach ===\n{roleText}\n=== End Approach ===\n"
                });
            }
        }

        // Decisions from brief
        if (!string.IsNullOrEmpty(decisions))
        {
            sections.Add(new ContextSection
            {
                Name = "decisions",
                Content = $"=== What's Already Decided ===\n{decisions}\n=== End Decisions ===\n"
            });
        }

        // Prior design docs
        if (!string.IsNullOrEmpty(priorSpecs))
        {
            sections.Add(new ContextSection
            {
                Name = "prior_specs",
                Content = $"=== Prior Design Docs (reference, don't contradict) ===\n{priorSpecs}\n=== End Prior Docs ===\n"
            });
        }

        // Unresolved open questions
        if (!string.IsNullOrEmpty(openQuestions))
        {
            sections.Add(new ContextSection
            {
                Name = "open_questions",
                Content = $"=== Unresolved Open Questions from Prior Docs ===\n{openQuestions}\n=== End Open Questions ===\n\nIf this question can resolve any of the above, do so.\n"
            });
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
            sections.Add(new ContextSection
            {
                Name = "prior_rounds",
                Content = $"=== Discussion So Far (this question) ===\n{combinedContext}\n=== End Discussion ===\n"
            });
        }

        // The question itself (protected — the core task)
        sections.Add(new ContextSection
        {
            Name = "question",
            Content = $"## Question: {question.Title}\n\n{question.Body}\n",
            IsProtected = true
        });

        // Round instruction (protected)
        if (!string.IsNullOrEmpty(roundInstruction))
        {
            sections.Add(new ContextSection
            {
                Name = "round_instruction",
                Content = roundInstruction + "\n",
                IsProtected = true
            });
        }

        // Speaking order context (protected)
        var speakingText = !string.IsNullOrEmpty(thisRoundSoFar)
            ? "Other agents have already spoken this round. Respond to their points directly -- disagree where you see a flaw, and be specific about why. Do not agree unless you have genuinely new evidence. 250 words max (excluding Position Summary)."
            : "You are speaking first this round. Set the agenda. 250 words max (excluding Position Summary).";
        sections.Add(new ContextSection { Name = "speaking_position", Content = speakingText, IsProtected = true });

        // Position summary format (protected)
        sections.Add(new ContextSection
        {
            Name = "position_summary_format",
            Content = "\nIMPORTANT: End your response with exactly this format:\n## Position Summary\n[3 sentences: what you advocate, what you reject, and why.]",
            IsProtected = true
        });

        return sections;
    }

    /// <summary>
    /// Assembles the Situation Layer + Task Layer for one agent's prompt.
    /// Builds structured sections, applies budget enforcement, records telemetry,
    /// then concatenates into the final payload string.
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
        var sections = BuildAgentSections(
            agentKey, team, systemPrompts, question, decisions,
            priorRounds, priorSpecs, openQuestions, roundInstruction,
            agentRoles, thisRoundSoFar);

        // Budget enforcement (auto-rescue)
        var budget = _configLoader.Defaults().ContextBudget;
        if (_budgetEnforcer != null && budget.EnableAutoRescue)
        {
            sections = _budgetEnforcer.Enforce(sections, budget);
        }

        // Build snapshot for telemetry
        var systemPrompt = systemPrompts.TryGetValue(agentKey, out var sp) ? sp : "";
        var snapshot = new ContextSnapshot
        {
            AgentKey = agentKey,
            Round = roundInstruction.Length > 20 ? "round" : "",
            QuestionNumber = question.Number,
            Sections = sections,
            SystemPromptChars = systemPrompt.Length,
            SystemPromptEstimatedTokens = ContextSection.EstimateTokens(systemPrompt),
            BudgetTokens = budget.MaxPayloadTokens
        };

        if (budget.EnableTelemetry && _telemetry != null)
        {
            _telemetry.Record(snapshot);
            _telemetry.LogToConsole(snapshot);
        }

        // Store snapshot for callback retrieval
        _lastSnapshot = snapshot;

        return ConcatenateSections(sections);
    }

    // Thread-local would be needed for parallel mode; for sequential this is fine.
    // The callback fires immediately after BuildAgentPayload in RunRoundAsync.
    private ContextSnapshot? _lastSnapshot;

    /// <summary>
    /// Returns the last recorded ContextSnapshot from BuildAgentPayload.
    /// </summary>
    public ContextSnapshot? LastSnapshot => _lastSnapshot;

    private static string ConcatenateSections(List<ContextSection> sections)
    {
        var sb = new StringBuilder();
        foreach (var section in sections)
        {
            if (string.IsNullOrEmpty(section.Content)) continue;
            if (sb.Length > 0) sb.AppendLine();
            sb.Append(section.Content);
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
            callbacks?.OnAgentContextStats?.Invoke(agentKey, _lastSnapshot!);

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
