// Session orchestrator ("Session Platform" from v1 docs).
// Parses a brief, runs each question through the discussion engine, writes crash-safe
// output, builds the decisions ledger, and generates the Morning Brief.
// Two execution modes:
//   - Session mode: full persistence, ledger, Morning Brief, crash recovery (RunSessionAsync)
//   - No-session mode: design docs only, no ledger (RunNoSessionAsync)

using System.Text;
using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Brief;
using EngineStandalone.Config;
using EngineStandalone.Discussion;
using EngineStandalone.Live;
using EngineStandalone.Runner;
using EngineStandalone.Synthesis;
using EngineStandalone.Telemetry;
using EngineStandalone.Types;

namespace EngineStandalone.Session;

/// <summary>
/// Result of running a question with cascade error handling.
/// </summary>
public class QuestionRunResult
{
    public QuestionRunStatus Status { get; set; }
    public string? Reason { get; set; }
    public Dictionary<string, RoundRunStatus> RoundStatus { get; set; } = new();
    public string? DesignDoc { get; set; }
    public string? Transcript { get; set; }
}

/// <summary>
/// Orchestrates full discussion sessions with crash recovery, ledger, and Morning Brief.
/// </summary>
public class SessionRunner
{
    private readonly string _baseDir;
    private readonly IConfigLoader _configLoader;
    private readonly IAgentLoader _agentLoader;
    private readonly IPromptBuilder _promptBuilder;
    private readonly IClaudeRunner _claudeRunner;
    private readonly IDiscussionEngine _discussionEngine;
    private readonly IMorningBriefGenerator _morningBriefGenerator;
    private readonly IContextTelemetry _telemetry;
    private readonly ISessionEventEmitter? _emitter;

    public SessionRunner(
        string baseDir,
        IConfigLoader configLoader,
        IAgentLoader agentLoader,
        IPromptBuilder promptBuilder,
        IClaudeRunner claudeRunner,
        IDiscussionEngine discussionEngine,
        IMorningBriefGenerator morningBriefGenerator,
        IContextTelemetry telemetry,
        ISessionEventEmitter? emitter = null)
    {
        _baseDir = baseDir;
        _configLoader = configLoader;
        _agentLoader = agentLoader;
        _promptBuilder = promptBuilder;
        _claudeRunner = claudeRunner;
        _discussionEngine = discussionEngine;
        _morningBriefGenerator = morningBriefGenerator;
        _telemetry = telemetry;
        _emitter = emitter;
    }

