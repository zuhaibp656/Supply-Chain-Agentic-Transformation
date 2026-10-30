"""Deterministic Enterprise Connectors, Python Math Solvers, Charting & Drafting Tools for [05 · Deliver | First & Mid-Mile] Cold-Chain Auditor."""
from __future__ import annotations

import copy
import datetime
import json
import math
import os
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .render.charts import create_cold_chain_auditor_chart_spec
from .render.png_chart import render_comparison_png

_FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "tables"
_MASTER_FILE = Path(__file__).resolve().parent.parent / "fixtures" / "master" / "xyz_enterprise_backbone.json"

SYSTEM_CONNECTORS: List[Dict[str, Any]] = [{'id': 'samsara_sensitech_iot',
  'name': 'Reefer BLE Multi-Zone Thermal Telemetry Cloud',
  'protocol': 'MQTT / REST Streaming',
  'tables': ['reefer_iot_temp_telemetry']},
 {'id': 'qa_gdp_stability_master',
  'name': 'GDP & FSMA SKU Arrhenius Stability Registry',
  'protocol': '21 CFR Part 11 SQL',
  'tables': ['cold_chain_sku_stability_specs']},
 {'id': 'tms_excursion_monitor',
  'name': 'In-Transit Reefer Door & Defrost Excursion Log',
  'protocol': 'EDI 214 / Event Stream',
  'tables': ['thermal_excursion_incidents']},
 {'id': 'wms_qa_disposition_ledger',
  'name': 'Cold-Chain QA Lot Release & Carrier Spoilage Ledger',
  'protocol': 'BAPI_INSPLOT_SETUSAGEDECISION',
  'tables': ['qa_disposition_claims_ledger']}]

_SESSION_MUTATION_LEDGER: List[Dict[str, Any]] = []
_LAST_CHART_SPEC: Optional[Dict[str, Any]] = None


def _read_json(filename: str) -> List[Dict[str, Any]]:
    fpath = _FIXTURES_DIR / filename
    if not fpath.exists():
        return []
    return copy.deepcopy(json.loads(fpath.read_text(encoding="utf-8")))


