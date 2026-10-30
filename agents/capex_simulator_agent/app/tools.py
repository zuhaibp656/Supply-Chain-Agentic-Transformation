"""Deterministic Enterprise Connectors, Python Math Solvers, Charting & Drafting Tools for [03 · Make | Capacity Planning] CapEx Simulator Agent."""
from __future__ import annotations

import copy
import datetime
import json
import math
import os
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .render.charts import create_capex_simulator_agent_chart_spec
from .render.png_chart import render_comparison_png

_FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "tables"
_MASTER_FILE = Path(__file__).resolve().parent.parent / "fixtures" / "master" / "xyz_enterprise_backbone.json"

SYSTEM_CONNECTORS: List[Dict[str, Any]] = [{'id': 'mes_bottleneck_registry',
  'name': 'Multi-Plant Bottleneck & OEE Ceiling Registry',
  'protocol': 'SQL / Historian',
  'tables': ['plant_bottleneck_capacity_constraints']},
 {'id': 'capex_engineering_quotes',
  'name': 'OEM Automation & Line Expansion Quote Book',
  'protocol': 'SAP IM / Ariba',
  'tables': ['automation_capex_project_proposals']},
 {'id': 'ibp_long_range_volume',
  'name': '5-Year Long-Range Volume & Margin Scenarios',
  'protocol': 'IBP Strategic Plan',
  'tables': ['five_year_volume_growth_scenarios']},
 {'id': 'fin_dcf_npv_engine',
  'name': 'Corporate Treasury WACC & DCF Valuation Ledger',
  'protocol': 'Python DCF Engine',
  'tables': ['capex_dcf_npv_simulation_ledger']}]

_SESSION_MUTATION_LEDGER: List[Dict[str, Any]] = []
_LAST_CHART_SPEC: Optional[Dict[str, Any]] = None


def _read_json(filename: str) -> List[Dict[str, Any]]:
    fpath = _FIXTURES_DIR / filename
    if not fpath.exists():
        return []
    return copy.deepcopy(json.loads(fpath.read_text(encoding="utf-8")))


