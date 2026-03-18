"""Bridge bmad-brainstorming output to beta-agent panel analysis.

Workflow:
  1. Takes a brainstorm session file (from /bmad-brainstorming) or a topic string
  2. Sends it to all 3 beta agents in parallel for analysis
  3. Synthesizes their responses into a requirements spec
  4. Saves everything to output/

Usage:
    # Analyze an existing brainstorm session file
    python brainstorm_to_panel.py path/to/brainstorm-session.md

    # Analyze with a specific question/focus
    python brainstorm_to_panel.py path/to/session.md --focus "Which ideas are viable for a solo builder?"

    # Quick mode: just a topic, no brainstorm file (panel discusses raw)
    python brainstorm_to_panel.py --topic "A time tracker for freelancers"

    # Debate mode: agents argue positions instead of parallel panel
    python brainstorm_to_panel.py path/to/session.md --mode debate

    # Skip synthesis (just get raw agent responses)
    python brainstorm_to_panel.py path/to/session.md --no-synthesis
"""

import argparse
import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ask_panel import ask_panel, _ensure_loaded, _team, _system_prompts
from claude_runner import run_claude_async, run_claude_sync
from multi_agent import run_debate, run_round_robin
from interact import load_team
from prompt_builder import build_system_prompt


SYNTHESIS_PROMPT = """You are synthesizing three expert perspectives on brainstormed ideas
into a single actionable requirements document.

Rules:
- Start with "Key Decisions" -- numbered list of choices made
- Where experts agree, state the decision confidently
- Where they disagree, pick the strongest position and note why
- Include a "Top Ideas" section ranking the most promising ideas with rationale
- Include a "Kill List" of ideas that should be dropped and why
- Include "Open Questions" that need more exploration
- Include "Next Steps" with concrete actions
- No code. Focus on WHAT to build and WHY.
- Be direct. Make choices. No hedging."""


def load_brainstorm_file(path: str) -> str:
    """Read a brainstorm session file and return its content."""
    p = Path(path)
    if not p.exists():
        print(f"File not found: {path}")
        sys.exit(1)
    content = p.read_text(encoding="utf-8")
    # Truncate if massive (keep first 8000 chars to fit in context)
    if len(content) > 8000:
        content = content[:8000] + "\n\n...(truncated for context efficiency)"
    return content


def build_analysis_prompt(brainstorm_content: str, focus: str = "") -> str:
    """Build the prompt that goes to the panel."""
    parts = [
        "## Brainstorm Session Output\n",
        "The following is output from a brainstorming session. Analyze it from your "
        "perspective.\n",
        "```",
        brainstorm_content,
        "```\n",
    ]

    if focus:
        parts.append(f"## Specific Focus\n\n{focus}\n")

    parts.append(
        "## Your Task\n\n"
        "From YOUR perspective and role:\n"
        "1. Which ideas have the most potential? Why?\n"
        "2. Which ideas should be killed? Why?\n"
        "3. What's missing -- what did the brainstorm NOT consider?\n"
        "4. What are the biggest risks in the top ideas?\n"
        "5. If you had to pick ONE idea to build first, which and why?\n\n"
        "Be specific. Reference actual ideas from the brainstorm. Stay in character."
    )

    return "\n".join(parts)


async def run_panel_analysis(
    brainstorm_content: str,
    focus: str = "",
    timeout: int = 420,
) -> dict[str, str]:
    """Send brainstorm content to all 3 agents in parallel."""
    prompt = build_analysis_prompt(brainstorm_content, focus)
    print("Sending to panel (3 agents in parallel)...", flush=True)
    start = time.time()
    responses = await ask_panel(prompt, timeout=timeout)
    elapsed = time.time() - start
    print(f"Panel responded in {elapsed:.0f}s", flush=True)
    return responses


async def synthesize(responses: dict[str, str], brainstorm_content: str) -> str:
    """Merge agent responses into a single requirements spec."""
    _ensure_loaded()
    agent_names = {
        "cognitive_architect": "The Cognitive Architect (creativity engine designer)",
        "systems_pragmatist": "The Systems Pragmatist (infrastructure realist)",
        "product_oracle": "The Product Oracle (user advocate)",
    }

    parts = ["# Agent Analysis of Brainstorm Session\n"]
    parts.append(f"## Brainstorm Summary (first 500 chars)\n\n{brainstorm_content[:500]}...\n")

    for key, resp in responses.items():
        name = agent_names.get(key, key)
        parts.append(f"## Analysis from {name}\n\n{resp}\n")

    parts.append("\nSynthesize into a single requirements document. Make decisions.")

    print("Synthesizing...", flush=True)
    start = time.time()
    synthesis = await run_claude_async(SYNTHESIS_PROMPT, "\n".join(parts), timeout=420)
    elapsed = time.time() - start
    print(f"Synthesis done in {elapsed:.0f}s", flush=True)
    return synthesis


