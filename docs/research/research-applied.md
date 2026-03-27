# Research Applied to Creativity Engine

**Date:** 2026-03-17
**Source:** MakingAgentsNotActLikeAIResearchResults.md (10 research domains, 40+ mechanisms)

---

## Research Area 1: Cognitive Diversity (Psychology / Organizational Behavior)

### Already Covered

- **Diverse cognitive toolboxes (Finding 1):** The existing Cognitive Style enum (Analytical, Intuitive, Systematic, Lateral, Narrative) and Domain Affinity list in `personalities.md` address Page's perspective/heuristic diversity. The technique archetype system in `techniques.md` (Visionary, Connector, Challenger, etc.) further differentiates reasoning methods.
- **Task conflict without relationship conflict (Finding 3):** The positional system in `positions.md` creates structural task conflict (Customer vs Investor, Builder vs Customer). AI agents inherently lack relationship conflict. Devil's Advocate Duty in `anti-slop-mechanisms.md` provides the rotating critic role.
- **Equal turn-taking (Woolley):** The bench system and roster rotation enforce participation balance.

### New Mechanisms to Add

**1. Adaptor-Innovator Dial**
- **Description:** A new personality dimension `paradigm_conformity` (0.0-1.0) distinct from creativity_temperature. Creativity temperature controls how wild ideas are; paradigm conformity controls whether the agent works within the existing frame or challenges the frame itself. 0.0 = "Why are we building this at all?" 1.0 = "How do we make this 20% better?"
- **Belongs in:** `personalities.md` as a 9th personality dimension
- **Entity modified:** AgentMind (new trait field)
- **Activates:** All phases, but amplified during Brainstorm (low conformity agents prioritized) and Specify (high conformity agents prioritized)
- **Expected effect:** Prevents the team from either always reinventing or always optimizing. Creates natural tension between "do things better" and "do things differently" agents.

**2. Bridge Agent Role**
- **Description:** An agent explicitly tasked with translating between high-paradigm-conformity and low-paradigm-conformity agents. When a radical reframer proposes something, the bridge translates it into actionable terms. When an optimizer proposes an increment, the bridge asks what paradigm shift it might enable.
- **Belongs in:** `techniques.md` as a new archetype ("The Translator")
- **Entity modified:** DiscussionAgent (new archetype option)
- **Activates:** Refine and Specify phases primarily, when the gap between radical and incremental proposals is largest
- **Expected effect:** Prevents radical ideas from being dismissed as impractical and incremental ideas from being dismissed as boring. Increases yield of usable ideas from brainstorm.

**3. FourSight Stage Affinity**
- **Description:** Map agents to creative problem-solving stages: Clarifier (explores problems), Ideator (generates possibilities), Developer (refines solutions), Implementer (drives to action). This is distinct from existing personality traits -- it governs which STAGE of work an agent excels at, not their style.
- **Belongs in:** `personalities.md` as a new enum: `creative_stage_affinity`
- **Entity modified:** AgentMind
- **Activates:** Bench priority decisions -- Clarifiers prioritized early in Brainstorm, Ideators mid-Brainstorm, Developers in Refine, Implementers in Specify
- **Expected effect:** Better bench rotation decisions. Agents come off the bench when their stage is active rather than only by topic relevance.

### Modifications to Existing Mechanisms

- **Cognitive Style enum:** Research suggests the distinction between "perspectives" (how problems are encoded) and "heuristics" (how solutions are searched) matters more than a single cognitive style. Consider splitting Cognitive Style into two dimensions: `problem_encoding` (how the agent frames the problem) and `solution_search` (how the agent finds answers). This is a significant change -- flag for architecture phase decision.

### What to Skip

- **De Bono Six Thinking Hats parallel protocol (all agents wear same hat, then switch):** The existing phase system already does this better. Phases gate the entire team's mode (YES-AND in Brainstorm, CHALLENGE in Refine). Layering a sub-protocol of hat-switching within phases would burn tokens on meta-coordination without clear benefit. The phase system IS the hat system.

---

## Research Area 2: Improv Theater and Comedy Writing Rooms

### Already Covered

- **Anti-blocking:** The YES-AND communication mode in Brainstorm phase (`phase-dynamics.md`) enforces building rather than negating.
- **Writers' room Blue Sky phase:** The Brainstorm phase with minimum idea count gate and high muse activity maps directly.
- **Showrunner model:** The Director BackgroundAgent has authoritative intervention power, and the TieBreakerGhost resolves deadlocks.

### New Mechanisms to Add

**4. Game Discovery Protocol**
- **Description:** A structured sub-protocol for the early Brainstorm phase. Step 1: Agents establish base reality (shared understanding of domain, users, competition). Step 2: Agents explicitly identify the most surprising tension or unmet need -- one agent "frames" it: "That's surprising because normally X, but here Y." Step 3: All agents shift to "If this insight is true, then what else must be true?" This replaces open-ended "generate ideas" with focused exploration of surprising insights.
- **Belongs in:** `phase-dynamics.md` as a Brainstorm sub-phase or activation protocol
- **Entity modified:** Phase (new optional sub-phase: `game_discovery`)
- **Activates:** First 3-5 turns of Brainstorm phase, before open ideation begins
- **Expected effect:** Grounds ideation in a genuinely surprising insight rather than letting agents generate from their default priors. Produces ideas that are responses to a real tension rather than ideas in a vacuum.

