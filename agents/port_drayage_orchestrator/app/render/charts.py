"""Vega-Lite chart specifications for PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_port_drayage_orchestrator_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for PortWatch — Global Ocean Vessel, Container Stowage & Port Drayage Orchestrator."""
    if not data_points:
        data_points = [
            {
                        "container_batch": "MSKU-904812 (Transload)",
                        "dwell_hours": 18.0,
                        "demurrage_saved_usd": 1875,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "container_batch": "MSKU-904819 (Dual Gate)",
                        "dwell_hours": 26.5,
                        "demurrage_saved_usd": 1500,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "container_batch": "CMAU-441029 (Rail Ramp)",
                        "dwell_hours": 31.0,
                        "demurrage_saved_usd": 1125,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "container_batch": "Unmonitored Port Baseline",
                        "dwell_hours": 114.0,
                        "demurrage_saved_usd": 0,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "PortWatch Container Dwell & Demurrage Avoidance",
        "title": {
            "text": "PortWatch Container Dwell & Demurrage Avoidance",
            "subtitle": "Spire Satellite AIS + WeatherNext 3 Berth Prediction (Port Dwell Hours vs. Demurrage $ Saved)",
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
                    "x": {"field": "container_batch", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "dwell_hours", "type": "quantitative", "title": "dwell_hours"},
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
                    "x": {"field": "container_batch", "type": "nominal"},
                    "y": {
                        "field": "demurrage_saved_usd",
                        "type": "quantitative",
                        "axis": {"title": "demurrage_saved_usd", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
