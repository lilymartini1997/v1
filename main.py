import argparse
import json
import sys
import os
from genesis_system.core.orchestrator import CampaignDirector
from genesis_system.core.llm_interface import MockLLM, OpenAILLM, GeminiLLM

def generate_deliverables_md(state):
    md = "# Campaign Deliverables\n\n"
    artifacts = state.get("artifacts", {})

    # 1. Offer Brief
    if "offer_brief" in artifacts:
        ob = artifacts["offer_brief"]
        md += f"## Offer Brief: {ob.get('offer_name', 'N/A')}\n"
        md += f"**Promise:** {ob.get('main_promise')}\n"
        md += f"**Target Market:** {ob.get('target_market')}\n"
        md += f"**Mechanism:** {ob.get('mechanism_claim')}\n\n"

    # 2. Segments
    if "segments" in artifacts:
        md += "## Segments\n"
        for seg in artifacts["segments"]:
            md += f"### {seg.get('segment_name')}\n"
            md += f"- **Desire:** {seg.get('core_desire')}\n"
            md += f"- **Winning Angles:** {', '.join(seg.get('winning_angles', []))}\n"
        md += "\n"

    # 3. Mechanisms (Top 3)
    if "top_3" in artifacts:
        md += "## Top Mechanisms\n"
        for mech in artifacts["top_3"]:
            md += f"### {mech.get('name')}\n"
            md += f"**Why it wins:** {mech.get('why_it_wins')}\n"
            md += f"**One Liner:** {mech.get('one_liner', '')}\n"
        md += "\n"

    # 4. Hooks
    if "hooks" in artifacts:
        md += "## Hooks\n"
        for hook in artifacts["hooks"]:
             md += f"- [{hook.get('type')}] {hook.get('hook')}\n"
        md += "\n"

    # 5. Scripts (Top selections or all)
    if "scripts" in artifacts:
        md += "## Generated Scripts\n"
        for script in artifacts["scripts"]:
             md += f"### Script ({script.get('format')})\n"
             md += f"**Hook:** {script.get('hook')}\n"
             md += "**Body:**\n"
             for line in script.get('body', []):
                 md += f"> {line}\n"
             md += f"\n**CTA:** {script.get('cta')}\n\n"

    # 6. Emails / Repurposed Assets
    if "repurposed_assets" in artifacts:
        md += "## Repurposed Assets\n"
        for collection in artifacts["repurposed_assets"]:
            md += f"### Format: {collection.get('target_format')}\n"
            for asset in collection.get("assets", []):
                md += f"#### {asset.get('title', 'Asset')}\n"
                for line in asset.get('body', []):
                    md += f"{line}\n"
                md += "\n"

    # 7. New Agent Specs (Builder Mode)
    if "new_agent_spec" in artifacts:
        spec = artifacts["new_agent_spec"]
        md += f"## New Agent Spec: {spec.get('agent_name')}\n"
        md += f"**Purpose:** {spec.get('purpose')}\n"
        md += "```json\n"
        md += json.dumps(spec, indent=2)
        md += "\n```\n"

    return md

def generate_assets_json(state):
    artifacts = state.get("artifacts", {})
    assets = {
        "scripts": artifacts.get("scripts", []),
        "hooks": artifacts.get("hooks", []),
        "ad_directions": artifacts.get("ad_directions", []),
        "emails": artifacts.get("repurposed_assets", []),
        "scene_plan": artifacts.get("scene_plan", {}),
        "new_agent_spec": artifacts.get("new_agent_spec", {})
    }
    return assets

def main():
    parser = argparse.ArgumentParser(description="Genesis System CLI")
    parser.add_argument("--mode", choices=["CREATE_CAMPAIGN", "CONVERT_ASSET", "BUILD_AGENT"], required=True)
    parser.add_argument("--input_file", help="Path to JSON file containing inputs", required=True)
    parser.add_argument("--output_dir", help="Directory to save outputs", default="output")
    parser.add_argument("--llm_provider", choices=["mock", "openai", "gemini"], default="mock", help="LLM Provider to use")
    parser.add_argument("--openai_api_key", help="OpenAI API Key (or set OPENAI_API_KEY env var)", default=None)
    parser.add_argument("--gemini_api_key", help="Gemini API Key (or set GEMINI_API_KEY env var)", default=None)
    parser.add_argument("--model", help="LLM Model to use (e.g. gemini-1.5-flash, gpt-4)", default=None)

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
        llm = OpenAILLM(api_key=args.openai_api_key, model=args.model or "gpt-4-turbo")
    elif args.llm_provider == "gemini":
        llm = GeminiLLM(api_key=args.gemini_api_key, model=args.model or "gemini-1.5-pro")
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
