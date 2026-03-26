using EngineStandalone.Config;

namespace EngineStandalone.Abstractions;

/// <summary>
/// Abstraction over YAML config loading with caching.
/// </summary>
public interface IConfigLoader
{
    AppSettings Defaults();
    AgentDisplayConfig AgentDisplay();
    Dictionary<string, string> DisplayNames();
    string DisplayName(string agentKey);
    string OverlayInstruction(string roleKey);
    string CounterProposeInstruction();
    string LoadPromptRaw(string templatePath);
    bool TemplateExists(string templatePath);
}
