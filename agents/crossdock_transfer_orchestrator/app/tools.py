"""Deterministic and fixture-backed tools for CrossDockFlow Transfer Orchestrator."""
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
    """Returns connected source systems, cross-dock sorters, and trailer bay dispatchers."""
    return {
        "agent": "crossdock_transfer_orchestrator",
        "systems": [
            {
                "id": "manhattan_crossdock_sorter",
                "name": "Manhattan Active WMS Dynamic Cross-Dock & Flow-Through Engine",
                "protocol": "REST / OpenAPI v3 / Real-Time Door-to-Door Routing",
                "tables": ["inbound_outbound_crossdock_manifests"],
            },
            {
                "id": "carrier_milestone_edi_feed",
                "name": "Carrier EDI 214 / Fleet Engine Inbound Milestone Geofencing",
                "protocol": "EDI 214 / Google Maps Fleet Engine Webhook",
                "tables": ["inbound_carrier_eta_milestones"],
            },
            {
                "id": "outbound_retail_wave_ledger",
                "name": "SAP EWM / Outbound Store Replenishment Wave Ledger",
                "protocol": "OData v4 / Real-Time Dock Bay Availability",
                "tables": ["outbound_trailer_bay_assignments"],
            },
            {
                "id": "pallet_flowthrough_telemetry",
                "name": "Intralogistics RFID / Forklift Telemetry Dwell Time Ledger",
                "protocol": "MQTT / Industrial IoT Dwell & Touch Counter",
                "tables": ["crossdock_dwell_time_records"],
            }
        ]
    }


def query_inbound_outbound_crossdock_manifests(
    manifest_id: str = "",
    supplier_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query inbound cross-dock manifests, eligible flow-through pallet counts, and assigned doors."""
    rows = _read_json("inbound_outbound_crossdock_manifests.json")
    all_rows = list(rows)
    if manifest_id:
        rows = [r for r in rows if manifest_id.lower() in r.get("manifest_id", "").lower()]
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "manhattan_crossdock_sorter",
        "table": "inbound_outbound_crossdock_manifests",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_inbound_carrier_eta_milestones(
    shipment_id: str = "",
    carrier_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query carrier arrival milestones, geofence check-ins, and unloading completion estimates."""
    rows = _read_json("inbound_carrier_eta_milestones.json")
    all_rows = list(rows)
    if shipment_id:
        rows = [r for r in rows if shipment_id.lower() in r.get("shipment_id", "").lower()]
    if carrier_id:
        rows = [r for r in rows if carrier_id.lower() in r.get("carrier_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "carrier_milestone_edi_feed",
        "table": "inbound_carrier_eta_milestones",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_outbound_trailer_bay_assignments(
    bay_id: str = "",
    destination_dc: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query outbound trailer bay capacities, scheduled departure cutoffs, and available pallet slots."""
    rows = _read_json("outbound_trailer_bay_assignments.json")
    all_rows = list(rows)
    if bay_id:
        rows = [r for r in rows if bay_id.lower() in r.get("bay_id", "").lower()]
    if destination_dc:
        rows = [r for r in rows if destination_dc.lower() in r.get("destination_dc", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "outbound_retail_wave_ledger",
        "table": "outbound_trailer_bay_assignments",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_crossdock_dwell_time_records(
    pallet_id: str = "",
    transfer_status: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query pallet dwell times, forklift transfer distances, and labor touch reduction counts."""
    rows = _read_json("crossdock_dwell_time_records.json")
    all_rows = list(rows)
    if pallet_id:
        rows = [r for r in rows if pallet_id.lower() in r.get("pallet_id", "").lower()]
    if transfer_status:
        rows = [r for r in rows if transfer_status.lower() in r.get("transfer_status", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "pallet_flowthrough_telemetry",
        "table": "crossdock_dwell_time_records",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_dispatch_direct_crossdock_transfer(
    inbound_manifest_id: str,
    inbound_door_id: str,
    outbound_bay_id: str,
    pallet_ids: List[str],
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Dispatch direct door-to-door pallet transfer bypassing staging racks and eliminating touches."""
    transfer_dispatch_id = _deterministic_id("XDOCK-TRF", inbound_manifest_id, outbound_bay_id, idempotency_key)
    payload = {
        "transfer_dispatch_id": transfer_dispatch_id,
        "inbound_manifest_id": inbound_manifest_id,
        "inbound_door_id": inbound_door_id,
        "outbound_bay_id": outbound_bay_id,
        "pallet_ids": pallet_ids,
        "pallet_count": len(pallet_ids),
        "wms_forklift_mission_id": f"FL-MISSION-{transfer_dispatch_id[-6:]}",
        "status": "CROSSDOCK_TRANSFER_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_direct_crossdock_transfer", payload)
    return payload


def action_hold_pallet_for_staging_buffer(
    pallet_id: str,
    staging_reason: str,
    holding_location_id: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Route non-conforming or delayed pallets to temporary staging buffer lane."""
    hold_id = _deterministic_id("XDOCK-HOLD", pallet_id, idempotency_key)
    payload = {
        "hold_id": hold_id,
        "pallet_id": pallet_id,
        "staging_reason": staging_reason,
        "holding_location_id": holding_location_id,
        "status": "PALLET_HELD_IN_STAGING",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_hold_pallet_for_staging_buffer", payload)
    return payload
