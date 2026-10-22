"""Deterministic and fixture-backed tools for SourcePulse Parametric Should-Cost Agent."""
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
    """Returns connected source systems, commodity benchmarks, and RFQ optimization engines."""
    return {
        "agent": "rfq_should_cost_agent",
        "systems": [
            {
                "id": "bigquery_commodity_lake",
                "name": "BigQuery Direct Materials & Commodity Index Lake",
                "protocol": "BigQuery SQL / Cortex Sourcing Data Foundation",
                "tables": ["material_should_cost_bom", "commodity_index_rates"],
            },
            {
                "id": "document_ai_rfq_vault",
                "name": "Google Document AI Multi-Bid Quote Ingestion Vault",
                "protocol": "Document AI Form/Table Parser API",
                "tables": ["supplier_rfq_bids"],
            },
            {
                "id": "google_ortools_procurement",
                "name": "Google OR-Tools Combinatorial Dual-Source Award Optimizer",
                "protocol": "OR-Tools MILP Integer Solver",
                "tables": ["award_allocation_scenarios"],
            },
            {
                "id": "sap_ariba_sourcing",
                "name": "SAP Ariba Strategic Sourcing & Contract Workspace",
                "protocol": "Ariba Open API / BAPI_CONTRACT_CREATE",
                "tables": [],
            }
        ]
    }


def query_material_should_cost_bom(
    part_number: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query bottom-up parametric should-cost models and engineering cost drivers."""
    rows = _read_json("material_should_cost_bom.json")
    all_rows = list(rows)
    if part_number:
        rows = [r for r in rows if part_number.lower() in r.get("part_number", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "bigquery_commodity_lake",
        "table": "material_should_cost_bom",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_commodity_index_rates(
    index_symbol: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query live London Metal Exchange (LME), ICIS resin, and ocean freight market indices."""
    rows = _read_json("commodity_index_rates.json")
    all_rows = list(rows)
    if index_symbol:
        rows = [r for r in rows if index_symbol.lower() in r.get("index_symbol", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "bigquery_commodity_lake",
        "table": "commodity_index_rates",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_supplier_rfq_bids(
    part_number: str = "",
    supplier_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Document AI normalized supplier quote proposals and should-cost variances."""
    rows = _read_json("supplier_rfq_bids.json")
    all_rows = list(rows)
    if part_number:
        rows = [r for r in rows if part_number.lower() in r.get("part_number", "").lower()]
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "document_ai_rfq_vault",
        "table": "supplier_rfq_bids",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_combinatorial_award_scenarios(
    scenario_id: str = "",
    part_number: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query OR-Tools solved dual-source award allocations balancing cost and security."""
    rows = _read_json("award_allocation_scenarios.json")
    all_rows = list(rows)
    if scenario_id:
        rows = [r for r in rows if scenario_id.lower() in r.get("scenario_id", "").lower()]
    if part_number:
        rows = [r for r in rows if part_number.lower() in r.get("part_number", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "google_ortools_procurement",
        "table": "award_allocation_scenarios",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_award_supplier_contract(
    scenario_id: str,
    part_number: str,
    primary_supplier: str,
    secondary_supplier: str,
    primary_split_pct: float,
    secondary_split_pct: float,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Commit optimal dual-source contract award to SAP Ariba Sourcing."""
    award_id = _deterministic_id("AWD-ARIBA", scenario_id, part_number, idempotency_key)
    payload = {
        "award_id": award_id,
        "scenario_id": scenario_id,
        "part_number": part_number,
        "primary_supplier": primary_supplier,
        "secondary_supplier": secondary_supplier,
        "primary_split_pct": primary_split_pct,
        "secondary_split_pct": secondary_split_pct,
        "status": "ARIBA_CONTRACT_AWARDED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_award_supplier_contract", payload)
    return payload


def action_challenge_vendor_outlier(
    bid_id: str,
    supplier_id: str,
    part_number: str,
    target_reduction_pct: float,
    should_cost_gap_pct: float,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Generate and dispatch automated should-cost fact-based negotiation challenge letter."""
    challenge_id = _deterministic_id("CHAL-OUTLIER", bid_id, supplier_id, idempotency_key)
    payload = {
        "challenge_id": challenge_id,
        "bid_id": bid_id,
        "supplier_id": supplier_id,
        "part_number": part_number,
        "target_reduction_pct": target_reduction_pct,
        "should_cost_gap_pct": should_cost_gap_pct,
        "status": "NEGOTIATION_CHALLENGE_DISPATCHED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_challenge_vendor_outlier", payload)
    return payload
