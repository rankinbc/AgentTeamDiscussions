// CLI entry point. Three commands:
//   EngineStandalone <brief.md>          — run session from brief file
//   EngineStandalone new [--topic "..."] — interactive or quick session creation
//   EngineStandalone eval <dir>          — evaluate experiment output
//   EngineStandalone list-teams          — show available teams and their modes
//
// All tunable settings live in config/defaults.yaml. CLI flags are overrides only.

using System.CommandLine;
using Microsoft.Extensions.DependencyInjection;
using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Config;
using EngineStandalone.Discussion;
using EngineStandalone.Evaluation;
using EngineStandalone.Live;
using EngineStandalone.Runner;
using EngineStandalone.Session;
using EngineStandalone.Synthesis;

namespace EngineStandalone;

class Program
{
    static async Task<int> Main(string[] args)
    {
        var baseDir = ResolveBaseDir();
        var provider = BuildServices(baseDir);
        var defaults = provider.GetRequiredService<IConfigLoader>().Defaults();

        var rootCommand = new RootCommand("Discussion Engine — multi-agent AI discussion orchestrator");

        // --- Root command: run from brief file ---
        var briefArg = new Argument<FileInfo?>("brief", () => null, "Brief markdown file (auto-discovers from input/ if omitted)");
        var resumeOption = new Option<string?>("--resume", "Resume a specific session by folder name") { };
        resumeOption.AddAlias("-r");
        var liveOption = new Option<bool>("--live", "Start live SSE dashboard");
        var evalOption = new Option<bool>("--eval", "Run evaluation after session completes");
        evalOption.AddAlias("-e");

        rootCommand.AddArgument(briefArg);
        rootCommand.AddOption(resumeOption);
        rootCommand.AddOption(liveOption);
        rootCommand.AddOption(evalOption);

        rootCommand.SetHandler(async (context) =>
        {
            var brief = context.ParseResult.GetValueForArgument(briefArg);
            var resume = context.ParseResult.GetValueForOption(resumeOption);
            var live = context.ParseResult.GetValueForOption(liveOption);
            var eval = context.ParseResult.GetValueForOption(evalOption) || defaults.Session.RunEval;

            var briefPath = ResolveBriefPath(brief, baseDir, defaults);
            if (briefPath == null)
            {
                context.ExitCode = 1;
                return;
            }

            try
            {
                var (emitter, webApp, _) = StartLiveServer(live, defaults.Session.LivePort, provider, baseDir);
                var runner = CreateRunner(baseDir, provider, emitter);
                var preparer = new SessionPreparer(
                    provider.GetRequiredService<IAgentLoader>(),
                    provider.GetRequiredService<IConfigLoader>());

                var config = preparer.PrepareFromBrief(briefPath);
                await runner.RunFromConfigAsync(config, runEval: eval, resumeSession: resume);

                await WaitForLiveServer(webApp, context);
            }
            catch (Exception ex)
            {
                PrintError(ex);
                context.ExitCode = 1;
            }
        });

        // --- Subcommand: new — interactive or quick session creation ---
        var newCommand = new Command("new", "Create and run a new session interactively");
        var topicOption = new Option<string?>("--topic", "Topic to discuss (skips interactive prompt)");
        topicOption.AddAlias("-t");
        var teamOption = new Option<string?>("--team", "Team name (skips team selection)");
        var agentsOption = new Option<string?>("--agents", "Comma-separated agent keys to include (e.g. cognitive_architect,adversarial_critic)");
        var newLiveOption = new Option<bool>("--live", "Start live SSE dashboard");
        var newEvalOption = new Option<bool>("--eval", "Run evaluation after session completes");

        newCommand.AddOption(topicOption);
        newCommand.AddOption(teamOption);
        newCommand.AddOption(agentsOption);
        newCommand.AddOption(newLiveOption);
        newCommand.AddOption(newEvalOption);

        newCommand.SetHandler(async (context) =>
        {
            var topic = context.ParseResult.GetValueForOption(topicOption);
            var teamName = context.ParseResult.GetValueForOption(teamOption);
            var agentsRaw = context.ParseResult.GetValueForOption(agentsOption);
            var live = context.ParseResult.GetValueForOption(newLiveOption);
            var eval = context.ParseResult.GetValueForOption(newEvalOption) || defaults.Session.RunEval;

            // Parse --agents flag
            List<string>? agentsList = null;
            if (!string.IsNullOrWhiteSpace(agentsRaw))
                agentsList = agentsRaw.Split(',', StringSplitOptions.RemoveEmptyEntries)
                    .Select(a => a.Trim()).ToList();

            try
            {
                var preparer = new SessionPreparer(
                    provider.GetRequiredService<IAgentLoader>(),
                    provider.GetRequiredService<IConfigLoader>());

                var config = string.IsNullOrWhiteSpace(topic)
                    ? preparer.Prepare()
                    : preparer.PrepareFromArgs(topic, teamName, agents: agentsList);

                var (emitter, webApp, _) = StartLiveServer(live, defaults.Session.LivePort, provider, baseDir);
                var runner = CreateRunner(baseDir, provider, emitter);
                await runner.RunFromConfigAsync(config, runEval: eval);

                await WaitForLiveServer(webApp, context);
            }
            catch (Exception ex)
            {
                PrintError(ex);
                context.ExitCode = 1;
            }
        });
        rootCommand.AddCommand(newCommand);

        // --- Subcommand: eval — evaluate experiment output ---
        var evalCommand = new Command("eval", "Evaluate experiment output");
        var evalDirArg = new Argument<DirectoryInfo>("directory", "Experiment output directory to evaluate");
        evalCommand.AddArgument(evalDirArg);

        evalCommand.SetHandler(async (context) =>
        {
            var dir = context.ParseResult.GetValueForArgument(evalDirArg);
            if (!dir.Exists)
            {
                Console.WriteLine($"ERROR: Directory not found: {dir.FullName}");
                context.ExitCode = 1;
                return;
            }

            try
            {
                var evaluator = new Evaluator(
                    provider.GetRequiredService<IClaudeRunner>(),
                    provider.GetRequiredService<IConfigLoader>());

                Console.WriteLine($"Evaluating: {dir.Name}");
                var startTime = DateTime.UtcNow;
                var (evaluations, summary) = await evaluator.EvaluateExperimentAsync(
                    dir.FullName, defaults.Timeouts.Evaluation);
                var elapsed = (DateTime.UtcNow - startTime).TotalSeconds;

                if (evaluations.Count == 0)
                {
                    Console.WriteLine("  No design docs found to evaluate.");
                    return;
                }

                Console.WriteLine($"  Overall: {summary.Overall}/10 ({elapsed:F0}s)");
                var report = evaluator.FormatReport(dir.Name, evaluations, summary, elapsed);
                var reportPath = Path.Combine(dir.FullName, $"eval-{dir.Name}.md");
                await File.WriteAllTextAsync(reportPath, report);
                Console.WriteLine($"  Report: {reportPath}");
            }
            catch (Exception ex)
            {
                PrintError(ex);
                context.ExitCode = 1;
            }
        });
        rootCommand.AddCommand(evalCommand);

        // --- Subcommand: list-teams — show teams with their modes ---
        var listTeamsCommand = new Command("list-teams", "List available teams and their modes");
        listTeamsCommand.SetHandler(() =>
        {
            try
            {
                var agentLoader = provider.GetRequiredService<IAgentLoader>();
                var teams = agentLoader.ListTeams();

                Console.WriteLine("Available teams:");
                Console.WriteLine();
                foreach (var (name, file, count) in teams)
                {
                    var teamName = Path.GetFileNameWithoutExtension(file);
                    Console.WriteLine($"  {name} ({count} agents)");

                    // Load team to show modes
                    try
                    {
                        var team = agentLoader.LoadTeamByName(teamName);
                        if (team.Modes.Count > 0)
                        {
                            foreach (var (modeName, mode) in team.Modes.OrderBy(m => m.Key))
                            {
                                var def = modeName == team.DefaultMode ? " *" : "";
                                Console.WriteLine($"    {modeName}{def} — {mode.Description}");
                            }
                        }
                    }
                    catch { /* skip if mode parsing fails */ }

                    Console.WriteLine();
                }
            }
            catch (Exception ex)
            {
                PrintError(ex);
            }
        });
        rootCommand.AddCommand(listTeamsCommand);

        // --- Subcommand: serve — start live server only (for UI-driven sessions) ---
        var serveCommand = new Command("serve", "Start the live server without a session (UI launches sessions via API)");
        serveCommand.SetHandler(async (context) =>
        {
            try
            {
                var (_, webApp, _) = StartLiveServer(true, defaults.Session.LivePort, provider, baseDir);
                Console.WriteLine("Server ready. Open the UI to configure and start a discussion.");
                await Task.Delay(Timeout.Infinite, context.GetCancellationToken());
            }
            catch (OperationCanceledException) { }
            catch (Exception ex)
            {
                PrintError(ex);
                context.ExitCode = 1;
            }
        });
        rootCommand.AddCommand(serveCommand);

        return await rootCommand.InvokeAsync(args);
    }

