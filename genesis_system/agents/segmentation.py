from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import SEGMENTATION_PROMPT

class SegmentationAgent(Agent):
    @property
    def name(self) -> str:
        return "SegmentationAgent"

    @property
    def system_prompt(self) -> str:
        return SEGMENTATION_PROMPT
