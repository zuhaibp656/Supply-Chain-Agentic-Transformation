#!/usr/bin/env python3
"""Idempotent Deployer: Supply Chain ADK Agents -> Vertex AI Agent Engine -> Gemini Enterprise.

Key Capabilities:
  - Names every agent in BOTH Vertex AI Agent Engine and Gemini Enterprise using the exact
    Website & Playbook name plus `(Pillar · Sub-Pillar)` in brackets:
      `<Website Agent Name> (<Pillar> · <Sub-Pillar>)`
    e.g. `Demand Sensing Agent (01 · Plan · Demand Forecasting)`,
         `Cold-Chain Auditor (05 · Logistics · First & Mid-Mile)`,
         `Freight Bill Audit Agent (05 · Logistics · Route & Carrier)`.
  - Overwrites / updates existing Vertex AI Reasoning Engines (`.reasoning_engine_id`) and
    existing Gemini Enterprise agent registrations (`provisionedReasoningEngine` match) IN-PLACE
    with zero duplicate deployments.
  - Syncs fresh `admin@zuhaibp.altostrat.com` OAuth credentials from `~/.config/gcloud/credentials.db`
    so CloudTop VSCode credential helper overrides never break Argolis authentication.
  - Supports `--curated-showcase` (25 high-ROI showcase agents spanning ALL 6 Pillars and ALL 20
    Sub-Pillars, including all 14 previously deployed Reasoning Engines updated in-place + 11 new
    sub-pillar leaders with extra Logistics depth), `--all-flagship`, `--all-60`, or `--agent <id>`.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
ROOT = Path(__file__).resolve().parent.parent
GCLOUD_DIR = Path.home() / ".config" / "gcloud"

# Canonical Website ID <-> Legacy Alias Directory pairs sharing a Reasoning Engine ID
ALIAS_SYNC_PAIRS: Dict[str, str] = {
    "predictive_oee_sentinel": "plant_oee_maintenance_agent",
    "inline_yield_guardian": "inline_quality_inspection_agent",
    "meio_safety_stock_agent": "echelon_inventory_allocator",
    "atp_order_promising_agent": "dynamic_order_promising_atp",
    "port_drayage_orchestrator": "ocean_port_drayage_orchestrator",
    "yard_dock_sequencer": "yard_dock_scheduling_agent",
    "freight_control_tower": "in_transit_control_tower",
}

# Legacy display names from earlier deployments so in-place matching catches 100% of prior resources
LEGACY_NAMES_BY_ID: Dict[str, List[str]] = {
    "csco_control_tower_copilot": [
        "CSCO Control Tower Copilot (TowerMind)",
        "[01 · Plan | S&OP / IBP] CSCO Control Tower Copilot (TowerMind)",
        "TowerMind Control Tower",
        "[Plan · S&OP/IBP] TowerMind Control Tower",
    ],
    "disruption_war_room_orchestrator": [
        "Disruption War Room Orchestrator (StormShield)",
        "[01 · Plan | S&OP / IBP] Disruption War Room Orchestrator (StormShield)",
        "StormShield War Room",
        "[Plan · S&OP/IBP] StormShield War Room",
    ],
    "demand_sensing_agent": [
        "Demand Sensing Engine (PulseCast)",
        "[01 · Plan | Demand Forecasting] Demand Sensing Engine (PulseCast)",
        "PulseCast Demand Sensing",
        "[Plan · Forecasting] PulseCast Demand Sensing",
    ],
    "sop_scenario_weaver": [
        "S&OP Scenario Weaver (Synapse)",
        "[01 · Plan | S&OP / IBP] S&OP Scenario Weaver (Synapse)",
        "Synapse S&OP Weaver",
        "[Plan · S&OP/IBP] Synapse S&OP Weaver",
    ],
    "rfq_should_cost_agent": [
        "Parametric Should-Cost & RFQ Agent (SourcePulse)",
        "[02 · Source | Material & Packaging] Parametric Should-Cost & RFQ Agent (SourcePulse)",
        "SourcePulse Should-Cost",
        "[Source · Material] SourcePulse Should-Cost",
    ],
    "tier_n_risk_sentinel": [
        "Multi-Tier Supply Network Sentinel (NexusShield)",
        "[02 · Source | Vendor Sourcing] Multi-Tier Supply Network Sentinel (NexusShield)",
        "NexusShield Risk Sentinel",
        "[Source · Vendor Risk] NexusShield Sentinel",
    ],
    "predictive_oee_sentinel": [
        "Plant OEE & Maintenance Guardian (AssetGuard)",
        "[03 · Make | Production Scheduling] Plant OEE & Maintenance Guardian (AssetGuard)",
        "AssetGuard Plant OEE",
        "[Make · OEE & Sched] AssetGuard Plant OEE",
    ],
    "plant_oee_maintenance_agent": [
        "Plant OEE & Maintenance Guardian (AssetGuard)",
        "AssetGuard Plant OEE",
    ],
    "inline_yield_guardian": [
        "Inline Multimodal Quality Inspector (VisionInspect)",
        "[03 · Make | Quality & Compliance] Inline Multimodal Quality Inspector (VisionInspect)",
        "VisionInspect Quality",
        "[Make · Quality] VisionInspect Quality",
    ],
    "inline_quality_inspection_agent": [
        "Inline Multimodal Quality Inspector (VisionInspect)",
        "VisionInspect Quality",
    ],
    "meio_safety_stock_agent": [
        "Multi-Echelon Inventory Allocator (EchelonFlow)",
        "[04 · Inventory & DC | Positioning & Optimization] Multi-Echelon Inventory Allocator (EchelonFlow)",
        "EchelonFlow MEIO",
        "[Inventory · MEIO] EchelonFlow Allocator",
    ],
    "echelon_inventory_allocator": [
        "Multi-Echelon Inventory Allocator (EchelonFlow)",
        "EchelonFlow MEIO",
    ],
    "atp_order_promising_agent": [
        "Sub-50ms Spanner ATP & Order Promising (PromiseGuard)",
        "[04 · Inventory & DC | Omnichannel Visibility] Sub-50ms Spanner ATP & Order Promising (PromiseGuard)",
        "PromiseGuard ATP",
        "[Inventory · Omnichannel] PromiseGuard ATP",
    ],
    "dynamic_order_promising_atp": [
        "Sub-50ms Spanner ATP & Order Promising (PromiseGuard)",
        "PromiseGuard ATP",
    ],
    "fleetflow_dispatch": [
        "Google Maps Corridor Route & Fleet Dispatch Studio (FleetFlow)",
        "[05 · Logistics | Last-Mile Delivery] Google Maps Corridor Route & Fleet Dispatch Studio (FleetFlow)",
        "FleetFlow Route & Dispatch",
        "[Logistics · Last-Mile] FleetFlow Dispatch",
    ],
    "load_consolidation_agent": [
        "Isometric LIFO Bay & 3D Load Consolidation Studio (CubeMaster 3D)",
        "[05 · Logistics | First & Mid-Mile] Isometric LIFO Bay & 3D Load Consolidation Studio (CubeMaster 3D)",
        "CubeMaster 3D Load Studio",
        "[Logistics · 3D Load] CubeMaster 3D Studio",
    ],
    "reverse_rma_optimizer": [
        "Autonomous RMA Grading & Circular Backhaul Optimizer (ReturnLoop)",
        "[06 · Returns & ESG | Returns & Claims Mgmt] Autonomous RMA Grading & Circular Backhaul Optimizer (ReturnLoop)",
        "ReturnLoop RMA & Backhaul",
        "[Returns · RMA Triage] ReturnLoop Optimizer",
    ],
    "carbon_scope3_ledger": [
        "Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger (EcoChain)",
        "[02 · Source | Vendor Sourcing] Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger (EcoChain)",
        "EcoChain Scope-3 & CBAM",
        "[Source · ESG & Carbon] EcoChain Scope-3",
    ],
}

# Google Material Symbols icon per agent (200 OK on fonts.gstatic.com/s/i/short-term/release/googlesymbols/<icon>/default/24px.svg)
AGENT_ICONS: Dict[str, str] = {
    "demand_sensing_agent": "trending_up",
    "promo_lift_simulator": "sell",
    "csco_control_tower_copilot": "hub",
    "sop_scenario_weaver": "tune",
    "disruption_war_room_orchestrator": "crisis_alert",
    "working_capital_cash_bridge": "account_balance",
    "tier_n_risk_sentinel": "security",
    "carbon_scope3_ledger": "eco",
    "rfq_should_cost_agent": "request_quote",
    "three_way_match_dispute": "receipt_long",
    "finite_production_scheduler": "schedule",
    "predictive_oee_sentinel": "precision_manufacturing",
    "inline_yield_guardian": "document_scanner",
    "meio_safety_stock_agent": "inventory_2",
    "warehouse_slotting_agent": "warehouse",
    "atp_order_promising_agent": "verified",
    "load_consolidation_agent": "view_in_ar",
    "cold_chain_auditor": "ac_unit",
    "port_drayage_orchestrator": "directions_boat",
    "geocoding_intelligence_agent": "pin_drop",
    "fleetflow_dispatch": "local_shipping",
    "freight_bill_audit_agent": "fact_check",
    "reverse_rma_optimizer": "assignment_return",
    "dynamic_markdown_agent": "loyalty",
    "rti_balance_reconciler": "inventory",
}

# 14 Canonical Website IDs corresponding to the 14 previously deployed Reasoning Engines
EXISTING_14_CANONICAL_IDS: List[str] = [
    "demand_sensing_agent",
    "sop_scenario_weaver",
    "disruption_war_room_orchestrator",
    "csco_control_tower_copilot",
    "tier_n_risk_sentinel",
    "carbon_scope3_ledger",
    "rfq_should_cost_agent",
    "predictive_oee_sentinel",
    "inline_yield_guardian",
    "meio_safety_stock_agent",
    "atp_order_promising_agent",
    "load_consolidation_agent",
    "fleetflow_dispatch",
    "reverse_rma_optimizer",
]

# 25 Curated Showcase Agents:
# - Updates ALL 14 existing Reasoning Engines IN-PLACE with Website Name + (Pillar · Sub-Pillar)
# - Adds 11 high-value showcase agents so ALL 20 Sub-Pillars across ALL 6 Pillars have >=1 live agent,
#   with 6 flagship showcase agents in 05 · Logistics (First/Mid-Mile, Cold-Chain, Store Curfew, Geocoding, Dynamic Rerouter, Freight Bill Audit).
CURATED_SHOWCASE_25_IDS: List[str] = [
    # 01 · Plan (4 Sub-Pillars: Demand Forecasting, Trade Promotion, S&OP / IBP, Portfolio & SKU)
    "demand_sensing_agent",             # (01 · Plan · Demand Forecasting) — In-Place RE Update
    "promo_lift_simulator",             # (01 · Plan · Trade Promotion) — New Sub-Pillar Showcase
    "csco_control_tower_copilot",       # (01 · Plan · S&OP / IBP) — In-Place RE Update
    "sop_scenario_weaver",              # (01 · Plan · S&OP / IBP) — In-Place RE Update
    "disruption_war_room_orchestrator", # (01 · Plan · S&OP / IBP) — In-Place RE Update
    "working_capital_cash_bridge",      # (01 · Plan · Portfolio & SKU) — New Sub-Pillar Showcase

    # 02 · Source (3 Sub-Pillars: Supplier Network, Material & Packaging, Contract & PO Mgmt)
    "tier_n_risk_sentinel",             # (02 · Source · Supplier Network) — In-Place RE Update
    "carbon_scope3_ledger",             # (02 · Source · Supplier Network) — In-Place RE Update
    "rfq_should_cost_agent",            # (02 · Source · Material & Packaging) — In-Place RE Update
    "three_way_match_dispute",          # (02 · Source · Contract & PO Mgmt) — New Sub-Pillar Showcase

    # 03 · Make (3 Sub-Pillars: Production Scheduling, Capacity Planning, Quality & Compliance)
    "finite_production_scheduler",      # (03 · Make · Production Scheduling) — New Sub-Pillar Showcase
    "predictive_oee_sentinel",          # (03 · Make · Capacity Planning) — In-Place RE Update
    "inline_yield_guardian",            # (03 · Make · Quality & Compliance) — In-Place RE Update

    # 04 · Inventory & DC (3 Sub-Pillars: Positioning & Optimization, Warehouse Operations, Omnichannel Visibility)
    "meio_safety_stock_agent",          # (04 · Inventory & DC · Positioning & Optimization) — In-Place RE Update
    "warehouse_slotting_agent",         # (04 · Inventory & DC · Warehouse Operations) — New Sub-Pillar Showcase
    "atp_order_promising_agent",        # (04 · Inventory & DC · Omnichannel Visibility) — In-Place RE Update

    # 05 · Logistics (4 Sub-Pillars: First & Mid-Mile, Store Replenishment, Last-Mile Delivery, Route & Carrier)
    "load_consolidation_agent",         # (05 · Logistics · First & Mid-Mile) — In-Place RE Update
    "cold_chain_auditor",               # (05 · Logistics · First & Mid-Mile) — New Logistics Showcase (Arrhenius MKT °C)
    "port_drayage_orchestrator",        # (05 · Logistics · Store Replenishment) — New Sub-Pillar Showcase
    "geocoding_intelligence_agent",     # (05 · Logistics · Last-Mile Delivery) — New Sub-Pillar Showcase (Haversine Drift)
    "fleetflow_dispatch",               # (05 · Logistics · Route & Carrier) — In-Place RE Update
    "freight_bill_audit_agent",         # (05 · Logistics · Route & Carrier) — New Logistics Showcase (EDI 210 + DOE FSC)

    # 06 · Returns & ESG (3 Sub-Pillars: Returns & Claims Mgmt, Expiry & Markdowns, Pallet & Tote Reclamation)
    "reverse_rma_optimizer",            # (06 · Returns & ESG · Returns & Claims Mgmt) — In-Place RE Update
    "dynamic_markdown_agent",           # (06 · Returns & ESG · Expiry & Markdowns) — New Sub-Pillar Showcase
    "rti_balance_reconciler",           # (06 · Returns & ESG · Pallet & Tote Reclamation) — New Sub-Pillar Showcase
]


def _detect_agent_model_and_class(agent_dir: Path, aid: str) -> tuple[str, str]:
    app_class = "".join(w.capitalize() for w in aid.split("_") if w) + "AdkApp"
    model = "gemini-3.1-pro-preview"
    agent_py = agent_dir / "app" / "agent.py"
    if agent_py.exists():
        txt = agent_py.read_text(encoding="utf-8")
        m_cls = re.search(r"class\s+(\w+)\(AdkApp\):", txt)
        if m_cls:
            app_class = m_cls.group(1)
        m_mod = re.search(r'GlobalGemini\(\s*model=["\']([^"\']+)["\']', txt)
        if m_mod:
            model = m_mod.group(1)
    return app_class, model


def _build_playbook_starter_prompts(website_name: str, bracket_label: str) -> List[str]:
    """Builds 4 crisp Playbook-aligned starter prompts (Diagnostic, Chart, Brief Draft, Write-Back Check)."""
    return [
        f"Run a read-only {website_name} diagnostic on XYZ-CORP-01 data and show the top KPI table.",
        f"Analyze operational metrics for {website_name} and render the visual comparison chart.",
        f"Draft a concise {website_name} operational action brief citing exact XYZ-CORP-01 IDs and variances.",
        f"Show the recommended {bracket_label} remediation action and verify pre-execution safety gates.",
    ]


def build_all_60_agents_config() -> Dict[str, Dict[str, Any]]:
    """Builds deployment specs for all 60 catalog agents using `<Website Name> (<Pillar> · <Sub-Pillar>)`."""
    cat_path = ROOT / "data" / "supply_chain_catalog.json"
    cat = json.loads(cat_path.read_text(encoding="utf-8"))
    configs: Dict[str, Dict[str, Any]] = {}

    suman_pillar_prefix = {
        "demand_sop": "01 · Planning & Strategy",
        "sourcing_procurement": "02 · Sourcing & Procurement",
        "manufacturing_prod": "03 · Manufacturing & Production",
        "inventory_warehouse": "04 · Inventory & Warehousing",
        "logistics_fleet": "05 · Distribution & Logistics",
        "circular_enable": "06 · Returns & Reverse Logistics",
    }

    for aid, ag in cat.get("agents", {}).items():
        agent_dir = ROOT / "agents" / aid
        app_class, model = _detect_agent_model_and_class(agent_dir, aid)

        website_name = ag["name"].strip()
        dept_id = ag.get("deptId", "demand_sop")
        pillar_label = suman_pillar_prefix.get(dept_id, "01 · Planning & Strategy")
        sub_pillar = (ag.get("subPillarName") or "General").strip()
        cat_tag = ag.get("categoryTag", f"{pillar_label} | {sub_pillar}").strip()
        short_bracket_label = cat_tag.replace(" | ", " · ")
        bracket_label = f"{pillar_label} · {sub_pillar}"
        cat_full = f"{pillar_label} | {sub_pillar}"

        # Exact format requested: `<Website Agent Name> (<Pillar> · <Sub-Pillar>)` aligned 100% with Suman's PPT
        unified_display_name = f"{website_name} ({bracket_label})"

        short_desc = ag.get("shortDesc") or ag.get("solution") or website_name
        outcome = ag.get("outcome") or ""
        desc = f"[{bracket_label}] {website_name} — {short_desc}"
        if outcome and outcome not in desc:
            desc = f"{desc} Outcome: {outcome}"

        legacy_list = list(LEGACY_NAMES_BY_ID.get(aid, []))
        for candidate in (
            website_name,
            f"{website_name} ({short_bracket_label})",
            ag.get("categoryDisplayName", ""),
            ag.get("geDisplayName", ""),
            f"[{cat_tag}] {website_name}",
        ):
            if candidate and candidate not in legacy_list:
                legacy_list.append(candidate)

        configs[aid] = {
            "section": cat_full,
            "bracket_label": bracket_label,
            "category": cat_full,
            "website_name": website_name,
            "display_name": unified_display_name,
            "ge_display_name": unified_display_name,
            "legacy_names": legacy_list,
            "description": desc[:480],
            "model": model,
            "icon": AGENT_ICONS.get(aid, "smart_toy"),
            "app_class": app_class,
            "tool_description": (
                f"({bracket_label}) Invoke {website_name} to query XYZ-CORP-01 enterprise tables, "
                f"run deterministic Python optimization math, render interactive VegaChart cards, "
                f"draft persona briefs, and execute governed ERP/WMS/TMS write-backs."
            ),
            "starter_prompts": _build_playbook_starter_prompts(website_name, bracket_label),
        }

    return configs


ALL_AGENTS_CONFIG = build_all_60_agents_config()

_TOKEN_OVERRIDE: str | None = None


def sync_gcloud_db_to_argolis_adc(project: str) -> None:
    """Syncs fresh admin@zuhaibp.altostrat.com OAuth refresh_token from gcloud credentials.db to ADC."""
    db_path = GCLOUD_DIR / "credentials.db"
    if not db_path.exists():
        return
    try:
        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        cur.execute("SELECT account_id, value FROM credentials")
        for account_id, val in cur.fetchall():
            if "zuhaibp.altostrat.com" in account_id:
                data = json.loads(val)
                if data.get("refresh_token") and data.get("client_id"):
                    payload = {
                        "account": account_id,
                        "client_id": data["client_id"],
                        "client_secret": data["client_secret"],
                        "refresh_token": data["refresh_token"],
                        "type": "authorized_user",
                        "quota_project_id": project,
                    }
                    for target in (
                        GCLOUD_DIR / "argolis_admin_adc.json",
                        GCLOUD_DIR / "application_default_credentials.json",
                    ):
                        target.write_text(json.dumps(payload, indent=2) + "\n")
                break
        conn.close()
    except Exception:
        pass


def get_token() -> str | None:
    if _TOKEN_OVERRIDE:
        return _TOKEN_OVERRIDE
    if os.environ.get("GCP_ACCESS_TOKEN"):
        return os.environ["GCP_ACCESS_TOKEN"]
    adc_p = GCLOUD_DIR / "argolis_admin_adc.json"
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
    adc_p = GCLOUD_DIR / "argolis_admin_adc.json"
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
        api(
            "POST",
            f"https://serviceusage.googleapis.com/v1/projects/{project}/services:batchEnable",
            {"serviceIds": services},
            project=project,
        )
        print(f"[OK] APIs verified ({len(services)}) in {project}")
    except RuntimeError as e:
        print(f"[NOTE] ServiceUsage batchEnable notice: {str(e)[:160]}")


def ensure_bucket(project: str, region: str, name: str) -> str:
    r = api("GET", f"https://storage.googleapis.com/storage/v1/b/{name}", project=project, ok404=True)
    if r.get("_404"):
        try:
            api(
                "POST",
                f"https://storage.googleapis.com/storage/v1/b?project={project}",
                {"name": name, "location": region, "iamConfiguration": {"uniformBucketLevelAccess": {"enabled": True}}},
                project=project,
            )
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
    "Pillow>=10.0.0",
]


def _write_reasoning_engine_state(agent_id: str, resource_name: str, metadata: Dict[str, Any]) -> None:
    agent_dir = ROOT / "agents" / agent_id
    (agent_dir / ".reasoning_engine_id").write_text(resource_name + "\n")
    (agent_dir / "deployment_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    # Sync paired alias directory if present
    alias_id = ALIAS_SYNC_PAIRS.get(agent_id)
    if alias_id and (ROOT / "agents" / alias_id).is_dir():
        (ROOT / "agents" / alias_id / ".reasoning_engine_id").write_text(resource_name + "\n")
        (ROOT / "agents" / alias_id / "deployment_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")


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
    legacy_names = set(spec.get("legacy_names", [])) | {display_name}
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
        cached = state_file.read_text().strip() if state_file.exists() else f"projects/{project}/locations/{region}/reasoningEngines/NEW-{agent_id}"
        mode = "IN-PLACE UPDATE" if state_file.exists() else "NEW CREATE"
        print(f"[DRY-RUN {mode}] {spec['app_class']} -> '{display_name}' | model={spec['model']} | re={cached.split('/')[-1]}")
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
                    if dname in legacy_names:
                        existing = eng.resource_name
                        break
            except Exception as e:
                print(f"[WARN] Error listing reasoning engines: {e}")

        t0 = time.time()
        if existing:
            print(f"[{agent_id}] REUSING & UPDATING IN PLACE: {existing} -> '{display_name}'")
            eng = agent_engines.get(existing).update(**kwargs)
        else:
            print(f"[{agent_id}] CREATING Reasoning Engine '{display_name}' in {project}/{region} ...")
            eng = agent_engines.create(**kwargs)

        res = eng.resource_name
        metadata = {
            "agent_id": agent_id,
            "website_name": spec["website_name"],
            "bracket_label": spec["bracket_label"],
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
        _write_reasoning_engine_state(agent_id, res, metadata)
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
) -> str:
    """Registers or updates the agent in Gemini Enterprise IN-PLACE (matching by Reasoning Engine or Display Name)."""
    ge_display = spec["ge_display_name"]
    legacy_names = set(spec.get("legacy_names", [])) | {ge_display}
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
        print(f"[DRY-RUN GE] '{ge_display}' -> {engine_resource_name.split('/')[-1]}")
        return f"dry-run-ge-{agent_id}"

    host = "discoveryengine.googleapis.com" if app_location == "global" else f"{app_location}-discoveryengine.googleapis.com"
    base = (
        f"https://{host}/v1alpha/projects/{project}/locations/{app_location}/collections/default_collection/"
        f"engines/{app_id}/assistants/default_assistant/agents"
    )

    agents = api("GET", base, project=project).get("agents", [])
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
        if a.get("displayName") in legacy_names:
            cur = a["name"]
            break

    if cur:
        res = api(
            "PATCH",
            f"https://{host}/v1alpha/{cur}?updateMask=displayName,description,icon,starterPrompts,adkAgentDefinition",
            body={**payload, "name": cur},
            project=project,
        )
        ge_name = res.get("name", cur)
        print(f"[{agent_id}] GE UPDATED IN-PLACE: {ge_name.split('/')[-1]} -> '{ge_display}'")
    else:
        res = api("POST", base, body=payload, project=project)
        ge_name = res.get("name", "")
        print(f"[{agent_id}] GE REGISTERED NEW: {ge_name.split('/')[-1]} -> '{ge_display}'")

    # Persist GE agent resource name in deployment_metadata.json
    meta_file = ROOT / "agents" / agent_id / "deployment_metadata.json"
    if meta_file.exists():
        try:
            m = json.loads(meta_file.read_text(encoding="utf-8"))
            m["gemini_enterprise_agent_name"] = ge_name
            meta_file.write_text(json.dumps(m, indent=2) + "\n")
        except Exception:
            pass
    return ge_name


def main() -> None:
    global _TOKEN_OVERRIDE
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--agent", choices=list(ALL_AGENTS_CONFIG.keys()), help="Deploy a single catalog agent (any of 60)")
    parser.add_argument(
        "--curated-showcase",
        action="store_true",
        help="Deploy/update the 25 curated showcase agents (all 14 existing REs updated in-place + 11 sub-pillar leaders across all 20 sub-pillars)",
    )
    parser.add_argument("--all-flagship", action="store_true", help="Deploy/update the 14 previously provisioned flagship agents in-place")
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
    else:
        sync_gcloud_db_to_argolis_adc(args.project)

    if not (args.agent or args.curated_showcase or args.all_flagship or args.all_60):
        parser.error("Specify --agent <agent_id>, --curated-showcase, --all-flagship, or --all-60")

    if args.all_60:
        targets = list(ALL_AGENTS_CONFIG.keys())
    elif args.curated_showcase:
        targets = list(CURATED_SHOWCASE_25_IDS)
    elif args.all_flagship:
        targets = list(EXISTING_14_CANONICAL_IDS)
    else:
        targets = [args.agent]

    staging_bucket = args.staging_bucket or f"{args.project}-agent-staging"
    media_bucket = args.media_bucket or f"{args.project}-supply-chain-media"

    print("==================================================================")
    print(" 🚀 Supply Chain Website-Named ADK Deployer (In-Place Reuse)")
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
            print(f"[PARALLEL START] Launching Reasoning Engine build/update for {aid} -> '{ALL_AGENTS_CONFIG[aid]['display_name']}' ...", flush=True)
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
                    print(f"[{aid}] ERROR child deploy exited with code {rc}:\n{out[-800:]}", flush=True)

        for agent_id in targets:
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
                    print(f"[{agent_id}] ERROR registering in Gemini Enterprise: {e}", flush=True)
    else:
        for idx, agent_id in enumerate(targets, 1):
            spec = ALL_AGENTS_CONFIG[agent_id]
            print(f"\n--- [{idx}/{len(targets)}] {agent_id} -> {spec['display_name']} ---")
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

    # Rebuild root deployment_metadata.json across ALL catalog agents that currently have a .reasoning_engine_id
    all_deployed = []
    for aid, aspec in ALL_AGENTS_CONFIG.items():
        state_file = ROOT / "agents" / aid / ".reasoning_engine_id"
        if not state_file.exists():
            continue
        re_name = state_file.read_text().strip()
        if not re_name:
            continue
        meta_file = ROOT / "agents" / aid / "deployment_metadata.json"
        deployed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        ge_agent_name = ""
        if meta_file.exists():
            try:
                m = json.loads(meta_file.read_text(encoding="utf-8"))
                deployed_at = m.get("deployed_at", deployed_at)
                ge_agent_name = m.get("gemini_enterprise_agent_name", "")
            except Exception:
                pass
        all_deployed.append({
            "agent_id": aid,
            "website_name": aspec["website_name"],
            "bracket_label": aspec["bracket_label"],
            "category": aspec["category"],
            "section": aspec["section"],
            "display_name": aspec["display_name"],
            "ge_display_name": aspec["ge_display_name"],
            "description": aspec["description"],
            "model": aspec["model"],
            "reasoning_engine": re_name,
            "gemini_enterprise_agent": ge_agent_name,
            "deployed_at": deployed_at,
        })

    if not args.dry_run:
        summary_path = ROOT / "deployment_metadata.json"
        summary_data = {
            "project_id": args.project,
            "region": args.region,
            "gemini_app_id": args.gemini_app_id,
            "deployed_count": len(all_deployed),
            "agents_deployed": all_deployed,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        summary_path.write_text(json.dumps(summary_data, indent=2) + "\n")
        print(f"\n✅ Deployment pipeline finished! Live summary ({len(all_deployed)} agents) saved to {summary_path}")


if __name__ == "__main__":
    main()
