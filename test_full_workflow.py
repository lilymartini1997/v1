from genesis_system.core.orchestrator import CampaignDirector
from genesis_system.core.llm_interface import MockLLM
import json

def test_workflow():
    print("Running Full Workflow Test...")

    inputs = {
        "offer_source": {
            "sales_page_text": "Buy my course."
        },
        "target_market": "Entrepreneurs",
        "channels": ["Meta", "Email"]
    }

    llm = MockLLM()
    director = CampaignDirector(llm)

    result = director.run_campaign("CREATE_CAMPAIGN", inputs)

    print("Workflow Finished.")
    print(f"Final Version: {result.get('version')}")
    print(f"Artifacts Count: {len(result.get('artifacts', {}))}")
    print(f"Agent Outputs Logged: {len(result.get('agent_outputs', []))}")

    # Basic Validation
    artifacts = result.get('artifacts', {})
    if "offer_brief" in artifacts:
        print("PASS: OfferBrief found.")
    else:
        print("FAIL: OfferBrief missing.")

    if "segments" in artifacts:
        print("PASS: Segments found.")
    else:
        print("FAIL: Segments missing.")

if __name__ == "__main__":
    test_workflow()
