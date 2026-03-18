"""Conversation state management."""

from dataclasses import dataclass, field

from models import AgentConfig
from prompt_builder import build_perspective_reminder, build_system_prompt


@dataclass
class Message:
    role: str  # "user" or "assistant"
    agent_name: str  # which agent (or "user")
    content: str


@dataclass
class Conversation:
    agent: AgentConfig
    system_prompt: str = field(init=False)
    history: list[Message] = field(default_factory=list)
    turn_count: int = 0

    def __post_init__(self):
        self.system_prompt = build_system_prompt(self.agent)

    def add_user_message(self, content: str):
        self.history.append(Message(role="user", agent_name="user", content=content))

    def add_assistant_message(self, content: str):
        self.history.append(Message(role="assistant", agent_name=self.agent.name, content=content))
        self.turn_count += 1

    def _truncated_history(self) -> list[Message]:
        """Keep first 2 + last 10 messages for long conversations."""
        if len(self.history) <= 14:
            return list(self.history)
        return self.history[:2] + self.history[-10:]

    def build_prompt_payload(self, current_message: str) -> str:
        """Build the full payload to send via stdin.

        Includes truncated history, perspective reminder, and current message.
        """
        parts = []

        # History
        truncated = self._truncated_history()
        if truncated:
            parts.append("=== Conversation History ===")
            for msg in truncated:
                label = msg.agent_name if msg.role == "assistant" else "User"
                parts.append(f"\n[{label}]: {msg.content}")
            parts.append("\n=== End History ===\n")

        # Perspective reminder (fights drift)
        reminder = build_perspective_reminder(self.agent)
        parts.append(reminder)

        # Current message
        parts.append(f"\n[User]: {current_message}")

        return "\n".join(parts)

    def should_trigger_uncomfortable_idea(self) -> bool:
        """Check if it's time for an uncomfortable idea based on quota."""
        quota = self.agent.anti_slop.uncomfortable_idea_quota
        if quota <= 0:
            return False
        interval = max(5, 10 - quota)
        return self.turn_count > 0 and self.turn_count % interval == 0


@dataclass
class MultiConversation:
    """Manages conversation state for multiple agents discussing a topic."""

    agents: dict[str, AgentConfig]
    system_prompts: dict[str, str] = field(default_factory=dict)
    history: list[Message] = field(default_factory=list)
    round_count: int = 0

    def __post_init__(self):
        for key, agent in self.agents.items():
            self.system_prompts[key] = build_system_prompt(agent)

    def add_user_message(self, content: str):
        self.history.append(Message(role="user", agent_name="user", content=content))

    def add_agent_message(self, agent_key: str, content: str):
        agent_name = self.agents[agent_key].name
        self.history.append(Message(role="assistant", agent_name=agent_name, content=content))

    def _truncated_history(self) -> list[Message]:
        if len(self.history) <= 20:
            return list(self.history)
        return self.history[:3] + self.history[-15:]

    def build_agent_payload(self, agent_key: str, context: str = "") -> str:
        """Build payload for a specific agent, including conversation history."""
        agent = self.agents[agent_key]
        parts = []

        truncated = self._truncated_history()
        if truncated:
            parts.append("=== Discussion So Far ===")
            for msg in truncated:
                label = msg.agent_name if msg.role == "assistant" else "User"
                parts.append(f"\n[{label}]: {msg.content}")
            parts.append("\n=== End Discussion ===\n")

        reminder = build_perspective_reminder(agent)
        parts.append(reminder)

        if context:
            parts.append(f"\n{context}")

        parts.append(
            f"\nNow respond as {agent.name}. Stay in character. "
            f"Engage with what others have said -- agree, disagree, build, or challenge."
        )

        return "\n".join(parts)
