"""Deterministic and fixture-backed tools for Synapse Autonomous S&OP Scenario Weaver."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    """Returns connected source systems, constraint solvers, and S&OP integration protocols."""
    return {
        "agent": "sop_scenario_weaver",
        "systems": [
            {
                "id": "spanner_constraint_graph",
                "name": "Cloud Spanner S&OP Supply Network Constraint Graph",
                "protocol": "Spanner Graph SQL / Vertex AI Agent Engine",
                "tables": ["plant_line_capacities", "supplier_component_allocations"],
            },
            {
                "id": "bigquery_cortex_pnl",
                "name": "BigQuery Cortex S&OP P&L & Cash Bridge",
                "protocol": "BigQuery SQL / Cortex Framework",
                "tables": ["sop_unconstrained_demand", "sop_scenario_tradeoffs"],
            },
            {
                "id": "google_ortools_milp",
                "name": "Google OR-Tools Mixed-Integer Linear Programming (MILP) Solver",
                "protocol": "Native C++ / Python MILP Optimization Engine",
                "tables": ["sop_scenario_tradeoffs"],
            },
            {
                "id": "sap_s4hana_ppds",
                "name": "SAP S/4HANA Production Planning & Detailed Scheduling (PP/DS)",
                "protocol": "OData v4 / BAPI_MPS_COMMIT",
                "tables": [],
            }
        ]
    }


def query_unconstrained_demand_gaps(
    plan_month: str = "",
    business_unit: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query unconstrained commercial demand vs constrained supply gaps."""
    rows = _read_json("sop_unconstrained_demand.json")
    if plan_month:
        rows = [r for r in rows if plan_month in r.get("plan_month", "")]
    if business_unit:
        rows = [r for r in rows if business_unit.lower() in r.get("business_unit", "").lower()]
    return {
        "source_system": "bigquery_cortex_pnl",
        "table": "sop_unconstrained_demand",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_plant_line_capacities(
    facility_id: str = "",
    is_bottleneck: bool = False,
    limit: int = 10
) -> Dict[str, Any]:
    """Query manufacturing plant line utilization, shifts, and bottleneck work centers."""
    rows = _read_json("plant_line_capacities.json")
    if facility_id:
        rows = [r for r in rows if facility_id.lower() in r.get("facility_id", "").lower()]
    if is_bottleneck:
        rows = [r for r in rows if r.get("is_bottleneck") is True]
    return {
        "source_system": "spanner_constraint_graph",
        "table": "plant_line_capacities",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_supplier_allocations(
    supplier_id: str = "",
    component_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Tier-1/Tier-2 component allocation limits, supplier MOQs, and lead times."""
    rows = _read_json("supplier_component_allocations.json")
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    if component_id:
        rows = [r for r in rows if component_id.lower() in r.get("component_id", "").lower()]
    return {
        "source_system": "spanner_constraint_graph",
        "table": "supplier_component_allocations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_sop_scenario_evaluations(
    scenario_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Google OR-Tools multi-criteria Pareto trade-off evaluations."""
    rows = _read_json("sop_scenario_tradeoffs.json")
    if scenario_id:
        rows = [r for r in rows if scenario_id.lower() in r.get("scenario_id", "").lower()]
    return {
        "source_system": "google_ortools_milp",
        "table": "sop_scenario_tradeoffs",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_commit_mps_consensus_plan(
    scenario_id: str,
    business_unit: str,
    committed_volume_units: int,
    approved_overtime_cost_usd: float,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Commit consensus Master Production Schedule (MPS) to SAP S/4HANA PP/DS."""
    mps_id = _deterministic_id("MPS-SOP", scenario_id, business_unit, idempotency_key)
    payload = {
        "mps_id": mps_id,
        "scenario_id": scenario_id,
        "business_unit": business_unit,
        "committed_volume_units": committed_volume_units,
        "approved_overtime_cost_usd": approved_overtime_cost_usd,
        "status": "MPS_COMMITTED_TO_SAP",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_commit_mps_consensus_plan", payload)
    return payload


def action_lock_sop_financial_bridge(
    scenario_id: str,
    target_revenue_usd: float,
    target_gross_margin_usd: float,
    working_capital_ceiling_usd: float,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Lock consensus S&OP revenue, margin, and working capital ceiling into Anaplan / Hyperion FP&A."""
    fpa_id = _deterministic_id("FPA-BRIDGE", scenario_id, idempotency_key)
    payload = {
        "fpa_id": fpa_id,
        "scenario_id": scenario_id,
        "target_revenue_usd": target_revenue_usd,
        "target_gross_margin_usd": target_gross_margin_usd,
        "working_capital_ceiling_usd": working_capital_ceiling_usd,
        "status": "FPA_FINANCIAL_LOCKED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_lock_sop_financial_bridge", payload)
    return payload
