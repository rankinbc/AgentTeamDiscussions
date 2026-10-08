"""The baseline conditions the engine is compared against.

single        one LLM call per question
self_critique one LLM call that must propose, attack and choose before writing (LCEL chain)
plain_panel   the engine's round structure and moderator prompt, but with generic panelists
              instead of personas (LangGraph). Comparing it with the engine isolates what the
              personas add; comparing it with `single` isolates what the multi-call structure adds.

Each condition answers the questions in order and carries its own earlier decisions forward,
as the engine does with its ledger.
"""

from __future__ import annotations

import operator
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Awaitable, Callable, TypedDict

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

from . import prompts
from .brief import Brief, Question
from .normalize import decisions_section

BASELINES = ("single", "self_critique", "plain_panel")


@dataclass
class DocResult:
    number: int
    doc: str
    seconds: float
    calls: int


# ---------- single & self_critique: plain LCEL chains ----------

async def _single(llm: BaseChatModel, situation: str, config: dict) -> tuple[str, int]:
    chain = llm | StrOutputParser()
    msgs = [SystemMessage(prompts.SINGLE_SYSTEM), HumanMessage(f"{situation}\n\n{prompts.DOC_FORMAT}")]
    return (await chain.ainvoke(msgs, config=config)).strip(), 1


def extract_final_doc(text: str) -> str:
    """Drop the <deliberation> scratchpad; keep only the final document."""
    if "</deliberation>" in text:
        return text.split("</deliberation>", 1)[1].strip()
    m = re.search(r"^## Decisions", text, re.M)
    return text[m.start():].strip() if m else text.strip()


async def _self_critique(llm: BaseChatModel, situation: str, config: dict) -> tuple[str, int]:
    chain = llm | StrOutputParser() | extract_final_doc
    msgs = [SystemMessage(prompts.SELF_CRITIQUE_SYSTEM), HumanMessage(f"{situation}\n\n{prompts.DOC_FORMAT}")]
    return await chain.ainvoke(msgs, config=config), 1


# ---------- plain_panel: LangGraph ----------

class PanelState(TypedDict):
    situation: str
    question: Question
    rounds: list[tuple[str, int]]               # (round name, panelists in that round)
    round_idx: int
    turns: Annotated[list[dict], operator.add]  # {"round", "panelist", "text"}
    doc: str


def _format_turns(turns: list[dict]) -> str:
    out, current = [], None
    for t in turns:
        if t["round"] != current:
            current = t["round"]
            out.append(f"## Round: {current.upper()}")
        out.append(f"### Panelist {t['panelist']}\n{t['text']}")
    return "\n\n".join(out)


def build_panel_graph(llm: BaseChatModel, engine_root: Path):
    parser = llm | StrOutputParser()

    async def run_round(state: PanelState, config: RunnableConfig) -> dict:
        name, count = state["rounds"][state["round_idx"]]
        first_id = sum(n for _, n in state["rounds"][: state["round_idx"]]) + 1
        prior = _format_turns(state["turns"])
        this_round: list[dict] = []
        for i in range(count):  # sequential, like the engine's default speaking order
            so_far = _format_turns(this_round)
            speaker = prompts.LATER_SPEAKER if this_round else prompts.FIRST_SPEAKER
            user = "\n\n".join(
                p for p in (
                    state["situation"],
                    f"# Discussion so far\n{prior}" if prior else "",
                    f"# This round so far\n{so_far}" if so_far else "",
                    f"# Your task ({name} round)\n{prompts.ROUND_INSTRUCTIONS.get(name, '')}\n{speaker}",
                ) if p
            )
            text = await parser.ainvoke(
                [SystemMessage(prompts.PANEL_SYSTEM.format(n=first_id + i)), HumanMessage(user)], config=config
            )
            this_round.append({"round": name, "panelist": first_id + i, "text": text.strip()})
        return {"turns": this_round, "round_idx": state["round_idx"] + 1}

    def more_rounds(state: PanelState) -> str:
        return "round" if state["round_idx"] < len(state["rounds"]) else "synthesize"

    async def synthesize(state: PanelState, config: RunnableConfig) -> dict:
        q = state["question"]
        user = f"{state['situation']}\n\n# Full discussion\n\n{_format_turns(state['turns'])}"
        system = prompts.render_synthesis_system(engine_root, q)
        doc = await parser.ainvoke([SystemMessage(system), HumanMessage(user)], config=config)
        return {"doc": doc.strip()}

    g = StateGraph(PanelState)
    g.add_node("round", run_round)
    g.add_node("synthesize", synthesize)
    g.add_edge(START, "round")
    g.add_conditional_edges("round", more_rounds, {"round": "round", "synthesize": "synthesize"})
    g.add_edge("synthesize", END)
    return g.compile()


# ---------- driver ----------

async def run_condition(
    name: str,
    llm: BaseChatModel,
    brief: Brief,
    engine_root: Path,
    round_counts: dict[str, int],
    config: dict | None = None,
    on_doc: Callable[[DocResult], Awaitable[None] | None] | None = None,
) -> list[DocResult]:
    if name not in BASELINES:
        raise ValueError(f"unknown condition {name!r}; expected one of {BASELINES}")
    config = config or {}
    graph = build_panel_graph(llm, engine_root) if name == "plain_panel" else None
    rounds = list(round_counts.items())
    results: list[DocResult] = []
    prior: list[str] = []

    for q in brief.questions:
        situation = prompts.situation(brief, q, "\n\n".join(prior))
        start = time.monotonic()
        if name == "single":
            doc, calls = await _single(llm, situation, config)
        elif name == "self_critique":
            doc, calls = await _self_critique(llm, situation, config)
        else:
            state = await graph.ainvoke(
                {"situation": situation, "question": q, "rounds": rounds, "round_idx": 0, "turns": [], "doc": ""},
                config={**config, "recursion_limit": 4 * len(rounds) + 10},
            )
            doc, calls = state["doc"], sum(n for _, n in rounds) + 1
        result = DocResult(q.number, doc, round(time.monotonic() - start, 1), calls)
        results.append(result)
        decided = decisions_section(doc)
        if decided:
            prior.append(f"### Q{q.number}: {q.title}\n{decided}")
        if on_doc:
            maybe = on_doc(result)
            if maybe is not None:
                await maybe
    return results
