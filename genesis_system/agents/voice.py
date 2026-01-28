from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import VOICE_PROMPT

class VoiceAgent(Agent):
    @property
    def name(self) -> str:
        return "VoiceAgent"

    @property
    def system_prompt(self) -> str:
        return VOICE_PROMPT
