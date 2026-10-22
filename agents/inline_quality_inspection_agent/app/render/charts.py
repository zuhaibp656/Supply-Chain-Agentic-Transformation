"""Vega-Lite chart specifications for VisionInspect Inline Quality Inspection Agent."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_vision_inspection_chart_spec(
    data_points: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates a Multimodal Vision Defect Classification Confidence & Defect Rate chart."""
    if not data_points:
        data_points = [
            {"station": "Induction Seal Integrity", "confidence_pct": 98.5, "defect_ppm": 320, "status": "ACTIVE_DEFECT_DIVERTED"},
            {"station": "Cap Screw Torque & Flange", "confidence_pct": 99.1, "defect_ppm": 45, "status": "IN_SPEC_STABLE"},
            {"station": "2D DataMatrix Barcode", "confidence_pct": 99.8, "defect_ppm": 12, "status": "IN_SPEC_STABLE"},
            {"station": "Carton Crease & Top Seam", "confidence_pct": 99.4, "defect_ppm": 68, "status": "IN_SPEC_STABLE"},
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "VisionInspect Multimodal Gemini 3.8 Flash Vision Inline Inspection Telemetry",
        "title": {
            "text": "VisionInspect Inline Optical Defect Classification (Aseptic Line 01)",
            "subtitle": "Multimodal Gemini 3.8 Flash Vision (120 fpm) · Induction Foil Seal Breach Diverted at 14.2 ms Latency",
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
                    "x": {"field": "station", "type": "nominal", "title": "Inspection Station", "axis": {"labelAngle": 0}},
                    "y": {"field": "confidence_pct", "type": "quantitative", "title": "Vision AI Confidence (%)", "scale": {"domain": [90, 100]}},
                    "color": {
                        "field": "status",
                        "type": "nominal",
                        "scale": {
                            "domain": ["ACTIVE_DEFECT_DIVERTED", "IN_SPEC_STABLE"],
                            "range": ["#ea4335", "#1e8e3e"]
                        },
                        "title": "Station State"
                    },
                    "tooltip": [
                        {"field": "station", "title": "Station"},
                        {"field": "confidence_pct", "title": "Model Confidence (%)"},
                        {"field": "defect_ppm", "title": "Defect Rate (PPM)"}
                    ]
                }
            },
            {
                "mark": {"type": "line", "point": True, "color": "#fbbc04", "strokeWidth": 2.5},
                "encoding": {
                    "x": {"field": "station", "type": "nominal"},
                    "y": {
                        "field": "defect_ppm",
                        "type": "quantitative",
                        "axis": {"title": "Station Defect Rate (PPM)", "orient": "right"},
                        "scale": {"domain": [0, 400]}
                    }
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
