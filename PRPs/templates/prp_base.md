---
name: "AgentTeamDiscussions PRP Base Template"
description: "Template for generating comprehensive PRPs for the AgentTeamDiscussions multi-agent orchestration platform"
---

## Purpose

Template optimized for AI agents to implement features in the AgentTeamDiscussions platform with sufficient context and self-validation capabilities to achieve working code through iterative refinement.

## Core Principles

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Research First**: Do extensive web research and codebase exploration before implementation
3. **Validation Loops**: Provide executable tests/lints the AI can run and fix
4. **Information Dense**: Use keywords and patterns from the codebase
5. **Progressive Success**: Start simple, validate, then enhance
6. **Global Rules**: Follow all rules in CLAUDE.md and zone-specific CLAUDE.md files

---

## Goal
[What needs to be built — be specific about the end state and desires]

## Why
- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What
[User-visible behavior and technical requirements]

### Success Criteria
- [ ] [Specific measurable outcomes]

## All Needed Context

### Documentation & References (MUST READ)
```yaml
# CODEBASE CONTEXT — Zone-specific rules
- file: CLAUDE.md
  why: Hard rules, project map, zone routing

- file: _SYSTEM/projects/engine/CLAUDE.md
  why: Engine-specific rules, architecture, CLI commands, test patterns

- file: _SYSTEM/data/CLAUDE.md
  why: Data zone rules for agent/team YAML definitions

- file: PLANNING.md
  why: Architecture overview, tech stack, style conventions, constraints

# IMPLEMENTATION REFERENCES
- file: [path/to/relevant/file.cs or .tsx or .yaml]
  why: [Specific pattern to follow, gotchas to avoid]

# EXTERNAL DOCUMENTATION (from web research)
- url: [Official docs URL]
  why: [Specific sections/methods you'll need]

- url: [Best practices guide]
  why: [Patterns and conventions to follow]

# PROJECT-SPECIFIC DOCS
- docfile: [PRPs/ai_docs/file.md]
  why: [Docs that have been added to the project]
```

### Current Codebase Tree (relevant zone)
```bash

```

### Desired Codebase Tree with files to add and responsibility
```bash

```

### Known Gotchas & Codebase Quirks
```csharp
// CRITICAL: Agent YAML is loaded once at session start and cached — never modify mid-session
// CRITICAL: All config changes go through defaults.yaml, not C# code
// CRITICAL: <!-- complete --> markers are crash recovery — never delete them

// PATTERN: ClaudeRunner has built-in retry — don't add duplicate retry logic
// PATTERN: Error responses from Claude are prefixed with "[" — check via string prefix
// PATTERN: Speaking order scored by assertiveness * 0.5 + intensity * 0.3 + stubbornness * 0.2

// ZONE: Agent/team YAML authoritative source is _SYSTEM/data/, not projects/engine/data/
// ZONE: Modes are defined in team YAML, not in C# code
// ZONE: Use DI in Program.cs for new services — follow existing registrations

// UI: React 19 + Vite — HMR may need manual refresh for SSE-related changes
// UI: Tailwind CSS 4 for styling — use utility classes, not custom CSS
```

## Implementation Blueprint

### Data Models and Structure

Create or modify core data models to ensure type safety and consistency.
```
Examples:
 - C# classes or record types in src/EngineStandalone/
 - TypeScript interfaces in ui/src/
 - YAML schema additions in config/ or data/
 - xUnit test data builders in src/EngineStandalone.Tests/
```

### List of Tasks (in execution order)

```yaml
Task 1:
MODIFY src/EngineStandalone/[File].cs:
  - FIND pattern: "class ExistingClass"
  - INJECT after line containing "public void Method"
  - PRESERVE existing method signatures

CREATE src/EngineStandalone/[NewFile].cs:
  - MIRROR pattern from: src/EngineStandalone/[SimilarFile].cs
  - MODIFY class name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...
```

### Per-Task Pseudocode (as needed)
```csharp
// Task 1
// Pseudocode with CRITICAL details — don't write entire code
public async Task<Result> NewFeature(string param)
{
    // PATTERN: Always validate input first
    var validated = Validate(param);

    // GOTCHA: ClaudeRunner has retry logic built in — don't add your own
    var response = await _claudeRunner.RunAsync(systemPrompt, payload, timeout);

    // PATTERN: Check for error responses
    if (response.StartsWith("["))
        throw new ClaudeRunnerException(response);

    return FormatResponse(response);
}
```

### Integration Points
```yaml
CONFIG:
  - add to: config/defaults.yaml
  - pattern: "new_feature_timeout: 60"

DI CONTAINER:
  - add to: Program.cs
  - pattern: "builder.Services.AddSingleton<INewFeature, NewFeature>();"

YAML DATA:
  - add to: _SYSTEM/data/teams/team-name.yaml
  - pattern: "new mode definition under modes:"

UI COMPONENT:
  - add to: ui/src/components/
  - pattern: "React functional component with TypeScript props"

SSE EVENTS:
  - add to: LiveServer.cs
  - pattern: "app.MapGet('/api/new-endpoint', handler)"

TESTS:
  - add to: src/EngineStandalone.Tests/
  - pattern: "xUnit [Fact] methods mirroring existing test structure"
```

## Validation Loop

### Level 1: Build & Type Safety
```bash
# Run these FIRST — fix any errors before proceeding
cd _SYSTEM/projects/engine
dotnet build

# For UI changes:
cd _SYSTEM/projects/engine/ui
npm run build

# Expected: No errors. If errors, READ the error and fix.
```

### Level 2: Unit Tests (follow existing xUnit patterns)
```csharp
// CREATE tests in src/EngineStandalone.Tests/ following existing patterns:
[Fact]
public void NewFeature_HappyPath_ReturnsExpected()
{
    // Arrange, Act, Assert
}

[Fact]
public void NewFeature_InvalidInput_ThrowsException()
{
    Assert.Throws<ArgumentException>(() => ...);
}

[Fact]
public void NewFeature_EdgeCase_HandlesGracefully()
{
    // Test boundary conditions
}
```

```bash
# Run and iterate until passing:
cd _SYSTEM/projects/engine
dotnet test

# If failing: Read error, understand root cause, fix code, re-run
```

### Level 3: Integration Test
```bash
# Start the engine with your feature
cd _SYSTEM/projects/engine
dotnet run --project src/EngineStandalone -- new --topic "Test topic" --live

# Start UI (if applicable)
cd _SYSTEM/projects/engine/ui
npm run dev
# Open http://localhost:5173

# Verify: Session runs to completion, output files created, dashboard renders correctly
```

## Final Validation Checklist

- [ ] Engine builds cleanly: `dotnet build`
- [ ] All tests pass (existing + new): `dotnet test`
- [ ] UI builds cleanly (if changed): `npm run build`
- [ ] No warnings treated as errors
- [ ] Manual test successful: [specific scenario]
- [ ] Error cases handled gracefully
- [ ] YAML config changes documented
- [ ] CLAUDE.md hard rules respected (all zones)
- [ ] TASK.md updated with completed work

---

## Anti-Patterns to Avoid

- Don't create new patterns when existing ones work — follow established codebase conventions
- Don't skip validation because "it should work"
- Don't ignore failing tests — fix them
- Don't hardcode values that belong in config/defaults.yaml
- Don't modify agent YAML at runtime — loaded once and cached
- Don't put data files in projects/engine/ — use _SYSTEM/data/
- Don't catch all exceptions — be specific
- Don't add modes in C# code — modes are YAML team-level config
- Don't skip web research — understand libraries and patterns deeply first
- Don't reorganize files during normal work — only when explicitly asked
