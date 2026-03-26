"""LLM-based evaluator for agent discussion experiments.

Reads design docs and transcripts from experiment output directories,
scores them on quality dimensions, and produces evaluation reports.
Supports single-experiment evaluation and cross-experiment comparison.

Usage:
    # Evaluate one experiment
    python evaluate_experiment.py ../../experiments/compete

    # Compare multiple experiments
    python evaluate_experiment.py ../../experiments/compete ../../experiments/bigsmall ../../experiments/angles

    # Evaluate with custom output location
    python evaluate_experiment.py ../../experiments/compete --report-dir ../../experiments/reports
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import yaml

# Enable ANSI escape codes on Windows
if sys.platform == "win32":
    os.system("")  # noqa: S605 -- triggers Windows to enable VT100 mode

sys.path.insert(0, str(Path(__file__).parent))

from agentteam.runner.claude import run_claude_async
from config_loader import load_prompt_raw, defaults

# -- Evaluation dimensions --

TRANSCRIPT_EVAL_PROMPT = load_prompt_raw("evaluation/transcript_eval.md.j2")

DESIGN_DOC_EVAL_PROMPT = load_prompt_raw("evaluation/design_doc_eval.md.j2")

AGENT_EVAL_PROMPT = load_prompt_raw("evaluation/agent_eval.md.j2")

EVAL_SYSTEM_PROMPT = load_prompt_raw("evaluation/eval_system.md.j2")

_DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
TEAM_CONFIG = _DATA_DIR / "teams" / "beta-agents.yaml"

# -- ANSI color codes for verbose output --
COLORS = {
    "reset":    "\033[0m",
    "bold":     "\033[1m",
    "dim":      "\033[2m",
    "red":      "\033[31m",
    "green":    "\033[32m",
    "yellow":   "\033[33m",
    "blue":     "\033[34m",
    "magenta":  "\033[35m",
    "cyan":     "\033[36m",
    "white":    "\033[37m",
    "bg_blue":  "\033[44m",
    "bg_green": "\033[42m",
    "bg_mag":   "\033[45m",
}

# Rotating colors for individual agents
AGENT_COLORS = ["cyan", "magenta", "green", "yellow", "blue", "red"]

# Global verbose flag (set from CLI args)
VERBOSE = False

# Lock for serializing verbose print output across parallel tasks
_print_lock = asyncio.Lock()


async def verbose_print(color: str, label: str, content: str):
    """Print color-coded output if verbose mode is on."""
    if not VERBOSE:
        return
    c = COLORS.get(color, "")
    r = COLORS["reset"]
    b = COLORS["bold"]
    d = COLORS["dim"]
    async with _print_lock:
        print(f"\n{b}{c}{'=' * 60}{r}", flush=True)
        print(f"{b}{c}  {label}{r}", flush=True)
        print(f"{b}{c}{'=' * 60}{r}", flush=True)
        # Print content with dimmed color for readability
        for line in content.split("\n"):
            print(f"{c}{line}{r}", flush=True)
        print(flush=True)


def find_experiment_files(exp_dir: Path) -> list[dict]:
    """Find paired design docs and transcripts in an experiment directory."""
    pairs = []
    for doc_path in sorted(exp_dir.glob("*.md")):
        name = doc_path.stem
        if name == "index" or name.endswith("-transcript"):
            continue
        transcript_path = exp_dir / f"{name}-transcript.md"
        pairs.append({
            "name": name,
            "doc_path": doc_path,
            "transcript_path": transcript_path if transcript_path.exists() else None,
        })
    return pairs


def parse_scores(response: str) -> dict | None:
    """Extract JSON scores from LLM response, handling common formatting issues."""
    # Strip markdown fences if present
    cleaned = re.sub(r"```json\s*", "", response)
    cleaned = re.sub(r"```\s*", "", cleaned)
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON object in the response
        match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return None


def load_agent_configs() -> dict:
    """Load agent configs from the team YAML file."""
    if not TEAM_CONFIG.exists():
        return {}
    with open(TEAM_CONFIG, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("agents", {})


def parse_agent_responses(transcript_text: str) -> dict[str, str]:
    """Extract each agent's responses from a transcript.

    Transcripts use '### Agent Name (role)' headers under '## Round: ROUND_NAME'.
    Returns {agent_display_name: concatenated_responses}.
    """
    agents = {}
    current_agent = None
    current_lines = []

    for line in transcript_text.split("\n"):
        if line.startswith("### "):
            # Save previous agent's content
            if current_agent:
                agents.setdefault(current_agent, []).extend(current_lines)
            # Parse agent name: "### The Cognitive Architect (role)"
            header = line[4:].strip()
            paren_idx = header.find("(")
            current_agent = header[:paren_idx].strip() if paren_idx > 0 else header
            current_lines = []
        elif line.startswith("## Round:"):
            # Only treat "## Round:" lines as section boundaries, not agent-internal ## headers
            if current_agent:
                agents.setdefault(current_agent, []).extend(current_lines)
            current_agent = None
            current_lines = []
        elif current_agent:
            current_lines.append(line)

    # Don't forget the last agent
    if current_agent:
        agents.setdefault(current_agent, []).extend(current_lines)

    return {name: "\n".join(lines) for name, lines in agents.items()}


def match_agent_config(display_name: str, configs: dict) -> tuple[str, dict] | None:
    """Match a transcript agent display name to its YAML config key.

    Display names are like 'The Cognitive Architect', config keys are like 'cognitive_architect'.
    """
    # Build lookup: config name field -> (key, config)
    for key, cfg in configs.items():
        cfg_name = cfg.get("name", "")
        if cfg_name == display_name:
            return key, cfg
    # Fallback: fuzzy match on key
    normalized = display_name.lower().replace("the ", "").strip().replace(" ", "_")
    for key, cfg in configs.items():
        if key == normalized or normalized.endswith(key) or key.endswith(normalized):
            return key, cfg
    return None


def format_agent_config_for_eval(cfg: dict) -> str:
    """Format an agent config as readable text for the evaluator."""
    return yaml.dump(cfg, default_flow_style=False, width=120, allow_unicode=True)


async def evaluate_agent(
    agent_name: str, agent_config: dict, agent_responses: str, timeout: int,
    color_idx: int = 0,
) -> dict | None:
    """Score a single agent's performance against its configured personality."""
    config_text = format_agent_config_for_eval(agent_config)
    payload = (
        f"## Agent Configuration\n\n```yaml\n{config_text}```\n\n"
        f"## Agent Responses\n\n{agent_responses[:defaults()['truncation']['agent_eval_input']]}"
    )
    color = AGENT_COLORS[color_idx % len(AGENT_COLORS)]
    await verbose_print(color, f"AGENT EVAL: {agent_name} [prompt]", payload[:2000] + "\n..." if len(payload) > 2000 else payload)
    response = await run_claude_async(
        EVAL_SYSTEM_PROMPT + "\n\n" + AGENT_EVAL_PROMPT,
        payload,
        timeout=timeout,
    )
    await verbose_print(color, f"AGENT EVAL: {agent_name} [response]", response)
    return parse_scores(response)


