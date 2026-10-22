"""Deterministic and fixture-backed tools for ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker."""
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
    """Returns connected enterprise systems and solver engines for multimodal_mode_shift_agent."""
    return {
        "agent": "multimodal_mode_shift_agent",
        "systems": [
            {
                        "id": "or_tools_multimodal_pareto_milp",
                        "name": "Google OR-Tools Multi-Modal Cost / Carbon / Stockout Pareto MILP",
                        "protocol": "Python MILP SDK",
                        "tables": [
                                    "dynamic_mode_split_recommendations"
                        ]
            },
            {
                        "id": "sap_ibp_stockout_exposure",
                        "name": "SAP IBP & Cloud Spanner Downstream Hub Stockout Exposure Feed",
                        "protocol": "OData v4 / Spanner SQL",
                        "tables": [
                                    "factory_gate_outbound_pos"
                        ]
            },
            {
                        "id": "global_corridor_tariff_engine",
                        "name": "CargoWise & Xeneta Multi-Modal Spot/Contract Tariff & Transit Matrix",
                        "protocol": "REST API",
                        "tables": [
                                    "multimodal_corridor_rate_tariff_matrix"
                        ]
            },
            {
                        "id": "mid_route_sea_air_broker",
                        "name": "Dubai / LAX / Singapore Sea-Air Transshipment Hub Orchestrator",
                        "protocol": "EDI 315 / ONE Record",
                        "tables": [
                                    "in_transit_mode_diversion_triggers"
                        ]
            }
]
    }

def query_factory_gate_outbound_pos(
    po_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query factory_gate_outbound_pos records from or_tools_multimodal_pareto_milp."""
    rows = _read_json("factory_gate_outbound_pos.json")
    all_rows = list(rows)
    if po_id:
        rows = [r for r in rows if po_id.lower() in str(r.get("po_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "or_tools_multimodal_pareto_milp",
        "table": "factory_gate_outbound_pos",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_multimodal_corridor_rate_tariff_matrix(
    mode_code: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query multimodal_corridor_rate_tariff_matrix records from sap_ibp_stockout_exposure."""
    rows = _read_json("multimodal_corridor_rate_tariff_matrix.json")
    all_rows = list(rows)
    if mode_code:
        rows = [r for r in rows if mode_code.lower() in str(r.get("mode_code", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_ibp_stockout_exposure",
        "table": "multimodal_corridor_rate_tariff_matrix",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_dynamic_mode_split_recommendations(
    po_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query dynamic_mode_split_recommendations records from global_corridor_tariff_engine."""
    rows = _read_json("dynamic_mode_split_recommendations.json")
    all_rows = list(rows)
    if po_id:
        rows = [r for r in rows if po_id.lower() in str(r.get("po_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "global_corridor_tariff_engine",
        "table": "dynamic_mode_split_recommendations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_in_transit_mode_diversion_triggers(
    transship_hub: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query in_transit_mode_diversion_triggers records from mid_route_sea_air_broker."""
    rows = _read_json("in_transit_mode_diversion_triggers.json")
    all_rows = list(rows)
    if transship_hub:
        rows = [r for r in rows if transship_hub.lower() in str(r.get("transship_hub", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "mid_route_sea_air_broker",
        "table": "in_transit_mode_diversion_triggers",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_execute_dynamic_mode_split_booking(
    po_id: Any,
    primary_mode: Any,
    primary_units: Any,
    expedite_mode: Any,
    expedite_units: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_execute_dynamic_mode_split_booking mutation with deterministic audit logging."""
    action_id = _deterministic_id("MODAL-SPL", po_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "po_id": po_id,
        "primary_mode": primary_mode,
        "primary_units": primary_units,
        "expedite_mode": expedite_mode,
        "expedite_units": expedite_units,
        "rationale": rationale,
        "status": "DYNAMIC_MODE_SPLIT_BOOKED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_execute_dynamic_mode_split_booking", payload)
    return payload


def action_trigger_mid_route_sea_air_upgrade(
    po_id: Any,
    transship_hub: Any,
    units_upgraded: Any,
    days_recovered: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_trigger_mid_route_sea_air_upgrade mutation with deterministic audit logging."""
    action_id = _deterministic_id("MODAL-UPG", po_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "po_id": po_id,
        "transship_hub": transship_hub,
        "units_upgraded": units_upgraded,
        "days_recovered": days_recovered,
        "rationale": rationale,
        "status": "MID_ROUTE_SEA_AIR_UPGRADED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_trigger_mid_route_sea_air_upgrade", payload)
    return payload

