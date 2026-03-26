// Deserializes agent and team YAML files into AgentConfig/TeamConfig objects.
// Team YAMLs reference agents by file (e.g. file: ev18hornet__flight_dreamer.yaml)
// or define them inline. Agents are keyed by agent_key for round assignment lookup.
using EngineStandalone.Abstractions;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace EngineStandalone.Agents;

/// <summary>
/// Loads agent and team configurations from YAML files.
/// </summary>
public class AgentLoader : IAgentLoader
{
    private readonly string _agentsDir;
    private readonly string _teamsDir;
    private readonly IDeserializer _deserializer;

    public AgentLoader(string dataDir)
    {
        _agentsDir = Path.Combine(dataDir, "agents");
        _teamsDir = Path.Combine(dataDir, "teams");
        _deserializer = new DeserializerBuilder()
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .IgnoreUnmatchedProperties()
            .Build();
    }

    /// <summary>
    /// Load an agent from a specific YAML file path.
    /// </summary>
    public AgentConfig LoadAgent(string configPath)
    {
        if (!File.Exists(configPath))
            throw new FileNotFoundException($"Agent config not found: {configPath}");

        var yaml = File.ReadAllText(configPath);
        var raw = _deserializer.Deserialize<Dictionary<string, object>>(yaml);

        return ParseAgentConfig(raw);
    }

    /// <summary>
    /// Load an agent by its key from the agents directory.
    /// </summary>
    public AgentConfig LoadAgentByKey(string agentKey)
    {
        if (!Directory.Exists(_agentsDir))
            throw new DirectoryNotFoundException($"Agents directory not found: {_agentsDir}");

        // Try exact match first, then fall back to prefix__key pattern
        var exactPath = Path.Combine(_agentsDir, $"{agentKey}.yaml");
        if (File.Exists(exactPath))
            return LoadAgent(exactPath);

        // Try pattern match (e.g., beta-agents__cognitive_architect.yaml)
        var files = Directory.GetFiles(_agentsDir, $"*__{agentKey}.yaml");
        if (files.Length > 0)
            return LoadAgent(files[0]);

        throw new FileNotFoundException($"No agent file found for key '{agentKey}' in {_agentsDir}");
    }

    /// <summary>
    /// Load a team by name from the teams directory.
    /// </summary>
    public TeamConfig LoadTeamByName(string teamName)
    {
        var teamPath = Path.Combine(_teamsDir, $"{teamName}.yaml");
        return LoadTeam(teamPath);
    }

    /// <summary>
    /// Load a team from a specific YAML file path.
    /// </summary>
    public TeamConfig LoadTeam(string configPath)
    {
        if (!File.Exists(configPath))
            throw new FileNotFoundException($"Team config not found: {configPath}");

        var yaml = File.ReadAllText(configPath);
        var raw = _deserializer.Deserialize<Dictionary<string, object>>(yaml);
        var teamDir = Path.GetDirectoryName(configPath)!;

        var team = new TeamConfig();

        if (raw.TryGetValue("agents", out var agentsObj) && agentsObj is List<object> agentsList)
        {
            foreach (var item in agentsList)
            {
                if (item is Dictionary<object, object> agentDict)
                {
                    var agentKey = GetString(agentDict, "agent_key", "");
                    var agentFile = GetString(agentDict, "file", null);

                    // Resolve agent: file reference takes priority, otherwise load by key
                    AgentConfig agent;
                    if (!string.IsNullOrEmpty(agentFile))
                    {
                        // Try team directory first, then agents directory
                        var agentPath = Path.Combine(teamDir, agentFile);
                        if (!File.Exists(agentPath))
                            agentPath = Path.Combine(_agentsDir, agentFile);

                        if (!File.Exists(agentPath))
                            throw new FileNotFoundException($"Agent file '{agentFile}' not found in team dir ({teamDir}) or agents dir ({_agentsDir})");

                        agent = LoadAgent(agentPath);
                    }
                    else
                    {
                        agent = LoadAgentByKey(agentKey);
                    }

                    team.Agents[agentKey] = agent;
                }
            }
        }
        else if (raw.TryGetValue("agents", out var agentsDict) && agentsDict is Dictionary<object, object> agentsDictInline)
        {
            // Handle inline agent definitions
            foreach (var kvp in agentsDictInline)
            {
                var agentKey = kvp.Key.ToString()!;
                if (kvp.Value is Dictionary<object, object> agentData)
                {
                    team.Agents[agentKey] = ParseAgentConfigFromDict(agentData);
                }
            }
        }

        // Parse modes (round structures) from team YAML
        if (raw.TryGetValue("modes", out var modesObj) && modesObj is Dictionary<object, object> modesDict)
        {
            foreach (var modeKvp in modesDict)
            {
                var modeName = modeKvp.Key.ToString()!;
                if (modeKvp.Value is Dictionary<object, object> modeData)
                {
                    var mode = new TeamMode
                    {
                        Description = GetString(modeData, "description", ""),
                    };

                    if (modeData.TryGetValue("groups", out var groupsObj) && groupsObj is Dictionary<object, object> groupsDict)
                    {
                        foreach (var gKvp in groupsDict)
                        {
                            var roundName = gKvp.Key.ToString()!;
                            var agents = new List<string>();
                            if (gKvp.Value is List<object> agentList)
                            {
                                agents.AddRange(agentList.Select(a => a.ToString()!));
                            }
                            mode.Groups[roundName] = agents;
                        }
                    }

                    if (modeData.TryGetValue("agent_roles", out var rolesObj) && rolesObj is Dictionary<object, object> rolesDict)
                    {
                        foreach (var rKvp in rolesDict)
                        {
                            mode.AgentRoles[rKvp.Key.ToString()!] = rKvp.Value?.ToString() ?? "";
                        }
                    }

                    team.Modes[modeName] = mode;
                }
            }
        }

        // Parse default_mode
        if (raw.TryGetValue("default_mode", out var defaultModeObj))
        {
            team.DefaultMode = defaultModeObj?.ToString() ?? "default";
        }

        return team;
    }

