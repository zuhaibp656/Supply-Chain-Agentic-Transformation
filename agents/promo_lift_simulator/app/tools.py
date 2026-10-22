"""Deterministic and fixture-backed tools for ElasticityIQ Promo Simulator."""
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
    """Returns connected source systems, trade promotion engines, and causal ML models."""
    return {
        "agent": "promo_lift_simulator",
        "systems": [
            {
                "id": "sap_tpm_salesforce",
                "name": "SAP Trade Promotion Management & Salesforce Consumer Goods Cloud",
                "protocol": "OData v4 / Salesforce REST API",
                "tables": ["planned_promo_campaigns"],
            },
            {
                "id": "bigquery_ml_causal",
                "name": "BigQuery ML Causal Double-ML Elasticity Engine",
                "protocol": "BigQuery ML / Vertex AI Feature Store",
                "tables": ["causal_promo_elasticity", "cross_sku_cannibalization"],
            },
            {
                "id": "alloydb_stock_buffer",
                "name": "AlloyDB PostgreSQL Multi-Echelon Stock Buffer",
                "protocol": "AlloyDB pgvector / MEIO Twin SQL",
                "tables": ["warehouse_promo_availability"],
            },
            {
                "id": "promo_shaping_gateway",
                "name": "Trade Spend & Promotional Shaping Gateway",
                "protocol": "REST Webhook / Enterprise Event Bus",
                "tables": [],
            }
        ]
    }


def query_planned_promo_campaigns(
    campaign_id: str = "",
    retailer: str = "",
    status: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query scheduled retail promotion campaigns, discount mechanics, and trade spend."""
    rows = _read_json("planned_promo_campaigns.json")
    all_rows = list(rows)
    if campaign_id:
        rows = [r for r in rows if campaign_id.lower() in r.get("campaign_id", "").lower()]
    if retailer:
        rows = [r for r in rows if retailer.lower() in r.get("retailer", "").lower()]
    if status:
        rows = [r for r in rows if status.lower() in r.get("status", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_tpm_salesforce",
        "table": "planned_promo_campaigns",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_causal_promo_elasticity(
    sku_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query BigQuery ML Double-ML causal price elasticity and gross lift estimates."""
    rows = _read_json("causal_promo_elasticity.json")
    all_rows = list(rows)
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "bigquery_ml_causal",
        "table": "causal_promo_elasticity",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_cross_sku_cannibalization(
    promoted_sku: str = "",
    risk_level: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Analyze cannibalization volume diverted from sister-SKUs and brand margin loss."""
    rows = _read_json("cross_sku_cannibalization.json")
    all_rows = list(rows)
    if promoted_sku:
        rows = [r for r in rows if promoted_sku.lower() in r.get("promoted_sku", "").lower()]
    if risk_level:
        rows = [r for r in rows if risk_level.lower() in r.get("brand_portfolio_risk", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "bigquery_ml_causal",
        "table": "cross_sku_cannibalization",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_warehouse_promo_availability(
    sku_id: str = "",
    risk_status: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query DC available-to-promise inventory vs promotional demand surge."""
    rows = _read_json("warehouse_promo_availability.json")
    all_rows = list(rows)
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if risk_status:
        rows = [r for r in rows if risk_status.lower() in r.get("post_promo_stockout_risk", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "alloydb_stock_buffer",
        "table": "warehouse_promo_availability",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_shape_promotional_mechanic(
    campaign_id: str,
    adjusted_discount_pct: float,
    bundle_sku: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Reshape promo discount and bundling to maximize net profit and protect warehouse stock."""
    shape_id = _deterministic_id("PROMO-SHAPE", campaign_id, idempotency_key)
    payload = {
        "shape_id": shape_id,
        "campaign_id": campaign_id,
        "adjusted_discount_pct": adjusted_discount_pct,
        "bundle_sku": bundle_sku,
        "status": "PROMO_MECHANIC_RESHAPED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_shape_promotional_mechanic", payload)
    return payload


def action_lock_tpm_calendar(
    campaign_id: str,
    locked_net_lift_units: int,
    committed_trade_spend_usd: float,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Write back finalized promotional calendar and shaped volume curves to SAP TPM & Salesforce."""
    lock_id = _deterministic_id("TPM-LOCK", campaign_id, idempotency_key)
    payload = {
        "lock_id": lock_id,
        "campaign_id": campaign_id,
        "locked_net_lift_units": locked_net_lift_units,
        "committed_trade_spend_usd": committed_trade_spend_usd,
        "status": "TPM_CALENDAR_LOCKED_ACTIVE",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_lock_tpm_calendar", payload)
    return payload
