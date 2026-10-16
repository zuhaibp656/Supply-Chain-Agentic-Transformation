"""Enterprise Twin ADK Agent.

Autonomous Google ADK (Agent Development Kit) Agent for enterprise supply chain
digital twin synthesis. Takes any company name (e.g., ITC, Volkswagen, Boeing,
Caterpillar, Shell, Pfizer) and:
1. Conducts LLM & tool-based corporate profiling (industry, facilities, products).
2. Mines authentic organizational job titles and operational toils across all 26 SCOR roles.
3. Customizes the operational details inside all 32 AI Agents (ERP/MES systems, inputs, outcomes)
   while keeping the core base architecture identical.
4. Persists the generated twin to local JSON storage, memory cache, and BigQuery/GCS staging.
5. Generates the tailored interactive portal files and ready-to-deploy Zipline bundles.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Ensure package path is registered
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from enterprise_twin.tools.company_profiler import profile_company, KNOWN_COMPANIES
from enterprise_twin.tools.career_persona_miner import mine_company_personas
from enterprise_twin.tools.agent_spec_miner import mine_company_agent_specs
from enterprise_twin.tools.ecosystem_miner import mine_company_ecosystem
from enterprise_twin.tools.persistence import save_twin, load_twin, list_saved_twins
from enterprise_twin.generator.html_compiler import compile_enterprise_twin


# ADK Agent Tool Callables
def tool_profile_enterprise(company_name: str, industry_hint: Optional[str] = None) -> Dict[str, Any]:
    """Profiles company branding, executive leadership, flagship factories, and core products."""
    return profile_company(company_name, industry_hint)


def tool_mine_personas(company_name: str, industry_id: str) -> Dict[str, Any]:
    """Discovers real organizational job titles and operational toils for the 26 SCOR personas."""
    return mine_company_personas(company_name, industry_id)


def tool_mine_agent_specs(company_name: str, industry_id: str) -> Dict[str, Any]:
    """Adapts internal operational details for 32 AI agents while keeping base engines intact."""
    return mine_company_agent_specs(company_name, industry_id)


def tool_persist_twin(twin_data: Dict[str, Any]) -> str:
    """Saves twin into persistent JSON memory and stages for BigQuery / GCS export."""
    path = save_twin(twin_data)
    return str(path)


def tool_compile_portal(twin_data: Dict[str, Any]) -> Dict[str, str]:
    """Compiles the standalone HTML portal and Zipline bundle for the enterprise twin."""
    out_dir = compile_enterprise_twin(twin_data)
    slug = out_dir.name
    return {
        "output_dir": str(out_dir),
        "index_html": str(out_dir / "index.html"),
        "periodic_table": str(out_dir / "periodic_table.html"),
        "mind_map": str(out_dir / "mind_map.html"),
        "zipline_bundle": str(out_dir / f"{slug}_zipline_bundle.zip")
    }


# High-Level Orchestrator Function
def run_enterprise_twin_agent(company_name: str, industry: Optional[str] = None, focus: Optional[str] = None) -> Dict[str, Any]:
    """Executes the full agentic pipeline to generate and persist an Enterprise Twin."""
    print(f"\n🤖 [ADK Agent] Initializing Enterprise Twin Agent for: '{company_name}'...")

    # 1. Check if twin already exists in memory / storage
    existing = load_twin(company_name)
    if existing and not focus:
        print(f"⚡ [ADK Agent] Found existing approved twin in memory: '{existing.get('canonicalName')}'")
        compile_res = tool_compile_portal(existing)
        return {
            "status": "success",
            "source": "memory_cache",
            "profile": existing,
            "artifacts": compile_res
        }

    # 2. Tool 1: Profile Enterprise Identity & Products
    print(f"🔍 [ADK Agent] Step 1/4: Profiling corporate identity, factories & brand...")
    profile = tool_profile_enterprise(company_name, industry)
    if focus:
        profile['executiveThesis'] += f" Strategic operational focus: {focus}."

    # 3. Tool 2: Mine Specialized Organizational Roles & Toils (All 26 Personas)
    print(f"👔 [ADK Agent] Step 2/4: Mining 26 SCOR persona titles & daily toils ({profile['industryId']})...")
    personas = tool_mine_personas(profile['canonicalName'], profile['industryId'])
    profile['personaOverrides'] = personas

    # 4. Tool 3: Adapt Internal Operational Details for 32 AI Agents
    print(f"⚙️  [ADK Agent] Step 3/4: Tailoring operational specs for 32 AI agents...")
    agent_specs = tool_mine_agent_specs(profile['canonicalName'], profile['industryId'])
    profile['agentOverrides'] = agent_specs

    # 5. Tool 4: Persist to Memory / Storage
    print(f"💾 [ADK Agent] Step 4/4: Persisting twin to memory & staging for BigQuery/GCS...")
    twin_file = tool_persist_twin(profile)

    # 6. Tool 5: Compile Standalone Portal & Zipline Bundle
    compile_res = tool_compile_portal(profile)

    print(f"✨ [ADK Agent] Complete! Twin generated for '{profile['canonicalName']}' -> {compile_res['output_dir']}\n")

    return {
        "status": "success",
        "source": "autonomous_synthesis",
        "profile": profile,
        "artifacts": compile_res
    }


# Attempt to instantiate official ADK Agent if google.adk is present
try:
    from google.adk.agents.llm_agent import Agent
    from google.adk.models.google_llm import Gemini

    adk_agent = Agent(
        name="enterprise_twin_agent",
        description="Autonomous Google ADK agent that researches enterprise companies and synthesizes bespoke supply chain digital twin portals.",
        instruction=(
            "You are the Enterprise Twin ADK Agent.\n"
            "Given any enterprise company name, research its real supply chain operations, products, and plants.\n"
            "Adapt all 26 SCOR personas into the company's real organizational titles with authentic industry lingo.\n"
            "Customize the operational details inside all 32 AI agents with the company's real ERP/MES systems.\n"
            "Persist the twin and generate the complete adapted portal."
        ),
        tools=[tool_profile_enterprise, tool_mine_personas, tool_mine_agent_specs, tool_persist_twin, tool_compile_portal]
    )
except Exception:
    adk_agent = None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enterprise Twin ADK Agent Runner")
    parser.add_argument("company", nargs="?", default="ITC Limited", help="Company name (e.g. 'ITC', 'Volkswagen', 'Boeing')")
    parser.add_argument("--industry", default=None, help="Industry sector hint (e.g. automotive, fmcg, aerospace)")
    parser.add_argument("--focus", default=None, help="Strategic operational focus")
    args = parser.parse_args()

    result = run_enterprise_twin_agent(args.company, args.industry, args.focus)
    print(json.dumps({
        "company": result["profile"]["canonicalName"],
        "industry": result["profile"]["industryId"],
        "executiveTitle": result["profile"]["executiveTitle"],
        "artifacts": result["artifacts"]
    }, indent=2))
