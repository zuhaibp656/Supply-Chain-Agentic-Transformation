"""Deterministic and fixture-backed tools for ChannelSync CPFR Harmonizer."""
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
    """Returns connected source systems, EDI streams, and collaborative CPFR layers."""
    return {
        "agent": "cpfr_sync_agent",
        "systems": [
            {
                "id": "retail_edi_dataflow",
                "name": "Cloud Dataflow Retailer EDI 852 / 830 Ingestion",
                "protocol": "AS2 / SFTP / Cloud PubSub",
                "tables": ["retailer_edi852_daily_pos", "retailer_edi830_order_forecasts"],
            },
            {
                "id": "bigquery_anomaly_vault",
                "name": "BigQuery Zero-Scan Phantom Inventory Anomaly Detector",
                "protocol": "BigQuery SQL / Poisson Process Outlier Model",
                "tables": ["store_phantom_inventory_anomalies"],
            },
            {
                "id": "sap_ibp_cpfr",
                "name": "SAP IBP Collaborative Planning & CPFR Consensus Bridge",
                "protocol": "OData v4 / BAPI_CPFR_RECONCILE",
                "tables": ["joint_cpfr_consensus_packets"],
            },
            {
                "id": "vmi_replenishment_engine",
                "name": "Vendor Managed Inventory (VMI) Replenishment Gateway",
                "protocol": "EDI 855 / EDI 850 Order Dispatch API",
                "tables": [],
            }
        ]
    }


def query_retailer_edi852_pos(
    store_id: str = "",
    retailer: str = "",
    sku_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query normalized daily retailer store POS scans, book inventory, and DC withdrawals."""
    rows = _read_json("retailer_edi852_daily_pos.json")
    all_rows = list(rows)
    if store_id:
        rows = [r for r in rows if store_id.lower() in r.get("store_id", "").lower()]
    if retailer:
        rows = [r for r in rows if retailer.lower() in r.get("retailer", "").lower()]
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "retail_edi_dataflow",
        "table": "retailer_edi852_daily_pos",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_retailer_edi830_forecasts(
    retailer: str = "",
    sku_id: str = "",
    volatility_flag: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query retailer 12-week forward order commitments and detect bullwhip swings."""
    rows = _read_json("retailer_edi830_order_forecasts.json")
    all_rows = list(rows)
    if retailer:
        rows = [r for r in rows if retailer.lower() in r.get("retailer", "").lower()]
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if volatility_flag:
        rows = [r for r in rows if volatility_flag.lower() in r.get("volatility_flag", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "retail_edi_dataflow",
        "table": "retailer_edi830_order_forecasts",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_phantom_inventory_anomalies(
    store_id: str = "",
    retailer: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Identify stores exhibiting zero daily scans despite positive book inventory."""
    rows = _read_json("store_phantom_inventory_anomalies.json")
    all_rows = list(rows)
    if store_id:
        rows = [r for r in rows if store_id.lower() in r.get("store_id", "").lower()]
    if retailer:
        rows = [r for r in rows if retailer.lower() in r.get("retailer", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "bigquery_anomaly_vault",
        "table": "store_phantom_inventory_anomalies",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_joint_cpfr_packets(
    packet_id: str = "",
    retailer: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Retrieve collaborative CPFR exception packets comparing retailer vs manufacturer demand."""
    rows = _read_json("joint_cpfr_consensus_packets.json")
    all_rows = list(rows)
    if packet_id:
        rows = [r for r in rows if packet_id.lower() in r.get("packet_id", "").lower()]
    if retailer:
        rows = [r for r in rows if retailer.lower() in r.get("retailer", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_ibp_cpfr",
        "table": "joint_cpfr_consensus_packets",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_dispatch_vmi_replenishment_order(
    retailer: str,
    sku_id: str,
    target_dc: str,
    order_quantity_units: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Generate and dispatch automated Vendor Managed Inventory (VMI) EDI 855 order to retail DC."""
    po_id = _deterministic_id("VMI-PO", retailer, sku_id, idempotency_key)
    payload = {
        "po_id": po_id,
        "retailer": retailer,
        "sku_id": sku_id,
        "target_dc": target_dc,
        "order_quantity_units": order_quantity_units,
        "status": "VMI_PO_TRANSMITTED_EDI855",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_vmi_replenishment_order", payload)
    return payload


def action_flag_retail_phantom_audit(
    anomaly_id: str,
    store_id: str,
    retailer: str,
    sku_id: str,
    expected_audit_date: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Trigger physical on-shelf cycle count audit task via retailer retail portal API."""
    audit_id = _deterministic_id("AUDIT-TASK", anomaly_id, idempotency_key)
    payload = {
        "audit_id": audit_id,
        "anomaly_id": anomaly_id,
        "store_id": store_id,
        "retailer": retailer,
        "sku_id": sku_id,
        "expected_audit_date": expected_audit_date,
        "status": "STORE_AUDIT_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_flag_retail_phantom_audit", payload)
    return payload
