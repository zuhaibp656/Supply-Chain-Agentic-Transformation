"""Deterministic and fixture-backed tools for YardPulse Yard & Dock Orchestrator."""
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
    """Returns connected source systems, yard geofences, and hostler spotter dispatchers."""
    return {
        "agent": "yard_dock_sequencer",
        "systems": [
            {
                "id": "fleet_engine_yard_geofence",
                "name": "Google Maps Fleet Engine Yard Geofence & Inbound ETA Stream",
                "protocol": "Fleet Engine gRPC / Real-Time Trailer GPS Geofence",
                "tables": ["yard_trailer_geofence_status"],
            },
            {
                "id": "hostler_spotter_dispatch",
                "name": "Kalmar / TICO Terminal Tractor Yard Spotter Telematics",
                "protocol": "J1939 CAN / MQTT / Real-Time Hostler Move Dispatch",
                "tables": ["yard_spotter_move_tasks"],
            },
            {
                "id": "dock_door_schedule_ledger",
                "name": "SAP EWM / Manhattan Yard Management Dock Door Scheduler",
                "protocol": "REST / OpenAPI v3 / Turnaround Cadence Matrix",
                "tables": ["dock_door_turnaround_schedules"],
            },
            {
                "id": "carrier_detention_penalty_ledger",
                "name": "Carrier Accessorial & Demurrage Free-Time Contract Ledger",
                "protocol": "PostgreSQL / REST / 2-Hour Free Time Rule Engine",
                "tables": ["carrier_detention_risk_records"],
            }
        ]
    }


def query_yard_trailer_geofence_status(
    trailer_id: str = "",
    yard_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query trailer yard presence, geofence check-in timestamp, and current yard slot location."""
    rows = _read_json("yard_trailer_geofence_status.json")
    all_rows = list(rows)
    if trailer_id:
        rows = [r for r in rows if trailer_id.lower() in r.get("trailer_id", "").lower()]
    if yard_id:
        rows = [r for r in rows if yard_id.lower() in r.get("yard_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "fleet_engine_yard_geofence",
        "table": "yard_trailer_geofence_status",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_yard_spotter_move_tasks(
    task_id: str = "",
    spotter_truck_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query yard spotter hostler move tasks, priority queues, and transit durations."""
    rows = _read_json("yard_spotter_move_tasks.json")
    all_rows = list(rows)
    if task_id:
        rows = [r for r in rows if task_id.lower() in r.get("task_id", "").lower()]
    if spotter_truck_id:
        rows = [r for r in rows if spotter_truck_id.lower() in r.get("spotter_truck_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "hostler_spotter_dispatch",
        "table": "yard_spotter_move_tasks",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_dock_door_turnaround_schedules(
    door_id: str = "",
    facility_zone: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query dock door occupancy, turnaround duration targets, and assigned forklift crews."""
    rows = _read_json("dock_door_turnaround_schedules.json")
    all_rows = list(rows)
    if door_id:
        rows = [r for r in rows if door_id.lower() in r.get("door_id", "").lower()]
    if facility_zone:
        rows = [r for r in rows if facility_zone.lower() in r.get("facility_zone", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "dock_door_schedule_ledger",
        "table": "dock_door_turnaround_schedules",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_carrier_detention_risk_records(
    trailer_id: str = "",
    carrier_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query carrier 2-hour detention thresholds, accrued dwell minutes, and demurrage risk penalties."""
    rows = _read_json("carrier_detention_risk_records.json")
    all_rows = list(rows)
    if trailer_id:
        rows = [r for r in rows if trailer_id.lower() in r.get("trailer_id", "").lower()]
    if carrier_id:
        rows = [r for r in rows if carrier_id.lower() in r.get("carrier_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "carrier_detention_penalty_ledger",
        "table": "carrier_detention_risk_records",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_dispatch_yard_spotter_move(
    trailer_id: str,
    current_yard_slot: str,
    target_dock_door: str,
    spotter_truck_id: str,
    priority: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Dispatch hostler terminal tractor to pull trailer from yard staging slot directly to dock door."""
    move_id = _deterministic_id("YARD-MOVE", trailer_id, target_dock_door, idempotency_key)
    payload = {
        "move_id": move_id,
        "trailer_id": trailer_id,
        "current_yard_slot": current_yard_slot,
        "target_dock_door": target_dock_door,
        "spotter_truck_id": spotter_truck_id,
        "priority": priority,
        "spotter_job_id": f"HOSTLER-JOB-{move_id[-6:]}",
        "status": "SPOTTER_MOVE_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_yard_spotter_move", payload)
    return payload


def action_resolve_carrier_detention_alert(
    trailer_id: str,
    carrier_id: str,
    turnaround_time_minutes: float,
    fee_avoided_usd: float,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Log demurrage resolution confirming turnaround completed within free time threshold."""
    resolution_id = _deterministic_id("DET-RESOLV", trailer_id, idempotency_key)
    payload = {
        "resolution_id": resolution_id,
        "trailer_id": trailer_id,
        "carrier_id": carrier_id,
        "turnaround_time_minutes": turnaround_time_minutes,
        "fee_avoided_usd": fee_avoided_usd,
        "status": "DETENTION_PENALTY_NEUTRALIZED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_resolve_carrier_detention_alert", payload)
    return payload
