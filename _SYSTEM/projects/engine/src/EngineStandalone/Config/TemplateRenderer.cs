// TemplateRenderer.cs — Scriban template engine (Jinja2-compatible) for prompt templates.
// Templates live in templates/prompts/ and templates/evaluation/.
// Compiled templates are cached to avoid re-parsing on every LLM call.

using Scriban;
using Scriban.Runtime;

namespace EngineStandalone.Config;

/// <summary>
/// Renders Scriban/Liquid templates (compatible with Jinja2 syntax for most cases).
/// </summary>
public class TemplateRenderer
{
    private readonly string _templateDir;
    private readonly Dictionary<string, Template> _cache = new();

    public TemplateRenderer(string templateDir)
    {
        _templateDir = templateDir;
    }

    /// <summary>
    /// Render a template with the given context.
    /// </summary>
    public string Render(string templatePath, Dictionary<string, object?> context)
    {
        var template = GetTemplate(templatePath);

        var scriptObject = new ScriptObject();
        foreach (var kvp in context)
        {
            scriptObject.Add(kvp.Key, kvp.Value);
        }

        var templateContext = new TemplateContext();
        templateContext.PushGlobal(scriptObject);
        templateContext.MemberRenamer = member => member.Name;

        return template.Render(templateContext);
    }

    /// <summary>
    /// Render a template string directly.
    /// </summary>
    public string RenderString(string templateContent, Dictionary<string, object?> context)
    {
        var template = Template.Parse(templateContent);

        var scriptObject = new ScriptObject();
        foreach (var kvp in context)
        {
            scriptObject.Add(kvp.Key, kvp.Value);
        }

        var templateContext = new TemplateContext();
        templateContext.PushGlobal(scriptObject);
        templateContext.MemberRenamer = member => member.Name;

        return template.Render(templateContext);
    }

    /// <summary>
    /// Load a raw template file without rendering.
    /// </summary>
    public string LoadRaw(string templatePath)
    {
        var fullPath = Path.Combine(_templateDir, templatePath);
        return File.ReadAllText(fullPath);
    }

    private Template GetTemplate(string templatePath)
    {
        if (_cache.TryGetValue(templatePath, out var cached))
            return cached;

        var fullPath = Path.Combine(_templateDir, templatePath);
        var content = File.ReadAllText(fullPath);
        var template = Template.Parse(content);

        if (template.HasErrors)
        {
            throw new InvalidOperationException($"Template parse errors in {templatePath}: {string.Join(", ", template.Messages)}");
        }

        _cache[templatePath] = template;
        return template;
    }
}
