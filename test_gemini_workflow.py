import os
import json
from genesis_system.core.orchestrator import CampaignDirector
from genesis_system.core.llm_interface import GeminiLLM

def test_gemini_workflow():
    print("Running Gemini Workflow Test...")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("SKIPPING: GEMINI_API_KEY not found.")
        return

    inputs = {
        "offer_source": {
            "sales_page_text": "Buy my course."
        },
        "target_market": "Entrepreneurs",
        "channels": ["Meta", "Email"]
    }

    # Use flash model for testing as requested
    llm = GeminiLLM(api_key=api_key, model="gemini-flash-latest")
    director = CampaignDirector(llm)

    try:
        result = director.run_campaign("CREATE_CAMPAIGN", inputs)

        print("Workflow Finished.")
        print(f"Final Version: {result.get('version')}")
        print(f"Artifacts Count: {len(result.get('artifacts', {}))}")

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

    except Exception as e:
        print(f"Workflow failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_workflow()
