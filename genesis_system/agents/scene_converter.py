from genesis_system.core.agent_base import Agent
from genesis_system.prompts.library import SCENE_CONVERTER_PROMPT

class ScriptToSceneConverterAgent(Agent):
    @property
    def name(self) -> str:
        return "ScriptToSceneConverterAgent"

    @property
    def system_prompt(self) -> str:
        return SCENE_CONVERTER_PROMPT
