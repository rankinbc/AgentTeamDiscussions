"""Rolling synthesis engine -- tracks consensus, mood, and topic exhaustion during live conversations.

Runs a background LLM call every N turns to produce a structured snapshot of where the conversation
stands. Used for:
  1. Live UI display (consensus panel)
  2. Topic exhaustion detection (should we move to the next question?)
  3. Accumulated snapshots feed the final Morning Brief
  4. Future: minority pressure injection into agent prompts
"""

import asyncio
import json
import re
from dataclasses import dataclass, field

from claude_runner import run_claude_async


@dataclass
class ConversationSnapshot:
    """Point-in-time summary of conversation state."""
    turn: int
    consensus: list[str]           # Things the group agrees on
    disagreements: list[str]       # Active unresolved disagreements
    ideas_alive: list[str]         # Ideas still being discussed (not killed)
    ideas_killed: list[str]        # Ideas that were challenged and dropped
    mood: str                      # e.g. "heated", "converging", "circular", "productive"
    exhaustion: str                # "low", "medium", "high" -- is this topic played out?
    top_insight: str               # Single most interesting thing said in this chunk
    raw: str = ""                  # Raw LLM output for debugging


SYNTHESIS_PROMPT = """You are a conversation analyst watching a live group discussion.

Analyze the recent chunk of conversation and produce a JSON object with these exact fields:

{
  "consensus": ["list of things the group now agrees on"],
  "disagreements": ["list of active unresolved disagreements -- who vs who on what"],
  "ideas_alive": ["ideas still being actively discussed"],
  "ideas_killed": ["ideas that were proposed but challenged and dropped"],
  "mood": "one word: heated | converging | circular | productive | scattered | stale",
  "exhaustion": "low | medium | high -- is this topic still generating new ideas or going in circles?",
  "top_insight": "the single most interesting or non-obvious point made in this chunk"
}

Rules:
- Be specific. "They agree on X" not "there is some agreement."
- For disagreements, name the agents involved.
- "exhaustion: high" means the topic is spent -- agents are repeating, agreeing, or just nitpicking details.
- "exhaustion: low" means genuinely new ideas are still appearing.
- Output ONLY the JSON object. No markdown, no explanation, no code fences."""


FINAL_SYNTHESIS_PROMPT = """You are producing a structured summary of a completed group discussion.

You have a series of rolling snapshots taken during the conversation, plus the full transcript.
Produce a structured document covering:

## Decisions Made
What the group agreed on. Be specific -- "decided X because Y" not "discussed X."

## Unresolved Disagreements
What they fought about and never resolved. Name the agents on each side. These are the real
design decisions the human needs to make.

## Key Ideas (Survived Challenge)
Ideas that were proposed, challenged, and survived. These are the strongest ideas.

## Ideas Killed
Ideas that were proposed but successfully attacked. Say who killed them and why.

## Surprising Insights
Things a human product designer probably wouldn't have thought of.

## Recommended Next Questions
Based on what's unresolved, what should the NEXT conversation focus on? Give 2-3 specific
questions that would advance the spec.

Be concise. Use bullet points. No fluff. Every line should be something the human can act on."""


