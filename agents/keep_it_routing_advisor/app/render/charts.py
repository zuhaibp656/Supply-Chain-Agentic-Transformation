"""Dynamic Vega-Lite v5 Chart Spec Builder for [06 · Return | Returns & Claims Mgmt] Returnless 'Keep-It' Economics Advisor."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

_FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures" / "tables"


def create_keep_it_routing_advisor_chart_spec(
    rows: Optional[List[Dict[str, Any]]] = None,
    title_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Builds a live Vega-Lite v5 grouped comparison spec from enterprise fixture data."""
    if rows is None:
        fpath = _FIXTURES_DIR / "keep_it_instant_refund_decisions.json"
        if fpath.exists():
            rows = json.loads(fpath.read_text(encoding="utf-8"))
        else:
            rows = []

    values: List[Dict[str, Any]] = []
    for r in rows[:8]:
        lbl = str(r.get("rma_req_id", "Record"))
        va = float(r.get("physical_return_cost_usd", 0.0) or 0.0)
        vb = float(r.get("expected_salvage_usd", 0.0) or 0.0)
        values.append({"entity": lbl, "series": 'Reverse Shipping + Labor ($)', "metric_value": round(va, 2)})
        values.append({"entity": lbl, "series": 'Expected Resale Recovery ($)', "metric_value": round(vb, 2)})

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title_override or "Returnless 'Keep-It' Economics — Reverse Shipping & Triage Cost ($) vs. Expected Salvage ($)",
            "subtitle": "XYZ Global Industries Corp. (XYZ-CORP-01) · Live Persona Telemetry",
            "anchor": "start",
            "fontSize": 14,
            "subtitleColor": "#64748b",
        },
        "width": "container",
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
                "title": 'USD per RMA',
                "axis": {"grid": True, "gridColor": "#e2e8f0"},
            },
            "color": {
                "field": "series",
                "type": "nominal",
                "title": "Metric Series",
                "scale": {
                    "domain": ['Reverse Shipping + Labor ($)', 'Expected Resale Recovery ($)'],
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
