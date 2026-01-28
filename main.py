import argparse
import json
import sys
import os
from genesis_system.core.orchestrator import CampaignDirector
from genesis_system.core.llm_interface import MockLLM, OpenAILLM

def generate_deliverables_md(state):
    md = "# Campaign Deliverables\n\n"
    artifacts = state.get("artifacts", {})

    if "offer_brief" in artifacts:
        ob = artifacts["offer_brief"]
        md += f"## Offer Brief: {ob.get('offer_name', 'N/A')}\n"
        md += f"**Promise:** {ob.get('main_promise')}\n\n"

    if "segments" in artifacts:
        md += "## Segments\n"
        for seg in artifacts["segments"]:
            md += f"- **{seg.get('segment_name')}**: {seg.get('core_desire')}\n"
        md += "\n"

    # Add more sections as needed

    return md

def generate_assets_json(state):
    artifacts = state.get("artifacts", {})
    assets = {
        "scripts": artifacts.get("scripts", []),
        "hooks": artifacts.get("hooks", []),
        "ad_directions": artifacts.get("ad_directions", []),
        "emails": artifacts.get("repurposed_assets", [])
    }
    return assets

def main():
    parser = argparse.ArgumentParser(description="Genesis System CLI")
    parser.add_argument("--mode", choices=["CREATE_CAMPAIGN", "CONVERT_ASSET"], required=True)
    parser.add_argument("--input_file", help="Path to JSON file containing inputs", required=True)
    parser.add_argument("--output_dir", help="Directory to save outputs", default="output")
    parser.add_argument("--llm_provider", choices=["mock", "openai"], default="mock", help="LLM Provider to use")
    parser.add_argument("--openai_api_key", help="OpenAI API Key (or set OPENAI_API_KEY env var)", default=None)

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    try:
        with open(args.input_file, 'r') as f:
            inputs = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    if args.llm_provider == "openai":
        llm = OpenAILLM(api_key=args.openai_api_key)
    else:
        llm = MockLLM()

    director = CampaignDirector(llm)

    try:
        result = director.run_campaign(args.mode, inputs)

        # 1. CampaignState.json
        with open(os.path.join(args.output_dir, "CampaignState.json"), 'w') as f:
            json.dump(result, f, indent=2)

        # 2. Deliverables.md
        md_content = generate_deliverables_md(result)
        with open(os.path.join(args.output_dir, "Deliverables.md"), 'w') as f:
            f.write(md_content)

        # 3. Assets.json
        assets_content = generate_assets_json(result)
        with open(os.path.join(args.output_dir, "Assets.json"), 'w') as f:
            json.dump(assets_content, f, indent=2)

        print(f"Campaign completed. Outputs saved to {args.output_dir}/")
    except Exception as e:
        print(f"Error running campaign: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
