"""Deterministic and fixture-backed tools for CubeMaster 3D — Isometric LIFO Bay & Load Consolidation Studio."""
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
    """Returns connected enterprise systems and solver engines for load_consolidation_agent."""
    return {
        "agent": "load_consolidation_agent",
        "systems": [
            {
                        "id": "or_tools_3d_voxel_packer",
                        "name": "Google OR-Tools 3D Extreme-Point & Guillotine Bin Packing Solver",
                        "protocol": "C++ / Python 3D Voxel Engine",
                        "tables": [
                                    "lifo_3d_voxel_load_plans"
                        ]
            },
            {
                        "id": "sap_ewm_carton_master",
                        "name": "SAP EWM & Material Master 3D Carton Geometry & Fragility Feed",
                        "protocol": "OData v4 / BAPI",
                        "tables": [
                                    "outbound_shipment_carton_dimensions"
                        ]
            },
            {
                        "id": "tms_trailer_fleet_specs",
                        "name": "Fleet Trailer Bay & DOT Axle-Weight Compliance Registry",
                        "protocol": "REST / JSON",
                        "tables": [
                                    "trailer_bay_geometry_specs"
                        ]
            },
            {
                        "id": "dock_lifo_axle_auditor",
                        "name": "Dock Scale & Crush-Pressure Physics Verification Engine",
                        "protocol": "IoT Weighbridge / REST",
                        "tables": [
                                    "axle_weight_crush_audit_logs"
                        ]
            }
]
    }

def query_outbound_shipment_carton_dimensions(
    shipment_wave_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query outbound_shipment_carton_dimensions records from or_tools_3d_voxel_packer."""
    rows = _read_json("outbound_shipment_carton_dimensions.json")
    if shipment_wave_id:
        rows = [r for r in rows if shipment_wave_id.lower() in str(r.get("shipment_wave_id", "")).lower()]
    return {
        "source_system": "or_tools_3d_voxel_packer",
        "table": "outbound_shipment_carton_dimensions",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_trailer_bay_geometry_specs(
    trailer_type_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query trailer_bay_geometry_specs records from sap_ewm_carton_master."""
    rows = _read_json("trailer_bay_geometry_specs.json")
    if trailer_type_id:
        rows = [r for r in rows if trailer_type_id.lower() in str(r.get("trailer_type_id", "")).lower()]
    return {
        "source_system": "sap_ewm_carton_master",
        "table": "trailer_bay_geometry_specs",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_lifo_3d_voxel_load_plans(
    load_plan_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query lifo_3d_voxel_load_plans records from tms_trailer_fleet_specs."""
    rows = _read_json("lifo_3d_voxel_load_plans.json")
    if load_plan_id:
        rows = [r for r in rows if load_plan_id.lower() in str(r.get("load_plan_id", "")).lower()]
    return {
        "source_system": "tms_trailer_fleet_specs",
        "table": "lifo_3d_voxel_load_plans",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_axle_weight_crush_audit_logs(
    load_plan_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query axle_weight_crush_audit_logs records from dock_lifo_axle_auditor."""
    rows = _read_json("axle_weight_crush_audit_logs.json")
    if load_plan_id:
        rows = [r for r in rows if load_plan_id.lower() in str(r.get("load_plan_id", "")).lower()]
    return {
        "source_system": "dock_lifo_axle_auditor",
        "table": "axle_weight_crush_audit_logs",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_commit_3d_lifo_load_plan(
    load_plan_id: Any,
    trailer_type_id: Any,
    cube_utilization_pct: Any,
    lifo_zones: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_commit_3d_lifo_load_plan mutation with deterministic audit logging."""
    action_id = _deterministic_id("CUBE-LP", load_plan_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "load_plan_id": load_plan_id,
        "trailer_type_id": trailer_type_id,
        "cube_utilization_pct": cube_utilization_pct,
        "lifo_zones": lifo_zones,
        "rationale": rationale,
        "status": "LOAD_PLAN_3D_COMMITTED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_commit_3d_lifo_load_plan", payload)
    return payload


def action_resequence_dock_staging_lanes(
    shipment_wave_id: Any,
    staging_lane_id: Any,
    loading_sequence_mode: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_resequence_dock_staging_lanes mutation with deterministic audit logging."""
    action_id = _deterministic_id("CUBE-STG", shipment_wave_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "shipment_wave_id": shipment_wave_id,
        "staging_lane_id": staging_lane_id,
        "loading_sequence_mode": loading_sequence_mode,
        "rationale": rationale,
        "status": "DOCK_STAGING_RESEQUENCED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_resequence_dock_staging_lanes", payload)
    return payload

