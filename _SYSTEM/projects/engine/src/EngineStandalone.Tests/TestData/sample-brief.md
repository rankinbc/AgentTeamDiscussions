# Sample Discussion Brief

This is a test brief for unit testing the parser.

## What's Already Decided

- The system uses async processing
- Output is written to markdown files
- Claude CLI is used for LLM calls

## Open Questions

1. **How should timeouts be handled?**
When a Claude CLI call times out, should the system retry automatically or fail immediately? Consider both user experience and resource usage.

2. **What format should the Morning Brief use?**
The Morning Brief summarizes decisions from the overnight session. Should it be a simple bullet list or a structured document with sections?

3. **How should prior context be truncated?**
When chaining design docs forward, how much context should be included? Too much may exceed token limits, too little may lose important decisions.