    /// <summary>
    /// List all available teams.
    /// </summary>
    public List<(string Name, string File, int AgentCount)> ListTeams()
    {
        var result = new List<(string, string, int)>();

        if (!Directory.Exists(_teamsDir))
            return result;

        foreach (var file in Directory.GetFiles(_teamsDir, "*.yaml").OrderBy(f => f))
        {
            var yaml = File.ReadAllText(file);
            var raw = _deserializer.Deserialize<Dictionary<string, object>>(yaml);

            var name = GetStringFromObjectDict(raw, "name", Path.GetFileNameWithoutExtension(file));
            var agentCount = 0;
            if (raw.TryGetValue("agents", out var agents))
            {
                if (agents is List<object> list) agentCount = list.Count;
                else if (agents is Dictionary<object, object> dict) agentCount = dict.Count;
            }

            result.Add((name, Path.GetFileName(file), agentCount));
        }

        return result;
    }

    /// <summary>
    /// List all available agents.
    /// </summary>
    public List<(string Id, string Name, string Key, string File)> ListAgents()
    {
        var result = new List<(string, string, string, string)>();

        if (!Directory.Exists(_agentsDir))
            return result;

        foreach (var file in Directory.GetFiles(_agentsDir, "*.yaml").OrderBy(f => f))
        {
            var yaml = File.ReadAllText(file);
            var raw = _deserializer.Deserialize<Dictionary<string, object>>(yaml);

            var id = GetStringFromObjectDict(raw, "id", "");
            var name = GetStringFromObjectDict(raw, "name", Path.GetFileNameWithoutExtension(file));
            var fileName = Path.GetFileNameWithoutExtension(file);
            var key = fileName.Contains("__") ? fileName.Split("__").Last() : fileName;

            result.Add((id, name, key, Path.GetFileName(file)));
        }

        return result;
    }

    private AgentConfig ParseAgentConfig(Dictionary<string, object> raw)
    {
        var config = new AgentConfig
        {
            Id = GetStringFromObjectDict(raw, "id", Guid.NewGuid().ToString()),
            Name = GetStringFromObjectDict(raw, "name", ""),
            Description = GetStringFromObjectDict(raw, "description", "")
        };

        if (raw.TryGetValue("personality", out var personalityObj) && personalityObj is Dictionary<object, object> personality)
        {
            config.Personality = ParsePersonalityConfig(personality);
        }

        if (raw.TryGetValue("position", out var positionObj) && positionObj is Dictionary<object, object> position)
        {
            config.Position = ParsePositionConfig(position);
        }

        if (raw.TryGetValue("technique", out var techObj) && techObj is Dictionary<object, object> technique)
        {
            config.Technique = ParseTechniqueConfig(technique);
        }

        if (raw.TryGetValue("anti_slop", out var antiSlopObj) && antiSlopObj is Dictionary<object, object> antiSlop)
        {
            config.AntiSlop = ParseAntiSlopConfig(antiSlop);
        }

        if (raw.TryGetValue("voice", out var voiceObj) && voiceObj is Dictionary<object, object> voice)
        {
            config.Voice = ParseVoiceConfig(voice);
        }

        if (raw.TryGetValue("output", out var outputObj) && outputObj is Dictionary<object, object> output)
        {
            config.Output = ParseOutputConfig(output);
        }

        return config;
    }

    private AgentConfig ParseAgentConfigFromDict(Dictionary<object, object> raw)
    {
        var converted = raw.ToDictionary(
            kvp => kvp.Key.ToString()!,
            kvp => kvp.Value!
        );
        return ParseAgentConfig(converted);
    }

