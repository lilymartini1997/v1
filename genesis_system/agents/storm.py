from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import STORM_RETARGETING_PROMPT

class STORMRetargetingAgent(Agent):
    @property
    def name(self) -> str:
        return "STORMRetargetingAgent"

    @property
    def system_prompt(self) -> str:
        return STORM_RETARGETING_PROMPT