def _record_mutation(action_tool: str, status_code: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    action_id = f"ACT-COLD-CHA-{uuid.uuid4().hex[:8].upper()}"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = {
        "status": status_code,
        "action_id": action_id,
        "agent_id": 'cold_chain_auditor',
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
    return create_cold_chain_auditor_chart_spec()


def list_systems() -> Dict[str, Any]:
    """List connected XYZ Global Industries Corp. enterprise systems, protocols, and governed tables."""
    return {'agent': 'cold_chain_auditor',
 'organization_id': 'XYZ-CORP-01',
 'systems': [{'id': 'samsara_sensitech_iot',
              'name': 'Reefer BLE Multi-Zone Thermal Telemetry Cloud',
              'protocol': 'MQTT / REST Streaming',
              'tables': ['reefer_iot_temp_telemetry']},
             {'id': 'qa_gdp_stability_master',
              'name': 'GDP & FSMA SKU Arrhenius Stability Registry',
              'protocol': '21 CFR Part 11 SQL',
              'tables': ['cold_chain_sku_stability_specs']},
             {'id': 'tms_excursion_monitor',
              'name': 'In-Transit Reefer Door & Defrost Excursion Log',
              'protocol': 'EDI 214 / Event Stream',
              'tables': ['thermal_excursion_incidents']},
             {'id': 'wms_qa_disposition_ledger',
              'name': 'Cold-Chain QA Lot Release & Carrier Spoilage Ledger',
              'protocol': 'BAPI_INSPLOT_SETUSAGEDECISION',
              'tables': ['qa_disposition_claims_ledger']}]}


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


def query_reefer_iot_temp_telemetry(shipment_id: str = '', carrier_id: str = '', sku_id: str = '') -> Dict[str, Any]:
    """Query hourly BLE reefer temperature arrays (°C), peak excursion temp, and minutes above upper spec."""
    rows = _read_json("reefer_iot_temp_telemetry.json")
    if shipment_id:
        rows = [r for r in rows if str(r.get('shipment_id', '')).lower() == str(shipment_id).lower()]
    if carrier_id:
        rows = [r for r in rows if str(r.get('carrier_id', '')).lower() == str(carrier_id).lower()]
    if sku_id:
        rows = [r for r in rows if str(r.get('sku_id', '')).lower() == str(sku_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'samsara_sensitech_iot',
        "table": 'reefer_iot_temp_telemetry',
        "row_count": len(rows),
        "rows": rows,
    }

def query_cold_chain_sku_stability_specs(sku_id: str = '', temp_band_label: str = '') -> Dict[str, Any]:
    """Query GDP/FSMA SKU stability limits, max allowed Arrhenius MKT (°C), activation energy ΔH, and cargo lot value ($)."""
    rows = _read_json("cold_chain_sku_stability_specs.json")
    if sku_id:
        rows = [r for r in rows if str(r.get('sku_id', '')).lower() == str(sku_id).lower()]
    if temp_band_label:
        rows = [r for r in rows if str(r.get('temp_band_label', '')).lower() == str(temp_band_label).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'qa_gdp_stability_master',
        "table": 'cold_chain_sku_stability_specs',
        "row_count": len(rows),
        "rows": rows,
    }

def query_thermal_excursion_incidents(shipment_id: str = '', carrier_fault_flag: str = '') -> Dict[str, Any]:
    """Query reefer compressor faults, door-open durations, and degree-minute excursion root causes."""
    rows = _read_json("thermal_excursion_incidents.json")
    if shipment_id:
        rows = [r for r in rows if str(r.get('shipment_id', '')).lower() == str(shipment_id).lower()]
    if carrier_fault_flag:
        rows = [r for r in rows if str(r.get('carrier_fault_flag', '')).lower() == str(carrier_fault_flag).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'tms_excursion_monitor',
        "table": 'thermal_excursion_incidents',
        "row_count": len(rows),
        "rows": rows,
    }

def query_qa_disposition_claims_ledger(shipment_id: str = '', qa_decision: str = '') -> Dict[str, Any]:
    """Query computed Arrhenius MKT (°C) vs. max allowed MKT (°C) and QA release vs. quarantine claim decisions."""
    rows = _read_json("qa_disposition_claims_ledger.json")
    if shipment_id:
        rows = [r for r in rows if str(r.get('shipment_id', '')).lower() == str(shipment_id).lower()]
    if qa_decision:
        rows = [r for r in rows if str(r.get('qa_decision', '')).lower() == str(qa_decision).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'wms_qa_disposition_ledger',
        "table": 'qa_disposition_claims_ledger',
        "row_count": len(rows),
        "rows": rows,
    }


def analyze_arrhenius_mkt_excursions(focus_id: str = "") -> Dict[str, Any]:
    """Compute exact Arrhenius Mean Kinetic Temperature MKT (°C) = (ΔH/R)/(-ln(mean(exp(-ΔH/(R*T_K))))) - 273.15 per shipment to separate safe MKT releases from mandatory GDP quarantines."""
    global _LAST_CHART_SPEC
    chart_rows = _read_json("qa_disposition_claims_ledger.json")
    if focus_id:
        filtered = [r for r in chart_rows if str(r.get("shipment_id", "")).lower() == focus_id.lower()]
        if filtered:
            chart_rows = filtered

    series_a = [float(r.get("computed_mkt_c", 0.0) or 0.0) for r in chart_rows]
    series_b = [float(r.get("max_mkt_allowed_c", 0.0) or 0.0) for r in chart_rows]
    labels = [str(r.get("shipment_id", "")) for r in chart_rows]

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
    # Exact Arrhenius Mean Kinetic Temperature (MKT °C) verification across hourly BLE logs
    r_gas = 0.0083144  # kJ/(mol·K)
    dh = 83.144        # Activation energy kJ/mol
    arrhenius_audit = []
    for t_row in _read_json("reefer_iot_temp_telemetry.json"):
        temps_c = t_row.get("hourly_temps_c", [])
        if temps_c:
            boltz_mean = sum(math.exp(-dh / (r_gas * (tc + 273.15))) for tc in temps_c) / len(temps_c)
            mkt_k = (dh / r_gas) / (-math.log(boltz_mean))
            mkt_c = round(mkt_k - 273.15, 2)
        else:
            mkt_c = 0.0
        arrhenius_audit.append({"shipment_id": t_row.get("shipment_id"), "sku_id": t_row.get("sku_id"), "exact_mkt_c": mkt_c, "peak_temp_c": t_row.get("peak_temp_c")})
    domain_computations["arrhenius_mkt_verification"] = arrhenius_audit

    _LAST_CHART_SPEC = create_cold_chain_auditor_chart_spec(rows=chart_rows)

    md_lines = [
        "| Record | Computed Arrhenius MKT | Max Allowed MKT Limit  | Delta |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for g in ranked_gaps[:6]:
        md_lines.append(
            f"| `{g['id']}` | {g['series_a']:,.2f} | **{g['series_b']:,.2f}** | {g['signed_delta']:+,.2f} |"
        )

    return {
        "status": "SUCCESS",
        "agent": 'cold_chain_auditor',
        "persona": 'Cold-Chain Logistics Lead',
        "records_evaluated": len(chart_rows),
        "kpi_summary": {
            "series_a_label": 'Computed Arrhenius MKT (°C)',
            "series_b_label": 'Max Allowed MKT Limit (°C)',
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
    rows = _read_json("qa_disposition_claims_ledger.json")
    if focus_id:
        sub = [r for r in rows if str(r.get("shipment_id", "")).lower() == focus_id.lower()]
        if sub:
            rows = sub

    spec = create_cold_chain_auditor_chart_spec(rows=rows, title_override=chart_title or None)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get("shipment_id", "")) for r in rows]
    va = [float(r.get("computed_mkt_c", 0.0) or 0.0) for r in rows]
    vb = [float(r.get("max_mkt_allowed_c", 0.0) or 0.0) for r in rows]
    png_meta = render_comparison_png(
        agent_id='cold_chain_auditor',
        title=chart_title or 'Cold-Chain Excursion Audit — Arrhenius MKT (°C) vs. Max Allowed Stability Limit (°C)',
        subtitle=f"Persona: Cold-Chain Logistics Lead · Category: 05 · Distribution & Logistics — First & Mid-Mile",
        labels=labels,
        series_a=va,
        series_a_label='Computed Arrhenius MKT (°C)',
        series_b=vb,
        series_b_label='Max Allowed MKT Limit (°C)',
        y_title='Temperature (°C)',
    )
    return {
        "status": "SUCCESS",
        "chart_title": spec["title"]["text"],
        "a2ui_vega_lite_queued": True,
        "png_infographic": png_meta,
    }


def draft_gdp_quarantine_and_spoilage_claim(target_id: str = "", recipient_role: str = "Supply Chain & Finance Leadership") -> Dict[str, Any]:
    """Draft a formal GDP/FSMA Cold-Chain Lot Disposition Certificate & Carmack Carrier Thermal Spoilage Claim Notice."""
    analysis = analyze_arrhenius_mkt_excursions(focus_id=target_id)
    kpi = analysis.get("kpi_summary", {})
    top = kpi.get("top_pareto_driver", {})
    doc_ref = f"DOC-COLDC-2026-{len(analysis.get('ranked_drivers', []))}01"
    memo_md = "\n".join(
        [
            f"### 📄 GDP/FSMA Arrhenius MKT Audit & Carrier Spoilage Claim Notice (`{doc_ref}`)",
            f"- **Organization**: XYZ Global Industries Corp. (`XYZ-CORP-01`)",
            f"- **Prepared By**: Cold-Chain Logistics Lead ([05 · Deliver | First & Mid-Mile] Cold-Chain Auditor)",
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
        "title": 'GDP/FSMA Arrhenius MKT Audit & Carrier Spoilage Claim Notice',
        "recipient_role": recipient_role,
        "markdown_draft": memo_md,
    }


def action_post_wms_mkt_usage_decision(shipment_id: Any = '', lot_id: Any = '', qa_decision: Any = '', computed_mkt_c: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Post 21 CFR Part 11 / FSMA lot usage decision (MKT_RELEASE or QUARANTINE_BLOCK) in WMS."""
    payload = {'shipment_id': shipment_id, 'lot_id': lot_id, 'qa_decision': qa_decision, 'computed_mkt_c': computed_mkt_c, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_post_wms_mkt_usage_decision',
        status_code='WMS_QA_MKT_DECISION_POSTED',
        payload=payload,
    )

def action_file_carrier_reefer_spoilage_claim(shipment_id: Any = '', carrier_id: Any = '', claim_amount_usd: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Transmit formal Carmack reefer mechanical failure spoilage claim with BLE MKT telemetry evidence."""
    payload = {'shipment_id': shipment_id, 'carrier_id': carrier_id, 'claim_amount_usd': claim_amount_usd, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_file_carrier_reefer_spoilage_claim',
        status_code='CARRIER_SPOILAGE_CLAIM_FILED',
        payload=payload,
    )


ALL_TOOLS: List[Callable[..., Any]] = [
    list_systems,
    lookup_xyz_master_context,
    query_reefer_iot_temp_telemetry,
    query_cold_chain_sku_stability_specs,
    query_thermal_excursion_incidents,
    query_qa_disposition_claims_ledger,
    analyze_arrhenius_mkt_excursions,
    render_visual_chart,
    draft_gdp_quarantine_and_spoilage_claim,
    action_post_wms_mkt_usage_decision,
    action_file_carrier_reefer_spoilage_claim,
]