    /// <summary>
    /// Run a full session with session management (ledger, Morning Brief, crash recovery).
    /// </summary>
    public async Task RunSessionAsync(
        string briefPath,
        string? sessionsDir = null,
        string modeName = "compete",
        int timeout = 120,
        bool runEval = false,
        string? resumeSession = null,
        string? teamYaml = null)
    {
        // Brief parsing: extract the decisions preamble and ordered question list
        var parser = new BriefParser();
        var (decisionsText, allQuestions) = parser.ParseBrief(briefPath);

        var defaults = _configLoader.Defaults();
        var sessionsRoot = sessionsDir ?? Path.Combine(_baseDir, defaults.Paths.SessionsDir);
        Directory.CreateDirectory(sessionsRoot);

        // Team loading: from --team flag or default
        var teamPath = teamYaml ?? Path.Combine(_baseDir, "data", "teams", $"{defaults.Paths.DefaultTeam}.yaml");
        var team = _agentLoader.LoadTeam(teamPath);

        // Mode loading: from the team's modes
        var mode = team.GetMode(modeName);
        if (mode == null)
        {
            Console.WriteLine($"ERROR: Unknown mode '{modeName}' for this team");
            Console.WriteLine($"  Available: {string.Join(", ", team.Modes.Keys)}");
            return;
        }
        var systemPrompts = team.Agents.ToDictionary(
            kvp => kvp.Key,
            kvp => _promptBuilder.BuildSystemPrompt(kvp.Value));

        // Session setup: hash the question list for resume integrity validation
        var qHash = SessionPersistence.HashQuestionList(
            allQuestions.Select(q => (q.Number, q.Title)));

        Console.WriteLine($"Parsed brief: {allQuestions.Count} questions (hash: {qHash})");

        string sessionDir;
        int completed;

        if (!string.IsNullOrEmpty(resumeSession))
        {
            // Resume logic: validate the session exists and the brief hash hasn't changed
            sessionDir = Path.Combine(sessionsRoot, resumeSession);
            if (!Directory.Exists(sessionDir))
            {
                Console.WriteLine($"ERROR: Session not found: {sessionDir}");
                return;
            }

            var storedStatus = SessionPersistence.LoadSessionStatus(sessionDir);
            if (!string.IsNullOrEmpty(storedStatus.QuestionHash) && storedStatus.QuestionHash != qHash)
            {
                Console.WriteLine("ERROR: Question list changed since this session started.");
                Console.WriteLine($"  Session hash: {storedStatus.QuestionHash}");
                Console.WriteLine($"  Current hash: {qHash}");
                Console.WriteLine("  Cannot resume with a different brief. Start a new session.");
                return;
            }

            completed = SessionPersistence.CountCompletedQuestions(sessionDir);
            Console.WriteLine($"Resuming session: {Path.GetFileName(sessionDir)} ({completed}/{allQuestions.Count} completed)");
        }
        else
        {
            // Check for auto-resume
            sessionDir = SessionPersistence.CreateSessionDir(sessionsRoot, Path.GetFileNameWithoutExtension(briefPath));
            completed = 0;
        }

        var questionsDir = Path.Combine(sessionDir, "questions");
        Directory.CreateDirectory(questionsDir);

        if (_emitter is SseSessionEmitter sseEmitter2)
        {
            sseEmitter2.SessionDir = sessionDir;
        }

        // Load/initialize session status
        var status = SessionPersistence.LoadSessionStatus(sessionDir);
        status.QuestionHash = qHash;
        status.Mode = modeName;
        status.Brief = Path.GetFileName(briefPath);
        status.Team = Path.GetFullPath(teamPath);
        SessionPersistence.WriteSessionStatus(sessionDir, status);

        var ledgerText = DecisionsLedger.ReadLedger(sessionDir);
        var displayNames = _configLoader.DisplayNames();

        // Prior context building: load completed design docs and accumulate open questions
        // for chaining. Each doc is truncated to DesignDocChain chars to stay within context limits.
        var priorSpecs = "";
        var accumulatedOpenQuestions = new List<(int FromQ, string Text)>();

        for (int i = 0; i < completed && i < allQuestions.Count; i++)
        {
            var q = allQuestions[i];
            var slug = BriefParser.Slugify(q.Title);
            var filename = $"{q.Number:D2}-{slug}";
            var docPath = Path.Combine(questionsDir, $"{filename}.md");

            if (SessionPersistence.IsComplete(docPath))
            {
                var docText = SessionPersistence.ReadWithoutMarker(docPath);
                priorSpecs += $"\n\n# {q.Title}\n\n{CompressDocToDecisions(docText)}";

                var newOqs = _discussionEngine.ExtractOpenQuestions(docText);
                foreach (var oq in newOqs)
                {
                    accumulatedOpenQuestions.Add((q.Number, oq));
                }
            }
        }

        var questionsToRun = allQuestions.Skip(completed).ToList();

        // Get mode agents
        var modeAgents = new HashSet<string>();
        foreach (var agents in mode.Groups.Values)
        {
            modeAgents.UnionWith(agents);
        }

        Console.WriteLine();
        Console.WriteLine(new string('=', 60));
        Console.WriteLine("Session Runner");
        Console.WriteLine($"Brief: {Path.GetFileName(briefPath)}");
        Console.WriteLine($"Mode: {modeName} -- {mode.Description}");
        Console.WriteLine($"Agents: {string.Join(", ", modeAgents.OrderBy(a => a))}");
        Console.WriteLine($"Questions: {completed} completed, {questionsToRun.Count} remaining");
        Console.WriteLine($"Timeout: {timeout}s per call");
        Console.WriteLine($"Session: {Path.GetFileName(sessionDir)}");
        Console.WriteLine($"Started: {DateTime.Now:yyyy-MM-dd HH:mm}");
        Console.WriteLine(new string('=', 60));

        // SSE event emission: session_start + agent_profile events for the live UI
        _emitter?.Emit(new SessionStartEvent
        {
            Brief = Path.GetFileName(briefPath),
            Mode = modeName,
            QuestionCount = allQuestions.Count,
            Agents = modeAgents.OrderBy(a => a).ToList(),
            DisplayNames = displayNames,
            Timeout = timeout
        });

        foreach (var agentKey in modeAgents)
        {
            if (team.Agents.TryGetValue(agentKey, out var agent))
            {
                _emitter?.Emit(new AgentProfileEvent
                {
                    Key = agentKey,
                    Name = agent.Name,
                    Role = agent.Position.Role,
                    Traits = new Dictionary<string, double>
                    {
                        ["assertiveness"] = agent.Personality.Assertiveness,
                        ["creativity_temp"] = agent.Personality.CreativityTemp,
                        ["risk_tolerance"] = agent.Personality.RiskTolerance,
                        ["stubbornness"] = agent.Personality.Stubbornness,
                        ["bluntness"] = agent.Personality.Bluntness
                    },
                    CognitiveStyle = agent.Personality.CognitiveStyle.ToString().ToLowerInvariant(),
                    EmotionalBaseline = agent.Personality.EmotionalBaseline.ToString().ToLowerInvariant(),
                    Drives = agent.Position.Drives,
                    PushbackOn = agent.Position.PushbackOn,
                    AntiSlop = new Dictionary<string, object>
                    {
                        ["agreement_tax"] = agent.AntiSlop.AgreementTax,
                        ["perspective_lock"] = agent.AntiSlop.PerspectiveEnforcement,
                        ["devils_advocate"] = agent.AntiSlop.DevilsAdvocateDuty,
                        ["uncomfortable_quota"] = agent.AntiSlop.UncomfortableIdeaQuota,
                        ["domain_pivot"] = agent.AntiSlop.DomainPivotTrigger
                    },
                    VoiceTone = agent.Voice.Tone,
                    Intensity = agent.Position.Intensity
                });
            }
        }

        // Question loop: iterate remaining questions with circuit breaker for consecutive failures
        var totalStart = DateTime.UtcNow;
        var consecutiveFailures = 0;

        foreach (var question in questionsToRun)
        {
            var qNum = question.Number;
            var qTitle = question.Title;
            var slug = BriefParser.Slugify(qTitle);
            var filename = $"{qNum:D2}-{slug}";
            var qKey = $"q{qNum}";

            // Circuit breaker
            if (consecutiveFailures >= defaults.HealthChecks.CircuitBreakerThreshold)
            {
                Console.WriteLine($"\n  CIRCUIT BREAKER: {consecutiveFailures} consecutive failures. Stopping.");
                var remainingIdx = questionsToRun.IndexOf(question);
                for (int i = remainingIdx; i < questionsToRun.Count; i++)
                {
                    var rq = questionsToRun[i];
                    status.Questions[$"q{rq.Number}"] = new QuestionStatus
                    {
                        Status = "skipped",
                        Title = rq.Title,
                        Reason = "circuit breaker"
                    };
                }
                SessionPersistence.WriteSessionStatus(sessionDir, status);
                break;
            }

            Console.WriteLine($"\n[{qNum}/{allQuestions.Count}] {qTitle}");
            _emitter?.Emit(new QuestionStartEvent
            {
                Number = qNum,
                Total = allQuestions.Count,
                Title = qTitle
            });
            var qStart = DateTime.UtcNow;

            // Moderator drain: check for human moderator directives injected via the live UI
            var modMsg = _emitter?.PopModerator();
            while (modMsg != null)
            {
                accumulatedOpenQuestions.Add((0, $"[MODERATOR DIRECTIVE] {modMsg}"));
                modMsg = _emitter?.PopModerator();
            }

            // Format accumulated open questions
            var oqText = "";
            if (accumulatedOpenQuestions.Count > 0)
            {
                var oqLines = accumulatedOpenQuestions.Select(oq => $"- [from Q{oq.FromQ}] {oq.Text}");
                oqText = string.Join("\n", oqLines);
            }

            // Per-question: run discussion rounds with cascade error handling
            var result = await RunQuestionWithCascadeAsync(
                question, team, systemPrompts, decisionsText, ledgerText,
                priorSpecs, oqText, timeout, mode, sessionDir);

            var qElapsed = (DateTime.UtcNow - qStart).TotalSeconds;

            if (result.Status == QuestionRunStatus.Complete)
            {
                var designDoc = result.DesignDoc!;
                var transcript = result.Transcript!;

                // Extract open questions from the design doc for chaining to subsequent questions
                var newOqs = _discussionEngine.ExtractOpenQuestions(designDoc);
                foreach (var oq in newOqs)
                {
                    accumulatedOpenQuestions.Add((qNum, oq));
                }

                // Write design doc
                var docPath = Path.Combine(questionsDir, $"{filename}.md");
                var header = $"# {qTitle}\n\n*Generated: {DateTime.Now:yyyy-MM-dd HH:mm} | " +
                             $"Question {qNum} | {qElapsed:F0}s | Mode: {modeName}*\n\n";
                SessionPersistence.WriteWithMarker(docPath, header + designDoc);

                // Write transcript
                var transcriptPath = Path.Combine(questionsDir, $"{filename}-transcript.md");
                SessionPersistence.WriteWithMarker(transcriptPath, transcript);

                // Ledger extraction: pull ## Ledger section from design doc, hallucination-check
                // it, then append to the running ledger file
                var ledgerSection = DecisionsLedger.ExtractLedgerSection(designDoc);
                if (string.IsNullOrEmpty(ledgerSection))
                {
                    Console.WriteLine("    No ledger in synthesis, using fallback...");
                    ledgerSection = DecisionsLedger.CreateFallbackEntry(qNum, qTitle);
                }
                else if (!DecisionsLedger.HallucinationCheck(designDoc, ledgerSection))
                {
                    Console.WriteLine("    WARNING: Ledger extraction looks suspicious, using anyway");
                }

                DecisionsLedger.AppendToLedger(sessionDir, ledgerSection, qNum, qTitle);
                ledgerText = DecisionsLedger.ReadLedger(sessionDir);

                // Design doc chaining: compress to decision statements for next question's context
                priorSpecs = CompressDocToDecisions(designDoc);

                // Session status tracking: write per-question status to session_status.json
                status.Questions[qKey] = new QuestionStatus
                {
                    Status = "complete",
                    Title = qTitle,
                    ElapsedSeconds = (int)qElapsed,
                    File = $"{filename}.md",
                    Rounds = result.RoundStatus.ToDictionary(r => r.Key, r => r.Value.ToString().ToLower())
                };
                SessionPersistence.WriteSessionStatus(sessionDir, status);

                var docLines = designDoc.Split('\n').Length;
                Console.WriteLine($"  Wrote {filename}.md ({docLines} lines) + transcript ({qElapsed:F0}s total)");

                _emitter?.Emit(new QuestionDoneEvent { Number = qNum, Elapsed = qElapsed });
                consecutiveFailures = 0;
            }
            else
            {
                status.Questions[qKey] = new QuestionStatus
                {
                    Status = result.Status.ToString().ToLower(),
                    Title = qTitle,
                    Reason = result.Reason,
                    ElapsedSeconds = (int)qElapsed,
                    Rounds = result.RoundStatus.ToDictionary(r => r.Key, r => r.Value.ToString().ToLower())
                };
                SessionPersistence.WriteSessionStatus(sessionDir, status);
                Console.WriteLine($"  Question {result.Status}: {result.Reason} ({qElapsed:F0}s)");
                _emitter?.Emit(new QuestionFailedEvent { Number = qNum, Reason = result.Reason ?? result.Status.ToString() });
                consecutiveFailures++;
            }
        }

        // Morning Brief generation: synthesize the accumulated ledger into an executive summary
        Console.WriteLine("\nGenerating Morning Brief...");
        _emitter?.Emit(new BriefStartEvent());
        ledgerText = DecisionsLedger.ReadLedger(sessionDir);

        string briefContent;
        if (string.IsNullOrWhiteSpace(ledgerText))
        {
            Console.WriteLine("  WARNING: Ledger is empty, writing minimal brief");
            briefContent = "# Morning Brief\n\nNo decisions were extracted. Review design docs directly.\n";
        }
        else
        {
            try
            {
                var rawBrief = await _morningBriefGenerator.GenerateAsync(ledgerText, status, timeout);
                briefContent = $"# Morning Brief: {Path.GetFileName(sessionDir)}\n\n" +
                               $"*Generated: {DateTime.Now:yyyy-MM-dd HH:mm}*\n\n" +
                               rawBrief;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  Morning Brief generation failed: {ex.Message}");
                briefContent = $"# Morning Brief (raw ledger -- synthesis call failed)\n\n" +
                               $"*Generated: {DateTime.Now:yyyy-MM-dd HH:mm}*\n\n" +
                               ledgerText;
            }
        }

        SessionPersistence.WriteWithMarker(Path.Combine(sessionDir, "summary.md"), briefContent);
        Console.WriteLine("  Wrote summary.md");
        _emitter?.Emit(new BriefDoneEvent
        {
            Preview = briefContent.Substring(0, Math.Min(500, briefContent.Length))
        });

        // Final status
        var totalElapsed = (DateTime.UtcNow - totalStart).TotalSeconds;
        var completedCount = status.Questions.Values.Count(q => q.Status == "complete");
        var failedCount = status.Questions.Values.Count(q => q.Status is "failed" or "skipped" or "partial");
        // Note: Legacy SessionStatus still uses strings; this is intentional for backward compat.

        status.SessionComplete = true;
        status.TotalElapsedSeconds = (int)totalElapsed;
        status.CompletedQuestions = completedCount;
        status.FailedQuestions = failedCount;
        SessionPersistence.WriteSessionStatus(sessionDir, status);

        await _telemetry.WriteSessionStatsAsync(sessionDir);

        _emitter?.Emit(new SessionDoneEvent
        {
            Elapsed = $"{totalElapsed:F0}",
            Completed = completedCount,
            Total = allQuestions.Count
        });

        Console.WriteLine();
        Console.WriteLine(new string('=', 60));
        Console.WriteLine($"Session complete: {completedCount} succeeded, {failedCount} failed/partial");
        Console.WriteLine($"Total time: {totalElapsed / 60:F1} minutes");
        Console.WriteLine($"Morning Brief: {Path.Combine(sessionDir, "summary.md")}");
        Console.WriteLine($"Session folder: {sessionDir}");
        Console.WriteLine(new string('=', 60));
    }