async def evaluate_transcript(transcript_text: str, timeout: int) -> dict | None:
    """Score a transcript on quality dimensions."""
    payload = f"## Transcript to Evaluate\n\n{transcript_text[:defaults()['truncation']['doc_eval_input']]}"
    await verbose_print("cyan", "TRANSCRIPT EVAL [prompt]", payload[:2000] + "\n..." if len(payload) > 2000 else payload)
    response = await run_claude_async(
        EVAL_SYSTEM_PROMPT + "\n\n" + TRANSCRIPT_EVAL_PROMPT,
        payload,
        timeout=timeout,
    )
    await verbose_print("cyan", "TRANSCRIPT EVAL [response]", response)
    return parse_scores(response)


async def evaluate_design_doc(doc_text: str, timeout: int) -> dict | None:
    """Score a design doc on quality dimensions."""
    payload = f"## Design Document to Evaluate\n\n{doc_text[:defaults()['truncation']['doc_eval_input']]}"
    await verbose_print("yellow", "DESIGN DOC EVAL [prompt]", payload[:2000] + "\n..." if len(payload) > 2000 else payload)
    response = await run_claude_async(
        EVAL_SYSTEM_PROMPT + "\n\n" + DESIGN_DOC_EVAL_PROMPT,
        payload,
        timeout=timeout,
    )
    await verbose_print("yellow", "DESIGN DOC EVAL [response]", response)
    return parse_scores(response)


