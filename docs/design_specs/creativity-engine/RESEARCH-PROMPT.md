# Research Prompt: Making AI-to-AI Discussions Genuinely Creative and Non-Homogeneous

## Context

I'm building a system where multiple AI agents (all Claude instances) have structured discussions to brainstorm and produce product specifications. The core challenge: **how do you make multiple instances of the same LLM produce genuinely different, surprising, high-quality thinking instead of converging on safe, obvious, homogeneous output?**

We've already identified several mechanisms (personality traits, positional framing, creativity techniques, anti-slop mechanisms). This research should go DEEPER and WIDER -- into fields beyond AI/LLM that have solved similar problems.

## What I Need

Research and produce findings on the following topics. For each finding, explain the concept, where it comes from, and specifically how it could be implemented as a mechanism in an AI multi-agent discussion system. Be concrete and specific, not abstract.

## Research Areas

### 1. Cognitive Diversity from Psychology and Organizational Behavior
- How do real teams of humans produce diverse thinking? What does the research say about cognitive diversity vs demographic diversity in terms of creative output?
- What are the known "thinking styles" frameworks (beyond Myers-Briggs)? Kirton's Adaption-Innovation Theory, Hermann Brain Dominance, De Bono's frameworks, others?
- How do these map to parameters we could set on AI agents?
- What does the research say about optimal team composition for creative problem solving?
- What is "constructive conflict" and how is it facilitated in real organizations?

### 2. Improv Theater and Comedy Writing Rooms
- How do improv troupes generate genuinely surprising material? What rules/structures do they use?
- How do TV comedy writing rooms work? What dynamics produce the best material?
- What's the role of "the game of the scene" in improv and how could it apply to structured discussions?
- What's "group mind" in improv and is it something to pursue or avoid in our context?
- How do improvisers avoid "wimping" (making safe choices) and "pimping" (forcing others into bad positions)?

### 3. Design Thinking and Innovation Labs
- What techniques do IDEO, Stanford d.school, MIT Media Lab use to produce breakthrough ideas?
- What is "creative abrasion" (from Harvard research) and how is it structured?
- How do design sprints (Google Ventures style) compress creative thinking into structured timeboxes?
- What's the role of physical prototyping in ideation and how could we simulate it with artifacts?
- How do innovation labs handle the "diverge then converge" transition without killing good ideas?

### 4. Argumentation Theory and Dialectics
- What does formal argumentation theory say about productive disagreement?
- Hegelian dialectics (thesis/antithesis/synthesis) -- how to structure this in agent conversations?
- Toulmin's model of argumentation -- could agents structure their arguments formally?
- What is "steel-manning" (arguing the strongest version of the opponent's position) and how to enforce it?
- What's the difference between adversarial and collaborative argumentation, and when is each better?

### 5. Game Theory and Mechanism Design
- How can you design incentive structures so agents are motivated to produce novel ideas rather than agree?
- What game theory concepts (Nash equilibrium, prisoner's dilemma, auction theory) apply to multi-agent discussion?
- How do prediction markets produce accurate group opinions? Could we use a prediction-market-like mechanism for idea quality?
- What is "mechanism design" and how could it structure the rules of agent interaction to produce better outcomes?
- How do scoring rules incentivize honest reporting of beliefs?

### 6. Biological and Evolutionary Approaches
- How do biological systems produce diversity (genetic algorithms, sexual reproduction, mutation)?
- How does the immune system generate diverse antibodies? Could a similar "random recombination" approach work for ideas?
- What is "evolutionary pressure" in the context of idea selection and how to simulate it?
- How do ecosystems maintain diversity (niche differentiation)? How to prevent one agent/idea from dominating?
- What is stigmergy (indirect coordination through environmental signals, like ant pheromones) and could it work for agent coordination?

### 7. Preventing LLM-Specific Failure Modes
- What does the research say about LLM sycophancy and how to mitigate it?
- What techniques exist for increasing output diversity from the same model? (Temperature, top-p, but also prompting strategies)
- What does "self-consistency" research tell us about getting different reasoning paths from the same model?
- How do constitutional AI and RLHF affect creative output, and how to work around the "safety" tendency to be agreeable?
- Are there prompting techniques specifically designed to produce contrarian or minority-view outputs?

### 8. Collective Intelligence and Wisdom of Crowds
- What conditions must be met for "wisdom of crowds" to work (independence, diversity, decentralization, aggregation)?
- How do Delphi methods produce expert consensus while maintaining independence?
- What is "information cascades" and how to prevent agents from just following the first strong opinion?
- How do citizen assemblies and deliberative democracy processes structure productive disagreement among non-experts?
- What can we learn from open source communities about distributed creative collaboration?

### 9. Narrative and Worldbuilding Techniques
- How do fiction writers create characters that feel genuinely different from each other?
- What's the role of "character motivation" vs "character personality" in creating authentic behavior?
- How do tabletop RPG game masters run NPCs that feel distinct? What techniques do they use?
- Could "method acting" principles help agents stay in character more authentically?
- How do worldbuilders create internally consistent but surprising fictional systems?

### 10. Unusual / Cross-Domain Approaches
- What can we learn from jazz improvisation about structured creativity between multiple performers?
- How do scientific peer review processes produce genuine evaluation rather than rubber-stamping?
- What techniques do intelligence agencies use for "red team" analysis?
- How do martial arts sparring sessions structure productive competition?
- What can we learn from philosophical traditions (Socratic method, Talmudic debate, Buddhist dialectics) about productive intellectual disagreement?

## Output Format

For each research area, produce:

1. **Key Findings** -- the 3-5 most relevant concepts from that domain
2. **Mechanism Proposals** -- for each finding, a specific mechanism that could be implemented in the agent system. Include:
   - What it does
   - When it activates (which Phase, what trigger)
   - Which entity it modifies (AgentMind, Idea, AgentDiscussionState, etc.)
   - Expected effect on discussion quality
3. **Risk/Caveat** -- what could go wrong with this mechanism or when it wouldn't apply

Save findings to: `docs/design_specs/creativity-engine/research-findings.md`