**5. Anti-Pattern Enforcement Rules**
- **Description:** Four specific rules monitored by the orchestrator across all phases:
  - Anti-wimping: Every response must include at least one specific, concrete proposal. Ban "we could explore various options."
  - Anti-pimping: Agents cannot pose open questions without first offering their own answer.
  - Anti-hedging: Ban qualifiers ("perhaps," "maybe," "potentially") during proposal phases. Force declarative statements.
  - Anti-gagging: Flag responses that go for the easy/impressive answer instead of engaging with the actual problem.
- **Belongs in:** `anti-slop-mechanisms.md` as Mechanism 11
- **Entity modified:** Orchestrator per-turn validation logic
- **Activates:** All phases. Anti-hedging strongest in Specify. Anti-wimping strongest in Brainstorm.
- **Expected effect:** Eliminates the filler and hedge-language that makes AI discussions read like committee meetings. Produces sharper, more committed contributions. Directly observable in transcript quality.
- **Action log event:** `anti_pattern_violation` with type (wimp/pimp/hedge/gag) and agent ID

**6. Pitch Phase Protocol**
- **Description:** Between Blue Sky brainstorming and group refinement, each agent independently develops one fully-formed proposal with problem-solution-reasoning structure. These get "posted" for critique. This mirrors the comedy writers' room requirement that pitches be "fully thought-out" rather than vague gestures.
- **Belongs in:** `phase-dynamics.md` as a transition protocol between Brainstorm and Refine
- **Entity modified:** Phase transition logic, ProposalArtifact (each pitch becomes one)
- **Activates:** At Brainstorm-to-Refine transition gate
- **Expected effect:** Forces agents to commit to a specific position before group evaluation. Prevents the common failure mode where promising brainstorm ideas evaporate because nobody develops them into concrete proposals.

### Modifications to Existing Mechanisms

- **Agreement Tax (Mechanism 3):** Add the improv-derived rule that agents who agree must also "heighten" -- push the idea further than the originator did, not just extend sideways. "Yes, and even more so because..." This strengthens the existing mechanism.

### What to Skip

- **Anti-blocking as a universal rule:** The research correctly notes this must be phase-gated. The existing design already handles this -- YES-AND in Brainstorm, CHALLENGE in Refine. Applying anti-blocking during Review would prevent legitimate criticism.

---

## Research Area 3: Design Thinking and Innovation Labs

### Already Covered

- **Divergent/convergent separation (Finding 1):** The four-phase system (Brainstorm/Refine/Specify/Review) with hard exit gates is exactly this. Communication modes switch between YES-AND, CHALLENGE, SPECIFY, and ADVERSARIAL.
- **Creative abrasion through positions (Finding 2):** The positional conflict matrix in `positions.md` (Customer vs Investor, Builder vs Customer, etc.) creates structural friction between genuinely different optimization targets.
- **The Groan Zone:** The Refine phase sits between divergent Brainstorm and convergent Specify, functioning as the synthesis zone. The Weaver BackgroundAgent handles cross-thread connection.

### New Mechanisms to Add

