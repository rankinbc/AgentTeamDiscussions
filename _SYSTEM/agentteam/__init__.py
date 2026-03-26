"""agentteam — Multi-agent AI discussion framework.

Install with: pip install -e .  (from _SYSTEM/)

Key modules:
    agentteam.types        — Agent config Pydantic models
    agentteam.runner       — Claude CLI subprocess wrapper
    agentteam.config       — YAML config + Jinja2 template loading
    agentteam.agents       — Agent/team YAML loading
    agentteam.prompts      — System prompt assembly
    agentteam.conversation — Conversation state management
    agentteam.synthesis    — Rolling synthesis engine
    agentteam.session      — Crash-safe persistence + decision ledger
    agentteam.brief        — Discussion brief parsing
"""
