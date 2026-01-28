from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import MECHANISM_ARCHITECT_PROMPT

class MechanismArchitectAgent(Agent):
    @property
    def name(self) -> str:
        return "MechanismArchitectAgent"

    @property
    def system_prompt(self) -> str:
        return MECHANISM_ARCHITECT_PROMPT
