"""Generate conversation engine design specs by consulting the beta agent panel.

Focused on HOW THE CONVERSATION WORKS -- turns, sequencing, team interaction,
phases, anti-slop. Not code, not infrastructure, not pipelines.
"""

import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ask_panel import ask_panel
from claude_runner import run_claude_async

OUTPUT_DIR = Path(__file__).parent / "design_specs_test"

SPECS = [
    {
        "id": "01",
        "filename": "01-what-is-a-turn.md",
        "title": "What Is a Turn",
        "question": """We need to define the atomic unit of conversation -- the "turn."

1. What information does an agent need to take a meaningful turn? What do they see
   and what are they asked to do?
2. Should agents produce just natural language, or should we expect some structured
   signals back (like "I'm agreeing/disagreeing", "here's a new idea", "I'm ready
   to move on")? What's the value of structured output vs the cost of enforcing it?
3. What's the difference between an internal deliberation turn (within a team) and
   a turn that's meant for the other team to see?
4. How should the "perspective reminder" work -- the thing that keeps agents in
   character across many turns? When does it show up, what does it say?
5. When an agent takes a turn, do they know how many turns have happened? Do they
   know where they are in the conversation arc? Should they?

Think about what makes a turn PRODUCTIVE -- not just what it contains but what
conditions lead to agents saying something worth reading vs filler.""",
    },
    {
        "id": "02",
        "filename": "02-who-speaks-next.md",
        "title": "Who Speaks Next",
        "question": """A team has 4-6 agents. After one finishes speaking, we need to decide
who goes next.

1. Should it be round-robin, relevance-based, random, or something else?
   What are the tradeoffs? Round-robin is predictable but boring. Relevance-based
   is smart but how do you measure relevance without an expensive extra call?
2. How does the bench work? Not every agent should speak every turn. What puts
   someone on the bench, what brings them back? Who decides -- the orchestrator
   or a background agent or the agents themselves?
3. How do we prevent a dominant agent from taking over? Hard limits? Soft nudges?
4. Devil's Advocate duty rotates -- how does this interact with who speaks next?
   Does the DA always get priority when it's their rotation?
5. Can an agent choose to stay silent? Or does the orchestrator make all
   speaking decisions? What's the "silence as signal" design?
6. Should the speaking lineup change when the phase changes? How?

Think about what makes a conversation FLOW vs what makes it feel mechanical.""",
    },
    {
        "id": "03",
        "filename": "03-how-teams-talk-to-each-other.md",
        "title": "How Teams Talk to Each Other",
        "question": """Two teams, separate context windows, communicating through a broker.
We need to define how that cross-team conversation actually works.

1. Teams deliberate internally, then send something to the other team. What triggers
   the "send"? A fixed number of internal turns? The orchestrator deciding the team
   has a position? An agent saying "let's tell them"?
2. Does one agent synthesize the team's position (spokesperson), or does the raw
   internal conversation cross the boundary? What are the tradeoffs?
3. What does the other team see? A full message? A summary? How compressed should
   cross-team communication be?
4. What happens when one team produces messages faster than the other reads them?
   Messages pile up -- do they get batched, prioritized, or does the fast team
   get throttled?
5. Can teams ask each other direct questions, or is all communication positional
   (stating views, not requesting info)?
6. How does this cross-team rhythm feel? Like exchanging letters? Like a debate?
   Like parallel tracks that periodically sync? What's the metaphor?

Think about what produces genuine cross-team tension and value vs what produces
two teams talking past each other.""",
    },
    {
        "id": "04",
        "filename": "04-phase-flow.md",
        "title": "How Phases Flow",
        "question": """The conversation moves through Brainstorm -> Refine -> Specify -> Review.
We need to define how these transitions work and what changes at each phase.

1. What makes a phase "done"? Brainstorm needs enough ideas, Refine needs ideas
   challenged, Specify needs requirements pinned down, Review needs adversarial
   validation. But how do you measure "enough" without manually counting?
2. Who decides the phase is done? Can it be automatic, or does it need evaluation?
   What if the phase is clearly done early vs what if it's dragging on?
3. When a phase transitions, what actually changes for the agents? Their instructions?
   Their tone? The bench lineup? The anti-slop rules? Walk through the concrete
   differences between how an agent behaves in Brainstorm vs Refine vs Specify.
4. Should agents know they're in a specific phase? Or should the behavioral change
   come from shifting their instructions without naming the phase?
5. Can a phase transition be reversed? What if Specify reveals we missed something
   fundamental -- can we go back to Brainstorm?
6. What happens at the phase boundary itself? Is there a summary, a reset, a
   handoff document? Or does the conversation just shift tone?

Think about natural conversation arcs -- how real brainstorming sessions shift
from wild ideas to evaluation to detail work.""",
    },
    {
        "id": "05",
        "filename": "05-anti-slop-in-practice.md",
        "title": "Anti-Slop Mechanisms in Practice",
        "question": """We have 10 anti-slop mechanisms designed. We need to figure out how they
actually work in practice during a running conversation.

1. Which mechanisms are just good instructions in the agent's prompt (agreement tax,
   perspective enforcement) vs which actually need the orchestrator to monitor and
   intervene (convergence suppression, novelty scoring)?
2. For the ones that need monitoring: what does the orchestrator look for, and what
   does it DO when it detects a problem? Inject a nudge into the next turn? Swap
   an agent? Change the prompt?
3. How do we detect consensus drift -- agents gradually agreeing more and saying
   less interesting things? What are the signals?
4. The "uncomfortable idea quota" says agents should periodically introduce
   challenging ideas. How does this work in practice? A prompt nudge every N turns?
   A special instruction to the next speaker?
5. If multiple anti-slop mechanisms want to fire at the same time, what wins?
   We can't inject 5 different nudges into one turn.
6. What's the MVP set? Which 3-4 mechanisms give us 80% of the value? What do we
   build first and what do we defer?

Think about what actually produces INTERESTING output vs what just adds complexity.
The goal isn't to check every box -- it's to keep the conversation genuinely creative.""",
    },
    {
        "id": "06",
        "filename": "06-agentmind-and-internal-state.md",
        "title": "AgentMind and Internal State",
        "question": """The design references "AgentMind" as the agent's internal state -- ideas
they hold, their conviction level, their mood. We need to decide what this is
and whether it's worth tracking.

1. What's the minimum viable AgentMind? Just the agent's config plus conversation
   history? Or do we need explicit state tracking for ideas, mood, conviction?
2. Does tracking idea "magnitude" (how strongly an agent feels about an idea) add
   real value, or does the conversation history itself capture this naturally?
   What's the argument for explicit tracking vs letting it emerge?
3. Mood -- is it useful to track and inject "you're feeling frustrated because your
   ideas keep getting shot down"? Or does this feel artificial? When would mood
   tracking actually change the conversation for the better?
4. If we track AgentMind, should the agent SEE their own state ("Your top idea is X
   with magnitude 0.8") or should it be invisible to them and only used by the
   orchestrator for decisions?
5. What persists between sessions? If the user runs a second session on the same
   idea, what should the agents "remember"?
6. Is AgentMind a v1 feature or a later addition? Could we ship without it and
   add it when we see what's missing?

Think about what internal state tracking would actually change about the conversation
vs what's just bookkeeping that doesn't affect output quality.""",
    },
]


