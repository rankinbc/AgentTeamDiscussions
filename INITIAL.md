# Feature Request

## FEATURE:

**What needs to be built?** [Be specific about the end state — what should exist when this is done]

---

## TEMPLATE PURPOSE:

**What specific use case should this feature solve?**

**Example:** "Add a new discussion mode that runs a rapid-fire brainstorming round before the standard propose/critique/evaluate cycle"

**Your purpose:** [Be very specific about what this feature enables]

---

## CORE FEATURES:

**What are the essential capabilities this feature must include?**

**Example for a new discussion mode:**
- New mode definition in team YAML
- Round structure with agent assignments
- Role overlay configuration
- Integration with existing SessionRunner
- Live dashboard support via SSE

**Your core features:** [List the specific capabilities]

---

## EXAMPLES TO FOLLOW:

**What existing code patterns or files should be used as reference?**

**Example:**
- `_SYSTEM/projects/engine/src/EngineStandalone/Discussion/DiscussionEngine.cs` — round orchestration pattern
- `_SYSTEM/data/teams/beta-agents.yaml` — mode definition structure
- `_SYSTEM/projects/engine/config/role_overlays.yaml` — overlay configuration pattern
- `_SYSTEM/projects/engine/src/EngineStandalone.Tests/` — xUnit test patterns

**Your examples:** [Point to specific files and explain what pattern to follow from each]

---

## DOCUMENTATION TO RESEARCH:

**What documentation should be thoroughly researched and referenced?**

**Example:**
- .NET 8 ASP.NET Web SDK docs for SSE endpoints
- YamlDotNet serialization patterns
- Scriban template syntax for prompt construction
- xUnit testing best practices

**Your documentation:** [List specific URLs and documentation sections to research deeply]

---

## DEVELOPMENT PATTERNS:

**What specific development patterns, project structures, or workflows should be followed?**

**Example:**
- How existing modes are defined in team YAML and consumed by DiscussionEngine
- How agent speaking order is computed and applied
- How SessionPersistence handles crash recovery for new round types
- How LiveServer emits SSE events for the UI

**Your development patterns:** [Specify the workflow and organizational patterns to follow]

---

## SECURITY & BEST PRACTICES:

**What are the critical constraints and best practices for this feature?**

**Example:**
- Agent YAML is loaded once at session start — never modify at runtime
- All config changes go through defaults.yaml, not C# code
- Use existing DI patterns in Program.cs for new services
- Follow existing error response patterns (prefix check for `[`)

**Your considerations:** [List technology-specific constraints and practices]

---

## COMMON GOTCHAS:

**What are the typical pitfalls or edge cases for this area of the codebase?**

**Example:**
- ClaudeRunner has built-in retry logic — don't add duplicate retries
- Speaking order scoring uses specific weights (assertiveness * 0.5 + intensity * 0.3 + stubbornness * 0.2)
- `<!-- complete -->` markers are crash recovery — never delete them
- Round health checks can cascade-fail a question if too many agents error

**Your gotchas:** [Identify the specific challenges and edge cases]

---

## VALIDATION REQUIREMENTS:

**What specific validation, testing, or quality checks are needed?**

**Example:**
- xUnit tests for new mode loading and round execution
- Engine builds cleanly: `dotnet build`
- All existing tests still pass: `dotnet test`
- UI builds if changed: `cd ui && npm run build`
- Manual test: run a session with the new mode end-to-end

**Your validation requirements:** [Specify the testing and validation needed]

---

## INTEGRATION POINTS:

**What parts of the system does this feature touch?**

**Example:**
- `config/defaults.yaml` — new timeout settings
- `Program.cs` — DI registration for new services
- `data/teams/*.yaml` — new mode definitions
- `ui/src/components/` — new dashboard components for the feature
- `LiveServer.cs` — new SSE event types

**Your integration points:** [List the key integration areas]

---

## ADDITIONAL NOTES:

**Any other specific requirements, constraints, or considerations?**

**Example:** "Must work with both beta-agents and ev18hornet teams"
**Example:** "Should degrade gracefully if an agent times out mid-round"

**Your additional notes:** [Any other important considerations]

---

## COMPLEXITY LEVEL:

- [ ] **Small** — Single file change, isolated scope
- [ ] **Medium** — Multiple files, follows existing patterns closely
- [ ] **Large** — New subsystem, architectural decisions needed
- [ ] **Complex** — Cross-zone changes, new patterns required

**Your choice:** [Select and explain why]

---

**REMINDER: Be as specific as possible in each section. The more detailed your INITIAL.md, the better the generated PRP will be. This is where you front-load all your requirements and context.**
