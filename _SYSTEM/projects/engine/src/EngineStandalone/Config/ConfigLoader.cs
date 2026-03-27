// ConfigLoader.cs — Central YAML configuration loader with caching.
// Reads from config/ and templates/ directories. All parsed configs are cached after first load.
// Provides: Defaults(), DisplayNames(), OverlayInstruction(), CounterProposeInstruction().
// Role overlays modify agent behavior per-mode (e.g., "competitive" -> "Frame as competing with other proposal").

using EngineStandalone.Abstractions;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace EngineStandalone.Config;

/// <summary>
/// Loads YAML configuration files and templates from the config and templates directories.
/// </summary>
public class ConfigLoader : IConfigLoader
{
    private readonly string _configDir;
    private readonly string _templateDir;
    private readonly IDeserializer _yamlDeserializer;
    private readonly Dictionary<string, object> _cache = new();

    public ConfigLoader(string configDir, string templateDir)
    {
        _configDir = configDir;
        _templateDir = templateDir;
        _yamlDeserializer = new DeserializerBuilder()
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .IgnoreUnmatchedProperties()
            .Build();
    }

    /// <summary>
    /// Load defaults.yaml and return AppSettings.
    /// </summary>
    public AppSettings Defaults()
    {
        const string key = "defaults";
        if (_cache.TryGetValue(key, out var cached))
            return (AppSettings)cached;

        var path = Path.Combine(_configDir, "defaults.yaml");
        var yaml = File.ReadAllText(path);
        var raw = _yamlDeserializer.Deserialize<Dictionary<string, object>>(yaml);

        var settings = new AppSettings();

        if (raw.TryGetValue("timeouts", out var timeoutsObj) && timeoutsObj is Dictionary<object, object> timeouts)
        {
            settings.Timeouts = new TimeoutSettings
            {
                Default = GetInt(timeouts, "default", 120),
                Discussion = GetInt(timeouts, "discussion", 420),
                Evaluation = GetInt(timeouts, "evaluation", 300),
                BatchQuestion = GetInt(timeouts, "batch_question", 600),
                LiveTurn = GetInt(timeouts, "live_turn", 60),
                SynthesisRolling = GetInt(timeouts, "synthesis_rolling", 30),
                Panel = GetInt(timeouts, "panel", 360),
                Brainstorm = GetInt(timeouts, "brainstorm", 420)
            };
        }

        if (raw.TryGetValue("truncation", out var truncObj) && truncObj is Dictionary<object, object> trunc)
        {
            settings.Truncation = new TruncationSettings
            {
                PriorSpecs = GetInt(trunc, "prior_specs", 6000),
                DesignDocChain = GetInt(trunc, "design_doc_chain", 3000),
                BrainstormInput = GetInt(trunc, "brainstorm_input", 8000),
                AgentEvalInput = GetInt(trunc, "agent_eval_input", 8000),
                DocEvalInput = GetInt(trunc, "doc_eval_input", 12000),
                RoundAnalysis = GetInt(trunc, "round_analysis", 1500),
                SpecGenContext = GetInt(trunc, "spec_gen_context", 2000),
                LowPatienceContext = GetInt(trunc, "low_patience_context", 2500),
                LiveContext = GetInt(trunc, "live_context", 5000)
            };
        }

        if (raw.TryGetValue("conversation", out var convObj) && convObj is Dictionary<object, object> conv)
        {
            settings.Conversation = new ConversationSettings
            {
                HistoryKeepFirst = GetInt(conv, "history_keep_first", 2),
                HistoryKeepLast = GetInt(conv, "history_keep_last", 10),
                HistoryTruncationThreshold = GetInt(conv, "history_truncation_threshold", 14),
                MultiHistoryKeepFirst = GetInt(conv, "multi_history_keep_first", 3),
                MultiHistoryKeepLast = GetInt(conv, "multi_history_keep_last", 15),
                MultiHistoryTruncationThreshold = GetInt(conv, "multi_history_truncation_threshold", 20),
                MaxWordCount = GetInt(conv, "max_word_count", 250),
                LiveSentenceLimit = GetString(conv, "live_sentence_limit", "2-4")
            };
        }

        if (raw.TryGetValue("health_checks", out var healthObj) && healthObj is Dictionary<object, object> health)
        {
            settings.HealthChecks = new HealthCheckSettings
            {
                MinResponseLength = GetInt(health, "min_response_length", 20),
                MinSynthesisLength = GetInt(health, "min_synthesis_length", 50),
                HallucinationRatioMax = GetDouble(health, "hallucination_ratio_max", 4.0),
                HallucinationRatioMin = GetDouble(health, "hallucination_ratio_min", 0.2),
                CircuitBreakerThreshold = GetInt(health, "circuit_breaker_threshold", 3)
            };
        }

        if (raw.TryGetValue("synthesis", out var synthObj) && synthObj is Dictionary<object, object> synth)
        {
            settings.Synthesis = new SynthesisSettings
            {
                IntervalTurns = GetInt(synth, "interval_turns", 10),
                MaxLedgerWords = GetInt(synth, "max_ledger_words", 50)
            };
        }

        if (raw.TryGetValue("display", out var dispObj) && dispObj is Dictionary<object, object> disp)
        {
            settings.Display = new DisplaySettings
            {
                SeparatorWidth = GetInt(disp, "separator_width", 60),
                SlugMaxLength = GetInt(disp, "slug_max_length", 60)
            };
        }

        if (raw.TryGetValue("context_budget", out var budgetObj) && budgetObj is Dictionary<object, object> budget)
        {
            settings.ContextBudget = new ContextBudgetSettings
            {
                Enabled = GetBool(budget, "enabled", false),
                MaxPayloadTokens = GetInt(budget, "max_payload_tokens", 4000),
                ImbalanceThreshold = GetDouble(budget, "imbalance_threshold", 0.60)
            };
        }

        if (raw.TryGetValue("paths", out var pathsObj) && pathsObj is Dictionary<object, object> paths)
        {
            settings.Paths = new PathSettings
            {
                SessionsDir = GetString(paths, "sessions_dir", "output/sessions"),
                OutputDir = GetString(paths, "output_dir", "output/design-docs"),
                DataDir = GetString(paths, "data_dir", "data"),
                InputDir = GetString(paths, "input_dir", "input"),
                DefaultTeam = GetString(paths, "default_team", "beta-agents")
            };
        }

        if (raw.TryGetValue("session", out var sessionObj) && sessionObj is Dictionary<object, object> session)
        {
            settings.Session = new SessionSettings
            {
                RunEval = GetBool(session, "run_eval", false),
                LivePort = GetInt(session, "live_port", 8899)
            };
        }

        if (raw.TryGetValue("completion_marker", out var marker))
        {
            settings.CompletionMarker = marker?.ToString() ?? "\n<!-- complete -->\n";
        }

        _cache[key] = settings;
        return settings;
    }

