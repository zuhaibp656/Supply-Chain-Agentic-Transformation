"""Deterministic and fixture-backed tools for NexusShield Multi-Tier Network Sentinel."""
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
    """Returns connected source systems, sub-tier knowledge graphs, and mitigation protocols."""
    return {
        "agent": "tier_n_risk_sentinel",
        "systems": [
            {
                "id": "spanner_subtier_graph",
                "name": "Cloud Spanner Multi-Tier Supply Network Knowledge Graph",
                "protocol": "Spanner Graph SQL / Vertex AI GNN",
                "tables": ["subtier_supplier_network", "bom_finished_good_lineage"],
            },
            {
                "id": "weathernext_geopolitical_hub",
                "name": "Google DeepMind WeatherNext 3 & Geopolitical Threat Feed",
                "protocol": "PubSub Streaming / Earth Engine Geospatial GIS",
                "tables": ["active_disruption_threats"],
            },
            {
                "id": "sap_s4hana_po_bridge",
                "name": "SAP S/4HANA Strategic PO Dual-Source Allocation Bridge",
                "protocol": "BAPI_PO_CREATE1 / OData v4",
                "tables": [],
            },
            {
                "id": "meio_buffer_gateway",
                "name": "Multi-Echelon Inventory Optimization (MEIO) Safety Buffer Gateway",
                "protocol": "REST / Event-Driven Webhook",
                "tables": ["mitigation_playbook_options"],
            }
        ]
    }


def query_subtier_network_nodes(
    node_id: str = "",
    tier_level: int = 0,
    chokepoint_only: bool = False,
    limit: int = 10
) -> Dict[str, Any]:
    """Query Tier-1 through Tier-4 supplier dependencies, parents, and single-source chokepoints."""
    rows = _read_json("subtier_supplier_network.json")
    all_rows = list(rows)
    if node_id:
        rows = [r for r in rows if node_id.lower() in r.get("node_id", "").lower()]
    if tier_level > 0:
        rows = [r for r in rows if r.get("tier_level") == tier_level]
    if chokepoint_only:
        rows = [r for r in rows if r.get("single_source_chokepoint") is True]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "spanner_subtier_graph",
        "table": "subtier_supplier_network",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_active_disruption_threats(
    threat_id: str = "",
    threat_type: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query active geopolitical, weather cyclone, seismic, or port halt disruption threats."""
    rows = _read_json("active_disruption_threats.json")
    all_rows = list(rows)
    if threat_id:
        rows = [r for r in rows if threat_id.lower() in r.get("threat_id", "").lower()]
    if threat_type:
        rows = [r for r in rows if threat_type.lower() in r.get("threat_type", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "weathernext_geopolitical_hub",
        "table": "active_disruption_threats",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_bom_revenue_lineage(
    impacted_node: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Trace exposed sub-tier component dependencies to finished goods and revenue at risk."""
    rows = _read_json("bom_finished_good_lineage.json")
    all_rows = list(rows)
    if impacted_node:
        rows = [r for r in rows if impacted_node.lower() in r.get("impacted_subtier_node", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "spanner_subtier_graph",
        "table": "bom_finished_good_lineage",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_mitigation_playbook_options(
    threat_id: str = "",
    playbook_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query pre-qualified backup suppliers, reallocations, expedite costs, and buffer surges."""
    rows = _read_json("mitigation_playbook_options.json")
    all_rows = list(rows)
    if threat_id:
        rows = [r for r in rows if threat_id.lower() in r.get("threat_id", "").lower()]
    if playbook_id:
        rows = [r for r in rows if playbook_id.lower() in r.get("playbook_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "meio_buffer_gateway",
        "table": "mitigation_playbook_options",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_dispatch_dual_source_po_split(
    playbook_id: str,
    backup_supplier: str,
    reallocation_split_pct: float,
    target_po_reallocation_units: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Dispatch PO volume reallocation split to qualified secondary supplier in SAP S/4HANA."""
    po_split_id = _deterministic_id("PO-SPLIT", playbook_id, idempotency_key)
    payload = {
        "po_split_id": po_split_id,
        "playbook_id": playbook_id,
        "backup_supplier": backup_supplier,
        "reallocation_split_pct": reallocation_split_pct,
        "target_po_reallocation_units": target_po_reallocation_units,
        "status": "SAP_PO_SPLIT_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_dispatch_dual_source_po_split", payload)
    return payload


def action_surge_meio_safety_buffer(
    playbook_id: str,
    sku_ids: List[str],
    days_buffer_increase: float,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Trigger dynamic safety buffer surge across regional DCs to absorb supply blackout."""
    buffer_id = _deterministic_id("SURGE-MEIO", playbook_id, idempotency_key)
    payload = {
        "buffer_id": buffer_id,
        "playbook_id": playbook_id,
        "sku_ids": sku_ids,
        "days_buffer_increase": days_buffer_increase,
        "status": "MEIO_BUFFER_SURGE_COMMITTED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_surge_meio_safety_buffer", payload)
    return payload
