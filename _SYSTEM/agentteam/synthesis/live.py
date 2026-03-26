"""Rolling synthesis — tracks consensus, mood, and topic exhaustion."""

import asyncio
import json
import re
from dataclasses import dataclass, field

from agentteam.runner.claude import run_claude_async


@dataclass
class ConversationSnapshot:
    turn: int
    consensus: list[str]
    disagreements: list[str]
    ideas_alive: list[str]
    ideas_killed: list[str]
    mood: str
    exhaustion: str
    top_insight: str
    raw: str = ""


_ROLLING_PROMPT = """You are a conversation analyst watching a live group discussion.

Analyze the recent chunk and produce JSON with these exact fields:
{"consensus": [...], "disagreements": [...], "ideas_alive": [...], "ideas_killed": [...],
 "mood": "heated|converging|circular|productive|scattered|stale",
 "exhaustion": "low|medium|high", "top_insight": "..."}

Rules: Be specific. Name agents in disagreements. exhaustion:high = topic is spent.
Output ONLY the JSON object. No markdown, no explanation."""

_FINAL_PROMPT = """Produce a structured summary of a completed group discussion.

## Decisions Made
## Unresolved Disagreements
## Key Ideas (Survived Challenge)
## Ideas Killed
## Surprising Insights
## Recommended Next Questions

Be concise. Use bullet points. Every line should help someone write a product spec."""


class LiveSynthesizer:
    def __init__(self, question: str, synthesis_interval: int = 5, model: str = None,
                 synthesis_prompt: str = None, final_synthesis_prompt: str = None):
        self.question = question
        self.interval = synthesis_interval
        self.model = model
        self.synthesis_prompt = synthesis_prompt or _ROLLING_PROMPT
        self.final_synthesis_prompt = final_synthesis_prompt or _FINAL_PROMPT
        self.snapshots: list[ConversationSnapshot] = []
        self._last_synthesis_turn = 0

    async def maybe_synthesize(self, history: list[dict], current_turn: int) -> ConversationSnapshot | None:
        if current_turn - self._last_synthesis_turn < self.interval or len(history) < 3:
            return None
        self._last_synthesis_turn = current_turn
        chunk_start = 0
        if self.snapshots:
            last_turn = self.snapshots[-1].turn
            chunk_start = next((i for i, h in enumerate(history) if h["turn"] > last_turn), 0)
        chunk = history[chunk_start:]
        if not chunk:
            return None
        chunk_text = f"Topic: {self.question}\n\n" + "".join(f"[{m['name']}]: {m['text']}\n\n" for m in chunk)
        if self.snapshots:
            last = self.snapshots[-1]
            chunk_text += f"\n[Prior: {len(last.consensus)} consensus points, mood '{last.mood}', exhaustion '{last.exhaustion}']\n"
        result = await run_claude_async(self.synthesis_prompt, chunk_text, timeout=30)
        snapshot = self._parse_snapshot(result, current_turn)
        self.snapshots.append(snapshot)
        return snapshot

    def _parse_snapshot(self, raw: str, turn: int) -> ConversationSnapshot:
        try:
            cleaned = re.sub(r"^```\w*\n?", "", raw.strip())
            cleaned = re.sub(r"\n?```$", "", cleaned)
            data = json.loads(cleaned)
            return ConversationSnapshot(turn=turn, consensus=data.get("consensus", []),
                disagreements=data.get("disagreements", []), ideas_alive=data.get("ideas_alive", []),
                ideas_killed=data.get("ideas_killed", []), mood=data.get("mood", "unknown"),
                exhaustion=data.get("exhaustion", "unknown"), top_insight=data.get("top_insight", ""), raw=raw)
        except Exception as e:
            return ConversationSnapshot(turn=turn, consensus=[], disagreements=[], ideas_alive=[],
                ideas_killed=[], mood="unknown", exhaustion="unknown",
                top_insight=f"(parse error: {str(e)[:50]})", raw=raw)

    def is_topic_exhausted(self) -> bool:
        if not self.snapshots:
            return False
        last = self.snapshots[-1]
        if last.exhaustion == "high":
            return True
        if len(self.snapshots) >= 2:
            prev = self.snapshots[-2]
            if prev.exhaustion in ("medium", "high") and last.exhaustion in ("medium", "high"):
                return True
        return False

    def get_latest(self) -> ConversationSnapshot | None:
        return self.snapshots[-1] if self.snapshots else None

    async def final_synthesis(self, history: list[dict], model: str = None) -> str:
        context = f"# Discussion Topic\n\n{self.question}\n\n"
        if self.snapshots:
            context += "# Rolling Snapshots\n\n"
            for s in self.snapshots:
                context += f"## Turn {s.turn}\nMood: {s.mood} | Exhaustion: {s.exhaustion}\n"
                if s.consensus:
                    context += f"Consensus: {'; '.join(s.consensus)}\n"
                if s.top_insight:
                    context += f"Top insight: {s.top_insight}\n"
                context += "\n"
        context += "# Full Transcript\n\n" + "".join(f"**{m['name']}** (turn {m['turn']}):\n{m['text']}\n\n" for m in history)
        return await run_claude_async(self.final_synthesis_prompt, context, timeout=120)
