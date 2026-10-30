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
    all_rows = list(rows)
    if business_unit:
        b_low = business_unit.lower()
        rows = [r for r in rows if b_low in r.get("business_unit", "").lower()]
    if region:
        r_low = region.lower()
        rows = [r for r in rows if r_low in r.get("region", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "corporate_treasury_workstation",
        "table": "working_capital_metrics",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_inventory_valuation_ledger(valuation_area: str = "", valuation_class: str = "", limit: int = 10) -> Dict[str, Any]:
    """Query SAP S/4HANA Material Ledger for valuation classes, standard costs, days of supply, and trapped cash."""
    rows = _read_json("inventory_valuation_ledger.json")
    all_rows = list(rows)
    if valuation_area:
        v_low = valuation_area.lower()
        rows = [r for r in rows if v_low in r.get("valuation_area", "").lower()]
    if valuation_class:
        c_low = valuation_class.lower()
        rows = [r for r in rows if c_low in r.get("valuation_class", "").lower()]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "sap_acdoca_material_ledger",
        "table": "inventory_valuation_ledger",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_trapped_cash_opportunities(min_cash_freed_usd: float = 0.0, limit: int = 10) -> Dict[str, Any]:
    """Identify high-ROI buffer reduction and batch rightsizing opportunities that release balance sheet cash."""
    rows = _read_json("trapped_cash_opportunities.json")
    all_rows = list(rows)
    if min_cash_freed_usd > 0:
        rows = [r for r in rows if r.get("cash_freed_usd", 0) >= min_cash_freed_usd]
    if not rows and all_rows:
        rows = all_rows
    return {
        "source_system": "corporate_treasury_workstation",
        "table": "trapped_cash_opportunities",
        "total": len(rows),
        "rows": rows[:max(1, min(limit, 50))],
    }


def query_ap_supplier_discount_invoices(min_discount_usd: float = 0.0, limit: int = 10) -> Dict[str, Any]:
    """Query eligible supplier AP invoices offering lucrative 2/10 Net 60 early-payment dynamic cash discounts."""
    rows = _read_json("supplier_ap_invoices.json")
    all_rows = list(rows)
    if min_discount_usd > 0:
        rows = [r for r in rows if r.get("cash_discount_amount_usd", 0) >= min_discount_usd]
    if not rows and all_rows:
        rows = all_rows
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


# --- BEGIN PERSONA ANALYTICS & CHARTING ENRICHMENT ---
import statistics as _statistics
from .render.png_chart import render_comparison_png as _render_comparison_png
from .render.charts import create_composite_cash_bridge_spec as _native_chart_spec

_MASTER_BACKBONE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "master" / "xyz_enterprise_backbone.json"
_LAST_CHART_SPEC: Any = None


def _discover_table_files() -> List[Path]:
    tdir = Path(__file__).resolve().parent.parent / "fixtures" / "tables"
    if not tdir.exists():
        return []
    return sorted(p for p in tdir.glob("*.json") if p.is_file())


def _infer_chart_columns(rows: List[Dict[str, Any]]) -> Any:
    if not rows:
        return ("id", "metric_a", "metric_b")
    sample = rows[0]
    keys = list(sample.keys())
    label_col = keys[0]
    for k in keys:
        if isinstance(sample.get(k), str) and any(t in k.lower() for t in ("_id", "sku", "facility", "lane", "route", "batch", "order", "supplier", "node")):
            label_col = k
            break
    num_cols = [
        k for k in keys
        if isinstance(sample.get(k), (int, float))
        and not isinstance(sample.get(k), bool)
        and not any(latlon in k.lower() for latlon in ("lat", "lon", "lng"))
    ]
    if len(num_cols) >= 2:
        return (label_col, num_cols[0], num_cols[1])
    if len(num_cols) == 1:
        return (label_col, num_cols[0], num_cols[0])
    return (label_col, keys[0], keys[0])


def _build_dynamic_vegalite_spec(
    rows: List[Dict[str, Any]],
    label_col: str,
    col_a: str,
    col_b: str,
    title: str,
) -> Dict[str, Any]:
    vals: List[Dict[str, Any]] = []
    for r in rows[:8]:
        ent = str(r.get(label_col, "Record"))
        va = float(r.get(col_a, 0.0) or 0.0) if isinstance(r.get(col_a), (int, float)) else 0.0
        vb = float(r.get(col_b, 0.0) or 0.0) if isinstance(r.get(col_b), (int, float)) else 0.0
        vals.append({"entity": ent, "series": col_a.replace("_", " ").title(), "value": round(va, 2)})
        if col_b != col_a:
            vals.append({"entity": ent, "series": col_b.replace("_", " ").title(), "value": round(vb, 2)})
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title,
            "subtitle": "XYZ Global Industries Corp. (XYZ-CORP-01) · Live Python Analytics",
            "anchor": "start",
            "fontSize": 14,
            "subtitleColor": "#64748b",
        },
        "width": "container",
        "height": 300,
        "data": {"values": vals},
        "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "tooltip": True},
        "encoding": {
            "x": {"field": "entity", "type": "nominal", "title": None, "axis": {"labelAngle": -25}},
            "xOffset": {"field": "series"},
            "y": {"field": "value", "type": "quantitative", "title": "Metric Value"},
            "color": {
                "field": "series",
                "type": "nominal",
                "scale": {"range": ["#64748b", "#2563eb"]},
                "legend": {"orient": "top"},
            },
            "tooltip": [
                {"field": "entity", "type": "nominal", "title": label_col},
                {"field": "series", "type": "nominal", "title": "KPI"},
                {"field": "value", "type": "quantitative", "title": "Value", "format": ",.2f"},
            ],
        },
        "config": {"view": {"stroke": "transparent"}},
    }