async def evaluate_pair(pair: dict, agent_configs: dict, timeout: int) -> dict:
    """Evaluate a doc/transcript pair and individual agents in parallel."""
    name = pair["name"]
    print(f"  Evaluating {name}...", flush=True)

    tasks = []

    # Design doc evaluation
    doc_text = pair["doc_path"].read_text(encoding="utf-8")
    tasks.append(evaluate_design_doc(doc_text, timeout))

    # Transcript evaluation (if exists)
    transcript_text = None
    if pair["transcript_path"]:
        transcript_text = pair["transcript_path"].read_text(encoding="utf-8")
        tasks.append(evaluate_transcript(transcript_text, timeout))
    else:
        async def _noop():
            return None
        tasks.append(_noop())

    # Agent-level evaluations (parallel with doc/transcript evals)
    agent_eval_names = []  # Track which agent each task corresponds to
    if transcript_text and agent_configs:
        agent_responses = parse_agent_responses(transcript_text)
        for display_name, responses in agent_responses.items():
            if not responses.strip():
                continue
            match = match_agent_config(display_name, agent_configs)
            if match:
                config_key, cfg = match
                color_idx = len(agent_eval_names)
                agent_eval_names.append(display_name)
                tasks.append(evaluate_agent(display_name, cfg, responses, timeout, color_idx))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    doc_scores = results[0] if not isinstance(results[0], Exception) else None
    transcript_scores = results[1] if len(results) > 1 and not isinstance(results[1], Exception) else None

    # Collect agent scores
    agent_scores = {}
    for i, agent_name in enumerate(agent_eval_names):
        result_idx = 2 + i
        if result_idx < len(results) and not isinstance(results[result_idx], Exception):
            agent_scores[agent_name] = results[result_idx]

    return {
        "name": name,
        "doc_scores": doc_scores,
        "transcript_scores": transcript_scores,
        "agent_scores": agent_scores,
    }


def compute_summary(evaluations: list[dict]) -> dict:
    """Compute aggregate scores across all evaluated pairs."""
    doc_totals = {}
    doc_counts = {}
    transcript_totals = {}
    transcript_counts = {}

    def _extract_score(data) -> float:
        """Safely extract a numeric score from LLM output."""
        raw = data.get("score", 0) if isinstance(data, dict) else data
        try:
            return float(raw)
        except (TypeError, ValueError):
            return 0.0

    # Agent-level aggregation: {agent_name: {dim: [scores]}}
    agent_dim_scores = {}

    for ev in evaluations:
        if ev["doc_scores"]:
            for dim, data in ev["doc_scores"].items():
                score = _extract_score(data)
                doc_totals[dim] = doc_totals.get(dim, 0) + score
                doc_counts[dim] = doc_counts.get(dim, 0) + 1

        if ev["transcript_scores"]:
            for dim, data in ev["transcript_scores"].items():
                score = _extract_score(data)
                transcript_totals[dim] = transcript_totals.get(dim, 0) + score
                transcript_counts[dim] = transcript_counts.get(dim, 0) + 1

        for agent_name, scores in ev.get("agent_scores", {}).items():
            if not scores:
                continue
            if agent_name not in agent_dim_scores:
                agent_dim_scores[agent_name] = {}
            for dim, data in scores.items():
                score = _extract_score(data)
                agent_dim_scores[agent_name].setdefault(dim, []).append(score)

    doc_avgs = {dim: round(doc_totals[dim] / doc_counts[dim], 1) for dim in doc_totals}
    transcript_avgs = {dim: round(transcript_totals[dim] / transcript_counts[dim], 1) for dim in transcript_totals}

    # Agent averages: {agent_name: {dim: avg, "avg": overall_avg}}
    agent_averages = {}
    for agent_name, dims in agent_dim_scores.items():
        agent_avgs = {}
        for dim, scores_list in dims.items():
            agent_avgs[dim] = round(sum(scores_list) / len(scores_list), 1)
        all_agent_scores = list(agent_avgs.values())
        agent_avgs["avg"] = round(sum(all_agent_scores) / len(all_agent_scores), 1) if all_agent_scores else 0
        agent_averages[agent_name] = agent_avgs

    all_scores = list(doc_avgs.values()) + list(transcript_avgs.values())
    overall = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0

    return {
        "doc_averages": doc_avgs,
        "transcript_averages": transcript_avgs,
        "agent_averages": agent_averages,
        "overall": overall,
    }


