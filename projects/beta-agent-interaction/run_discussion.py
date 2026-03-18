"""Facilitated multi-round agent discussion on open questions from a brief.

For each question, runs 3 structured rounds mapped to agent job types:
  Round 1 - Proposals:   cognitive_architect + flow_orchestrator (job: propose)
  Round 2 - Critiques:   systems_pragmatist + adversarial_critic (job: critique)
  Round 3 - Evaluations: product_oracle + context_surgeon (job: evaluate)
Then a neutral moderator synthesizes into a design doc.

Prior design docs chain forward as context for subsequent questions.
"""

import argparse
import asyncio
import re
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from interact import load_team
from prompt_builder import build_system_prompt, build_perspective_reminder, build_context_lens, filter_prior_rounds
from claude_runner import run_claude_async

TEAM_CONFIG = Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"

AGENT_GROUPS = {
    "propose": ["cognitive_architect", "flow_orchestrator"],
    "critique": ["systems_pragmatist", "adversarial_critic"],
    "evaluate": ["product_oracle", "context_surgeon"],
}

ROUND_LABELS = ["propose", "critique", "evaluate"]

COUNTER_PROPOSE_INSTRUCTION = (
    "Another designer has already proposed a solution (shown in the discussion so far). "
    "Your job: propose a DIFFERENT approach. Do not refine or agree with their proposal. "
    "Find a fundamentally different way to solve the same problem. If you cannot find one, "
    "explain why only one approach works -- but try hard to find an alternative first."
)

# -- Per-agent role overlays --
# Injected into the propose round to give each proposer a distinct mindset.
# These layer ON TOP of the agent's existing personality/voice/technique.
# The agent stays in character but approaches the problem through this lens.

PROPOSE_ROLES = {
    # Competitive: wants to WIN. Treats the proposal as a pitch.
    "competitive": (
        "You are trying to come up with the single BEST answer to this question. "
        "Not a survey of options -- your ONE best idea. You are competing against "
        "another designer who is answering the same question. You want YOUR design "
        "to be the one that survives critique. Be bold. Commit fully."
    ),
    # Minimalist: wants the smallest thing that works. Allergic to complexity.
    "minimalist": (
        "You are a minimalist. You believe the best design is the one with the fewest "
        "moving parts. You are not shy about cutting things other people think are "
        "important. If something can be deferred, defer it. If something can be removed, "
        "remove it. Your proposal should be the smallest possible version that actually "
        "answers the question. Complexity is a cost -- justify every piece."
    ),
    # Maximalist: wants the most capable version. Thinks big.
    "maximalist": (
        "You think big. You want the version of this that unlocks the most capability "
        "and handles the most edge cases. You are not afraid of complexity if it serves "
        "a purpose. Where others want to defer, you want to solve it now. Design for "
        "the full problem, not the easy subset."
    ),
    # Contrarian: instinctively suspicious of the obvious answer.
    "contrarian": (
        "You are suspicious of whatever answer seems obvious. If everyone would "
        "naturally gravitate toward approach X, you want to seriously consider "
        "approach Y. Not for the sake of being different -- but because obvious "
        "answers often have hidden assumptions nobody examines. Find the road not taken "
        "and argue for it honestly."
    ),
    # Operator: thinks about what it's like to RUN this, not build it.
    "operator": (
        "You think like someone who has to operate this system at 3 AM when it breaks. "
        "Your proposal optimizes for debuggability, observability, and recoverability. "
        "You don't care if the design is elegant -- you care if you can figure out what "
        "went wrong from the logs. Every mechanism you propose should be inspectable."
    ),
    # User-first: works backward from what the human experiences.
    "user_first": (
        "You work backward from what the human user experiences. Start with: what does "
        "the user see in the Morning Brief because of this design choice? If this "
        "mechanism works perfectly, what changes for the user? If it fails silently, "
        "does the user notice? Design from the outside in."
    ),
}