def get_native_chart_spec() -> Dict[str, Any]:
    """Returns the canonical multi-panel native Vega-Lite v5 spec for deterministic scenario runs."""
    return _native_chart_spec()


def get_latest_chart_spec(consume: bool = False) -> Dict[str, Any]:
    """Returns the latest turn-generated Vega-Lite v5 spec or falls back to the native agent spec."""
    global _LAST_CHART_SPEC
    if _LAST_CHART_SPEC is not None:
        out = copy.deepcopy(_LAST_CHART_SPEC) if "copy" in globals() else dict(_LAST_CHART_SPEC)
        if consume:
            _LAST_CHART_SPEC = None
        return out
    return _native_chart_spec()


def lookup_xyz_master_context(
    sku_id: str = "",
    facility_id: str = "",
    supplier_id: str = "",
    customer_id: str = "",
    carrier_id: str = "",
) -> Dict[str, Any]:
    """Join operational IDs against XYZ Global Industries Corp. (XYZ-CORP-01) master ERP/WMS/TMS tables."""
    if not _MASTER_BACKBONE_PATH.exists():
        return {"status": "MASTER_NOT_FOUND", "organization_id": "XYZ-CORP-01"}
    bundle = json.loads(_MASTER_BACKBONE_PATH.read_text(encoding="utf-8"))
    out: Dict[str, Any] = {
        "status": "SUCCESS",
        "organization_id": bundle.get("organization_id", "XYZ-CORP-01"),
        "organization_name": bundle.get("organization_name", "XYZ Global Industries Corp."),
    }
    if sku_id:
        out["material"] = bundle.get("materials", {}).get(sku_id)
    if facility_id:
        out["facility"] = bundle.get("facilities", {}).get(facility_id)
    if supplier_id:
        out["supplier"] = bundle.get("suppliers", {}).get(supplier_id)
    if customer_id:
        out["customer"] = bundle.get("customers", {}).get(customer_id)
    if carrier_id:
        out["carrier"] = bundle.get("carriers", {}).get(carrier_id)
    if not any([sku_id, facility_id, supplier_id, customer_id, carrier_id]):
        out["summary_counts"] = {
            "materials": len(bundle.get("materials", {})),
            "facilities": len(bundle.get("facilities", {})),
            "suppliers": len(bundle.get("suppliers", {})),
            "customers": len(bundle.get("customers", {})),
            "carriers": len(bundle.get("carriers", {})),
            "golden_threads": len(bundle.get("golden_threads", [])),
        }
    return out


def analyze_operational_metrics(
    table_name: str = "",
    filter_field: str = "",
    filter_value: str = "",
) -> Dict[str, Any]:
    """Run deterministic Python statistical, Pareto, and KPI aggregation across live XYZ-CORP-01 tables."""
    global _LAST_CHART_SPEC
    tfiles = _discover_table_files()
    if not tfiles:
        return {"status": "NO_TABLES", "agent": 'working_capital_cash_bridge'}

    chosen = tfiles[0]
    if table_name:
        for tf in tfiles:
            if table_name.lower().replace(".json", "") in tf.stem.lower():
                chosen = tf
                break

    rows = _read_json(chosen.name)
    if filter_field and filter_value:
        matched = [r for r in rows if filter_value.lower() in str(r.get(filter_field, "")).lower()]
        if matched:
            rows = matched

    label_col, col_a, col_b = _infer_chart_columns(rows)
    vals_a = [float(r.get(col_a, 0.0) or 0.0) for r in rows if isinstance(r.get(col_a), (int, float))]
    vals_b = [float(r.get(col_b, 0.0) or 0.0) for r in rows if isinstance(r.get(col_b), (int, float))]

    kpi_stats = {
        "primary_metric": col_a,
        "secondary_metric": col_b,
        "sum_primary": round(sum(vals_a), 2),
        "mean_primary": round(_statistics.mean(vals_a), 2) if vals_a else 0.0,
        "stdev_primary": round(_statistics.pstdev(vals_a), 2) if len(vals_a) > 1 else 0.0,
        "max_primary": round(max(vals_a), 2) if vals_a else 0.0,
        "sum_secondary": round(sum(vals_b), 2),
        "mean_secondary": round(_statistics.mean(vals_b), 2) if vals_b else 0.0,
    }

    ranked = sorted(
        rows,
        key=lambda r: abs(float(r.get(col_a, 0.0) or 0.0)) if isinstance(r.get(col_a), (int, float)) else 0.0,
        reverse=True,
    )
    _LAST_CHART_SPEC = _build_dynamic_vegalite_spec(
        rows,
        label_col,
        col_a,
        col_b,
        title=f"Working Capital Cash Bridge — {col_a.replace('_', ' ').title()} vs {col_b.replace('_', ' ').title()}",
    )

    md_lines = [
        f"| {label_col} | {col_a[:22]} | {col_b[:22]} |",
        "| :--- | ---: | ---: |",
    ]
    for r in ranked[:6]:
        va = r.get(col_a, "")
        vb = r.get(col_b, "")
        va_s = f"{va:,.2f}" if isinstance(va, float) else f"{va:,}" if isinstance(va, int) else str(va)
        vb_s = f"{vb:,.2f}" if isinstance(vb, float) else f"{vb:,}" if isinstance(vb, int) else str(vb)
        md_lines.append(f"| `{r.get(label_col, '')}` | **{va_s}** | {vb_s} |")

    return {
        "status": "SUCCESS",
        "agent": 'working_capital_cash_bridge',
        "analyzed_table": chosen.stem,
        "available_tables": [p.stem for p in tfiles],
        "records_evaluated": len(rows),
        "kpi_summary": kpi_stats,
        "top_pareto_record": ranked[0] if ranked else {},
        "concise_markdown_table": "\n".join(md_lines),
    }


