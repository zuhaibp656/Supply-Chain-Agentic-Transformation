"""Deterministic and fixture-backed tools for CSCO Control Tower Copilot."""
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
    """Returns connected source systems, enterprise digital twins, and integration protocols."""
    return {
        "agent": "csco_control_tower_copilot",
        "systems": [
            {
                "id": "bigquery_sc_twin",
                "name": "BigQuery Multi-Echelon Enterprise Digital Twin",
                "protocol": "BigQuery SQL / Vertex AI Feature Store",
                "tables": ["sc_kpi_summary", "network_bottlenecks", "multiechelon_twin_status"],
            },
            {
                "id": "sap_s4hana_core",
                "name": "SAP S/4HANA Enterprise Resource Planning (ERP)",
                "protocol": "OData v4 / RFC / CDC PubSub",
                "tables": ["cross_erp_order_backlog"],
            },
            {
                "id": "looker_governance",
                "name": "Google Looker Semantic Metric Governance Layer",
                "protocol": "LookML semantic API",
                "tables": ["sc_kpi_summary"],
            },
            {
                "id": "executive_orchestrator",
                "name": "CSCO Executive Decision & Playbook Engine",
                "protocol": "REST API / Event Driven Webhook",
                "tables": ["executive_playbooks"],
            }
        ]
    }


def query_executive_kpis(region: str = "", period: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query high-level executive supply chain KPIs including OTIF, DIO, OEE, Line-Down Risk, and Trapped Working Capital."""
    rows = _read_json("sc_kpi_summary.json")
    if region:
        r_low = region.lower()
        rows = [r for r in rows if r_low in r.get("region", "").lower()]
    if period:
        p_low = period.lower()
        rows = [r for r in rows if p_low in r.get("period", "").lower()]
    return {
        "source_system": "bigquery_sc_twin",
        "table": "sc_kpi_summary",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_network_bottlenecks(severity: str = "", region: str = "", min_impact_usd: float = 0.0, limit: int = 10) -> Dict[str, Any]:
    """Query real-time supply chain bottlenecks, chokepoints, and high-dollar operational jeopardy events."""
    rows = _read_json("network_bottlenecks.json")
    if severity:
        rows = [r for r in rows if severity.upper() == r.get("severity", "").upper()]
    if region:
        r_low = region.lower()
        rows = [r for r in rows if r_low in r.get("region", "").lower()]
    if min_impact_usd > 0:
        rows = [r for r in rows if r.get("revenue_impact_usd", 0) >= min_impact_usd]
    return {
        "source_system": "bigquery_sc_twin",
        "table": "network_bottlenecks",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_multiechelon_twin_status(echelon_level: Optional[int] = None, safety_stock_health: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query multi-echelon node status (Tier-0 plants, Tier-1 central mega-hubs, Tier-2 regional DCs) for buffer health."""
    rows = _read_json("multiechelon_twin_status.json")
    if echelon_level is not None:
        rows = [r for r in rows if r.get("echelon_level") == echelon_level]
    if safety_stock_health:
        rows = [r for r in rows if safety_stock_health.upper() in r.get("safety_stock_health", "").upper()]
    return {
        "source_system": "bigquery_sc_twin",
        "table": "multiechelon_twin_status",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_cross_erp_order_backlog(order_type: str = "", status: str = "", days_delayed_min: int = 0, limit: int = 10) -> Dict[str, Any]:
    """Query cross-ERP customer sales orders and supplier purchase orders currently delayed or in stockout jeopardy."""
    rows = _read_json("cross_erp_order_backlog.json")
    if order_type:
        rows = [r for r in rows if order_type.upper() in r.get("order_type", "").upper()]
    if status:
        rows = [r for r in rows if status.upper() in r.get("status", "").upper()]
    if days_delayed_min > 0:
        rows = [r for r in rows if r.get("days_delayed", 0) >= days_delayed_min]
    return {
        "source_system": "sap_s4hana_core",
        "table": "cross_erp_order_backlog",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_execute_executive_playbook(
    playbook_id: str,
    target_facilities: List[str],
    allocated_budget_usd: float,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Autonomous mutation tool to execute an executive supply chain playbook across plants, hubs, and carriers."""
    if not playbook_id or not target_facilities or allocated_budget_usd <= 0 or not rationale:
        return {
            "error": "missing_required_arguments",
            "required": ["playbook_id", "target_facilities", "allocated_budget_usd", "rationale"]
        }

    # Governance guardrail: budgets over $2,000,000 require CSCO / CFO board signoff
    if allocated_budget_usd > 2000000:
        return {
            "error": "budget_exceeds_delegation_authority",
            "threshold_usd": 2000000,
            "requested_usd": allocated_budget_usd,
            "escalation": "request_csco_cfo_approval"
        }

    execution_id = _deterministic_id("EXEC-PB", playbook_id, allocated_budget_usd, idempotency_key or "default")
    record = {
        "execution_id": execution_id,
        "playbook_id": playbook_id,
        "target_facilities": target_facilities,
        "allocated_budget_usd": allocated_budget_usd,
        "rationale": rationale,
        "status": "EXECUTED_ACTIVE",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_execute_executive_playbook", record)
    return {
        "status": "executed",
        "execution_id": execution_id,
        "audit_trail": (
            f"Executive Playbook '{playbook_id}' executed [{execution_id}] with budget ${allocated_budget_usd:,.2f} "
            f"across {len(target_facilities)} facilities. Rationale: {rationale}."
        )
    }


def action_rebalance_network_allocation(
    source_node: str,
    target_node: str,
    sku_id: str,
    quantity: int,
    expedite_mode: str,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Dispatches lateral inventory rebalancing between multi-echelon nodes to prevent customer stockout."""
    if not source_node or not target_node or not sku_id or quantity <= 0 or not rationale:
        return {
            "error": "missing_required_arguments",
            "required": ["source_node", "target_node", "sku_id", "quantity", "rationale"]
        }

    transfer_id = _deterministic_id("TRF", source_node, target_node, sku_id, quantity)
    record = {
        "transfer_id": transfer_id,
        "source_node": source_node,
        "target_node": target_node,
        "sku_id": sku_id,
        "quantity": quantity,
        "expedite_mode": expedite_mode,
        "rationale": rationale,
        "status": "TRANSFER_ORDER_CREATED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_rebalance_network_allocation", record)
    return {
        "status": "dispatched",
        "transfer_id": transfer_id,
        "audit_trail": (
            f"Stock transfer {transfer_id} created: {quantity} units of {sku_id} moved from {source_node} "
            f"to {target_node} via {expedite_mode}. Rationale: {rationale}."
        )
    }
