"""Deterministic and fixture-backed tools for SlotMaster Warehouse Slotting Optimizer."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    """Returns connected source systems, 3D WMS slotting twins, and AMR fleet controllers."""
    return {
        "agent": "warehouse_slotting_agent",
        "systems": [
            {
                "id": "manhattan_active_wms_slotting",
                "name": "Manhattan Active WMS 3D Slotting & Heatmap Module",
                "protocol": "REST / OpenAPI v3 / Dynamic Velocity Slotting",
                "tables": ["warehouse_slotting_velocity_tiers"],
            },
            {
                "id": "kion_amr_fleet_manager",
                "name": "KION / Dematic Autonomous Mobile Robot (AMR) Swarm Controller",
                "protocol": "VDA 5050 / WebSocket / Real-Time Travel Telemetry",
                "tables": ["amr_picker_travel_telemetry"],
            },
            {
                "id": "wms_wave_release_engine",
                "name": "Blue Yonder / Manhattan Wave Planning & Release Sequencer",
                "protocol": "REST API / Event Stream / Real-Time Aisle Throttle",
                "tables": ["wave_release_order_allocations"],
            },
            {
                "id": "ergonomic_pick_face_ledger",
                "name": "OSHA Ergonomic Golden Zone & Replenishment Task Ledger",
                "protocol": "PostgreSQL / REST / Golden Zone Biometrics",
                "tables": ["slot_reassignment_recommendations"],
            }
        ]
    }


def query_warehouse_slotting_velocity_tiers(
    sku_id: str = "",
    velocity_tier: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query SKU pick velocity tiers, pack station travel distances, and ergonomic golden zone status."""
    rows = _read_json("warehouse_slotting_velocity_tiers.json")
    all_rows = list(rows)
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if velocity_tier:
        rows = [r for r in rows if velocity_tier.lower() in r.get("velocity_tier", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "manhattan_active_wms_slotting",
        "table": "warehouse_slotting_velocity_tiers",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_amr_picker_travel_telemetry(
    dc_id: str = "",
    wave_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query AMR robot travel distance, picker walking percentage, and aisle congestion wait times."""
    rows = _read_json("amr_picker_travel_telemetry.json")
    all_rows = list(rows)
    if dc_id:
        rows = [r for r in rows if dc_id.lower() in r.get("dc_id", "").lower()]
    if wave_id:
        rows = [r for r in rows if wave_id.lower() in r.get("wave_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "kion_amr_fleet_manager",
        "table": "amr_picker_travel_telemetry",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_wave_release_order_allocations(
    wave_id: str = "",
    zone_id: str = "",
    dc_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query warehouse wave release status, active picker density, and congestion throttling recommendations."""
    rows = _read_json("wave_release_order_allocations.json")
    all_rows = list(rows)
    if dc_id:
        rows = [r for r in rows if dc_id.lower() in r.get("dc_id", "").lower()]
    if wave_id:
        rows = [r for r in rows if wave_id.lower() in r.get("wave_id", "").lower()]
    if zone_id:
        rows = [r for r in rows if zone_id.lower() in r.get("zone_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "wms_wave_release_engine",
        "table": "wave_release_order_allocations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_slot_reassignment_recommendations(
    sku_id: str = "",
    current_bin_id: str = "",
    recommended_bin_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query slot reassignment recommendations, travel reduction estimates, and annual labor savings."""
    rows = _read_json("slot_reassignment_recommendations.json")
    all_rows = list(rows)
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if current_bin_id:
        rows = [r for r in rows if current_bin_id.lower() in r.get("current_bin_id", "").lower()]
    if recommended_bin_id:
        rows = [r for r in rows if recommended_bin_id.lower() in r.get("recommended_bin_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "ergonomic_pick_face_ledger",
        "table": "slot_reassignment_recommendations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_execute_slot_reassignment(
    sku_id: str,
    current_bin_id: str,
    target_bin_id: str,
    priority: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Dispatch WMS physical stock relocation move task to transfer SKU into the ergonomic golden zone."""
    relocation_task_id = _deterministic_id("SLOT-RELOC", sku_id, target_bin_id, idempotency_key)
    payload = {
        "relocation_task_id": relocation_task_id,
        "sku_id": sku_id,
        "current_bin_id": current_bin_id,
        "target_bin_id": target_bin_id,
        "priority": priority,
        "wms_move_ticket_id": f"WMS-MOV-{relocation_task_id[-6:]}",
        "status": "RELOCATION_TASK_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_execute_slot_reassignment", payload)
    return payload


def action_balance_wave_release_profile(
    wave_id: str,
    zone_id: str,
    max_concurrent_pickers: int,
    release_status: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Dynamically throttle wave release and limit picker density to eliminate aisle gridlock."""
    wave_throttle_id = _deterministic_id("WAVE-THROT", wave_id, zone_id, idempotency_key)
    payload = {
        "wave_throttle_id": wave_throttle_id,
        "wave_id": wave_id,
        "zone_id": zone_id,
        "max_concurrent_pickers": max_concurrent_pickers,
        "release_status": release_status,
        "status": "WAVE_PROFILE_REBALANCED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_balance_wave_release_profile", payload)
    return payload