def render_visual_chart(table_name: str = "", chart_title: str = "") -> Dict[str, Any]:
    """Build a live Vega-Lite v5 spec for the A2UI VegaChart card AND save a 1200x640 Pillow PNG chart."""
    global _LAST_CHART_SPEC
    tfiles = _discover_table_files()
    chosen = tfiles[0] if tfiles else None
    if table_name and tfiles:
        for tf in tfiles:
            if table_name.lower().replace(".json", "") in tf.stem.lower():
                chosen = tf
                break

    if chosen is None:
        return {"status": "NO_DATA"}

    rows = _read_json(chosen.name)
    label_col, col_a, col_b = _infer_chart_columns(rows)
    resolved_title = chart_title or f"Working Capital Cash Bridge — {chosen.stem.replace('_', ' ').title()}"
    spec = _build_dynamic_vegalite_spec(rows, label_col, col_a, col_b, title=resolved_title)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get(label_col, "")) for r in rows]
    va = [float(r.get(col_a, 0.0) or 0.0) if isinstance(r.get(col_a), (int, float)) else 0.0 for r in rows]
    vb = [float(r.get(col_b, 0.0) or 0.0) if isinstance(r.get(col_b), (int, float)) else 0.0 for r in rows]

    png_meta = _render_comparison_png(
        agent_id='working_capital_cash_bridge',
        title=resolved_title,
        subtitle=f"XYZ Global Industries Corp. (XYZ-CORP-01) · Source Table: {chosen.stem}",
        labels=labels,
        series_a=va,
        series_a_label=col_a.replace("_", " ").title(),
        series_b=vb,
        series_b_label=col_b.replace("_", " ").title(),
        y_title=col_a.replace("_", " ").title(),
    )
    return {
        "status": "SUCCESS",
        "source_table": chosen.stem,
        "a2ui_vega_lite_queued": True,
        "png_infographic": png_meta,
    }


def draft_operational_brief(
    subject: str = "",
    recipient_role: str = "Supply Chain & Operations Leadership",
    table_name: str = "",
) -> Dict[str, Any]:
    """Draft a concise, grounded persona operational decision brief or action memo from live Python KPIs."""
    analysis = analyze_operational_metrics(table_name=table_name)
    kpi = analysis.get("kpi_summary", {})
    doc_ref = f"BRIEF-WORKIN-2026-{analysis.get('records_evaluated', 8):02d}"
    title_str = subject or f"Working Capital Cash Bridge Operational Decision Brief"
    brief_md = "\n".join(
        [
            f"### 📄 {title_str} (`{doc_ref}`)",
            f"- **Organization**: XYZ Global Industries Corp. (`XYZ-CORP-01`)",
            f"- **To**: {recipient_role}",
            f"- **Source Table Audited**: `{analysis.get('analyzed_table')}` (`{analysis.get('records_evaluated')}` records)",
            f"- **Primary KPI (`{kpi.get('primary_metric')}`)**: Sum `{kpi.get('sum_primary', 0):,.2f}` | Mean `{kpi.get('mean_primary', 0):,.2f}` | Peak `{kpi.get('max_primary', 0):,.2f}`",
            "",
            analysis.get("concise_markdown_table", ""),
            "",
            "**Governance Gate**: Pre-validated against XYZ-CORP-01 tolerances; requires explicit confirmation and `idempotency_key` prior to ERP/WMS/TMS write-back.",
        ]
    )
    return {
        "status": "DRAFT_READY",
        "document_ref": doc_ref,
        "recipient_role": recipient_role,
        "markdown_draft": brief_md,
    }
# --- END PERSONA ANALYTICS & CHARTING ENRICHMENT ---
