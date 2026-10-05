"""Per-turn prompt assembly — port of RoundRunner.BuildAgentSections /
ConcatenateSections, PromptBuilder's per-turn helpers, DiscussionCompressor,
DiscussionEngine.SynthesizeAsync's payload and MorningBriefGenerator's payload.

The orchestrating model never composes these; it only passes file paths.
"""

import re

from . import data
from .data import Agent

ROUND_INSTRUCTIONS = {
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
}

FIRST_SPEAKER = "You are speaking first this round. Set the agenda. 250 words max (excluding Position Summary)."
LATER_SPEAKER = (
    "Other agents have already spoken this round. Respond to their points directly -- disagree "
    "where you see a flaw, and be specific about why. Do not agree unless you have genuinely new "
    "evidence. 250 words max (excluding Position Summary)."
)
SUMMARY_FORMAT = (
    "IMPORTANT: End your response with exactly this format:\n"
    "## Position Summary\n"
    "[3 sentences: what you advocate, what you reject, and why.]"
)


def round_instruction(round_name: str) -> str:
    if round_name == "counter":
        return data.counter_propose_instruction()
    return ROUND_INSTRUCTIONS.get(round_name, "")


def round_label(round_name: str) -> str:
    return "COUNTER-PROPOSAL" if round_name == "counter" else round_name.upper()


# --- PromptBuilder per-turn helpers ---------------------------------------

def perspective_reminder(agent: Agent) -> str:
    p = agent.personality
    return (
        f"[You are {agent.name} -- {agent.position.role}. "
        f"Style: {p.cognitive_style}, {p.emotional_baseline}. "
        f"Technique: {agent.technique.primary.replace('_', ' ')}. "
        "Stay in character. Add substance or stay silent.]"
    )


def context_lens(agent: Agent) -> str:
    lines = []
    if agent.position.drives:
        lines.append("When reading the context below, focus on:")
        lines += [f"  - {d}" for d in agent.position.drives[:3]]
    if agent.position.pushback_on:
        lines.append("Flag anything that looks like:")
        lines += [f"  - {p}" for p in agent.position.pushback_on[:3]]
    if agent.personality.domain_affinities:
        lines.append("Apply your expertise in: " + ", ".join(agent.personality.domain_affinities[:4]))
    r = agent.personality.idea_receptivity
    if r >= 0.7:
        lines.append("Pay close attention to what other agents proposed. Build on their best ideas.")
    elif r <= 0.3:
        lines.append("Stay focused on your own perspective. Don't get pulled into other agents' framing.")
    if agent.personality.patience <= 0.3:
        lines.append("If the discussion is covering old ground, call it out and push forward.")
    if not lines:
        return ""
    return "=== Your Focus for This Context ===\n" + "\n".join(lines) + "\n=== End Focus ===\n"


def filter_prior_rounds(prior_rounds: str, agent: Agent) -> str:
    if not prior_rounds:
        return prior_rounds
    r, p = agent.personality.idea_receptivity, agent.personality.patience
    if r >= 0.5 and p >= 0.5:
        return prior_rounds
    if p < 0.3 and len(prior_rounds) > 3000:
        trimmed = prior_rounds[-2500:]
        idx = trimmed.find("\n[")
        trimmed = trimmed[idx:] if idx >= 0 else "...\n" + trimmed
        return f"[Earlier discussion truncated -- focusing on recent exchanges]\n{trimmed}"
    return prior_rounds


# --- DiscussionCompressor ---------------------------------------------------

def extract_position_summary(response: str) -> str:
    if not response:
        return ""
    m = re.search(r"##\s*Position Summary\s*\n(.*?)(?=\n## |\Z)", response, re.S)
    if m:
        return m.group(1).strip()
    if len(response) <= 300:
        return response.strip()
    tail = response[-300:]
    sentence_start = tail.find(". ")
    if 0 < sentence_start < 200:
        tail = tail[sentence_start + 2:]
    return tail.strip()


def compress_to_summaries(accumulated: str) -> str:
    if not accumulated:
        return ""
    out = []
    for m in re.finditer(r"\[([^\]]+)\]\n(.*?)(?=\n\[|\Z)", accumulated, re.S):
        out.append(f"[{m.group(1)}]\n{extract_position_summary(m.group(2))}\n")
    return "\n".join(out) + ("\n" if out else "")


def accumulate_discussion(rounds: list) -> str:
    """rounds: [(round_name, [(agent_key, response), ...]), ...] in order."""
    text = ""
    for round_name, responses in rounds:
        for key, resp in responses:
            text += f"[{round_label(round_name)} - {data.display_name(key)}]\n{resp}\n\n"
    return text


# --- Turn payload -------------------------------------------------------------

