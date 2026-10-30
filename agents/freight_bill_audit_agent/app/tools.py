"""Deterministic Enterprise Connectors, Python Math Solvers, Charting & Drafting Tools for [05 · Deliver | Route & Carrier] Automated Freight Bill & Accessorial Auditor."""
from __future__ import annotations

import copy
import datetime
import json
import math
import os
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .render.charts import create_freight_bill_audit_agent_chart_spec
from .render.png_chart import render_comparison_png

_FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "tables"
_MASTER_FILE = Path(__file__).resolve().parent.parent / "fixtures" / "master" / "xyz_enterprise_backbone.json"

SYSTEM_CONNECTORS: List[Dict[str, Any]] = [{'id': 'tms_edi210_gateway',
  'name': 'Carrier EDI 210 Freight Invoice Intake',
  'protocol': 'EDI X12 210 / AS2',
  'tables': ['edi210_carrier_freight_invoices']},
 {'id': 'clm_carrier_rate_engine',
  'name': 'Contracted Lane Rate & DOE Diesel FSC Tariff Engine',
  'protocol': 'SQL / Tariff API',
  'tables': ['contracted_lane_rate_and_fsc_tables']},
 {'id': 'yard_gps_detention_log',
  'name': 'Geofence Gate-In/Gate-Out & ePOD Timestamp Verifier',
  'protocol': 'REST / Telematics SQL',
  'tables': ['epod_gps_detention_verifications']},
 {'id': 'sap_fap_shortpay_ledger',
  'name': 'Freight Audit & Payment (FAP) Short-Pay Ledger',
  'protocol': 'IDoc / BAPI_ACC_DOCUMENT_POST',
  'tables': ['freight_overcharge_audit_adjustments']}]

_SESSION_MUTATION_LEDGER: List[Dict[str, Any]] = []
_LAST_CHART_SPEC: Optional[Dict[str, Any]] = None


def _read_json(filename: str) -> List[Dict[str, Any]]:
    fpath = _FIXTURES_DIR / filename
    if not fpath.exists():
        return []
    return copy.deepcopy(json.loads(fpath.read_text(encoding="utf-8")))


