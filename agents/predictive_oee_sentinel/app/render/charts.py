"""Vega-Lite chart specifications for AssetGuard Plant Predictive Maintenance & OEE Agent."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_oee_breakdown_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an OEE Waterfall / Component Breakdown and World-Class benchmark comparison."""
    if not data_points:
        data_points = [
            {"component": "Availability", "rate_pct": 73.33, "benchmark_pct": 90.0, "status": "DOWNTIME_LOSS"},
            {"component": "Performance", "rate_pct": 84.66, "benchmark_pct": 95.0, "status": "SPEED_LOSS"},
            {"component": "Quality", "rate_pct": 91.95, "benchmark_pct": 99.0, "status": "SCRAP_LOSS"},
            {"component": "Overall OEE", "rate_pct": 57.08, "benchmark_pct": 85.0, "status": "CRITICAL_DEFICIT"},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "AssetGuard OEE Loss Decomposition and World-Class Benchmark Comparison",
        "title": {
            "text": "AssetGuard OEE Loss Waterfall (CNC Milling Center CNC-04)",
            "subtitle": "Current OEE 57.1% vs World-Class Target 85.0% · 128 min Unplanned Bearing Interlock Loss",
            "anchor": "start",
            "fontSize": 14,
            "subtitleFontSize": 11,
            "subtitleColor": "#5f6368"
        },
        "width": 640,
        "height": 280,
        "data": {"values": data_points},
        "layer": [
            {
                "mark": {"type": "bar", "cornerRadiusTopLeft": 4, "cornerRadiusTopRight": 4, "size": 38},
                "encoding": {
                    "x": {"field": "component", "type": "nominal", "title": "OEE Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "rate_pct", "type": "quantitative", "title": "Efficiency Percentage (%)", "scale": {"domain": [0, 100]}},
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["DOWNTIME_LOSS", "SPEED_LOSS", "SCRAP_LOSS", "CRITICAL_DEFICIT"],
                            "range": ["#ea4335", "#fbbc04", "#4285f4", "#b31412"]
                        },
                        "title": "Loss Classification"
                    },
                    "tooltip": [
                        {"field": "component", "title": "Metric"},
                        {"field": "rate_pct", "title": "Observed (%)"},
                        {"field": "benchmark_pct", "title": "Target (%)"}
                    ]
                }
            },
            {
                "mark": {"type": "tick", "color": "#188038", "thickness": 3, "size": 42},
                "encoding": {
                    "x": {"field": "component", "type": "nominal"},
                    "y": {"field": "benchmark_pct", "type": "quantitative"}
                }
            }
        ]
    }
