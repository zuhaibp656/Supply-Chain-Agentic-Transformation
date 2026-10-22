"""Vega-Lite chart specifications for OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_otif_penalty_shield_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent."""
    if not data_points:
        data_points = [
            {
                        "key_account": "BigBox Retail #01 (OTIFShield)",
                        "otif_pct": 99.2,
                        "penalties_saved_usd": 22050,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "key_account": "National Grocer #02 (OTIFShield)",
                        "otif_pct": 98.9,
                        "penalties_saved_usd": 16800,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "key_account": "Reactive Post-Mortem Baseline",
                        "otif_pct": 93.4,
                        "penalties_saved_usd": 0,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "OTIFShield Penalty Prevention & Chargeback Recovery",
        "title": {
            "text": "OTIFShield Penalty Prevention & Chargeback Recovery",
            "subtitle": "72h Predictive SLA Rescue + Geofence Dispute Dossiers (OTIF % vs. Chargebacks Recovered $)",
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
                    "x": {"field": "key_account", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "otif_pct", "type": "quantitative", "title": "otif_pct"},
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
                    "x": {"field": "key_account", "type": "nominal"},
                    "y": {
                        "field": "penalties_saved_usd",
                        "type": "quantitative",
                        "axis": {"title": "penalties_saved_usd", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
