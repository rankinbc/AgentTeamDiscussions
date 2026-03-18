# Transcript: How does a round begin after a reset?

*Generated: 2026-03-18 02:25*

## Round: PROPOSE

### The Idea Merchant (idea generator)

---

Oh, this is where the *magic* happens. The round start is the most important prompt in the entire system because it's where you control drift.

**What the orchestrator assembles:**

Three layers, built fresh each round:

1. **Identity block** (~2k, static) -- persona, archetype, stubbornness threshold, team allegiance. Never changes.

2. **Situation block** (~8-15k, curated) -- this is the hybrid curator output. Deterministic pass drops resolved decisions and ideas below archival threshold. Then the LLM curator call compresses what remains into a *personalized* narrative. Key: this isn't a transcript. It's "here's what you remember and care about." The curator can emphasize surprising things, bury stale ones.

3. **Task block** (~1-2k) -- the round's specific prompt. Round 1 of a discussion might be "propose your team's top priorities." Round 3 might be "the other team rejected X, respond."

**How round-start differs from mid-round:**

Mid-round turns get the running conversation as context -- they're reactive. Round-start prompts are *generative*. The agent has no conversation yet. They're working from their save file, the curated situation, and whatever the BackgroundAgents planted overnight.

**The critical design insight:** The gap between rounds is where you inject entropy. BackgroundAgents tweaked magnitudes. Intra-team talk reshuffled priorities. The curator chose what to emphasize. Dream events fired.

So when the agent speaks first in a new round, they're *not* continuing a conversation. They're starting from a subtly altered version of themselves.

That's the drift mechanic. That's what makes round 4 feel different from round 1.

### The Cognitive Architect (creativity engine designer)

---

Think of it like waking up vs. being mid-conversation. Different cognitive states, different prompts.