def format_report(exp_name: str, evaluations: list[dict], summary: dict, elapsed: float) -> str:
    """Format a human-readable evaluation report."""
    lines = [
        f"# Evaluation: {exp_name}",
        "",
        f"*Evaluated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | {elapsed:.0f}s*",
        "",
        f"## Overall Score: {summary['overall']}/10",
        "",
    ]

    # Summary table - design docs
    if summary["doc_averages"]:
        lines.append("### Design Doc Scores (averaged)")
        lines.append("")
        lines.append("| Dimension | Avg Score |")
        lines.append("|-----------|-----------|")
        for dim, score in sorted(summary["doc_averages"].items()):
            lines.append(f"| {dim.replace('_', ' ').title()} | {score}/10 |")
        lines.append("")

    # Summary table - transcripts
    if summary["transcript_averages"]:
        lines.append("### Transcript Scores (averaged)")
        lines.append("")
        lines.append("| Dimension | Avg Score |")
        lines.append("|-----------|-----------|")
        for dim, score in sorted(summary["transcript_averages"].items()):
            lines.append(f"| {dim.replace('_', ' ').title()} | {score}/10 |")
        lines.append("")

    # Agent authenticity scores
    if summary.get("agent_averages"):
        lines.append("### Agent Authenticity Scores")
        lines.append("")
        lines.append("| Agent | Avg | Strongest | Weakest |")
        lines.append("|-------|-----|-----------|---------|")
        for agent_name, dims in sorted(summary["agent_averages"].items()):
            avg = dims.get("avg", "-")
            # Find best/worst dimensions (excluding 'avg')
            scored_dims = {k: v for k, v in dims.items() if k != "avg" and isinstance(v, (int, float))}
            if scored_dims:
                best_k = max(scored_dims, key=scored_dims.get)
                worst_k = min(scored_dims, key=scored_dims.get)
                best = f"{best_k.replace('_', ' ')} ({scored_dims[best_k]})"
                worst = f"{worst_k.replace('_', ' ')} ({scored_dims[worst_k]})"
            else:
                best = worst = "-"
            lines.append(f"| {agent_name} | {avg} | {best} | {worst} |")
        lines.append("")

    # Per-question detail
    lines.append("## Per-Question Detail")
    lines.append("")

    for ev in evaluations:
        lines.append(f"### {ev['name']}")
        lines.append("")

        if ev["doc_scores"]:
            lines.append("**Design Doc:**")
            lines.append("")
            for dim, data in ev["doc_scores"].items():
                if isinstance(data, dict):
                    lines.append(f"- **{dim.replace('_', ' ').title()}**: {data.get('score', '?')}/10 -- {data.get('evidence', '')}")
                else:
                    lines.append(f"- **{dim.replace('_', ' ').title()}**: {data}/10")
            lines.append("")

        if ev["transcript_scores"]:
            lines.append("**Transcript:**")
            lines.append("")
            for dim, data in ev["transcript_scores"].items():
                if isinstance(data, dict):
                    lines.append(f"- **{dim.replace('_', ' ').title()}**: {data.get('score', '?')}/10 -- {data.get('evidence', '')}")
                else:
                    lines.append(f"- **{dim.replace('_', ' ').title()}**: {data}/10")
            lines.append("")

        if ev.get("agent_scores"):
            lines.append("**Agent Authenticity:**")
            lines.append("")
            for agent_name, scores in sorted(ev["agent_scores"].items()):
                if not scores:
                    continue
                parts = []
                for dim, data in scores.items():
                    if isinstance(data, dict):
                        s = data.get("score", "?")
                        e = data.get("evidence", "")
                        parts.append(f"{dim.replace('_', ' ')}: {s}")
                    else:
                        parts.append(f"{dim.replace('_', ' ')}: {data}")
                lines.append(f"- **{agent_name}**: {' | '.join(parts)}")
            lines.append("")

    return "\n".join(lines)


