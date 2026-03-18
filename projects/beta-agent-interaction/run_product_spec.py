"""Product Spec Pipeline -- chains conversations across two teams to produce a structured spec.

Runs the same questions through two different teams (e.g. software architects + normal people),
synthesizes each independently, then compares and merges into a product spec.

Usage:
    python run_product_spec.py "What's the product?" --questions questions.txt
    python run_product_spec.py "What's the product?" --team-a config/teams/beta-agents.yaml --team-b config/teams/normal-people.yaml
"""

import argparse
import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from claude_runner import run_claude_async
from interact import load_team
from live_synthesizer import LiveSynthesizer
from live_conversation import run_conversation, _build_agent_colors
from run_discussion import TEAM_CONFIG


SPEC_TEMPLATE_PROMPT = """You are a product specification writer. You have two synthesis documents
from two independent team discussions on the same product, plus a comparison analysis.

Produce a clean, actionable Product Spec document with these sections:

# Product Spec: [Product Name]

## Problem Statement
What problem does this product solve? For whom? Be specific.

## Target User
Who is the primary user? What's their context? (Use insights from both teams.)

## Core Value Proposition
The one sentence that explains why someone pays for this.

## MVP Feature Set
Prioritized list of features for v1. Each feature gets:
- **Name**: short label
- **What it does**: one line
- **Why it matters**: what user need it addresses
- **Confidence**: high/medium/low (based on how many agents from both teams supported it)

## Features Deferred
Ideas that came up but should NOT be in v1. Say why.

## Business Model
Pricing, target price point, acquisition strategy. Ground in what both teams said.

## Key Risks
What could kill this product? What assumptions are we making?

## Open Decisions
Decisions the human still needs to make. List each with the options and tradeoffs.

## Appendix: Team Perspectives
Brief summary of where the two teams agreed and diverged.

Write for a solo builder who needs to start building tomorrow. No fluff. Every line actionable."""


