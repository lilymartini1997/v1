from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import REPURPOSER_PROMPT

class RepurposerAgent(Agent):
    @property
    def name(self) -> str:
        return "RepurposerAgent"

    @property
    def system_prompt(self) -> str:
        return REPURPOSER_PROMPT
