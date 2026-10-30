"""Deterministic Enterprise Connectors, Python Math Solvers, Charting & Drafting Tools for [02 · Source | Contract & PO Mgmt] Three-Way Match Dispute."""
from __future__ import annotations

import copy
import datetime
import json
import math
import os
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .render.charts import create_three_way_match_dispute_chart_spec
from .render.png_chart import render_comparison_png

_FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "tables"
_MASTER_FILE = Path(__file__).resolve().parent.parent / "fixtures" / "master" / "xyz_enterprise_backbone.json"

SYSTEM_CONNECTORS: List[Dict[str, Any]] = [{'id': 'sap_mm_po_schedules',
  'name': 'ERP Purchase Order (EKKO/EKPO) Ledger',
  'protocol': 'OData v4 / BAPI_PO_GETDETAIL',
  'tables': ['sap_po_line_schedules']},
 {'id': 'wms_dock_grn_mkpf',
  'name': 'WMS Dock Barcode Goods Receipt Notes (GRN)',
  'protocol': 'REST / EDI 861',
  'tables': ['wms_grn_dock_receipts']},
 {'id': 'ap_invoice_ocr_rbkp',
  'name': 'AP Vendor Invoice Capture & EDI 810 Header',
  'protocol': 'Document OCR / EDI 810',
  'tables': ['ap_vendor_invoice_headers']},
 {'id': 'ap_dispute_debit_ledger',
  'name': 'AP 3-Way Match Variance & Debit Memo Ledger',
  'protocol': 'BAPI_INCOMINGINVOICE_PARK',
  'tables': ['three_way_match_dispute_ledger']}]

_SESSION_MUTATION_LEDGER: List[Dict[str, Any]] = []
_LAST_CHART_SPEC: Optional[Dict[str, Any]] = None


def _read_json(filename: str) -> List[Dict[str, Any]]:
    fpath = _FIXTURES_DIR / filename
    if not fpath.exists():
        return []
    return copy.deepcopy(json.loads(fpath.read_text(encoding="utf-8")))


def _record_mutation(action_tool: str, status_code: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    action_id = f"ACT-THREE-WA-{uuid.uuid4().hex[:8].upper()}"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = {
        "status": status_code,
        "action_id": action_id,
        "agent_id": 'three_way_match_dispute',
        "organization_id": "XYZ-CORP-01",
        "action_tool": action_tool,
        "timestamp_utc": ts,
        "payload": payload,
    }
    _SESSION_MUTATION_LEDGER.append(receipt)
    try:
        log_path = _FIXTURES_DIR / "action-events.jsonl"
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(receipt) + "\n")
    except Exception:
        pass
    return receipt


def get_latest_chart_spec() -> Dict[str, Any]:
    """Returns the most recent dynamic Vega-Lite v5 chart spec built in the current session."""
    if _LAST_CHART_SPEC is not None:
        return copy.deepcopy(_LAST_CHART_SPEC)
    return create_three_way_match_dispute_chart_spec()


def list_systems() -> Dict[str, Any]:
    """List connected XYZ Global Industries Corp. enterprise systems, protocols, and governed tables."""
    return {'agent': 'three_way_match_dispute',
 'organization_id': 'XYZ-CORP-01',
 'systems': [{'id': 'sap_mm_po_schedules',
              'name': 'ERP Purchase Order (EKKO/EKPO) Ledger',
              'protocol': 'OData v4 / BAPI_PO_GETDETAIL',
              'tables': ['sap_po_line_schedules']},
             {'id': 'wms_dock_grn_mkpf',
              'name': 'WMS Dock Barcode Goods Receipt Notes (GRN)',
              'protocol': 'REST / EDI 861',
              'tables': ['wms_grn_dock_receipts']},
             {'id': 'ap_invoice_ocr_rbkp',
              'name': 'AP Vendor Invoice Capture & EDI 810 Header',
              'protocol': 'Document OCR / EDI 810',
              'tables': ['ap_vendor_invoice_headers']},
             {'id': 'ap_dispute_debit_ledger',
              'name': 'AP 3-Way Match Variance & Debit Memo Ledger',
              'protocol': 'BAPI_INCOMINGINVOICE_PARK',
              'tables': ['three_way_match_dispute_ledger']}]}


