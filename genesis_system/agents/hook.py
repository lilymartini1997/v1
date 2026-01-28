from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import HOOK_ENGINE_PROMPT

class HookEngineAgent(Agent):
    @property
    def name(self) -> str:
        return "HookEngineAgent"

    @property
    def system_prompt(self) -> str:
        return HOOK_ENGINE_PROMPT
