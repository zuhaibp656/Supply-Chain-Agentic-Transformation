"""Vega-Lite chart specifications for ChangeSync — Engineering Change (ECO) & NPI Cutover Orchestrator."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_eco_cutover_orchestrator_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a visual Vega-Lite v5 specification for ChangeSync — Engineering Change (ECO) & NPI Cutover Orchestrator."""
    if not data_points:
        data_points = [
            {
                        "cutover_mode": "ChangeSync Dynamic Runout",
                        "scrap_writeoff_usd": 8400,
                        "exhaustion_pct": 98.1,
                        "status": "OPTIMIZED_CVRPTW"
            },
            {
                        "cutover_mode": "Blind Immediate Cutover",
                        "scrap_writeoff_usd": 436500,
                        "exhaustion_pct": 12.0,
                        "status": "LEGACY_STATIC"
            },
            {
                        "cutover_mode": "Manual Spreadsheet Guess",
                        "scrap_writeoff_usd": 194000,
                        "exhaustion_pct": 55.5,
                        "status": "LEGACY_STATIC"
            }
]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "ChangeSync Multi-Plant ECO Runout & E&O Write-Off Prevention",
        "title": {
            "text": "ChangeSync Multi-Plant ECO Runout & E&O Write-Off Prevention",
            "subtitle": "PLM-to-ERP Dynamic BOM Effectivity Solver (Obsolete Scrap Write-Off $ vs. Runout %)",
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
                    "x": {"field": "cutover_mode", "type": "nominal", "title": "Operational Dimension", "axis": {"labelAngle": 0}},
                    "y": {"field": "scrap_writeoff_usd", "type": "quantitative", "title": "scrap_writeoff_usd"},
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
                    "x": {"field": "cutover_mode", "type": "nominal"},
                    "y": {
                        "field": "exhaustion_pct",
                        "type": "quantitative",
                        "axis": {"title": "exhaustion_pct", "orient": "right"},
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
