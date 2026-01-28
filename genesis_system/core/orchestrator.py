from typing import Dict, Any, List
from genesis_system.core.llm_interface import LLMInterface
from genesis_system.core.state_manager import CampaignState
from genesis_system.core.utils import fetch_text_from_url

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

        # PRE-PROCESSING: URL Fetching
        if "sales_page_url" in inputs:
            url = inputs["sales_page_url"]
            # Check if text is missing or empty
            has_text = "sales_page_text" in inputs and inputs["sales_page_text"]
            has_dump = "sales_page_url_text_dump" in inputs and inputs["sales_page_url_text_dump"]

            if not (has_text or has_dump):
                print(f"  -> Fetching content from {url}...")
                fetched_text = fetch_text_from_url(url)
                if fetched_text:
                    print(f"  -> Successfully fetched {len(fetched_text)} characters.")
                    inputs["sales_page_url_text_dump"] = fetched_text
                else:
                    print("  -> Failed to fetch text. Proceeding without it (Agent may hallucinate or rely on market descriptor).")

        self.state.update_inputs(inputs)

        if request_type == "CREATE_CAMPAIGN":
            self._run_create_campaign()
        elif request_type == "CONVERT_ASSET":
            self._run_convert_asset()
        elif request_type == "BUILD_AGENT":
            self._run_build_agent()
        else:
            print(f"Unknown request type: {request_type}")

        return self.state.to_json()

    def _run_build_agent(self):
        print("  -> Running Bot Builder Workflow")
        self._run_agent("AgentBuilderAgent")

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

        # QA REVISION LOOP
        qa_report = self.state.get_artifact("qa_report")
        if qa_report and qa_report.get("revision_requests"):
            print("  !! QA Agent requested revisions. Re-running Scriptwriter & Repurposer.")
            # In a real system, we would extract the specific instructions and pass them as new inputs.
            # Here we simulate the loop by re-running the agents.
            self._run_agent("ScriptwriterAgent")
            self._run_agent("RepurposerAgent")
            self._run_agent("QAAgent") # Re-verify

        self._run_agent("CuratorAgent")

        # CURATOR DIVERSITY LOOP
        curator_report = self.state.get_artifact("curated")
        if curator_report and curator_report.get("next_generation_instructions"):
            print("  !! Curator Agent requested more variants. Re-running Lottery & Hook Engine.")
            self._run_agent("AdLotteryAgent")
            self._run_agent("HookEngineAgent")
            self._run_agent("ScriptwriterAgent")
            self._run_agent("CuratorAgent") # Re-curate

    def _run_convert_asset(self):
        inputs = self.state.data["inputs"]
        source_type = inputs.get("source_asset_type", "")

        # Special handling for VSL Transcript (Run 3)
        # Goal: "system returns hooks + short scripts + retargeting blueprint"
        if source_type == "vsl_transcript" or "vsl_transcript" in inputs:
            print("  -> Detected VSL Conversion Workflow (Run 3)")
            if not self.state.get_artifact("offer_brief"):
                self._run_agent("IntakeAgent")

            # Need persuasion architecture to break down the VSL logic
            self._run_agent("OutcomeEngineerAgent")
            self._run_agent("MechanismArchitectAgent")
            self._run_agent("BeliefAnalystAgent")
            self._run_agent("BeliefAlchemistAgent")

            # Generate new assets
            self._run_agent("HookEngineAgent")
            self._run_agent("ScriptwriterAgent")
            self._run_agent("STORMRetargetingAgent")
            return

        # Standard Convert Asset (Run 2)
        if "sales_page_text" in inputs or "sales_page_url_text_dump" in inputs:
             self._run_agent("IntakeAgent")

        if not self.state.get_artifact("voice_guide"):
             self._run_agent("VoiceAgent")

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
        current_context = self.state.data["inputs"].copy()
        current_context.update(self.state.get_all_artifacts())

        output = agent.run(current_context)

        # Update state
        self.state.add_agent_output(agent_name, output)
        print(f"  <- {agent_name} completed.")
