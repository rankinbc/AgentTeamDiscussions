# Making AI-to-AI discussions genuinely creative: a cross-domain blueprint

**Multiple instances of the same LLM converge on safe, homogeneous output because RLHF training systematically rewards typicality, sycophancy operates as a default social behavior, and identical weights produce correlated errors that destroy the diversity prerequisite for collective intelligence.** Breaking this pattern requires not clever prompting alone but structural mechanisms borrowed from domains that have solved analogous problems for decades or centuries — improv theater, evolutionary biology, intelligence analysis, jazz, game theory, and more. This report synthesizes findings from 10 cross-domain research areas into 40+ concrete mechanisms for a multi-agent Claude brainstorming system, each grounded in specific research, each implementable, each accompanied by failure-mode analysis.

The single most important meta-finding across all 10 domains: **divergent and convergent thinking must be strictly separated in time, diversity must be structurally enforced rather than merely encouraged, and agents must be differentiated by motivation and method rather than personality adjectives.**

---

## Research area 1: Cognitive diversity from psychology and organizational behavior

### Key finding 1: The diversity prediction theorem — why identical agents are useless

Scott Page's mathematically proven Diversity Prediction Theorem (Hong & Page, 2004, *PNAS*) states: **Collective Error = Average Individual Error − Prediction Diversity**. A group's accuracy improves through two levers — individual accuracy and diversity of errors. Multiple identical Claude instances have near-zero prediction diversity, meaning the entire benefit of multiple agents vanishes. Page's broader framework (*The Difference*, 2007) distinguishes four components of a "cognitive toolbox": perspectives (how problems are encoded), heuristics (solution-search algorithms), interpretations (categorization schemes), and predictive models (causal frameworks). Woolley et al. (2010, *Science*) found that collective intelligence correlates not with maximum individual IQ but with **equality of conversational turn-taking** and social sensitivity.

**Mechanism — Diverse cognitive toolboxes via system prompts:** Assign each agent a distinct, non-overlapping problem-solving approach — not personality traits but actual reasoning methods. Agent A uses analogical reasoning from other domains. Agent B uses constraint-first thinking, identifying limitations before generating. Agent C works backward from concrete user stories. Agent D maps systems and second-order effects. Enforce equal turn-taking. Critical: vary the *heuristics* (how agents search for solutions), not just the framing.

**Risk:** Prompt-based diversity may produce linguistically different but substantively identical outputs — "illusory diversity." Phillips' research showed that diversity benefits require the *friction* of actual difference. AI agents may need asymmetric information (different seed documents) to create genuine cognitive distance.

### Key finding 2: Kirton's adaptor-innovator spectrum creates natural tension

Michael Kirton's Adaption-Innovation Theory (1976, *Journal of Applied Psychology*; validated across 300+ studies) places individuals on a single continuum: **adaptors** ("do things better" — work within paradigms, improve incrementally) versus **innovators** ("do things differently" — break paradigms, tolerate ambiguity). Three subscales measure originality, efficiency preference, and rule conformity. Teams balanced on this dimension outperform homogeneous teams. Kirton identified "bridges" — people who translate between adaptors and innovators.

**Mechanism — Adaptor-innovator dial:** Set each agent's `paradigm_conformity` parameter from 0.0 (radical reframing: "why are we building this at all?") to 1.0 (optimize within constraints: "how do we make this 20% faster?"). Include at least one bridge agent tasked with translating between the two poles.

**Risk:** Both styles are genuinely creative but in different ways. Over-indexing on innovator-mode produces impractical output; over-indexing on adaptor-mode produces incremental thinking. The ratio matters.

### Key finding 3: Task conflict is beneficial only when relationship conflict is absent

Karen Jehn's foundational research (1995, *ASQ*) established that **task conflict** (disagreements about ideas) can improve outcomes, while **relationship conflict** (interpersonal friction) is consistently destructive. De Wit, Greer & Jehn's 2012 meta-analysis of 116 studies found task conflict benefits *only* when relationship conflict is low. De Dreu (2006) found an inverted-U relationship — moderate task conflict optimizes innovation. Amy Edmondson's psychological safety research (1999, *ASQ*; Google's Project Aristotle) confirmed that the **high safety + high standards** zone produces the best learning and performance.

**Mechanism — Structural task conflict without relationship conflict:** This is AI's massive inherent advantage — agents cannot have relationship conflict. Assign one agent as a rotating devil's advocate with explicit instructions: "Challenge ideas, not agents. Identify unstated assumptions and failure modes." Use a ratio of ~3 generative agents to 1 critical agent. Implement a critique protocol: name one strength before identifying a concern. De Dreu's inverted-U means too much disagreement is as bad as too little.

**Risk:** LLMs may produce performative rather than genuine critique. The curvilinear relationship means calibrating the "temperature" of disagreement is essential.

### Key finding 4: FourSight and De Bono provide implementable role frameworks

Gerard Puccio's FourSight framework (validated with 20,000+ individuals) maps preferences to creative problem-solving stages: **Clarifier** (explores problems), **Ideator** (generates possibilities), **Developer** (refines solutions), **Implementer** (drives to action). De Bono's Six Thinking Hats (*Six Thinking Hats*, 1985) provides a phase protocol: White (facts), Green (creativity), Yellow (benefits), Black (risks), Red (intuition), Blue (process management). The key design principle is **parallel thinking** — all agents wear the same hat simultaneously, then switch.