AGENT_DISPLAY_NAMES = {
    "cognitive_architect": "The Cognitive Architect (creativity engine designer)",
    "flow_orchestrator": "The Flow Orchestrator (mechanical flow designer)",
    "systems_pragmatist": "The Systems Pragmatist (infrastructure realist)",
    "adversarial_critic": "The Adversarial Critic (adversarial reviewer)",
    "product_oracle": "The Product Oracle (user advocate)",
    "context_surgeon": "The Context Surgeon (context efficiency evaluator)",
    "idea_merchant": "The Idea Merchant (idea generator)",
}

SYNTHESIS_SYSTEM_PROMPT = """You are a requirements writer synthesizing a structured design discussion.

You received:
- PROPOSALS from two designers with different perspectives
- CRITIQUES from two reviewers who found problems, assumptions, and gaps
- EVALUATIONS from two evaluators who judged feasibility and user impact

Your job: produce one clear design doc.

Rules:
- Start with "## Decisions" -- numbered list of concrete choices
- Where proposals survived critique, state the decision
- Where critiques killed a proposal, explain why and what replaces it
- Where evaluators flagged concerns, note mitigation or deferral
- No code, no schemas -- describe behavior and rules
- Make choices. No hedging, no "either approach could work"
- Keep it readable -- someone should understand the design by reading this doc
- End with "## Deferred" for things explicitly punted
- End with "## Open Questions" for things that need more thought

CRITICAL: Output ONLY the design doc text. Do NOT request file permissions, describe
what you would write, summarize what the doc covers, or wrap the content in meta-
commentary. Start directly with "## Decisions" and write the full document. Your
entire response IS the design doc.

ADDITIONAL REQUIREMENT: After all other sections, add a final section exactly like this:

## Ledger

### Q{N}: {short topic tag, 2-4 words}
- DECIDED: {terse constraint, max 50 words, stated as a rule not rationale}
- DECIDED: {another constraint}
- OPEN: {unresolved question if any}

List EVERY concrete decision from the Decisions section as a one-line DECIDED entry.
List every unresolved item from Open Questions as an OPEN entry.
Keep each entry under 50 words. State constraints, not rationale."""


# -- Experiment modes --
# Each mode defines which agents participate in each round and how round 2 works.
# "counter" mode: 2nd proposer sees 1st proposal and must propose an ALTERNATIVE.
# "lean" mode: 4 agents only (drop weakest proposer + weakest evaluator).
# "default" mode: original 6-agent 3-round structure.

