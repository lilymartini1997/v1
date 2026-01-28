import json
import copy
from typing import Dict, Any

class CampaignState:
    def __init__(self):
        self.data = {
            "version": 1,
            "inputs": {}, # Initial user inputs
            "artifacts": {}, # Structured outputs from agents
            "agent_outputs": [] # Log of all full agent outputs
        }

    def update_inputs(self, inputs: Dict[str, Any]):
        """Updates the initial inputs."""
        self.data["inputs"].update(inputs)
        self.increment_version()

    def add_agent_output(self, agent_name: str, output: Dict[str, Any]):
        """Records a full agent output and merges known keys into artifacts."""
        entry = {
            "agent": agent_name,
            "timestamp": "TODO", # In a real system, add timestamp
            "output": copy.deepcopy(output)
        }
        self.data["agent_outputs"].append(entry)

        # Merge outputs into artifacts for easy access by other agents
        if "outputs" in output:
            for key, value in output["outputs"].items():
                self.data["artifacts"][key] = value

        self.increment_version()

    def get_artifact(self, key: str, default=None):
        return self.data["artifacts"].get(key, default)

    def get_all_artifacts(self):
        return self.data["artifacts"]

    def increment_version(self):
        self.data["version"] += 1

    def to_json(self):
        return self.data
