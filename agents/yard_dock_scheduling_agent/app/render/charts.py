"""Vega-Lite chart specifications for YardPulse Yard & Dock Orchestrator."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_yard_dock_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a Trailer Turnaround Dwell Time & Demurrage Risk chart."""
    if not data_points:
        data_points = [
            {"trailer": "TRL-SWIFT-7741", "carrier": "Swift", "dwell_minutes": 85.0, "threshold_minutes": 120.0, "status": "EXPEDITED_AT_RISK"},
            {"trailer": "TRL-JB-HUNT-1204", "carrier": "J.B. Hunt", "dwell_minutes": 35.0, "threshold_minutes": 120.0, "status": "IN_SPEC_HEALTHY"},
            {"trailer": "TRL-SCHNEIDER-882", "carrier": "Schneider", "dwell_minutes": 48.0, "threshold_minutes": 120.0, "status": "IN_SPEC_HEALTHY"},
            {"trailer": "TRL-KNIGHT-3319", "carrier": "Knight-Swift", "dwell_minutes": 62.0, "threshold_minutes": 120.0, "status": "IN_SPEC_HEALTHY"},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "YardPulse Yard Gate Dwell & 2-Hour Carrier Detention Threshold",
        "title": {
            "text": "YardPulse Trailer Turnaround & Detention Demurrage Shield",
            "subtitle": "Swift Trailer TRL-7741 Expedited to Door 08 at 85 min Dwell · Avoided $255 Detention Surcharge",
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
                    "x": {"field": "trailer", "type": "nominal", "title": "Inbound Carrier Trailer", "axis": {"labelAngle": 0}},
                    "y": {"field": "dwell_minutes", "type": "quantitative", "title": "Yard Dwell Time (Minutes)", "scale": {"domain": [0, 140]}},
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["EXPEDITED_AT_RISK", "IN_SPEC_HEALTHY"],
                            "range": ["#ea4335", "#1e8e3e"]
                        },
                        "title": "Turnaround SLA"
                    },
                    "tooltip": [
                        {"field": "trailer", "title": "Trailer"},
                        {"field": "carrier", "title": "Carrier"},
                        {"field": "dwell_minutes", "title": "Current Dwell (min)"},
                        {"field": "threshold_minutes", "title": "Free Detention Limit (min)"}
                    ]
                }
            },
            {
                "mark": {"type": "rule", "color": "#fbbc04", "strokeWidth": 2.5, "strokeDash": [6, 4]},
                "encoding": {
                    "y": {"datum": 120.0}
                }
            }
        ]
    }
