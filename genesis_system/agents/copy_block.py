from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import COPY_BLOCK_PROMPT

class CopyBlockExtractorAgent(Agent):
    @property
    def name(self) -> str:
        return "CopyBlockExtractorAgent"

    @property
    def system_prompt(self) -> str:
        return COPY_BLOCK_PROMPT
