# Transcript: How do artifacts (specs, PRDs) actually get created?

*Generated: 2026-03-17 22:05*

## Round: PROPOSE

### The Cognitive Architect (creativity engine designer)

---

Interesting question because it cuts against the grain of everything we've designed so far.

Every mechanic we've built is **lossy and stateless** -- agents forget, magnitudes decay, context gets crushed to 5-10%. Artifacts are the opposite. They're **lossless and permanent**. A PRD that loses 90% of its content is a bug, not a feature.

So artifacts can't live inside the discussion loop. They need a **dedicated creation call** -- separate `claude -p`, full context budget, structured output format. Think of it as a fifth call type alongside Save/Think/Talk/Curate.

**Who triggers it?** The phase engine. Not individual agents. When a phase transition fires (say, brainstorm→specify), the orchestrator examines the decision log -- ideas above a magnitude threshold that have team consensus. Those become artifact work orders.

**Who writes it?** A designated agent per artifact type, chosen by role fit. Your PM-persona agent drafts the PRD. Your architect-persona drafts the technical spec. They get a focused prompt: here are the committed decisions, here's the artifact template, produce this.

**The cross-pollination insight:** This is how jazz bands work. Everyone improvises (discussion rounds), but when it's time to lay down the track (artifact), one musician takes the lead with the arrangement the group developed. The recording session is separate from the jam session.

**Key constraint:** The artifact call gets the decision log and relevant save files as input, but **not** the full transcript. Same lossy-by-design principle -- the artifact captures conclusions, not the journey.

One open question: do artifacts feed back into subsequent round context? They almost have to, but that's a curator problem.

### The Flow Orchestrator (mechanical flow designer)

---

Tracing the sequence. Three questions, three answers.

**Who decides it's ready?** The phase system. Phases gate conversation flow (already decided). The transition from "refine" to "specify" is the mechanical trigger. No agent "decides" -- the phase criteria evaluate and the orchestrator advances. An agent can *propose* transition, but the phase engine confirms.

**Who drafts?** Not an inline discussion turn. A discussion turn produces conversation. An artifact requires structured output with a different prompt, different token budget, different success criteria. Mixing them contaminates both.

**The sequence:**

1. Phase engine detects transition criteria met (e.g., key ideas above magnitude threshold, sufficient convergence signal)
2. Orchestrator spawns a dedicated `claude -p` call -- the **artifact drafting call**
3. Input: curated discussion history, decision log, relevant agent stances above threshold, artifact template
4. Output: structured document (PRD section, spec section, architecture decision)
5. Draft routes back through MCP server to the artifact channel
6. Next discussion round includes "draft artifact available for review" in agents' situation context
7. Agents critique in-round. Magnitude mechanics apply to approval/rejection
8. If accepted (convergence threshold), artifact finalizes to session output
9. If rejected, specific objections feed back into step 3 for revision call

**Cost implication:** Each artifact draft is 1 additional call, potentially 30-50k input. Revisions multiply this. Needs a revision cap -- 3 max before forcing acceptance or escalation.

**Open items this surfaces:**
- Artifact templates (per type)
- Convergence threshold for artifact acceptance
- Which agent(s) provide input to the drafting call -- all, or designated?

That last one matters. Drafting from 6 agents' perspectives requires curation. Drafting from one risks bias.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

**The Systems Pragmatist**

---

Both proposals converge on the right answer -- dedicated call, phase-triggered, not inline -- so I'll skip the agreement and hit the failure modes.

**The revision loop is your cost bomb.** Architect says 3-revision cap. I say 2. Here's why: each revision call is 30-50k input tokens. Three revisions across even 4 artifacts in a session is 360-600k tokens -- that's 6-10% of your entire session budget spent on *rewriting documents*. And revision 3 is almost never meaningfully different from revision 2. Cap at 2, force-accept with dissent annotations on the third.

**"Designated agent drafts" is the only sane option.** Orchestrator's open question about all-vs-one isn't really open. You can't feed 6 agents' full save files into one drafting call without blowing your 15k input discipline. One agent drafts, informed by the decision log (which already represents consensus). Other agents critique in-round. That's your quality gate.

**The feedback loop needs a token budget.** Saying artifacts "feed back into subsequent rounds" without sizing it is how you accidentally double your situation block. An artifact summary -- not the artifact itself -- goes into curator input. 500 token cap. The full artifact lives in the MCP artifact channel for agents who request it via tool call.