async def run_spec_pipeline(
    questions: list[str],
    team_a_config: str,
    team_b_config: str,
    max_turns: int = 15,
    turns_per_topic: int = 0,
    timeout: int = 60,
    model: str = None,
):
    """Run the full product spec pipeline."""

    output_dir = Path(__file__).resolve().parent.parent.parent / "sessions" / "specs"
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M")

    team_a = load_team(team_a_config)
    team_b = load_team(team_b_config)
    team_a_name = Path(team_a_config).stem.replace("-", " ").replace("_", " ").title()
    team_b_name = Path(team_b_config).stem.replace("-", " ").replace("_", " ").title()

    agent_keys_a = list(team_a.agents.keys())
    agent_keys_b = list(team_b.agents.keys())

    print(f"\n{'='*60}")
    print(f"  Product Spec Pipeline")
    print(f"  Team A: {team_a_name} ({len(agent_keys_a)} agents)")
    print(f"  Team B: {team_b_name} ({len(agent_keys_b)} agents)")
    print(f"  Questions: {len(questions)}")
    print(f"  Max turns: {max_turns}")
    print(f"{'='*60}\n")

    # Phase 1: Run Team A
    print(f"[Phase 1] Running {team_a_name}...")
    start = time.time()
    result_a = await run_conversation(
        questions=questions,
        agent_keys=agent_keys_a,
        max_turns=max_turns,
        timeout=timeout,
        model=model,
        team_config=team_a_config,
        turns_per_topic=turns_per_topic,
        synthesize=True,
    )
    elapsed_a = time.time() - start
    print(f"  Done in {elapsed_a/60:.1f}m | {len(result_a['history'])} messages")

    # Save Team A results
    (output_dir / f"{ts}_team_a_synthesis.md").write_text(
        f"# {team_a_name} Synthesis\n\n{result_a['synthesis']}", encoding="utf-8"
    )

    # Phase 2: Run Team B
    print(f"\n[Phase 2] Running {team_b_name}...")
    start = time.time()
    result_b = await run_conversation(
        questions=questions,
        agent_keys=agent_keys_b,
        max_turns=max_turns,
        timeout=timeout,
        model=model,
        team_config=team_b_config,
        turns_per_topic=turns_per_topic,
        synthesize=True,
    )
    elapsed_b = time.time() - start
    print(f"  Done in {elapsed_b/60:.1f}m | {len(result_b['history'])} messages")

    # Save Team B results
    (output_dir / f"{ts}_team_b_synthesis.md").write_text(
        f"# {team_b_name} Synthesis\n\n{result_b['synthesis']}", encoding="utf-8"
    )

    # Phase 3: Compare teams
    print(f"\n[Phase 3] Comparing team outputs...")
    synth = LiveSynthesizer(questions[0])
    comparison = await synth.comparison_synthesis(
        result_a["synthesis"], result_b["synthesis"],
        team_a_name, team_b_name,
        model=model or "sonnet",
    )
    (output_dir / f"{ts}_comparison.md").write_text(
        f"# Team Comparison\n\n{comparison}", encoding="utf-8"
    )
    print(f"  Comparison complete")

    # Phase 4: Generate product spec
    print(f"\n[Phase 4] Generating product spec...")
    spec_input = f"""# Team A ({team_a_name}) Synthesis
{result_a['synthesis']}

# Team B ({team_b_name}) Synthesis
{result_b['synthesis']}

# Comparison Analysis
{comparison}

# Original Questions
{chr(10).join(f'{i+1}. {q}' for i, q in enumerate(questions))}"""

    spec = await run_claude_async(SPEC_TEMPLATE_PROMPT, spec_input, timeout=120, model=model or "sonnet")

    spec_path = output_dir / f"{ts}_product_spec.md"
    spec_path.write_text(spec, encoding="utf-8")
    print(f"  Spec saved: {spec_path}")

    # Save all snapshots for debugging
    snapshots_path = output_dir / f"{ts}_snapshots.json"
    snapshots_path.write_text(json.dumps({
        "team_a": {"name": team_a_name, "snapshots": result_a["snapshots"]},
        "team_b": {"name": team_b_name, "snapshots": result_b["snapshots"]},
    }, indent=2), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  Pipeline complete!")
    print(f"  Output: {output_dir}")
    print(f"  Files:")
    print(f"    {ts}_team_a_synthesis.md")
    print(f"    {ts}_team_b_synthesis.md")
    print(f"    {ts}_comparison.md")
    print(f"    {ts}_product_spec.md")
    print(f"    {ts}_snapshots.json")
    print(f"{'='*60}\n")

    return spec


def main():
    parser = argparse.ArgumentParser(description="Product Spec Pipeline")
    parser.add_argument("question", help="The main product question")
    parser.add_argument("--questions", default=None,
                        help="Path to file with one question per line (overrides positional)")
    parser.add_argument("--team-a", default=str(TEAM_CONFIG),
                        help="Team A config (default: beta-agents.yaml)")
    parser.add_argument("--team-b", default=str(Path(__file__).parent / "config" / "teams" / "normal-people.yaml"),
                        help="Team B config (default: normal-people.yaml)")
    parser.add_argument("--turns", type=int, default=15,
                        help="Max turns per team (default: 15)")
    parser.add_argument("--turns-per-topic", type=int, default=0,
                        help="Max turns per topic (default: auto)")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--model", default=None)

    args = parser.parse_args()

    if args.questions:
        q_path = Path(args.questions)
        questions = [line.strip() for line in q_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        questions = [args.question]

    asyncio.run(run_spec_pipeline(
        questions=questions,
        team_a_config=args.team_a,
        team_b_config=args.team_b,
        max_turns=args.turns,
        turns_per_topic=args.turns_per_topic,
        timeout=args.timeout,
        model=args.model,
    ))


if __name__ == "__main__":
    main()
