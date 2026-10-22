"""Deterministic and fixture-backed tools for ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List

FIXTURES = Path(os.environ.get("FIXTURES_ROOT", str(Path(__file__).resolve().parent.parent / "fixtures")))
ACTION_EVENTS_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "action-events.jsonl"


def _read_json(table_filename: str) -> List[Dict[str, Any]]:
    p = FIXTURES / "tables" / table_filename
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []


def _append_action_event(tool_name: str, payload: Dict[str, Any]) -> None:
    ACTION_EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ACTION_EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"tool": tool_name, **payload}, sort_keys=True) + "\n")


def _deterministic_id(prefix: str, *parts: Any) -> str:
    payload = "|".join(str(p) for p in parts if p is not None and p != "")
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:8].upper() if payload else "00000000"
    return f"{prefix}-{digest}"


def list_systems() -> Dict[str, Any]:
    """Returns connected enterprise systems and solver engines for reverse_rma_optimizer."""
    return {
        "agent": "reverse_rma_optimizer",
        "systems": [
            {
                        "id": "gemini_38_flash_rma_vision",
                        "name": "Vertex AI Gemini 3.8 Flash Optical RMA Condition & Seal Grader",
                        "protocol": "gRPC Multimodal API",
                        "tables": [
                                    "multimodal_vision_grading_results"
                        ]
            },
            {
                        "id": "loop_sap_rma_portal",
                        "name": "SAP S/4HANA Returns & Customer RMA Intake Portal",
                        "protocol": "REST / OData v4",
                        "tables": [
                                    "customer_rma_intake_requests"
                        ]
            },
            {
                        "id": "fleetflow_backhaul_matcher",
                        "name": "FleetFlow Returning Delivery Truck Backhaul Milk-Run Matcher",
                        "protocol": "Google Maps CVRPTW",
                        "tables": [
                                    "fleet_backhaul_pickup_slots"
                        ]
            },
            {
                        "id": "circular_disposition_solver",
                        "name": "OR-Tools Circular Recovery Margin Solver (Restock vs Refurb vs Harvest)",
                        "protocol": "Python MILP",
                        "tables": [
                                    "circular_disposition_routing_ledger"
                        ]
            }
]
    }

def query_customer_rma_intake_requests(
    rma_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query customer_rma_intake_requests records from gemini_38_flash_rma_vision."""
    rows = _read_json("customer_rma_intake_requests.json")
    if rma_id:
        rows = [r for r in rows if rma_id.lower() in str(r.get("rma_id", "")).lower()]
    return {
        "source_system": "gemini_38_flash_rma_vision",
        "table": "customer_rma_intake_requests",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_multimodal_vision_grading_results(
    rma_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query multimodal_vision_grading_results records from loop_sap_rma_portal."""
    rows = _read_json("multimodal_vision_grading_results.json")
    if rma_id:
        rows = [r for r in rows if rma_id.lower() in str(r.get("rma_id", "")).lower()]
    return {
        "source_system": "loop_sap_rma_portal",
        "table": "multimodal_vision_grading_results",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_fleet_backhaul_pickup_slots(
    rma_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query fleet_backhaul_pickup_slots records from fleetflow_backhaul_matcher."""
    rows = _read_json("fleet_backhaul_pickup_slots.json")
    if rma_id:
        rows = [r for r in rows if rma_id.lower() in str(r.get("rma_id", "")).lower()]
    return {
        "source_system": "fleetflow_backhaul_matcher",
        "table": "fleet_backhaul_pickup_slots",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_circular_disposition_routing_ledger(
    rma_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query circular_disposition_routing_ledger records from circular_disposition_solver."""
    rows = _read_json("circular_disposition_routing_ledger.json")
    if rma_id:
        rows = [r for r in rows if rma_id.lower() in str(r.get("rma_id", "")).lower()]
    return {
        "source_system": "circular_disposition_solver",
        "table": "circular_disposition_routing_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_assign_rma_disposition_and_backhaul(
    rma_id: Any,
    optical_grade: Any,
    target_facility_id: Any,
    backhaul_vehicle_id: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_assign_rma_disposition_and_backhaul mutation with deterministic audit logging."""
    action_id = _deterministic_id("RMA-LOOP", rma_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "rma_id": rma_id,
        "optical_grade": optical_grade,
        "target_facility_id": target_facility_id,
        "backhaul_vehicle_id": backhaul_vehicle_id,
        "rationale": rationale,
        "status": "RMA_DISPOSITION_AND_BACKHAUL_LOCKED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_assign_rma_disposition_and_backhaul", payload)
    return payload


def action_issue_instant_customer_rma_credit_or_swap(
    rma_id: Any,
    customer_id: Any,
    credit_amount_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_issue_instant_customer_rma_credit_or_swap mutation with deterministic audit logging."""
    action_id = _deterministic_id("RMA-CRED", rma_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "rma_id": rma_id,
        "customer_id": customer_id,
        "credit_amount_usd": credit_amount_usd,
        "rationale": rationale,
        "status": "INSTANT_RMA_CREDIT_ISSUED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_issue_instant_customer_rma_credit_or_swap", payload)
    return payload

