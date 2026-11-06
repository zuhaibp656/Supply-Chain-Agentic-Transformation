"""Dynamic Vega-Lite v5 Chart Spec Builder for [05 · Deliver | First & Mid-Mile] Cold-Chain Auditor."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

def _resolve_charts_fixtures_dir() -> Path:
    import os as _os
    import sys as _sys
    from pathlib import Path as _Path
    candidates = [
        _Path(__file__).resolve().parent.parent.parent / "fixtures" / "tables",
        _Path.cwd() / "fixtures" / "tables",
        _Path("/code/fixtures/tables"),
    ]
    env_root = _os.environ.get("FIXTURES_ROOT")
    if env_root:
        candidates.append(_Path(env_root) / "tables")
    for sp in list(_sys.path):
        if sp:
            candidates.append(_Path(sp) / "fixtures" / "tables")
    for c in candidates:
        try:
            if c.is_dir():
                return c
        except Exception:
            continue
    return candidates[0]



def create_cold_chain_auditor_chart_spec(
    rows: Optional[List[Dict[str, Any]]] = None,
    title_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Builds a live Vega-Lite v5 grouped comparison spec from enterprise fixture data."""
    if rows is None:
        fpath = _resolve_charts_fixtures_dir() / "qa_disposition_claims_ledger.json"
        if fpath.exists():
            rows = json.loads(fpath.read_text(encoding="utf-8"))
        else:
            rows = []

    values: List[Dict[str, Any]] = []
    for r in rows[:8]:
        lbl = str(r.get("shipment_id", "Record"))
        va = float(r.get("computed_mkt_c", 0.0) or 0.0)
        vb = float(r.get("max_mkt_allowed_c", 0.0) or 0.0)
        values.append({"entity": lbl, "series": 'Computed Arrhenius MKT (°C)', "metric_value": round(va, 2)})
        values.append({"entity": lbl, "series": 'Max Allowed MKT Limit (°C)', "metric_value": round(vb, 2)})

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title_override or 'Cold-Chain Excursion Audit — Arrhenius MKT (°C) vs. Max Allowed Stability Limit (°C)',
            "subtitle": "XYZ Global Industries Corp. (XYZ-CORP-01) · Live Persona Telemetry",
            "anchor": "start",
            "fontSize": 14,
            "subtitleColor": "#64748b",
        },
        "width": 620,
        "height": 300,
        "data": {"values": values},
        "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "tooltip": True},
        "encoding": {
            "x": {
                "field": "entity",
                "type": "nominal",
                "title": None,
                "axis": {"labelAngle": -25, "labelFontSize": 11},
            },
            "xOffset": {"field": "series"},
            "y": {
                "field": "metric_value",
                "type": "quantitative",
                "title": 'Temperature (°C)',
                "axis": {"grid": True, "gridColor": "#e2e8f0"},
            },
            "color": {
                "field": "series",
                "type": "nominal",
                "title": "Metric Series",
                "scale": {
                    "domain": ['Computed Arrhenius MKT (°C)', 'Max Allowed MKT Limit (°C)'],
                    "range": ["#64748b", "#2563eb"],
                },
                "legend": {"orient": "top"},
            },
            "tooltip": [
                {"field": "entity", "type": "nominal", "title": "Record"},
                {"field": "series", "type": "nominal", "title": "Series"},
                {"field": "metric_value", "type": "quantitative", "title": "Value", "format": ",.2f"},
            ],
        },
        "config": {"view": {"stroke": "transparent"}, "font": "Inter, system-ui, sans-serif"},
    }