**7. Independent Mini-Spec Round**
- **Description:** At the Brainstorm-to-Refine transition, each agent independently writes a 1-page mini-spec for their strongest idea. These are produced in isolation (no agent sees another's work), then "posted" to the shared space for structured speed critique. This is the "Build to Think" principle -- making ideas tangible changes the quality of thinking.
- **Belongs in:** `phase-dynamics.md` as a mandatory transition protocol
- **Entity modified:** ProposalArtifact (new subtype: `mini_spec`), Phase transition logic
- **Activates:** At Brainstorm exit gate, before Refine begins
- **Expected effect:** Forces commitment and specificity. Produces concrete targets for critique rather than abstract positions. The independent production prevents anchoring.
- **Note:** This overlaps with mechanism 6 (Pitch Phase). Implement as a single mechanism: the Pitch Phase requires each agent to produce a mini-spec ProposalArtifact.

### Modifications to Existing Mechanisms

- **Muse BackgroundAgent:** Research confirms that random stimulation works but should be concentrated in Brainstorm and off in Specify/Review. The existing design already does this (`phase-dynamics.md` sets Muse activity to High/Low/Off/Off). No change needed.

### What to Skip

- **Dot voting for idea selection:** The existing system uses magnitude-based scoring in AgentMinds plus Pareto analysis. Simulating dot voting would add a mechanism that duplicates what magnitude + bench rotation already achieve, without clear benefit. The organic process of magnitude rising/falling based on argument quality is more authentic than artificial voting.

---

## Research Area 4: Argumentation Theory and Dialectics

### Already Covered

- **Structured argumentation:** The PositionPaper entity in the entity model provides structured argument format for disagreements. The Disagreement lifecycle with position papers and TieBreakerGhost resolution is already a dialectical process.
- **Steel-manning (Finding 3):** Partially covered by the Agreement Tax requiring substantive engagement before agreement. But the explicit steel-man-before-critique protocol is NOT currently in the design.

### New Mechanisms to Add

**8. Steel-Man Requirement**
- **Description:** Before any rebuttal in Refine or Review phases, an agent must: (1) restate the opposing position in its strongest form, (2) list explicit points of agreement, (3) state what they learned from the position, (4) only then critique. Monitored by orchestrator. This is Dennett's four rules operationalized.
- **Belongs in:** `anti-slop-mechanisms.md` as Mechanism 12
- **Entity modified:** Orchestrator per-turn validation (in CHALLENGE and ADVERSARIAL communication modes)
- **Activates:** Refine and Review phases. NOT Brainstorm (would slow ideation) or Specify (critiques are about precision, not positions).
- **Expected effect:** Prevents dismissive or shallow critiques. Forces agents to genuinely understand what they're arguing against. Produces higher-quality disagreements that are more useful to human readers of the transcript.
- **Action log event:** `steel_man_check` with pass/fail and deficiency type

**9. Pragma-Dialectical Guardrails**
- **Description:** Three enforceable rules monitored by a validator (the Specter BackgroundAgent can do this during surprise audits):
  - No straw-manning: critiques must address the actual stated position, not a distortion of it.
  - Burden of proof: whoever advances a claim must provide reasoning. "I think we should do X" requires "because Y."
  - Closure rule: when an agent's argument has been decisively refuted, they must retract or modify their position. Holding a defeated position without new evidence is flagged.
- **Belongs in:** `anti-slop-mechanisms.md` as Mechanism 13
- **Entity modified:** Specter BackgroundAgent audit criteria, Disagreement resolution logic
- **Activates:** Refine and Review phases
- **Expected effect:** Prevents circular arguments and zombie ideas that keep returning after being refuted. The closure rule is the most impactful -- it forces actual resolution rather than repetition.

**10. Toulmin Structure for Key Decisions**
- **Description:** When a Decision entity is being formed, the proposing agent must structure the argument as: Claim, Grounds (evidence), Warrant (why evidence supports claim), Qualifier (confidence/limitations), Rebuttal (strongest counter-argument). A validator checks completeness. Other agents specifically target the weakest component.
- **Belongs in:** `entity-model.md` as an optional structured format for Decision rationale
- **Entity modified:** Decision (new optional `toulmin_structure` field), ProposalArtifact
- **Activates:** Specify and Review phases, only for significant Decisions (not every micro-agreement)
- **Expected effect:** Increases decision quality by forcing explicit articulation of assumptions and counter-arguments. Makes the transcript more useful for human readers who want to understand WHY a decision was made.

### Modifications to Existing Mechanisms

- **Disagreement resolution:** The existing TieBreakerGhost should incorporate the closure rule -- when it rules, the losing side must update their AgentMind magnitude accordingly. Currently the entity model says magnitude "may" be tweaked; this should be "must" for TieBreakerGhost rulings.

### What to Skip

- **Full pragma-dialectical 10-rule framework:** Over-engineered for this context. The three rules above capture 80% of the value. The remaining rules govern things like freedom to advance standpoints (already handled by bench system) and language clarity (better handled by anti-hedging).
- **Ideological Turing Test (agents argue FOR positions they've opposed):** Interesting but burns tokens on a meta-exercise. The steel-man requirement captures the same insight more efficiently.

---

## Research Area 5: Game Theory and Mechanism Design

### Already Covered

- **Anti-coordination incentives:** Novelty Scoring (Mechanism 4) penalizes ideas >0.85 similar to existing ones. Domain Pivot Triggers (Mechanism 1) break clustering. These are anti-coordination mechanisms by another name.

### New Mechanisms to Add

**11. Idea Congestion Penalty**
- **Description:** When scoring ideas (via Oracle BackgroundAgent), apply an explicit congestion penalty: the first agent to propose in a conceptual territory gets full credit; subsequent agents in the same territory get diminishing returns. Score = base_quality * (1 / sqrt(n_similar_ideas)). This transforms brainstorming from "find the best idea" to "find an idea nobody else found."
- **Belongs in:** `anti-slop-mechanisms.md` as an enhancement to Mechanism 4 (Novelty Scoring)
- **Entity modified:** Idea (new field: `territory_novelty_score`), Oracle BackgroundAgent scoring logic
- **Activates:** Brainstorm phase primarily. Scoring runs after each batch of contributions.
- **Expected effect:** Directly incentivizes agents to search unexplored territory rather than piling onto a promising direction. Combined with the existing novelty scoring, creates a strong anti-clustering pressure.

**12. Divergent Priming (Schelling Focal Point Breaking)**
- **Description:** Before Brainstorm begins, each agent receives a different "seed packet" -- a unique combination of: (1) a different subset of the idea brief's constraints, (2) a different analogous product/domain to consider, (3) a different user persona to prioritize. This breaks the shared focal point that causes all agents to generate the same "obvious" first idea.
- **Belongs in:** `phase-dynamics.md` under Brainstorm phase setup
- **Entity modified:** Session preparation logic (new step: `divergent_priming`), AgentMind (seed packet stored as `session_priming`)
- **Activates:** Session preparation, before first Brainstorm turn
- **Expected effect:** Agents start from genuinely different places rather than converging on the same "Grand Central at noon" obvious first idea. This is cheap (small addition to each agent's context) with high expected impact on initial diversity.
- **Configuration:** Seed packets defined in team YAML or auto-generated by Director BackgroundAgent based on idea brief analysis.

**13. Meta-Predictive Scoring (Simplified BTS)**
- **Description:** Periodically during Brainstorm, each agent predicts what the OTHER agents will propose next. Ideas that are "surprisingly common" (proposed by more agents than predicted) get flagged as potential genuine insights. Ideas that everyone predicted but nobody proposed reveal blind spots.
- **Belongs in:** New sub-section in `anti-slop-mechanisms.md` or `techniques.md`
- **Entity modified:** BackgroundAgent (new Curator sub-routine), Idea (new metadata: `prediction_surprise_score`)
- **Activates:** Every N turns during Brainstorm (configurable, default every 10 turns)
- **Expected effect:** Surfaces ideas that represent genuine minority perspectives rather than noise. Reveals group blind spots. Produces an interesting transcript moment ("Nobody predicted X, but three agents independently proposed it").
- **Token cost:** Moderate. Each agent produces a short prediction (~100 tokens) every N turns. Worth it for the insight.

### Modifications to Existing Mechanisms

- **Novelty Scoring (Mechanism 4):** Rename to "Novelty and Congestion Scoring" and integrate the congestion penalty. The similarity threshold (currently 0.85) should be configurable per phase -- tighter in Brainstorm (encourage exploration), looser in Specify (allow convergence).

### What to Skip

- **Marginal contribution scoring (Shapley value):** Computationally expensive and conceptually redundant with the congestion penalty. The leave-one-out analysis requires re-evaluating the entire idea set per agent. The congestion penalty achieves similar incentives at much lower cost.
- **Full Bayesian Truth Serum implementation:** The simplified version (meta-predictive scoring) captures the useful insight without the mathematical machinery that has mixed empirical results even with humans.

---

## Research Area 6: Biological and Evolutionary Approaches

### Already Covered

- **Niche differentiation (Finding 3):** The Domain Affinity list in `personalities.md` and the Position types in `positions.md` create explicit niches. The Naturalist archetype in `techniques.md` uses biological metaphors.
- **Adaptive temperature across phases (Finding 2):** Phase dynamics already shift from high creativity temperature in Brainstorm to low in Specify/Review. This IS adaptive annealing.
- **Keystone critic (Finding 3):** Devil's Advocate Duty (Mechanism 5) and the Specter BackgroundAgent serve the keystone role -- targeting consensus ideas for scrutiny.

### New Mechanisms to Add

**14. V(D)J Modular Prompt Assembly**
- **Description:** Create four interchangeable component libraries: [Problem Framings] x [Analytical Methods] x [Solution Archetypes] x [Constraint Sets]. Each agent randomly assembles one combination per session. With 5 options per slot: 625 unique starting configurations from 20 components. Add "junctional noise" -- a random secondary constraint (e.g., "must work offline," "must be explainable to a child") to further amplify diversity.
- **Belongs in:** New file: `prompt-assembly.md` (or add as a section in `techniques.md`)
- **Entity modified:** Session preparation (new step: `vdj_assembly`), DiscussionAgent (new field: `active_configuration`)
- **Activates:** Session preparation, refreshed at each phase transition
- **Expected effect:** Guarantees genuine cognitive diversity across agents even when personality traits happen to overlap. The combinatorial explosion means no two agents start from the same place.
- **Configuration:** Component libraries defined per idea domain. The system ships with default libraries; users can customize in team YAML.

**Component library examples:**
- Problem Framings: "as an access problem," "as a trust problem," "as a coordination problem," "as a discovery problem," "as a retention problem"
- Analytical Methods: "first-principles decomposition," "analogical reasoning from [random domain]," "constraint-first thinking," "user-story backward reasoning," "failure-mode analysis"
- Solution Archetypes: "platform," "marketplace," "tool," "community," "protocol"
- Constraint Sets: "must work in 1 minute," "must cost nothing," "must require no login," "must work for 1M users," "must be built in 2 weeks"

**15. Stigmergic Annotation Layer**
- **Description:** Add typed annotations to the shared Idea space that trigger agent behaviors. Annotation types: "promising but unvalidated," "conflict detected," "connection opportunity," "needs champion," "evidence requested." Annotations have signal strength (based on endorsements) and temporal decay -- old unmodified annotations fade. Different annotation types trigger different agent responses.
- **Belongs in:** `entity-model.md` as a new entity or Idea sub-entity
- **Entity modified:** Idea (new field: `annotations[]` with type, strength, decay_rate, author), AgentMind (annotation-triggered behavior rules)
- **Activates:** All phases. Annotations accumulate and decay continuously.
- **Expected effect:** Enables decentralized coordination. Agents respond to the state of the idea board rather than only to direct messages. Creates emergent prioritization without centralized control. The temporal decay prevents old ideas from permanently dominating.
- **Action log event:** `annotation_added`, `annotation_decayed`, `annotation_triggered_action`

### Modifications to Existing Mechanisms

- **Phase temperature mapping:** Make the annealing schedule explicit and configurable. Current design implies temperature shifts per phase but doesn't define the curve. Add to `phase-dynamics.md`: a `diversity_target` per phase (Brainstorm: 0.8+, Refine: 0.5-0.7, Specify: 0.3-0.5, Review: 0.2-0.4) that the orchestrator monitors and adjusts agent configurations to maintain.

### What to Skip

- **Full stigmergic replacement of direct messaging:** The research suggests replacing agent-to-agent messaging entirely with artifact-based coordination. This conflicts with the system's core design (transcript as product). The conversation IS the deliverable -- users read it. A hybrid approach (conversation + annotation layer) is better than pure stigmergy.

---

## Research Area 7: LLM-Specific Failure Modes

### Already Covered

- **RLHF mode collapse awareness:** The entire anti-slop-mechanisms.md exists because of this problem. Semantic clustering, premature convergence, polite agreement, sycophancy -- all addressed.
- **Anti-sycophancy (Finding 2):** Agreement Tax (Mechanism 3), Devil's Advocate Duty (Mechanism 5), Convergence Suppression (Mechanism 2) all target sycophancy cascades.
- **Persona vs methodology distinction (Finding 3):** The technique archetype system assigns reasoning METHODS (reversal, cross-pollination, first principles) not just personality labels. The position system adds motivation. This is better than simple persona assignment.

### New Mechanisms to Add

**16. Blind Proposal Round**
- **Description:** At the start of each phase, all agents generate their initial proposals in parallel isolation -- no agent sees any other's output until all have committed. The orchestrator collects all proposals, then presents them simultaneously (in randomized order) for discussion. This is the single most research-supported mechanism for preventing sycophancy cascades.
- **Belongs in:** `phase-dynamics.md` as a mandatory first step in each phase
- **Entity modified:** Phase (new property: `blind_round_required: boolean`), Session orchestration logic
- **Activates:** Start of Brainstorm and Refine phases. Optional for Specify and Review.
- **Expected effect:** Eliminates first-mover advantage and anchoring bias. Research shows the first speaker has disproportionate influence on outcomes. Blind rounds make this structurally impossible.
- **Implementation note:** This maps naturally to the system architecture -- each team's agents share a context window, but the orchestrator can collect responses before distributing them.

**17. Temperature Variation Across Agents**
- **Description:** Assign different sampling temperatures to different agents based on their role. Conservative agents (high paradigm_conformity, low risk_tolerance): T=0.7. Creative agents (high creativity_temperature, low paradigm_conformity): T=1.0-1.2 with min-p sampling. This uses the LLM's own latent diversity (which research confirms is substantial) rather than relying solely on prompt differentiation.
- **Belongs in:** `personalities.md` as a note on implementation, or a new section on sampling configuration
- **Entity modified:** DiscussionAgent (new field: `sampling_config` with temperature, top_p, min_p)
- **Activates:** All phases. Temperature may also vary by phase (higher in Brainstorm, lower in Specify).
- **Expected effect:** Genuine output diversity at the model level, not just prompt level. Research shows T=0.8-1.0 diversity gains with minimal accuracy loss. Combined with prompt-level differentiation, this creates two independent sources of diversity.

**18. Multi-Sample Generation**
- **Description:** For key contributions (pitch proposals, position papers, disagreement responses), have each agent generate 3-5 independent responses internally and select the most distinctive one (measured against existing ideas in the discussion). Research identifies 8 samples as the sweet spot for diversity vs compute, but 3-5 is more token-efficient.
- **Belongs in:** `techniques.md` or `phase-dynamics.md` as an optional enhancement for high-stakes contributions
- **Entity modified:** PrivateAction (new type: `multi_sample_generation`), AgentMind
- **Activates:** Pitch Phase (mechanism 6), position paper writing, key disagreement responses
- **Expected effect:** Exploits within-model diversity that prompt engineering alone cannot access. The agent's "best" idea (first sample) may not be their most distinctive.
- **Token cost:** High. 3-5x token usage per enhanced contribution. Reserve for high-value moments, not every turn. Configurable.

### Modifications to Existing Mechanisms

- **Perspective Enforcement (Mechanism 6):** Research confirms per-turn injection is essential ("different reasoning methodologies matter more than different personas"). The existing mechanism is correctly designed. Enhancement: include the agent's active V(D)J configuration in the per-turn reminder, not just Position and Personality.
- **Convergence Suppression (Mechanism 2):** Add monitoring for "confidence cascade" -- when one agent states high confidence, subsequent agents tend to agree regardless of merit. The orchestrator should strip or normalize confidence signals between agents during Brainstorm.

### What to Skip

- **Verbalized sampling (having agents generate probability distributions over multiple responses):** Interesting research but awkward to implement in a conversation context. The multi-sample generation mechanism captures the same benefit in a more natural way.
- **Stripping formatting constraints during brainstorming:** The transcript is the product. Users need readable, formatted output. Can't sacrifice readability for marginal diversity gains.

---

## Research Area 8: Collective Intelligence and Wisdom of Crowds

### Already Covered

- **Independence enforcement (Finding 1):** Partially. The bench system means not all agents speak every turn, and teams operate in separate context windows. But agents WITHIN a team share a context window and see each other's contributions in real-time.
- **Delphi-inspired iteration (Finding 2):** The multi-session design with between-session curation provides iterative refinement. Briefings serve as controlled feedback.
- **Cross-pollination between groups (Finding 3):** The Weaver BackgroundAgent connects threads between sessions. Cross-team messaging happens through the MCP server.

### New Mechanisms to Add

**19. Randomized Presentation Order**
- **Description:** When sharing proposals, position papers, or critique results across teams, randomize the order of presentation each time. The research is unambiguous: the first item presented anchors subsequent evaluation. Simple to implement, zero token cost.
- **Belongs in:** `anti-slop-mechanisms.md` as Mechanism 14
- **Entity modified:** Orchestrator message ordering logic
- **Activates:** All phases, all cross-team and intra-team information sharing
- **Expected effect:** Eliminates order-of-presentation bias. Over multiple rounds, all ideas get fair initial positioning.

**20. Reasoning-Before-Conclusions Sharing**
- **Description:** When agents share work across teams, share the reasoning and evidence FIRST, conclusions SECOND. This prevents anchoring on conclusions and forces the receiving team to engage with the argument, not just the claim.
- **Belongs in:** `phase-dynamics.md` as a cross-team communication protocol
- **Entity modified:** Message (new format guidance for cross-team messages), Briefing generation
- **Activates:** All cross-team communication, especially at phase transitions
- **Expected effect:** Reduces anchoring bias. The receiving team forms preliminary interpretations from evidence before being told what to conclude. More authentic engagement with the argument.

### Modifications to Existing Mechanisms

- **Blind Proposal Round (mechanism 16 above):** This IS the independence enforcement the research demands. The existing design doesn't explicitly require it. Making it mandatory for Brainstorm phase start is the single highest-impact change from this research area.

### What to Skip

- **Full Delphi protocol with anonymized statistical summaries:** The system's agents are already "anonymous" in the sense that they're AI -- there's no social status hierarchy to anonymize around. The agent personas create useful differentiation that anonymization would destroy. The iterative refinement benefit is already captured by the multi-session design.
- **Citizens' assembly working groups with random assignment:** The existing team structure with cross-team MCP communication already provides this. Random sub-group assignment within a team would add complexity without clear benefit given the small team sizes (4-6 agents).

---

## Research Area 9: Narrative and Worldbuilding Techniques

### Already Covered

- **Motivation through positions (Finding 1):** The position system in `positions.md` already defines agents by what they WANT -- the Customer wants their problem solved, the Investor wants ROI, the Competitor wants to find weaknesses. This is motivation-first design.
- **Exclusive capabilities through archetypes (Finding 4):** Technique archetypes in `techniques.md` give agents distinct cognitive tools. The position system creates domain authority.

### New Mechanisms to Add

**21. The Lie Filter**
- **Description:** Each agent holds a "Lie" -- a partially true but incomplete belief that acts as a cognitive filter. The Lie must be something a smart person could genuinely believe. Examples: "The biggest risk is always shipping too late" (partial truth: sometimes the risk is shipping the wrong thing). "Users will forgive slow rollout but not bugs" (partial truth: sometimes users need something fast and imperfect). The Lie determines what the agent notices, dismisses, and gravitates toward. Two agents with identical information but different Lies reach radically different conclusions.
- **Belongs in:** `positions.md` as a new dimension of positional framing, or `personalities.md` as a cognitive bias dimension
- **Entity modified:** AgentMind (new field: `core_lie` with text description and `lie_strength` 0.0-1.0)
- **Activates:** All phases. The Lie is persistent across a session but can be updated between sessions by Director BackgroundAgent if the agent encounters overwhelming counter-evidence.
- **Expected effect:** Produces genuine interpretive divergence from the same input. Unlike personality traits (which affect HOW an agent processes), the Lie affects WHAT the agent sees. This is the missing cognitive filter layer.
- **Configuration:** Lies defined per agent in team YAML. The system could include a library of validated Lies per position type.

**22. BIT System (Beliefs, Instincts, Traits)**
- **Description:** Each agent gets: 3 Beliefs (principle + actionable goal: "Great products solve one problem perfectly -- I will argue we cut scope to one core feature"), 2-3 Instincts (automatic behavioral triggers: "When someone proposes adding scope, I always ask what we'd cut to compensate"), and 1 explicit Blind Spot ("I tend to undervalue marketing"). Track consistency -- agents that maintain their BITs produce more coherent, differentiated contributions.
- **Belongs in:** `personalities.md` as a new section, or a separate file `agent-bits.md`
- **Entity modified:** AgentMind (new fields: `beliefs[]`, `instincts[]`, `blind_spots[]`), Orchestrator (consistency tracking)
- **Activates:** All phases. Beliefs can be updated between sessions based on new information (but not mid-session -- stability matters for consistency).
- **Expected effect:** Creates agents with genuine convictions that drive behavior rather than personality adjectives that describe behavior. An agent with the belief "shipping late kills products" will NATURALLY argue for scope cuts without needing the prompt to say "you prefer smaller scope." This is generative, not descriptive.
- **Consistency scoring:** Track whether agents act consistently with their BITs. Inconsistency is flagged for the agent ("Your last proposal contradicts your stated belief that X"). This self-correction mechanism prevents agents from drifting toward the group's center.
- **Action log event:** `bit_consistency_check` with score and specific violations

**23. Hard Capability Constraints (Playbook Protocol)**
- **Description:** Each agent has exclusive "Moves" only they can perform, AND hard limitations. The Technical Architect can call for feasibility assessment but CANNOT evaluate business viability. The User Advocate can invoke user stories but CANNOT assess technical complexity. This creates genuine interdependence -- agents must rely on each other rather than all being generalists.
- **Belongs in:** `positions.md` as a new section on capability constraints per position
- **Entity modified:** DiscussionAgent (new fields: `exclusive_moves[]`, `hard_constraints[]`), Orchestrator (move validation)
- **Activates:** All phases. Constraints may loosen slightly in Brainstorm (everyone can ideate) but tighten in Refine/Specify/Review.
- **Expected effect:** Prevents all agents from reasoning about everything equally (which produces homogeneous output). Forces genuine collaboration. Produces a transcript where different agents contribute genuinely different value.
- **Risk to mitigate:** Too-tight constraints create siloed thinking. Each agent needs a primary domain plus awareness of adjacent domains. Implement as "you MUST defer to [agent] on [domain]" rather than "you CANNOT think about [domain]."

### Modifications to Existing Mechanisms

- **Position system:** The existing position types (Customer, Investor, Builder, etc.) define what agents care about but not what they fundamentally BELIEVE (Lie) or what they will DO automatically (Instincts). Adding the Lie and BIT layers to each position creates a much richer behavioral generator. Position defines the role, Lie defines the filter, BITs define the behaviors.
- **Personality Evolution:** Currently the Director BackgroundAgent adjusts personality traits between sessions. Extend this to also adjust BITs -- an agent whose Belief was conclusively disproven should have that Belief updated.

### What to Skip

- **Maslow-level motivation mapping:** The positional system already creates motivation differentiation (Customer's survival need vs Investor's growth need). Explicitly mapping to Maslow hierarchy adds theoretical framework without practical implementation benefit. The positions ARE the motivations.

---

## Research Area 10: Cross-Domain Approaches

### Already Covered

- **Red team / adversarial analysis (Finding 2):** The Review phase is explicitly adversarial. The Competitor and Skeptic positions serve the Red Cell function. Chaos Engineering and Failure Analysis are listed as active techniques. Devil's Advocate Duty rotates the contrarian role.
- **Pre-mortem (Finding 2):** Referenced in Review phase technique categories. The Specter BackgroundAgent monitors for degradation.
- **Graduated resistance (Finding 4):** The phase progression from YES-AND (Brainstorm) through CHALLENGE (Refine) to ADVERSARIAL (Review) IS graduated resistance -- light, medium, hard sparring.

### New Mechanisms to Add

**24. Sacred Disagreement Meta-Rules**
- **Description:** Three meta-rules governing all agent interaction:
  1. Before disagreeing, explicitly reference the common goal ("We're all trying to find the best product for [target user]").
  2. Before critiquing a position, state the strongest version of that position first (as Beit Hillel taught Shammai's views first). This overlaps with mechanism 8 (Steel-Man Requirement) -- implement as one mechanism.
  3. When genuine disagreement persists after deliberation, both positions are preserved in the output with full reasoning rather than forced to false consensus. No artificial resolution.
- **Belongs in:** `anti-slop-mechanisms.md` as a meta-rule section (these govern other mechanisms)
- **Entity modified:** Decision (new type option: `preserved_dissent` alongside consensus/executive/tiebreaker), Artifact output format
- **Activates:** All phases, but most important in Refine and Review
- **Expected effect:** Solves the premature convergence problem at the output level. Even if the discussion converges, genuinely contested points are preserved as dissenting views in the final spec. This produces more honest, useful specifications. Human readers get to see the real trade-offs rather than a false consensus.
- **Key insight:** Rule 3 is the most valuable. Current design forces resolution through TieBreakerGhost. Some disagreements SHOULD remain unresolved in the output -- they represent genuine trade-offs that the implementing team needs to know about.

**25. Champion Requirement**
- **Description:** For any feature/requirement to be included in the final Artifact, at least one agent must serve as its active champion -- providing a substantive, evidence-based case for inclusion. Requirements without champions are dropped. Requirements with champions but strong counter-evidence are flagged as "contested."
- **Belongs in:** `phase-dynamics.md` under Specify phase exit gate criteria
- **Entity modified:** Idea (new status: `championed` / `unchampioned`), Artifact validation gate
- **Activates:** Specify phase. Champion status evaluated at phase exit gate.
- **Expected effect:** Prevents "lowest common denominator" specifications full of features nobody actually believes in. If nobody cares enough to champion a requirement, it probably shouldn't be in the spec. Also prevents specs full of requirements added by one agent that nobody challenged but nobody actually supports.
- **Action log event:** `champion_assigned` / `champion_requirement_unmet`

**26. Key Assumptions Check**
- **Description:** At the transition into Review phase, one agent (assigned by Director BackgroundAgent) surfaces all implicit assumptions in the current spec. A different agent then systematically challenges each assumption. This is distinct from general adversarial review -- it specifically targets the unstated beliefs the spec is built on.
- **Belongs in:** `phase-dynamics.md` as a Review phase initialization step
- **Entity modified:** Phase transition logic, new ProposalArtifact subtype: `assumptions_audit`
- **Activates:** At Specify-to-Review transition
- **Expected effect:** Catches the class of failures that adversarial review misses -- not errors in the spec but errors in what the spec takes for granted. "We assumed users would sign up with email" or "We assumed the API would be free" are the kind of assumptions that kill products.

### Modifications to Existing Mechanisms

- **TieBreakerGhost resolution:** Add the sacred disagreement Rule 3 -- the TieBreakerGhost should have a third option beyond "Side A wins" and "Side B wins": "Genuine trade-off -- preserve both positions in output with full reasoning." This changes the Disagreement resolution options from (consensus, executive, tiebreaker) to (consensus, executive, tiebreaker, preserved_dissent).
- **Review phase:** Add ACH (Analysis of Competing Hypotheses) as a technique. Frame competing spec elements as hypotheses, systematically evaluate evidence for/against each. This is a structured version of what adversarial review should already be doing but gives agents a concrete framework.

### What to Skip

- **Jazz "comping" agents:** The concept of agents who support and elaborate rather than lead is already captured by the bench system (agents come off the bench to support, not always to lead) and the YES-AND communication mode. Adding a formal "comping" role would over-specialize the already rich agent type system.
- **Modal constraint architecture ("provide scales not scores"):** This is how the system already works -- positions and phases provide constraints, not scripts. The existing design philosophy matches this principle. No new mechanism needed.

---

## Summary: Priority-Ranked New Mechanisms

### High Priority (high impact, moderate token cost, addresses gaps in current design)

| # | Mechanism | Primary Gap Addressed |
|---|---|---|
| 16 | Blind Proposal Round | First-mover bias, sycophancy cascades |
| 12 | Divergent Priming | Shared focal points, identical starting states |
| 21 | The Lie Filter | Agents process same input identically |
| 22 | BIT System | Personality describes but doesn't generate behavior |
| 24 | Sacred Disagreement Rule 3 (preserved dissent) | False consensus in output |
| 5 | Anti-Pattern Enforcement | Hedge-language, wimping, filler |
| 8 | Steel-Man Requirement | Shallow critiques |
| 25 | Champion Requirement | Unchampioned requirements in final spec |

### Medium Priority (clear value, either higher token cost or narrower scope)

| # | Mechanism | Primary Gap Addressed |
|---|---|---|
| 14 | V(D)J Modular Prompt Assembly | Agent starting state diversity |
| 11 | Idea Congestion Penalty | Territory clustering |
| 4 | Game Discovery Protocol | Unfocused brainstorm openings |
| 6/7 | Pitch Phase / Independent Mini-Spec | Ideas evaporating between phases |
| 17 | Temperature Variation | Model-level output diversity |
| 15 | Stigmergic Annotation Layer | Decentralized coordination |
| 26 | Key Assumptions Check | Unstated assumptions in specs |

### Lower Priority (interesting but either high token cost, narrow scope, or partially redundant)

| # | Mechanism | Notes |
|---|---|---|
| 1 | Adaptor-Innovator Dial | Partially captured by creativity_temperature |
| 2 | Bridge Agent Role | Narrow scope; Director BackgroundAgent can serve this function |
| 3 | FourSight Stage Affinity | Partially captured by phase-based bench priority |
| 9 | Pragma-Dialectical Guardrails | Partially captured by steel-man + closure via TieBreakerGhost |
| 10 | Toulmin Structure | High value but high token cost; reserve for key decisions |
| 13 | Meta-Predictive Scoring | Interesting but unproven, moderate token cost |
| 18 | Multi-Sample Generation | Very high token cost (3-5x per enhanced turn) |
| 19 | Randomized Presentation Order | Trivial to implement but small impact in AI context |
| 20 | Reasoning-Before-Conclusions | Good practice but hard to enforce structurally |
| 23 | Hard Capability Constraints | Risk of over-constraining agents |

---

## Key Modifications to Existing Design

1. **Disagreement resolution types:** Add `preserved_dissent` as a resolution option alongside consensus/executive/tiebreaker. Some disagreements should NOT be resolved.

2. **Novelty Scoring thresholds:** Make configurable per phase. Tighter in Brainstorm (encourage exploration), looser in Specify (allow convergence).

3. **TieBreakerGhost rulings:** Make magnitude adjustment mandatory (not optional) when a ruling is made. Losing side must update.

4. **Agreement Tax enhancement:** Require "heightening" (pushing the idea further) not just sideways extension.

5. **Phase transitions:** Add mandatory blind proposal round at start of Brainstorm and Refine. Add independent mini-spec round at Brainstorm-to-Refine transition.

6. **Perspective Enforcement (Mechanism 6):** Include V(D)J configuration and active Lie in the per-turn injection, not just Position and Personality.

7. **Convergence Suppression (Mechanism 2):** Add confidence cascade detection -- strip or normalize confidence signals between agents during Brainstorm.

---

## Files to Update

| File | Changes |
|---|---|
| `personalities.md` | Add paradigm_conformity dimension, creative_stage_affinity enum, sampling_config, Lie filter, BIT system |
| `positions.md` | Add hard capability constraints section, Lie examples per position type |
| `techniques.md` | Add Bridge/Translator archetype, V(D)J prompt assembly section |
| `anti-slop-mechanisms.md` | Add mechanisms 5, 8, 9, 11, 14, 19; add sacred disagreement meta-rules section |
| `phase-dynamics.md` | Add blind proposal round, game discovery protocol, pitch phase, divergent priming, key assumptions check, champion requirement gate |
| `entity-model.md` | Add annotations to Idea, preserved_dissent to Decision, toulmin_structure to Decision, assumptions_audit to ProposalArtifact |
| New: `prompt-assembly.md` | V(D)J component libraries and assembly logic (if not inlined into techniques.md) |