    /// <summary>
    /// Load agent_display.yaml and return display configuration.
    /// </summary>
    public AgentDisplayConfig AgentDisplay()
    {
        const string key = "agent_display";
        if (_cache.TryGetValue(key, out var cached))
            return (AgentDisplayConfig)cached;

        var path = Path.Combine(_configDir, "agent_display.yaml");
        var yaml = File.ReadAllText(path);
        var raw = _yamlDeserializer.Deserialize<Dictionary<string, object>>(yaml);

        var config = new AgentDisplayConfig();

        if (raw.TryGetValue("display_names", out var namesObj) && namesObj is Dictionary<object, object> names)
        {
            foreach (var kvp in names)
            {
                config.DisplayNames[kvp.Key.ToString()!] = kvp.Value?.ToString() ?? "";
            }
        }

        if (raw.TryGetValue("colors_hex", out var colorsObj) && colorsObj is Dictionary<object, object> colors)
        {
            foreach (var kvp in colors)
            {
                config.ColorsHex[kvp.Key.ToString()!] = kvp.Value?.ToString() ?? "";
            }
        }

        if (raw.TryGetValue("colors_ansi_cycle", out var ansiObj) && ansiObj is List<object> ansiList)
        {
            config.ColorsAnsiCycle = ansiList.Select(c => c.ToString()!).ToList();
        }

        _cache[key] = config;
        return config;
    }

