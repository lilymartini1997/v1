from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import CURATOR_PROMPT

class CuratorAgent(Agent):
    @property
    def name(self) -> str:
        return "CuratorAgent"

    @property
    def system_prompt(self) -> str:
        return CURATOR_PROMPT
