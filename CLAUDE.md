# AgentTeamDiscussions - Organization System

**Project Type:** Multi-agent AI orchestration platform
**Last Updated:** 2026-03-17

---

## Your Role

You are responsible for maintaining this project's file organization. When files are created in the wrong places or the project becomes disorganized, the user will ask you to clean it up.

**DO NOT** reorganize files during normal work. Only organize when explicitly asked with `/organize` or `/status` commands.

---

## Project Overview

AgentTeamDiscussions enables autonomous AI team-to-team conversations. Two AI teams (e.g., BMAD agents and a configurable client team) communicate through an MCP message broker, each with their own context window. Teams can deliberate internally, conduct research, and produce structured artifacts (specs, PRDs, architecture docs) -- all running unattended overnight.

**Key Concepts:**
- Teams communicate only through the MCP server -- never share context
- Each team gets a deliberation budget (internal turns before responding)
- Phases (brainstorm, refine, specify, review) gate the conversation flow
- The client team is configured via simple YAML -- swap ideas by editing one file

---

## Project Structure

```
/docs/                        # Design documentation (see docs/index.md)
  ├── design_specs/           # Authoritative specs (PRD, entity model, engines)
  └── beta-agent-output/      # Test run artifacts and known issues
/projects/                    # Application code
  ├── mcp-server/             # TypeScript MCP message broker
  └── orchestrator/           # Python orchestrator driving team conversations
/config/                      # Runtime configuration
  ├── teams/                  # Team definitions (YAML)
  └── phases.yaml             # Phase definitions and transition criteria
/sessions/                    # Output per run (timestamped)
  └── {session-id}/
      ├── transcript.md       # Full cross-team conversation
      ├── internal/           # Per-team deliberation logs
      ├── decisions.json      # Logged decisions with confidence
      └── artifacts/          # Generated specs, PRDs, architecture docs
/ideas/                       # Idea seeds and brainstorm inputs
/temp/                        # Temporary files, experiments, scratch work
```

**Principles:**
- `projects/` contains deployable applications -- each is its own package
- `config/` is what users edit between runs
- `sessions/` is write-only output -- never edit, only review
- `ideas/` stores reusable idea briefs that feed into `config/teams/`
- Keep related files together within each project subfolder

---

## File Organization Rules

### Application Code
**Detection:** `.ts`, `.py`, `.js` source files, `package.json`, `requirements.txt`
**Location:** `/projects/{app-name}/`
**Note:** Each app is self-contained with its own dependencies and build config

### Team Configuration
**Detection:** YAML files defining agent personas, idea seeds, constraints
**Location:** `/config/teams/`
**Examples:** `bmad-team.yaml`, `client-team.yaml`

### Session Output
**Detection:** Transcripts, decision logs, generated artifacts from runs
**Location:** `/sessions/{session-id}/`
**Cleanup Policy:** Archive sessions older than 30 days

### Idea Files
**Detection:** Markdown or YAML files describing product ideas, briefs, constraints
**Location:** `/ideas/`

### Temporary/Experimental Files
**Detection:**
- Filenames containing: `test`, `debug`, `temp`, `scratch`, `tmp`, `example`
- Files with dates in names
- Files with version suffixes

**Location:** `/temp/`
**Cleanup Policy:** Suggest deleting files older than 7 days during organization

### Configuration Files
**Detection:** `.env`, `.config`, `settings.*`, `*.yml`, `*.toml`
**Location:** Keep in project root or `/config/`
**Protection:** Never move without explicit permission

---

## Protected Files

**NEVER move, rename, or reorganize these without explicit permission:**
- CLAUDE.md (root level)
- .gitignore, .git/ folder
- package.json, package-lock.json (within projects/)
- requirements.txt, pyproject.toml (within projects/)
- .env, .env.* environment files
- Any root-level configuration files

---

## Organization Commands

### `/organize`

Full cleanup workflow:

1. **Scan Project** - Find misplaced files
2. **Categorize** - Group by confidence level
3. **Present Recommendations** - Batch with confirmation for uncertain moves
4. **Execute** - Process and report
5. **Summary** - Stats and recommendations

### `/status`

Organizational health report with file counts, misplaced files, and recommendations.

---

## Technical Details

### MCP Server (TypeScript)
- Message broker with channels: brainstorm, internal, research, decisions, specs
- Phase state management and transition logic
- Artifact versioning and storage
- Runs as standalone server

### Orchestrator (Python)
- Drives two Claude API conversations via Max subscription OAuth
- Manages turn-taking and deliberation budgets
- Handles research sub-agent spawning
- Phase transition enforcement

### Authentication
- Uses Claude Max subscription OAuth token (not API key)
- Token sourced from environment or config

---

## Project-Specific Notes

- BMAD team personas are derived from the BMAD agent manifest at `_bmad/_config/agent-manifest.csv`
- The client team YAML is the primary user-facing config -- keep it simple and well-documented
- Session transcripts should be human-readable markdown for easy review
- Designed for extensibility: UI project, additional team types, new MCP tools can be added under `projects/`

---

## Folder Descriptions

- **projects/mcp-server/** - The MCP message broker that both teams communicate through. Handles channels, phase state, artifacts, and decision logging.
- **projects/orchestrator/** - Python application that manages the conversation loop. Creates two separate Claude conversations and routes messages between them via the MCP server.
- **config/** - All user-editable configuration. Team definitions, phase rules, and session settings.
- **sessions/** - Runtime output. Each run produces a timestamped folder with the full transcript, decisions, and any generated spec artifacts.
- **ideas/** - Reusable idea briefs. Write your product idea here, reference it from a client team config.

---

**Template Version:** 1.0
**Initialized:** 2026-03-17