def build_turn_prompt(
    agent: Agent,
    question,
    *,
    decisions: str,
    prior_rounds: str,
    prior_specs: str,
    open_questions: str,
    round_name: str,
    overlay: str = "",
    this_round_so_far: str = "",
    context: str = "",
) -> str:
    """Same section order and separators as RoundRunner.ConcatenateSections."""
    parts = [perspective_reminder(agent)]
    lens = context_lens(agent)
    if lens:
        parts.append(lens)
    if overlay:
        parts.append(f"=== Your Approach ===\n{overlay}\n=== End Approach ===")
    if context.strip():
        parts.append(f"=== Context (reference material for this discussion) ===\n{context}\n=== End Context ===")
    if decisions:
        parts.append(f"=== What's Already Decided ===\n{decisions}\n=== End Decisions ===")
    if prior_specs:
        parts.append(f"=== Prior Design Docs (reference, don't contradict) ===\n{prior_specs}\n=== End Prior Docs ===")
    if open_questions:
        parts.append(
            "=== Unresolved Open Questions from Prior Docs ===\n"
            f"{open_questions}\n=== End Open Questions ===\n\n"
            "If this question can resolve any of the above, do so."
        )

    prior = filter_prior_rounds(prior_rounds, agent)
    if prior or this_round_so_far:
        block = "=== Discussion So Far (this question) ===\n"
        if prior:
            block += prior + "\n"
        if this_round_so_far:
            if prior:
                block += "\n"
            block += f"--- This round so far ---\n{this_round_so_far}\n"
        block += "=== End Discussion ==="
        parts.append(block)

    parts.append(f"## Question: {question.title}\n\n{question.body}")
    instruction = round_instruction(round_name)
    if instruction:
        parts.append(instruction)
    parts.append(LATER_SPEAKER if this_round_so_far else FIRST_SPEAKER)
    parts.append(SUMMARY_FORMAT)
    return "\n\n".join(parts) + "\n"


# --- Synthesis payload --------------------------------------------------------

def build_synthesis_prompt(question, rounds: list, *, decisions: str, prior_specs: str,
                           open_questions: str, context: str = "", max_ledger_words: int = 50) -> str:
    """Port of DiscussionEngine.SynthesizeAsync's user message, prefixed with the
    values the synthesis template needs (the engine leaves its Jinja placeholders unfilled)."""
    topic_tag = question.title[:60]
    lines = [
        f"Question number: {question.number}",
        f"Topic tag: {topic_tag}",
        f"Max ledger words per entry: {max_ledger_words}",
        "",
        f"# Design Question: {question.title}",
        "",
        "## The Question",
        "",
        question.body,
        "",
    ]
    if context.strip():
        lines += ["## Context (reference material from brief)", "", context, ""]
    if decisions:
        lines += ["## Prior Decisions (from brief)", "", decisions, ""]
    if prior_specs:
        lines += ["## Prior Design Docs", "", prior_specs, ""]
    if open_questions:
        lines += ["## Unresolved Open Questions from Prior Docs", "",
                  "Resolve any of these that this discussion addresses:", "", open_questions, ""]
    for round_name, responses in rounds:
        lines += [f"## Round: {round_label(round_name)}", ""]
        for key, resp in responses:
            lines += [f"### {data.display_name(key)}", "", resp, ""]
    lines += [
        "Synthesize into a single design doc. No code. Focus on behavior and rules.",
        "",
        "IMPORTANT: Output ONLY the design doc. Start with '## Decisions'. "
        "Do not request file permissions, describe what you would write, or add any "
        "meta-commentary before or after the document.",
    ]
    return "\n".join(lines) + "\n"


def build_brief_prompt(ledger_text: str, question_states: dict) -> str:
    """Port of MorningBriefGenerator.GenerateAsync's payload."""
    gaps = []
    for q_key in sorted(question_states, key=lambda k: int(k[1:]) if k[1:].isdigit() else 0):
        st = question_states[q_key]
        if st.get("status") in ("skipped", "partial", "failed"):
            gaps.append(f"- {q_key} ({st.get('title') or '?'}): {st['status']} -- {st.get('reason') or 'unknown'}")
    gap_section = ""
    if gaps:
        gap_section = "\n\nSESSION GAPS (include these in your output):\n" + "\n".join(gaps)
    return f"## Decisions Ledger\n\n{ledger_text}\n{gap_section}\n"


# --- Design-doc derived context ----------------------------------------------

def compress_doc_to_decisions(design_doc: str) -> str:
    headings = re.findall(r"^### (.+)$", design_doc, re.M)
    if not headings:
        return design_doc[:500]
    return "\n".join(f"- {h.strip()}" for h in headings)


def extract_open_questions(design_doc: str) -> list:
    m = re.search(r"## Open Questions\s*\n(.*?)(?=\n## |\Z)", design_doc, re.S)
    if not m:
        return []
    return [i.group(1) for i in re.finditer(r"^[\s]*[-*\d.]+\s+(.+)", m.group(1).strip(), re.M)]
