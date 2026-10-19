"""Vega-Lite chart specifications for QualiShield Supplier Quality Sentinel."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_spc_cpk_control_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an SPC X-bar / Cpk run chart with USL, LSL, UCL, LCL, and lot measurements."""
    if not data_points:
        data_points = [
            {"lot_sample": "Lot 8835", "measurement": 181.2, "status": "CONFORMING", "usl": 190.0, "lsl": 170.0, "target": 180.0, "ucl": 186.0, "lcl": 174.0},
            {"lot_sample": "Lot 8836", "measurement": 179.8, "status": "CONFORMING", "usl": 190.0, "lsl": 170.0, "target": 180.0, "ucl": 186.0, "lcl": 174.0},
            {"lot_sample": "Lot 8837", "measurement": 178.5, "status": "CONFORMING", "usl": 190.0, "lsl": 170.0, "target": 180.0, "ucl": 186.0, "lcl": 174.0},
            {"lot_sample": "Lot 8838", "measurement": 175.2, "status": "WARNING_DRIFT", "usl": 190.0, "lsl": 170.0, "target": 180.0, "ucl": 186.0, "lcl": 174.0},
            {"lot_sample": "Lot 8839", "measurement": 173.0, "status": "WARNING_DRIFT", "usl": 190.0, "lsl": 170.0, "target": 180.0, "ucl": 186.0, "lcl": 174.0},
            {"lot_sample": "Lot 8840", "measurement": 169.4, "status": "OUT_OF_SPEC", "usl": 190.0, "lsl": 170.0, "target": 180.0, "ucl": 186.0, "lcl": 174.0},
            {"lot_sample": "Lot 8841 (Quarantined)", "measurement": 164.2, "status": "OUT_OF_SPEC_CRITICAL", "usl": 190.0, "lsl": 170.0, "target": 180.0, "ucl": 186.0, "lcl": 174.0},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "QualiShield Statistical Process Control (SPC) Lot Inspection & Cpk Drift Analysis",
        "title": {
            "text": "QualiShield SPC Process Capability Drift (Kyocera AlN Substrates)",
            "subtitle": "Thermal Conductivity (W/m·K) vs Specification Limits (USL 190 / LSL 170) · Cpk = 0.54 (Unstable)",
            "anchor": "start",
            "fontSize": 14,
            "subtitleFontSize": 11,
            "subtitleColor": "#5f6368"
        },
        "width": 640,
        "height": 300,
        "data": {"values": data_points},
        "layer": [
            {
                "mark": {"type": "line", "point": True, "strokeWidth": 2.5},
                "encoding": {
                    "x": {"field": "lot_sample", "type": "nominal", "title": "Inspection Lot Subgroup", "axis": {"labelAngle": -20}},
                    "y": {
                        "field": "measurement",
                        "type": "quantitative",
                        "title": "Measured Thermal Conductivity (W/m·K)",
                        "scale": {"domain": [155, 195]}
                    },
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "title": "Inspection Disposition",
                        "scale": {
                            "domain": ["CONFORMING", "WARNING_DRIFT", "OUT_OF_SPEC", "OUT_OF_SPEC_CRITICAL"],
                            "range": ["#1e8e3e", "#f9ab00", "#d93025", "#b31412"]
                        }
                    },
                    "tooltip": [
                        {"field": "lot_sample", "title": "Lot"},
                        {"field": "measurement", "title": "Conductivity (W/m·K)"},
                        {"field": "status", "title": "Disposition"}
                    ]
                }
            },
            {
                "mark": {"type": "rule", "strokeDash": [4, 4], "color": "#d93025", "size": 1.5},
                "encoding": {"y": {"datum": 170.0}}
            },
            {
                "mark": {"type": "rule", "strokeDash": [4, 4], "color": "#1a73e8", "size": 1.5},
                "encoding": {"y": {"datum": 180.0}}
            },
            {
                "mark": {"type": "rule", "strokeDash": [4, 4], "color": "#d93025", "size": 1.5},
                "encoding": {"y": {"datum": 190.0}}
            }
        ]
    }