EXPERIMENT_MODES = {
    "default": {
        "description": "Original 6-agent, 3-round structure (no role overlays)",
        "groups": {
            "propose": ["cognitive_architect", "flow_orchestrator"],
            "critique": ["systems_pragmatist", "adversarial_critic"],
            "evaluate": ["product_oracle", "context_surgeon"],
        },
        "agent_roles": {},
    },
    "counter": {
        "description": "1st proposer solo, 2nd proposer sees 1st and must counter-propose",
        "groups": {
            "propose": ["cognitive_architect"],
            "counter": ["flow_orchestrator"],
            "critique": ["systems_pragmatist", "adversarial_critic"],
            "evaluate": ["product_oracle", "context_surgeon"],
        },
        "agent_roles": {},
    },
    "lean": {
        "description": "4 agents: drop Cognitive Architect + Product Oracle",
        "groups": {
            "propose": ["flow_orchestrator"],
            "critique": ["systems_pragmatist", "adversarial_critic"],
            "evaluate": ["context_surgeon"],
        },
        "agent_roles": {},
    },
    # -- Role overlay experiments --
    "compete": {
        "description": "Competitive vs Minimalist proposers",
        "groups": {
            "propose": ["cognitive_architect", "flow_orchestrator"],
            "critique": ["systems_pragmatist", "adversarial_critic"],
            "evaluate": ["product_oracle", "context_surgeon"],
        },
        "agent_roles": {
            "cognitive_architect": "competitive",
            "flow_orchestrator": "minimalist",
        },
    },
    "bigsmall": {
        "description": "Maximalist vs Minimalist proposers",
        "groups": {
            "propose": ["cognitive_architect", "flow_orchestrator"],
            "critique": ["systems_pragmatist", "adversarial_critic"],
            "evaluate": ["product_oracle", "context_surgeon"],
        },
        "agent_roles": {
            "cognitive_architect": "maximalist",
            "flow_orchestrator": "minimalist",
        },
    },
    "angles": {
        "description": "Contrarian vs Operator proposers, User-first evaluator",
        "groups": {
            "propose": ["cognitive_architect", "flow_orchestrator"],
            "critique": ["systems_pragmatist", "adversarial_critic"],
            "evaluate": ["product_oracle", "context_surgeon"],
        },
        "agent_roles": {
            "cognitive_architect": "contrarian",
            "flow_orchestrator": "operator",
            "product_oracle": "user_first",
        },
    },
    "ideas": {
        "description": "Idea Merchant generates, Architect refines, critics + evaluators as normal",
        "groups": {
            "propose": ["idea_merchant", "cognitive_architect"],
            "critique": ["systems_pragmatist", "adversarial_critic"],
            "evaluate": ["product_oracle", "context_surgeon"],
        },
        "agent_roles": {},
    },
    "ideas_compete": {
        "description": "Idea Merchant (wild) vs Flow Orchestrator (minimalist), then critiqued and evaluated",
        "groups": {
            "propose": ["idea_merchant", "flow_orchestrator"],
            "critique": ["systems_pragmatist", "adversarial_critic"],
            "evaluate": ["product_oracle", "context_surgeon"],
        },
        "agent_roles": {
            "flow_orchestrator": "minimalist",
        },
    },
}


def parse_brief(path: Path) -> tuple[str, list[dict]]:
    """Parse a discussion brief markdown file.

    Returns:
        (decisions_text, questions_list)
        where questions_list is [{"number": int, "title": str, "body": str}, ...]
    """
    text = path.read_text(encoding="utf-8")

    # Extract "What's Already Decided" section
    decisions_match = re.search(
        r"## What's Already Decided\s*\n(.*?)(?=\n## |\Z)",
        text,
        re.DOTALL,
    )
    decisions = decisions_match.group(1).strip() if decisions_match else ""

    # Extract "Open Questions" section
    questions_match = re.search(
        r"## Open Questions[^\n]*\n(.*?)(?=\n## |\Z)",
        text,
        re.DOTALL,
    )
    if not questions_match:
        print("ERROR: No 'Open Questions' section found in brief.", flush=True)
        sys.exit(1)

    questions_text = questions_match.group(1).strip()

    # Parse numbered questions: "1. **Title** Body text"
    pattern = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*?)(?=^\d+\.\s+\*\*|\Z)", re.MULTILINE | re.DOTALL)
    questions = []
    for m in pattern.finditer(questions_text):
        questions.append({
            "number": int(m.group(1)),
            "title": m.group(2).strip(),
            "body": m.group(3).strip(),
        })

    if not questions:
        print("ERROR: No questions parsed from brief.", flush=True)
        sys.exit(1)

    return decisions, questions


