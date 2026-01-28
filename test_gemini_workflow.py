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
    # Note: If this fails with 429, it means the API key quota is exhausted.
    # Using 'gemini-2.0-flash' which is listed as available.
    llm = GeminiLLM(api_key=api_key, model="gemini-2.0-flash")
    director = CampaignDirector(llm)

    try:
        print("Starting workflow...")
        result = director.run_campaign("CREATE_CAMPAIGN", inputs)

        print("Workflow Finished.")
        print(f"Final Version: {result.get('version')}")
        print(f"Artifacts Count: {len(result.get('artifacts', {}))}")

        # Basic Validation
        artifacts = result.get('artifacts', {})

        # Offer Brief
        if "offer_brief" in artifacts:
            print("PASS: OfferBrief found.")
        else:
            print("FAIL: OfferBrief missing.")

        # Segments
        if "segments" in artifacts:
            print("PASS: Segments found.")
        else:
            print("FAIL: Segments missing.")

        # Buyer Profiles
        if "buyer_profiles" in artifacts:
            print("PASS: BuyerProfiles found.")
        else:
            print("FAIL: BuyerProfiles missing.")

        # Voice Guide
        if "voice_guide" in artifacts:
            print("PASS: VoiceGuide found.")
        else:
            print("FAIL: VoiceGuide missing.")

    except Exception as e:
        print(f"Workflow failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_workflow()
