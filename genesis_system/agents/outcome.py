from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import OUTCOME_ENGINEER_PROMPT

class OutcomeEngineerAgent(Agent):
    @property
    def name(self) -> str:
        return "OutcomeEngineerAgent"

    @property
    def system_prompt(self) -> str:
        return OUTCOME_ENGINEER_PROMPT