    /// <summary>
    /// Load role_overlays.yaml and return overlay configurations.
    /// </summary>
    public (Dictionary<string, RoleOverlay> Overlays, string CounterProposeInstruction) RoleOverlays()
    {
        const string key = "role_overlays";
        if (_cache.TryGetValue(key, out var cached))
            return ((Dictionary<string, RoleOverlay>, string))cached;

        var path = Path.Combine(_configDir, "role_overlays.yaml");
        var yaml = File.ReadAllText(path);
        var raw = _yamlDeserializer.Deserialize<Dictionary<string, object>>(yaml);

        var overlays = new Dictionary<string, RoleOverlay>();
        var counterPropose = "";

        if (raw.TryGetValue("overlays", out var overlaysObj) && overlaysObj is Dictionary<object, object> overlayDict)
        {
            foreach (var kvp in overlayDict)
            {
                var name = kvp.Key.ToString()!;
                if (kvp.Value is Dictionary<object, object> data)
                {
                    overlays[name] = new RoleOverlay
                    {
                        Description = GetString(data, "description", ""),
                        Instruction = GetString(data, "instruction", "")
                    };
                }
            }
        }

        if (raw.TryGetValue("counter_propose_instruction", out var cpObj))
        {
            counterPropose = cpObj?.ToString() ?? "";
        }

        var result = (overlays, counterPropose);
        _cache[key] = result;
        return result;
    }

    /// <summary>
    /// Get display name for an agent key.
    /// </summary>
    public string DisplayName(string agentKey)
    {
        var config = AgentDisplay();
        return config.DisplayNames.TryGetValue(agentKey, out var name) ? name : agentKey;
    }

    /// <summary>
    /// Get all display names.
    /// </summary>
    public Dictionary<string, string> DisplayNames() => AgentDisplay().DisplayNames;

    /// <summary>
    /// Get overlay instruction for a role key.
    /// </summary>
    public string OverlayInstruction(string roleKey)
    {
        var (overlays, _) = RoleOverlays();
        return overlays.TryGetValue(roleKey, out var overlay) ? overlay.Instruction : "";
    }

    /// <summary>
    /// Get counter-propose instruction.
    /// </summary>
    public string CounterProposeInstruction()
    {
        var (_, counterPropose) = RoleOverlays();
        return counterPropose;
    }

    /// <summary>
    /// Load a prompt template as raw text.
    /// </summary>
    public string LoadPromptRaw(string templatePath)
    {
        var path = Path.Combine(_templateDir, templatePath);
        return File.ReadAllText(path);
    }

    /// <summary>
    /// Check if a template exists.
    /// </summary>
    public bool TemplateExists(string templatePath)
    {
        var path = Path.Combine(_templateDir, templatePath);
        return File.Exists(path);
    }

    private static int GetInt(Dictionary<object, object> dict, string key, int defaultValue)
    {
        if (dict.TryGetValue(key, out var value))
        {
            if (value is int i) return i;
            if (int.TryParse(value?.ToString(), out var parsed)) return parsed;
        }
        return defaultValue;
    }

    private static double GetDouble(Dictionary<object, object> dict, string key, double defaultValue)
    {
        if (dict.TryGetValue(key, out var value))
        {
            if (value is double d) return d;
            if (double.TryParse(value?.ToString(), out var parsed)) return parsed;
        }
        return defaultValue;
    }

    private static string GetString(Dictionary<object, object> dict, string key, string defaultValue)
    {
        if (dict.TryGetValue(key, out var value))
        {
            return value?.ToString() ?? defaultValue;
        }
        return defaultValue;
    }

    private static bool GetBool(Dictionary<object, object> dict, string key, bool defaultValue)
    {
        if (dict.TryGetValue(key, out var value))
        {
            if (value is bool b) return b;
            if (bool.TryParse(value?.ToString(), out var parsed)) return parsed;
        }
        return defaultValue;
    }
}
