from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import BELIEF_ANALYST_PROMPT

class BeliefAnalystAgent(Agent):
    @property
    def name(self) -> str:
        return "BeliefAnalystAgent"

    @property
    def system_prompt(self) -> str:
        return BELIEF_ANALYST_PROMPT
