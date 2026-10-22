"""Deterministic and fixture-backed tools for PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator."""
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
    """Returns connected enterprise systems and solver engines for port_drayage_orchestrator."""
    return {
        "agent": "port_drayage_orchestrator",
        "systems": [
            {
                        "id": "spire_maritime_satellite_ais",
                        "name": "Spire Maritime Satellite AIS & Google DeepMind WeatherNext 3 Feed",
                        "protocol": "GraphQL / gRPC Stream",
                        "tables": [
                                    "ocean_vessel_ais_berth_telemetry"
                        ]
            },
            {
                        "id": "cargowise_ocean_fcl_ledger",
                        "name": "CargoWise One Global Ocean Container & LFD Demurrage Ledger",
                        "protocol": "EDI 315 / XML",
                        "tables": [
                                    "container_discharge_demurrage_ledger"
                        ]
            },
            {
                        "id": "port_terminal_gate_api",
                        "name": "Port of LA/LB PierPASS & Rotterdam Terminal Gate Appointment API",
                        "protocol": "REST / Webhook",
                        "tables": [
                                    "port_terminal_gate_appointments"
                        ]
            },
            {
                        "id": "drayage_transload_solver",
                        "name": "Google OR-Tools Bipartite Drayage & Transload Allocation Solver",
                        "protocol": "Python MILP SDK",
                        "tables": [
                                    "drayage_chassis_transload_allocations"
                        ]
            }
]
    }

def query_ocean_vessel_ais_berth_telemetry(
    vessel_imo: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query ocean_vessel_ais_berth_telemetry records from spire_maritime_satellite_ais."""
    rows = _read_json("ocean_vessel_ais_berth_telemetry.json")
    if vessel_imo:
        rows = [r for r in rows if vessel_imo.lower() in str(r.get("vessel_imo", "")).lower()]
    return {
        "source_system": "spire_maritime_satellite_ais",
        "table": "ocean_vessel_ais_berth_telemetry",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_container_discharge_demurrage_ledger(
    container_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query container_discharge_demurrage_ledger records from cargowise_ocean_fcl_ledger."""
    rows = _read_json("container_discharge_demurrage_ledger.json")
    if container_id:
        rows = [r for r in rows if container_id.lower() in str(r.get("container_id", "")).lower()]
    return {
        "source_system": "cargowise_ocean_fcl_ledger",
        "table": "container_discharge_demurrage_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_port_terminal_gate_appointments(
    terminal_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query port_terminal_gate_appointments records from port_terminal_gate_api."""
    rows = _read_json("port_terminal_gate_appointments.json")
    if terminal_id:
        rows = [r for r in rows if terminal_id.lower() in str(r.get("terminal_id", "")).lower()]
    return {
        "source_system": "port_terminal_gate_api",
        "table": "port_terminal_gate_appointments",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_drayage_chassis_transload_allocations(
    container_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query drayage_chassis_transload_allocations records from drayage_transload_solver."""
    rows = _read_json("drayage_chassis_transload_allocations.json")
    if container_id:
        rows = [r for r in rows if container_id.lower() in str(r.get("container_id", "")).lower()]
    return {
        "source_system": "drayage_transload_solver",
        "table": "drayage_chassis_transload_allocations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_book_dual_transaction_drayage_gate(
    container_id: Any,
    terminal_id: Any,
    gate_slot_id: Any,
    drayage_carrier_id: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_book_dual_transaction_drayage_gate mutation with deterministic audit logging."""
    action_id = _deterministic_id("PORT-GATE", container_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "container_id": container_id,
        "terminal_id": terminal_id,
        "gate_slot_id": gate_slot_id,
        "drayage_carrier_id": drayage_carrier_id,
        "rationale": rationale,
        "status": "DUAL_DRAYAGE_GATE_BOOKED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_book_dual_transaction_drayage_gate", payload)
    return payload


def action_divert_container_to_transload_hub(
    container_id: Any,
    transload_facility_id: Any,
    outbound_mode: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_divert_container_to_transload_hub mutation with deterministic audit logging."""
    action_id = _deterministic_id("PORT-TRNS", container_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "container_id": container_id,
        "transload_facility_id": transload_facility_id,
        "outbound_mode": outbound_mode,
        "rationale": rationale,
        "status": "CONTAINER_DIVERTED_TO_TRANSLOAD",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_divert_container_to_transload_hub", payload)
    return payload

