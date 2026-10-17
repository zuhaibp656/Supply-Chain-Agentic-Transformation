"""Deterministic Vega-Lite Chart Specs for CSCO Control Tower Copilot."""
from __future__ import annotations
from typing import Any, Dict, List, Optional

FONT = "Google Sans, Roboto, Arial, sans-serif"


def create_bottleneck_impact_bars(width: int = 560, height: int = 210) -> Dict[str, Any]:
    """Generates an executive bar chart of network bottlenecks by revenue at risk ($M)."""
    data = [
        {"location": "Red Sea / Suez Maritime Chokepoint", "impact_m": 7.2, "delay": "14.5d", "color": "#d93025"},
        {"location": "Frankfurt Airport Cargo Terminal 2", "impact_m": 3.8, "delay": "4.2d", "color": "#f9ab00"},
        {"location": "Dallas Regional Cross-Dock Hub", "impact_m": 2.4, "delay": "3.8d", "color": "#f9ab00"},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "Network Bottlenecks · Revenue at Immediate Risk ($M)",
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": data},
        "mark": {"type": "bar", "cornerRadiusEnd": 4},
        "encoding": {
            "y": {
                "field": "location",
                "type": "nominal",
                "sort": "-x",
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": None, "domain": False},
            },
            "x": {
                "field": "impact_m",
                "type": "quantitative",
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": "Revenue Impact ($M)", "grid": True},
            },
            "color": {
                "field": "color",
                "type": "nominal",
                "scale": None,
            },
            "tooltip": [
                {"field": "location", "type": "nominal", "title": "Bottleneck Node"},
                {"field": "impact_m", "type": "quantitative", "title": "Jeopardy ($M)"},
                {"field": "delay", "type": "nominal", "title": "Transit Delay"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_otif_trend_line_chart(width: int = 560, height: int = 190) -> Dict[str, Any]:
    """Generates an OTIF recovery trajectory line chart comparing historical vs agentic remediation."""
    data = [
        {"period": "Wk 38 (Actual)", "otif": 87.2, "target": 95.0, "stage": "Historical Baseline"},
        {"period": "Wk 39 (Actual)", "otif": 85.8, "target": 95.0, "stage": "Historical Baseline"},
        {"period": "Wk 40 (Actual)", "otif": 86.4, "target": 95.0, "stage": "Historical Baseline"},
        {"period": "Wk 41 (Dispatch)", "otif": 91.5, "target": 95.0, "stage": "Autonomous Remediation"},
        {"period": "Wk 42 (Projected)", "otif": 96.2, "target": 95.0, "stage": "Target Met"},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "Enterprise On-Time In-Full (OTIF %) Trajectory vs Target (95%)",
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": data},
        "layer": [
            {
                "mark": {"type": "line", "point": {"filled": True, "size": 42}, "strokeWidth": 2.5, "color": "#1a73e8"},
                "encoding": {
                    "x": {"field": "period", "type": "nominal", "axis": {"labelFont": FONT, "labelFontSize": 10, "title": None}},
                    "y": {"field": "otif", "type": "quantitative", "scale": {"domain": [80, 100]}, "axis": {"labelFont": FONT, "labelFontSize": 10, "title": "OTIF %"}},
                    "tooltip": [{"field": "period", "title": "Period"}, {"field": "otif", "title": "OTIF %"}, {"field": "stage", "title": "Stage"}],
                },
            },
            {
                "mark": {"type": "rule", "color": "#188038", "strokeWidth": 1.5, "strokeDash": [4, 4]},
                "encoding": {
                    "y": {"datum": 95.0},
                    "tooltip": [{"value": "SLA Benchmark: 95.0%"}],
                },
            },
        ],
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_composite_control_tower_spec(width: int = 560) -> Dict[str, Any]:
    """Combines network bottleneck bars and OTIF trajectory into an executive infographic."""
    bars = create_bottleneck_impact_bars(width=width, height=190)
    lines = create_otif_trend_line_chart(width=width, height=170)

    clean_bars = {k: v for k, v in bars.items() if k != "$schema"}
    clean_lines = {k: v for k, v in lines.items() if k != "$schema"}

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "TowerMind · CSCO Multi-Echelon Control Tower Cockpit",
            "font": FONT,
            "fontSize": 15,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "vconcat": [clean_bars, clean_lines],
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }
