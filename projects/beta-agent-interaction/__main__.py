"""Entry point -- run with: python __main__.py [single|multi|brainstorm]

Usage:
    cd beta-agent-interaction/
    python __main__.py                          # mode picker
    python __main__.py single                   # single-agent conversation
    python __main__.py multi                    # multi-agent discussion
    python __main__.py brainstorm               # analyze brainstorm session with panel
    python __main__.py brainstorm path/to/file  # analyze specific file
"""

import sys
from pathlib import Path

# Ensure this directory is on sys.path for direct imports
_pkg_dir = str(Path(__file__).resolve().parent)
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else None

    if mode == "single":
        from interact import main as interact_main
        interact_main()
        return
    elif mode == "multi":
        from multi_agent import main as multi_main
        multi_main()
        return
    elif mode == "brainstorm":
        from brainstorm_to_panel import main as brainstorm_main
        # Pass remaining args (file path, --focus, etc.)
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        brainstorm_main()
        return

    print("Beta Agent System")
    print("=================")
    print()
    print("Modes:")
    print("  1. Single agent conversation")
    print("  2. Multi-agent discussion")
    print("  3. Brainstorm analysis (feed /bmad-brainstorming output to panel)")
    print()
    print("Or run: python __main__.py single | multi | brainstorm")
    print()

    choice = input("Pick a mode (1-3): ").strip()

    if choice == "1":
        from interact import main as interact_main
        interact_main()
    elif choice == "2":
        from multi_agent import main as multi_main
        multi_main()
    elif choice == "3":
        _interactive_brainstorm()
    else:
        print("Invalid choice.")
        sys.exit(1)


def _interactive_brainstorm():
    """Interactive brainstorm analysis mode."""
    from brainstorm_to_panel import (
        load_brainstorm_file,
        run_panel_analysis,
        synthesize,
        save_output,
        build_analysis_prompt,
    )
    import asyncio
    import time

    print()
    print("Brainstorm Analysis")
    print("-------------------")
    print()
    print("Options:")
    print("  1. Analyze a brainstorm session file")
    print("  2. Quick topic analysis (no file)")
    print()

    choice = input("Pick (1-2): ").strip()

    if choice == "1":
        file_path = input("Path to brainstorm file: ").strip()
        if not file_path:
            print("No path provided.")
            return
        brainstorm_content = load_brainstorm_file(file_path)
        source = file_path
    elif choice == "2":
        topic = input("Topic: ").strip()
        if not topic:
            print("No topic provided.")
            return
        brainstorm_content = topic
        source = f"topic: {topic}"
    else:
        print("Invalid choice.")
        return

    focus = input("Specific focus/question (or Enter to skip): ").strip()

    print()
    print("Mode:")
    print("  1. Panel (parallel, independent responses + synthesis)")
    print("  2. Debate (agents argue positions)")
    print("  3. Round-robin (agents build on each other)")
    print()
    mode = input("Pick (1-3) [1]: ").strip() or "1"

    output_dir = Path(__file__).parent / "output"

    if mode == "1":
        total_start = time.time()
        responses = asyncio.run(run_panel_analysis(brainstorm_content, focus))

        agent_names = {
            "cognitive_architect": "The Cognitive Architect",
            "systems_pragmatist": "The Systems Pragmatist",
            "product_oracle": "The Product Oracle",
        }
        for key, resp in responses.items():
            name = agent_names.get(key, key)
            print(f"\n{'='*40}")
            print(name)
            print(f"{'='*40}")
            print(resp)

        synthesis = asyncio.run(synthesize(responses, brainstorm_content))
        print(f"\n{'='*40}")
        print("SYNTHESIS")
        print(f"{'='*40}")
        print(synthesis)

        output_path = save_output(responses, synthesis, source, output_dir)
        print(f"\nSaved: {output_path}")
        print(f"Total: {time.time() - total_start:.0f}s")

    elif mode == "2":
        from multi_agent import run_debate
        from interact import load_team
        config_path = Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"
        team = load_team(str(config_path))
        prompt = build_analysis_prompt(brainstorm_content, focus)
        run_debate(team, prompt, rounds=2)

    elif mode == "3":
        from multi_agent import run_round_robin
        from interact import load_team
        config_path = Path(__file__).parent / "config" / "teams" / "beta-agents.yaml"
        team = load_team(str(config_path))
        prompt = build_analysis_prompt(brainstorm_content, focus)
        run_round_robin(team, prompt, rounds=3)


if __name__ == "__main__":
    main()
