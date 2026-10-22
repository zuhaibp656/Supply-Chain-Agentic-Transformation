"""Vega-Lite chart specifications for ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_multimodal_mode_shift_agent_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for ModalShift — Factory→Ship→Air→Rail→Truck Dynamic Mode-Switch Broker."""
    if not data_points:
        data_points = [
            {
                        "routing_strategy": "ModalShift 85/15 Split",
                        "freight_cost_usd": 12975,
                        "effective_lead_days": 14,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "routing_strategy": "100% Panic Air Charter",
                        "freight_cost_usd": 106200,
                        "effective_lead_days": 4,
                        "status": "LEGACY_STATIC"
            },
            {
                        "routing_strategy": "100% Slow Ocean (+Stockout)",
                        "freight_cost_usd": 7560,
                        "effective_lead_days": 34,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "ModalShift Multi-Modal Split vs. Single-Mode Panic Expedite",
        "title": {
            "text": "ModalShift Multi-Modal Split vs. Single-Mode Panic Expedite",
            "subtitle": "Pareto Optimal 85% Ocean + 15% Sea-Air Split (Total Freight Cost $ vs. Transit Days)",
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
                    "x": {"field": "routing_strategy", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "freight_cost_usd", "type": "quantitative", "title": "freight_cost_usd"},
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
                    "x": {"field": "routing_strategy", "type": "nominal"},
                    "y": {
                        "field": "effective_lead_days",
                        "type": "quantitative",
                        "axis": {"title": "effective_lead_days", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
