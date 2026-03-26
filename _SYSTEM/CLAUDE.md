# _SYSTEM

All active application code, data, and configuration for AgentTeamDiscussions.

---

## Structure

```
projects/
  engine/               → C# .NET 8 discussion engine + React UI
    src/                → C# source (EngineStandalone solution)
    ui/                 → React + Vite live dashboard
    config/             → YAML config (defaults, agent display, role overlays)
    data/               → Agent/team YAML definitions (engine-local copy)
    templates/          → Prompt templates
    input/              → Brief files (session input)
    output/             → Session output (design docs, ledger, Morning Brief)
data/                   → Shared agent/team YAML definitions + briefs
docs/                   → Design documentation
```

---

## Running

```bash
cd projects/engine
dotnet build
dotnet run --project src/EngineStandalone -- new             # interactive
dotnet run --project src/EngineStandalone -- new --live      # with SSE dashboard
dotnet run --project src/EngineStandalone -- input/brief.md  # from brief file
dotnet test                                                   # run tests
```

## Reference

Read `projects/engine/CLAUDE.md` for full engine documentation (commands, flags, architecture, session format).