    /// <summary>
    /// Run a session without session management (just design docs).
    /// </summary>
    public async Task RunNoSessionAsync(
        string briefPath,
        string? outputDir = null,
        string modeName = "compete",
        int timeout = 120,
        string? teamYaml = null)
    {
        var parser = new BriefParser();
        var (decisionsText, allQuestions) = parser.ParseBrief(briefPath);

        var defaults = _configLoader.Defaults();
        var outPath = outputDir ?? Path.Combine(_baseDir, defaults.Paths.OutputDir);
        Directory.CreateDirectory(outPath);

        // Load team
        var teamPath = teamYaml ?? Path.Combine(_baseDir, "data", "teams", $"{defaults.Paths.DefaultTeam}.yaml");
        var team = _agentLoader.LoadTeam(teamPath);

        var mode = team.GetMode(modeName);
        if (mode == null)
        {
            Console.WriteLine($"ERROR: Unknown mode '{modeName}' for this team");
            return;
        }
        var systemPrompts = team.Agents.ToDictionary(
            kvp => kvp.Key,
            kvp => _promptBuilder.BuildSystemPrompt(kvp.Value));

        var displayNames = _configLoader.DisplayNames();

        // Get mode agents
        var modeAgents = new HashSet<string>();
        foreach (var agents in mode.Groups.Values)
        {
            modeAgents.UnionWith(agents);
        }

        Console.WriteLine(new string('=', 60));
        Console.WriteLine("Agent Discussion (no session management)");
        Console.WriteLine($"Brief: {Path.GetFileName(briefPath)}");
        Console.WriteLine($"Mode: {modeName} -- {mode.Description}");
        Console.WriteLine($"Agents: {string.Join(", ", modeAgents.OrderBy(a => a))}");
        Console.WriteLine($"Output: {outPath}");
        Console.WriteLine(new string('=', 60));

        var priorSpecs = "";
        var accumulatedOpenQuestions = new List<(int FromQ, string Text)>();
        var totalStart = DateTime.UtcNow;

        foreach (var question in allQuestions)
        {
            var qNum = question.Number;
            var qTitle = question.Title;
            var slug = BriefParser.Slugify(qTitle);
            var filename = $"{qNum:D2}-{slug}";

            Console.WriteLine($"\n[{qNum}/{allQuestions.Count}] {qTitle}");
            var qStart = DateTime.UtcNow;

            // Format accumulated open questions
            var oqText = "";
            if (accumulatedOpenQuestions.Count > 0)
            {
                var oqLines = accumulatedOpenQuestions.Select(oq => $"- [from Q{oq.FromQ}] {oq.Text}");
                oqText = string.Join("\n", oqLines);
            }

            var result = await _discussionEngine.RunQuestionAsync(
                question, team, systemPrompts, decisionsText,
                priorSpecs.Length > defaults.Truncation.PriorSpecs
                    ? priorSpecs.Substring(priorSpecs.Length - defaults.Truncation.PriorSpecs)
                    : priorSpecs,
                oqText, timeout, mode);

            var qElapsed = (DateTime.UtcNow - qStart).TotalSeconds;

            var newOqs = _discussionEngine.ExtractOpenQuestions(result.DesignDoc);
            foreach (var oq in newOqs)
            {
                accumulatedOpenQuestions.Add((qNum, oq));
            }

            var header = $"# {qTitle}\n\n*Generated: {DateTime.Now:yyyy-MM-dd HH:mm} | " +
                         $"Question {qNum} | {qElapsed:F0}s | Mode: {modeName}*\n\n";

            File.WriteAllText(Path.Combine(outPath, $"{filename}.md"), header + result.DesignDoc);
            File.WriteAllText(Path.Combine(outPath, $"{filename}-transcript.md"), result.Transcript);

            priorSpecs += $"\n\n# {qTitle}\n\n{CompressDocToDecisions(result.DesignDoc)}";
            Console.WriteLine($"  Wrote {filename}.md ({qElapsed:F0}s)");
        }

        var totalElapsed = (DateTime.UtcNow - totalStart).TotalSeconds;
        Console.WriteLine($"\nDone. {allQuestions.Count} docs in {totalElapsed / 60:F1} minutes. Output: {outPath}");
    }

