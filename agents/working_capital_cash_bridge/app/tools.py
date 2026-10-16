"""Deterministic and fixture-backed tools for Working Capital & Cash Conversion Bridge."""
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
    """Returns connected source systems, financial ledgers, and cash optimization modules."""
    return {
        "agent": "working_capital_cash_bridge",
        "systems": [
            {
                "id": "sap_acdoca_material_ledger",
                "name": "SAP S/4HANA Finance & Material Ledger (ACDOCA)",
                "protocol": "SAP Financial BAPI / RFC / OData",
                "tables": ["inventory_valuation_ledger", "working_capital_metrics"],
            },
            {
                "id": "corporate_treasury_workstation",
                "name": "Global Treasury Management & Cash Forecasting System",
                "protocol": "SWIFT / REST API",
                "tables": ["working_capital_metrics"],
            },
            {
                "id": "supplier_ap_financing_portal",
                "name": "Dynamic Supplier AP Discounting & Working Capital Portal",
                "protocol": "REST API / Cloud SQL",
                "tables": ["supplier_ap_invoices"],
            }
        ]
    }


def query_working_capital_metrics(business_unit: str = "", region: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query enterprise cash conversion cycle (CCC), DIO, DSO, DPO, and trapped working capital."""
    rows = _read_json("working_capital_metrics.json")
    if business_unit:
        b_low = business_unit.lower()
        rows = [r for r in rows if b_low in r.get("business_unit", "").lower()]
    if region:
        r_low = region.lower()
        rows = [r for r in rows if r_low in r.get("region", "").lower()]
    return {
        "source_system": "corporate_treasury_workstation",
        "table": "working_capital_metrics",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_inventory_valuation_ledger(valuation_area: str = "", valuation_class: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query SAP S/4HANA Material Ledger for valuation classes, standard costs, days of supply, and trapped cash."""
    rows = _read_json("inventory_valuation_ledger.json")
    if valuation_area:
        v_low = valuation_area.lower()
        rows = [r for r in rows if v_low in r.get("valuation_area", "").lower()]
    if valuation_class:
        c_low = valuation_class.lower()
        rows = [r for r in rows if c_low in r.get("valuation_class", "").lower()]
    return {
        "source_system": "sap_acdoca_material_ledger",
        "table": "inventory_valuation_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_trapped_cash_opportunities(min_cash_freed_usd: float = 0.0, limit: int = 10) -> Dict[str, Any]:
    """Identify high-ROI buffer reduction and batch rightsizing opportunities that release balance sheet cash."""
    rows = _read_json("trapped_cash_opportunities.json")
    if min_cash_freed_usd > 0:
        rows = [r for r in rows if r.get("cash_freed_usd", 0) >= min_cash_freed_usd]
    return {
        "source_system": "corporate_treasury_workstation",
        "table": "trapped_cash_opportunities",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_ap_supplier_discount_invoices(min_discount_usd: float = 0.0, limit: int = 10) -> Dict[str, Any]:
    """Query eligible supplier AP invoices offering lucrative 2/10 Net 60 early-payment dynamic cash discounts."""
    rows = _read_json("supplier_ap_invoices.json")
    if min_discount_usd > 0:
        rows = [r for r in rows if r.get("cash_discount_amount_usd", 0) >= min_discount_usd]
    return {
        "source_system": "supplier_ap_financing_portal",
        "table": "supplier_ap_invoices",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def action_rebalance_working_capital_buffer(
    target_plant: str,
    target_sku: str,
    recommended_reduction_units: int,
    cash_freed_usd: float,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Autonomous mutation tool to right-size excess inventory buffers and release trapped working capital to treasury."""
    if not target_plant or not target_sku or recommended_reduction_units <= 0 or cash_freed_usd <= 0 or not rationale:
        return {
            "error": "missing_required_arguments",
            "required": ["target_plant", "target_sku", "recommended_reduction_units", "cash_freed_usd", "rationale"]
        }

    rebal_id = _deterministic_id("REBAL-WC", target_plant, target_sku, recommended_reduction_units, idempotency_key or "default")
    record = {
        "rebal_id": rebal_id,
        "target_plant": target_plant,
        "target_sku": target_sku,
        "recommended_reduction_units": recommended_reduction_units,
        "cash_freed_usd": cash_freed_usd,
        "rationale": rationale,
        "status": "BUFFER_RIGHTSIZED",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_rebalance_working_capital_buffer", record)
    return {
        "status": "rebalanced",
        "rebal_id": rebal_id,
        "audit_trail": (
            f"Working capital rightsized [{rebal_id}]: {target_sku} at {target_plant} reduced by "
            f"{recommended_reduction_units} units, releasing ${cash_freed_usd:,.2f} to treasury cash flow. Rationale: {rationale}."
        )
    }


def action_trigger_dynamic_ap_discounting(
    vendor_id: str,
    invoice_id: str,
    early_payment_discount_pct: float,
    cash_discount_usd: float,
    rationale: str,
    idempotency_key: str = ""
) -> Dict[str, Any]:
    """Executes early invoice settlement capture to earn 25-36% annualized risk-free cash discounts."""
    if not vendor_id or not invoice_id or early_payment_discount_pct <= 0 or cash_discount_usd <= 0 or not rationale:
        return {
            "error": "missing_required_arguments",
            "required": ["vendor_id", "invoice_id", "early_payment_discount_pct", "cash_discount_usd", "rationale"]
        }

    discount_id = _deterministic_id("DISC", vendor_id, invoice_id, cash_discount_usd)
    record = {
        "discount_id": discount_id,
        "vendor_id": vendor_id,
        "invoice_id": invoice_id,
        "early_payment_discount_pct": early_payment_discount_pct,
        "cash_discount_usd": cash_discount_usd,
        "rationale": rationale,
        "status": "PAYMENT_SCHEDULED_EARLY",
        "idempotency_key": idempotency_key
    }
    _append_action_event("action_trigger_dynamic_ap_discounting", record)
    return {
        "status": "discount_captured",
        "discount_id": discount_id,
        "audit_trail": (
            f"Dynamic AP discount captured [{discount_id}]: Invoice {invoice_id} ({vendor_id}) approved for early payment "
            f"saving ${cash_discount_usd:,.2f} ({early_payment_discount_pct*100:.1f}% discount). Rationale: {rationale}."
        )
    }