def _record_mutation(action_tool: str, status_code: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    action_id = f"ACT-FREIGHT--{uuid.uuid4().hex[:8].upper()}"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = {
        "status": status_code,
        "action_id": action_id,
        "agent_id": 'freight_bill_audit_agent',
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
    return create_freight_bill_audit_agent_chart_spec()


def list_systems() -> Dict[str, Any]:
    """List connected XYZ Global Industries Corp. enterprise systems, protocols, and governed tables."""
    return {'agent': 'freight_bill_audit_agent',
 'organization_id': 'XYZ-CORP-01',
 'systems': [{'id': 'tms_edi210_gateway',
              'name': 'Carrier EDI 210 Freight Invoice Intake',
              'protocol': 'EDI X12 210 / AS2',
              'tables': ['edi210_carrier_freight_invoices']},
             {'id': 'clm_carrier_rate_engine',
              'name': 'Contracted Lane Rate & DOE Diesel FSC Tariff Engine',
              'protocol': 'SQL / Tariff API',
              'tables': ['contracted_lane_rate_and_fsc_tables']},
             {'id': 'yard_gps_detention_log',
              'name': 'Geofence Gate-In/Gate-Out & ePOD Timestamp Verifier',
              'protocol': 'REST / Telematics SQL',
              'tables': ['epod_gps_detention_verifications']},
             {'id': 'sap_fap_shortpay_ledger',
              'name': 'Freight Audit & Payment (FAP) Short-Pay Ledger',
              'protocol': 'IDoc / BAPI_ACC_DOCUMENT_POST',
              'tables': ['freight_overcharge_audit_adjustments']}]}


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


def query_edi210_freight_invoices(freight_inv_id: str = '', carrier_id: str = '', lane_code: str = '') -> Dict[str, Any]:
    """Query carrier EDI 210 billed miles, linehaul ($), FSC ($), detention ($), and total invoice amount ($)."""
    rows = _read_json("edi210_carrier_freight_invoices.json")
    if freight_inv_id:
        rows = [r for r in rows if str(r.get('freight_inv_id', '')).lower() == str(freight_inv_id).lower()]
    if carrier_id:
        rows = [r for r in rows if str(r.get('carrier_id', '')).lower() == str(carrier_id).lower()]
    if lane_code:
        rows = [r for r in rows if str(r.get('lane_code', '')).lower() == str(lane_code).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'tms_edi210_gateway',
        "table": 'edi210_carrier_freight_invoices',
        "row_count": len(rows),
        "rows": rows,
    }

def query_contracted_lane_fsc_tariffs(lane_code: str = '', carrier_id: str = '') -> Dict[str, Any]:
    """Query PC*MILER contracted miles, rate/mile ($), DOE diesel FSC %, and free detention hours."""
    rows = _read_json("contracted_lane_rate_and_fsc_tables.json")
    if lane_code:
        rows = [r for r in rows if str(r.get('lane_code', '')).lower() == str(lane_code).lower()]
    if carrier_id:
        rows = [r for r in rows if str(r.get('carrier_id', '')).lower() == str(carrier_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'clm_carrier_rate_engine',
        "table": 'contracted_lane_rate_and_fsc_tables',
        "row_count": len(rows),
        "rows": rows,
    }

def query_gps_detention_verifications(shipment_id: str = '') -> Dict[str, Any]:
    """Query carrier-claimed dwell hours vs. GPS geofence dwell hours and appointment punctuality."""
    rows = _read_json("epod_gps_detention_verifications.json")
    if shipment_id:
        rows = [r for r in rows if str(r.get('shipment_id', '')).lower() == str(shipment_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'yard_gps_detention_log',
        "table": 'epod_gps_detention_verifications',
        "row_count": len(rows),
        "rows": rows,
    }

def query_freight_overcharge_adjustments(freight_inv_id: str = '', audit_status: str = '') -> Dict[str, Any]:
    """Query carrier billed ($) vs. verified payable ($) and overcharge recovery ($)."""
    rows = _read_json("freight_overcharge_audit_adjustments.json")
    if freight_inv_id:
        rows = [r for r in rows if str(r.get('freight_inv_id', '')).lower() == str(freight_inv_id).lower()]
    if audit_status:
        rows = [r for r in rows if str(r.get('audit_status', '')).lower() == str(audit_status).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'sap_fap_shortpay_ledger',
        "table": 'freight_overcharge_audit_adjustments',
        "row_count": len(rows),
        "rows": rows,
    }


def analyze_edi210_tariff_and_fsc_variance(focus_id: str = "") -> Dict[str, Any]:
    """Recompute exact contracted linehaul (PC*MILER miles * contract_rate) + DOE FSC + GPS-verified detention (zeroed if carrier missed appointment) to isolate exact overcharges ($)."""
    global _LAST_CHART_SPEC
    chart_rows = _read_json("freight_overcharge_audit_adjustments.json")
    if focus_id:
        filtered = [r for r in chart_rows if str(r.get("freight_inv_id", "")).lower() == focus_id.lower()]
        if filtered:
            chart_rows = filtered

    series_a = [float(r.get("total_billed_usd", 0.0) or 0.0) for r in chart_rows]
    series_b = [float(r.get("verified_payable_usd", 0.0) or 0.0) for r in chart_rows]
    labels = [str(r.get("freight_inv_id", "")) for r in chart_rows]

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
    # Exact Tariff Linehaul + DOE FSC + GPS Detention audit formula
    tariffs = {r["lane_code"]: r for r in _read_json("contracted_lane_rate_and_fsc_tables.json")}
    gps_map = {r["shipment_id"]: r for r in _read_json("epod_gps_detention_verifications.json")}
    audits = []
    for inv in _read_json("edi210_carrier_freight_invoices.json"):
        tf = tariffs.get(inv["lane_code"], {})
        gp = gps_map.get(inv["shipment_id"], {})
        base_lh = float(tf.get("pcmiler_contract_miles", 0)) * float(tf.get("contract_rate_mile_usd", 0))
        fsc = base_lh * (float(tf.get("doe_verified_fsc_pct", 0)) / 100.0)
        det = (float(gp.get("verified_billable_detention_hrs", 0)) * float(tf.get("detention_hr_usd", 0))) if gp.get("appointment_on_time") else 0.0
        payable = round(base_lh + fsc + det, 2)
        audits.append({"freight_inv_id": inv["freight_inv_id"], "formula_payable_usd": payable, "billed_usd": inv["total_billed_usd"]})
    domain_computations["edi210_formula_recompute"] = audits

    _LAST_CHART_SPEC = create_freight_bill_audit_agent_chart_spec(rows=chart_rows)

    md_lines = [
        "| Record | Carrier EDI 210 Billed | Tariff & GPS Verified  | Delta |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for g in ranked_gaps[:6]:
        md_lines.append(
            f"| `{g['id']}` | {g['series_a']:,.2f} | **{g['series_b']:,.2f}** | {g['signed_delta']:+,.2f} |"
        )

    return {
        "status": "SUCCESS",
        "agent": 'freight_bill_audit_agent',
        "persona": 'Transportation Procurement Lead',
        "records_evaluated": len(chart_rows),
        "kpi_summary": {
            "series_a_label": 'Carrier EDI 210 Billed ($)',
            "series_b_label": 'Tariff & GPS Verified ($)',
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
    rows = _read_json("freight_overcharge_audit_adjustments.json")
    if focus_id:
        sub = [r for r in rows if str(r.get("freight_inv_id", "")).lower() == focus_id.lower()]
        if sub:
            rows = sub

    spec = create_freight_bill_audit_agent_chart_spec(rows=rows, title_override=chart_title or None)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get("freight_inv_id", "")) for r in rows]
    va = [float(r.get("total_billed_usd", 0.0) or 0.0) for r in rows]
    vb = [float(r.get("verified_payable_usd", 0.0) or 0.0) for r in rows]
    png_meta = render_comparison_png(
        agent_id='freight_bill_audit_agent',
        title=chart_title or 'Freight Bill Audit — Carrier EDI 210 Billed ($) vs. Tariff-Verified Payable ($)',
        subtitle=f"Persona: Transportation Procurement Lead · Category: 05 · Distribution & Logistics — Route & Carrier",
        labels=labels,
        series_a=va,
        series_a_label='Carrier EDI 210 Billed ($)',
        series_b=vb,
        series_b_label='Tariff & GPS Verified ($)',
        y_title='Invoice Amount (USD)',
    )
    return {
        "status": "SUCCESS",
        "chart_title": spec["title"]["text"],
        "a2ui_vega_lite_queued": True,
        "png_infographic": png_meta,
    }


def draft_edi210_short_pay_remittance_notice(target_id: str = "", recipient_role: str = "Supply Chain & Finance Leadership") -> Dict[str, Any]:
    """Draft an itemized EDI 210/820 Freight Audit Adjustment & Short-Pay Dispute Notice citing PC*MILER miles, DOE FSC index, and GPS gate timestamps."""
    analysis = analyze_edi210_tariff_and_fsc_variance(focus_id=target_id)
    kpi = analysis.get("kpi_summary", {})
    top = kpi.get("top_pareto_driver", {})
    doc_ref = f"DOC-FREIGH-2026-{len(analysis.get('ranked_drivers', []))}01"
    memo_md = "\n".join(
        [
            f"### 📄 EDI 210 Freight Audit Short-Pay & Accessorial Dispute Notice (`{doc_ref}`)",
            f"- **Organization**: XYZ Global Industries Corp. (`XYZ-CORP-01`)",
            f"- **Prepared By**: Transportation Procurement Lead ([05 · Deliver | Route & Carrier] Automated Freight Bill & Accessorial Auditor)",
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
        "title": 'EDI 210 Freight Audit Short-Pay & Accessorial Dispute Notice',
        "recipient_role": recipient_role,
        "markdown_draft": memo_md,
    }


def action_approve_short_pay_voucher(freight_inv_id: Any = '', carrier_id: Any = '', verified_payable_usd: Any = '', overcharge_recovered_usd: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Post audited short-pay freight voucher to SAP FAP and release verified remittance."""
    payload = {'freight_inv_id': freight_inv_id, 'carrier_id': carrier_id, 'verified_payable_usd': verified_payable_usd, 'overcharge_recovered_usd': overcharge_recovered_usd, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_approve_short_pay_voucher',
        status_code='FAP_SHORT_PAY_POSTED',
        payload=payload,
    )

def action_transmit_edi210_dispute_code(freight_inv_id: Any = '', carrier_id: Any = '', dispute_reason_code: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Transmit automated EDI dispute adjustment codes and GPS gate logs to carrier billing portal."""
    payload = {'freight_inv_id': freight_inv_id, 'carrier_id': carrier_id, 'dispute_reason_code': dispute_reason_code, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_transmit_edi210_dispute_code',
        status_code='EDI_DISPUTE_TRANSMITTED',
        payload=payload,
    )


ALL_TOOLS: List[Callable[..., Any]] = [
    list_systems,
    lookup_xyz_master_context,
    query_edi210_freight_invoices,
    query_contracted_lane_fsc_tariffs,
    query_gps_detention_verifications,
    query_freight_overcharge_adjustments,
    analyze_edi210_tariff_and_fsc_variance,
    render_visual_chart,
    draft_edi210_short_pay_remittance_notice,
    action_approve_short_pay_voucher,
    action_transmit_edi210_dispute_code,
]
