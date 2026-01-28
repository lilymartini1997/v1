from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import INTAKE_PROMPT

class IntakeAgent(Agent):
    @property
    def name(self) -> str:
        return "IntakeAgent"

    @property
    def system_prompt(self) -> str:
        return INTAKE_PROMPT