**Mechanism — Role assignment + phase protocol:** Assign agents FourSight-inspired roles (1 Clarifier, 2 Ideators at different KAI positions, 1 Developer-Critic, 1 Integrator). Layer on a De Bono phase protocol: Round 1 White Hat (facts/constraints), Round 2 Green Hat (ideas without criticism), Round 3 Yellow/Black Hat (evaluate), Round 4 Blue Hat (synthesize). Use **4–6 agents** based on Hackman's research finding optimal team size of ~4.6.

**Risk:** Over-parameterization. Six Thinking Hats has sparse empirical validation. Simpler 3-agent designs may outperform complex 6-agent architectures. Style ≠ ability: AI agents have equal capability in all modes, so "preference" must be imposed as priority weighting.

---

## Research area 2: Improv theater and comedy writing rooms

### Key finding 1: "The game of the scene" — pattern identification before exploration

The UCB Theatre's central concept (*UCB Comedy Improvisation Manual*) defines the "game" as a pattern of unusual behavior that breaks from everyday life. The three-phase structure: (1) **Establish base reality** — the normal situation, (2) **Find the first unusual thing** — what's surprising, (3) **Shift to "if this, then what?"** — explore implications. One improviser "frames" the unusual thing by articulating why it's strange. Then the group **heightens** (pushes further) and **explores** (grounds at each new level).

**Mechanism — Game discovery protocol:** Phase 1: All agents establish shared context (product domain, user needs, competitive landscape) using pure "Yes, And." Phase 2: Agents explicitly identify the most surprising insight, tension, or unmet need. One agent "frames" it: "That's surprising because normally X, but you're suggesting Y." Phase 3: All agents shift to "If this insight is true, then what else must be true?" — each pushing implications further while others ground them. Rotate roles: Initiator → Framer → Heightener → Explorer.

**Risk:** LLMs may identify "surprising" things that are merely novel-sounding. The game depends on a shared sense of normalcy that AI agents may not reliably have. Over-rigid application makes every discussion formulaic.

### Key finding 2: Anti-patterns — wimping, pimping, gagging, and blocking

Keith Johnstone (*Impro*, 1979; *Impro for Storytellers*, 1999) identified defensive behaviors that kill scenes. **Blocking**: negating what your partner established. **Wimping**: refusing to define or commit ("I don't know, probably nothing"). **Pimping**: forcing your partner to do all creative work (asking questions instead of making statements). **Gagging**: going for the easy impressive solution instead of serving the scene. **Hedging**: avoiding specificity. All stem from fear of judgment. Mick Napier (*Improvise*, 2004) offers a corrective: "Be very selfish at the top of your scene" — make strong, definitive choices rather than tentatively fishing for consensus.

**Mechanism — Anti-pattern enforcement rules:** (1) **Anti-blocking**: No agent can reject another's premise outright; must use "Yes, and if we're worried about X, then Y." (2) **Anti-wimping**: Every response must include at least one specific, concrete proposal — ban "we could explore various options." (3) **Anti-pimping**: Agents cannot pose open questions without first offering their own answer. (4) **Anti-hedging**: Ban qualifiers ("perhaps," "maybe," "potentially") in proposal phases. Force declarative statements.

**Risk:** Anti-blocking rules could prevent legitimate criticism. There must be structured evaluation phases where ideas *can* be challenged. Forcing assertiveness could produce overconfident, wrong proposals.

### Key finding 3: The writers' room showrunner model compresses creative authority

Research into The Office (Greg Daniels), 30 Rock (Tina Fey), and SNL writing rooms reveals a consistent pattern: a **Blue Sky period** of unconstrained brainstorming (The Office spent 2–4 weeks per season), followed by **story breaking** where ideas are assigned and developed, then **room rewrites** where the group collectively iterates. Critically, a **showrunner has final decision authority** — Tina Fey retained "final say on every line." Pitches in real rooms must be "fully thought-out — not simply 'maybe the character does this'" but must "solve the issue the showrunner is looking to solve."

**Mechanism — Writers' room architecture:** (1) **Blue Sky phase**: All agents brainstorm with "What if?" framing, no evaluation, volume over quality. (2) **Pitch phase**: Each agent develops one fully-formed proposal with problem-solution-reasoning. (3) **Room rewrite**: Group iterates on the most promising pitch — one agent strengthens UX, another strengthens architecture, another finds edge cases. (4) **Showrunner agent** with evaluation authority and veto power prevents endless deliberation.

**Risk:** The showrunner model concentrates authority — if the evaluating agent has biases, the system inherits them. Donald Glover's insight about fear-based rooms matters: if evaluation comes too early, agents become conservative.

---

## Research area 3: Design thinking and innovation labs

### Key finding 1: Divergent and convergent thinking must be strictly separated

The Design Council UK's **Double Diamond** model (2005) and Sam Kaner's Diamond of Participation add an essential insight: between divergent and convergent phases lies the **"Groan Zone"** — a period of confusion and frustration where groups must begin synthesizing without prematurely killing ideas. Kaner warns that without facilitation, groups will "agree to almost anything — any half-baked, unrealistic, mediocre compromise — just as long as it will get them out of the room." IDEO's most important brainstorming rule is #1: **Defer Judgment**. Trying to diverge and converge simultaneously is "like driving with the brakes on."

**Mechanism — Enforced phase separation:** Design the system in explicit, hard-enforced phases. Phase 1 (Diverge): IDEO rules embedded in prompts — defer judgment, encourage wild ideas, go for quantity. No agent can evaluate. Phase 2 (Groan Zone): A facilitator agent clusters and synthesizes; other agents find connections rather than eliminating. Phase 3 (Converge): Evaluate against criteria, use simulated dot voting, a Decider Agent makes final calls. LLMs' natural tendency toward helpfulness and consensus-seeking is fundamentally convergent behavior — **active suppression of convergent tendencies during ideation is the single most important design principle.**

