import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMInterface(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, agent_name: str) -> Dict[str, Any]:
        """
        Generates a response from the LLM.
        Expected to return a dictionary parsed from JSON.
        """
        pass

class MockLLM(LLMInterface):
    def generate(self, system_prompt: str, user_prompt: str, agent_name: str) -> Dict[str, Any]:
        """
        Returns a mock JSON response based on the agent name.
        """
        print(f"--- MockLLM: Generating response for {agent_name} ---")

        # Base envelope
        response = {
            "agent": agent_name,
            "version": "1.0",
            "inputs_used": {"mock": "inputs"},
            "assumptions": ["Mock assumption"],
            "questions_for_user": [],
            "confidence": 0.9,
            "outputs": {},
            "next_recommended_agents": []
        }

        # specific mock outputs based on agent_name to satisfy downstream dependencies
        if agent_name == "IntakeAgent":
            response["outputs"]["offer_brief"] = {
                "offer_name": "Mock Offer",
                "category": "Marketing",
                "target_market": "Business Owners",
                "main_promise": "Make more money",
                "mechanism_claim": "AI Automation",
                "price": "$997",
                "bonuses": ["Bonus 1"],
                "guarantee": "30 days",
                "delivery": "Digital Course",
                "proof_assets": {"present": ["Testimonial"], "missing": []},
                "objection_handling": [],
                "compliance_sensitive_claims": []
            }
        elif agent_name == "SegmentationAgent":
            response["outputs"]["segments"] = [
                {
                    "segment_name": "Mock Segment 1",
                    "core_desire": "Growth",
                    "key_constraints": [],
                    "awareness_notes": "Problem Aware",
                    "demographics": {},
                    "psychographics": [],
                    "winning_angles": [],
                    "best_formats": ["email"]
                }
            ]
        elif agent_name == "BuyerResearchAgent":
            response["outputs"]["buyer_profiles"] = {
                "general": {"identity": "General Buyer"},
                "by_segment": {"Mock Segment 1": {"identity": "Segment Buyer"}}
            }
        elif agent_name == "VoiceAgent":
            response["outputs"]["voice_guide"] = {
                "voice_archetype": "Sage",
                "tone": ["professional"],
                "reading_level": "simple"
            }
        elif agent_name == "CopyBlockExtractorAgent":
             response["outputs"]["copy_block_library"] = {
                "pain": [], "promise": [], "proof": [], "constraints": [], "curiosity": []
            }

        return response

class OpenAILLM(LLMInterface):
    def __init__(self, api_key: str = None, model: str = "gpt-4-turbo"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        if not self.api_key:
            # We don't raise error immediately to allow instantiation for help/setup
            # but generate will fail.
            pass

    def generate(self, system_prompt: str, user_prompt: str, agent_name: str) -> Dict[str, Any]:
        if not self.api_key:
             raise ValueError("OpenAI API key is not set. Please set OPENAI_API_KEY environment variable.")

        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package is not installed. Please install it with `pip install openai`.")

        client = OpenAI(api_key=self.api_key)

        print(f"--- OpenAILLM: Generating response for {agent_name} ---")

        try:
            # We request JSON object to ensure parsing
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            raise e
