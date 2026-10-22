"""Vega-Lite chart specifications for IntermodalSync — Factory-to-DC Intermodal Rail, Barge & Linehaul Orchestrator."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_intermodal_rail_linehaul_agent_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for IntermodalSync — Factory-to-DC Intermodal Rail, Barge & Linehaul Orchestrator."""
    if not data_points:
        data_points = [
            {
                        "corridor_mode": "LAX\u2794CHI (COFC Rail)",
                        "cost_usd": 2890,
                        "co2e_kg": 890,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "corridor_mode": "LAX\u2794CHI (OTR Truck)",
                        "cost_usd": 4650,
                        "co2e_kg": 2815,
                        "status": "LEGACY_STATIC"
            },
            {
                        "corridor_mode": "SAV\u2794MEM (CSX Rail)",
                        "cost_usd": 1420,
                        "co2e_kg": 410,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "corridor_mode": "SAV\u2794MEM (OTR Truck)",
                        "cost_usd": 2350,
                        "co2e_kg": 1290,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "IntermodalSync OTR-to-Rail Cost & Carbon Reduction",
        "title": {
            "text": "IntermodalSync OTR-to-Rail Cost & Carbon Reduction",
            "subtitle": "Class-I COFC Double-Stack Rail vs. OTR Diesel Truck (Linehaul Cost $ vs. CO2e kg)",
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
                    "x": {"field": "corridor_mode", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "cost_usd", "type": "quantitative", "title": "cost_usd"},
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["OPTIMIZED_CVRPTW", "LEGACY_STATIC"],
                            "range": ["#1e8e3e", "#ea4335"]
                        },
                        "title": "Execution Mode"
                    },
                }
            },
            {
                "mark": {"type": "line", "point": True, "color": "#fbbc04", "strokeWidth": 2.5},
                "encoding": {
                    "x": {"field": "corridor_mode", "type": "nominal"},
                    "y": {
                        "field": "co2e_kg",
                        "type": "quantitative",
                        "axis": {"title": "co2e_kg", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
