"""Vega-Lite chart specifications for BeatSync — Field Sales & Distributor Inventory Harmonizer."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_field_beat_distributor_sync_agent_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for BeatSync — Field Sales & Distributor Inventory Harmonizer."""
    if not data_points:
        data_points = [
            {
                        "beat_territory": "West Zone (BeatSync Live)",
                        "fill_rate_pct": 98.4,
                        "productive_call_pct": 89.5,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "beat_territory": "North Zone (BeatSync Live)",
                        "fill_rate_pct": 97.6,
                        "productive_call_pct": 87.2,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "beat_territory": "Unsynced Static Beat",
                        "fill_rate_pct": 76.5,
                        "productive_call_pct": 62.0,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "BeatSync Secondary Order Fill-Rate & FSO Productive Call Lift",
        "title": {
            "text": "BeatSync Secondary Order Fill-Rate & FSO Productive Call Lift",
            "subtitle": "Live DMS-to-SFA Synchronization (Secondary Order Fill Rate % vs. Productive Calls)",
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
                    "x": {"field": "beat_territory", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "fill_rate_pct", "type": "quantitative", "title": "fill_rate_pct"},
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
                    "x": {"field": "beat_territory", "type": "nominal"},
                    "y": {
                        "field": "productive_call_pct",
                        "type": "quantitative",
                        "axis": {"title": "productive_call_pct", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