    /// <summary>
    /// Runs a single question through all round groups with cascade failure handling:
    ///   - Propose fails -> skip entire question (can't build on nothing)
    ///   - Critique/Evaluate fails -> save partial output (proposal only or proposal+critique)
    ///   - Synthesis fails -> save transcript, mark as partial
    /// </summary>
    private async Task<QuestionRunResult> RunQuestionWithCascadeAsync(
        Question question,
        TeamConfig team,
        Dictionary<string, string> systemPrompts,
        string decisionsText,
        string ledgerText,
        string priorSpecs,
        string openQuestions,
        int timeout,
        TeamMode mode,
        string sessionDir,
        string context = "")
    {
        var groups = mode.Groups;
        var roundLabels = groups.Keys.ToList();
        var agentRoles = mode.AgentRoles;
        var displayNames = _configLoader.DisplayNames();
        var defaults = _configLoader.Defaults();
        var counterProposeInstruction = _configLoader.CounterProposeInstruction();

        var roundResponses = new Dictionary<string, Dictionary<string, string>>();
        var accumulatedDiscussion = "";
        var priorRoundSummaries = "";
        var roundStatus = new Dictionary<string, RoundRunStatus>();
        var questionsDir = Path.Combine(sessionDir, "questions");
        var slug = BriefParser.Slugify(question.Title);
        var filename = $"{question.Number:D2}-{slug}";

        // Combine decisions with ledger
        var fullDecisions = string.IsNullOrEmpty(ledgerText)
            ? decisionsText
            : decisionsText + "\n\n" + ledgerText;

        // Round execution: iterate through the mode's round groups (e.g. propose->critique->evaluate)
        foreach (var roundName in roundLabels)
        {
            if (!groups.TryGetValue(roundName, out var agents))
                continue;

            var agentNames = string.Join(", ", agents.Select(a => displayNames.TryGetValue(a, out var n) ? n : a));
            var displayName = roundName == "counter" ? "counter-propose" : roundName;

            var roleInfo = "";
            foreach (var a in agents)
            {
                if (agentRoles.TryGetValue(a, out var roleKey))
                    roleInfo += $" [{a}: {roleKey}]";
            }
            Console.WriteLine($"  [{question.Number}] Round {displayName}: {agentNames}{roleInfo}");
            _emitter?.Emit(new RoundStartEvent { Round = roundName, Agents = agentNames });

            var roundInst = roundName switch
            {
                "counter" => counterProposeInstruction,
                "critique" => "You have read the proposals above. Your job is to BREAK them. " +
                    "Do not fix surface issues -- challenge the core design. What will fail first? " +
                    "What assumption is wrong? If both proposals agree on something, that's the most " +
                    "dangerous assumption -- examine it hardest. Be specific about failure scenarios.",
                "evaluate" => "You have read the proposals and critiques above. Do not merge or compromise. " +
                    "Pick the stronger approach and explain why the other one loses. If the critique " +
                    "destroyed a proposal, say so. If both survived, pick the one with fewer unresolved " +
                    "risks and commit. State your verdict clearly.",
                _ => ""
            };

            // SSE callbacks: bridge round-level events to the live UI event emitter
            var callbacks = _emitter != null ? new RoundCallbacks
            {
                OnAgentStart = (agentKey) =>
                {
                    var dn = displayNames.TryGetValue(agentKey, out var n) ? n : agentKey;
                    _emitter.Emit(new AgentThinkingEvent
                    {
                        Agent = agentKey,
                        DisplayName = dn,
                        Round = roundName,
                        Question = question.Number
                    });
                },
                OnAgentContext = (agentKey, sysPrompt, payload) =>
                {
                    var dn = displayNames.TryGetValue(agentKey, out var n) ? n : agentKey;
                    _emitter.Emit(new AgentContextEvent
                    {
                        Agent = agentKey,
                        DisplayName = dn,
                        Round = roundName,
                        Question = question.Number,
                        SystemPrompt = sysPrompt,
                        Payload = payload
                    });
                },
                OnAgentDone = (agentKey, response, elapsed) =>
                {
                    var dn = displayNames.TryGetValue(agentKey, out var n) ? n : agentKey;
                    var isError = response.Contains("[Claude CLI timed out") || response.Contains("[Error");
                    _emitter.Emit(new AgentResponseEvent
                    {
                        Agent = agentKey,
                        DisplayName = dn,
                        Response = response,
                        Elapsed = elapsed,
                        Question = question.Number,
                        Round = roundName,
                        Error = isError ? true : null
                    });
                },
                OnAgentContextStats = (snapshot) =>
                {
                    _emitter.Emit(new AgentContextStatsEvent
                    {
                        Agent = snapshot.AgentKey,
                        Round = snapshot.RoundName,
                        Question = snapshot.QuestionNumber,
                        TotalTokens = snapshot.TotalTokens,
                        BudgetTokens = snapshot.BudgetTokens,
                        BudgetPct = Math.Round(snapshot.BudgetPercent * 100, 1),
                        Sections = snapshot.Sections
                            .Where(s => s.Chars > 0)
                            .Select(s => new ContextSectionStat
                            {
                                Name = s.Name,
                                Chars = s.Chars,
                                Tokens = s.Tokens,
                                IsProtected = s.IsProtected
                            }).ToList(),
                        RescueActions = snapshot.RescueActions
                    });
                }
            } : null;

            var startTime = DateTime.UtcNow;
            try
            {
                var responses = await _discussionEngine.RunRoundAsync(
                    agents, systemPrompts, team, question, fullDecisions,
                    priorRoundSummaries,
                    priorSpecs.Length > defaults.Truncation.PriorSpecs
                        ? priorSpecs.Substring(priorSpecs.Length - defaults.Truncation.PriorSpecs)
                        : priorSpecs,
                    openQuestions, timeout, roundInst,
                    agentRoles,
                    callbacks: callbacks,
                    roundName: roundName,
                    questionNumber: question.Number,
                    context: context);

                var elapsed = (DateTime.UtcNow - startTime).TotalSeconds;

                // Round health check: at least one agent must produce usable output (>=20 chars, no error markers)
                var (healthy, errorAgents) = CheckRoundHealth(responses, defaults);
                foreach (var ea in errorAgents)
                {
                    var resp = responses.TryGetValue(ea, out var r) ? r : "???";
                    Console.WriteLine($"    WARNING: {ea}: {resp.Substring(0, Math.Min(80, resp.Length))}");
                }

                if (!healthy)
                {
                    throw new Exception($"All agents failed in {roundName} round");
                }

                roundResponses[roundName] = responses;
                roundStatus[roundName] = RoundRunStatus.Complete;

                // Write round output
                var roundFile = Path.Combine(questionsDir, $"{filename}-{roundName}.md");
                var roundText = new StringBuilder();
                foreach (var (key, resp) in responses)
                {
                    var name = displayNames.TryGetValue(key, out var dn) ? dn : key;
                    roundText.AppendLine($"### {name}");
                    roundText.AppendLine();
                    roundText.AppendLine(resp);
                    roundText.AppendLine();
                }
                SessionPersistence.WriteWithMarker(roundFile, roundText.ToString());

                // Accumulate full discussion (for synthesis) and compressed summaries (for next round)
                foreach (var (key, resp) in responses)
                {
                    var name = displayNames.TryGetValue(key, out var dn) ? dn : key;
                    var label = roundName == "counter" ? "COUNTER-PROPOSAL" : roundName.ToUpper();
                    accumulatedDiscussion += $"[{label} - {name}]\n{resp}\n\n";
                }
                priorRoundSummaries = DiscussionCompressor.CompressToSummaries(accumulatedDiscussion);

                Console.WriteLine($"    Done in {elapsed:F0}s");
            }
            catch (Exception ex)
            {
                var elapsed = (DateTime.UtcNow - startTime).TotalSeconds;
                Console.WriteLine($"    ROUND FAILED: {roundName} -- {ex.Message} ({elapsed:F0}s)");
                roundStatus[roundName] = RoundRunStatus.Failed;

                // Cascade rule: propose/counter fails -> skip (can't build on nothing)
                if (roundName is "propose" or "counter")
                {
                    return new QuestionRunResult
                    {
                        Status = QuestionRunStatus.Skipped,
                        Reason = $"Propose round failed: {ex.Message}",
                        RoundStatus = roundStatus
                    };
                }
                else
                {
                    // Cascade rule: critique/evaluate fails -> save partial output
                    var transcript = _discussionEngine.FormatTranscript(question, roundResponses);
                    var transcriptPath = Path.Combine(questionsDir, $"{filename}-transcript.md");
                    SessionPersistence.WriteWithMarker(transcriptPath, transcript);

                    return new QuestionRunResult
                    {
                        Status = QuestionRunStatus.Partial,
                        Reason = $"{roundName} round failed: {ex.Message}",
                        RoundStatus = roundStatus,
                        Transcript = transcript
                    };
                }
            }
        }

        // Synthesis: final LLM call merging all round outputs into a unified design doc
        Console.WriteLine($"  [{question.Number}] Synthesizing design doc...");
        _emitter?.Emit(new SynthesisStartEvent { Question = question.Number });
        var synthStart = DateTime.UtcNow;

        try
        {
            var designDoc = await _discussionEngine.SynthesizeAsync(
                question, roundResponses, roundLabels, fullDecisions,
                priorSpecs, openQuestions, timeout, context);

            var synthElapsed = (DateTime.UtcNow - synthStart).TotalSeconds;

            if (string.IsNullOrWhiteSpace(designDoc) || designDoc.Length < defaults.HealthChecks.MinSynthesisLength)
            {
                throw new Exception($"Synthesis produced empty/minimal output ({designDoc?.Length ?? 0} chars)");
            }

            Console.WriteLine($"    Synthesis done in {synthElapsed:F0}s");
            _emitter?.Emit(new SynthesisDoneEvent
            {
                QuestionNum = question.Number,
                QuestionTitle = question.Title,
                FullDoc = designDoc,
                Preview = designDoc.Substring(0, Math.Min(500, designDoc.Length)),
                Elapsed = synthElapsed,
                Lines = designDoc.Split('\n').Length
            });
            roundStatus["synthesis"] = RoundRunStatus.Complete;

            var transcript = _discussionEngine.FormatTranscript(question, roundResponses);

            return new QuestionRunResult
            {
                Status = QuestionRunStatus.Complete,
                RoundStatus = roundStatus,
                DesignDoc = designDoc,
                Transcript = transcript
            };
        }
        catch (Exception ex)
        {
            // Cascade rule: synthesis fails -> save transcript, mark as partial
            var synthElapsed = (DateTime.UtcNow - synthStart).TotalSeconds;
            Console.WriteLine($"    SYNTHESIS FAILED: {ex.Message} ({synthElapsed:F0}s)");
            roundStatus["synthesis"] = RoundRunStatus.Failed;

            var transcript = _discussionEngine.FormatTranscript(question, roundResponses);
            var transcriptPath = Path.Combine(questionsDir, $"{filename}-transcript.md");
            SessionPersistence.WriteWithMarker(transcriptPath, transcript);

            return new QuestionRunResult
            {
                Status = QuestionRunStatus.Partial,
                Reason = $"Synthesis failed: {ex.Message}",
                RoundStatus = roundStatus,
                Transcript = transcript
            };
        }
    }

