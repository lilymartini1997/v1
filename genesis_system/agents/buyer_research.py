from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import BUYER_RESEARCH_PROMPT

class BuyerResearchAgent(Agent):
    @property
    def name(self) -> str:
        return "BuyerResearchAgent"

    @property
    def system_prompt(self) -> str:
        return BUYER_RESEARCH_PROMPT
