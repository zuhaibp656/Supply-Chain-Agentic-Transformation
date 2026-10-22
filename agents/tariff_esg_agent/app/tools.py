"""Deterministic and fixture-backed tools for ClauseGuard Contract & Trade Compliance Agent."""
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
    """Returns connected source systems, legal contract intelligence layers, and customs registries."""
    return {
        "agent": "tariff_esg_agent",
        "systems": [
            {
                "id": "alloydb_contract_rag",
                "name": "AlloyDB pgvector Legal Contract & MSA Clause RAG",
                "protocol": "AlloyDB SQL / pgvector cosine embeddings",
                "tables": ["contract_clause_obligations", "supplier_rebate_accruals"],
            },
            {
                "id": "customs_tariff_database",
                "name": "Global Customs & WCO Harmonized System Database",
                "protocol": "USITC / EU TARIC / CROSS Rulings API",
                "tables": ["hs_tariff_classifications", "cross_border_duty_impact"],
            },
            {
                "id": "sap_gts_compliance",
                "name": "SAP Global Trade Services (GTS)",
                "protocol": "OData v4 / BAPI_GTS_CUSTOMS_UPDATE",
                "tables": [],
            },
            {
                "id": "sap_ap_finance",
                "name": "SAP S/4HANA Accounts Payable & Rebate Recovery",
                "protocol": "BAPI_ACC_DOCUMENT_POST / EDI 812 Debit Memo",
                "tables": [],
            }
        ]
    }


def query_contract_clause_obligations(
    contract_id: str = "",
    supplier_id: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query Document AI extracted contract rebate tiers, price caps, and SLA obligations."""
    rows = _read_json("contract_clause_obligations.json")
    all_rows = list(rows)
    if contract_id:
        rows = [r for r in rows if contract_id.lower() in r.get("contract_id", "").lower()]
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "alloydb_contract_rag",
        "table": "contract_clause_obligations",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_supplier_rebate_accruals(
    accrual_id: str = "",
    supplier_id: str = "",
    status: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query earned contractual supplier volume rebates and unrecovered cash leakage."""
    rows = _read_json("supplier_rebate_accruals.json")
    all_rows = list(rows)
    if accrual_id:
        rows = [r for r in rows if accrual_id.lower() in r.get("accrual_id", "").lower()]
    if supplier_id:
        rows = [r for r in rows if supplier_id.lower() in r.get("supplier_id", "").lower()]
    if status:
        rows = [r for r in rows if status.lower() in r.get("status", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "alloydb_contract_rag",
        "table": "supplier_rebate_accruals",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_hs_tariff_classifications(
    part_number: str = "",
    ten_digit_hs_code: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query 10-digit HS tariff classifications, CROSS legal rulings, and FTA eligibility."""
    rows = _read_json("hs_tariff_classifications.json")
    all_rows = list(rows)
    if part_number:
        rows = [r for r in rows if part_number.lower() in r.get("part_number", "").lower()]
    if ten_digit_hs_code:
        rows = [r for r in rows if ten_digit_hs_code in r.get("ten_digit_hs_code", "")]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "customs_tariff_database",
        "table": "hs_tariff_classifications",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_cross_border_duty_impact(
    entry_id: str = "",
    part_number: str = "",
    limit: int = 10
) -> Dict[str, Any]:
    """Query shipment-level customs declarations, preferential duty savings, and CBAM status."""
    rows = _read_json("cross_border_duty_impact.json")
    all_rows = list(rows)
    if entry_id:
        rows = [r for r in rows if entry_id.lower() in r.get("entry_id", "").lower()]
    if part_number:
        rows = [r for r in rows if part_number.lower() in r.get("part_number", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "customs_tariff_database",
        "table": "cross_border_duty_impact",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_lock_hs_tariff_classification(
    part_number: str,
    ten_digit_hs_code: str,
    cross_ruling_reference: str,
    preferential_fta: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Lock legally binding 10-digit HS tariff code and FTA preference in SAP GTS."""
    lock_id = _deterministic_id("GTS-HS", part_number, ten_digit_hs_code, idempotency_key)
    payload = {
        "lock_id": lock_id,
        "part_number": part_number,
        "ten_digit_hs_code": ten_digit_hs_code,
        "cross_ruling_reference": cross_ruling_reference,
        "preferential_fta": preferential_fta,
        "status": "SAP_GTS_HS_LOCKED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_lock_hs_tariff_classification", payload)
    return payload


def action_issue_supplier_rebate_debit_memo(
    accrual_id: str,
    supplier_id: str,
    claim_amount_usd: float,
    contract_reference: str,
    rationale: str,
    idempotency_key: str
) -> Dict[str, Any]:
    """Issue automated debit memo in SAP AP to recover earned supplier volume rebate."""
    debit_id = _deterministic_id("AP-DEBIT", accrual_id, supplier_id, idempotency_key)
    payload = {
        "debit_id": debit_id,
        "accrual_id": accrual_id,
        "supplier_id": supplier_id,
        "claim_amount_usd": claim_amount_usd,
        "contract_reference": contract_reference,
        "status": "SAP_AP_DEBIT_MEMO_POSTED",
        "rationale": rationale,
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_issue_supplier_rebate_debit_memo", payload)
    return payload
