"""Deterministic and fixture-backed tools for AeroFreight — Air Cargo Charter, Belly Allocation & 3D ULD Contour Optimizer."""
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
    """Returns connected enterprise systems and solver engines for air_cargo_uld_optimizer."""
    return {
        "agent": "air_cargo_uld_optimizer",
        "systems": [
            {
                        "id": "uld_3d_contour_solver",
                        "name": "Google OR-Tools 3D Contoured Aircraft ULD (LD3/LD7/PMC) Polyhedral Solver",
                        "protocol": "C++ / Python 3D Geometry SDK",
                        "tables": [
                                    "uld_3d_packing_manifests",
                                    "uld_contour_geometry_specs"
                        ]
            },
            {
                        "id": "iata_one_record_cargo",
                        "name": "IATA ONE Record & Champ Cargospot e-AWB Booking Gateway",
                        "protocol": "JSON-LD / REST API",
                        "tables": [
                                    "air_freight_priority_shipments"
                        ]
            },
            {
                        "id": "flightaware_adsb_telemetry",
                        "name": "FlightAware Firehose ADS-B Live Aircraft Tail & Tarmac Connection Feed",
                        "protocol": "Streaming WebSocket",
                        "tables": [
                                    "flightaware_adsb_belly_capacity"
                        ]
            },
            {
                        "id": "sap_tm_air_settlement",
                        "name": "SAP TM Air Rate Table & BSA Block Space Agreement Optimizer",
                        "protocol": "OData v4",
                        "tables": [
                                    "air_freight_priority_shipments"
                        ]
            }
]
    }

def query_air_freight_priority_shipments(
    awb_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query air_freight_priority_shipments records from uld_3d_contour_solver."""
    rows = _read_json("air_freight_priority_shipments.json")
    all_rows = list(rows)
    if awb_id:
        rows = [r for r in rows if awb_id.lower() in str(r.get("awb_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "uld_3d_contour_solver",
        "table": "air_freight_priority_shipments",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_uld_contour_geometry_specs(
    uld_type: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query uld_contour_geometry_specs records from iata_one_record_cargo."""
    rows = _read_json("uld_contour_geometry_specs.json")
    all_rows = list(rows)
    if uld_type:
        rows = [r for r in rows if uld_type.lower() in str(r.get("uld_type", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "iata_one_record_cargo",
        "table": "uld_contour_geometry_specs",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_uld_3d_packing_manifests(
    uld_manifest_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query uld_3d_packing_manifests records from flightaware_adsb_telemetry."""
    rows = _read_json("uld_3d_packing_manifests.json")
    all_rows = list(rows)
    if uld_manifest_id:
        rows = [r for r in rows if uld_manifest_id.lower() in str(r.get("uld_manifest_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "flightaware_adsb_telemetry",
        "table": "uld_3d_packing_manifests",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_flightaware_adsb_belly_capacity(
    flight_number: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query flightaware_adsb_belly_capacity records from sap_tm_air_settlement."""
    rows = _read_json("flightaware_adsb_belly_capacity.json")
    all_rows = list(rows)
    if flight_number:
        rows = [r for r in rows if flight_number.lower() in str(r.get("flight_number", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_tm_air_settlement",
        "table": "flightaware_adsb_belly_capacity",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_release_3d_uld_buildup_manifest(
    uld_manifest_id: Any,
    uld_type: Any,
    awb_id: Any,
    volumetric_efficiency_pct: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_release_3d_uld_buildup_manifest mutation with deterministic audit logging."""
    action_id = _deterministic_id("AERO-ULD", uld_manifest_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "uld_manifest_id": uld_manifest_id,
        "uld_type": uld_type,
        "awb_id": awb_id,
        "volumetric_efficiency_pct": volumetric_efficiency_pct,
        "rationale": rationale,
        "status": "ULD_3D_MANIFEST_RELEASED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_release_3d_uld_buildup_manifest", payload)
    return payload


def action_book_air_charter_or_belly_allotment(
    awb_id: Any,
    flight_number: Any,
    capacity_type: Any,
    rate_per_kg_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_book_air_charter_or_belly_allotment mutation with deterministic audit logging."""
    action_id = _deterministic_id("AERO-AWB", awb_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "awb_id": awb_id,
        "flight_number": flight_number,
        "capacity_type": capacity_type,
        "rate_per_kg_usd": rate_per_kg_usd,
        "rationale": rationale,
        "status": "AIR_CAPACITY_ALLOTMENT_LOCKED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_book_air_charter_or_belly_allotment", payload)
    return payload