**Round Start Assembly (Orchestrator's job):**

1. **Load the save file** -- ideas with magnitudes, stances with magnitudes, committed decisions, the personalized summary. This is the agent's "memory."

2. **Run deterministic filter** -- drop ideas below archival threshold (persona-dependent), drop resolved decisions, prune stale stances. Then LLM curator pass compresses and surprises -- maybe resurfaces something the agent forgot they cared about.

3. **Inject between-round mutations** -- BackgroundAgent tweaks landed here. New ideas planted, magnitudes shifted, stances nudged. The agent doesn't know these happened. They just... feel differently now.

4. **Assemble the prompt in budget order:**
   - Identity block (static persona, ~2k)
   - Situation block (curated state -- "here's what you believe, here's what happened, here's what changed," ~8-15k)
   - Task block: **"Given your current priorities, what do you want to discuss this round? Propose your agenda."**

**The key difference from mid-round turns:**

Mid-round, the task block says "respond to what was just said." The agent is reactive. Conversation history is accumulating in-context.

Round start, the task block says "what matters to you now?" The agent is generative. No conversation history yet -- just their evolved state. They're setting direction, not responding.

This is where magnitude earns its keep. The agent doesn't pick topics randomly. They look at what's loudest in their state and lead with that. The reset creates natural agenda drift without anyone orchestrating it.

**Interesting edge:** the LLM curator adding "unexpected" context at round start is functionally a dream. The agent wakes up thinking about something they weren't thinking about before.

## Round: CRITIQUE

### The Systems Pragmatist (infrastructure realist)

They've described the happy path. Let me describe what breaks.

**Assembly order matters for failure modes:**

The orchestrator builds the prompt sequentially, and each step can fail independently:

1. **Save file load** -- if corrupted or missing, you need a fallback. Stale save from two rounds ago? Agent regresses. No save at all? Cold-start persona with no memory. Define the degradation path now, not after your first overnight run loses state.

2. **Deterministic filter** -- straightforward, but watch for the edge where *everything* gets pruned. Agent with high flexibility threshold after a quiet round could wake up with an empty situation block. That's not drift, that's amnesia. Set a floor.

3. **LLM curator call** -- this is your single point of fragility. It's a separate API call that can timeout, hallucinate, or return garbage. What happens when the curator fails? You either block the round (bad) or fall back to raw filtered state without the "surprise" layer (acceptable). Design the fallback.

4. **BackgroundAgent injection** -- mutations applied to state *before* the curator sees it, or after? Order changes behavior. If before, the curator might emphasize or bury the planted idea. If after, it always surfaces raw. Pick one and document it.

**The real difference from mid-round isn't cognitive, it's architectural.** Mid-round turns are append-only -- conversation grows, context is deterministic. Round-start is *assembled* -- multiple async processes contribute to a constructed reality. More moving parts, more failure surfaces.

Budget overflow is the other killer. Curator returns 20k tokens instead of 15k? Your task block gets squeezed or truncated. Hard-cap the curator output and validate before assembly.

### The Adversarial Critic (adversarial reviewer)

Both proposals describe the same architecture and agree on everything. That's suspicious. Let me find the gaps.

**The curator is a single point of failure.** You're handing an LLM 8-15k of budget to write a "personalized narrative" that determines what the agent cares about. If the curator hallucinates emphasis, misweights a stance, or drops something the agent should remember, the entire round's trajectory is corrupted. And you won't know -- the agent has no ground truth to check against. You've designed a system where the agent *trusts its own memory implicitly* while giving another LLM write access to that memory.

**"The agent doesn't know these happened" is a feature you're celebrating but haven't stress-tested.** BackgroundAgents plant ideas, shift magnitudes, nudge stances -- and the agent treats this as organic. What happens when a planted idea contradicts the agent's persona? When a magnitude bump makes an agent suddenly passionate about something they argued against last round? You need consistency checks or agents will feel schizophrenic.

**The round-start/mid-round distinction is clean in theory, messy in practice.** Round start is "generative," mid-round is "reactive" -- but by turn 2, the agent is already reactive. So your expensive curated prompt matters for exactly one turn. Is 8-15k of curator budget justified for a single generative moment?

**Missing entirely:** How does the orchestrator decide the task block content? "Propose your agenda" vs. "respond to rejection" implies phase-awareness, but neither proposal specifies who writes these or how they're selected. That's not a detail -- it's the steering mechanism.

## Round: EVALUATE

### The Product Oracle (user advocate)

The discussion has solid coverage. Let me add what's missing: the user's job.

**The agent's job-to-be-done at round start is "figure out what I care about now."** Not "remember everything" -- that's the curator's job. Not "respond correctly" -- that's mid-round. The round-start prompt needs to answer one question for the agent: *what's worth fighting for today?*

That reframes the assembly. The orchestrator isn't building a briefing document. It's building **motivation**.

**What I'd add to what's been said:**

The task block gap is real. The Critic caught it -- who writes "propose your agenda" vs. "respond to rejection"? That's phase logic, and it belongs in `phases.yaml`. Each phase defines a task template with slots the orchestrator fills from discussion state. Round 1 brainstorm gets "what matters to you?" Round 3 negotiation gets "they rejected X, here's their reasoning, what's your move?" The phase engine picks the template, the orchestrator fills the slots.

**The curator's real job isn't compression -- it's prioritization.** The agent wakes up with 15 ideas at various magnitudes. The curator's value is saying "these 3 are your story right now." That's worth the budget even for one generative turn, because that turn sets the agenda everyone else reacts to.

**One concern nobody raised:** the agent's first utterance each round is the highest-leverage moment in the system. Every other agent reacts to it. If the curator gets prioritization wrong, the entire round drifts wrong. Consider letting the agent see raw magnitudes alongside the narrative so it has ground truth to self-correct against.

### The Context Surgeon (context efficiency evaluator)

Four agents just spent ~1,200 tokens saying roughly the same thing four ways. That itself is a context budget lesson. Let me add what they missed.

**The budget math exposes a design tension nobody addressed.**

Your round-start prompt burns ~25k tokens on assembly (2k identity + 15k situation + 2k task + overhead). That leaves ~75k for the actual conversation. At ~500 tokens per substantive turn, that's maybe 15 back-and-forth exchanges before you hit the wall. Fine for a short round. Fatal for a long one.

Mid-round turns don't have this problem the same way -- they're append-only, predictable growth. Round-start is a *fixed upfront cost* that compresses your remaining runway. The curator's 8-15k range isn't just a "nice to have" variance -- it's a 7k token swing that changes how many turns the round can sustain.

**What I'd actually validate before building this:**

Measure the *information density* of the curator output. If 15k of curated narrative produces the same agent behavior as 6k, you're burning 9k tokens on atmosphere. Run the same round with progressively smaller situation blocks and find the knee in the curve. My bet: it's lower than you think.

**The one structural gap:** Nobody specified whether the save file summary (3-5 sentences) is *redundant* with the curator output. If the curator is already summarizing "what happened," the save file summary is wasted tokens. One should feed the other, not duplicate it.

Budget is architecture. Measure before you commit.