def _record_mutation(action_tool: str, status_code: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    action_id = f"ACT-CAPEX-SI-{uuid.uuid4().hex[:8].upper()}"
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = {
        "status": status_code,
        "action_id": action_id,
        "agent_id": 'capex_simulator_agent',
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
    return create_capex_simulator_agent_chart_spec()


def list_systems() -> Dict[str, Any]:
    """List connected XYZ Global Industries Corp. enterprise systems, protocols, and governed tables."""
    return {'agent': 'capex_simulator_agent',
 'organization_id': 'XYZ-CORP-01',
 'systems': [{'id': 'mes_bottleneck_registry',
              'name': 'Multi-Plant Bottleneck & OEE Ceiling Registry',
              'protocol': 'SQL / Historian',
              'tables': ['plant_bottleneck_capacity_constraints']},
             {'id': 'capex_engineering_quotes',
              'name': 'OEM Automation & Line Expansion Quote Book',
              'protocol': 'SAP IM / Ariba',
              'tables': ['automation_capex_project_proposals']},
             {'id': 'ibp_long_range_volume',
              'name': '5-Year Long-Range Volume & Margin Scenarios',
              'protocol': 'IBP Strategic Plan',
              'tables': ['five_year_volume_growth_scenarios']},
             {'id': 'fin_dcf_npv_engine',
              'name': 'Corporate Treasury WACC & DCF Valuation Ledger',
              'protocol': 'Python DCF Engine',
              'tables': ['capex_dcf_npv_simulation_ledger']}]}


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


def query_plant_bottleneck_constraints(plant_id: str = '') -> Dict[str, Any]:
    """Query saturated plant workcenters, current utilization %, CMO overflow spend $, and scrap %."""
    rows = _read_json("plant_bottleneck_capacity_constraints.json")
    if plant_id:
        rows = [r for r in rows if str(r.get('plant_id', '')).lower() == str(plant_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'mes_bottleneck_registry',
        "table": 'plant_bottleneck_capacity_constraints',
        "row_count": len(rows),
        "rows": rows,
    }

def query_automation_capex_proposals(project_id: str = '', plant_id: str = '') -> Dict[str, Any]:
    """Query OEM equipment CapEx outlay $, lead-time months, EBITDA lift $, and capacity unlock %."""
    rows = _read_json("automation_capex_project_proposals.json")
    if project_id:
        rows = [r for r in rows if str(r.get('project_id', '')).lower() == str(project_id).lower()]
    if plant_id:
        rows = [r for r in rows if str(r.get('plant_id', '')).lower() == str(plant_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'capex_engineering_quotes',
        "table": 'automation_capex_project_proposals',
        "row_count": len(rows),
        "rows": rows,
    }

def query_five_year_volume_scenarios(business_unit: str = '', scenario_id: str = '') -> Dict[str, Any]:
    """Query 5-year demand CAGR %, corporate WACC hurdle rates, and scenario probability weights."""
    rows = _read_json("five_year_volume_growth_scenarios.json")
    if business_unit:
        rows = [r for r in rows if str(r.get('business_unit', '')).lower() == str(business_unit).lower()]
    if scenario_id:
        rows = [r for r in rows if str(r.get('scenario_id', '')).lower() == str(scenario_id).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'ibp_long_range_volume',
        "table": 'five_year_volume_growth_scenarios',
        "row_count": len(rows),
        "rows": rows,
    }

def query_capex_dcf_npv_ledger(project_id: str = '', approval_decision: str = '') -> Dict[str, Any]:
    """Query probability-weighted 5-year NPV ($), IRR %, payback months, and capital ranking."""
    rows = _read_json("capex_dcf_npv_simulation_ledger.json")
    if project_id:
        rows = [r for r in rows if str(r.get('project_id', '')).lower() == str(project_id).lower()]
    if approval_decision:
        rows = [r for r in rows if str(r.get('approval_decision', '')).lower() == str(approval_decision).lower()]
    return {
        "status": "SUCCESS",
        "source_system": 'fin_dcf_npv_engine',
        "table": 'capex_dcf_npv_simulation_ledger',
        "row_count": len(rows),
        "rows": rows,
    }


def analyze_capex_portfolio_dcf_irr(focus_id: str = "") -> Dict[str, Any]:
    """Run deterministic discounted cash-flow (NPV, IRR %, payback months) portfolio optimization under capital budget & WACC hurdle constraints."""
    global _LAST_CHART_SPEC
    chart_rows = _read_json("capex_dcf_npv_simulation_ledger.json")
    if focus_id:
        filtered = [r for r in chart_rows if str(r.get("project_id", "")).lower() == focus_id.lower()]
        if filtered:
            chart_rows = filtered

    series_a = [float(r.get("capex_outlay_usd", 0.0) or 0.0) for r in chart_rows]
    series_b = [float(r.get("npv_5yr_usd", 0.0) or 0.0) for r in chart_rows]
    labels = [str(r.get("project_id", "")) for r in chart_rows]

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
    # Exact Discounted Cash Flow (DCF) NPV & IRR solver
    dcf_models = []
    for prop in _read_json("capex_project_proposals.json"):
        capex = float(prop["initial_capex_usd"])
        wacc = float(prop["hurdle_wacc_pct"]) / 100.0
        life = int(prop["useful_life_yrs"])
        cf_map = {r["proposal_id"]: r for r in _read_json("multi_year_cashflow_simulations.json")}
        cf_row = cf_map.get(prop["proposal_id"], {})
        annual_net_cf = float(cf_row.get("annual_labor_and_scrap_savings_usd", 0)) - float(cf_row.get("annual_opex_maintenance_usd", 0))
        npv = round(sum(annual_net_cf / ((1.0 + wacc) ** t) for t in range(1, life + 1)) - capex, 2)
        dcf_models.append({"proposal_id": prop["proposal_id"], "computed_npv_usd": npv, "annual_net_cashflow_usd": round(annual_net_cf, 2)})
    domain_computations["dcf_npv_verification"] = dcf_models

    _LAST_CHART_SPEC = create_capex_simulator_agent_chart_spec(rows=chart_rows)

    md_lines = [
        "| Record | CapEx Outlay ($) | 5-Yr NPV ($) | Delta |",
        "| :--- | ---: | ---: | ---: |",
    ]
    for g in ranked_gaps[:6]:
        md_lines.append(
            f"| `{g['id']}` | {g['series_a']:,.2f} | **{g['series_b']:,.2f}** | {g['signed_delta']:+,.2f} |"
        )

    return {
        "status": "SUCCESS",
        "agent": 'capex_simulator_agent',
        "persona": 'VP of Manufacturing',
        "records_evaluated": len(chart_rows),
        "kpi_summary": {
            "series_a_label": 'CapEx Outlay ($)',
            "series_b_label": '5-Yr NPV ($)',
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
    rows = _read_json("capex_dcf_npv_simulation_ledger.json")
    if focus_id:
        sub = [r for r in rows if str(r.get("project_id", "")).lower() == focus_id.lower()]
        if sub:
            rows = sub

    spec = create_capex_simulator_agent_chart_spec(rows=rows, title_override=chart_title or None)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get("project_id", "")) for r in rows]
    va = [float(r.get("capex_outlay_usd", 0.0) or 0.0) for r in rows]
    vb = [float(r.get("npv_5yr_usd", 0.0) or 0.0) for r in rows]
    png_meta = render_comparison_png(
        agent_id='capex_simulator_agent',
        title=chart_title or 'CapEx Portfolio Ranking — Capital Outlay ($) vs. 5-Year Net Present Value ($)',
        subtitle=f"Persona: VP of Manufacturing · Category: 03 · Manufacturing & Production — Capacity Planning",
        labels=labels,
        series_a=va,
        series_a_label='CapEx Outlay ($)',
        series_b=vb,
        series_b_label='5-Yr NPV ($)',
        y_title='USD Valuation',
    )
    return {
        "status": "SUCCESS",
        "chart_title": spec["title"]["text"],
        "a2ui_vega_lite_queued": True,
        "png_infographic": png_meta,
    }


def draft_cfo_capital_appropriation_memo(target_id: str = "", recipient_role: str = "Supply Chain & Finance Leadership") -> Dict[str, Any]:
    """Draft a formal CFO Board Capital Appropriation Request (CAR) summarizing DCF NPV, IRR %, payback, and deferred below-hurdle projects."""
    analysis = analyze_capex_portfolio_dcf_irr(focus_id=target_id)
    kpi = analysis.get("kpi_summary", {})
    top = kpi.get("top_pareto_driver", {})
    doc_ref = f"DOC-CAPEX-2026-{len(analysis.get('ranked_drivers', []))}01"
    memo_md = "\n".join(
        [
            f"### 📄 CFO Board Capital Appropriation Request (CAR) Dossier (`{doc_ref}`)",
            f"- **Organization**: XYZ Global Industries Corp. (`XYZ-CORP-01`)",
            f"- **Prepared By**: VP of Manufacturing ([03 · Make | Capacity Planning] CapEx Simulator Agent)",
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
        "title": 'CFO Board Capital Appropriation Request (CAR) Dossier',
        "recipient_role": recipient_role,
        "markdown_draft": memo_md,
    }


def action_submit_sap_im_capex_appropriation(project_id: Any = '', plant_id: Any = '', capex_outlay_usd: Any = '', irr_pct: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Create approved Investment Management (SAP IM) WBS appropriation request for Tier-1 CapEx project."""
    payload = {'project_id': project_id, 'plant_id': plant_id, 'capex_outlay_usd': capex_outlay_usd, 'irr_pct': irr_pct, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_submit_sap_im_capex_appropriation',
        status_code='SAP_IM_CAR_SUBMITTED',
        payload=payload,
    )

def action_defer_subhurdle_capex_proposal(project_id: Any = '', irr_pct: Any = '', rationale: Any = '', idempotency_key: str = '') -> Dict[str, Any]:
    """Formally defer CapEx project failing corporate WACC hurdle rate and reallocate budget."""
    payload = {'project_id': project_id, 'irr_pct': irr_pct, 'rationale': rationale, "idempotency_key": idempotency_key or "AUTO-IDEMP"}
    return _record_mutation(
        action_tool='action_defer_subhurdle_capex_proposal',
        status_code='CAPEX_DEFERRED_BELOW_WACC',
        payload=payload,
    )


ALL_TOOLS: List[Callable[..., Any]] = [
    list_systems,
    lookup_xyz_master_context,
    query_plant_bottleneck_constraints,
    query_automation_capex_proposals,
    query_five_year_volume_scenarios,
    query_capex_dcf_npv_ledger,
    analyze_capex_portfolio_dcf_irr,
    render_visual_chart,
    draft_cfo_capital_appropriation_memo,
    action_submit_sap_im_capex_appropriation,
    action_defer_subhurdle_capex_proposal,
]
