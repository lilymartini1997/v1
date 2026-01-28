from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import UNHINGED_HOOK_PROMPT

class UnhingedHookAgent(Agent):
    @property
    def name(self) -> str:
        return "UnhingedHookAgent"

    @property
    def system_prompt(self) -> str:
        return UNHINGED_HOOK_PROMPT
