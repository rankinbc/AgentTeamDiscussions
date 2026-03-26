"""Conversation state management — single source of truth."""

from dataclasses import dataclass, field

from agentteam.types import AgentConfig
from agentteam.prompts.builder import build_perspective_reminder, build_system_prompt


@dataclass
class Message:
    role: str        # "user" or "assistant"
    agent_name: str  # which agent (or "user")
    content: str


@dataclass
class Conversation:
    """Single-agent conversation with history truncation."""
    agent: AgentConfig
    system_prompt: str = field(init=False)
    history: list[Message] = field(default_factory=list)
    turn_count: int = 0
    keep_first: int = 2
    keep_last: int = 10
    truncation_threshold: int = 14

    def __post_init__(self):
        self.system_prompt = build_system_prompt(self.agent)

    def add_user_message(self, content: str):
        self.history.append(Message(role="user", agent_name="user", content=content))

    def add_assistant_message(self, content: str):
        self.history.append(Message(role="assistant", agent_name=self.agent.name, content=content))
        self.turn_count += 1

    def _truncated_history(self) -> list[Message]:
        if len(self.history) <= self.truncation_threshold:
            return list(self.history)
        return self.history[:self.keep_first] + self.history[-self.keep_last:]

    def build_prompt_payload(self, current_message: str) -> str:
        parts = []
        truncated = self._truncated_history()
        if truncated:
            parts.append("=== Conversation History ===")
            for msg in truncated:
                label = msg.agent_name if msg.role == "assistant" else "User"
                parts.append(f"\n[{label}]: {msg.content}")
            parts.append("\n=== End History ===\n")
        parts.append(build_perspective_reminder(self.agent))
        parts.append(f"\n[User]: {current_message}")
        return "\n".join(parts)

    def should_trigger_uncomfortable_idea(self) -> bool:
        quota = self.agent.anti_slop.uncomfortable_idea_quota
        if quota <= 0:
            return False
        interval = max(5, 10 - quota)
        return self.turn_count > 0 and self.turn_count % interval == 0


@dataclass
class MultiConversation:
    """Multi-agent discussion state with shared history."""
    agents: dict[str, AgentConfig]
    system_prompts: dict[str, str] = field(default_factory=dict)
    history: list[Message] = field(default_factory=list)
    round_count: int = 0
    keep_first: int = 3
    keep_last: int = 15
    truncation_threshold: int = 20

    def __post_init__(self):
        for key, agent in self.agents.items():
            self.system_prompts[key] = build_system_prompt(agent)

    def add_user_message(self, content: str):
        self.history.append(Message(role="user", agent_name="user", content=content))

    def add_agent_message(self, agent_key: str, content: str):
        self.history.append(Message(role="assistant", agent_name=self.agents[agent_key].name, content=content))

    def _truncated_history(self) -> list[Message]:
        if len(self.history) <= self.truncation_threshold:
            return list(self.history)
        return self.history[:self.keep_first] + self.history[-self.keep_last:]

    def build_agent_payload(self, agent_key: str, context: str = "") -> str:
        agent = self.agents[agent_key]
        parts = []
        truncated = self._truncated_history()
        if truncated:
            parts.append("=== Discussion So Far ===")
            for msg in truncated:
                label = msg.agent_name if msg.role == "assistant" else "User"
                parts.append(f"\n[{label}]: {msg.content}")
            parts.append("\n=== End Discussion ===\n")
        parts.append(build_perspective_reminder(agent))
        if context:
            parts.append(f"\n{context}")
        parts.append(f"\nNow respond as {agent.name}. Stay in character. Engage with what others have said.")
        return "\n".join(parts)
