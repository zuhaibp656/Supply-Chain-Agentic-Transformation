"""Vega-Lite chart specifications for TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_network_twin_architect_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for TwinDesign — Supply Chain Network & Cost-to-Serve Optimizer."""
    if not data_points:
        data_points = [
            {
                        "network_topology": "Optimized + Savannah Hub",
                        "annual_cost_m_usd": 67.4,
                        "one_day_sla_pct": 91.2,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "network_topology": "Nearshore Tariff Resilient",
                        "annual_cost_m_usd": 69.1,
                        "one_day_sla_pct": 89.8,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "network_topology": "Legacy 3-RDC Baseline",
                        "annual_cost_m_usd": 74.2,
                        "one_day_sla_pct": 76.4,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "TwinDesign Network Center-of-Gravity & Cost-to-Serve Optimization",
        "title": {
            "text": "TwinDesign Network Center-of-Gravity & Cost-to-Serve Optimization",
            "subtitle": "OR-Tools Facility Location MILP (Total Network Cost $M vs. 1-Day Ground SLA %)",
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
                    "x": {"field": "network_topology", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "annual_cost_m_usd", "type": "quantitative", "title": "annual_cost_m_usd"},
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
                    "x": {"field": "network_topology", "type": "nominal"},
                    "y": {
                        "field": "one_day_sla_pct",
                        "type": "quantitative",
                        "axis": {"title": "one_day_sla_pct", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
