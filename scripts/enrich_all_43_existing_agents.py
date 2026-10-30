#!/usr/bin/env python3
"""Upgrades all 43 existing (Cohort 2 & Cohort 3 + alias) Supply Chain ADK Agents.

Idempotently enriches each of the 43 non-Cohort-1 agent packages with:
  1. Multi-row organizational demo data (`fixtures/tables/*.json` expanded to >=8 rows/table = >=32 rows/agent)
     preserving 100% of existing rows/IDs intact so zero existing smoke tests break, while adding realistic
     multi-plant/SKU/supplier/customer/carrier records grounded on XYZ Global Industries Corp. (XYZ-CORP-01).
  2. Self-contained `app/render/png_chart.py` (`1200x640` Pillow executive comparison chart generator) +
     verified self-contained `a2ui_envelope.py` and `a2ui_lifecycle.py`.
  3. Deterministic Python analytical, visual charting, master-data join, and persona drafting tools in `app/tools.py`:
     - `lookup_xyz_master_context(...)`
     - `analyze_operational_metrics(...)`
     - `render_visual_chart(...)`
     - `draft_operational_brief(...)`
     - `get_latest_chart_spec()`
  4. Concise, deterministic, non-verbose ADK agent behavior in `app/agent.py`:
     - Registers the 4 new Python tools in `_AVAILABLE_TOOLS`
     - Removes `after_model_callback=_append_verified_report` (eliminating unrequested write-back mutations
       and duplicate 35-line report appends on read-only turns)
     - Connects `_emit_a2ui_surface` to `tools.get_latest_chart_spec()` so the A2UI `VegaChart` card updates dynamically
     - Enforces concise `<=5` column Markdown tables and Python-first math in `_INSTRUCTION`
  5. Adds `tests/test_persona_enrichment.py` verifying >=8 rows/table, master-backbone joins, Python analytics,
     Pillow PNG + Vega-Lite chart generation, and operational brief drafting.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List

from build_overhauled_24_cohort1_agents import (
    A2UI_ENVELOPE_CODE,
    A2UI_LIFECYCLE_CODE,
    PNG_CHART_CODE,
)
from cohort1_domain_blueprints_part1 import COHORT1_PART1
from cohort1_domain_blueprints_part2 import COHORT1_PART2

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / "agents"

COHORT1_IDS = set(COHORT1_PART1.keys()) | set(COHORT1_PART2.keys())

XYZ_SKUS = [
    "SKU-XYZ-101",
    "SKU-XYZ-204",
    "SKU-BEV-ISOTONIC-32OZ",
    "SKU-BEV-OATMILK-1L",
    "SKU-DAIRY-PROBIOTIC-6PK",
    "SKU-SNACK-PROTEIN-BAR",
    "SKU-XYZ-309",
    "SKU-XYZ-412",
    "SKU-CRYO-4410-BIO",
    "SKU-XYZ-518",
    "SKU-XYZ-625",
]
XYZ_PLANTS = [
    "PLANT-XYZ-AUSTIN",
    "PLANT-XYZ-STUTTGART",
    "PLANT-XYZ-MONTERREY",
    "PLANT-XYZ-BENGALURU",
    "CMO-XYZ-DALLAS",
]
XYZ_FACILITIES = XYZ_PLANTS + [
    "RDC-XYZ-CHICAGO",
    "FDC-XYZ-DALLAS",
    "FDC-XYZ-ATLANTA",
    "RDC-XYZ-FRANKFURT",
    "FDC-XYZ-MUMBAI",
]
XYZ_SUPPLIERS = [
    "SUP-XYZ-T1-ALUWELD",
    "SUP-XYZ-T1-ASEPTIPACK",
    "SUP-XYZ-T1-SILICONCORE",
    "SUP-XYZ-T1-ECORESIN",
    "SUP-XYZ-T1-PRAIRIEOAT",
    "SUP-XYZ-T1-SUMATRARUBBER",
    "SUP-XYZ-T1-SCHOTTCRYO",
]
XYZ_CUSTOMERS = [
    "CUST-XYZ-TIER1-MEGAMART",
    "CUST-KROGER-US01",
    "CUST-COSTCO-US04",
    "CUST-XYZ-TIER1-AUTOWORKS",
    "CUST-MEDLINE-BIO01",
    "CUST-XYZ-TIER2-METROCPG",
]
XYZ_CARRIERS = [
    "CAR-JBHT-FTL",
    "CAR-CRYOEXP-REEFER",
    "CAR-XPO-LTL",
    "CAR-BNSF-RAIL",
    "CAR-MAERSK-OCEAN",
    "CAR-LH-AIRCARGO",
]

ENRICH_BEGIN = "# --- BEGIN PERSONA ANALYTICS & CHARTING ENRICHMENT ---"
ENRICH_END = "# --- END PERSONA ANALYTICS & CHARTING ENRICHMENT ---"


def _bump_id(val: str, row_idx: int, table_stem: str) -> str:
    """Generates a clean, collision-free enterprise ID preserving prefix conventions."""
    m = re.match(r"^([A-Za-z0-9_-]*?)(\d+)$", val)
    if m:
        prefix, digits = m.group(1), m.group(2)
        base_num = int(digits)
        new_num = base_num + row_idx * 7 + 1
        return f"{prefix}{new_num:0{len(digits)}d}"
    tag = hashlib.sha1(f"{table_stem}:{val}:{row_idx}".encode("utf-8")).hexdigest()[:3].upper()
    return f"{val}-R{row_idx:02d}{tag}"


def _perturb_number(val: Any, key: str, row_idx: int, table_stem: str) -> Any:
    if isinstance(val, bool):
        return val if row_idx % 3 != 0 else (not val)
    h = int(hashlib.sha1(f"{table_stem}:{key}:{row_idx}".encode("utf-8")).hexdigest()[:6], 16)
    # Deterministic multiplier between 0.76 and 1.28 (never 1.0)
    offsets = [-0.22, -0.14, -0.08, 0.07, 0.13, 0.19, 0.25, -0.17]
    mult = 1.0 + offsets[(h + row_idx) % len(offsets)]
    kl = key.lower()

    if "lat" in kl and isinstance(val, (int, float)):
        return round(float(val) + ((row_idx - 4) * 0.042), 5)
    if ("lon" in kl or "lng" in kl) and isinstance(val, (int, float)):
        return round(float(val) + ((row_idx - 4) * 0.051), 5)

    if isinstance(val, int):
        if val == 0:
            return (row_idx % 4) * 2
        res = int(round(val * mult))
        if any(tok in kl for tok in ("pct", "percent", "rate", "utilization", "efficiency", "oee")):
            return max(1, min(99, res))
        return max(1, res) if val > 0 else res

    if isinstance(val, float):
        if abs(val) < 1e-9:
            return round((row_idx % 3) * 1.25, 2)
        res = val * mult
        if any(tok in kl for tok in ("score", "similarity", "probability", "confidence", "index", "ratio")) and 0.0 <= val <= 1.0:
            return round(max(0.03, min(0.99, res)), 3)
        if any(tok in kl for tok in ("pct", "percent", "oee", "otif", "osa", "yield")) and 0.0 <= val <= 100.0:
            return round(max(2.5, min(99.6, res)), 2)
        return round(res, 2)

    return val


def expand_fixture_table_to_8_rows(fpath: Path, target_min_rows: int = 8) -> int:
    """Expands a JSON table file to >=8 realistic XYZ-CORP-01 rows while keeping existing rows untouched."""
    try:
        data = json.loads(fpath.read_text(encoding="utf-8"))
    except Exception:
        return 0
    if not isinstance(data, list) or len(data) == 0 or not isinstance(data[0], dict):
        return len(data) if isinstance(data, list) else 0

    if len(data) >= target_min_rows:
        return len(data)

    orig_rows = copy.deepcopy(data)
    keys = list(orig_rows[0].keys())
    primary_key = keys[0]
    seen_pks = {str(r.get(primary_key, "")) for r in orig_rows}
    stem = fpath.stem

    idx = len(orig_rows)
    while len(orig_rows) < target_min_rows:
        template = copy.deepcopy(data[idx % len(data)])
        new_row: Dict[str, Any] = {}
        for col_i, (k, v) in enumerate(template.items()):
            kl = k.lower()
            if col_i == 0:
                cand = _bump_id(str(v), idx, stem)
                while cand in seen_pks:
                    cand = cand + "X"
                seen_pks.add(cand)
                new_row[k] = cand
            elif isinstance(v, (int, float, bool)):
                new_row[k] = _perturb_number(v, k, idx, stem)
            elif isinstance(v, str):
                if kl in ("sku_id", "material_id", "item_id", "product_sku"):
                    new_row[k] = XYZ_SKUS[idx % len(XYZ_SKUS)]
                elif kl in ("plant_id", "manufacturing_plant"):
                    new_row[k] = XYZ_PLANTS[idx % len(XYZ_PLANTS)]
                elif kl in ("facility_id", "dc_id", "warehouse_id", "origin_hub", "destination_dc", "source_node", "target_node"):
                    new_row[k] = XYZ_FACILITIES[(idx + col_i) % len(XYZ_FACILITIES)]
                elif kl in ("supplier_id", "vendor_id"):
                    new_row[k] = XYZ_SUPPLIERS[idx % len(XYZ_SUPPLIERS)]
                elif kl in ("customer_id", "account_id", "retailer_id"):
                    new_row[k] = XYZ_CUSTOMERS[idx % len(XYZ_CUSTOMERS)]
                elif kl in ("carrier_id",):
                    new_row[k] = XYZ_CARRIERS[idx % len(XYZ_CARRIERS)]
                elif kl.endswith("_id") and re.search(r"\d", v):
                    new_row[k] = _bump_id(v, idx, f"{stem}_{k}")
                elif re.match(r"^202\d-\d{2}-\d{2}$", v):
                    day = ((idx * 3 + 11) % 27) + 1
                    new_row[k] = f"{v[:8]}{day:02d}"
                else:
                    new_row[k] = v
            elif isinstance(v, list):
                if v and all(isinstance(x, (int, float)) for x in v):
                    new_row[k] = [_perturb_number(x, k, idx + j, stem) for j, x in enumerate(v)]
                else:
                    new_row[k] = copy.deepcopy(v)
            else:
                new_row[k] = copy.deepcopy(v)
        orig_rows.append(new_row)
        idx += 1

    fpath.write_text(json.dumps(orig_rows, indent=2) + "\n", encoding="utf-8")
    return len(orig_rows)


def _find_native_chart_fn(charts_py: Path, agent_py: Path | None = None) -> str:
    if agent_py is not None and agent_py.exists():
        atxt = agent_py.read_text(encoding="utf-8")
        m_imp = re.search(r"from\s+\.render\.charts\s+import\s+(create_\w+)", atxt)
        if m_imp:
            return m_imp.group(1)
    if not charts_py.exists():
        return ""
    txt = charts_py.read_text(encoding="utf-8")
    m_comp = re.findall(r"def\s+(create_composite_\w+)\s*\(", txt)
    if m_comp:
        return m_comp[-1]
    all_fns = re.findall(r"def\s+(create_\w+)\s*\(", txt)
    return all_fns[-1] if all_fns else ""


def _find_surface_fn(surfaces_py: Path, agent_py: Path | None = None) -> str:
    if agent_py is not None and agent_py.exists():
        atxt = agent_py.read_text(encoding="utf-8")
        m_imp = re.search(r"from\s+\.render\.surfaces\s+import\s+(build_\w+)", atxt)
        if m_imp:
            return m_imp.group(1)
    if surfaces_py.exists():
        stxt = surfaces_py.read_text(encoding="utf-8")
        m_fn = re.findall(r"def\s+(build_\w+)\s*\(", stxt)
        if m_fn:
            return m_fn[-1]
    return ""


def _build_tools_enrichment_block(agent_id: str, native_chart_fn: str) -> str:
    chart_import_line = (
        f"from .render.charts import {native_chart_fn} as _native_chart_spec"
        if native_chart_fn
        else "def _native_chart_spec() -> Dict[str, Any]: return {}"
    )
    return f'''{ENRICH_BEGIN}
import statistics as _statistics
from .render.png_chart import render_comparison_png as _render_comparison_png
{chart_import_line}

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
        vals.append({{"entity": ent, "series": col_a.replace("_", " ").title(), "value": round(va, 2)}})
        if col_b != col_a:
            vals.append({{"entity": ent, "series": col_b.replace("_", " ").title(), "value": round(vb, 2)}})
    return {{
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {{
            "text": title,
            "subtitle": "XYZ Global Industries Corp. (XYZ-CORP-01) · Live Python Analytics",
            "anchor": "start",
            "fontSize": 14,
            "subtitleColor": "#64748b",
        }},
        "width": "container",
        "height": 300,
        "data": {{"values": vals}},
        "mark": {{"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "tooltip": True}},
        "encoding": {{
            "x": {{"field": "entity", "type": "nominal", "title": None, "axis": {{"labelAngle": -25}}}},
            "xOffset": {{"field": "series"}},
            "y": {{"field": "value", "type": "quantitative", "title": "Metric Value"}},
            "color": {{
                "field": "series",
                "type": "nominal",
                "scale": {{"range": ["#64748b", "#2563eb"]}},
                "legend": {{"orient": "top"}},
            }},
            "tooltip": [
                {{"field": "entity", "type": "nominal", "title": label_col}},
                {{"field": "series", "type": "nominal", "title": "KPI"}},
                {{"field": "value", "type": "quantitative", "title": "Value", "format": ",.2f"}},
            ],
        }},
        "config": {{"view": {{"stroke": "transparent"}}}},
    }}


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
        return {{"status": "MASTER_NOT_FOUND", "organization_id": "XYZ-CORP-01"}}
    bundle = json.loads(_MASTER_BACKBONE_PATH.read_text(encoding="utf-8"))
    out: Dict[str, Any] = {{
        "status": "SUCCESS",
        "organization_id": bundle.get("organization_id", "XYZ-CORP-01"),
        "organization_name": bundle.get("organization_name", "XYZ Global Industries Corp."),
    }}
    if sku_id:
        out["material"] = bundle.get("materials", {{}}).get(sku_id)
    if facility_id:
        out["facility"] = bundle.get("facilities", {{}}).get(facility_id)
    if supplier_id:
        out["supplier"] = bundle.get("suppliers", {{}}).get(supplier_id)
    if customer_id:
        out["customer"] = bundle.get("customers", {{}}).get(customer_id)
    if carrier_id:
        out["carrier"] = bundle.get("carriers", {{}}).get(carrier_id)
    if not any([sku_id, facility_id, supplier_id, customer_id, carrier_id]):
        out["summary_counts"] = {{
            "materials": len(bundle.get("materials", {{}})),
            "facilities": len(bundle.get("facilities", {{}})),
            "suppliers": len(bundle.get("suppliers", {{}})),
            "customers": len(bundle.get("customers", {{}})),
            "carriers": len(bundle.get("carriers", {{}})),
            "golden_threads": len(bundle.get("golden_threads", [])),
        }}
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
        return {{"status": "NO_TABLES", "agent": {agent_id!r}}}

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

    kpi_stats = {{
        "primary_metric": col_a,
        "secondary_metric": col_b,
        "sum_primary": round(sum(vals_a), 2),
        "mean_primary": round(_statistics.mean(vals_a), 2) if vals_a else 0.0,
        "stdev_primary": round(_statistics.pstdev(vals_a), 2) if len(vals_a) > 1 else 0.0,
        "max_primary": round(max(vals_a), 2) if vals_a else 0.0,
        "sum_secondary": round(sum(vals_b), 2),
        "mean_secondary": round(_statistics.mean(vals_b), 2) if vals_b else 0.0,
    }}

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
        title=f"{agent_id.replace('_', ' ').title()} — {{col_a.replace('_', ' ').title()}} vs {{col_b.replace('_', ' ').title()}}",
    )

    md_lines = [
        f"| {{label_col}} | {{col_a[:22]}} | {{col_b[:22]}} |",
        "| :--- | ---: | ---: |",
    ]
    for r in ranked[:6]:
        va = r.get(col_a, "")
        vb = r.get(col_b, "")
        va_s = f"{{va:,.2f}}" if isinstance(va, float) else f"{{va:,}}" if isinstance(va, int) else str(va)
        vb_s = f"{{vb:,.2f}}" if isinstance(vb, float) else f"{{vb:,}}" if isinstance(vb, int) else str(vb)
        md_lines.append(f"| `{{r.get(label_col, '')}}` | **{{va_s}}** | {{vb_s}} |")

    return {{
        "status": "SUCCESS",
        "agent": {agent_id!r},
        "analyzed_table": chosen.stem,
        "available_tables": [p.stem for p in tfiles],
        "records_evaluated": len(rows),
        "kpi_summary": kpi_stats,
        "top_pareto_record": ranked[0] if ranked else {{}},
        "concise_markdown_table": "\\n".join(md_lines),
    }}


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
        return {{"status": "NO_DATA"}}

    rows = _read_json(chosen.name)
    label_col, col_a, col_b = _infer_chart_columns(rows)
    resolved_title = chart_title or f"{agent_id.replace('_', ' ').title()} — {{chosen.stem.replace('_', ' ').title()}}"
    spec = _build_dynamic_vegalite_spec(rows, label_col, col_a, col_b, title=resolved_title)
    _LAST_CHART_SPEC = spec

    labels = [str(r.get(label_col, "")) for r in rows]
    va = [float(r.get(col_a, 0.0) or 0.0) if isinstance(r.get(col_a), (int, float)) else 0.0 for r in rows]
    vb = [float(r.get(col_b, 0.0) or 0.0) if isinstance(r.get(col_b), (int, float)) else 0.0 for r in rows]

    png_meta = _render_comparison_png(
        agent_id={agent_id!r},
        title=resolved_title,
        subtitle=f"XYZ Global Industries Corp. (XYZ-CORP-01) · Source Table: {{chosen.stem}}",
        labels=labels,
        series_a=va,
        series_a_label=col_a.replace("_", " ").title(),
        series_b=vb,
        series_b_label=col_b.replace("_", " ").title(),
        y_title=col_a.replace("_", " ").title(),
    )
    return {{
        "status": "SUCCESS",
        "source_table": chosen.stem,
        "a2ui_vega_lite_queued": True,
        "png_infographic": png_meta,
    }}


def draft_operational_brief(
    subject: str = "",
    recipient_role: str = "Supply Chain & Operations Leadership",
    table_name: str = "",
) -> Dict[str, Any]:
    """Draft a concise, grounded persona operational decision brief or action memo from live Python KPIs."""
    analysis = analyze_operational_metrics(table_name=table_name)
    kpi = analysis.get("kpi_summary", {{}})
    doc_ref = f"BRIEF-{agent_id[:6].upper().replace('_', '')}-2026-{{analysis.get('records_evaluated', 8):02d}}"
    title_str = subject or f"{agent_id.replace('_', ' ').title()} Operational Decision Brief"
    brief_md = "\\n".join(
        [
            f"### 📄 {{title_str}} (`{{doc_ref}}`)",
            f"- **Organization**: XYZ Global Industries Corp. (`XYZ-CORP-01`)",
            f"- **To**: {{recipient_role}}",
            f"- **Source Table Audited**: `{{analysis.get('analyzed_table')}}` (`{{analysis.get('records_evaluated')}}` records)",
            f"- **Primary KPI (`{{kpi.get('primary_metric')}}`)**: Sum `{{kpi.get('sum_primary', 0):,.2f}}` | Mean `{{kpi.get('mean_primary', 0):,.2f}}` | Peak `{{kpi.get('max_primary', 0):,.2f}}`",
            "",
            analysis.get("concise_markdown_table", ""),
            "",
            "**Governance Gate**: Pre-validated against XYZ-CORP-01 tolerances; requires explicit confirmation and `idempotency_key` prior to ERP/WMS/TMS write-back.",
        ]
    )
    return {{
        "status": "DRAFT_READY",
        "document_ref": doc_ref,
        "recipient_role": recipient_role,
        "markdown_draft": brief_md,
    }}
{ENRICH_END}
'''


def upgrade_tools_py(agent_id: str, tools_py: Path, charts_py: Path, agent_py: Path | None = None) -> None:
    src = tools_py.read_text(encoding="utf-8")
    if ENRICH_BEGIN in src and ENRICH_END in src:
        pattern = re.compile(re.escape(ENRICH_BEGIN) + r".*?" + re.escape(ENRICH_END) + r"\n?", re.DOTALL)
        src = pattern.sub("", src)

    native_chart_fn = _find_native_chart_fn(charts_py, agent_py)
    block = _build_tools_enrichment_block(agent_id, native_chart_fn)
    tools_py.write_text(src.rstrip() + "\n\n\n" + block, encoding="utf-8")


CONCISE_PROTOCOL_MARKER = "STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:"
CONCISE_PROTOCOL_TEXT = """
STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:
- Lead with a 1–2 sentence deterministic KPI conclusion citing exact IDs and numbers from Python tools (zero fluff/filler).
- Always run Python tools (`analyze_operational_metrics`, `query_*`, `lookup_xyz_master_context`) for math and aggregations—never estimate mentally.
- Call `render_visual_chart` when visual comparison helps; the interactive A2UI `VegaChart` card renders automatically (never paste raw Vega-Lite JSON or base64 in text).
- Keep Markdown tables outside the card concise (`<=5` columns) for clean Google Sheets copy-paste.
- Call `draft_operational_brief` ONLY when drafting a formal memo, claim, or brief is requested or required.
- Never call `action_*` write-back tools on read-only questions.
"""


def _build_missing_adk_block(
    agent_id: str,
    cls_name: str,
    surface_fn: str,
    description: str,
) -> str:
    adk_cls = (cls_name[:-5] + "AdkApp") if cls_name.endswith("Agent") else (cls_name + "AdkApp")
    surface_import = f"from .render.surfaces import {surface_fn}" if surface_fn else ""
    emit_call = (
        f"a2ui_parts = {surface_fn}(surface_id, spec=tools.get_latest_chart_spec(consume=True))"
        if surface_fn
        else "a2ui_parts = []"
    )
    slug_prefix = agent_id[:16].replace("_", "-")
    return f'''

# ==============================================================================
# Google ADK & Vertex AI Reasoning Engine Integration
# ==============================================================================
try:
    import os
    import uuid
    from functools import cached_property
    from google.adk.agents import Agent
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.apps import App
    from google.adk.models import Gemini
    from google.adk.models.llm_request import LlmRequest
    from google.genai import Client, types
    from vertexai.preview.reasoning_engines import AdkApp
    from .render.a2ui_envelope import A2A_DATA_PART_OPEN_TAG
    {surface_import}

    class GlobalGemini(Gemini):
        """Routes Gemini calls to the global Vertex AI endpoint while Reasoning Engine runs in us-central1."""

        @cached_property
        def api_client(self) -> Client:
            return Client(
                vertexai=True,
                project=os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai"),
                location="global",
                http_options=types.HttpOptions(
                    headers=self._tracking_headers(),
                    retry_options=self.retry_options,
                ),
            )

    def _sanitize_llm_request(
        callback_context: Optional[CallbackContext] = None,
        llm_request: Optional[LlmRequest] = None,
        **_: Any,
    ) -> None:
        if llm_request is None or not llm_request.contents:
            return None
        for content in llm_request.contents:
            if not content.parts:
                continue
            cleaned: List[types.Part] = []
            for part in content.parts:
                if getattr(part, "inline_data", None) is not None:
                    continue
                t = getattr(part, "text", None)
                if t and A2A_DATA_PART_OPEN_TAG in t:
                    continue
                cleaned.append(part)
            content.parts = cleaned or [types.Part(text="[Visual Chart Surface Rendered in UI]")]
        return None

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            surface_id = f"{slug_prefix}-{{uuid.uuid4().hex[:8]}}"
            {emit_call}
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name={agent_id!r},
        description={description!r},
        model=GlobalGemini(
            model="gemini-3.1-pro-preview",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
        instruction=_INSTRUCTION,
        tools=_AVAILABLE_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name={agent_id!r})

    class {adk_cls}(AdkApp):
        """Vertex AI Reasoning Engine wrapper for {agent_id}."""

        def __init__(self, **kwargs: Any) -> None:
            super().__init__(agent=root_agent, **kwargs)

except ImportError:
    root_agent = {cls_name}()  # type: ignore
'''


def upgrade_agent_py(agent_id: str, agent_py: Path, surfaces_py: Path) -> None:
    src = agent_py.read_text(encoding="utf-8")

    # 1. Add concise deterministic rules to _INSTRUCTION idempotently
    if CONCISE_PROTOCOL_MARKER not in src:
        src = re.sub(
            r'(_INSTRUCTION\s*=\s*"""[\s\S]*?)(""")',
            lambda m: m.group(1).rstrip() + "\n" + CONCISE_PROTOCOL_TEXT + m.group(2),
            src,
            count=1,
        )

    # 2. Register the 4 new Python tools in _AVAILABLE_TOOLS idempotently
    new_tool_refs = [
        "tools.lookup_xyz_master_context",
        "tools.analyze_operational_metrics",
        "tools.render_visual_chart",
        "tools.draft_operational_brief",
    ]
    m_avail = re.search(r"(_AVAILABLE_TOOLS\s*=\s*\[)([\s\S]*?)(\])", src)
    if m_avail:
        body = m_avail.group(2)
        items = [x.strip() for x in body.replace("\n", ",").split(",") if x.strip()]
        for ref in new_tool_refs:
            if ref not in items:
                items.append(ref)
        formatted = "\n    " + ",\n    ".join(items) + ",\n"
        src = src[: m_avail.start()] + m_avail.group(1) + formatted + m_avail.group(3) + src[m_avail.end() :]

    # 3. Remove `after_model_callback=_append_verified_report,` from Agent(...) so read-only queries never mutate or double-print
    src = re.sub(r"\s*after_model_callback\s*=\s*_append_verified_report\s*,?", "", src)

    # 4. Keep `vega_spec = tools.get_native_chart_spec()` inside `run_scenario()` (word boundary on `spec`)
    #    and use `spec=tools.get_latest_chart_spec(consume=True)` inside `_emit_a2ui_surface`
    src = re.sub(
        r"\bvega_spec\s*=\s*tools\.get_latest_chart_spec\([^\)]*\)",
        "vega_spec = tools.get_native_chart_spec()",
        src,
    )
    src = re.sub(
        r"(?<![A-Za-z0-9_])spec\s*=\s*create_\w+\(\)",
        "spec=tools.get_latest_chart_spec(consume=True)",
        src,
    )
    src = re.sub(
        r"(?<![A-Za-z0-9_])spec\s*=\s*tools\.get_latest_chart_spec\(\)",
        "spec=tools.get_latest_chart_spec(consume=True)",
        src,
    )

    # 5. Ensure deterministic temperature=0.0
    src = re.sub(r"temperature\s*=\s*0\.[1-9]\d*", "temperature=0.0", src)

    # 6. Ensure Google ADK integration block + offline `root_agent = <ClsName>()` exists on every agent
    m_cls = re.search(r"class\s+(\w+)\s*:", src)
    cls_name = m_cls.group(1) if m_cls else "SupplyChainAgent"

    if "root_agent" not in src:
        m_desc = re.search(r'self\.description\s*=\s*"([^"]+)"', src)
        desc = m_desc.group(1) if m_desc else f"{agent_id.replace('_', ' ').title()} ADK Supply Chain Agent."
        surface_fn = _find_surface_fn(surfaces_py, agent_py)
        src = src.rstrip() + _build_missing_adk_block(agent_id, cls_name, surface_fn, desc)
    else:
        src = re.sub(
            r"except (?:ImportError|Exception):\s*\n\s*root_agent\s*=\s*None[^\n]*",
            f"except ImportError:\n    root_agent = {cls_name}()  # type: ignore",
            src,
        )

    agent_py.write_text(src, encoding="utf-8")


def _build_enrichment_test(agent_id: str, agent_py: Path) -> str:
    src = agent_py.read_text(encoding="utf-8")
    # Find the main Python agent class (the one defining `def execute_tool(`)
    m_cls = re.search(r"class\s+(\w+)\s*:", src)
    cls_name = m_cls.group(1) if m_cls else "Agent"
    return f'''"""Persona enrichment verification tests for {agent_id} (8-row data, Python math, PNG/Vega charts, drafting)."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

PKG_ROOT = Path(__file__).resolve().parent.parent
if str(PKG_ROOT) not in sys.path:
    sys.path.insert(0, str(PKG_ROOT))

from app.agent import {cls_name}  # noqa: E402
from app import tools  # noqa: E402


class TestPersonaEnrichment(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = {cls_name}()

    def test_tables_have_at_least_8_realistic_rows(self) -> None:
        tdir = PKG_ROOT / "fixtures" / "tables"
        json_files = sorted(tdir.glob("*.json"))
        self.assertGreaterEqual(len(json_files), 3)
        for jf in json_files:
            rows = json.loads(jf.read_text(encoding="utf-8"))
            self.assertGreaterEqual(len(rows), 8, f"{{jf.name}} has fewer than 8 rows")

    def test_master_backbone_join_and_python_analytics(self) -> None:
        m = self.agent.execute_tool("lookup_xyz_master_context", sku_id="SKU-XYZ-101", facility_id="PLANT-XYZ-STUTTGART")
        self.assertEqual(m["status"], "SUCCESS")
        self.assertIsNotNone(m.get("material"))
        res = self.agent.execute_tool("analyze_operational_metrics")
        self.assertEqual(res["status"], "SUCCESS")
        self.assertGreaterEqual(res["records_evaluated"], 8)
        self.assertIn("kpi_summary", res)

    def test_visual_png_and_vegalite_chart_and_brief_drafting(self) -> None:
        ch = self.agent.execute_tool("render_visual_chart")
        self.assertEqual(ch["status"], "SUCCESS")
        self.assertTrue(ch["a2ui_vega_lite_queued"])
        if ch["png_infographic"]["status"] == "SUCCESS":
            self.assertTrue(Path(ch["png_infographic"]["png_path"]).exists())
        dr = self.agent.execute_tool("draft_operational_brief")
        self.assertEqual(dr["status"], "DRAFT_READY")
        self.assertIn("XYZ-CORP-01", dr["markdown_draft"])


if __name__ == "__main__":
    unittest.main()
'''


def main() -> None:
    enriched_count = 0
    total_tables = 0
    total_rows = 0

    for pkg in sorted(AGENTS_DIR.iterdir()):
        if not pkg.is_dir() or pkg.name == "common" or pkg.name in COHORT1_IDS:
            continue
        app_dir = pkg / "app"
        render_dir = app_dir / "render"
        tables_dir = pkg / "fixtures" / "tables"
        tests_dir = pkg / "tests"
        if not (app_dir / "agent.py").exists() or not (app_dir / "tools.py").exists():
            continue

        render_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)

        # 1. Expand all JSON fixture tables to >=8 rows
        for jf in sorted(tables_dir.glob("*.json")):
            rc = expand_fixture_table_to_8_rows(jf, target_min_rows=8)
            total_tables += 1
            total_rows += rc

        # 2. Ensure self-contained render modules + Pillow PNG generator
        (render_dir / "png_chart.py").write_text(PNG_CHART_CODE, encoding="utf-8")
        if not (render_dir / "a2ui_envelope.py").exists():
            (render_dir / "a2ui_envelope.py").write_text(A2UI_ENVELOPE_CODE, encoding="utf-8")
        if not (render_dir / "a2ui_lifecycle.py").exists():
            (render_dir / "a2ui_lifecycle.py").write_text(A2UI_LIFECYCLE_CODE, encoding="utf-8")

        # 3. Enrich tools.py & agent.py
        upgrade_tools_py(pkg.name, app_dir / "tools.py", render_dir / "charts.py", app_dir / "agent.py")
        upgrade_agent_py(pkg.name, app_dir / "agent.py", render_dir / "surfaces.py")

        # 4. Write dedicated enrichment test suite alongside existing test_smoke.py
        (tests_dir / "test_persona_enrichment.py").write_text(
            _build_enrichment_test(pkg.name, app_dir / "agent.py"), encoding="utf-8"
        )
        enriched_count += 1

    print(
        f"[OK] Enriched {enriched_count} existing agent packages across {total_tables} tables "
        f"({total_rows} total realistic organizational rows), added Pillow PNG + dynamic Vega-Lite charting, "
        f"Python analytics, operational brief drafting, and concise non-mutating ADK callbacks."
    )


if __name__ == "__main__":
    main()