    /// <summary>
    /// Run a session from a SessionConfig — the new unified entry point.
    /// The SessionConfig contains everything: questions, team, mode, decisions.
    /// Creates the session dir, writes session.json, and runs the full session loop.
    /// </summary>
    public async Task RunFromConfigAsync(
        SessionConfig config,
        string? sessionsDir = null,
        bool runEval = false,
        string? resumeSession = null)
    {
        var defaults = _configLoader.Defaults();
        var sessionsRoot = sessionsDir
            ?? Path.Combine(_baseDir, defaults.Paths.SessionsDir);
        Directory.CreateDirectory(sessionsRoot);

        // Resolve team
        var teamPath = config.ResolvedTeamPath
            ?? Path.Combine(_baseDir, "data", "teams", $"{config.Team}.yaml");
        if (!File.Exists(teamPath))
        {
            Console.WriteLine($"ERROR: Team file not found: {teamPath}");
            return;
        }
        config.ResolvedTeamPath = Path.GetFullPath(teamPath);

        var team = _agentLoader.LoadTeam(teamPath);

        // Resolve mode from team
        // Filter agents if a subset was selected
        if (config.Agents is { Count: > 0 })
        {
            var filtered = team.Agents
                .Where(kvp => config.Agents.Contains(kvp.Key))
                .ToDictionary(kvp => kvp.Key, kvp => kvp.Value);

            if (filtered.Count == 0)
            {
                Console.WriteLine("ERROR: None of the selected agents exist in this team.");
                return;
            }

            team = new TeamConfig
            {
                Agents = filtered,
                Modes = team.Modes,
                DefaultMode = team.DefaultMode,
            };
        }

        var mode = team.GetMode(config.Mode);
        if (mode == null)
        {
            Console.WriteLine($"ERROR: Unknown mode '{config.Mode}' for team '{config.Team}'");
            Console.WriteLine($"  Available modes: {string.Join(", ", team.Modes.Keys)}");
            return;
        }

        // Filter mode groups to only include selected agents
        var activeAgentKeys = team.Agents.Keys.ToHashSet();
        var filteredMode = new TeamMode
        {
            Description = mode.Description,
            Groups = mode.Groups.ToDictionary(
                g => g.Key,
                g => g.Value.Where(a => activeAgentKeys.Contains(a)).ToList()),
            AgentRoles = mode.AgentRoles
                .Where(r => activeAgentKeys.Contains(r.Key))
                .ToDictionary(r => r.Key, r => r.Value),
        };
        // Drop empty rounds
        filteredMode.Groups = filteredMode.Groups
            .Where(g => g.Value.Count > 0)
            .ToDictionary(g => g.Key, g => g.Value);

        if (filteredMode.Groups.Count == 0)
        {
            Console.WriteLine("ERROR: No rounds have agents after filtering. Select more agents or a different mode.");
            return;
        }
        mode = filteredMode;

        var systemPrompts = team.Agents.ToDictionary(
            kvp => kvp.Key,
            kvp => _promptBuilder.BuildSystemPrompt(kvp.Value));

        var qHash = config.QuestionHash ?? SessionPersistence.HashQuestionList(
            config.Questions.Select(q => (q.Number, q.Title)));
        config.QuestionHash = qHash;

        Console.WriteLine($"Session: {config.Title} — {config.Questions.Count} questions (hash: {qHash})");

        // Session directory: resume or create
        string sessionDir;
        int completed;

        if (!string.IsNullOrEmpty(resumeSession))
        {
            sessionDir = Path.Combine(sessionsRoot, resumeSession);
            if (!Directory.Exists(sessionDir))
            {
                Console.WriteLine($"ERROR: Session not found: {sessionDir}");
                return;
            }

            var existing = SessionPersistence.LoadSessionConfig(sessionDir);
            if (existing != null && existing.QuestionHash != qHash)
            {
                Console.WriteLine("ERROR: Question list changed since this session started.");
                return;
            }

            completed = SessionPersistence.CountCompletedQuestions(sessionDir);
            Console.WriteLine($"Resuming: {Path.GetFileName(sessionDir)} ({completed}/{config.Questions.Count} completed)");
        }
        else
        {
            var slug = Brief.BriefParser.Slugify(config.Title);
            sessionDir = SessionPersistence.CreateSessionDir(sessionsRoot, slug);
            completed = 0;
        }

        // Write session.json
        config.State.Status = SessionRunStatus.Running;
        SessionPersistence.WriteSessionConfig(sessionDir, config);

        if (_emitter is SseSessionEmitter sseEmitter)
        {
            sseEmitter.SessionDir = sessionDir;
        }

        var questionsDir = Path.Combine(sessionDir, "questions");
        Directory.CreateDirectory(questionsDir);

        // Also write legacy session_status.json for backward compat
        var legacyStatus = new SessionStatus
        {
            QuestionHash = qHash,
            Mode = config.Mode,
            Brief = config.Source,
            Team = config.ResolvedTeamPath,
        };
        SessionPersistence.WriteSessionStatus(sessionDir, legacyStatus);

        var ledgerText = DecisionsLedger.ReadLedger(sessionDir);
        var displayNames = _configLoader.DisplayNames();

        // Reconstruct decisions text from config
        var decisionsText = config.Decided.Count > 0
            ? string.Join("\n", config.Decided.Select(d => $"- {d}"))
            : "";

        // Convert SessionQuestions to Brief.Questions for the engine
        var allQuestions = config.Questions.Select(q => new Brief.Question
        {
            Number = q.Number,
            Title = q.Title,
            Body = q.Body,
        }).ToList();

        // Build prior context from completed questions
        var priorSpecs = "";
        var accumulatedOpenQuestions = new List<(int FromQ, string Text)>();

        for (int i = 0; i < completed && i < allQuestions.Count; i++)
        {
            var q = allQuestions[i];
            var slug = BriefParser.Slugify(q.Title);
            var docPath = Path.Combine(questionsDir, $"{q.Number:D2}-{slug}.md");
            if (SessionPersistence.IsComplete(docPath))
            {
                var docText = SessionPersistence.ReadWithoutMarker(docPath);
                priorSpecs += $"\n\n# {q.Title}\n\n{CompressDocToDecisions(docText)}";
                foreach (var oq in _discussionEngine.ExtractOpenQuestions(docText))
                    accumulatedOpenQuestions.Add((q.Number, oq));
            }
        }

        var questionsToRun = allQuestions.Skip(completed).ToList();
        var modeAgents = mode.Groups.Values.SelectMany(a => a).Distinct().ToHashSet();

        // Session banner
        Console.WriteLine();
        Console.WriteLine(new string('=', 60));
        Console.WriteLine("Session Runner");
        Console.WriteLine($"  Title:     {config.Title}");
        Console.WriteLine($"  Team:      {config.Team}");
        Console.WriteLine($"  Mode:      {config.Mode} — {mode.Description}");
        Console.WriteLine($"  Agents:    {string.Join(", ", modeAgents.OrderBy(a => a))}");
        Console.WriteLine($"  Questions: {completed} completed, {questionsToRun.Count} remaining");
        Console.WriteLine($"  Timeout:   {config.Timeout}s per call");
        Console.WriteLine($"  Session:   {Path.GetFileName(sessionDir)}");
        Console.WriteLine(new string('=', 60));

        if (_emitter != null)
        {
            _emitter.Emit(new SessionStartEvent
            {
                Brief = config.Source,
                Mode = config.Mode,
                QuestionCount = allQuestions.Count,
                Agents = modeAgents.OrderBy(a => a).ToList(),
                DisplayNames = modeAgents.ToDictionary(k => k, k => displayNames.GetValueOrDefault(k, k)),
                Timeout = config.Timeout,
            });

            foreach (var agentKey in modeAgents)
            {
                if (team.Agents.TryGetValue(agentKey, out var agent))
                {
                    _emitter.Emit(new AgentProfileEvent
                    {
                        Key = agentKey,
                        Name = agent.Name,
                        Role = agent.Position.Role,
                        Traits = new Dictionary<string, double>
                        {
                            ["assertiveness"] = agent.Personality.Assertiveness,
                            ["creativity_temp"] = agent.Personality.CreativityTemp,
                            ["risk_tolerance"] = agent.Personality.RiskTolerance,
                            ["stubbornness"] = agent.Personality.Stubbornness,
                            ["bluntness"] = agent.Personality.Bluntness
                        },
                        CognitiveStyle = agent.Personality.CognitiveStyle.ToString().ToLowerInvariant(),
                        EmotionalBaseline = agent.Personality.EmotionalBaseline.ToString().ToLowerInvariant(),
                        Drives = agent.Position.Drives,
                        PushbackOn = agent.Position.PushbackOn,
                        AntiSlop = new Dictionary<string, object>
                        {
                            ["agreement_tax"] = agent.AntiSlop.AgreementTax,
                            ["perspective_lock"] = agent.AntiSlop.PerspectiveEnforcement,
                            ["devils_advocate"] = agent.AntiSlop.DevilsAdvocateDuty,
                            ["uncomfortable_quota"] = agent.AntiSlop.UncomfortableIdeaQuota,
                            ["domain_pivot"] = agent.AntiSlop.DomainPivotTrigger
                        },
                        VoiceTone = agent.Voice.Tone,
                        Intensity = agent.Position.Intensity
                    });
                }
            }
        }

        var totalStart = DateTime.UtcNow;
        var consecutiveFailures = 0;

        foreach (var question in questionsToRun)
        {
            var qNum = question.Number;
            var qTitle = question.Title;
            var qKey = $"q{qNum}";
            var slug = BriefParser.Slugify(qTitle);
            var filename = $"{qNum:D2}-{slug}";

            // Circuit breaker
            if (consecutiveFailures >= defaults.HealthChecks.CircuitBreakerThreshold)
            {
                Console.WriteLine($"\n  CIRCUIT BREAKER: {consecutiveFailures} consecutive failures. Stopping.");
                foreach (var remaining in questionsToRun.SkipWhile(q => q.Number != qNum))
                {
                    config.State.Questions[$"q{remaining.Number}"] = new QuestionState
                    {
                        Status = QuestionRunStatus.Skipped,
                        Title = remaining.Title,
                        Reason = "circuit breaker",
                    };
                }
                break;
            }

            Console.WriteLine($"\n[{qNum}/{allQuestions.Count}] {qTitle}");
            if (_emitter != null)
                _emitter.Emit(new QuestionStartEvent { Number = qNum, Total = allQuestions.Count, Title = qTitle });

            var qStart = DateTime.UtcNow;

            // Format open questions
            var oqText = accumulatedOpenQuestions.Count > 0
                ? string.Join("\n", accumulatedOpenQuestions.Select(oq => $"- [from Q{oq.FromQ}] {oq.Text}"))
                : "";

            var result = await RunQuestionWithCascadeAsync(
                question, team, systemPrompts,
                decisionsText + (string.IsNullOrEmpty(ledgerText) ? "" : $"\n\n{ledgerText}"),
                ledgerText,
                priorSpecs.Length > defaults.Truncation.PriorSpecs
                    ? priorSpecs[^defaults.Truncation.PriorSpecs..]
                    : priorSpecs,
                oqText,
                config.Timeout, mode, sessionDir, config.Context);

            var qElapsed = (int)(DateTime.UtcNow - qStart).TotalSeconds;

            if (result.Status == QuestionRunStatus.Complete)
            {
                var designDoc = result.DesignDoc!;

                // Extract open questions for next iteration
                foreach (var oq in _discussionEngine.ExtractOpenQuestions(designDoc))
                    accumulatedOpenQuestions.Add((qNum, oq));

                // Write design doc
                var header = $"# {qTitle}\n\n*Generated: {DateTime.Now:yyyy-MM-dd HH:mm} | Q{qNum} | {qElapsed}s | Mode: {config.Mode}*\n\n";
                SessionPersistence.WriteWithMarker(Path.Combine(questionsDir, $"{filename}.md"), header + designDoc);
                SessionPersistence.WriteWithMarker(Path.Combine(questionsDir, $"{filename}-transcript.md"), result.Transcript ?? "");

                // Ledger extraction
                var ledgerSection = DecisionsLedger.ExtractLedgerSection(designDoc);
                if (string.IsNullOrEmpty(ledgerSection))
                    ledgerSection = DecisionsLedger.CreateFallbackEntry(qNum, qTitle);

                if (!string.IsNullOrEmpty(ledgerSection))
                {
                    if (!DecisionsLedger.HallucinationCheck(designDoc, ledgerSection,
                        defaults.HealthChecks.HallucinationRatioMax, defaults.HealthChecks.HallucinationRatioMin))
                    {
                        Console.WriteLine("    WARNING: Ledger extraction looks suspicious, using anyway");
                    }
                    DecisionsLedger.AppendToLedger(sessionDir, ledgerSection, qNum, qTitle);
                    ledgerText = DecisionsLedger.ReadLedger(sessionDir);
                }

                priorSpecs = CompressDocToDecisions(designDoc);

                config.State.Questions[qKey] = new QuestionState
                {
                    Status = QuestionRunStatus.Complete,
                    Title = qTitle,
                    ElapsedSeconds = qElapsed,
                    File = $"{filename}.md",
                    Rounds = result.RoundStatus,
                };
                SessionPersistence.WriteSessionConfig(sessionDir, config);

                Console.WriteLine($"  Wrote {filename}.md ({designDoc.Split('\n').Length} lines) ({qElapsed}s)");

                if (_emitter != null)
                    _emitter.Emit(new QuestionDoneEvent { Number = qNum, Elapsed = qElapsed });

                consecutiveFailures = 0;
            }
            else
            {
                config.State.Questions[qKey] = new QuestionState
                {
                    Status = result.Status,
                    Title = qTitle,
                    Reason = result.Reason,
                    ElapsedSeconds = qElapsed,
                    Rounds = result.RoundStatus,
                };
                SessionPersistence.WriteSessionConfig(sessionDir, config);
                Console.WriteLine($"  Question {result.Status}: {result.Reason} ({qElapsed}s)");

                if (_emitter != null)
                    _emitter.Emit(new QuestionFailedEvent { Number = qNum, Reason = result.Reason ?? result.Status.ToString() });

                consecutiveFailures++;
            }
        }

        // Morning Brief
        Console.WriteLine("\nGenerating Morning Brief...");
        if (_emitter != null)
            _emitter.Emit(new BriefStartEvent());

        ledgerText = DecisionsLedger.ReadLedger(sessionDir);

        string briefContent;
        if (string.IsNullOrWhiteSpace(ledgerText))
        {
            briefContent = "# Morning Brief\n\nNo decisions were extracted. Review design docs directly.\n";
        }
        else
        {
            try
            {
                // Build legacy status for MorningBriefGenerator compatibility
                var briefStatus = new SessionStatus
                {
                    Questions = config.State.Questions.ToDictionary(
                        kvp => kvp.Key,
                        kvp => new QuestionStatus
                        {
                            Status = kvp.Value.Status.ToString().ToLower(),
                            Title = kvp.Value.Title,
                            Reason = kvp.Value.Reason,
                        })
                };
                var raw = await _morningBriefGenerator.GenerateAsync(ledgerText, briefStatus, config.Timeout);
                briefContent = $"# Morning Brief: {Path.GetFileName(sessionDir)}\n\n*Generated: {DateTime.Now:yyyy-MM-dd HH:mm}*\n\n{raw}";
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  Morning Brief generation failed: {ex.Message}");
                briefContent = $"# Morning Brief (raw ledger)\n\n*Generated: {DateTime.Now:yyyy-MM-dd HH:mm}*\n\n{ledgerText}";
            }
        }

        SessionPersistence.WriteWithMarker(Path.Combine(sessionDir, "summary.md"), briefContent);
        Console.WriteLine("  Wrote summary.md");

        if (_emitter != null)
            _emitter.Emit(new BriefDoneEvent { Preview = briefContent[..Math.Min(briefContent.Length, 400)] });

        // Final status
        var totalElapsed = (int)(DateTime.UtcNow - totalStart).TotalSeconds;
        var completedCount = config.State.Questions.Count(q => q.Value.Status == QuestionRunStatus.Complete);
        var failedCount = config.State.Questions.Count(q => q.Value.Status is QuestionRunStatus.Failed or QuestionRunStatus.Skipped or QuestionRunStatus.Partial);

        config.State.Status = SessionRunStatus.Complete;
        config.State.SessionComplete = true;
        config.State.TotalElapsedSeconds = totalElapsed;
        config.State.CompletedQuestions = completedCount;
        config.State.FailedQuestions = failedCount;
        SessionPersistence.WriteSessionConfig(sessionDir, config);

        await _telemetry.WriteSessionStatsAsync(sessionDir);

        Console.WriteLine();
        Console.WriteLine(new string('=', 60));
        Console.WriteLine($"Session complete: {completedCount} succeeded, {failedCount} failed/partial");
        Console.WriteLine($"Total time: {totalElapsed / 60.0:F1} minutes");
        Console.WriteLine($"Morning Brief: {Path.Combine(sessionDir, "summary.md")}");
        Console.WriteLine($"Session folder: {sessionDir}");
        Console.WriteLine(new string('=', 60));

        if (_emitter != null)
            _emitter.Emit(new SessionDoneEvent { Elapsed = $"{totalElapsed / 60.0:F1}m", Completed = completedCount, Total = allQuestions.Count });

        if (runEval)
        {
            Console.WriteLine("\nRunning evaluation...");
            try
            {
                var evaluator = new Evaluation.Evaluator(_claudeRunner, _configLoader);
                var (evaluations, summary) = await evaluator.EvaluateExperimentAsync(questionsDir, config.Timeout);
                Console.WriteLine($"  Overall score: {summary.Overall}/10");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  Evaluation failed: {ex.Message}");
            }
        }
    }

