from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import SCRIPTWRITER_PROMPT

class ScriptwriterAgent(Agent):
    @property
    def name(self) -> str:
        return "ScriptwriterAgent"

    @property
    def system_prompt(self) -> str:
        return SCRIPTWRITER_PROMPT