    // --- Helpers ---

    private static ServiceProvider BuildServices(string baseDir)
    {
        var services = new ServiceCollection();
        services.AddSingleton<IClaudeRunner>(new ClaudeRunner());
        var configLoader = new ConfigLoader(
            Path.Combine(baseDir, "config"), Path.Combine(baseDir, "templates"));
        services.AddSingleton<IConfigLoader>(configLoader);
        var defaults = configLoader.Defaults();
        var dataDir = Path.IsPathRooted(defaults.Paths.DataDir)
            ? defaults.Paths.DataDir
            : Path.GetFullPath(Path.Combine(baseDir, defaults.Paths.DataDir));
        services.AddSingleton<IAgentLoader>(new AgentLoader(dataDir, "discussionAgents"));
        services.AddSingleton<IPromptBuilder>(new PromptBuilder());
        services.AddSingleton<IRoundRunner>(sp =>
            new RoundRunner(sp.GetRequiredService<IClaudeRunner>(),
                sp.GetRequiredService<IPromptBuilder>(),
                sp.GetRequiredService<IConfigLoader>()));
        services.AddSingleton<IDiscussionEngine>(sp =>
            new DiscussionEngine(sp.GetRequiredService<IClaudeRunner>(),
                sp.GetRequiredService<IPromptBuilder>(),
                sp.GetRequiredService<IConfigLoader>(),
                sp.GetRequiredService<IRoundRunner>()));
        services.AddSingleton<IMorningBriefGenerator>(sp =>
            new MorningBriefGenerator(sp.GetRequiredService<IClaudeRunner>(),
                sp.GetRequiredService<IConfigLoader>()));
        return services.BuildServiceProvider();
    }

