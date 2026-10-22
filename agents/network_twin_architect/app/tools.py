"""Deterministic and fixture-backed tools for TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer."""
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
    """Returns connected enterprise systems and solver engines for network_twin_architect."""
    return {
        "agent": "network_twin_architect",
        "systems": [
            {
                        "id": "or_tools_facility_location_milp",
                        "name": "Google OR-Tools Capacitated Facility Location & Territory MILP",
                        "protocol": "C++ / Python MILP",
                        "tables": [
                                    "center_of_gravity_milp_scenarios",
                                    "network_facility_nodes_and_leases"
                        ]
            },
            {
                        "id": "bigquery_abc_cost_to_serve",
                        "name": "BigQuery Activity-Based Cost-to-Serve (CTS) & Margin Waterfall Engine",
                        "protocol": "BigQuery SQL",
                        "tables": [
                                    "sku_customer_cost_to_serve_matrix"
                        ]
            },
            {
                        "id": "tariff_port_strike_simulator",
                        "name": "Macro Tariff & Port Disruption Network Stress-Test Simulator",
                        "protocol": "Python Monte Carlo + MILP",
                        "tables": [
                                    "network_stress_test_simulations"
                        ]
            },
            {
                        "id": "sap_ibp_network_master",
                        "name": "SAP IBP & S/4HANA Sourcing Rules & Customer Territory Master",
                        "protocol": "OData v4",
                        "tables": [
                                    "center_of_gravity_milp_scenarios"
                        ]
            }
]
    }

def query_network_facility_nodes_and_leases(
    facility_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query network_facility_nodes_and_leases records from or_tools_facility_location_milp."""
    rows = _read_json("network_facility_nodes_and_leases.json")
    if facility_id:
        rows = [r for r in rows if facility_id.lower() in str(r.get("facility_id", "")).lower()]
    return {
        "source_system": "or_tools_facility_location_milp",
        "table": "network_facility_nodes_and_leases",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_sku_customer_cost_to_serve_matrix(
    customer_segment_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query sku_customer_cost_to_serve_matrix records from bigquery_abc_cost_to_serve."""
    rows = _read_json("sku_customer_cost_to_serve_matrix.json")
    if customer_segment_id:
        rows = [r for r in rows if customer_segment_id.lower() in str(r.get("customer_segment_id", "")).lower()]
    return {
        "source_system": "bigquery_abc_cost_to_serve",
        "table": "sku_customer_cost_to_serve_matrix",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_center_of_gravity_milp_scenarios(
    scenario_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query center_of_gravity_milp_scenarios records from tariff_port_strike_simulator."""
    rows = _read_json("center_of_gravity_milp_scenarios.json")
    if scenario_id:
        rows = [r for r in rows if scenario_id.lower() in str(r.get("scenario_id", "")).lower()]
    return {
        "source_system": "tariff_port_strike_simulator",
        "table": "center_of_gravity_milp_scenarios",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_network_stress_test_simulations(
    stress_test_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query network_stress_test_simulations records from sap_ibp_network_master."""
    rows = _read_json("network_stress_test_simulations.json")
    if stress_test_id:
        rows = [r for r in rows if stress_test_id.lower() in str(r.get("stress_test_id", "")).lower()]
    return {
        "source_system": "sap_ibp_network_master",
        "table": "network_stress_test_simulations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_publish_network_territory_realignment(
    scenario_id: Any,
    new_hub_id: Any,
    annual_savings_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_publish_network_territory_realignment mutation with deterministic audit logging."""
    action_id = _deterministic_id("TWIN-NET", scenario_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "scenario_id": scenario_id,
        "new_hub_id": new_hub_id,
        "annual_savings_usd": annual_savings_usd,
        "rationale": rationale,
        "status": "NETWORK_TERRITORY_REALIGNED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_publish_network_territory_realignment", payload)
    return payload


def action_update_cost_to_serve_order_policy(
    customer_segment_id: Any,
    new_moq_layer_pallets: Any,
    margin_improvement_pct: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_update_cost_to_serve_order_policy mutation with deterministic audit logging."""
    action_id = _deterministic_id("TWIN-CTS", customer_segment_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "customer_segment_id": customer_segment_id,
        "new_moq_layer_pallets": new_moq_layer_pallets,
        "margin_improvement_pct": margin_improvement_pct,
        "rationale": rationale,
        "status": "COST_TO_SERVE_POLICY_UPDATED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_update_cost_to_serve_order_policy", payload)
    return payload