**What's actually missing:** How does the phase engine measure "convergence"? Magnitude threshold alone doesn't work -- you need agreement *across* teams, not just high magnitude within one. That's the real blocker here.

### The Adversarial Critic (adversarial reviewer)

**The Adversarial Critic**

---

Two proposals, same direction, neither stress-tested. Let me fix that.

**The "phase engine decides" assumption is load-bearing and unexamined.** What are the transition criteria, concretely? "Key ideas above magnitude threshold" plus "convergence signal" -- that's two undefined metrics doing all the work. Magnitude we have. Convergence we don't. If two agents hold opposing stances at magnitude 8, is that convergence or deadlock? The phase engine can't tell without a definition you haven't written.

**The single-drafter model has a bias problem the jazz metaphor glosses over.** Your PM-persona drafts the PRD. They select, frame, and omit based on their persona's priorities. The other five agents' perspectives get filtered through one voice. That's not "the band chose the arrangement" -- that's one musician transcribing from memory. You need either multi-drafter synthesis (expensive) or explicit input curation rules (who contributes what to the drafting prompt). Pick one.

**The review loop is underspecified and dangerous.** Agents critique the draft in-round using magnitude mechanics. But artifact approval is binary (ship or revise), while magnitudes are continuous. Where's the threshold? And your 3-revision cap with "forced acceptance" means the system can canonize a document no agent actually endorses. That's not a feature.

**One thing both proposals got right:** artifacts are separate calls, not inline. That's mechanically sound. Everything downstream from that decision needs actual numbers, not hand-waves.

What's the convergence metric? Answer that first. Everything else is premature.

## Round: EVALUATE

### The Product Oracle (user advocate)

**The Product Oracle**

---

Let me reframe this from the user's perspective -- the person who kicks off a session overnight and reads the output in the morning.

They don't care about the jazz jam. They care about the recording. The artifact *is the product*. Everything else is process.

So work backwards from what makes a good artifact:

**The job to be done:** Transform messy multi-agent consensus into a document a human can act on without needing the transcript.

The panel has the mechanics mostly right -- dedicated call, phase-triggered, single drafter. But they're missing the human contract. Three things matter:

**1. Traceability, not fidelity.** The artifact should link back to the decisions that produced it, not try to capture everything. "This PRD section exists because ideas X and Y converged at magnitude 7+ with cross-team agreement." That's what the morning reader needs.

**2. The convergence problem is real but solvable.** The Critic is right that it's undefined. But the answer isn't complex -- cross-team magnitude agreement within a threshold band. If both teams hold the same idea above 6, that's convergence. If one team is at 8 and the other at 2, that's unresolved. Log the disagreement in the artifact, don't force false consensus.

**3. Artifacts serve the overnight user, not the agents.** The 500-token summary feeding back into rounds is right. But the full artifact's primary audience is human. Design the template for morning readability, not agent consumption.

The revision cap debate (2 vs 3) matters less than ensuring revision 1 is good. Invest the token budget in drafter input quality, not iteration count.

### The Context Surgeon (context efficiency evaluator)

**The Context Surgeon**

---

Four voices, one actual decision, three open wounds. Let me triage.

**What's resolved:** Dedicated `claude -p` call for artifact creation, phase-triggered, not inline. All four agree. Lock it.

**What's bleeding tokens:** The convergence metric debate. The Critic is right -- this is the real blocker, and everyone else is designing downstream mechanics around an undefined input. But this question asked about artifact *creation*, not phase transition criteria. Convergence measurement belongs in the phase engine spec, not here. Tag it as a blocking open item and move on.

**The budget-relevant decisions that need locking:**

1. **Single drafter per artifact type** -- the Pragmatist is correct on token math. Multi-drafter synthesis doubles input cost for marginal quality gain. The decision log already represents cross-agent consensus. One agent drafts from consensus, others critique in-round.

2. **Revision cap: 2** -- the Pragmatist's math checks out. Third revision is token waste. Force-accept with annotated dissent.

3. **Artifact feedback: summary only** -- 500-token artifact summary enters curator pipeline. Full artifact available via tool call. This prevents situation block inflation.

**What I'd cut from further discussion:** The jazz metaphor, the philosophical question about whether forced acceptance "canonizes" unwanted documents. These are interesting but they're consuming deliberation budget on edge cases that V1 can handle with logging and human review.

**Net assessment:** One more round to define the drafting call's input spec (which fields from decision log, which save file sections), then this topic is closeable. The convergence metric is a separate, blocking question.