    private PersonalityConfig ParsePersonalityConfig(Dictionary<object, object> raw)
    {
        var config = new PersonalityConfig
        {
            Assertiveness = GetDouble(raw, "assertiveness", 0.5),
            CreativityTemp = GetDouble(raw, "creativity_temp", 0.5),
            RiskTolerance = GetDouble(raw, "risk_tolerance", 0.5),
            AttentionSpan = GetDouble(raw, "attention_span", 0.5),
            Stubbornness = GetDouble(raw, "stubbornness", 0.5),
            IdeaReceptivity = GetDouble(raw, "idea_receptivity", 0.5),
            Bluntness = GetDouble(raw, "bluntness", 0.5),
            Patience = GetDouble(raw, "patience", 0.5)
        };

        var cogStyleStr = GetString(raw, "cognitive_style", "analytical");
        config.CognitiveStyle = Enum.TryParse<CognitiveStyle>(cogStyleStr, true, out var cogStyle)
            ? cogStyle : CognitiveStyle.Analytical;

        var emBaseStr = GetString(raw, "emotional_baseline", "neutral");
        config.EmotionalBaseline = Enum.TryParse<EmotionalBaseline>(emBaseStr, true, out var emBase)
            ? emBase : EmotionalBaseline.Neutral;

        if (raw.TryGetValue("domain_affinities", out var daObj) && daObj is List<object> daList)
        {
            config.DomainAffinities = daList.Select(x => x.ToString()!).ToList();
        }

        return config;
    }

    private PositionConfig ParsePositionConfig(Dictionary<object, object> raw)
    {
        var config = new PositionConfig
        {
            Role = GetString(raw, "role", "participant"),
            Intensity = GetDouble(raw, "intensity", 0.5)
        };

        if (raw.TryGetValue("drives", out var drivesObj) && drivesObj is List<object> drivesList)
        {
            config.Drives = drivesList.Select(x => x.ToString()!).ToList();
        }

        if (raw.TryGetValue("pushback_on", out var pbObj) && pbObj is List<object> pbList)
        {
            config.PushbackOn = pbList.Select(x => x.ToString()!).ToList();
        }

        return config;
    }

    private TechniqueConfig ParseTechniqueConfig(Dictionary<object, object> raw)
    {
        var config = new TechniqueConfig
        {
            Primary = GetString(raw, "primary", "none"),
            StyleDescription = GetString(raw, "style_description", "")
        };

        if (raw.TryGetValue("behaviors", out var behavObj) && behavObj is List<object> behavList)
        {
            config.Behaviors = behavList.Select(x => x.ToString()!).ToList();
        }

        return config;
    }

    private AntiSlopConfig ParseAntiSlopConfig(Dictionary<object, object> raw)
    {
        return new AntiSlopConfig
        {
            AgreementTax = GetBool(raw, "agreement_tax", true),
            PerspectiveEnforcement = GetBool(raw, "perspective_enforcement", true),
            DevilsAdvocateDuty = GetBool(raw, "devils_advocate_duty", false),
            UncomfortableIdeaQuota = GetInt(raw, "uncomfortable_idea_quota", 0),
            DomainPivotTrigger = GetBool(raw, "domain_pivot_trigger", false)
        };
    }

    private VoiceConfig ParseVoiceConfig(Dictionary<object, object> raw)
    {
        var config = new VoiceConfig
        {
            Tone = GetString(raw, "tone", "professional")
        };

        var brevityStr = GetString(raw, "brevity", "normal");
        config.Brevity = Enum.TryParse<Brevity>(brevityStr, true, out var brevity)
            ? brevity : Brevity.Normal;

        if (raw.TryGetValue("vocabulary_hints", out var vhObj) && vhObj is List<object> vhList)
        {
            config.VocabularyHints = vhList.Select(x => x.ToString()!).ToList();
        }

        if (raw.TryGetValue("anti_patterns", out var apObj) && apObj is List<object> apList)
        {
            config.AntiPatterns = apList.Select(x => x.ToString()!).ToList();
        }

        return config;
    }

    private OutputConfig ParseOutputConfig(Dictionary<object, object> raw)
    {
        var config = new OutputConfig();

        var levelStr = GetString(raw, "operating_level", "requirements");
        config.OperatingLevel = Enum.TryParse<OperatingLevel>(levelStr, true, out var level)
            ? level : OperatingLevel.Requirements;

        var jobStr = GetString(raw, "job", "propose");
        config.Job = Enum.TryParse<JobType>(jobStr, true, out var job)
            ? job : JobType.Propose;

        return config;
    }

    private static double GetDouble(Dictionary<object, object> dict, string key, double defaultValue)
    {
        if (dict.TryGetValue(key, out var value))
        {
            if (value is double d) return d;
            if (value is int i) return i;
            if (double.TryParse(value?.ToString(), out var parsed)) return parsed;
        }
        return defaultValue;
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

    private static bool GetBool(Dictionary<object, object> dict, string key, bool defaultValue)
    {
        if (dict.TryGetValue(key, out var value))
        {
            if (value is bool b) return b;
            if (bool.TryParse(value?.ToString(), out var parsed)) return parsed;
        }
        return defaultValue;
    }

    private static string GetString(Dictionary<object, object> dict, string key, string? defaultValue)
    {
        if (dict.TryGetValue(key, out var value))
        {
            return value?.ToString() ?? defaultValue ?? "";
        }
        return defaultValue ?? "";
    }

    private static string GetStringFromObjectDict(Dictionary<string, object> dict, string key, string defaultValue)
    {
        if (dict.TryGetValue(key, out var value))
        {
            return value?.ToString() ?? defaultValue;
        }
        return defaultValue;
    }
}
