from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import AGENT_BUILDER_PROMPT

class AgentBuilderAgent(Agent):
    @property
    def name(self) -> str:
        return "AgentBuilderAgent"

    @property
    def system_prompt(self) -> str:
        return AGENT_BUILDER_PROMPT
