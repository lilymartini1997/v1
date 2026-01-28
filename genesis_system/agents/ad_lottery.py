from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import AD_LOTTERY_PROMPT

class AdLotteryAgent(Agent):
    @property
    def name(self) -> str:
        return "AdLotteryAgent"

    @property
    def system_prompt(self) -> str:
        return AD_LOTTERY_PROMPT
