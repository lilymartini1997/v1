import json
from abc import ABC, abstractmethod
from typing import Dict, Any
from .llm_interface import LLMInterface
from genesis_system.prompts.library import SHARED_CONVENTIONS

class Agent(ABC):
    def __init__(self, llm: LLMInterface):
        self.llm = llm

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the agent."""
        pass

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The specific system prompt for this agent."""
        pass

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the agent task.
        Constructs the full system prompt and user prompt (inputs),
        calls the LLM, and returns the parsed JSON.
        """
        full_system_prompt = f"{SHARED_CONVENTIONS}\n\n{self.system_prompt}"

        # Serialize inputs to JSON for the user prompt
        user_prompt = f"Here are your inputs for this task:\n{json.dumps(inputs, indent=2, default=str)}"

        response = self.llm.generate(
            system_prompt=full_system_prompt,
            user_prompt=user_prompt,
            agent_name=self.name
        )

        return response
