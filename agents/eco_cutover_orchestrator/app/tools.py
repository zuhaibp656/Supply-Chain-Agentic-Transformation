"""Deterministic and fixture-backed tools for ChangeSync — Engineering Change (ECO) & NPI Cutover Orchestrator."""
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
    """Returns connected enterprise systems and solver engines for eco_cutover_orchestrator."""
    return {
        "agent": "eco_cutover_orchestrator",
        "systems": [
            {
                        "id": "teamcenter_plm_eco_stream",
                        "name": "Siemens Teamcenter / PTC Windchill PLM Engineering Change (ECO) Feed",
                        "protocol": "REST / Webhook",
                        "tables": [
                                    "plm_engineering_change_orders"
                        ]
            },
            {
                        "id": "sap_mm_pp_runout_ledger",
                        "name": "SAP S/4HANA MM/PP Multi-Plant WIP & Open Supplier PO Runout Ledger",
                        "protocol": "OData v4 / BAPI",
                        "tables": [
                                    "multi_plant_predecessor_inventory_runout",
                                    "erp_bom_effectivity_sync_audit"
                        ]
            },
            {
                        "id": "or_tools_eco_cutover_solver",
                        "name": "Google OR-Tools Dynamic BOM Phase-In / Phase-Out Cutover Solver",
                        "protocol": "Python MILP SDK",
                        "tables": [
                                    "eco_optimal_cutover_schedules"
                        ]
            },
            {
                        "id": "ariba_po_revision_updater",
                        "name": "SAP Ariba Open Supplier Purchase Order Revision Cutover Engine",
                        "protocol": "cXML / REST",
                        "tables": [
                                    "erp_bom_effectivity_sync_audit"
                        ]
            }
]
    }

def query_plm_engineering_change_orders(
    eco_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query plm_engineering_change_orders records from teamcenter_plm_eco_stream."""
    rows = _read_json("plm_engineering_change_orders.json")
    all_rows = list(rows)
    if eco_id:
        rows = [r for r in rows if eco_id.lower() in str(r.get("eco_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "teamcenter_plm_eco_stream",
        "table": "plm_engineering_change_orders",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_multi_plant_predecessor_inventory_runout(
    eco_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query multi_plant_predecessor_inventory_runout records from sap_mm_pp_runout_ledger."""
    rows = _read_json("multi_plant_predecessor_inventory_runout.json")
    all_rows = list(rows)
    if eco_id:
        rows = [r for r in rows if eco_id.lower() in str(r.get("eco_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_mm_pp_runout_ledger",
        "table": "multi_plant_predecessor_inventory_runout",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_eco_optimal_cutover_schedules(
    eco_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query eco_optimal_cutover_schedules records from or_tools_eco_cutover_solver."""
    rows = _read_json("eco_optimal_cutover_schedules.json")
    all_rows = list(rows)
    if eco_id:
        rows = [r for r in rows if eco_id.lower() in str(r.get("eco_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "or_tools_eco_cutover_solver",
        "table": "eco_optimal_cutover_schedules",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_erp_bom_effectivity_sync_audit(
    eco_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query erp_bom_effectivity_sync_audit records from ariba_po_revision_updater."""
    rows = _read_json("erp_bom_effectivity_sync_audit.json")
    all_rows = list(rows)
    if eco_id:
        rows = [r for r in rows if eco_id.lower() in str(r.get("eco_id", "")).lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "ariba_po_revision_updater",
        "table": "erp_bom_effectivity_sync_audit",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_lock_multi_plant_eco_effectivity_dates(
    eco_id: Any,
    optimal_effectivity_date: Any,
    scrap_avoided_usd: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_lock_multi_plant_eco_effectivity_dates mutation with deterministic audit logging."""
    action_id = _deterministic_id("ECO-LOCK", eco_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "eco_id": eco_id,
        "optimal_effectivity_date": optimal_effectivity_date,
        "scrap_avoided_usd": scrap_avoided_usd,
        "rationale": rationale,
        "status": "BOM_EFFECTIVITY_LOCKED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_lock_multi_plant_eco_effectivity_dates", payload)
    return payload


def action_modify_open_supplier_po_revision(
    open_po_id: Any,
    predecessor_part: Any,
    successor_part: Any,
    units_converted: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_modify_open_supplier_po_revision mutation with deterministic audit logging."""
    action_id = _deterministic_id("ECO-PO", open_po_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "open_po_id": open_po_id,
        "predecessor_part": predecessor_part,
        "successor_part": successor_part,
        "units_converted": units_converted,
        "rationale": rationale,
        "status": "SUPPLIER_PO_REVISION_UPDATED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_modify_open_supplier_po_revision", payload)
    return payload

