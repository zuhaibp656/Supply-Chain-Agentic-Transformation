"""Deterministic and fixture-backed tools for AssetGuard Plant Predictive Maintenance & OEE Agent."""
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
    """Returns connected source systems, shopfloor MES historians, and plant maintenance systems."""
    return {
        "agent": "predictive_oee_sentinel",
        "systems": [
            {
                "id": "mes_siemens_opcenter",
                "name": "Siemens Opcenter MES Execution Lake",
                "protocol": "OPC UA / OData v4 / MQTT Pub/Sub",
                "tables": ["oee_breakdown_metrics"],
            },
            {
                "id": "osisoft_pi_historian",
                "name": "OSIsoft PI Historian Vibration & Current Sensor Lake",
                "protocol": "BigQuery Time-Series / PI Web API REST",
                "tables": ["plant_machine_telemetry", "predictive_maintenance_anomalies"],
            },
            {
                "id": "sap_pm_plant_maintenance",
                "name": "SAP S/4HANA Plant Maintenance (PM)",
                "protocol": "BAPI_ALM_ORDER_MAINTAIN / OData v4",
                "tables": [],
            },
            {
                "id": "sap_mm_spare_parts",
                "name": "SAP S/4HANA Materials Management (MM) Spare Parts Crib",
                "protocol": "BAPI_RESERVATION_CREATE1",
                "tables": ["spare_parts_inventory_status"],
            }
        ]
    }


def query_plant_machine_telemetry(
    asset_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query live vibration RMS, bearing temperatures, motor amps, and spindle speed."""
    rows = _read_json("plant_machine_telemetry.json")
    all_rows = list(rows)
    if asset_id:
        rows = [r for r in rows if asset_id.lower() in r.get("asset_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "osisoft_pi_historian",
        "table": "plant_machine_telemetry",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_oee_breakdown_metrics(
    asset_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Overall Equipment Effectiveness (Availability, Performance, Quality, Downtime losses)."""
    rows = _read_json("oee_breakdown_metrics.json")
    all_rows = list(rows)
    if asset_id:
        rows = [r for r in rows if asset_id.lower() in r.get("asset_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "mes_siemens_opcenter",
        "table": "oee_breakdown_metrics",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_predictive_maintenance_anomalies(
    anomaly_id: str = "",
    asset_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query machine learning early failure warnings, time-to-failure (TTF), and avoided losses."""
    rows = _read_json("predictive_maintenance_anomalies.json")
    all_rows = list(rows)
    if anomaly_id:
        rows = [r for r in rows if anomaly_id.lower() in r.get("anomaly_id", "").lower()]
    if asset_id:
        rows = [r for r in rows if asset_id.lower() in r.get("asset_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "osisoft_pi_historian",
        "table": "predictive_maintenance_anomalies",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_spare_parts_inventory_status(
    part_number: str = "",
    compatible_asset: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query maintenance spare parts inventory, stock on hand, crib bin location, and lead times."""
    rows = _read_json("spare_parts_inventory_status.json")
    all_rows = list(rows)
    if part_number:
        rows = [r for r in rows if part_number.lower() in r.get("part_number", "").lower()]
    if compatible_asset:
        rows = [r for r in rows if any(compatible_asset.lower() in a.lower() for a in r.get("compatible_assets", []))]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_mm_spare_parts",
        "table": "spare_parts_inventory_status",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_dispatch_preventive_work_order(
    asset_id: str,
    maintenance_type: str,
    priority: str,
    maintenance_window: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Dispatch automated preventive maintenance work order in SAP PM before asset catastrophic failure."""
    work_order_id = _deterministic_id("PM-WO", asset_id, maintenance_type, idempotency_key)
    payload = {
        "work_order_id": work_order_id,
        "asset_id": asset_id,
        "maintenance_type": maintenance_type,
        "priority": priority,
        "maintenance_window": maintenance_window,
        "status": "SAP_PM_WORK_ORDER_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_preventive_work_order", payload)
    return payload


def action_reserve_spare_parts(
    work_order_id: str,
    part_number: str,
    quantity: int,
    asset_id: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Reserve critical replacement spare parts in SAP MM for the dispatched work order."""
    reservation_id = _deterministic_id("RES-MM", work_order_id, part_number, idempotency_key)
    payload = {
        "reservation_id": reservation_id,
        "work_order_id": work_order_id,
        "part_number": part_number,
        "quantity": quantity,
        "asset_id": asset_id,
        "status": "SAP_MM_PARTS_RESERVED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_reserve_spare_parts", payload)
    return payload
