"""Deterministic and fixture-backed tools for FleetFlow — Google Maps Corridor Route & Fleet Dispatch Studio."""
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
    """Returns connected enterprise systems and solver engines for fleetflow_dispatch."""
    return {
        "agent": "fleetflow_dispatch",
        "systems": [
            {
                        "id": "google_maps_routes_preferred",
                        "name": "Google Maps Platform Routes Preferred & Live Traffic Matrix API",
                        "protocol": "gRPC / REST v2",
                        "tables": [
                                    "google_maps_corridor_routes"
                        ]
            },
            {
                        "id": "or_tools_cvrptw_solver",
                        "name": "Google OR-Tools Capacitated Vehicle Routing (CVRPTW) Engine",
                        "protocol": "C++ / Python Solver SDK",
                        "tables": [
                                    "corridor_delivery_orders"
                        ]
            },
            {
                        "id": "samsara_eld_telematics",
                        "name": "Samsara ELD & Google Maps Fleet Engine Vehicle Telemetry",
                        "protocol": "Webhook / MQTT",
                        "tables": [
                                    "fleet_vehicle_telematics_hos"
                        ]
            },
            {
                        "id": "backhaul_freight_matcher",
                        "name": "Blue Yonder TMS Backhaul & Deadhead Elimination Broker",
                        "protocol": "OData / EDI 204",
                        "tables": [
                                    "backhaul_consolidation_opportunities"
                        ]
            }
]
    }

def query_corridor_delivery_orders(
    corridor_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query corridor_delivery_orders records from google_maps_routes_preferred."""
    rows = _read_json("corridor_delivery_orders.json")
    all_rows = list(rows)
    if corridor_id:
        rows = [r for r in rows if corridor_id.lower() in str(r.get("corridor_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "google_maps_routes_preferred",
        "table": "corridor_delivery_orders",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_fleet_vehicle_telematics_hos(
    vehicle_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query fleet_vehicle_telematics_hos records from or_tools_cvrptw_solver."""
    rows = _read_json("fleet_vehicle_telematics_hos.json")
    all_rows = list(rows)
    if vehicle_id:
        rows = [r for r in rows if vehicle_id.lower() in str(r.get("vehicle_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "or_tools_cvrptw_solver",
        "table": "fleet_vehicle_telematics_hos",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_google_maps_corridor_routes(
    route_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query google_maps_corridor_routes records from samsara_eld_telematics."""
    rows = _read_json("google_maps_corridor_routes.json")
    all_rows = list(rows)
    if route_id:
        rows = [r for r in rows if route_id.lower() in str(r.get("route_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "samsara_eld_telematics",
        "table": "google_maps_corridor_routes",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_backhaul_consolidation_opportunities(
    backhaul_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query backhaul_consolidation_opportunities records from backhaul_freight_matcher."""
    rows = _read_json("backhaul_consolidation_opportunities.json")
    all_rows = list(rows)
    if backhaul_id:
        rows = [r for r in rows if backhaul_id.lower() in str(r.get("backhaul_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "backhaul_freight_matcher",
        "table": "backhaul_consolidation_opportunities",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_dispatch_corridor_route_manifest(
    route_id: Any,
    vehicle_id: Any,
    corridor_id: Any,
    stop_count: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_dispatch_corridor_route_manifest mutation with deterministic audit logging."""
    action_id = _deterministic_id("FF-DISP", route_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "route_id": route_id,
        "vehicle_id": vehicle_id,
        "corridor_id": corridor_id,
        "stop_count": stop_count,
        "rationale": rationale,
        "status": "CORRIDOR_ROUTE_DISPATCHED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_corridor_route_manifest", payload)
    return payload


def action_assign_backhaul_return_load(
    backhaul_id: Any,
    vehicle_id: Any,
    origin_hub: Any,
    destination_dc: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_assign_backhaul_return_load mutation with deterministic audit logging."""
    action_id = _deterministic_id("FF-BKH", backhaul_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "backhaul_id": backhaul_id,
        "vehicle_id": vehicle_id,
        "origin_hub": origin_hub,
        "destination_dc": destination_dc,
        "rationale": rationale,
        "status": "BACKHAUL_RETURN_ASSIGNED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_assign_backhaul_return_load", payload)
    return payload

