"""Blind pairwise judging.

Each pair of docs is judged twice with the positions swapped. A side wins a criterion
only if it wins in both orders; anything else counts as a tie. This cancels the judge's
position bias instead of averaging it in, and the report shows how often the two orders
agreed.
"""

from __future__ import annotations

import asyncio
from typing import Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from . import prompts

CRITERIA = ("risk_discovery", "decision_quality", "actionability", "alternatives", "signal_to_noise", "overall")
Choice = Literal["A", "B", "tie"]

# Comparisons run by default: what the engine adds overall, over good prompting, over the same
# structure without personas, and what the structure alone adds over one call.
DEFAULT_PAIRS = (
    ("engine", "single"),
    ("engine", "self_critique"),
    ("engine", "plain_panel"),
    ("plain_panel", "single"),
)


class Verdict(BaseModel):
    reasoning: str = Field(description="Brief comparison of the two documents before deciding.")
    risk_discovery: Choice
    decision_quality: Choice
    actionability: Choice
    alternatives: Choice
    signal_to_noise: Choice
    overall: Choice
    confidence: Literal["low", "medium", "high"]


def combine(first: dict, second: dict) -> dict[str, str]:
    """first: x shown as A. second: y shown as A. Returns winner per criterion: x, y or tie."""
    out = {}
    for c in CRITERIA:
        a = {"A": "x", "B": "y", "tie": "tie"}[first[c]]
        b = {"A": "y", "B": "x", "tie": "tie"}[second[c]]
        out[c] = a if a == b else "tie"
    return out


async def judge_once(llm: BaseChatModel, situation: str, doc_a: str, doc_b: str, config: dict) -> dict:
    # json_schema, not forced tool calling: newer Claude models do not support forced tool use.
    structured = llm.with_structured_output(Verdict, method="json_schema")
    verdict = await structured.ainvoke(
        [SystemMessage(prompts.JUDGE_SYSTEM), HumanMessage(prompts.judge_user(situation, doc_a, doc_b))],
        config=config,
    )
    return verdict.model_dump() if isinstance(verdict, BaseModel) else dict(verdict)


async def judge_pair(
    llm: BaseChatModel, situation: str, x: str, doc_x: str, y: str, doc_y: str, config: dict | None = None
) -> dict:
    config = config or {}
    first, second = await asyncio.gather(
        judge_once(llm, situation, doc_x, doc_y, config),
        judge_once(llm, situation, doc_y, doc_x, config),
    )
    outcome = combine(first, second)
    first_overall = {"A": "x", "B": "y", "tie": "tie"}[first["overall"]]
    second_overall = {"A": "y", "B": "x", "tie": "tie"}[second["overall"]]
    return {
        "x": x,
        "y": y,
        "outcome": outcome,
        "orders_agree": first_overall == second_overall,
        "x_first": first,
        "y_first": second,
    }