def format_comparison(all_results: dict[str, dict]) -> str:
    """Format a cross-experiment comparison report."""
    lines = [
        "# Experiment Comparison",
        "",
        f"*Compared: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "## Overall Scores",
        "",
        "| Experiment | Overall | Best Dimension | Worst Dimension |",
        "|------------|---------|----------------|-----------------|",
    ]

    for exp_name, data in all_results.items():
        summary = data["summary"]
        overall = summary["overall"]

        # Find best and worst across all dimensions
        all_dims = {}
        all_dims.update(summary.get("doc_averages", {}))
        all_dims.update(summary.get("transcript_averages", {}))

        if all_dims:
            best = max(all_dims, key=all_dims.get)
            worst = min(all_dims, key=all_dims.get)
            best_str = f"{best.replace('_', ' ')} ({all_dims[best]})"
            worst_str = f"{worst.replace('_', ' ')} ({all_dims[worst]})"
        else:
            best_str = worst_str = "N/A"

        lines.append(f"| {exp_name} | **{overall}**/10 | {best_str} | {worst_str} |")

    lines.append("")

    # Dimension-by-dimension comparison
    lines.append("## Design Doc Dimensions")
    lines.append("")

    # Collect all doc dimensions
    all_doc_dims = set()
    for data in all_results.values():
        all_doc_dims.update(data["summary"].get("doc_averages", {}).keys())

    if all_doc_dims:
        header = "| Dimension |"
        separator = "|-----------|"
        for exp_name in all_results:
            header += f" {exp_name} |"
            separator += "------|"
        lines.append(header)
        lines.append(separator)

        for dim in sorted(all_doc_dims):
            row = f"| {dim.replace('_', ' ').title()} |"
            scores = []
            for exp_name, data in all_results.items():
                score = data["summary"].get("doc_averages", {}).get(dim, "-")
                scores.append(score)
                row += f" {score} |"
            # Bold the winner
            lines.append(row)
        lines.append("")

    # Transcript dimensions
    lines.append("## Transcript Dimensions")
    lines.append("")

    all_trans_dims = set()
    for data in all_results.values():
        all_trans_dims.update(data["summary"].get("transcript_averages", {}).keys())

    if all_trans_dims:
        header = "| Dimension |"
        separator = "|-----------|"
        for exp_name in all_results:
            header += f" {exp_name} |"
            separator += "------|"
        lines.append(header)
        lines.append(separator)

        for dim in sorted(all_trans_dims):
            row = f"| {dim.replace('_', ' ').title()} |"
            for exp_name, data in all_results.items():
                score = data["summary"].get("transcript_averages", {}).get(dim, "-")
                row += f" {score} |"
            lines.append(row)
        lines.append("")

    # Agent authenticity comparison
    all_agents = set()
    for data in all_results.values():
        all_agents.update(data["summary"].get("agent_averages", {}).keys())

    if all_agents:
        lines.append("## Agent Authenticity (averaged across questions)")
        lines.append("")
        header = "| Agent |"
        separator = "|-------|"
        for exp_name in all_results:
            header += f" {exp_name} |"
            separator += "------|"
        lines.append(header)
        lines.append(separator)

        for agent_name in sorted(all_agents):
            row = f"| {agent_name} |"
            for exp_name, data in all_results.items():
                score = data["summary"].get("agent_averages", {}).get(agent_name, {}).get("avg", "-")
                row += f" {score} |"
            lines.append(row)
        lines.append("")

    # Recommendations
    lines.append("## Winner")
    lines.append("")
    if all_results:
        winner = max(all_results, key=lambda k: all_results[k]["summary"]["overall"])
        lines.append(f"**{winner}** with overall score {all_results[winner]['summary']['overall']}/10")
    lines.append("")

    return "\n".join(lines)


