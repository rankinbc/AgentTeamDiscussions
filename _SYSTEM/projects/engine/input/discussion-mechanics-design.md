# Discussion Mechanics: What Format Produces the Best Outputs?

You are agents in a multi-agent discussion system. Your human operator uses your outputs as source material to build software, design systems, and make product decisions. He doesn't want academic reports — he wants outputs he can turn directly into code, specs, and decisions.

Right now you discuss topics in fixed rounds: each agent proposes once, critiques once, evaluates once. A synthesis step merges your responses into a design document. This session is about whether that structure is the right one.

## What's Already Decided

- Sessions are unattended — no human moderator between rounds
- Each question produces a design document + transcript
- Decisions made in one question are visible as context in subsequent questions
- The goal is useful output, not thoroughness for its own sake

## Open Questions

1. **How many times should each agent speak per question, and in what sequence?** The current model is one turn per agent per round. Would speaking more than once per question produce better output, or just more words? If agents speak multiple times on a single question, what should change between their first and second contribution — should they be responding to what others said, updating their own position, or doing something else entirely? Be specific about what a better turn structure looks like and why it would produce better output than the current model.

2. **Should agents respond directly to each other by name, or only to the question?** Right now agents see what previous agents said but address the question, not each other. Would direct address — "I disagree with what the Architect said because..." — produce sharper thinking or just noise? What are the failure modes of each approach? If direct address is valuable, which rounds or moments should allow it, and which should not?

3. **What should each stage be trying to accomplish, and how should the prompt or context make that purpose unmistakable?** Right now "propose" means say what you think, "critique" means poke holes, "evaluate" means assess. But these stages often blur together. What is the *single job* of each stage, and what would need to be different — in what you're told, what context you see, what constraints you're under — to make each stage do its actual job instead of producing another variation of the same response?

4. **What is the most useful shape of output for a human building things from your discussion?** Right now you produce a design document with a decisions section, contested points, and open questions. Is that the right artifact? If the goal is something a developer can build from, what would the ideal document contain that the current format misses, and what does the current format include that wastes space? Describe the ideal output format as concretely as you can.