    private static SessionRunner CreateRunner(string baseDir, ServiceProvider provider, ISessionEventEmitter? emitter)
    {
        return new SessionRunner(baseDir,
            provider.GetRequiredService<IConfigLoader>(),
            provider.GetRequiredService<IAgentLoader>(),
            provider.GetRequiredService<IPromptBuilder>(),
            provider.GetRequiredService<IClaudeRunner>(),
            provider.GetRequiredService<IDiscussionEngine>(),
            provider.GetRequiredService<IMorningBriefGenerator>(),
            emitter);
    }

    private static (SseSessionEmitter? Emitter, WebApplication? App, SessionManager? Manager) StartLiveServer(
        bool live, int port, ServiceProvider provider, string baseDir)
    {
        if (!live) return (null, null, null);

        var emitter = new SseSessionEmitter();
        var manager = new SessionManager(baseDir, provider);
        var agentLoader = provider.GetRequiredService<IAgentLoader>();
        var webApp = LiveServer.Build(emitter, manager, agentLoader, baseDir, port);
        _ = webApp.StartAsync();
        Console.WriteLine($"Live SSE dashboard: http://localhost:{port}");
        return (emitter, webApp, manager);
    }

    private static async Task WaitForLiveServer(WebApplication? webApp, System.CommandLine.Invocation.InvocationContext context)
    {
        if (webApp == null) return;
        Console.WriteLine("Session complete. SSE server still running. Press Ctrl+C to exit.");
        await Task.Delay(Timeout.Infinite, context.GetCancellationToken());
    }

    private static string? ResolveBriefPath(FileInfo? brief, string baseDir, AppSettings defaults)
    {
        if (brief != null)
        {
            if (!File.Exists(brief.FullName))
            {
                Console.WriteLine($"ERROR: Brief not found: {brief.FullName}");
                return null;
            }
            return brief.FullName;
        }

        var inputDir = Path.IsPathRooted(defaults.Paths.InputDir)
            ? defaults.Paths.InputDir
            : Path.GetFullPath(Path.Combine(baseDir, defaults.Paths.InputDir));
        if (Directory.Exists(inputDir))
        {
            var briefs = Directory.GetFiles(inputDir, "*.md");
            if (briefs.Length > 0)
            {
                Console.WriteLine($"Using brief: {briefs[0]}");
                return briefs[0];
            }
        }

        Console.WriteLine($"ERROR: No brief file specified and none found in {inputDir}");
        Console.WriteLine("Usage: EngineStandalone <brief.md> or EngineStandalone new");
        return null;
    }

    /// <summary>
    /// Resolve the engine project root directory.
    /// When running via 'dotnet run', BaseDirectory is bin/Debug/net8.0/ — walk up to find
    /// the engine root (the directory containing config/ and data/).
    /// Falls back to BaseDirectory if the project root can't be found.
    /// </summary>
    private static string ResolveBaseDir()
    {
        var binDir = AppDomain.CurrentDomain.BaseDirectory;

        // Walk up from bin/Debug/net8.0/ looking for the engine project root.
        // Skip the bin dir itself (config/ is copied there but it's not the real root).
        // The real root has config/defaults.yaml AND a src/ directory.
        var candidate = binDir;
        for (int i = 0; i < 6; i++)
        {
            var parent = Directory.GetParent(candidate)?.FullName;
            if (parent == null) break;
            candidate = parent;

            if (File.Exists(Path.Combine(candidate, "config", "defaults.yaml")) &&
                Directory.Exists(Path.Combine(candidate, "src")))
            {
                return candidate + Path.DirectorySeparatorChar;
            }
        }

        // Fallback: use bin directory (has copies via CopyToOutputDirectory)
        return binDir;
    }

    private static void PrintError(Exception ex)
    {
        Console.WriteLine($"ERROR: {ex.Message}");
        if (Environment.GetEnvironmentVariable("DEBUG") == "1")
            Console.WriteLine(ex.StackTrace);
    }
}
