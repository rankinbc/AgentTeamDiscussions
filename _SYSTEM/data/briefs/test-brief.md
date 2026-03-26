## What's Already Decided

- The system runs multi-agent discussions using the Claude CLI
- Sessions are stored as markdown files with completion markers
- Agents are configured via YAML files

## Open Questions

1. **How should agent responses be truncated for long discussions?** As discussions grow, context windows fill up. What's the right strategy for deciding what history each agent sees — full history, sliding window, or smart summarization?
