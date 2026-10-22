"""Deterministic and fixture-backed tools for PromiseGuard ATP Order Promising Agent."""
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
    """Returns connected source systems, Cloud Spanner real-time ATP engines, and order management brokers."""
    return {
        "agent": "atp_order_promising_agent",
        "systems": [
            {
                "id": "spanner_realtime_atp_engine",
                "name": "Google Cloud Spanner Global Real-Time ATP / CTP Engine",
                "protocol": "Spanner gRPC / Sub-20ms Strong Consistency Query",
                "tables": ["realtime_sku_atp_allocations"],
            },
            {
                "id": "customer_contract_tier_ledger",
                "name": "SAP S/4HANA Sales & Distribution Customer Allocation Ledger",
                "protocol": "OData v4 / Real-Time Tier Quota Guard",
                "tables": ["customer_tier_sla_commitments"],
            },
            {
                "id": "omnichannel_order_stream",
                "name": "Enterprise OMS / EDI 850 Order Ingestion Event Stream",
                "protocol": "Cloud Pub/Sub / Kafka / Sub-Second Order Event Capture",
                "tables": ["inbound_customer_order_requests"],
            },
            {
                "id": "fulfillment_routing_optimizer",
                "name": "Google OR-Tools Omnichannel Sourcing & Promising Optimizer",
                "protocol": "REST API / Cost-to-Serve & SLA Fulfillment Router",
                "tables": ["order_promising_routing_decisions"],
            }
        ]
    }


def query_realtime_sku_atp_allocations(
    sku_id: str = "",
    network_node_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query real-time available-to-promise (ATP) inventory, capable-to-promise (CTP), and tier reserves."""
    rows = _read_json("realtime_sku_atp_allocations.json")
    all_rows = list(rows)
    if sku_id:
        rows = [r for r in rows if sku_id.lower() in r.get("sku_id", "").lower()]
    if network_node_id:
        rows = [r for r in rows if network_node_id.lower() in r.get("network_node_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "spanner_realtime_atp_engine",
        "table": "realtime_sku_atp_allocations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_customer_tier_sla_commitments(
    customer_id: str = "",
    contract_tier: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query customer contract tier SLAs, minimum fill rate commitments, and OTIF penalty liabilities."""
    rows = _read_json("customer_tier_sla_commitments.json")
    all_rows = list(rows)
    if customer_id:
        rows = [r for r in rows if customer_id.lower() in r.get("customer_id", "").lower()]
    if contract_tier:
        rows = [r for r in rows if contract_tier.lower() in r.get("contract_tier", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "customer_contract_tier_ledger",
        "table": "customer_tier_sla_commitments",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_inbound_customer_order_requests(
    order_id: str = "",
    customer_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query inbound customer order requests awaiting real-time ATP commitment and promised delivery date."""
    rows = _read_json("inbound_customer_order_requests.json")
    all_rows = list(rows)
    if order_id:
        rows = [r for r in rows if order_id.lower() in r.get("order_id", "").lower()]
    if customer_id:
        rows = [r for r in rows if customer_id.lower() in r.get("customer_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "omnichannel_order_stream",
        "table": "inbound_customer_order_requests",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_order_promising_routing_decisions(
    order_id: str = "",
    customer_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query optimal fulfillment node routing decisions, transit hours, and OTIF penalty risk elimination."""
    rows = _read_json("order_promising_routing_decisions.json")
    all_rows = list(rows)
    if order_id:
        rows = [r for r in rows if order_id.lower() in r.get("order_id", "").lower()]
    if customer_id:
        rows = [r for r in rows if customer_id.lower() in r.get("customer_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "fulfillment_routing_optimizer",
        "table": "order_promising_routing_decisions",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_commit_dynamic_order_promise(
    order_id: str,
    customer_id: str,
    promised_fulfillment_node: str,
    promised_delivery_date: str,
    atp_reserved_qty: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Commit binding ATP order promise and reserve inventory allocations across Cloud Spanner and OMS."""
    promise_id = _deterministic_id("PROMISE-COMMIT", order_id, customer_id, idempotency_key)
    payload = {
        "promise_id": promise_id,
        "order_id": order_id,
        "customer_id": customer_id,
        "promised_fulfillment_node": promised_fulfillment_node,
        "promised_delivery_date": promised_delivery_date,
        "atp_reserved_qty": atp_reserved_qty,
        "spanner_txn_id": f"SPAN-TXN-{promise_id[-6:]}",
        "status": "ATP_PROMISE_COMMITTED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_commit_dynamic_order_promise", payload)
    return payload


def action_protect_tier1_allocation_reserve(
    sku_id: str,
    network_node_id: str,
    reserve_quantity: int,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Ringfence inventory quota for strategic Tier 1 contract customers to prevent unauthorized depletion."""
    protection_id = _deterministic_id("TIER-RINGFENCE", sku_id, network_node_id, idempotency_key)
    payload = {
        "protection_id": protection_id,
        "sku_id": sku_id,
        "network_node_id": network_node_id,
        "reserve_quantity": reserve_quantity,
        "status": "TIER1_ALLOCATION_RINGFENCED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_protect_tier1_allocation_reserve", payload)
    return payload