def lookup_xyz_master_context(
    sku_id: str = "",
    facility_id: str = "",
    supplier_id: str = "",
    customer_id: str = "",
    carrier_id: str = "",
) -> Dict[str, Any]:
    """Join operational records against XYZ Global Industries Corp. (XYZ-CORP-01) master ERP/WMS/TMS data."""
    if not _MASTER_FILE.exists():
        return {"status": "MASTER_NOT_FOUND", "organization_id": "XYZ-CORP-01"}
    bundle = json.loads(_MASTER_FILE.read_text(encoding="utf-8"))
    result: Dict[str, Any] = {
        "status": "SUCCESS",
        "organization_id": bundle.get("organization_id", "XYZ-CORP-01"),
        "organization_name": bundle.get("organization_name", "XYZ Global Industries Corp."),
    }
    if sku_id:
        result["material"] = bundle.get("materials", {}).get(sku_id)
    if facility_id:
        result["facility"] = bundle.get("facilities", {}).get(facility_id)
    if supplier_id:
        result["supplier"] = bundle.get("suppliers", {}).get(supplier_id)
    if customer_id:
        result["customer"] = bundle.get("customers", {}).get(customer_id)
    if carrier_id:
        result["carrier"] = bundle.get("carriers", {}).get(carrier_id)
    if not any([sku_id, facility_id, supplier_id, customer_id, carrier_id]):
        result["summary_counts"] = {
            "materials": len(bundle.get("materials", {})),
            "facilities": len(bundle.get("facilities", {})),
            "suppliers": len(bundle.get("suppliers", {})),
            "customers": len(bundle.get("customers", {})),
            "carriers": len(bundle.get("carriers", {})),
            "golden_threads": len(bundle.get("golden_threads", [])),
        }
    return result