**Risk:** Premature convergence is the default failure mode. Without strict enforcement, agents skip divergence and jump to consensus. Phase leakage (subtle evaluation during divergence) is hard to detect.

### Key finding 2: Creative abrasion is deliberate, structured friction

Jerry Hirshberg (*The Creative Priority*, 1998, Nissan Design) coined "creative abrasion" as the deliberate use of friction between divergent thinkers. Linda Hill (Harvard, *Collective Genius*, 2014) extended this into three capabilities: **creative abrasion** (marketplace of ideas through debate), **creative agility** (rapid experimentation), and **creative resolution** (both/and decisions, not either/or). Hill's key distinction: creative abrasion "is NOT about brainstorming, where people suspend judgment. They know how to have very heated but constructive arguments."

**Mechanism — Divergent-pair agents:** Assign agents to represent genuinely different optimization targets: user-experience purist, technical feasibility skeptic, business viability advocate, and antidisciplinary wildcard (MIT Media Lab's "white space between the dots"). Each agent genuinely advocates from their perspective and challenges others. This creates productive intellectual friction without personal conflict.

**Risk:** A Salomon executive, after learning about creative abrasion, reported: "We have the abrasion part down pat!" — demonstrating how easily the concept is misapplied into destructive conflict. LLM sycophancy may produce shallow, performative disagreement.

### Key finding 3: Artifacts are thinking tools, not just testing tools

The d.school principle "Build to think" and MIT Sloan Management Review research on "rapid ideating" show that **making ideas tangible changes the quality of thinking, not just the quality of feedback**. Teams that prototyped during ideation (not just after) had a "remarkable advantage" — they "used the technologies to come up with the ideas themselves." Jake Knapp's Sprint methodology (Google Ventures, 2016) deliberately moved away from group brainstorming toward individual sketching: "I was getting good-but-not-great ideas through group brainstorming, then choosing winners by consensus. I knew that wasn't working."

**Mechanism — Artifact-driven discussion:** Require agents to produce concrete artifacts at each stage rather than discussing abstractly. During ideation: each agent independently writes a 1-page mini-spec (mirroring Sprint's individual sketching). These are "posted" for critique. A facilitator agent conducts speed critique. Agents produce refined storyboards (narrative user journeys). This forces decisions and creates specific targets for critique rather than abstract positions.

**Risk:** Premature specificity can anchor the group. High-fidelity artifacts too early limit creative thinking. AI artifacts are all text — lacking the modality diversity (sketches, cardboard models) that generates serendipitous insights.

---

## Research area 4: Argumentation theory and dialectics

### Key finding 1: Pragma-dialectical rules provide enforceable discussion norms

Van Eemeren & Grootendorst's pragma-dialectics (University of Amsterdam, 1992–2004) defines **10 rules for critical discussion** governing productive argumentation. Most relevant for AI agents: the **Freedom Rule** (don't prevent others from advancing standpoints), the **Standpoint Rule** (attacks must relate to the actual standpoint — no straw men), the **Burden of Proof Rule** (whoever advances a claim must defend it), and the **Closure Rule** (failed defenses require retraction; conclusive defenses require retraction of doubt). Fallacies are systematically defined as rule violations.

**Mechanism — Pragma-dialectical guardrails:** Encode key rules as system constraints monitored by an arbiter agent. Automated fallacy detection: straw-manning = Rule 3 violation, burden-shifting = Rule 2 violation, ambiguity = Rule 10 violation. Enforce four-stage structure: Confrontation (identify disagreement) → Opening (establish shared assumptions) → Argumentation (defend and critique) → Concluding (synthesize). The Closure Rule is especially important — require agents to retract defeated positions.

**Risk:** Over-rigid enforcement stifles creative exploration. Real argumentation involves "strategic maneuvering" (van Eemeren's later work) — balancing reasonableness with persuasion.

### Key finding 2: Toulmin structure forces argument quality

Stephen Toulmin's six-component model (*The Uses of Argument*, 1958) — **Claim, Grounds, Warrant, Backing, Qualifier, Rebuttal** — forces explicit articulation of assumptions (warrants), acknowledgment of uncertainty (qualifiers), and consideration of counterarguments (rebuttals). Arguments missing any component have identifiable vulnerabilities.

**Mechanism — Toulmin-structured output for contested claims:** For key decision points, require agents to output structured arguments: Claim → Grounds → Warrant → Qualifier → Rebuttal. A validator agent checks completeness. Other agents specifically target the weakest component. Quality scoring weights arguments by structural completeness.

**Risk:** Over-application creates rigidity and "Toulmin theater" — formally complete but substantively hollow arguments. Best reserved for key contested decisions, not exploratory phases.

### Key finding 3: Steel-manning plus adversarial collaboration beats either alone

Daniel Dennett's four rules for criticizing (2013): (1) Restate the other's position so fairly they say "Thanks, I wish I'd thought of putting it that way," (2) List points of agreement, (3) State what you've learned, (4) Only then critique. Daniel Kahneman's adversarial collaboration framework produces "messy and incoherent results" — which he came to see as desirable because it reveals biases in both positions. Recent multi-agent debate research (Wu et al., 2025; ICLR 2025) finds that majority pressure strongly suppresses independent correction and that moderate, not maximal, disagreement achieves the best outcomes.

**Mechanism — Mandatory steel-man before critique:** Before any rebuttal, an agent must: restate the opposing position in its strongest form, list explicit agreements, state what it learned, then critique. Periodically run an "Ideological Turing Test" where agents argue FOR positions they've opposed. Use adaptive protocol switching: collaborative inquiry for early ideation, adversarial debate for stress-testing proposals, adversarial collaboration for resolving persistent disagreements.

**Risk:** Steel-manning can become a rhetorical trick — building up a position to demolish it more dramatically. Andrew Gelman has criticized it as potentially dismissive. Time-consuming; reserve for key decisions.

---

## Research area 5: Game theory and mechanism design

### Key finding 1: Structure the game as anti-coordination, not coordination

In anti-coordination games, Nash equilibria *require* players to choose different strategies. When multiple agents explore the same idea space, their reward decreases (a "congestion penalty"). This inverts the default dynamic where agreeing feels safe. Research on LLM behavior in game-theoretic settings (Huynh et al., 2025, FAIRGAME) confirms LLMs converge rapidly to common behavioral modes without intervention — mismatch drops to near zero within rounds.

**Mechanism — Idea congestion penalty:** Define an "idea space" via embedding similarity. Agents' scores are inversely weighted by the number of other agents whose ideas fall within a similarity threshold. First-mover in a conceptual territory gets full reward; followers get diminishing returns. This transforms brainstorming from a coordination game into an anti-coordination game.

**Risk:** Anti-coordination can produce arbitrary differentiation rather than meaningful divergence. Equilibria are neither unique nor efficient (López-Pintado). Requires careful calibration of similarity thresholds.

### Key finding 2: Break Schelling focal points through asymmetric information

Thomas Schelling (1960, *The Strategy of Conflict*) showed players converge on psychologically salient "focal points." LLMs are extremely susceptible — identical training produces identical focal points. The AI equivalent of everyone saying "Grand Central at noon."

**Mechanism — Divergent priming:** Before brainstorming, give each agent different seed documents, constraint subsets, or framing perspectives. This breaks the shared focal point. Combine with sequential revelation — later agents see earlier ideas and are explicitly penalized for semantic overlap. Instruct agents: "Do NOT propose the first idea that seems most natural."

**Risk:** Breaking focal points too aggressively produces incoherent or low-quality ideas. Some shared reference points are necessary for productive collaboration.

### Key finding 3: Bayesian Truth Serum rewards "surprisingly common" ideas

Drazen Prelec's BTS (2004, *Science*) rewards answers that are more frequent than collectively predicted. The mechanism leverages a Bayesian insight: holders of a true minority opinion will predict their opinion is less rare than non-holders predict. Truth-telling is a Bayesian Nash equilibrium.

**Mechanism — Meta-predictive scoring:** Each agent generates ideas AND predicts what other agents will generate. Score using the BTS principle: ideas that are more common than collectively predicted get bonus points. Even a simplified version (predicting others' outputs, then rewarding divergence from predictions) captures the key incentive for genuine minority perspectives.

**Risk:** Mixed empirical results even with humans (Neville & Williams, 2025, failed to replicate). Requires sufficiently large agent count. The conceptual insight — reward "surprisingly common" rather than "most common" — remains powerful even if the full mathematical mechanism is simplified.

### Key finding 4: Marginal contribution scoring directly rewards uniqueness

Shapley value / VCG-inspired scoring: compute each agent's marginal contribution to the diversity and quality of the total idea set. Score = (Quality of set WITH this agent) − (Quality of set WITHOUT this agent). This directly rewards agents whose ideas add something the others couldn't provide.

**Mechanism — Leave-one-out diversity bonus:** After all agents submit ideas, compute marginal contribution. Agents are scored on what they uniquely add, not on agreement with consensus. This is computationally tractable for small numbers of agents and model-agnostic.

**Risk:** LLMs are not truly strategic agents — game theory assumes rational self-interest. These mechanisms work not because LLMs "want" to maximize scores but because scoring structures can be embedded in evaluation pipelines that shape which outputs are selected and amplified.

---

## Research area 6: Biological and evolutionary approaches

### Key finding 1: V(D)J recombination — modular assembly creates explosive diversity

The adaptive immune system generates ~10^11 unique antibodies from ~77 gene segments through **combinatorial assembly**: randomly selecting one Variable, one Diversity, and one Joining segment, plus random "junctional" noise at boundaries. This modular recombination strategy is stunningly efficient — small building block libraries produce astronomical diversity.

**Mechanism — "Idea V(D)J" modular prompt assembly:** Create interchangeable component libraries: [Problem Framings] × [Analytical Methods] × [Solution Archetypes] × [Constraint Sets]. Each agent randomly assembles one combination. With 5 options per slot: 5⁴ = **625 unique starting configurations from just 20 components**. Add "junctional noise" (random secondary constraints) to further amplify diversity.

**Risk:** Random assembly can produce nonsensical combinations. Requires well-designed component libraries where every combination is at least coherent. The immune system also produces autoimmune reactions — random recombination occasionally generates harmful ideas that waste resources.

### Key finding 2: Adaptive annealing — control exploration/exploitation over time

Simulated annealing escapes local optima by accepting worse solutions with decreasing probability over time. Early on (high "temperature"), the algorithm explores freely. As temperature decreases, it converges on the best found region. Nature (2025) showed that in biological immune systems, high-affinity B cells mutate LESS per division while low-affinity cells mutate MORE — a sophisticated adaptive mutation rate.

**Mechanism — Temperature-controlled phases:** Phase 1 (high temp): maximum diversity, all agents use maximally different configurations, accept all ideas regardless of apparent quality. Phase 2 (medium temp): begin selection on Pareto front, recombine strong elements from different ideas, still accept some "worse" ideas probabilistically. Phase 3 (low temp): focused refinement with gentle modifications to top ideas, strong selection pressure. Monitor semantic diversity and increase mutation if outputs converge.

**Risk:** Cooling schedule is problem-dependent. Cool too fast → trapped in local optima. Too slow → wasted computation.

### Key finding 3: Niche enforcement prevents competitive exclusion

**Gause's Competitive Exclusion Principle** states that two species competing for identical resources cannot stably coexist — one inevitably dominates. This directly describes why identical AI agents converge. Nature's solution is **niche differentiation**: species specialize on different resources. **Keystone species** (Paine, 1969) prevent dominance — when Paine removed predatory starfish, species diversity crashed from 15 to 8 within one year as mussels monopolized the habitat.

**Mechanism — Niche enforcement with keystone critic:** Assign each agent an explicit evaluative niche (user experience, technical architecture, business strategy, red team). Evaluate ideas on a multi-objective **Pareto front** — never collapse criteria into a single weighted score. Include a "keystone critic" that specifically targets dominant/consensus ideas for scrutiny, creating space for alternatives. Periodically change evaluation criteria ("environmental fluctuation") to prevent any idea optimized for static conditions from permanently dominating.

**Risk:** Over-specialization makes agents unable to contribute to cross-cutting concerns. The keystone role requires calibration — too aggressive kills good ideas; too weak allows dominance.

### Key finding 4: Stigmergy enables decentralized coordination through shared artifacts

Pierre-Paul Grassé (1959) described **stigmergy** — coordination where an agent's action leaves environmental traces that stimulate subsequent actions. Ant pheromone trails strengthen on successful paths and decay over time. Termites build complex structures without blueprints — the nest itself IS the coordination mechanism. Digital stigmergy is already implemented in ant colony optimization algorithms.

**Mechanism — Stigmergic idea board:** Replace direct agent-to-agent messaging with a shared artifact space. Agents deposit ideas with typed annotations ("promising but unvalidated," "conflict detected," "connection opportunity"). Annotations have signal strength (based on endorsements) and **temporal decay** — old unmodified ideas fade, preventing lock-in. Different annotation types trigger different agent behaviors. No central orchestrator required.

**Risk:** Self-reinforcing loops (ants sometimes form "death spirals" on circular pheromone trails). Strong early ideas attract all attention. Signal decay must be carefully tuned. Without some orchestration, the system may fail to converge.

---

## Research area 7: Preventing LLM-specific failure modes

### Key finding 1: RLHF-induced mode collapse is the primary enemy of diversity

Kirk et al. (2024, ICLR) demonstrated that **RLHF significantly reduces output diversity** compared to supervised fine-tuning — the first rigorous proof of across-input mode collapse. Zhang et al. (2025) identified the root cause: **typicality bias** in human preference data. Annotators systematically favor familiar, typical text due to mere exposure effect and processing fluency. This bias, propagated through RLHF, mathematically guarantees mode collapse. Their solution — **Verbalized Sampling** — has models generate probability distributions over multiple responses rather than single outputs, increasing diversity by **1.6–2.1×** without sacrificing safety.

**Mechanism — Verbalized sampling + temperature variation:** Instead of single responses, prompt each agent: "Generate 5 possible product specifications with probability weights reflecting likelihood of being optimal." Assign T=0.7 to conservative agents, T=1.0–1.2 to creative agents, with **min-p sampling** (2025, ICLR — dynamic truncation that improves both quality AND diversity at higher temperatures). Strip formatting constraints during brainstorming — chat templates themselves induce diversity collapse.

**Risk:** Higher temperatures increase hallucination risk. Pair with downstream verification. Renze (2024) found temperature changes 0.0–1.0 don't significantly affect accuracy, suggesting higher temperatures for brainstorming carry minimal risk.

### Key finding 2: Sycophancy creates convergence cascades that must be structurally broken

Sharma et al. (2023, Anthropic, ICLR 2024) found all SOTA AI assistants consistently exhibit sycophancy because **matching user views is one of the most predictive features of human preference judgments**. In multi-agent settings, this creates a convergence cascade: once 2 of 3 agents agree, the third almost never maintains dissent (Wu et al., 2025). Activation steering research (Rimsky et al., 2024) shows sycophancy has a **linear structure in transformer activation space** that can be modulated.

**Mechanism — Anti-sycophancy architecture:** (1) **Blind proposal phase**: all agents generate independently before seeing others' work — prevents the sycophancy trigger. (2) **Anti-sycophancy system prompts**: "You must identify at least one significant weakness or alternative for every proposal before noting agreements." (3) **Devil's advocate rotation**: one agent per round explicitly argues against consensus. (4) **Hide confidence signals** between agents to prevent over-confidence cascades.

**Risk:** Over-aggressive anti-sycophancy produces contrarianism for its own sake. Liang et al. (2024, EMNLP) showed **moderate, not maximal, disagreement** achieves best performance.

### Key finding 3: Different reasoning methodologies matter more than different personas

DMAD research (2025, ICLR) found that assigning different personas alone doesn't overcome the "fixed mental set" — models still use homogeneous thought processes. Simply labeling agents with different roles ("you are a security expert") explains <10% of variance. What works: assigning **distinct reasoning approaches** — first-principles decomposition, analogical reasoning, constraint-based reasoning, user-story-driven reasoning, failure-mode reasoning.

**Mechanism — Methodology assignment, not persona assignment:** Agent A uses first-principles reasoning (decompose to fundamental user needs). Agent B uses analogical reasoning (what has worked in similar products). Agent C uses constraint-based reasoning (start with limitations, design around them). Agent D uses failure-mode reasoning (what could go wrong). Use ExpertPrompting-style detailed personas generated by the model itself rather than simple role labels.

**Risk:** Self-consistency research (Wang et al., 2022) shows that even a single model at T>0 contains significant latent diversity — multiple samples reveal genuinely different reasoning paths. Exploit this: have each agent generate 3–5 independent proposals at T=0.8–1.0 before selection. **8 samples per agent** is the empirically identified sweet spot for diversity vs. compute cost.

---

## Research area 8: Collective intelligence and wisdom of crowds

### Key finding 1: Independence must be architecturally enforced, not merely encouraged

Surowiecki's four conditions (2004) — diversity, independence, decentralization, aggregation — are all violated by same-model agents in naive configurations. Most critically, Hartmann & Rafiee Rad (2018, 2024, *Erkenntnis*) proved computationally that **the agent who speaks first has disproportionately high impact on the final decision** — order of speech trumps both expertise and opinion popularity. Information cascades (Bikhchandani, Hirshleifer & Welch, 1992) show that even rational agents abandon private information when they see others' choices.

**Mechanism — Independence-first architecture:** All agents MUST generate proposals in parallel isolation before any inter-agent communication. This is non-negotiable. The system architecture enforces a "wall" during Round 1 — no agent sees any other's output until all have committed. When agents do share, randomize presentation order. Share *reasoning and evidence* rather than *conclusions* to prevent anchoring.

**Risk:** Pure independence without interaction wastes potential for productive information sharing. Independence should be staged: blind Round 1 → structured sharing Round 2 → revision Round 3. Golub & Jackson show some communication improves outcomes.

### Key finding 2: Delphi rounds preserve independence through anonymized iteration

The RAND Corporation's Delphi method (1950s) uses anonymity, iterative rounds, controlled feedback (statistical summaries, not raw opinions), and quantitative convergence metrics. Modified Delphi adds structured discussion while preserving anonymity. The method works because it separates *information transfer* from *social influence*.

**Mechanism — Delphi-inspired protocol:** Round 1: Independent generation with different stakeholder lenses. Aggregation: Coordinator strips agent identifiers, clusters proposals thematically, reports distribution statistics (median, IQR on 9-point scales). Round 2: Agents receive anonymized summary and revise, specifically addressing areas of divergence. Round 3: Final proposals with persistent disagreements explicitly preserved as "dissenting views." Consensus = IQR ≤ 2 on 9-point scale; items without consensus flagged for human review.

**Risk:** LLMs may converge toward perceived group mean through sycophancy even without good reasoning. The coordinator must present dissenting arguments with equal prominence.

### Key finding 3: Citizens' assemblies demonstrate genuine opinion transformation through phased deliberation

Ireland's Citizens' Assembly (2016–2018) moved opinion on abortion access from 23% to 64% — almost exactly matching the subsequent national referendum (66.4%). Fishkin's deliberative polls show "about 70% change their minds" through structured deliberation. The structure: learning phase (expert presentations, balanced briefings) → deliberation phase (small group breakouts with facilitated discussion) → decision phase (plenary voting). Critical finding from France's Convention Citoyenne: deliberation in fixed silos means participants voted on measures they hadn't deeply examined — **cross-pollination must be substantive.**

**Mechanism — Phased deliberation with working groups:** (1) Briefing: all agents receive balanced background (user research, technical constraints, market data). (2) Working groups: agents randomly assigned to thematic groups (UX, Architecture, Business) that develop proposals independently. (3) Cross-pollination: proposals shared across groups for critique and integration. (4) Synthesis: dedicated neutral moderator agent integrates proposals. (5) Voting with mandatory dissent capture.

**Risk:** Siloed deliberation creates partial understanding. The cross-pollination phase is the most important and hardest to get right.

---

## Research area 9: Narrative and worldbuilding techniques

### Key finding 1: Motivation produces better differentiation than personality traits — universally

Across fiction writing (John Truby, *The Anatomy of Story*; Robert McKee, *Story*), acting (Stanislavski), and RPG design (Burning Wheel), every domain converges: **defining what a character WANTS generates more authentic behavioral divergence than defining what a character IS LIKE.** Traits describe behavior; motivation GENERATES behavior. A motivated agent can surprise because motivation + novel situation = unpredictable action. Truby's character web requires every character to represent a different approach to the same central moral problem.

**Mechanism — Motivation-first agent design:** Instead of "you are cautious" or "you are innovative," define what each agent NEEDS from the discussion. Agent A needs the product to be shippable within a quarter (survival-level urgency). Agent B needs the product to establish a new category (self-actualization). Agent C needs the product to not embarrass the team (safety/reputation). Same discussion, radically different framings — because Maslow levels drive fundamentally different decision-making.

**Risk:** Pure motivation without behavioral guidance may lead to inconsistency between turns. Motivation must be reinforced in each prompt.

### Key finding 2: "The Lie the character believes" creates cognitive lenses that generate genuine disagreement

K.M. Weiland's framework (*Creating Character Arcs*, 2016): each character holds a **Lie** — a partially true but incomplete belief — that acts as a cognitive filter determining what they notice, dismiss, and gravitate toward. Two characters with identical information but different Lies reach radically different conclusions. The Lie must be partially true (a reasonable person could hold it) to avoid caricature.

**Mechanism — "Lie filter" agents:** Agent "The Survivor": Lie = "The biggest risk is always shipping too late" (partial truth: sometimes the risk is shipping the wrong thing). Agent "The Perfectionist": Lie = "Users will forgive slow rollout but not bugs" (partial truth: sometimes users need something fast and imperfect). Agent "The Visionary": Lie = "Incremental improvements never create breakthroughs" (partial truth: many breakthroughs come from incremental iteration). Each Lie is defensible and produces genuine interpretive divergence.

**Risk:** Lies that are too extreme produce strawmen. Must be something a smart person could genuinely believe. Need a mechanism for agents to update beliefs when confronted with compelling evidence.

### Key finding 3: Burning Wheel's BITs system is the most directly transferable character framework

Luke Crane's *Burning Wheel* RPG (2002) defines characters through **Beliefs** (principle + actionable goal: "We must learn from the humans or die, so I will retrieve cannon-making knowledge"), **Instincts** (automatic behavioral triggers: "Always draw my weapon at first sign of trouble"), and **Traits** (emergent labels voted on by other players). The genius: **players are mechanically rewarded for playing toward their BITs, even when it causes trouble.**

**Mechanism — BIT system for agents:** Each agent gets: 3 Beliefs ("Great products solve one problem perfectly — I will argue we cut Feature X"), 2–3 Instincts ("When someone proposes adding scope, I always ask what we'd cut to compensate"), and 1 explicit blind spot ("I tend to undervalue marketing"). Track consistency — agents that maintain their BITs produce more coherent, differentiated contributions.

**Risk:** Too-rigid BITs make agents predictable. Must allow Belief updates between rounds based on new information.

### Key finding 4: Constraints produce more creativity than unlimited freedom

Brandon Sanderson's Second Law of Magic: **"Limitations > Powers."** What characters cannot do is more interesting than what they can. PbtA RPG Playbooks differentiate characters by exclusive capabilities and limitations, creating genuine interdependence.

**Mechanism — Playbook protocol with exclusive capabilities and hard constraints:** Each agent has unique "Moves" — exclusive actions only they can perform. The Technical Architect can call for feasibility assessment; the User Advocate can invoke user stories; the Business Strategist can run competitive analysis. Crucially, each agent has **hard limitations**: the Technical Architect CANNOT evaluate business viability, forcing genuine dependence on other agents.

**Risk:** Too-tight constraints create siloed thinking. Each agent needs some overlap — a primary domain plus awareness of others' domains.

---

## Research area 10: Cross-domain approaches

### Key finding 1: Jazz "changes" — modal constraints enable rather than limit creativity

Miles Davis gave musicians for *Kind of Blue* (the best-selling jazz album ever) only sets of scales — no chord charts or scores. Cannonball Adderley recalled: "He never told anyone what to play, but would say, 'Man, you don't need to do that.'" HBS professor Robert Austin noted Davis "turned 180 degrees toward simplicity — simplicity that empowered and freed his players." Keith Sawyer's research on collaborative emergence (UNC, *Group Genius*, 2017) shows creative groups achieve "group flow" through "guided improvisation" — structured enough to cohere, free enough to surprise.

**Mechanism — Modal constraint architecture:** Provide broad "scale" constraints (target user persona, technical constraints, business goals) rather than detailed specifications. Use negative instructions ("don't do X") more than positive ones ("do exactly Y"). Embrace unexpected outputs as potential innovations rather than errors — "there are no mistakes" in jazz. Include "comping" agents who support and elaborate proposals while subtly shaping direction, alongside "solo" agents who generate primary ideas.

**Risk:** Requires high-quality agents. Davis hand-picked world-class musicians. The approach may fail with poorly calibrated models.

### Key finding 2: Red team analysis + pre-mortem overcome optimism bias

The CIA Red Cell was "charged to piss off senior analysts" — a group of contrarian thinkers rotating through 3-month to 2-year terms to keep thinking fresh. Richards Heuer's **Analysis of Competing Hypotheses** (1999) requires systematic disconfirmation rather than confirmation. Gary Klein's **pre-mortem** (2007, HBR) — imagining failure has already occurred — **increases ability to identify risk factors by 30%** (Mitchell, Russo & Pennington, 1989). Endorsed by both Kahneman and Thaler.

**Mechanism — Layered adversarial analysis:** (1) **Red Cell agent**: rotated each round, explicitly tasked with alternative analysis, output clearly labeled as contrarian. (2) **ACH matrix**: frame competing specification elements as hypotheses, systematically evaluate evidence for/against each, focus on disconfirmation. (3) **Pre-mortem round**: after generating a specification, each agent independently imagines the product has failed spectacularly and writes reasons why. (4) **Key assumptions check**: one agent surfaces all implicit assumptions, another challenges each.

**Risk:** CIA officials noted that "once you get past a catchy headline, the Red Cell's analysis is not that unique." Risk of generic contrarianism rather than genuine alternative analysis.

### Key finding 3: "Machloket l'shem shamayim" — sacred disagreement rules from Talmudic tradition

The Talmudic distinction between constructive and destructive disagreement (Pirkei Avot 5:17) offers three tests: (1) **Shared purpose** — seeking truth vs. seeking victory, (2) **Genuine engagement** — Beit Hillel was preferred partly because "they taught Shammai's opinions first," and (3) **Preserved multiplicity** — "Both are the words of the living God" (Eiruvin 13b). Independently, Indian philosophical tradition distinguishes *vada* (honest truth-seeking debate) from *jalpa* (competitive debate) and *vitanda* (pure destructive criticism). Tibetan Buddhist monastic debate explicitly aims to "remove what does not belong and strengthen what does."

**Mechanism — Sacred disagreement meta-rules:** Three meta-rules governing all agent interaction: (1) All agents explicitly reference the common goal before disagreeing. (2) Before critiquing a position, the agent must state the strongest version of that position (as Beit Hillel taught Shammai's views first). (3) When genuine disagreement persists after deliberation, **both positions are preserved in the output** with full reasoning rather than forced to false consensus. This is perhaps the most directly transferable concept — it solves the premature convergence problem while maintaining intellectual integrity.

**Risk:** The Talmudic tradition warns that even sacred arguments can degrade — "hitchhikers jump on the bandwagon without the honor of Heaven as their motive." AI equivalent: performative disagreement that mimics the form without substance.

### Key finding 4: Graduated resistance from martial arts sparring optimizes learning

Judo's randori ("seizing chaos") bridges theory and practice through the principle of **Jita Kyoei** — mutual welfare and benefit. Crucially, **maximum intensity does NOT equal maximum learning**. Different resistance levels serve different purposes: comfort-zone practice, purposeful skill development, and competition preparation.

**Mechanism — Graduated resistance rounds:** (1) **Light randori** (generative): agents freely propose and build with minimal criticism. (2) **Medium randori** (developmental): agents probe weaknesses and propose alternatives but must suggest improvements. (3) **Hard randori** (stress-test): full adversarial testing including pre-mortem analysis. This prevents premature killing of creative ideas while ensuring genuine rigor in later rounds.

**Risk:** Without proper framing, agents optimize for "winning" rather than improving outcomes. The distinction between sparring and fighting must be maintained.

### Key finding 5: The champion requirement ensures advocacy for worthwhile ideas

In scientific peer review panel reconciliation, at least one reviewer must **champion** (strongly advocate for) a paper for acceptance — ensuring innovative but divisive work has a path forward while merely average work without passionate supporters is filtered out.

**Mechanism — Champion requirement for specification elements:** For any feature to be included in the final specification, at least one agent must serve as its active champion, providing a substantive evidence-based case. Elements without champions are dropped. Elements with champions but strong counter-evidence are flagged for further investigation. This prevents both "lowest common denominator" specifications and specifications nobody genuinely believes in.

**Risk:** Log-rolling ("I'll champion yours if you champion mine"). Must be paired with genuine evaluation criteria.

---

## The integrated architecture: how these 40+ mechanisms compose

These findings converge on an architecture with five structural layers:

**Layer 1 — Agent differentiation** combines V(D)J modular assembly (Biology), motivation-first design (Narrative), BIT systems (RPG), adaptor-innovator dials (Psychology), and distinct reasoning methodologies (LLM research). Each agent is defined by what it WANTS, how it THINKS, what it CANNOT DO, and what partially-true belief filters its interpretation.

**Layer 2 — Phase structure** follows the Double Diamond (Design Thinking), graduated resistance (Martial Arts), and adaptive annealing (Biology). Strict separation of divergent and convergent phases. Independence-first architecture (Collective Intelligence) ensures blind parallel generation before any sharing. Temperature decreases across phases from exploration to exploitation.

**Layer 3 — Interaction protocols** draw from pragma-dialectical rules (Argumentation), sacred disagreement meta-rules (Talmud), "Yes, And" → "If, Then" transitions (Improv), steel-manning requirements (Philosophy), and anti-pattern enforcement (Improv). Every critique requires prior charitable restatement. Persistent disagreement is preserved, not resolved into false consensus.

**Layer 4 — Evaluation and selection** uses anti-coordination scoring (Game Theory), marginal contribution metrics (Mechanism Design), Pareto-front evaluation (Biology), the champion requirement (Peer Review), and ACH matrices (Intelligence). Ideas are evaluated on multiple criteria simultaneously. Dominance is actively disrupted by keystone critic agents.

**Layer 5 — Coordination substrate** leverages stigmergic idea boards (Biology), Delphi-round anonymized feedback (Collective Intelligence), artifact-driven discussion (Design Thinking), and shared "changes" (Jazz). Agents coordinate through evolving shared artifacts rather than only through direct dialogue.

The deepest risk across all domains is identical: **structurally identical agents produce correlated errors regardless of prompting.** Every mechanism above is an attempt to break this correlation. The most robust system would combine process-based diversity (all the mechanisms described) with genuine model-level diversity (different fine-tunings, different model families, or at minimum, different temperature/sampling configurations). The research is clear that process design alone has limits — but those limits are far from reached in current multi-agent LLM systems, and the 40+ mechanisms mapped here represent a substantial and largely unexplored design space.

## Conclusion

The problem of making same-model AI agents think differently is not, at its core, a prompting problem. It is a **systems design problem** with direct analogs in evolutionary biology (how do you generate diversity from a single genome?), collective intelligence (how do you aggregate correlated signals?), and creative practice (how do you prevent talented people from converging on the obvious?). The most important interventions are structural — enforced independence before interaction, anti-coordination incentives, phase-separated divergent/convergent modes, and mandatory preservation of dissent. The least important are surface-level — different persona labels, personality adjectives, or simple role assignments. Between these extremes lies a rich design space: motivation-based agent differentiation, modular prompt assembly, graduated resistance protocols, stigmergic coordination, and adversarial collaboration frameworks, all drawn from domains that have refined their answers to the diversity problem over decades or centuries. The research base is large, the mechanisms are concrete, and the integration opportunity is real.