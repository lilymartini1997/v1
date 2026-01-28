from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import INSIGHT_VECTORS_PROMPT

class InsightVectorsAgent(Agent):
    @property
    def name(self) -> str:
        return "InsightVectorsAgent"

    @property
    def system_prompt(self) -> str:
        return INSIGHT_VECTORS_PROMPT