def slugify(title: str) -> str:
    """Convert a title to a filename-safe slug."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug[:60]


def compute_speaking_order(agents: list[str], team) -> list[str]:
    """Order agents by assertiveness * position intensity, with randomness.

    Higher assertiveness + intensity = speaks earlier.
    Small random factor prevents deterministic ordering.
    """
    import random

    scored = []
    for key in agents:
        agent = team.agents[key]
        p = agent.personality
        # Speaking priority: assertiveness * intensity, weighted by stubbornness
        score = (p.assertiveness * 0.5 + agent.position.intensity * 0.3 + p.stubbornness * 0.2)
        # Add small random jitter (+-0.1) so it's not perfectly deterministic
        score += random.uniform(-0.1, 0.1)
        scored.append((key, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [key for key, _ in scored]


def _build_agent_payload(
    agent_key: str,
    team,
    system_prompts: dict,
    question: dict,
    decisions: str,
    prior_rounds: str,
    prior_specs: str,
    open_questions: str,
    round_instruction: str,
    agent_roles: dict[str, str] | None,
    this_round_so_far: str = "",
) -> str:
    """Build the prompt payload for one agent."""
    agent = team.agents[agent_key]
    reminder = build_perspective_reminder(agent)

    payload = f"{reminder}\n\n"

    # Agent-specific context lens
    context_lens = build_context_lens(agent)
    if context_lens:
        payload += f"{context_lens}\n\n"

    # Per-agent role overlay
    if agent_roles and agent_key in agent_roles:
        role_key = agent_roles[agent_key]
        role_text = PROPOSE_ROLES.get(role_key, "")
        if role_text:
            payload += f"=== Your Approach ===\n{role_text}\n=== End Approach ===\n\n"

    if decisions:
        payload += f"=== What's Already Decided ===\n{decisions}\n=== End Decisions ===\n\n"

    if prior_specs:
        payload += f"=== Prior Design Docs (reference, don't contradict) ===\n{prior_specs}\n=== End Prior Docs ===\n\n"

    if open_questions:
        payload += f"=== Unresolved Open Questions from Prior Docs ===\n{open_questions}\n=== End Open Questions ===\n\nIf this question can resolve any of the above, do so.\n\n"

    # Context: prior rounds + what's been said THIS round so far
    agent_prior_rounds = filter_prior_rounds(prior_rounds, agent)
    combined_context = ""
    if agent_prior_rounds:
        combined_context += agent_prior_rounds
    if this_round_so_far:
        combined_context += f"\n\n--- This round so far ---\n{this_round_so_far}"
    if combined_context:
        payload += f"=== Discussion So Far (this question) ===\n{combined_context}\n=== End Discussion ===\n\n"

    payload += f"## Question: {question['title']}\n\n{question['body']}\n\n"

    if round_instruction:
        payload += f"{round_instruction}\n\n"

    if this_round_so_far:
        payload += "Other agents have already spoken this round. Respond to their points directly. Agree, disagree, or build on what they said. 250 words max."
    else:
        payload += "You are speaking first this round. Set the agenda. 250 words max."

    return payload


async def run_round(
    agents: list[str],
    system_prompts: dict[str, str],
    team,
    question: dict,
    decisions: str,
    prior_rounds: str,
    prior_specs: str,
    open_questions: str,
    timeout: int,
    round_instruction: str = "",
    agent_roles: dict[str, str] = None,
    sequential: bool = True,
    on_agent_start=None,
    on_agent_done=None,
) -> dict[str, str]:
    """Run one round. Sequential by default: each agent sees prior speakers.

    Callbacks on_agent_start(agent_key) and on_agent_done(agent_key, response, elapsed)
    are called for live UI updates.
    """
    if not sequential:
        # Parallel mode (legacy) -- all agents fire at once
        async def ask_parallel(agent_key):
            payload = _build_agent_payload(
                agent_key, team, system_prompts, question, decisions,
                prior_rounds, prior_specs, open_questions, round_instruction,
                agent_roles,
            )
            response = await run_claude_async(system_prompts[agent_key], payload, timeout=timeout)
            return agent_key, response

        tasks = [ask_parallel(key) for key in agents]
        results = await asyncio.gather(*tasks)
        return {key: resp for key, resp in results}

    # Sequential mode: agents speak one at a time, each seeing previous speakers
    ordered = compute_speaking_order(agents, team)
    responses = {}
    this_round_so_far = ""

    for agent_key in ordered:
        if on_agent_start:
            on_agent_start(agent_key)

        start = time.time()
        payload = _build_agent_payload(
            agent_key, team, system_prompts, question, decisions,
            prior_rounds, prior_specs, open_questions, round_instruction,
            agent_roles, this_round_so_far,
        )
        response = await run_claude_async(system_prompts[agent_key], payload, timeout=timeout)
        elapsed = time.time() - start

        responses[agent_key] = response

        if on_agent_done:
            on_agent_done(agent_key, response, elapsed)

        # Add this agent's response to the running context for the next speaker
        name = AGENT_DISPLAY_NAMES.get(agent_key, agent_key)
        this_round_so_far += f"[{name}]\n{response}\n\n"

    return responses


async def synthesize(
    question: dict,
    round_responses: dict[str, dict[str, str]],
    round_labels: list[str],
    decisions: str,
    prior_specs: str,
    open_questions: str,
    timeout: int,
) -> str:
    """Moderator call: merge rounds into a design doc."""
    synth_input = f"# Design Question: {question['title']}\n\n"
    synth_input += f"## The Question\n\n{question['body']}\n\n"

    if decisions:
        synth_input += f"## Prior Decisions (from brief)\n\n{decisions}\n\n"

    if prior_specs:
        synth_input += f"## Prior Design Docs\n\n{prior_specs}\n\n"

    if open_questions:
        synth_input += f"## Unresolved Open Questions from Prior Docs\n\nResolve any of these that this discussion addresses:\n\n{open_questions}\n\n"

    for round_name in round_labels:
        responses = round_responses[round_name]
        label = round_name.upper()
        if label == "COUNTER":
            label = "COUNTER-PROPOSAL"
        synth_input += f"## Round: {label}\n\n"
        for agent_key, response in responses.items():
            name = AGENT_DISPLAY_NAMES.get(agent_key, agent_key)
            synth_input += f"### {name}\n\n{response}\n\n"

    synth_input += (
        "Synthesize into a single design doc. No code. Focus on behavior and rules.\n\n"
        "IMPORTANT: Output ONLY the design doc. Start with '## Decisions'. "
        "Do not request file permissions, describe what you would write, or add any "
        "meta-commentary before or after the document."
    )

    return await run_claude_async(SYNTHESIS_SYSTEM_PROMPT, synth_input, timeout=timeout)


def format_transcript(question: dict, round_responses: dict[str, dict[str, str]]) -> str:
    """Format the full transcript for a question."""
    lines = [
        f"# Transcript: {question['title']}",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
    ]

    for round_name, responses in round_responses.items():
        label = "COUNTER-PROPOSAL" if round_name == "counter" else round_name.upper()
        lines.append(f"## Round: {label}")
        lines.append("")
        for agent_key, response in responses.items():
            name = AGENT_DISPLAY_NAMES.get(agent_key, agent_key)
            lines.append(f"### {name}")
            lines.append("")
            lines.append(response)
            lines.append("")

    return "\n".join(lines)


def extract_open_questions(design_doc: str) -> list[str]:
    """Extract open questions from a design doc's ## Open Questions section."""
    match = re.search(r"## Open Questions\s*\n(.*?)(?=\n## |\Z)", design_doc, re.DOTALL)
    if not match:
        return []
    text = match.group(1).strip()
    # Extract bullet/numbered items
    items = re.findall(r"^[\s]*[-*\d.]+\s+(.+)", text, re.MULTILINE)
    return items