    /// <summary>
    /// Validates each agent's response: non-empty, meets min length, no error prefixes.
    /// Compress a design doc to its decision/contested/open headings only.
    /// Replaces full prose with one-line summaries for downstream context chaining.
    /// </summary>
    private static string CompressDocToDecisions(string designDoc)
    {
        var lines = new List<string>();
        var headings = System.Text.RegularExpressions.Regex.Matches(
            designDoc, @"^### (.+)$", System.Text.RegularExpressions.RegexOptions.Multiline);

        foreach (System.Text.RegularExpressions.Match h in headings)
        {
            lines.Add($"- {h.Groups[1].Value.Trim()}");
        }

        if (lines.Count == 0)
        {
            // Fallback: truncate to 500 chars if no headings found
            return designDoc[..Math.Min(designDoc.Length, 500)];
        }

        return string.Join("\n", lines);
    }

    /// <summary>
    /// Round is healthy if at least one agent succeeded.
    /// </summary>
    private static (bool Healthy, List<string> ErrorAgents) CheckRoundHealth(
        Dictionary<string, string> responses, AppSettings defaults)
    {
        var errorAgents = new List<string>();

        foreach (var (agentKey, resp) in responses)
        {
            // Check minimum length threshold
            if (string.IsNullOrEmpty(resp) || resp.Trim().Length < defaults.HealthChecks.MinResponseLength)
            {
                errorAgents.Add(agentKey);
            }
            // Check for known error marker prefixes from the CLI runner
            else if (resp.Contains("[Claude CLI timed out") || resp.Contains("[Error") || resp.Contains("[Empty response"))
            {
                errorAgents.Add(agentKey);
            }
        }

        // Round is healthy if at least one agent produced usable output
        var healthy = errorAgents.Count < responses.Count;
        return (healthy, errorAgents);
    }
}
