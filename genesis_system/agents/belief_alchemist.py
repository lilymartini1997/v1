from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import BELIEF_ALCHEMIST_PROMPT

class BeliefAlchemistAgent(Agent):
    @property
    def name(self) -> str:
        return "BeliefAlchemistAgent"

    @property
    def system_prompt(self) -> str:
        return BELIEF_ALCHEMIST_PROMPT