async def run_question(
    question: dict,
    team,
    system_prompts: dict[str, str],
    decisions: str,
    prior_specs: str,
    open_questions: str,
    timeout: int,
    mode: dict = None,
) -> tuple[str, str]:
    """Run the full discussion + synthesis for one question.

    Returns (design_doc, transcript).
    """
    if mode is None:
        mode = EXPERIMENT_MODES["default"]

    q_num = question["number"]
    groups = mode["groups"]
    round_labels = list(groups.keys())

    agent_roles = mode.get("agent_roles", {})
    round_responses = {}
    accumulated_discussion = ""

    for round_name in round_labels:
        agents = groups[round_name]
        agent_names = ", ".join(AGENT_DISPLAY_NAMES.get(a, a) for a in agents)
        display_name = "counter-propose" if round_name == "counter" else round_name

        # Show role overlays if any
        role_info = ""
        for a in agents:
            if a in agent_roles:
                role_info += f" [{a}: {agent_roles[a]}]"
        print(f"  [{q_num}] Round {display_name}: {agent_names}{role_info}", flush=True)

        round_inst = ""
        if round_name == "counter":
            round_inst = COUNTER_PROPOSE_INSTRUCTION

        start = time.time()
        responses = await run_round(
            agents=agents,
            system_prompts=system_prompts,
            team=team,
            question=question,
            decisions=decisions,
            prior_rounds=accumulated_discussion,
            prior_specs=prior_specs,
            open_questions=open_questions,
            timeout=timeout,
            round_instruction=round_inst,
            agent_roles=agent_roles if round_name in ("propose", "counter") else None,
        )
        elapsed = time.time() - start

        round_responses[round_name] = responses

        # Check for timeouts
        for key, resp in responses.items():
            if "[Claude CLI timed out" in resp or "[Error" in resp:
                print(f"    WARNING: {key}: {resp[:80]}", flush=True)

        # Accumulate discussion for next round's context
        for key, resp in responses.items():
            name = AGENT_DISPLAY_NAMES.get(key, key)
            label = "COUNTER-PROPOSAL" if round_name == "counter" else round_name.upper()
            accumulated_discussion += f"[{label} - {name}]\n{resp}\n\n"

        print(f"    Done in {elapsed:.0f}s", flush=True)

    # Synthesis
    print(f"  [{q_num}] Synthesizing design doc...", flush=True)
    start = time.time()
    design_doc = await synthesize(
        question, round_responses, round_labels, decisions,
        prior_specs, open_questions, timeout,
    )
    elapsed = time.time() - start
    print(f"    Synthesis done in {elapsed:.0f}s", flush=True)

    transcript = format_transcript(question, round_responses)
    return design_doc, transcript