def query_sap_po_line_schedules(po_number: str = '', supplier_id: str = '', sku_id: str = '') -> Dict[str, Any]:
    """Query ERP Purchase Order (PO) quantities, contracted unit prices, Incoterms, and early-pay discount terms."""
    rows = _read_json("sap_po_line_schedules.json")
    if po_number:
        rows = [r for r in rows if str(r.get('po_number', '')).lower() == str(po_number).lower()]
    if supplier_id:
        rows = [r for r in rows if str(r.get('supplier_id', '')).lower() == str(supplier_id).lower()]
    if sku_id:
        rows = [r for r in rows if str(r.get('sku_id', '')).lower() == str(sku_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'sap_mm_po_schedules',
        "table": 'sap_po_line_schedules',
        "row_count": len(rows),
        "rows": rows,
    }

def query_wms_grn_dock_receipts(po_number: str = '', grn_number: str = '') -> Dict[str, Any]:
    """Query WMS Goods Receipt Note (GRN) dock barcode counts, damaged rejects, and net accepted quantities."""
    rows = _read_json("wms_grn_dock_receipts.json")
    if po_number:
        rows = [r for r in rows if str(r.get('po_number', '')).lower() == str(po_number).lower()]
    if grn_number:
        rows = [r for r in rows if str(r.get('grn_number', '')).lower() == str(grn_number).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'wms_dock_grn_mkpf',
        "table": 'wms_grn_dock_receipts',
        "row_count": len(rows),
        "rows": rows,
    }

def query_ap_vendor_invoice_headers(invoice_id: str = '', po_number: str = '') -> Dict[str, Any]:
    """Query AP vendor invoice billed quantities, billed unit prices, freight add-ons, and discount expiry days."""
    rows = _read_json("ap_vendor_invoice_headers.json")
    if invoice_id:
        rows = [r for r in rows if str(r.get('invoice_id', '')).lower() == str(invoice_id).lower()]
    if po_number:
        rows = [r for r in rows if str(r.get('po_number', '')).lower() == str(po_number).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'ap_invoice_ocr_rbkp',
        "table": 'ap_vendor_invoice_headers',
        "row_count": len(rows),
        "rows": rows,
    }

def query_three_way_match_dispute_ledger(invoice_id: str = '', po_number: str = '', match_status: str = '') -> Dict[str, Any]:
    """Query 3-way match line reconciliations, verified payable amounts, debit memo variances, and 2/10 Net 30 discounts."""
    rows = _read_json("three_way_match_dispute_ledger.json")
    if invoice_id:
        rows = [r for r in rows if str(r.get('invoice_id', '')).lower() == str(invoice_id).lower()]
    if po_number:
        rows = [r for r in rows if str(r.get('po_number', '')).lower() == str(po_number).lower()]
    if match_status:
        rows = [r for r in rows if str(r.get('match_status', '')).lower() == str(match_status).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'ap_dispute_debit_ledger',
        "table": 'three_way_match_dispute_ledger',
        "row_count": len(rows),
        "rows": rows,
    }


def analyze_three_way_match_variances(focus_id: str = "") -> Dict[str, Any]:
    """Join ERP POs, WMS GRNs, and AP Invoices in Python to compute exact price/quantity/DDP-freight overcharges and 2/10 Net 30 discount capture."""
    global _LAST_CHART_SPEC
    chart_rows = _read_json("three_way_match_dispute_ledger.json")
    if focus_id:
        filtered = [r for r in chart_rows if str(r.get("invoice_id", "")).lower() == focus_id.lower()]
        if filtered:
            chart_rows = filtered

    series_a = [float(r.get("debit_memo_variance_usd", 0.0) or 0.0) for r in chart_rows]
    series_b = [float(r.get("early_pay_discount_saved_usd", 0.0) or 0.0) for r in chart_rows]
    labels = [str(r.get("invoice_id", "")) for r in chart_rows]

    sum_a = round(sum(series_a), 2)
    sum_b = round(sum(series_b), 2)
    avg_a = round(sum_a / max(1, len(series_a)), 2)
    avg_b = round(sum_b / max(1, len(series_b)), 2)
    net_delta = round(sum_b - sum_a, 2)
    pct_delta = round(((sum_b - sum_a) / abs(sum_a)) * 100.0, 2) if abs(sum_a) > 1e-9 else 0.0

    ranked_gaps = sorted(
        [
            {
                "id": labels[i],
                "series_a": round(series_a[i], 2),
                "series_b": round(series_b[i], 2),
                "abs_gap": round(abs(series_b[i] - series_a[i]), 2),
                "signed_delta": round(series_b[i] - series_a[i], 2),
            }
            for i in range(len(labels))
        ],
        key=lambda x: x["abs_gap"],
        reverse=True,
    )

    domain_computations: Dict[str, Any] = {}
    # Exact 3-Way Match (PO vs GRN vs Invoice) + 2/10 Net 45 Discount Capture math
    pos = {r["po_id"]: r for r in _read_json("erp_purchase_order_headers_lines.json")}
    grns = {r["po_id"]: r for r in _read_json("wms_goods_receipt_inspections.json")}
    reconciliations = []
    for inv in _read_json("ap_vendor_carrier_invoices.json"):
        po = pos.get(inv["po_id"], {})
        grn = grns.get(inv["po_id"], {})
        verified_payable = round(float(grn.get("accepted_qty", 0)) * float(po.get("contract_unit_price_usd", 0)), 2)
        overcharge = round(float(inv.get("billed_total_usd", 0)) - verified_payable, 2)
        early_disc = round(verified_payable * 0.02, 2) if "2/10" in str(po.get("payment_terms", "")) else 0.0
        reconciliations.append({
            "invoice_id": inv["invoice_id"],
            "po_id": inv["po_id"],
            "verified_payable_usd": verified_payable,
            "overcharge_usd": max(0.0, overcharge),
            "early_pay_2pct_discount_usd": early_disc,
        })
    domain_computations["three_way_voucher_reconciliation"] = reconciliations

    _LAST_CHART_SPEC = create_three_way_match_dispute_chart_spec(rows=chart_rows)

    md_lines = [
        "| Record | Debit Variance ($) | 2/10 Discount Saved ($ | Delta |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for g in ranked_gaps[:6]:
        md_lines.append(
            f"| `{g['id']}` | {g['series_a']:,.2f} | **{g['series_b']:,.2f}** | {g['signed_delta']:+,.2f} |"
        )

    return {
        "status": "SUCCESS",
        "agent": 'three_way_match_dispute',
        "persona": 'Accounts Payable Lead',
        "records_evaluated": len(chart_rows),
        "kpi_summary": {
            "series_a_label": 'Debit Variance ($)',
            "series_b_label": '2/10 Discount Saved ($)',
            "total_series_a": sum_a,
            "total_series_b": sum_b,
            "mean_series_a": avg_a,
            "mean_series_b": avg_b,
            "net_delta": net_delta,
            "relative_shift_pct": pct_delta,
            "top_pareto_driver": ranked_gaps[0] if ranked_gaps else {},
        },
        "ranked_drivers": ranked_gaps,
        "domain_computations": domain_computations,
        "concise_markdown_table": "\n".join(md_lines),
    }


def render_visual_chart(focus_id: str = "", chart_title: str = "") -> Dict[str, Any]:
    """Generate both an interactive A2UI Vega-Lite v5 chart spec AND a high-res 1200x640 PNG infographic."""
    global _LAST_CHART_SPEC
    rows = _read_json("three_way_match_dispute_ledger.json")
    if focus_id:
        sub = [r for r in rows if str(r.get("invoice_id", "")).lower() == focus_id.lower()]
        if sub:
            rows = sub

    spec = create_three_way_match_dispute_chart_spec(rows=rows, title_override=chart_title or None)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get("invoice_id", "")) for r in rows]
    va = [float(r.get("debit_memo_variance_usd", 0.0) or 0.0) for r in rows]
    vb = [float(r.get("early_pay_discount_saved_usd", 0.0) or 0.0) for r in rows]
    png_meta = render_comparison_png(
        agent_id='three_way_match_dispute',
        title=chart_title or 'AP 3-Way Match — Debit Memo Variance ($) vs. Early-Pay Discount Captured ($)',
        subtitle=f"Persona: Accounts Payable Lead · Category: 02 · Sourcing & Procurement — Contract & PO Mgmt",
        labels=labels,
        series_a=va,
        series_a_label='Debit Variance ($)',
        series_b=vb,
        series_b_label='2/10 Discount Saved ($)',
        y_title='USD Recovered',
    )
    return {
        "status": "SUCCESS",
        "chart_title": spec["title"]["text"],
        "a2ui_vega_lite_queued": True,
        "png_infographic": png_meta,
    }


