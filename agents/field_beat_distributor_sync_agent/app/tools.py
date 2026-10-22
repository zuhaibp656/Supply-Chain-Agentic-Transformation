"""Deterministic and fixture-backed tools for BeatSync — Field Sales & Distributor Inventory Harmonizer."""
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
    """Returns connected enterprise systems and solver engines for field_beat_distributor_sync_agent."""
    return {
        "agent": "field_beat_distributor_sync_agent",
        "systems": [
            {
                        "id": "dms_distributor_inventory_cloud",
                        "name": "Enterprise Distributor Management System (DMS) Real-Time Stock Ledger",
                        "protocol": "REST API / Webhook",
                        "tables": [
                                    "distributor_dms_live_inventory",
                                    "primary_replenishment_auto_orders"
                        ]
            },
            {
                        "id": "sfa_field_beat_optimizer",
                        "name": "Sales Force Automation (SFA) + Google Maps Beat Route Sequencer",
                        "protocol": "gRPC / Mobile Sync",
                        "tables": [
                                    "fso_daily_beat_store_outlets"
                        ]
            },
            {
                        "id": "pitch_to_stock_recommender",
                        "name": "Vertex AI Pitch-to-Stock Dynamic SKU Substitution Engine",
                        "protocol": "Python / BigQuery ML",
                        "tables": [
                                    "pitch_to_stock_substitution_rules"
                        ]
            },
            {
                        "id": "sap_sd_primary_billing",
                        "name": "SAP S/4HANA SD Primary Factory-to-Distributor Auto-Replenishment",
                        "protocol": "OData v4 / IDoc",
                        "tables": [
                                    "primary_replenishment_auto_orders"
                        ]
            }
]
    }

def query_distributor_dms_live_inventory(
    distributor_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query distributor_dms_live_inventory records from dms_distributor_inventory_cloud."""
    rows = _read_json("distributor_dms_live_inventory.json")
    if distributor_id:
        rows = [r for r in rows if distributor_id.lower() in str(r.get("distributor_id", "")).lower()]
    return {
        "source_system": "dms_distributor_inventory_cloud",
        "table": "distributor_dms_live_inventory",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_fso_daily_beat_store_outlets(
    fso_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query fso_daily_beat_store_outlets records from sfa_field_beat_optimizer."""
    rows = _read_json("fso_daily_beat_store_outlets.json")
    if fso_id:
        rows = [r for r in rows if fso_id.lower() in str(r.get("fso_id", "")).lower()]
    return {
        "source_system": "sfa_field_beat_optimizer",
        "table": "fso_daily_beat_store_outlets",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_pitch_to_stock_substitution_rules(
    stocked_out_sku: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query pitch_to_stock_substitution_rules records from pitch_to_stock_recommender."""
    rows = _read_json("pitch_to_stock_substitution_rules.json")
    if stocked_out_sku:
        rows = [r for r in rows if stocked_out_sku.lower() in str(r.get("stocked_out_sku", "")).lower()]
    return {
        "source_system": "pitch_to_stock_recommender",
        "table": "pitch_to_stock_substitution_rules",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }

def query_primary_replenishment_auto_orders(
    distributor_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query primary_replenishment_auto_orders records from sap_sd_primary_billing."""
    rows = _read_json("primary_replenishment_auto_orders.json")
    if distributor_id:
        rows = [r for r in rows if distributor_id.lower() in str(r.get("distributor_id", "")).lower()]
    return {
        "source_system": "sap_sd_primary_billing",
        "table": "primary_replenishment_auto_orders",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_push_fso_dynamic_beat_and_pitch_list(
    fso_id: Any,
    distributor_id: Any,
    suppressed_sku_id: Any,
    promoted_substitute_sku: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_push_fso_dynamic_beat_and_pitch_list mutation with deterministic audit logging."""
    action_id = _deterministic_id("BEAT-SYNC", fso_id, idempotency_key)
    payload = {
        "dispatch_execution_id": action_id,
        "fso_id": fso_id,
        "distributor_id": distributor_id,
        "suppressed_sku_id": suppressed_sku_id,
        "promoted_substitute_sku": promoted_substitute_sku,
        "rationale": rationale,
        "status": "FSO_BEAT_AND_PITCH_SYNCED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_push_fso_dynamic_beat_and_pitch_list", payload)
    return payload


def action_trigger_distributor_primary_replenishment(
    distributor_id: Any,
    sku_id: Any,
    replenish_cases: Any,
    source_cfa_depot: Any,
    rationale: Any,
    idempotency_key: str
) -> Dict[str, Any]:
    """Execute action_trigger_distributor_primary_replenishment mutation with deterministic audit logging."""
    action_id = _deterministic_id("BEAT-REPL", distributor_id, idempotency_key)
    payload = {
        "secondary_action_id": action_id,
        "distributor_id": distributor_id,
        "sku_id": sku_id,
        "replenish_cases": replenish_cases,
        "source_cfa_depot": source_cfa_depot,
        "rationale": rationale,
        "status": "PRIMARY_REPLENISHMENT_RELEASED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_trigger_distributor_primary_replenishment", payload)
    return payload

