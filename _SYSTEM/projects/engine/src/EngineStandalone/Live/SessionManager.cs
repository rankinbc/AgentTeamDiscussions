using EngineStandalone.Abstractions;
using EngineStandalone.Agents;
using EngineStandalone.Config;
using EngineStandalone.Discussion;
using EngineStandalone.Runner;
using EngineStandalone.Session;
using EngineStandalone.Synthesis;

namespace EngineStandalone.Live;

public class SessionManager
{
    private readonly string _baseDir;
    private readonly IServiceProvider _provider;
    private Task? _runningTask;
    private CancellationTokenSource? _cts;
    private SseSessionEmitter? _emitter;

    public bool IsRunning => _runningTask is { IsCompleted: false };
    public SseSessionEmitter? Emitter => _emitter;
    public IConfigLoader ConfigLoader => _provider.GetRequiredService<IConfigLoader>();

    public SessionManager(string baseDir, IServiceProvider provider)
    {
        _baseDir = baseDir;
        _provider = provider;
    }

    public bool Start(SessionConfig config, SseSessionEmitter emitter)
    {
        if (IsRunning) return false;

        _emitter = emitter;
        _cts = new CancellationTokenSource();
        var ct = _cts.Token;

        var runner = new SessionRunner(
            _baseDir,
            _provider.GetRequiredService<IConfigLoader>(),
            _provider.GetRequiredService<IAgentLoader>(),
            _provider.GetRequiredService<IPromptBuilder>(),
            _provider.GetRequiredService<IClaudeRunner>(),
            _provider.GetRequiredService<IDiscussionEngine>(),
            _provider.GetRequiredService<IMorningBriefGenerator>(),
            emitter);

        _runningTask = Task.Run(async () =>
        {
            try
            {
                await runner.RunFromConfigAsync(config);
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Session cancelled by user.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Session error: {ex.Message}");
            }
        }, ct);

        return true;
    }

    public bool Stop()
    {
        if (!IsRunning) return false;
        _cts?.Cancel();
        _emitter?.Emit(new SessionStoppedEvent());
        return true;
    }
}
