"""Deterministic and fixture-backed tools for PulseCast Demand Sensing Engine."""
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
    """Returns connected source systems, sensing layers, and integration protocols."""
    return {
        "agent": "demand_sensing_agent",
        "systems": [
            {
                "id": "bigquery_demand_lake",
                "name": "BigQuery Enterprise Demand Lake",
                "protocol": "BigQuery SQL / Cloud Dataflow Streaming",
                "tables": ["pos_store_scans", "external_signals_weathernext", "timesfm_quantile_horizons"],
            },
            {
                "id": "vertex_ai_timesfm",
                "name": "Vertex AI TimesFM Zero-Shot & Fine-Tuned Quantile Forecaster",
                "protocol": "Vertex AI Prediction Endpoint (P10/P50/P90)",
                "tables": ["timesfm_quantile_horizons"],
            },
            {
                "id": "sap_ibp_supply",
                "name": "SAP Integrated Business Planning (IBP)",
                "protocol": "OData v4 / BAPI_PIR_CHANGE / RFC",
                "tables": ["fva_sales_bias"],
            },
            {
                "id": "apigee_ibp_gateway",
                "name": "Google Apigee IBP Enterprise Integration Gateway",
                "protocol": "REST / Event-Driven Webhook",
                "tables": [],
            }
        ]
    }


def query_pos_store_scans(
    store_id: str = "",
    retailer: str = "",
    region: str = "",
    sku_id: str = "",
    stockout_only: bool = False,
    limit: int = 10
) -> Dict[str, Any]:
    """Query daily retailer POS scan sell-through and censored demand records."""
    rows = _read_json("pos_store_scans.json")
    if store_id:
        rows = [r for r in rows if store_id.lower() in r.get("store_id", "").lower()]
    if retailer:
        rows = [r for r in rows if retailer.lower() in r.get("retailer", "").lower()]
    if region:
        rows = [r for r in rows if region.lower() in r.get("region", "").lower()]
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if stockout_only:
        rows = [r for r in rows if r.get("stockout_flag") is True]
    return {
        "source_system": "bigquery_demand_lake",
        "table": "pos_store_scans",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_external_demand_signals(
    region: str = "",
    event_type: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Google DeepMind WeatherNext 3 weather anomalies and Google Maps foot-traffic surges."""
    rows = _read_json("external_signals_weathernext.json")
    if region:
        rows = [r for r in rows if region.lower() in r.get("region", "").lower()]
    if event_type:
        rows = [r for r in rows if event_type.lower() in r.get("event_type", "").lower()]
    return {
        "source_system": "bigquery_demand_lake",
        "table": "external_signals_weathernext",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_timesfm_forecast_horizons(
    sku_id: str = "",
    region: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Vertex AI TimesFM P10/P50/P90 probabilistic demand forecast horizons."""
    rows = _read_json("timesfm_quantile_horizons.json")
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if region:
        rows = [r for r in rows if region.lower() in r.get("region", "").lower()]
    return {
        "source_system": "vertex_ai_timesfm",
        "table": "timesfm_quantile_horizons",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_fva_sales_bias(
    sku_id: str = "",
    bias_type: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Forecast Value Added (FVA) sales override history to identify chronic bias."""
    rows = _read_json("fva_sales_bias.json")
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if bias_type:
        rows = [r for r in rows if bias_type.lower() in r.get("bias_classification", "").lower()]
    return {
        "source_system": "sap_ibp_supply",
        "table": "fva_sales_bias",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_commit_ibp_pir_change(
    sku_id: str,
    plant_or_region: str,
    target_key_figure: str,
    adjusted_pir_units: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Commit sensed demand PIR adjustments directly to SAP IBP Key Figures via Apigee."""
    writeback_id = _deterministic_id("IBP-PIR", sku_id, plant_or_region, target_key_figure, idempotency_key)
    payload = {
        "writeback_id": writeback_id,
        "sku_id": sku_id,
        "plant_or_region": plant_or_region,
        "target_key_figure": target_key_figure,
        "adjusted_pir_units": adjusted_pir_units,
        "status": "IBP_COMMITTED_SUCCESS",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_commit_ibp_pir_change", payload)
    return payload


def action_suppress_fva_bias(
    override_id: str,
    recommended_dampened_units: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Strip chronic sales optimism/pessimism bias from the consensus demand plan."""
    dampen_id = _deterministic_id("FVA-DAMPEN", override_id, idempotency_key)
    payload = {
        "dampen_id": dampen_id,
        "override_id": override_id,
        "recommended_dampened_units": recommended_dampened_units,
        "status": "BIAS_DAMPENED_APPLIED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_suppress_fva_bias", payload)
    return payload
