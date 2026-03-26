namespace EngineStandalone.Abstractions;

/// <summary>
/// Abstraction over the Claude CLI subprocess runner.
/// </summary>
public interface IClaudeRunner
{
    Task<string> RunAsync(string systemPrompt, string userMessage, int? timeout = null);
    string RunSync(string systemPrompt, string userMessage, int? timeout = null);
}
