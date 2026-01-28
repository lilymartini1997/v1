from typing import Dict, Any, List
from genesis_system.core.llm_interface import LLMInterface
from genesis_system.core.state_manager import CampaignState

# Import all agents
from genesis_system.agents.intake import IntakeAgent
from genesis_system.agents.segmentation import SegmentationAgent
from genesis_system.agents.buyer_research import BuyerResearchAgent
from genesis_system.agents.voice import VoiceAgent
from genesis_system.agents.copy_block import CopyBlockExtractorAgent
from genesis_system.agents.outcome import OutcomeEngineerAgent
from genesis_system.agents.mechanism import MechanismArchitectAgent
from genesis_system.agents.belief_analyst import BeliefAnalystAgent
from genesis_system.agents.belief_alchemist import BeliefAlchemistAgent
from genesis_system.agents.insight import InsightVectorsAgent
from genesis_system.agents.ad_lottery import AdLotteryAgent
from genesis_system.agents.hook import HookEngineAgent
from genesis_system.agents.unhinged_hook import UnhingedHookAgent
from genesis_system.agents.scriptwriter import ScriptwriterAgent
from genesis_system.agents.scene_converter import ScriptToSceneConverterAgent
from genesis_system.agents.repurposer import RepurposerAgent
from genesis_system.agents.storm import STORMRetargetingAgent
from genesis_system.agents.qa import QAAgent
from genesis_system.agents.curator import CuratorAgent
from genesis_system.agents.builder import AgentBuilderAgent
from genesis_system.prompts.library import ORCHESTRATOR_PROMPT

class CampaignDirector:
    def __init__(self, llm: LLMInterface):
        self.llm = llm
        self.state = CampaignState()
        self.agents = {
            "IntakeAgent": IntakeAgent(llm),
            "SegmentationAgent": SegmentationAgent(llm),
            "BuyerResearchAgent": BuyerResearchAgent(llm),
            "VoiceAgent": VoiceAgent(llm),
            "CopyBlockExtractorAgent": CopyBlockExtractorAgent(llm),
            "OutcomeEngineerAgent": OutcomeEngineerAgent(llm),
            "MechanismArchitectAgent": MechanismArchitectAgent(llm),
            "BeliefAnalystAgent": BeliefAnalystAgent(llm),
            "BeliefAlchemistAgent": BeliefAlchemistAgent(llm),
            "InsightVectorsAgent": InsightVectorsAgent(llm),
            "AdLotteryAgent": AdLotteryAgent(llm),
            "HookEngineAgent": HookEngineAgent(llm),
            "UnhingedHookAgent": UnhingedHookAgent(llm),
            "ScriptwriterAgent": ScriptwriterAgent(llm),
            "ScriptToSceneConverterAgent": ScriptToSceneConverterAgent(llm),
            "RepurposerAgent": RepurposerAgent(llm),
            "STORMRetargetingAgent": STORMRetargetingAgent(llm),
            "QAAgent": QAAgent(llm),
            "CuratorAgent": CuratorAgent(llm),
            "AgentBuilderAgent": AgentBuilderAgent(llm),
        }

    def run_campaign(self, request_type: str, inputs: Dict[str, Any]):
        """
        Main entry point for running a campaign workflow.
        """
        print(f"Starting Campaign Director: {request_type}")
        self.state.update_inputs(inputs)

        # Inject Orchestrator logic/prompt if needed, but here we hardcode the flow
        # based on the system prompt description which says "You MUST Trigger the correct agents".
        # We simulate the Orchestrator agent's decision making by implementing the logic directly.

        if request_type == "CREATE_CAMPAIGN":
            self._run_create_campaign()
        elif request_type == "CONVERT_ASSET":
            self._run_convert_asset()
        else:
            print(f"Unknown request type: {request_type}")

        return self.state.to_json()

    def _run_create_campaign(self):
        # 1. Foundational Intelligence
        self._run_agent("IntakeAgent")
        self._run_agent("SegmentationAgent")
        self._run_agent("BuyerResearchAgent")
        self._run_agent("VoiceAgent")
        self._run_agent("CopyBlockExtractorAgent")

        # 2. Persuasion Architecture
        self._run_agent("OutcomeEngineerAgent")
        self._run_agent("MechanismArchitectAgent")
        self._run_agent("BeliefAnalystAgent")
        self._run_agent("BeliefAlchemistAgent")
        self._run_agent("InsightVectorsAgent")

        # 3. Production Outputs
        self._run_agent("AdLotteryAgent")
        self._run_agent("HookEngineAgent")
        self._run_agent("UnhingedHookAgent")
        self._run_agent("ScriptwriterAgent")

        # 4. Conversion Artifacts & Repurposing
        self._run_agent("ScriptToSceneConverterAgent")
        self._run_agent("RepurposerAgent")
        self._run_agent("STORMRetargetingAgent")

        # 5. QA & Curation
        self._run_agent("QAAgent")
        self._run_agent("CuratorAgent")

    def _run_convert_asset(self):
        # Simplified flow for asset conversion as described in the prompt
        # "If OfferBrief missing -> run IntakeAgent" - we assume we might need some context.
        # But for strictly CONVERT_ASSET per Run 2/3 examples:

        # We always want some context if possible.
        if "sales_page_text" in self.state.data["inputs"] or "sales_page_url_text_dump" in self.state.data["inputs"]:
             self._run_agent("IntakeAgent")

        # In a real system, the Orchestrator (LLM) would decide this.
        # Here we follow the dependency graph: we need Voice and Segments often.
        if not self.state.get_artifact("voice_guide"):
             self._run_agent("VoiceAgent") # Might default or use inputs

        # Run specific conversion agents
        self._run_agent("RepurposerAgent")
        self._run_agent("ScriptToSceneConverterAgent")
        self._run_agent("STORMRetargetingAgent")

    def _run_agent(self, agent_name: str):
        """
        Runs a specific agent if it hasn't been run or logic dictates.
        Passes the ENTIRE current artifact state + inputs to the agent.
        """
        print(f"  -> Running {agent_name}...")
        agent = self.agents[agent_name]

        # Prepare inputs: Combine original inputs + all artifacts produced so far
        # This gives the agent full context.
        current_context = self.state.data["inputs"].copy()
        current_context.update(self.state.get_all_artifacts())

        output = agent.run(current_context)

        # Update state
        self.state.add_agent_output(agent_name, output)
        print(f"  <- {agent_name} completed.")