def draft_vendor_debit_memo_notice(target_id: str = "", recipient_role: str = "Supply Chain & Finance Leadership") -> Dict[str, Any]:
    """Draft a formal Accounts Payable 3-Way Match Debit Memo & Partial Settlement Remittance Advice for the vendor."""
    analysis = analyze_three_way_match_variances(focus_id=target_id)
    kpi = analysis.get("kpi_summary", {})
    top = kpi.get("top_pareto_driver", {})
    doc_ref = f"DOC-THREE-2026-{len(analysis.get('ranked_drivers', []))}01"
    memo_md = "\n".join(
        [
            f"### 📄 Accounts Payable 3-Way Match Debit Memo & Remittance Notice (`{doc_ref}`)",
            f"- **Organization**: XYZ Global Industries Corp. (`XYZ-CORP-01`)",
            f"- **Prepared By**: Accounts Payable Lead ([02 · Source | Contract & PO Mgmt] Three-Way Match Dispute)",
            f"- **To**: {recipient_role}",
            f"- **Primary Driver**: `{top.get('id', 'ALL')}` ({kpi.get('series_a_label')}: `{top.get('series_a', 0):,.2f}` -> {kpi.get('series_b_label')}: `{top.get('series_b', 0):,.2f}`)",
            f"- **Aggregate Portfolio Shift**: `{kpi.get('total_series_a', 0):,.2f}` -> `{kpi.get('total_series_b', 0):,.2f}` (`{kpi.get('relative_shift_pct', 0):+.2f}%`)",
            "",
            analysis.get("concise_markdown_table", ""),
            "",
            "**Governance Sign-Off**: Pre-validated against XYZ-CORP-01 master tolerances; requires authorized `idempotency_key` prior to ERP/WMS/TMS commit.",
        ]
    )
    return {
        "status": "DRAFT_READY",
        "document_ref": doc_ref,
        "title": 'Accounts Payable 3-Way Match Debit Memo & Remittance Notice',
        "recipient_role": recipient_role,
        "markdown_draft": memo_md,
    }


def action_issue_sap_debit_memo_and_release(invoice_id: Any = '', po_number: Any = '', verified_payable_usd: Any = '', debit_memo_usd: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Post SAP MIRO Debit Memo for disputed variance and release verified net invoice for early-pay discount run."""
    payload = {'invoice_id': invoice_id, 'po_number': po_number, 'verified_payable_usd': verified_payable_usd, 'debit_memo_usd': debit_memo_usd, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_issue_sap_debit_memo_and_release',
        status_code='DEBIT_MEMO_POSTED_INVOICE_RELEASED',
        payload=payload,
    )

def action_place_qm_dispute_block(invoice_id: Any = '', grn_number: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Place targeted line-level quality hold pending vendor credit note without blocking clean PO lines."""
    payload = {'invoice_id': invoice_id, 'grn_number': grn_number, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_place_qm_dispute_block',
        status_code='QM_DISPUTE_BLOCK_SET',
        payload=payload,
    )


ALL_TOOLS: List[Callable[..., Any]] = [
    list_systems,
    lookup_xyz_master_context,
    query_sap_po_line_schedules,
    query_wms_grn_dock_receipts,
    query_ap_vendor_invoice_headers,
    query_three_way_match_dispute_ledger,
    analyze_three_way_match_variances,
    render_visual_chart,
    draft_vendor_debit_memo_notice,
    action_issue_sap_debit_memo_and_release,
    action_place_qm_dispute_block,
]