async def evaluate_experiment(exp_dir: Path, timeout: int) -> tuple[list[dict], dict]:
    """Evaluate all files in an experiment directory."""
    pairs = find_experiment_files(exp_dir)
    if not pairs:
        print(f"  No design docs found in {exp_dir}")
        return [], {"doc_averages": {}, "transcript_averages": {}, "agent_averages": {}, "overall": 0}

    # Load agent configs for authenticity evaluation
    agent_configs = load_agent_configs()

    # Evaluate all pairs in parallel
    tasks = [evaluate_pair(pair, agent_configs, timeout) for pair in pairs]
    evaluations = await asyncio.gather(*tasks)
    evaluations = [e for e in evaluations if not isinstance(e, Exception)]

    summary = compute_summary(evaluations)
    return evaluations, summary


async def main():
    parser = argparse.ArgumentParser(
        description="Evaluate agent discussion experiment output using LLM scoring.",
    )
    parser.add_argument(
        "experiments",
        nargs="+",
        help="One or more experiment output directories to evaluate",
    )
    parser.add_argument(
        "--report-dir",
        default=None,
        help="Where to write reports (default: next to each experiment dir)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout per LLM eval call (default: 300s)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show color-coded LLM prompts and responses as they complete",
    )

    args = parser.parse_args()

    global VERBOSE
    VERBOSE = args.verbose

    all_results = {}
    total_start = time.time()

    for exp_path_str in args.experiments:
        exp_dir = Path(exp_path_str)
        if not exp_dir.is_absolute():
            exp_dir = Path.cwd() / exp_dir
        if not exp_dir.exists():
            print(f"WARNING: {exp_dir} not found, skipping")
            continue

        exp_name = exp_dir.name
        print(f"\n{'=' * 50}")
        print(f"Evaluating: {exp_name}")
        print(f"{'=' * 50}")

        start = time.time()
        evaluations, summary = await evaluate_experiment(exp_dir, args.timeout)
        elapsed = time.time() - start

        if not evaluations:
            continue

        print(f"  Overall: {summary['overall']}/10 ({elapsed:.0f}s)")

        # Write individual report
        report = format_report(exp_name, evaluations, summary, elapsed)
        if args.report_dir:
            report_dir = Path(args.report_dir)
            if not report_dir.is_absolute():
                report_dir = Path.cwd() / report_dir
        else:
            report_dir = exp_dir

        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"eval-{exp_name}.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"  Report: {report_path}")

        all_results[exp_name] = {
            "evaluations": evaluations,
            "summary": summary,
        }

    # Cross-experiment comparison if multiple
    if len(all_results) > 1:
        comparison = format_comparison(all_results)

        if args.report_dir:
            comp_dir = Path(args.report_dir)
            if not comp_dir.is_absolute():
                comp_dir = Path.cwd() / comp_dir
        else:
            comp_dir = Path(args.experiments[0])
            if not comp_dir.is_absolute():
                comp_dir = Path.cwd() / comp_dir
            comp_dir = comp_dir.parent

        comp_dir.mkdir(parents=True, exist_ok=True)
        comp_path = comp_dir / "eval-comparison.md"
        comp_path.write_text(comparison, encoding="utf-8")
        print(f"\nComparison report: {comp_path}")

    total_elapsed = time.time() - total_start
    print(f"\nDone. {len(all_results)} experiments evaluated in {total_elapsed:.0f}s")


if __name__ == "__main__":
    asyncio.run(main())
