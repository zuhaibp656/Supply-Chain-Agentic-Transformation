"""Deterministic and fixture-backed tools for IntermodalSync — Factory-to-DC Intermodal Rail, Barge & Linehaul Orchestrator."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List

FIXTURES = Path(os.environ.get("FIXTURES_ROOT", str(Path(__file__).resolve().parent.parent / "fixtures")))
ACTION_EVENTS_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "action-events.jsonl"


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


def _deterministic_id(prefix: str, *parts: Any) -> str:
    payload = "|".join(str(p) for p in parts if p is not None and p != "")
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8].upper() if payload else "00000000"
    return f"{prefix}-{digest}"


def list_systems() -> Dict[str, Any]:
    """Returns connected enterprise systems and solver engines for intermodal_rail_linehaul_agent."""
    return {
        "agent": "intermodal_rail_linehaul_agent",
        "systems": [
            {
                        "id": "railinc_clm_edi417_feed",
                        "name": "Railinc Car Location Message (CLM) & Class-I Rail EDI 404/417 Gateway",
                        "protocol": "EDI 404 / 417 / REST",
                        "tables": [
                                    "railinc_edi417_train_consists"
                        ]
            },
            {
                        "id": "intermodal_lane_milp_solver",
                        "name": "Google OR-Tools OTR-to-Rail Intermodal Mode Conversion Solver",
                        "protocol": "Python MILP SDK",
                        "tables": [
                                    "intermodal_corridor_shipments",
                                    "otr_to_rail_mode_conversion_ledger"
                        ]
            },
            {
                        "id": "ramp_crane_drayage_sync",
                        "name": "BNSF / Union Pacific / CSX Intermodal Ramp Cut-Off & Crane Scheduler",
                        "protocol": "REST API / Webhook",
                        "tables": [
                                    "rail_ramp_cutoff_and_drayage"
                        ]
            },
            {
                        "id": "glec_rail_carbon_calculator",
                        "name": "GLEC v3.0 Intermodal Rail vs OTR Truck Carbon Intensity Ledger",
                        "protocol": "BigQuery SQL / JSON",
                        "tables": [
                                    "otr_to_rail_mode_conversion_ledger"
                        ]
            }
]
    }

def query_intermodal_corridor_shipments(
    shipment_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query intermodal_corridor_shipments records from railinc_clm_edi417_feed."""
    rows = _read_json("intermodal_corridor_shipments.json")
    all_rows = list(rows)
    if shipment_id:
        rows = [r for r in rows if shipment_id.lower() in str(r.get("shipment_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "railinc_clm_edi417_feed",
        "table": "intermodal_corridor_shipments",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_railinc_edi417_train_consists(
    train_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query railinc_edi417_train_consists records from intermodal_lane_milp_solver."""
    rows = _read_json("railinc_edi417_train_consists.json")
    all_rows = list(rows)
    if train_id:
        rows = [r for r in rows if train_id.lower() in str(r.get("train_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "intermodal_lane_milp_solver",
        "table": "railinc_edi417_train_consists",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_rail_ramp_cutoff_and_drayage(
    ramp_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query rail_ramp_cutoff_and_drayage records from ramp_crane_drayage_sync."""
    rows = _read_json("rail_ramp_cutoff_and_drayage.json")
    all_rows = list(rows)
    if ramp_id:
        rows = [r for r in rows if ramp_id.lower() in str(r.get("ramp_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "ramp_crane_drayage_sync",
        "table": "rail_ramp_cutoff_and_drayage",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_otr_to_rail_mode_conversion_ledger(
    corridor_lane: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query otr_to_rail_mode_conversion_ledger records from glec_rail_carbon_calculator."""
    rows = _read_json("otr_to_rail_mode_conversion_ledger.json")
    all_rows = list(rows)
    if corridor_lane:
        rows = [r for r in rows if corridor_lane.lower() in str(r.get("corridor_lane", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "glec_rail_carbon_calculator",
        "table": "otr_to_rail_mode_conversion_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_tender_edi404_rail_intermodal_bill(
    shipment_id: Any,
    rail_carrier: Any,
    train_id: Any,
    origin_ramp: Any,
    dest_ramp: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_tender_edi404_rail_intermodal_bill mutation with deterministic audit logging."""
    action_id = _deterministic_id("RAIL-404", shipment_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "shipment_id": shipment_id,
        "rail_carrier": rail_carrier,
        "train_id": train_id,
        "origin_ramp": origin_ramp,
        "dest_ramp": dest_ramp,
        "rationale": rationale,
        "status": "EDI404_RAIL_TENDER_ACCEPTED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_tender_edi404_rail_intermodal_bill", payload)
    return payload


def action_synchronize_ramp_crane_drayage_slot(
    train_id: Any,
    ramp_id: Any,
    drayage_tractor_id: Any,
    chassis_id: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_synchronize_ramp_crane_drayage_slot mutation with deterministic audit logging."""
    action_id = _deterministic_id("RAIL-DRAY", train_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "train_id": train_id,
        "ramp_id": ramp_id,
        "drayage_tractor_id": drayage_tractor_id,
        "chassis_id": chassis_id,
        "rationale": rationale,
        "status": "RAMP_CRANE_DRAYAGE_SYNCHRONIZED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_synchronize_ramp_crane_drayage_slot", payload)
    return payload

