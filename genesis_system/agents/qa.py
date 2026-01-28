from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import QA_PROMPT

class QAAgent(Agent):
    @property
    def name(self) -> str:
        return "QAAgent"

    @property
    def system_prompt(self) -> str:
        return QA_PROMPT
