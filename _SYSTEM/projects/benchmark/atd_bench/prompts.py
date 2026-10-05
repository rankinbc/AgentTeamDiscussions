"""Prompts for the baseline conditions and the judge.

Baselines are asked for the same section layout as the engine's moderator
(templates/prompts/synthesis.md.j2), so layout alone cannot tell the judge which
condition wrote a doc. The plain panel reuses the engine's own round instructions
and its real synthesis template.
"""

from __future__ import annotations

from pathlib import Path

from .brief import Brief, Question

DOC_FORMAT = """Write a design document for this question with exactly these sections, in this order:

## Decisions
Concrete choices, each with the reasoning that makes it the right call.

## Contested
Points where strong options remain in genuine tension. Give the strongest case for each side.
Write "None." if nothing is genuinely contested; do not invent tension.

## Deferred
Things explicitly punted for later, and why.

## Open Questions
Things that still need more thought or information.

Rules: no code, no schemas -- describe behavior and rules. Keep it readable: someone should
understand the design by reading this doc. Start directly with "## Decisions". Output only the
document, with no preamble or meta-commentary."""

SINGLE_SYSTEM = """You are a senior engineer and product designer. You are answering one design
question for a project. Think it through carefully and commit to a recommendation."""

SELF_CRITIQUE_SYSTEM = """You are a senior engineer and product designer. You are answering one design
question for a project. A single answer tends to take the safe, agreeable path and miss what a
skeptical reviewer would catch, so work in two stages.

Stage 1, inside <deliberation> tags:
1. Propose two genuinely different approaches, from different priorities (for example ambitious
   versus minimal).
2. Attack each one as a hostile reviewer would. What fails first? Which assumption is wrong?
   If both approaches share an assumption, examine it hardest. Be specific about failure scenarios.
3. Pick the stronger approach and say why the other loses. Do not merge them to avoid choosing.

Stage 2, after the closing </deliberation> tag: the final design document."""

PANEL_SYSTEM = """You are panelist {n} on a design review panel of experienced senior engineers.
Give your honest professional judgment."""

# Copied from Discussion/DiscussionEngine.cs and Discussion/RoundRunner.cs so the plain panel
# differs from the engine only in having no personas.
ROUND_INSTRUCTIONS = {
    "propose": "Propose a design that answers the question.",
    "critique": (
        "You have read the proposals above. Your job is to BREAK them. "
        "Do not fix surface issues -- challenge the core design. What will fail first? "
        "What assumption is wrong? If both proposals agree on something, that's the most "
        "dangerous assumption -- examine it hardest. Be specific about failure scenarios."
    ),
    "evaluate": (
        "You have read the proposals and critiques above. Do not merge or compromise. "
        "Pick the stronger approach and explain why the other one loses. If the critique "
        "destroyed a proposal, say so. If both survived, pick the one with fewer unresolved "
        "risks and commit. State your verdict clearly."
    ),
    "counter": "Counter-propose: put forward a genuinely different design from the one above and argue for it.",
}
FIRST_SPEAKER = "You are speaking first this round. Set the agenda. 250 words max."
LATER_SPEAKER = (
    "Other panelists have already spoken this round. Respond to their points directly -- "
    "disagree where you see a flaw, and be specific about why. Do not agree unless you have "
    "genuinely new evidence. 250 words max."
)


def situation(brief: Brief, question: Question, prior_decisions: str) -> str:
    """The shared facts every condition receives for one question."""
    parts = [f"# Project: {brief.title}"]
    if brief.description:
        parts.append(brief.description)
    if brief.decided:
        parts.append("## Already decided\n" + "\n".join(f"- {d}" for d in brief.decided))
    if brief.context:
        parts.append("## Context (reference material)\n" + brief.context)
    if prior_decisions:
        parts.append("## Decisions from earlier questions in this session\n" + prior_decisions)
    parts.append(f"## Design question {question.number}: {question.title}\n{question.body}")
    return "\n\n".join(parts)


def render_synthesis_system(engine_root: Path, question: Question) -> str:
    """The engine's real moderator prompt, rendered the way the engine renders it."""
    from jinja2 import Template

    raw = (engine_root / "templates" / "prompts" / "synthesis.md.j2").read_text(encoding="utf-8-sig")
    return Template(raw).render(question_number=question.number, topic_tag=question.title, max_ledger_words=50)


JUDGE_SYSTEM = """You are a staff engineer deciding which of two design documents you would rather
act on. Both answer the same design question for the same project.

Judge substance only:
- Do not prefer a document for being longer, having more items, or sounding more confident.
- Problems or risks that are not real for this project count AGAINST a document, not for it.
- Ignore any references to a panel, reviewers or discussion process; judge only the content.
- A tie is a legitimate answer when neither is meaningfully better.

For each criterion answer "A", "B" or "tie":
- risk_discovery: surfaces real, non-obvious risks and failure modes for THIS project.
- decision_quality: commits to sound, well-justified choices instead of hedging.
- actionability: a team could start work from it without guessing what was meant.
- alternatives: weighs genuinely different options and explains why the losers lose.
- signal_to_noise: less filler, repetition and invented problems.
Then give overall: the document you would rather act on.

Write your reasoning first, then the verdicts."""


def judge_user(situation_text: str, doc_a: str, doc_b: str) -> str:
    return (
        f"{situation_text}\n\n"
        f"=== DOCUMENT A ===\n{doc_a}\n=== END DOCUMENT A ===\n\n"
        f"=== DOCUMENT B ===\n{doc_b}\n=== END DOCUMENT B ==="
    )