def save_output(
    responses: dict[str, str],
    synthesis: str | None,
    source: str,
    output_dir: Path,
) -> Path:
    """Save everything to a timestamped output file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"brainstorm_analysis_{timestamp}.md"
    output_path = output_dir / filename

    agent_names = {
        "cognitive_architect": "The Cognitive Architect",
        "systems_pragmatist": "The Systems Pragmatist",
        "product_oracle": "The Product Oracle",
    }

    lines = [
        f"# Brainstorm Analysis",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Source:** {source}",
        f"",
    ]

    if synthesis:
        lines.extend([
            "---",
            "",
            "## Synthesis",
            "",
            synthesis,
            "",
        ])

    lines.extend(["---", "", "## Individual Agent Analyses", ""])

    for key, resp in responses.items():
        name = agent_names.get(key, key)
        lines.extend([f"### {name}", "", resp, "", "---", ""])

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def run_debate_on_brainstorm(brainstorm_content: str, focus: str = ""):
    """Run a debate between agents about the brainstorm output."""
    config_path = Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"
    team = load_team(str(config_path))

    topic = build_analysis_prompt(brainstorm_content, focus)
    return run_debate(team, topic, rounds=2)


def main():
    parser = argparse.ArgumentParser(
        description="Bridge brainstorm sessions to beta-agent panel analysis"
    )
    parser.add_argument(
        "brainstorm_file",
        nargs="?",
        help="Path to brainstorm session markdown file",
    )
    parser.add_argument(
        "--topic",
        help="Quick mode: analyze a topic directly (no brainstorm file needed)",
    )
    parser.add_argument(
        "--focus",
        default="",
        help="Specific question or focus for the analysis",
    )
    parser.add_argument(
        "--mode",
        choices=["panel", "debate", "roundrobin"],
        default="panel",
        help="Discussion mode (default: panel)",
    )
    parser.add_argument(
        "--no-synthesis",
        action="store_true",
        help="Skip the synthesis step, just get raw agent responses",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=420,
        help="Timeout per agent call in seconds (default: 420)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).parent / "output"),
        help="Output directory (default: ./output/)",
    )

    args = parser.parse_args()

    if not args.brainstorm_file and not args.topic:
        parser.error("Provide a brainstorm file or --topic")

    # Load content
    if args.brainstorm_file:
        brainstorm_content = load_brainstorm_file(args.brainstorm_file)
        source = args.brainstorm_file
    else:
        brainstorm_content = args.topic
        source = f"topic: {args.topic}"

    print("=" * 60)
    print("Brainstorm -> Panel Analysis")
    print(f"Source: {source}")
    print(f"Mode: {args.mode}")
    print(f"Focus: {args.focus or '(none)'}")
    print("=" * 60)

    total_start = time.time()

    if args.mode == "panel":
        # Parallel panel analysis + optional synthesis
        responses = asyncio.run(
            run_panel_analysis(brainstorm_content, args.focus, args.timeout)
        )

        # Print responses
        agent_names = {
            "cognitive_architect": "The Cognitive Architect",
            "systems_pragmatist": "The Systems Pragmatist",
            "product_oracle": "The Product Oracle",
        }
        for key, resp in responses.items():
            name = agent_names.get(key, key)
            print(f"\n{'='*40}")
            print(f"{name}")
            print(f"{'='*40}")
            print(resp)

        # Synthesis
        synthesis = None
        if not args.no_synthesis:
            synthesis = asyncio.run(synthesize(responses, brainstorm_content))
            print(f"\n{'='*40}")
            print("SYNTHESIS")
            print(f"{'='*40}")
            print(synthesis)

        # Save
        output_path = save_output(
            responses, synthesis, source, Path(args.output_dir)
        )

    elif args.mode == "debate":
        run_debate_on_brainstorm(brainstorm_content, args.focus)
        output_path = None  # debate mode prints to console

    elif args.mode == "roundrobin":
        config_path = Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"
        team = load_team(str(config_path))
        prompt = build_analysis_prompt(brainstorm_content, args.focus)
        run_round_robin(team, prompt, rounds=3)
        output_path = None

    total_time = time.time() - total_start
    print(f"\nTotal time: {total_time:.0f}s ({total_time/60:.1f} min)")
    if output_path:
        print(f"Output saved: {output_path}")


if __name__ == "__main__":
    main()