SYNTHESIS_SYSTEM_PROMPT = """You are a requirements writer for a multi-agent conversation system.
You receive design proposals from three consultants with different perspectives.

Your job: synthesize their proposals into one clear requirements spec for how the
conversation engine should work.

Rules:
- Start with "Decisions Made" -- a numbered list of the key choices
- Where consultants agree, state the decision
- Where they disagree, pick the best approach and briefly note why
- Focus on HOW THE CONVERSATION WORKS, not code or infrastructure
- No code, no schemas, no class definitions -- describe behavior and rules
- Make choices. No hedging, no "either approach could work"
- Keep it readable -- someone should be able to understand the conversation model
  by reading this spec
- End with "Deferred" for things explicitly punted
- End with "Open Questions" for things the consultants raised that need more thought"""


async def consult_and_synthesize(spec: dict, prior_specs: list[str]) -> str:
    """Ask the panel, then synthesize into a spec."""
    spec_id = spec["id"]
    title = spec["title"]

    context = ""
    if prior_specs:
        context = "=== Decisions from prior specs (reference these, don't contradict) ===\n\n"
        for ps in prior_specs[-3:]:
            context += ps[:2000] + "\n\n...(truncated)\n\n"
        context += "=== End prior decisions ===\n"

    print(f"\n[{spec_id}] Consulting panel on: {title}", flush=True)
    start = time.time()
    responses = await ask_panel(spec["question"], timeout=420, context=context)
    panel_time = time.time() - start
    print(f"[{spec_id}] Panel responded in {panel_time:.0f}s", flush=True)

    for key, resp in responses.items():
        if "[Claude CLI timed out" in resp:
            print(f"  WARNING: {key} timed out", flush=True)

    print(f"[{spec_id}] Synthesizing spec...", flush=True)
    synth_start = time.time()

    synth_input = f"# Spec to write: {title}\n\n"
    synth_input += f"## The Question\n\n{spec['question']}\n\n"

    agent_names = {
        "cognitive_architect": "The Cognitive Architect (creativity engine designer)",
        "systems_pragmatist": "The Systems Pragmatist (infrastructure realist)",
        "product_oracle": "The Product Oracle (user advocate)",
    }

    for key, resp in responses.items():
        name = agent_names.get(key, key)
        synth_input += f"## Proposal from {name}\n\n{resp}\n\n"

    if context:
        synth_input += f"\n{context}\n"

    synth_input += "\nSynthesize into a single requirements spec. No code. Focus on behavior and rules."

    synthesis = await run_claude_async(SYNTHESIS_SYSTEM_PROMPT, synth_input, timeout=420)
    synth_time = time.time() - synth_start
    print(f"[{spec_id}] Synthesis done in {synth_time:.0f}s", flush=True)

    return synthesis


