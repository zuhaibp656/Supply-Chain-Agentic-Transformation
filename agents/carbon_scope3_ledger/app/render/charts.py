"""Vega-Lite chart specifications for EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_carbon_scope3_ledger_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger."""
    if not data_points:
        data_points = [
            {
                        "compliance_scope": "Hydro EAF Aluminum (Primary)",
                        "emissions_tco2e": 252,
                        "cbam_eur_saved": 64260,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "compliance_scope": "EU Default Penalty Factor",
                        "emissions_tco2e": 1008,
                        "cbam_eur_saved": 0,
                        "status": "LEGACY_STATIC"
            },
            {
                        "compliance_scope": "Rhine HVO100 + Barge Swap",
                        "emissions_tco2e": 410,
                        "cbam_eur_saved": 28400,
                        "status": "OPTIMIZED_CVRPTW"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "EcoChain Scope-3 Carbon Intensity & EU CBAM Tax Shield",
        "title": {
            "text": "EcoChain Scope-3 Carbon Intensity & EU CBAM Tax Shield",
            "subtitle": "ISO 14083 Primary Telemetry vs. EU Default Penalty Factors (tCO2e vs. CBAM \u20ac Saved)",
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
                    "x": {"field": "compliance_scope", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "emissions_tco2e", "type": "quantitative", "title": "emissions_tco2e"},
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
                    "x": {"field": "compliance_scope", "type": "nominal"},
                    "y": {
                        "field": "cbam_eur_saved",
                        "type": "quantitative",
                        "axis": {"title": "cbam_eur_saved", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