async def main():
    parser = argparse.ArgumentParser(
        description="Run structured multi-round agent discussions on brief questions.",
    )
    parser.add_argument("brief", help="Path to the discussion brief markdown file")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory (default: ../../proposed_design_docs relative to script)",
    )
    parser.add_argument(
        "--questions",
        default=None,
        help="Comma-separated question numbers to run (e.g. 1,3,5). Default: all.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=420,
        help="Timeout in seconds per LLM call (default: 420)",
    )
    parser.add_argument(
        "--mode",
        choices=list(EXPERIMENT_MODES.keys()),
        default="default",
        help="Experiment mode: default (6 agents), counter (2nd proposer must counter-propose), lean (4 agents)",
    )

    args = parser.parse_args()

    # Resolve paths
    brief_path = Path(args.brief)
    if not brief_path.is_absolute():
        brief_path = Path.cwd() / brief_path
    if not brief_path.exists():
        print(f"ERROR: Brief not found: {brief_path}")
        sys.exit(1)

    if args.output_dir:
        output_dir = Path(args.output_dir)
        if not output_dir.is_absolute():
            output_dir = Path.cwd() / output_dir
    else:
        output_dir = Path(__file__).resolve().parent.parent.parent / "proposed_design_docs"

    # Parse brief
    decisions, all_questions = parse_brief(brief_path)
    print(f"Parsed brief: {len(all_questions)} questions, {len(decisions)} chars of prior decisions")

    # Filter questions if requested
    if args.questions:
        selected = {int(n.strip()) for n in args.questions.split(",")}
        questions = [q for q in all_questions if q["number"] in selected]
        if not questions:
            print(f"ERROR: No matching questions for --questions {args.questions}")
            sys.exit(1)
    else:
        questions = all_questions

    # Load team and build system prompts
    mode = EXPERIMENT_MODES[args.mode]
    team = load_team(str(TEAM_CONFIG))
    system_prompts = {key: build_system_prompt(agent) for key, agent in team.agents.items()}

    # Figure out which agents this mode uses
    mode_agents = set()
    for agents in mode["groups"].values():
        mode_agents.update(agents)

    print("=" * 60)
    print("Facilitated Agent Discussion")
    print(f"Brief: {brief_path.name}")
    print(f"Mode: {args.mode} -- {mode['description']}")
    print(f"Agents: {', '.join(sorted(mode_agents))}")
    print(f"Rounds: {' -> '.join(mode['groups'].keys())}")
    print(f"Questions: {', '.join(str(q['number']) for q in questions)}")
    print(f"Output: {output_dir}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Timeout per call: {args.timeout}s")
    print("=" * 60)

    output_dir.mkdir(parents=True, exist_ok=True)
    prior_specs = ""
    accumulated_open_questions = []
    results = []
    total_start = time.time()

    for question in questions:
        q_num = question["number"]
        q_title = question["title"]
        slug = slugify(q_title)
        filename = f"{q_num:02d}-{slug}"

        print(f"\n[{q_num}/{len(all_questions)}] {q_title}", flush=True)
        q_start = time.time()

        # Format accumulated open questions for context
        oq_text = ""
        if accumulated_open_questions:
            oq_lines = [f"- [from Q{oq['from_q']}] {oq['text']}" for oq in accumulated_open_questions]
            oq_text = "\n".join(oq_lines)

        design_doc, transcript = await run_question(
            question=question,
            team=team,
            system_prompts=system_prompts,
            decisions=decisions,
            prior_specs=prior_specs[-6000:] if prior_specs else "",
            open_questions=oq_text,
            timeout=args.timeout,
            mode=mode,
        )

        q_elapsed = time.time() - q_start

        # Extract open questions from this doc and accumulate
        new_oqs = extract_open_questions(design_doc)
        for oq in new_oqs:
            accumulated_open_questions.append({"from_q": q_num, "text": oq})

        # Write design doc
        doc_path = output_dir / f"{filename}.md"
        header = (
            f"# {q_title}\n\n"
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
            f"Question {q_num} | {q_elapsed:.0f}s | Mode: {args.mode}*\n\n"
        )
        doc_path.write_text(header + design_doc, encoding="utf-8")

        # Write transcript
        transcript_path = output_dir / f"{filename}-transcript.md"
        transcript_path.write_text(transcript, encoding="utf-8")

        doc_lines = len(design_doc.split("\n"))
        print(f"  Wrote {filename}.md ({doc_lines} lines) + transcript ({q_elapsed:.0f}s total)",
              flush=True)

        # Chain forward: add this design doc as context for next questions
        prior_specs += f"\n\n# {q_title}\n\n{design_doc[:3000]}"
        results.append({"number": q_num, "title": q_title, "filename": filename})

    # Write index
    total_time = time.time() - total_start
    index_lines = [
        "# Proposed Design Docs",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Brief: {brief_path.name}",
        f"Mode: {args.mode} -- {mode['description']}",
        f"Total generation time: {total_time/60:.1f} minutes",
        "",
        "## Round Structure",
        "",
    ]
    for round_name, agents in mode["groups"].items():
        agent_names = ", ".join(AGENT_DISPLAY_NAMES.get(a, a.replace("_", " ").title()) for a in agents)
        index_lines.append(f"- **{round_name.title()}**: {agent_names}")
    index_lines.append("")

    index_lines.append("## Design Docs")
    index_lines.append("")
    for r in results:
        index_lines.append(f"- [{r['number']:02d}. {r['title']}]({r['filename']}.md) "
                           f"([transcript]({r['filename']}-transcript.md))")

    # Open questions summary
    if accumulated_open_questions:
        index_lines.append("")
        index_lines.append("## Accumulated Open Questions")
        index_lines.append("")
        for oq in accumulated_open_questions:
            index_lines.append(f"- [Q{oq['from_q']}] {oq['text']}")

    index_path = output_dir / "index.md"
    index_path.write_text("\n".join(index_lines), encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"Done. {len(results)} design docs in {total_time/60:.1f} minutes")
    print(f"Open questions accumulated: {len(accumulated_open_questions)}")
    print(f"Output: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
