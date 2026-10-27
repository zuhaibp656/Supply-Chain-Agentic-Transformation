#!/usr/bin/env python3
"""One-shot idempotent deployer: Supply Chain Categorized ADK Agents -> Vertex AI Agent Engine -> Gemini Enterprise.

Features:
  - Explicitly includes each agent's Category (`[<Pillar> · <Sub-Pillar>]`) in its `display_name`,
    `ge_display_name`, `description`, and `tool_description`.
  - Supports all 60 catalog agents (`--agent <id>` or `--all-60`) as well as the 14 provisioned
    flagship agents (`--all-flagship`), reusing existing Vertex AI Reasoning Engines (`.reasoning_engine_id`)
    and existing Gemini Enterprise agent registrations (`provisionedReasoningEngine` match) IN-PLACE!
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
ROOT = Path(__file__).resolve().parent.parent

# ==============================================================================
# 14 Provisioned Flagship Agents (with Category in Name & Description + Resource Reuse)
# ==============================================================================
FLAGSHIP_CONFIG: Dict[str, Dict[str, Any]] = {
    "csco_control_tower_copilot": {
        "section": "01 · Plan | S&OP / IBP",
        "category": "01 · Planning & Strategy — S&OP / IBP",
        "display_name": "[01 · Plan | S&OP / IBP] CSCO Control Tower Copilot (TowerMind)",
        "legacy_display_name": "CSCO Control Tower Copilot (TowerMind)",
        "ge_display_name": "[Plan · S&OP/IBP] TowerMind Control Tower",
        "legacy_ge_display_name": "TowerMind Control Tower",
        "description": "[Category: 01 · Planning & Strategy — S&OP / IBP] CSCO Control Tower Copilot (TowerMind): multi-echelon bottleneck triage, real-time KPI visibility, and autonomous S&OP/IBP playbook execution across ERP, WMS, and TMS.",
        "model": "gemini-3.1-pro-preview",
        "icon": "hub",
        "app_class": "CscoControlTowerAdkApp",
        "tool_description": "[Category: 01 · Plan | S&OP / IBP] Use TowerMind to investigate global supply chain KPIs, detect multi-echelon bottlenecks, and execute executive remediation playbooks.",
        "starter_prompts": [
            "Show global supply chain KPI briefing and active bottlenecks",
            "Investigate Suez Canal delay impact on Stuttgart assembly line",
            "Trigger intermodal air expedite playbook for critical battery modules",
            "Rebalance inventory from Central US Hub to European staging",
        ],
    },
    "disruption_war_room_orchestrator": {
        "section": "01 · Plan | S&OP / IBP",
        "category": "01 · Planning & Strategy — S&OP / IBP",
        "display_name": "[01 · Plan | S&OP / IBP] Disruption War Room Orchestrator (StormShield)",
        "legacy_display_name": "Disruption War Room Orchestrator (StormShield)",
        "ge_display_name": "[Plan · S&OP/IBP] StormShield War Room",
        "legacy_ge_display_name": "StormShield War Room",
        "description": "[Category: 01 · Planning & Strategy — S&OP / IBP] Disruption War Room Orchestrator (StormShield): multi-modal geopolitical crisis response, maritime vessel tracking, weather radar correlation, and automated S&OP recovery.",
        "model": "gemini-3.1-pro-preview",
        "icon": "crisis_alert",
        "app_class": "DisruptionWarRoomAdkApp",
        "tool_description": "[Category: 01 · Plan | S&OP / IBP] Use StormShield to scan maritime corridors for typhoon alerts, map multi-tier supplier exposure, and launch emergency war rooms.",
        "starter_prompts": [
            "Scan global maritime corridors for active typhoon disruptions",
            "Assess Tier-1 supplier facility flood exposure in Southeast Asia",
            "Convene emergency War Room for Mediterranean port congestion",
            "Execute Cape of Good Hope rerouting with fuel surcharge impact",
        ],
    },
    "demand_sensing_agent": {
        "section": "01 · Plan | Demand Forecasting",
        "category": "01 · Planning & Strategy — Demand Forecasting",
        "display_name": "[01 · Plan | Demand Forecasting] Demand Sensing Engine (PulseCast)",
        "legacy_display_name": "Demand Sensing Engine (PulseCast)",
        "ge_display_name": "[Plan · Forecasting] PulseCast Demand Sensing",
        "legacy_ge_display_name": "PulseCast Demand Sensing",
        "description": "[Category: 01 · Planning & Strategy — Demand Forecasting] Demand Sensing Engine (PulseCast): multi-signal probabilistic forecasting with WeatherNext 3, POS scans, and TimesFM quantile intervals.",
        "model": "gemini-3.1-pro-preview",
        "icon": "trending_up",
        "app_class": "DemandSensingAdkApp",
        "tool_description": "[Category: 01 · Plan | Demand Forecasting] Use PulseCast to ingest store POS scans, correlate WeatherNext weather signals, and calculate TimesFM probabilistic demand forecasts.",
        "starter_prompts": [
            "Sense demand shift for beverage category across Midwest stores",
            "Incorporate WeatherNext heatwave alert into 14-day demand forecast",
            "Detect demand shaping lift from upcoming retail promotion",
            "Harmonize channel POS scan discrepancies with CPFR distributor feed",
        ],
    },
    "sop_scenario_weaver": {
        "section": "01 · Plan | S&OP / IBP",
        "category": "01 · Planning & Strategy — S&OP / IBP",
        "display_name": "[01 · Plan | S&OP / IBP] S&OP Scenario Weaver (Synapse)",
        "legacy_display_name": "S&OP Scenario Weaver (Synapse)",
        "ge_display_name": "[Plan · S&OP/IBP] Synapse S&OP Weaver",
        "legacy_ge_display_name": "Synapse S&OP Weaver",
        "description": "[Category: 01 · Planning & Strategy — S&OP / IBP] S&OP Scenario Weaver (Synapse): finite plant capacity balancing, supplier allocation quotas, and margin-maximizing scenario tradeoffs.",
        "model": "gemini-3.1-pro-preview",
        "icon": "tune",
        "app_class": "SopScenarioWeaverAdkApp",
        "tool_description": "[Category: 01 · Plan | S&OP / IBP] Use Synapse to generate 5-step monthly S&OP consensus scenarios, balance finite plant line capacities, and optimize component allocations.",
        "starter_prompts": [
            "Generate 5-step monthly S&OP consensus scenario comparison",
            "Evaluate plant line capacity overrun if European demand surges 15%",
            "Optimize supplier component allocations under dual-sourcing quota",
            "Recommend margin-maximizing production mix for Q4 peak season",
        ],
    },
    "rfq_should_cost_agent": {
        "section": "02 · Source | Material & Packaging",
        "category": "02 · Sourcing & Procurement — Material & Packaging",
        "display_name": "[02 · Source | Material & Packaging] Parametric Should-Cost & RFQ Agent (SourcePulse)",
        "legacy_display_name": "Parametric Should-Cost & RFQ Agent (SourcePulse)",
        "ge_display_name": "[Source · Material] SourcePulse Should-Cost",
        "legacy_ge_display_name": "SourcePulse Should-Cost",
        "description": "[Category: 02 · Sourcing & Procurement — Material & Packaging] Parametric Should-Cost & RFQ Agent (SourcePulse): automated BOM cost breakdown, commodity index tracking, and autonomous supplier RFQ bid analysis.",
        "model": "gemini-3.1-pro-preview",
        "icon": "request_quote",
        "app_class": "RfqShouldCostAdkApp",
        "tool_description": "[Category: 02 · Source | Material & Packaging] Use SourcePulse to calculate bottom-up parametric should-cost models, benchmark commodity indexes, and audit supplier RFQ bids.",
        "starter_prompts": [
            "Calculate parametric should-cost for aluminum heat exchanger BOM",
            "Benchmark supplier RFQ bids against London Metal Exchange index",
            "Flag outlier quotes with excessive margin in injection molding",
            "Recommend multi-supplier award allocation maximizing margin",
        ],
    },
    "tier_n_risk_sentinel": {
        "section": "02 · Source | Vendor Sourcing",
        "category": "02 · Sourcing & Procurement — Vendor Sourcing",
        "display_name": "[02 · Source | Vendor Sourcing] Multi-Tier Supply Network Sentinel (NexusShield)",
        "legacy_display_name": "Multi-Tier Supply Network Sentinel (NexusShield)",
        "ge_display_name": "[Source · Vendor Risk] NexusShield Sentinel",
        "legacy_ge_display_name": "NexusShield Risk Sentinel",
        "description": "[Category: 02 · Sourcing & Procurement — Vendor Sourcing] Multi-Tier Supply Network Sentinel (NexusShield): Cloud Spanner Graph lineage, deep supplier dependencies, geopolitical risk, and single-source exposure.",
        "model": "gemini-3.1-pro-preview",
        "icon": "security",
        "app_class": "TierNRiskSentinelAdkApp",
        "tool_description": "[Category: 02 · Source | Vendor Sourcing] Use NexusShield to trace multi-tier supplier lineage in Spanner Graph, detect single-source component risks, and simulate trade impacts.",
        "starter_prompts": [
            "Trace Tier-3 semiconductor dependencies for engine control units",
            "Identify single-source chokepoints in Tier-2 raw material supply",
            "Simulate trade restriction impact on Taiwanese component suppliers",
            "Recommend qualified secondary suppliers with audited capacity",
        ],
    },
    "plant_oee_maintenance_agent": {
        "section": "03 · Make | Production Scheduling",
        "category": "03 · Manufacturing & Production — Production Scheduling",
        "display_name": "[03 · Make | Production Scheduling] Plant OEE & Maintenance Guardian (AssetGuard)",
        "legacy_display_name": "Plant OEE & Maintenance Guardian (AssetGuard)",
        "ge_display_name": "[Make · OEE & Sched] AssetGuard Plant OEE",
        "legacy_ge_display_name": "AssetGuard Plant OEE",
        "description": "[Category: 03 · Manufacturing & Production — Production Scheduling] Plant OEE & Maintenance Guardian (AssetGuard): real-time IoT vibration analysis, anomaly detection, predictive maintenance scheduling, and spare parts inventory.",
        "model": "gemini-3.1-pro-preview",
        "icon": "precision_manufacturing",
        "app_class": "PlantOeeMaintenanceAdkApp",
        "tool_description": "[Category: 03 · Make | Production Scheduling] Use AssetGuard to audit plant OEE metrics, analyze machine vibration telemetry, detect anomalies, and schedule maintenance windows.",
        "starter_prompts": [
            "Show OEE breakdown across automotive assembly lines A and B",
            "Analyze spindle vibration telemetry on CNC Machine 4",
            "Check spare parts availability for high-risk hydraulic pump",
            "Schedule preventative maintenance window to avoid unplanned downtime",
        ],
    },
    "inline_quality_inspection_agent": {
        "section": "03 · Make | Quality & Compliance",
        "category": "03 · Manufacturing & Production — Quality & Compliance",
        "display_name": "[03 · Make | Quality & Compliance] Inline Multimodal Quality Inspector (VisionInspect)",
        "legacy_display_name": "Inline Multimodal Quality Inspector (VisionInspect)",
        "ge_display_name": "[Make · Quality] VisionInspect Quality",
        "legacy_ge_display_name": "VisionInspect Quality",
        "description": "[Category: 03 · Manufacturing & Production — Quality & Compliance] Inline Multimodal Quality Inspector (VisionInspect): Gemini 3.8 Flash multimodal vision, micro-crack & seal defect detection, and pneumatic diverter gate triage.",
        "model": "gemini-3.8-flash",
        "icon": "document_scanner",
        "app_class": "InlineQualityInspectionAdkApp",
        "tool_description": "[Category: 03 · Make | Quality & Compliance] Use VisionInspect with Gemini 3.8 Flash to inspect camera frames, classify micro-defects, audit batch records, and calibrate pneumatic diverters.",
        "starter_prompts": [
            "Inspect latest high-speed camera frame for seal integrity defects",
            "Review electronic batch record deviation log for Line 3",
            "Calibrate pneumatic reject gate timing for micro-crack ejection",
            "Summarize daily scrap rate and defect classification distribution",
        ],
    },
    "echelon_inventory_allocator": {
        "section": "04 · Inventory & DC | Positioning & Optimization",
        "category": "04 · Inventory & Warehousing — Positioning & Optimization",
        "display_name": "[04 · Inventory & DC | Positioning & Optimization] Multi-Echelon Inventory Allocator (EchelonFlow)",
        "legacy_display_name": "Multi-Echelon Inventory Allocator (EchelonFlow)",
        "ge_display_name": "[Inventory · MEIO] EchelonFlow Allocator",
        "legacy_ge_display_name": "EchelonFlow MEIO",
        "description": "[Category: 04 · Inventory & Warehousing — Positioning & Optimization] Multi-Echelon Inventory Allocator (EchelonFlow): stochastic Clark-Scarf multi-echelon safety stock optimization, service level projection, and lateral DC rebalancing.",
        "model": "gemini-3.1-pro-preview",
        "icon": "inventory_2",
        "app_class": "EchelonInventoryAllocatorAdkApp",
        "tool_description": "[Category: 04 · Inventory & DC | Positioning & Optimization] Use EchelonFlow to run Clark-Scarf multi-echelon safety stock calculations, evaluate service level vs capital, and execute lateral DC transfers.",
        "starter_prompts": [
            "Optimize multi-echelon safety stock across Central RDC and 4 FDCs",
            "Simulate service level vs working capital curve for A-category SKUs",
            "Plan lateral DC inventory transfer to avert stockout in Atlanta",
            "Review Clark-Scarf echelon holding cost vs stockout penalty tradeoffs",
        ],
    },
    "dynamic_order_promising_atp": {
        "section": "04 · Inventory & DC | Omnichannel Visibility",
        "category": "04 · Inventory & Warehousing — Omnichannel Visibility",
        "display_name": "[04 · Inventory & DC | Omnichannel Visibility] Sub-50ms Spanner ATP & Order Promising (PromiseGuard)",
        "legacy_display_name": "Sub-50ms Spanner ATP & Order Promising (PromiseGuard)",
        "ge_display_name": "[Inventory · Omnichannel] PromiseGuard ATP",
        "legacy_ge_display_name": "PromiseGuard ATP",
        "description": "[Category: 04 · Inventory & Warehousing — Omnichannel Visibility] Sub-50ms Spanner ATP & Order Promising (PromiseGuard): real-time available-to-promise, strategic customer tier quota protection, and multi-facility order routing.",
        "model": "gemini-3.1-pro-preview",
        "icon": "verified",
        "app_class": "DynamicOrderPromisingAtpAdkApp",
        "tool_description": "[Category: 04 · Inventory & DC | Omnichannel Visibility] Use PromiseGuard to evaluate sub-50ms Spanner ATP availability, protect strategic tier quotas, and route customer sales orders.",
        "starter_prompts": [
            "Check real-time ATP for 5,000 units of Enterprise Server SKU",
            "Evaluate order promising for Tier-1 customer with strict 48h SLA",
            "Protect strategic quota from stockout during wholesale rush",
            "Route split-shipment order across Dallas DC and Chicago Hub",
        ],
    },
    "fleetflow_dispatch": {
        "section": "05 · Logistics | Last-Mile Delivery",
        "category": "05 · Distribution & Logistics — Last-Mile Delivery",
        "display_name": "[05 · Logistics | Last-Mile Delivery] Google Maps Corridor Route & Fleet Dispatch Studio (FleetFlow)",
        "legacy_display_name": "Google Maps Corridor Route & Fleet Dispatch Studio (FleetFlow)",
        "ge_display_name": "[Logistics · Last-Mile] FleetFlow Dispatch",
        "legacy_ge_display_name": "FleetFlow Route & Dispatch",
        "description": "[Category: 05 · Distribution & Logistics — Last-Mile Delivery] FleetFlow Dispatch Studio: angular sector corridor clustering, Google Maps Routes v2 live traffic matrices, and OR-Tools CVRPTW fleet dispatch.",
        "model": "gemini-3.1-pro-preview",
        "icon": "local_shipping",
        "app_class": "FleetflowDispatchAdkApp",
        "tool_description": "[Category: 05 · Logistics | Last-Mile Delivery] Use FleetFlow to cluster urban delivery stops into directional corridors, solve OR-Tools CVRPTW fleet dispatch, and issue mobile driver manifests.",
        "starter_prompts": [
            "Cluster 64 retail delivery drops into 8 directional highway corridors",
            "Optimize morning fleet dispatch to cut active truck count from 10 to 8",
            "Pin lead driver Ravi to West corridor on 14-ft truck and rebalance overflow",
            "Generate turn-by-turn Google Maps navigation links and driver challans",
        ],
    },
    "load_consolidation_agent": {
        "section": "05 · Logistics | First & Mid-Mile",
        "category": "05 · Distribution & Logistics — First & Mid-Mile",
        "display_name": "[05 · Logistics | First & Mid-Mile] Isometric LIFO Bay & 3D Load Consolidation Studio (CubeMaster 3D)",
        "legacy_display_name": "Isometric LIFO Bay & 3D Load Consolidation Studio (CubeMaster 3D)",
        "ge_display_name": "[Logistics · 3D Load] CubeMaster 3D Studio",
        "legacy_ge_display_name": "CubeMaster 3D Load Studio",
        "description": "[Category: 05 · Distribution & Logistics — First & Mid-Mile] CubeMaster 3D Load Studio: cab-to-door reverse-stop LIFO bay zoning, 3D Guillotine bin-packing, crush-fragility stacking, and CMVR Rule 93 axle balance.",
        "model": "gemini-3.1-pro-preview",
        "icon": "view_in_ar",
        "app_class": "LoadConsolidationAgentAdkApp",
        "tool_description": "[Category: 05 · Logistics | First & Mid-Mile] Use CubeMaster 3D to pack multi-stop cartons in reverse delivery order (LIFO), verify 80%+ vertical support, and balance steer/drive axle torque.",
        "starter_prompts": [
            "Generate 3D cab-to-door LIFO loading plan for 53-ft trailer on Corridor West",
            "Verify zero crush-fragility violations and 80%+ floor support across all tiers",
            "Check CMVR Rule 93 steer vs drive axle weight balance and Center of Gravity",
            "Commit verified 3D bay loading manifest to Manhattan WMS dock doors",
        ],
    },
    "reverse_rma_optimizer": {
        "section": "06 · Returns & ESG | Returns & Claims Mgmt",
        "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt",
        "display_name": "[06 · Returns & ESG | Returns & Claims Mgmt] Autonomous RMA Grading & Circular Backhaul Optimizer (ReturnLoop)",
        "legacy_display_name": "Autonomous RMA Grading & Circular Backhaul Optimizer (ReturnLoop)",
        "ge_display_name": "[Returns · RMA Triage] ReturnLoop Optimizer",
        "legacy_ge_display_name": "ReturnLoop RMA & Backhaul",
        "description": "[Category: 06 · Returns & Reverse Logistics — Returns & Claims Mgmt] ReturnLoop RMA Optimizer: Gemini 3.8 Flash multimodal defect grading, automated disposition routing, and empty-backhaul fleet insertion.",
        "model": "gemini-3.8-flash",
        "icon": "assignment_return",
        "app_class": "ReverseRmaOptimizerAdkApp",
        "tool_description": "[Category: 06 · Returns & ESG | Returns & Claims Mgmt] Use ReturnLoop to grade customer RMA photos with Gemini 3.8 Flash vision, route refurbish vs scrap dispositions, and match return pickups to empty backhauls.",
        "starter_prompts": [
            "Grade customer RMA return photos and classify refurbish vs scrap disposition",
            "Match 18 retail return pallets to returning FleetFlow empty-backhaul trucks",
            "Calculate net circular recovery value across open RMA queue",
            "Issue instant customer RMA credit memo and refurbishment work order",
        ],
    },
    "carbon_scope3_ledger": {
        "section": "02 · Source | Vendor Sourcing",
        "category": "02 · Sourcing & Procurement — Vendor Sourcing",
        "display_name": "[02 · Source | Vendor Sourcing] Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger (EcoChain)",
        "legacy_display_name": "Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger (EcoChain)",
        "ge_display_name": "[Source · ESG & Carbon] EcoChain Scope-3",
        "legacy_ge_display_name": "EcoChain Scope-3 & CBAM",
        "description": "[Category: 02 · Sourcing & Procurement — Vendor Sourcing] EcoChain Carbon Ledger: ISO 14083 & GLEC v3.0 primary telemetry Scope-3 accounting, EU CBAM embedded carbon declarations, and Earth Engine EUDR verification.",
        "model": "gemini-3.1-pro-preview",
        "icon": "eco",
        "app_class": "CarbonScope3LedgerAdkApp",
        "tool_description": "[Category: 02 · Source | Vendor Sourcing] Use EcoChain to compute ISO 14083 shipment Scope-3 emissions, certify EU CBAM smelter declarations, and verify EUDR zero-deforestation plots via Earth Engine.",
        "starter_prompts": [
            "Calculate ISO 14083 primary telemetry Scope-3 emissions for Rhine corridor",
            "Generate EU CBAM embedded carbon declaration using primary smelter certificates",
            "Verify zero post-2020 deforestation on supplier rubber plots via Earth Engine",
            "Recommend low-carbon HVO100 biofuel and electric barge carrier swaps",
        ],
    },
}


def build_all_60_agents_config() -> Dict[str, Dict[str, Any]]:
    """Builds deployment specs for all 60 catalog agents (merging with FLAGSHIP_CONFIG)."""
    merged = dict(FLAGSHIP_CONFIG)
    cat_path = ROOT / "data" / "supply_chain_catalog.json"
    if not cat_path.exists():
        return merged

    cat = json.loads(cat_path.read_text(encoding="utf-8"))
    for aid, ag in cat.get("agents", {}).items():
        if aid in merged:
            continue
        agent_dir = ROOT / "agents" / aid
        agent_py = agent_dir / "app" / "agent.py"
        app_class = "".join(w.capitalize() for w in aid.split("_") if w) + "AdkApp"
        if agent_py.exists():
            import re
            m = re.search(r"class\s+(\w+)\(AdkApp\):", agent_py.read_text(encoding="utf-8"))
            if m:
                app_class = m.group(1)

        cat_tag = ag.get("categoryTag", "01 · Plan")
        cat_full = ag.get("category", "01 · Planning & Strategy")
        disp = ag.get("categoryDisplayName") or f"[{cat_tag}] {ag['name']}"
        ge_disp = ag.get("geDisplayName") or disp[:58]
        desc = ag.get("categorizedDescription") or f"[Category: {cat_full}] {ag.get('shortDesc', ag['name'])}"
        model = "gemini-3.8-flash" if any(k in aid for k in ("vision", "inspection", "rma", "sanitation", "cold_chain", "batch_record")) else "gemini-3.1-pro-preview"

        merged[aid] = {
            "section": cat_tag,
            "category": cat_full,
            "display_name": disp,
            "legacy_display_name": ag["name"],
            "ge_display_name": ge_disp,
            "legacy_ge_display_name": ag["name"],
            "description": desc,
            "model": model,
            "icon": "smart_toy",
            "app_class": app_class,
            "tool_description": f"[{cat_tag}] Use {ag['name']} ({cat_full}) to analyze enterprise telemetry and commit governed ERP actions.",
            "starter_prompts": [
                f"Run {ag['name']} diagnostic on FAC-PLANT-US-AUS01",
                f"Evaluate constraint matrix and optimization scenarios for {ag['name']}",
                f"Commit verified ERP write-back action for SKU-SEMI-9900-X1",
                f"Show KPI impact summary for {cat_full}",
            ],
        }
    return merged


ALL_AGENTS_CONFIG = build_all_60_agents_config()

_TOKEN_OVERRIDE: str | None = None


def get_token() -> str | None:
    if _TOKEN_OVERRIDE:
        return _TOKEN_OVERRIDE
    if os.environ.get("GCP_ACCESS_TOKEN"):
        return os.environ["GCP_ACCESS_TOKEN"]
    adc_p = Path(os.path.expanduser("~/.config/gcloud/argolis_admin_adc.json"))
    if adc_p.exists():
        try:
            import google.oauth2.credentials
            from google.auth.transport.requests import Request
            c = google.oauth2.credentials.Credentials.from_authorized_user_file(
                str(adc_p), scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            c.refresh(Request())
            return c.token
        except Exception:
            pass
    try:
        tok = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if tok:
            return tok
    except Exception:
        pass
    return None


def get_credentials():
    adc_p = Path(os.path.expanduser("~/.config/gcloud/argolis_admin_adc.json"))
    if adc_p.exists():
        try:
            import google.oauth2.credentials
            from google.auth.transport.requests import Request
            c = google.oauth2.credentials.Credentials.from_authorized_user_file(
                str(adc_p), scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            c.refresh(Request())
            return c
        except Exception:
            pass
    tok = get_token()
    if tok:
        import google.oauth2.credentials
        return google.oauth2.credentials.Credentials(tok)
    import google.auth
    creds, _ = google.auth.default()
    return creds


def api(
    method: str,
    url: str,
    body: dict | None = None,
    token: str | None = None,
    project: str | None = None,
    ok404: bool = False,
) -> dict:
    tok = token or get_token()
    headers = {"Content-Type": "application/json"}
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    if project:
        headers["X-Goog-User-Project"] = project

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode() if body is not None else None,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="ignore")
        if ok404 and e.code == 404:
            return {"_404": True}
        raise RuntimeError(f"{method} {url} -> {e.code}: {txt[:350]}") from None


def enable_apis(project: str) -> None:
    services = [
        "aiplatform.googleapis.com",
        "storage.googleapis.com",
        "discoveryengine.googleapis.com",
        "bigquery.googleapis.com",
        "logging.googleapis.com",
    ]
    try:
        api("POST", f"https://serviceusage.googleapis.com/v1/projects/{project}/services:batchEnable",
            {"serviceIds": services}, project=project)
        print(f"[OK] APIs verified ({len(services)}) in {project}")
    except RuntimeError as e:
        print(f"[NOTE] ServiceUsage batchEnable notice: {str(e)[:160]}")


def ensure_bucket(project: str, region: str, name: str) -> str:
    r = api("GET", f"https://storage.googleapis.com/storage/v1/b/{name}", project=project, ok404=True)
    if r.get("_404"):
        try:
            api("POST", f"https://storage.googleapis.com/storage/v1/b?project={project}",
                {"name": name, "location": region, "iamConfiguration": {"uniformBucketLevelAccess": {"enabled": True}}},
                project=project)
            print(f"[CREATED] gs://{name} ({region})")
        except Exception as e:
            print(f"[WARN] Bucket create note: {e}")
    else:
        print(f"[OK] Bucket gs://{name}")
    return name


REQUIREMENTS = [
    "google-cloud-aiplatform[agent_engines,adk]>=1.160.0",
    "google-adk>=2.6.0,<3.0.0",
    "google-genai>=1.20.0",
    "google-cloud-storage>=2.18.0,<4.0.0",
    "google-cloud-bigquery>=3.25.0",
    "pydantic>=2.0.0",
]


def deploy_agent_engine(
    agent_id: str,
    spec: Dict[str, Any],
    project: str,
    region: str,
    staging_bucket: str,
    dry_run: bool = False,
) -> str:
    """Deploys or updates the agent IN-PLACE on Vertex AI Agent Engine (reusing existing resources)."""
    display_name = spec["display_name"]
    legacy_display_name = spec.get("legacy_display_name", display_name)
    agent_dir = ROOT / "agents" / agent_id

    for mod_name in list(sys.modules.keys()):
        if mod_name == "app" or mod_name.startswith("app."):
            del sys.modules[mod_name]

    sys.path.insert(0, str(agent_dir))
    try:
        mod = importlib.import_module("app.agent")
        root_agent = getattr(mod, "root_agent")
        app_cls = getattr(mod, spec["app_class"])
    except Exception as e:
        raise RuntimeError(f"Failed to load agent {agent_id}: {e}") from e
    finally:
        if str(agent_dir) in sys.path:
            sys.path.remove(str(agent_dir))

    if dry_run:
        state_file = agent_dir / ".reasoning_engine_id"
        cached = state_file.read_text().strip() if state_file.exists() else f"projects/{project}/locations/{region}/reasoningEngines/verified-{agent_id}"
        print(f"[DRY-RUN VERIFIED] Loaded {spec['app_class']} ({display_name}) | model={spec['model']} | reuse={cached}")
        return cached

    import google.auth
    import vertexai
    from vertexai import agent_engines

    creds = get_credentials()
    google.auth.default = lambda *a, **k: (creds, project)
    vertexai.init(project=project, location=region, staging_bucket=f"gs://{staging_bucket}", credentials=creds)

    adk_app = app_cls(agent=root_agent)
    env_vars = {
        "GOOGLE_GENAI_USE_VERTEXAI": "TRUE",
        "SC_AGENT_ID": agent_id,
        "SC_AGENT_CATEGORY": spec.get("category", spec["section"]),
        "SC_MODEL": spec["model"],
    }

    prev_cwd = os.getcwd()
    os.chdir(agent_dir)
    try:
        extra_packages = ["app"]
        if (agent_dir / "fixtures").exists():
            extra_packages.append("fixtures")

        kwargs = dict(
            agent_engine=adk_app,
            requirements=REQUIREMENTS,
            extra_packages=extra_packages,
            gcs_dir_name=agent_id,
            display_name=display_name,
            description=spec["description"],
            env_vars=env_vars,
            resource_limits={"cpu": "2", "memory": "4Gi"},
            min_instances=1,
        )

        state_file = agent_dir / ".reasoning_engine_id"
        existing = None
        if state_file.exists():
            try:
                cached_id = state_file.read_text().strip()
                existing = agent_engines.get(cached_id).resource_name
            except Exception:
                existing = None

        if not existing:
            try:
                for eng in agent_engines.list():
                    dname = getattr(eng, "display_name", "")
                    if dname in (display_name, legacy_display_name):
                        existing = eng.resource_name
                        break
            except Exception as e:
                print(f"[WARN] Error listing reasoning engines: {e}")

        t0 = time.time()
        if existing:
            print(f"[{agent_id}] REUSING & UPDATING IN PLACE: {existing}")
            eng = agent_engines.get(existing).update(**kwargs)
        else:
            print(f"[{agent_id}] CREATING Reasoning Engine '{display_name}' in {project}/{region} ...")
            eng = agent_engines.create(**kwargs)

        res = eng.resource_name
        state_file.write_text(res)
        metadata = {
            "agent_id": agent_id,
            "category": spec.get("category", spec["section"]),
            "display_name": display_name,
            "ge_display_name": spec["ge_display_name"],
            "section": spec["section"],
            "project_id": project,
            "region": region,
            "reasoning_engine_resource_name": res,
            "model": spec["model"],
            "deployed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        (agent_dir / "deployment_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        print(f"[{agent_id}] OK in {time.time() - t0:.1f}s: {res}")
        return res
    finally:
        os.chdir(prev_cwd)


def register_gemini_enterprise(
    agent_id: str,
    spec: Dict[str, Any],
    project: str,
    engine_resource_name: str,
    app_id: str,
    app_location: str = "global",
    dry_run: bool = False,
) -> None:
    """Registers or updates the agent in Gemini Enterprise IN-PLACE (matching by Reasoning Engine or Display Name)."""
    ge_display = spec["ge_display_name"]
    legacy_ge_display = spec.get("legacy_ge_display_name", ge_display)
    icon_name = spec["icon"]
    icon_url = f"https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/{icon_name}/default/24px.svg"

    payload = {
        "displayName": ge_display,
        "description": spec["description"],
        "icon": {"uri": icon_url},
        "starterPrompts": [{"text": p} for p in spec["starter_prompts"]],
        "adkAgentDefinition": {
            "toolSettings": {"toolDescription": spec["tool_description"]},
            "provisionedReasoningEngine": {"reasoningEngine": engine_resource_name},
        },
    }

    if dry_run:
        print(f"[DRY-RUN] Would update/register in Gemini Enterprise '{app_id}': {ge_display} -> {engine_resource_name}")
        return

    host = "discoveryengine.googleapis.com" if app_location == "global" else f"{app_location}-discoveryengine.googleapis.com"
    base = (
        f"https://{host}/v1alpha/projects/{project}/locations/{app_location}/collections/default_collection/"
        f"engines/{app_id}/assistants/default_assistant/agents"
    )

    try:
        agents = api("GET", base, project=project).get("agents", [])
        # Match existing agent by provisionedReasoningEngine first (100% resource reuse), then by current or legacy displayName
        cur = None
        for a in agents:
            re_ref = (
                a.get("adkAgentDefinition", {})
                .get("provisionedReasoningEngine", {})
                .get("reasoningEngine", "")
            )
            if re_ref and engine_resource_name and re_ref.split("/")[-1] == engine_resource_name.split("/")[-1]:
                cur = a["name"]
                break
            if a.get("displayName") in (ge_display, legacy_ge_display):
                cur = a["name"]
                break

        if cur:
            res = api(
                "PATCH",
                f"https://{host}/v1alpha/{cur}?updateMask=displayName,description,icon,starterPrompts,adkAgentDefinition",
                body={**payload, "name": cur},
                project=project,
            )
            print(f"[{agent_id}] GE REUSED & UPDATED IN-PLACE: {res.get('name', cur)} -> '{ge_display}'")
        else:
            res = api("POST", base, body=payload, project=project)
            print(f"[{agent_id}] GE REGISTERED: {res.get('name')} -> '{ge_display}'")
    except RuntimeError as e:
        print(f"[{agent_id}] GE NOTE: {str(e)[:300]}")


def main() -> None:
    global _TOKEN_OVERRIDE
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--agent", choices=list(ALL_AGENTS_CONFIG.keys()), help="Deploy a single agent (any of 60)")
    parser.add_argument("--all-flagship", action="store_true", help="Deploy/update the 14 provisioned flagship agents in-place")
    parser.add_argument("--all-60", action="store_true", help="Deploy/update all 60 catalog agents")
    parser.add_argument("--project", default=os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai"))
    parser.add_argument("--region", default="us-central1")
    parser.add_argument("--gemini-app-id", default="gemini-enterprise-zuhaibp_1784012666241")
    parser.add_argument("--gemini-app-location", default="global")
    parser.add_argument("--staging-bucket", default="")
    parser.add_argument("--media-bucket", default="")
    parser.add_argument("--token", default="", help="OAuth2 access token override")
    parser.add_argument("--skip-ge", action="store_true", help="Skip registration in Gemini Enterprise")
    parser.add_argument("--skip-engine", action="store_true", help="Skip Vertex AI Agent Engine deployment")
    parser.add_argument("--parallel", type=int, default=1, help="Number of parallel Reasoning Engine deploy workers")
    parser.add_argument("--dry-run", action="store_true", help="Dry run without calling GCP mutating APIs")
    args = parser.parse_args()

    if args.token:
        _TOKEN_OVERRIDE = args.token

    if not args.agent and not args.all_flagship and not args.all_60:
        parser.error("Specify --agent <agent_id>, --all-flagship, or --all-60")

    if args.all_60:
        targets = list(ALL_AGENTS_CONFIG.keys())
    elif args.all_flagship:
        targets = list(FLAGSHIP_CONFIG.keys())
    else:
        targets = [args.agent]

    staging_bucket = args.staging_bucket or f"{args.project}-agent-staging"
    media_bucket = args.media_bucket or f"{args.project}-supply-chain-media"

    print("==================================================================")
    print(" 🚀 Supply Chain Categorized ADK Deployer (Resource Reuse Enabled)")
    print(f" Target Project : {args.project}")
    print(f" Vertex Region  : {args.region}")
    print(f" GE App ID      : {args.gemini_app_id}")
    print(f" Agent Count    : {len(targets)} agents")
    print(f" Parallelism    : {args.parallel} workers")
    print(f" Dry Run Mode   : {args.dry_run}")
    print("==================================================================")

    if not args.dry_run and not args.skip_engine:
        enable_apis(args.project)
        ensure_bucket(args.project, args.region, staging_bucket)
        ensure_bucket(args.project, args.region, media_bucket)

    deployed_summary = []

    if args.parallel > 1 and len(targets) > 1 and not args.dry_run and not args.skip_engine:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def _run_child_engine(aid: str) -> tuple[str, int, str]:
            cmd = [
                sys.executable,
                str(Path(__file__).resolve()),
                "--agent", aid,
                "--project", args.project,
                "--region", args.region,
                "--staging-bucket", staging_bucket,
                "--media-bucket", media_bucket,
                "--skip-ge",
            ]
            print(f"[PARALLEL START] Launching Reasoning Engine update for {aid} ...")
            proc = subprocess.run(cmd, capture_output=True, text=True)
            out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
            for line in out.splitlines():
                if any(k in line for k in (f"[{aid}]", "ERROR", "WARN", "CREATING", "REUSING")):
                    print(line, flush=True)
            return aid, proc.returncode, out

        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            futs = {pool.submit(_run_child_engine, aid): aid for aid in targets}
            for fut in as_completed(futs):
                aid, rc, out = fut.result()
                if rc != 0:
                    print(f"[{aid}] Child deploy exited with code {rc}:\n{out[-600:]}")

        for idx, agent_id in enumerate(targets, 1):
            spec = ALL_AGENTS_CONFIG[agent_id]
            state_file = ROOT / "agents" / agent_id / ".reasoning_engine_id"
            engine_res = state_file.read_text().strip() if state_file.exists() else ""
            if not args.skip_ge and engine_res:
                try:
                    register_gemini_enterprise(
                        agent_id,
                        spec,
                        args.project,
                        engine_res,
                        args.gemini_app_id,
                        args.gemini_app_location,
                        dry_run=args.dry_run,
                    )
                except Exception as e:
                    print(f"[{agent_id}] ERROR registering in Gemini Enterprise: {e}")
            deployed_summary.append({
                "agent_id": agent_id,
                "category": spec.get("category", spec["section"]),
                "section": spec["section"],
                "display_name": spec["display_name"],
                "ge_display_name": spec["ge_display_name"],
                "description": spec["description"],
                "model": spec["model"],
                "reasoning_engine": engine_res,
            })
    else:
        for idx, agent_id in enumerate(targets, 1):
            spec = ALL_AGENTS_CONFIG[agent_id]
            print(f"\n--- [{idx}/{len(targets)}] {agent_id} ({spec['section']}) ---")
            engine_res = ""
            if not args.skip_engine:
                try:
                    engine_res = deploy_agent_engine(
                        agent_id, spec, args.project, args.region, staging_bucket, dry_run=args.dry_run
                    )
                except Exception as e:
                    print(f"[{agent_id}] ERROR deploying Reasoning Engine: {e}")
                    if not args.dry_run:
                        continue
            else:
                state_file = ROOT / "agents" / agent_id / ".reasoning_engine_id"
                if state_file.exists():
                    engine_res = state_file.read_text().strip()

            if not args.skip_ge and engine_res:
                try:
                    register_gemini_enterprise(
                        agent_id,
                        spec,
                        args.project,
                        engine_res,
                        args.gemini_app_id,
                        args.gemini_app_location,
                        dry_run=args.dry_run,
                    )
                except Exception as e:
                    print(f"[{agent_id}] ERROR registering in Gemini Enterprise: {e}")

            deployed_summary.append({
                "agent_id": agent_id,
                "category": spec.get("category", spec["section"]),
                "section": spec["section"],
                "display_name": spec["display_name"],
                "ge_display_name": spec["ge_display_name"],
                "description": spec["description"],
                "model": spec["model"],
                "reasoning_engine": engine_res,
            })

    # Update deployment_metadata.json
    all_deployed = []
    for aid, aspec in FLAGSHIP_CONFIG.items():
        meta_file = ROOT / "agents" / aid / "deployment_metadata.json"
        state_file = ROOT / "agents" / aid / ".reasoning_engine_id"
        re_name = state_file.read_text().strip() if state_file.exists() else ""
        deployed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        if meta_file.exists():
            try:
                m = json.loads(meta_file.read_text(encoding="utf-8"))
                re_name = m.get("reasoning_engine_resource_name", re_name)
                deployed_at = m.get("deployed_at", deployed_at)
            except Exception:
                pass
        all_deployed.append({
            "agent_id": aid,
            "category": aspec.get("category", aspec["section"]),
            "section": aspec["section"],
            "display_name": aspec["display_name"],
            "ge_display_name": aspec["ge_display_name"],
            "description": aspec["description"],
            "model": aspec["model"],
            "reasoning_engine": re_name,
            "deployed_at": deployed_at,
        })

    summary_path = ROOT / "deployment_metadata.json"
    summary_data = {
        "project_id": args.project,
        "region": args.region,
        "gemini_app_id": args.gemini_app_id,
        "agents_deployed": all_deployed,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    summary_path.write_text(json.dumps(summary_data, indent=2) + "\n")
    print(f"\n✅ Deployment pipeline finished! Summary ({len(all_deployed)} agents) saved to {summary_path}")


if __name__ == "__main__":
    main()
