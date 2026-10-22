"""Vega-Lite chart specifications for PromiseGuard ATP Order Promising Agent."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_order_promising_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a Real-Time ATP Allocation & Tier Quota Protection chart."""
    if not data_points:
        data_points = [
            {"node": "CDC Chicago (Tier 1)", "tier1_reserved": 20000, "uncommitted_atp": 34200, "committed_allocated": 14200},
            {"node": "RDC Dallas (Tier 2)", "tier1_reserved": 5000, "uncommitted_atp": 3300, "committed_allocated": 5400},
            {"node": "RDC Atlanta (Tier 2)", "tier1_reserved": 8000, "uncommitted_atp": 12400, "committed_allocated": 4100},
            {"node": "FDC Austin (Tier 3)", "tier1_reserved": 1500, "uncommitted_atp": 1800, "committed_allocated": 800},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "PromiseGuard Sub-50ms Spanner ATP & Strategic Tier Quota Protection",
        "title": {
            "text": "PromiseGuard Real-Time Order Promising & ATP Inventory Pools",
            "subtitle": "Spanner Real-Time Stock Sub-15ms · Kroger Strategic Tier 1 Quota Protected (20,000 Units)",
            "anchor": "start",
            "fontSize": 14,
            "subtitleFontSize": 11,
            "subtitleColor": "#5f6368"
        },
        "width": 640,
        "height": 280,
        "data": {"values": data_points},
        "transform": [
            {"fold": ["tier1_reserved", "uncommitted_atp", "committed_allocated"], "as": ["Pool", "Units"]}
        ],
        "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4},
        "encoding": {
            "x": {"field": "node", "type": "nominal", "title": "Fulfillment Node", "axis": {"labelAngle": 0}},
            "y": {"field": "Units", "type": "quantitative", "title": "Inventory Allocation (Units)"},
            "color": {
                "field": "Pool",
                "type": "nominal",
                "scale": {
                    "domain": ["tier1_reserved", "uncommitted_atp", "committed_allocated"],
                    "range": ["#1a73e8", "#1e8e3e", "#5f6368"]
                },
                "legend": {
                    "title": "Inventory Pool",
                    "labelExpr": "datum.value == 'tier1_reserved' ? 'Strategic Tier 1 Quota' : datum.value == 'uncommitted_atp' ? 'Uncommitted ATP' : 'Committed / In-Flight'"
                }
            },
            "tooltip": [
                {"field": "node", "title": "Node"},
                {"field": "Pool", "title": "Allocation Pool"},
                {"field": "Units", "title": "Units"}
            ]
        }
    }
