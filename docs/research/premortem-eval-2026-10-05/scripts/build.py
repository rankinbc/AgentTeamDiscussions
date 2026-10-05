#!/usr/bin/env python3
"""Build the Step 1 experiment: 5 subjects x (single-call arm, 3-critic team arm).

Writes one context packet per subject plus every prompt file. Both arms get the
same packet, the same output format and the same length cap.
"""

from pathlib import Path

REPO = Path("/home/user/AgentTeamDiscussions")
OUT = Path(__file__).resolve().parent
DOCS = REPO / "docs"

ENGINE_FACTS = """## Current engine facts (as of 2026-10-05, verified against the code)

- C# .NET 8 engine shells out to `claude -p` for every agent turn; one system prompt per persona, built from YAML.
- A session runs a list of questions. Each question runs fixed rounds from a mode (e.g. propose -> critique -> evaluate),
  agents speak sequentially within a round, then one synthesis call writes a design doc.
- Between rounds, agents only see earlier rounds' "## Position Summary" blocks (3 sentences each); within a round they
  see earlier speakers in full.
- Context per turn: persona reminder, focus lens, role overlay, brief context, decided items + decisions ledger,
  headings of the previous design doc, open questions carried from earlier docs, discussion so far, the question.
  A budget enforcer trims unprotected sections when a payload exceeds ~10k tokens.
- The decisions ledger (DECIDED / CONTESTED / OPEN lines per question) chains forward to later questions.
  Until 2026-10-05 the synthesis template was never rendered, so no session before then produced a real ledger.
- An Evaluator exists: after a session it scores design docs (7 dimensions) and transcripts (10 dimensions) 1-10 via an
  LLM judge and writes a report. Nothing reads those scores back; persona YAML is static and edited by hand.
- There is no phase system, no moderator input channel, no research engine, and no live/rolling synthesis in the
  running code. Templates for rolling synthesis exist but are unused.
- One developer, solo project. Sessions are run occasionally, not in production. 17 sessions exist on disk.
"""

SUBJECTS = [
    {
        "id": "s1-phase-triggers",
        "title": "How should phase transitions be triggered?",
        "body": ("The V2 roadmap plans a Phase System (Brainstorm -> Refine -> Specify -> Review). Open question: "
                 "should transitions be time-based, convergence-based, round-count based, or something else?"),
        "docs": ["v2/ROADMAP.md", "v2/ideas/phase-dynamics.md", "v2/ideas/orchestrator-event-cadence.md"],
    },
    {
        "id": "s2-eval-feedback",
        "title": "How does the evaluation engine feed back into agent behavior for subsequent sessions?",
        "body": ("The roadmap lists an Evaluation Engine (rubric scoring of design docs). Open question: how should "
                 "evaluation results change agent behavior in later sessions?"),
        "docs": ["v2/ROADMAP.md", "v1/v1-spec-gaps.md", "v2/ideas/agent-behavior-philosophy.md"],
    },
    {
        "id": "s3-moderator-vs-phases",
        "title": "What's the boundary between moderator input and phase system auto-transitions?",
        "body": ("V2 plans both live moderator steering via HTTP and automatic phase transitions. Open question: "
                 "where is the boundary between the two, and who wins when they conflict?"),
        "docs": ["v2/ROADMAP.md", "v2/ideas/moderator-input.md", "v2/ideas/phase-dynamics.md"],
    },
    {
        "id": "s4-research-integration",
        "title": "How do research engine results integrate into the context assembly pipeline?",
        "body": ("V2 plans a Research Engine that gathers external knowledge during discussions. Open question: how "
                 "do its results enter the per-turn context assembly?"),
        "docs": ["v2/ROADMAP.md", "v2/ideas/research-engine.md", "v2/ideas/research-scope-controls.md",
                 "v1/conversation-engine/context-assembly-template.md"],
    },
    {
        "id": "s5-critical-path",
        "title": "Is the V2 critical path (build order) right?",
        "body": ("The roadmap proposes this build order: blind proposals -> manifest versioning -> phase system -> "
                 "key takeaways -> stale detection -> anti-sycophancy detection, with the BIT system in parallel. "
                 "Is this the right plan?"),
        "docs": ["v2/ROADMAP.md", "v2/ideas/implementation-gaps.md"],
    },
]

TASK = """## Your task: pre-mortem

Assume the plan described in the documents above was built as written, and three months later it has clearly failed
or been abandoned. Work out why. Then report what is still undecided and what only the author can answer.

Rules:
- Every finding must be specific to THIS plan and these documents. Generic software advice is worthless.
- Ground findings in the documents or the engine facts: cite the doc or fact you are relying on.
- Rank by how likely and how costly the failure is. Fewer, sharper findings beat a long list.
- No code, no schemas.
"""

FORMAT = """## Output format (exactly these three sections, at most {cap} words in total)

## What breaks
Numbered, most important first. Each item: one bold sentence stating the failure, then 1-3 sentences on why,
citing the document or fact.

## Undecided
Bulleted decisions the plan needs but has not made.

## Questions for you
Bulleted questions only the author can answer, each one sentence.
"""


def packet(s: dict) -> str:
    parts = [f"# Pre-mortem subject: {s['title']}", "", s["body"], "", ENGINE_FACTS]
    for rel in s["docs"]:
        parts += ["", f"---\n\n# Source document: docs/{rel}", "", (DOCS / rel).read_text(encoding="utf-8").strip()]
    return "\n".join(parts) + "\n"


def main():
    for s in SUBJECTS:
        d = OUT / s["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "packet.md").write_text(packet(s), encoding="utf-8")

        # Arm A: one strong call.
        (d / "single.prompt.md").write_text(
            "You are a senior design reviewer doing a rigorous, adversarial pre-mortem of a planning document. "
            "Attack the plan from every angle that matters: engineering feasibility, failure modes and operations, "
            "the user's real experience, and scope for a solo developer. Do not be agreeable.\n\n"
            f"Read the context packet: {d / 'packet.md'}\n\n" + TASK + "\n" + FORMAT.format(cap=700),
            encoding="utf-8")

        # Arm B: three independent critics, then a synthesis.
        (d / "critic.prompt.md").write_text(
            f"Read the context packet: {d / 'packet.md'}\n\n" + TASK +
            "\nYou are one of three independent reviewers; you cannot see the others. Attack from YOUR perspective "
            "only. At most 400 words, as a numbered list of findings, each with a bold one-sentence failure and why.\n",
            encoding="utf-8")
        (d / "synth.prompt.md").write_text(
            "You are merging three independent pre-mortem reviews of the same plan into one report for the author.\n\n"
            f"Context packet (for checking claims): {d / 'packet.md'}\n"
            f"Review 1: {d / 'critic-1.md'}\nReview 2: {d / 'critic-2.md'}\nReview 3: {d / 'critic-3.md'}\n\n"
            "Rules:\n"
            "- You are a reporter, not a fourth reviewer: do not add findings of your own.\n"
            "- Merge duplicates; rank by how many reviewers raised it and how costly the failure is.\n"
            "- Drop findings that are generic or contradicted by the packet.\n"
            "- Where reviewers disagree, keep both sides in one item.\n"
            "- Do not name or describe the reviewers or say how many there were; write as a single report.\n\n"
            + FORMAT.format(cap=700),
            encoding="utf-8")
    print("built", len(SUBJECTS), "subjects in", OUT)
    for s in SUBJECTS:
        print(s["id"], len((OUT / s["id"] / "packet.md").read_text().split()), "words")


if __name__ == "__main__":
    main()
