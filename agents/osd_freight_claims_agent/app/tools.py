"""Deterministic enterprise tools & quality gates for [06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
ACTION_EVENTS_PATH = FIXTURES / "action-events.jsonl"

SYSTEM_CONNECTORS: List[Dict[str, Any]] = [
    {"id": "sap_s4hana_erp", "name": "SAP S/4HANA & IBP Enterprise Connector", "protocol": "OData v4 / BAPI", "tables": ["osd_freight_claims_agent_telemetry_feed", "osd_freight_claims_agent_constraint_matrix"]},
    {"id": "bigquery_supply_chain_twin", "name": "BigQuery & Cloud Spanner Digital Twin", "protocol": "Storage Read API / SQL", "tables": ["osd_freight_claims_agent_optimization_scenarios", "osd_freight_claims_agent_execution_ledger"]},
]


def _read_json(table_filename: str) -> List[Dict[str, Any]]:
    candidates = [
        Path(__file__).resolve().parent.parent / "fixtures" / "tables" / table_filename,
        Path.cwd() / "fixtures" / "tables" / table_filename,
        Path("/code/fixtures/tables") / table_filename,
        FIXTURES / "tables" / table_filename,
    ]
    for p in candidates:
        try:
            if p.exists():
                return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    return []


def _append_action_event(tool_name: str, payload: Dict[str, Any]) -> None:
    for target in (ACTION_EVENTS_PATH, Path("/tmp/supply_chain_action_events.jsonl")):
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"tool": tool_name, **payload}, sort_keys=True) + "\n")
            return
        except Exception:
            continue


def _deterministic_id(prefix: str, seed: str) -> str:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8].upper()
    return f"{prefix}-{digest}"

def query_osd_freight_claims_agent_telemetry_feed(facility_id: str = "FAC-PLANT-US-AUS01") -> Dict[str, Any]:
    """Query `osd_freight_claims_agent_telemetry_feed` table for [06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims (06 · Returns & Reverse Logistics — Returns & Claims Mgmt)."""
    rows = _read_json("osd_freight_claims_agent_telemetry_feed.json")
    all_rows = list(rows)
    if facility_id and facility_id.upper() != "ALL":
        rows = [r for r in rows if str(r.get("facility_id", "")).lower() == str(facility_id).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "status": "SUCCESS",
        "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt",
        "table": "osd_freight_claims_agent_telemetry_feed",
        "filter": {"facility_id": facility_id},
        "row_count": len(rows),
        "rows": rows,
    }

def query_osd_freight_claims_agent_constraint_matrix(sku_id: str = "SKU-SEMI-9900-X1") -> Dict[str, Any]:
    """Query `osd_freight_claims_agent_constraint_matrix` table for [06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims (06 · Returns & Reverse Logistics — Returns & Claims Mgmt)."""
    rows = _read_json("osd_freight_claims_agent_constraint_matrix.json")
    all_rows = list(rows)
    if sku_id and sku_id.upper() != "ALL":
        rows = [r for r in rows if str(r.get("sku_id", "")).lower() == str(sku_id).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "status": "SUCCESS",
        "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt",
        "table": "osd_freight_claims_agent_constraint_matrix",
        "filter": {"sku_id": sku_id},
        "row_count": len(rows),
        "rows": rows,
    }

def query_osd_freight_claims_agent_optimization_scenarios(scenario_id: str = "SCEN-AI-OPTIMAL") -> Dict[str, Any]:
    """Query `osd_freight_claims_agent_optimization_scenarios` table for [06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims (06 · Returns & Reverse Logistics — Returns & Claims Mgmt)."""
    rows = _read_json("osd_freight_claims_agent_optimization_scenarios.json")
    all_rows = list(rows)
    if scenario_id and scenario_id.upper() != "ALL":
        rows = [r for r in rows if str(r.get("scenario_id", "")).lower() == str(scenario_id).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "status": "SUCCESS",
        "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt",
        "table": "osd_freight_claims_agent_optimization_scenarios",
        "filter": {"scenario_id": scenario_id},
        "row_count": len(rows),
        "rows": rows,
    }

def query_osd_freight_claims_agent_execution_ledger(shipment_id: str = "SHP-XYZ-90884") -> Dict[str, Any]:
    """Query `osd_freight_claims_agent_execution_ledger` table for [06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims (06 · Returns & Reverse Logistics — Returns & Claims Mgmt)."""
    rows = _read_json("osd_freight_claims_agent_execution_ledger.json")
    all_rows = list(rows)
    if shipment_id and shipment_id.upper() != "ALL":
        rows = [r for r in rows if str(r.get("shipment_id", "")).lower() == str(shipment_id).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "status": "SUCCESS",
        "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt",
        "table": "osd_freight_claims_agent_execution_ledger",
        "filter": {"shipment_id": shipment_id},
        "row_count": len(rows),
        "rows": rows,
    }


def action_commit_osd_freight_claims_agent_plan(
    target_node: str = "FAC-PLANT-US-AUS01",
    sku_id: str = "SKU-SEMI-9900-X1",
    confidence_score: float = 0.96,
) -> Dict[str, Any]:
    """Commit autonomous optimization write-back for [06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims after quality gate verification."""
    if confidence_score < 0.75:
        return {
            "status": "BLOCKED_BY_QUALITY_GATE",
            "reason": f"Confidence score {confidence_score} is below threshold 0.75.",
            "target_node": target_node,
        }
    action_id = _deterministic_id("ACT-OSD_", f"{target_node}:{sku_id}:{confidence_score}")
    receipt = {
        "action_id": action_id,
        "status": "COMMITTED",
        "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt",
        "agent": "[06 · Returns & ESG | Returns & Claims Mgmt] OS&D Freight Claims",
        "target_node": target_node,
        "sku_id": sku_id,
        "confidence_score": confidence_score,
        "erp_writeback": "SAP SD Alternate-DC Order Re-Allocation & Automated Retailer Portal Dispute Submission via Apigee",
    }
    _append_action_event("action_commit_osd_freight_claims_agent_plan", receipt)
    return receipt


def action_dispatch_osd_freight_claims_agent_alert(
    persona_recipient: str = "Claims Specialist / Controller",
    severity: str = "HIGH",
    summary: str = "Autonomous optimization committed",
) -> Dict[str, Any]:
    """Dispatch executive control tower notification to Claims Specialist / Controller."""
    if severity.upper() not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        return {"status": "BLOCKED_BY_QUALITY_GATE", "reason": f"Invalid severity: {severity}"}
    alert_id = _deterministic_id("ALT-OSD_", f"{persona_recipient}:{severity}:{summary}")
    receipt = {
        "action_id": alert_id,
        "status": "DISPATCHED",
        "category": "06 · Returns & Reverse Logistics — Returns & Claims Mgmt",
        "persona_recipient": persona_recipient,
        "severity": severity.upper(),
        "summary": summary,
    }
    _append_action_event("action_dispatch_osd_freight_claims_agent_alert", receipt)
    return receipt


ALL_TOOLS = [
    query_osd_freight_claims_agent_telemetry_feed,
    query_osd_freight_claims_agent_constraint_matrix,
    query_osd_freight_claims_agent_optimization_scenarios,
    query_osd_freight_claims_agent_execution_ledger,
    action_commit_osd_freight_claims_agent_plan,
    action_dispatch_osd_freight_claims_agent_alert,
]
