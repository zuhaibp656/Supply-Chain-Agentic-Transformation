"""Deterministic and fixture-backed tools for FlowMaster Finite Production Scheduler."""
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
    """Returns connected source systems, mathematical constraint solvers, and SAP PP/DS production interfaces."""
    return {
        "agent": "line_schedule_optimizer",
        "systems": [
            {
                "id": "or_tools_cpsat_solver",
                "name": "Google OR-Tools CP-SAT Finite Capacity Scheduling Engine",
                "protocol": "Python OR-Tools / C++ CP-SAT MIP Engine",
                "tables": ["optimized_sequence_schedule"],
            },
            {
                "id": "sap_ppds_production",
                "name": "SAP S/4HANA Production Planning & Detailed Scheduling (PP/DS)",
                "protocol": "BAPI_PRODORD_CHANGE_STATUS / OData v4",
                "tables": ["production_orders_backlog"],
            },
            {
                "id": "changeover_matrix_vault",
                "name": "Allergen & Color Cleaning-in-Place (CIP) Changeover Matrix Vault",
                "protocol": "PostgreSQL / AlloyDB Static Rules",
                "tables": ["changeover_matrix_rules"],
            },
            {
                "id": "plant_line_workcenters",
                "name": "Shopfloor Aseptic Line Workcenter Registry",
                "protocol": "Siemens Opcenter MES / SAP Work Centers",
                "tables": ["plant_line_workcenters"],
            }
        ]
    }


def query_production_orders_backlog(
    order_id: str = "",
    product_family: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query released unscheduled production orders, allergen flags, batch volumes, and due dates."""
    rows = _read_json("production_orders_backlog.json")
    all_rows = list(rows)
    if order_id:
        rows = [r for r in rows if order_id.lower() in r.get("order_id", "").lower()]
    if product_family:
        rows = [r for r in rows if product_family.lower() in r.get("product_family", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_ppds_production",
        "table": "production_orders_backlog",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_changeover_matrix_rules(
    rule_id: str = "",
    from_family: str = "",
    to_family: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query sequence-dependent changeover matrix wash times, CIP hours, and allergen sanitization rules."""
    rows = _read_json("changeover_matrix_rules.json")
    all_rows = list(rows)
    if rule_id:
        rows = [r for r in rows if rule_id.lower() in r.get("rule_id", "").lower()]
    if from_family:
        rows = [r for r in rows if from_family.lower() in r.get("from_product_family", "").lower()]
    if to_family:
        rows = [r for r in rows if to_family.lower() in r.get("to_product_family", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "changeover_matrix_vault",
        "table": "changeover_matrix_rules",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_plant_line_workcenters(
    workcenter_id: str = "",
    plant_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query plant workcenter rated throughput liters/hr, CIP system specs, and current shift patterns."""
    rows = _read_json("plant_line_workcenters.json")
    all_rows = list(rows)
    if workcenter_id:
        rows = [r for r in rows if workcenter_id.lower() in r.get("workcenter_id", "").lower()]
    if plant_id:
        rows = [r for r in rows if plant_id.lower() in r.get("plant_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "plant_line_workcenters",
        "table": "plant_line_workcenters",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_optimized_sequence_schedule(
    schedule_id: str = "",
    workcenter_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query OR-Tools CP-SAT solved schedule blocks, changeover hours saved, and capacity gains."""
    rows = _read_json("optimized_sequence_schedule.json")
    all_rows = list(rows)
    if schedule_id:
        rows = [r for r in rows if schedule_id.lower() in r.get("schedule_id", "").lower()]
    if workcenter_id:
        rows = [r for r in rows if workcenter_id.lower() in r.get("workcenter_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "or_tools_cpsat_solver",
        "table": "optimized_sequence_schedule",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_solve_and_lock_finite_sequence(
    workcenter_id: str,
    order_ids: List[str],
    objective_type: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute Google OR-Tools CP-SAT solver to sequence production batches with minimum changeover wash hours."""
    sequence_id = _deterministic_id("SEQ-CPSAT", workcenter_id, objective_type, idempotency_key)
    payload = {
        "sequence_id": sequence_id,
        "workcenter_id": workcenter_id,
        "order_ids": order_ids,
        "objective_type": objective_type,
        "changeover_hours_saved": 5.0,
        "status": "OR_TOOLS_SEQUENCE_LOCKED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_solve_and_lock_finite_sequence", payload)
    return payload


def action_dispatch_sap_ppds_sequence(
    schedule_id: str,
    workcenter_id: str,
    sap_plant: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Dispatch locked finite sequence blocks into SAP PP/DS production order execution queue."""
    dispatch_id = _deterministic_id("PPDS-DISP", schedule_id, sap_plant, idempotency_key)
    payload = {
        "dispatch_id": dispatch_id,
        "schedule_id": schedule_id,
        "workcenter_id": workcenter_id,
        "sap_plant": sap_plant,
        "status": "SAP_PPDS_SCHEDULE_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_sap_ppds_sequence", payload)
    return payload
