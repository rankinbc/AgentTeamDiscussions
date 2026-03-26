using EngineStandalone.Config;
using Xunit;

namespace EngineStandalone.Tests;

public class ConfigLoaderTests
{
    private readonly string _configDir;
    private readonly string _templateDir;

    public ConfigLoaderTests()
    {
        // Use the actual config from the engine_standalone directory
        var baseDir = Path.GetFullPath(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "..", "..", "..", "..", ".."));
        _configDir = Path.Combine(baseDir, "config");
        _templateDir = Path.Combine(baseDir, "templates");
    }

    [Fact]
    public void Defaults_LoadsTimeouts()
    {
        // Skip if config not available
        if (!Directory.Exists(_configDir))
        {
            return;
        }

        // Arrange
        var loader = new ConfigLoader(_configDir, _templateDir);

        // Act
        var defaults = loader.Defaults();

        // Assert
        Assert.True(defaults.Timeouts.Default > 0);
        Assert.True(defaults.Timeouts.Discussion > 0);
    }

    [Fact]
    public void Defaults_LoadsTruncationSettings()
    {
        // Skip if config not available
        if (!Directory.Exists(_configDir))
        {
            return;
        }

        // Arrange
        var loader = new ConfigLoader(_configDir, _templateDir);

        // Act
        var defaults = loader.Defaults();

        // Assert
        Assert.True(defaults.Truncation.PriorSpecs > 0);
        Assert.True(defaults.Truncation.DesignDocChain > 0);
    }

    [Fact]
    public void AgentDisplay_LoadsDisplayNames()
    {
        // Skip if config not available
        if (!Directory.Exists(_configDir))
        {
            return;
        }

        // Arrange
        var loader = new ConfigLoader(_configDir, _templateDir);

        // Act
        var display = loader.AgentDisplay();

        // Assert
        Assert.NotEmpty(display.DisplayNames);
    }

    [Fact]
    public void DisplayName_ReturnsNameForKnownAgent()
    {
        // Skip if config not available
        if (!Directory.Exists(_configDir))
        {
            return;
        }

        // Arrange
        var loader = new ConfigLoader(_configDir, _templateDir);

        // Act
        var name = loader.DisplayName("cognitive_architect");

        // Assert
        Assert.NotEqual("cognitive_architect", name); // Should return display name, not key
        Assert.Contains("Architect", name);
    }

    [Fact]
    public void DisplayName_ReturnsKeyForUnknownAgent()
    {
        // Skip if config not available
        if (!Directory.Exists(_configDir))
        {
            return;
        }

        // Arrange
        var loader = new ConfigLoader(_configDir, _templateDir);

        // Act
        var name = loader.DisplayName("nonexistent_agent");

        // Assert
        Assert.Equal("nonexistent_agent", name);
    }

    [Fact]
    public void RoleOverlays_LoadsOverlays()
    {
        // Skip if config not available
        if (!Directory.Exists(_configDir))
        {
            return;
        }

        // Arrange
        var loader = new ConfigLoader(_configDir, _templateDir);

        // Act
        var (overlays, counterPropose) = loader.RoleOverlays();

        // Assert
        Assert.NotEmpty(overlays);
        Assert.NotEmpty(counterPropose);
    }

    [Fact]
    public void LoadPromptRaw_LoadsSynthesisPrompt()
    {
        // Skip if templates not available
        if (!Directory.Exists(_templateDir))
        {
            return;
        }

        // Arrange
        var loader = new ConfigLoader(_configDir, _templateDir);

        // Act
        var prompt = loader.LoadPromptRaw("prompts/synthesis.md.j2");

        // Assert
        Assert.NotEmpty(prompt);
        Assert.Contains("design doc", prompt.ToLower());
    }
}