async def main():
    print("=" * 60)
    print("Conversation Engine Spec Generation")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    OUTPUT_DIR.mkdir(exist_ok=True)
    prior_specs = []
    total_start = time.time()

    for spec in SPECS:
        spec_start = time.time()
        synthesis = await consult_and_synthesize(spec, prior_specs)

        output_path = OUTPUT_DIR / spec["filename"]
        header = (
            f"# {spec['title']}\n\n"
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
            f"Spec ID: {spec['id']}*\n\n"
        )
        output_path.write_text(header + synthesis, encoding="utf-8")

        spec_time = time.time() - spec_start
        lines = len(synthesis.split("\n"))
        print(f"[{spec['id']}] Wrote {spec['filename']} ({lines} lines, {spec_time:.0f}s)\n",
              flush=True)

        prior_specs.append(f"# {spec['title']}\n\n{synthesis[:3000]}")

    total_time = time.time() - total_start
    print("=" * 60)
    print(f"All specs generated in {total_time:.0f}s ({total_time/60:.1f} min)")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)

    index_path = OUTPUT_DIR / "index.md"
    index_lines = [
        "# Conversation Engine Design Specs (Test Run)",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Total generation time: {total_time/60:.1f} minutes",
        "",
        "Specs generated by consulting three beta agents on each topic,",
        "then synthesizing their proposals into requirements.",
        "",
        "## Specs",
        "",
    ]
    for spec in SPECS:
        index_lines.append(f"- [{spec['id']}. {spec['title']}]({spec['filename']})")
    index_path.write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Index written to: {index_path}")


if __name__ == "__main__":
    asyncio.run(main())
