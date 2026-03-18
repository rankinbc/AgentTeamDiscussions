# Test Brief

## What's Already Decided

- V1 is a Python CLI that spawns stateless claude -p subprocess calls
- Structured 3-round discussions: propose, critique, evaluate, then synthesize
- Session output goes to a timestamped folder

## Open Questions

1. **How should the orchestrator handle a question that produces contradictory proposals?** When two proposers generate fundamentally incompatible designs, what does the synthesis step do? Does it pick a winner, merge them, or present both with a recommendation? Design the rule.
