"""Deterministic and fixture-backed tools for EchelonFlow MEIO Allocator."""
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
    """Returns connected source systems, MEIO engines, and WMS inventory nodes."""
    return {
        "agent": "meio_safety_stock_agent",
        "systems": [
            {
                "id": "sap_ibp_meio_engine",
                "name": "SAP Integrated Business Planning (IBP) for MEIO / Clark-Scarf Engine",
                "protocol": "OData v4 / RFC / Multi-Echelon Stochastic Optimization",
                "tables": ["multi_echelon_safety_stock_recommendations"],
            },
            {
                "id": "manhattan_wms_dc_inventory",
                "name": "Manhattan Active WMS Enterprise DC Inventory Ledger",
                "protocol": "REST / OpenAPI v3 / Real-Time Perpetual Inventory Feed",
                "tables": ["dc_inventory_echelon_balances"],
            },
            {
                "id": "lateral_transshipment_service",
                "name": "Oracle OTM / Carrier Fleet Lateral Transshipment Dispatcher",
                "protocol": "EDI 204 / REST API / Inter-DC Rebalance Dispatch",
                "tables": ["lateral_dc_rebalance_transfers"],
            },
            {
                "id": "stockout_risk_predictor",
                "name": "BigQuery ML Stochastic Service Level & Stockout Risk Model",
                "protocol": "BigQuery SQL / Vertex AI TimesFM Monte Carlo Engine",
                "tables": ["echelon_service_level_projections"],
            }
        ]
    }


def query_multi_echelon_safety_stock_recommendations(
    sku_id: str = "",
    echelon_tier: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Clark-Scarf multi-echelon safety stock recommendations, capital freed, and target SLAs."""
    rows = _read_json("multi_echelon_safety_stock_recommendations.json")
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if echelon_tier:
        rows = [r for r in rows if echelon_tier.lower() in r.get("echelon_tier", "").lower()]
    return {
        "source_system": "sap_ibp_meio_engine",
        "table": "multi_echelon_safety_stock_recommendations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_dc_inventory_echelon_balances(
    dc_id: str = "",
    sku_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query on-hand stock, ATP balances, days of supply, and stockout alert status across DC tiers."""
    rows = _read_json("dc_inventory_echelon_balances.json")
    if dc_id:
        rows = [r for r in rows if dc_id.lower() in r.get("dc_id", "").lower()]
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    return {
        "source_system": "manhattan_wms_dc_inventory",
        "table": "dc_inventory_echelon_balances",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_lateral_dc_rebalance_transfers(
    transfer_id: str = "",
    source_dc_id: str = "",
    destination_dc_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query lateral inter-DC stock rebalancing transfers, avoided stockout savings, and transport modes."""
    rows = _read_json("lateral_dc_rebalance_transfers.json")
    if transfer_id:
        rows = [r for r in rows if transfer_id.lower() in r.get("transfer_id", "").lower()]
    if source_dc_id:
        rows = [r for r in rows if source_dc_id.lower() in r.get("source_dc_id", "").lower()]
    if destination_dc_id:
        rows = [r for r in rows if destination_dc_id.lower() in r.get("destination_dc_id", "").lower()]
    return {
        "source_system": "lateral_transshipment_service",
        "table": "lateral_dc_rebalance_transfers",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_echelon_service_level_projections(
    sku_id: str = "",
    network_node_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query stochastic service level projections, baseline stockout risk, and ATP shortfall avoidance."""
    rows = _read_json("echelon_service_level_projections.json")
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if network_node_id:
        rows = [r for r in rows if network_node_id.lower() in r.get("network_node_id", "").lower()]
    return {
        "source_system": "stockout_risk_predictor",
        "table": "echelon_service_level_projections",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_execute_lateral_dc_rebalance(
    source_dc_id: str,
    destination_dc_id: str,
    sku_id: str,
    transfer_quantity: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Dispatch lateral DC-to-DC rebalancing transfer order to avert downstream regional stockout."""
    rebalance_transfer_id = _deterministic_id("REBAL-TRF", source_dc_id, destination_dc_id, sku_id, idempotency_key)
    payload = {
        "rebalance_transfer_id": rebalance_transfer_id,
        "source_dc_id": source_dc_id,
        "destination_dc_id": destination_dc_id,
        "sku_id": sku_id,
        "transfer_quantity_units": transfer_quantity,
        "otm_shipment_id": f"OTM-SHP-{rebalance_transfer_id[-6:]}",
        "status": "LATERAL_REBALANCE_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_execute_lateral_dc_rebalance", payload)
    return payload


def action_update_echelon_safety_stock_policy(
    echelon_tier: str,
    sku_id: str,
    new_safety_stock_units: int,
    target_service_level_pct: float,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Update multi-echelon safety stock policy and reorder parameters in SAP IBP / ERP."""
    policy_update_id = _deterministic_id("MEIO-POL", echelon_tier, sku_id, idempotency_key)
    payload = {
        "policy_update_id": policy_update_id,
        "echelon_tier": echelon_tier,
        "sku_id": sku_id,
        "new_safety_stock_units": new_safety_stock_units,
        "target_service_level_pct": target_service_level_pct,
        "sap_ibp_job_id": f"IBP-JOB-{policy_update_id[-6:]}",
        "status": "MEIO_SAFETY_STOCK_POLICY_UPDATED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_update_echelon_safety_stock_policy", payload)
    return payload