class LiveSynthesizer:
    """Runs periodic synthesis during a conversation and produces final output."""

    def __init__(self, question: str, synthesis_interval: int = 5, model: str = None):
        self.question = question
        self.interval = synthesis_interval
        self.model = model  # Use same model as conversation (None = CLI default)
        self.snapshots: list[ConversationSnapshot] = []
        self._last_synthesis_turn = 0

    async def maybe_synthesize(self, history: list[dict], current_turn: int) -> ConversationSnapshot | None:
        """Check if it's time to synthesize, and do it if so. Returns snapshot or None."""
        if current_turn - self._last_synthesis_turn < self.interval:
            return None
        if len(history) < 3:
            return None

        self._last_synthesis_turn = current_turn

        # Get the chunk since last synthesis
        chunk_start = 0
        if self.snapshots:
            # Find messages after last snapshot's turn
            last_turn = self.snapshots[-1].turn
            chunk_start = next((i for i, h in enumerate(history) if h["turn"] > last_turn), 0)

        chunk = history[chunk_start:]
        if not chunk:
            return None

        # Build the chunk text
        chunk_text = f"Topic: {self.question}\n\n"
        for msg in chunk:
            chunk_text += f"[{msg['name']}]: {msg['text']}\n\n"

        # Add prior context if we have snapshots
        if self.snapshots:
            last = self.snapshots[-1]
            chunk_text += f"\n[Prior state: consensus on {len(last.consensus)} points, {len(last.disagreements)} active disagreements, mood was '{last.mood}', exhaustion was '{last.exhaustion}']\n"

        result = await run_claude_async(SYNTHESIS_PROMPT, chunk_text, timeout=30, model=self.model)

        snapshot = self._parse_snapshot(result, current_turn)
        self.snapshots.append(snapshot)
        return snapshot

    def _parse_snapshot(self, raw: str, turn: int) -> ConversationSnapshot:
        """Parse LLM output into a ConversationSnapshot."""
        try:
            # Strip markdown code fences if present
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```\w*\n?", "", cleaned)
                cleaned = re.sub(r"\n?```$", "", cleaned)

            data = json.loads(cleaned)
            return ConversationSnapshot(
                turn=turn,
                consensus=data.get("consensus", []),
                disagreements=data.get("disagreements", []),
                ideas_alive=data.get("ideas_alive", []),
                ideas_killed=data.get("ideas_killed", []),
                mood=data.get("mood", "unknown"),
                exhaustion=data.get("exhaustion", "unknown"),
                top_insight=data.get("top_insight", ""),
                raw=raw,
            )
        except (json.JSONDecodeError, AttributeError) as e:
            import sys
            print(f"[Synthesis parse error: {e}] Raw: {raw[:200]}", file=sys.stderr)
            return ConversationSnapshot(
                turn=turn,
                consensus=[], disagreements=[], ideas_alive=[], ideas_killed=[],
                mood="unknown", exhaustion="unknown", top_insight=f"(parse error: {str(e)[:50]})",
                raw=raw,
            )

    def is_topic_exhausted(self) -> bool:
        """Check if the current topic is exhausted based on recent snapshots."""
        if not self.snapshots:
            return False
        last = self.snapshots[-1]
        if last.exhaustion == "high":
            return True
        # Also check if last 2 snapshots both say medium+
        if len(self.snapshots) >= 2:
            prev = self.snapshots[-2]
            if prev.exhaustion in ("medium", "high") and last.exhaustion in ("medium", "high"):
                return True
        return False

    def get_latest(self) -> ConversationSnapshot | None:
        """Get the most recent snapshot."""
        return self.snapshots[-1] if self.snapshots else None

    async def final_synthesis(self, history: list[dict], model: str = None) -> str:
        """Produce the final structured summary after conversation ends."""
        use_model = model or "sonnet"  # Use a better model for final synthesis

        # Build full context: snapshots + transcript
        context = f"# Discussion Topic\n\n{self.question}\n\n"

        if self.snapshots:
            context += "# Rolling Snapshots (taken during conversation)\n\n"
            for s in self.snapshots:
                context += f"## Turn {s.turn} snapshot\n"
                context += f"- Mood: {s.mood} | Exhaustion: {s.exhaustion}\n"
                if s.consensus:
                    context += f"- Consensus: {'; '.join(s.consensus)}\n"
                if s.disagreements:
                    context += f"- Disagreements: {'; '.join(s.disagreements)}\n"
                if s.ideas_alive:
                    context += f"- Ideas alive: {'; '.join(s.ideas_alive)}\n"
                if s.ideas_killed:
                    context += f"- Ideas killed: {'; '.join(s.ideas_killed)}\n"
                if s.top_insight:
                    context += f"- Top insight: {s.top_insight}\n"
                context += "\n"

        context += "# Full Transcript\n\n"
        for msg in history:
            context += f"**{msg['name']}** (turn {msg['turn']}):\n{msg['text']}\n\n"

        return await run_claude_async(FINAL_SYNTHESIS_PROMPT, context, timeout=120, model=use_model)

    async def comparison_synthesis(self, team_a_summary: str, team_b_summary: str,
                                    team_a_name: str, team_b_name: str,
                                    model: str = None) -> str:
        """Compare two team discussions on the same topic."""
        use_model = model or "sonnet"

        prompt = f"""You have two separate team discussions on the same product question.

# {team_a_name} Discussion Summary
{team_a_summary}

# {team_b_name} Discussion Summary
{team_b_summary}

Produce a comparison document:

## Where Teams Agree
Points both teams converged on independently. These are high-confidence decisions.

## Where Teams Diverge
Points where the teams reached different conclusions. These are the critical design decisions.
Say what each team thinks and why.

## Insights Unique to {team_a_name}
Ideas only the first team surfaced.

## Insights Unique to {team_b_name}
Ideas only the second team surfaced.

## Combined Spec Recommendations
Merge the best of both into actionable spec items. Prioritize ideas that survived challenge
from EITHER team.

## Open Questions
What neither team resolved. These need human judgment.

Be specific and actionable. Every line should help someone write a product spec."""

        return await run_claude_async(
            "You are a product strategist synthesizing insights from two independent team discussions.",
            prompt, timeout=120, model=use_model
        )
