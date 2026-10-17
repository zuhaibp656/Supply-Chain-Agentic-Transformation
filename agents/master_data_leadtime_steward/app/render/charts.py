"""Deterministic Vega-Lite Chart Specs for Master Data Lead Time Steward."""
from __future__ import annotations
from typing import Any, Dict, List, Optional

FONT = "Google Sans, Roboto, Arial, sans-serif"


def create_leadtime_drift_diverging_bars(width: int = 560, height: int = 210) -> Dict[str, Any]:
    """Generates a diverging bar chart comparing planned vs actual transit lead-time drift in days."""
    data = [
        {"material": "MAT-880019 (HV Inverter SiC)", "drift_days": 25, "planned": 21, "actual": 46},
        {"material": "MAT-901140 (Cavitating Valve)", "drift_days": 34, "planned": 14, "actual": 48},
        {"material": "MAT-440212 (LFP Battery Cell)", "drift_days": 3, "planned": 35, "actual": 38},
        {"material": "MAT-102944 (Hydraulic Seal Ring)", "drift_days": -2, "planned": 10, "actual": 8},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "SAP Lead-Time Drift · Historical Transit vs Planned MARA/MARC Days",
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
                "field": "material",
                "type": "nominal",
                "sort": "-x",
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": None, "domain": False},
            },
            "x": {
                "field": "drift_days",
                "type": "quantitative",
                "axis": {"labelFont": FONT, "labelFontSize": 11, "title": "Lead-Time Drift (Days)", "grid": True},
            },
            "color": {
                "condition": {
                    "test": "datum.drift_days > 7",
                    "value": "#d93025",  # Critical drift
                },
                "value": "#188038",      # Nominal or acceptable
            },
            "tooltip": [
                {"field": "material", "type": "nominal", "title": "Material"},
                {"field": "drift_days", "type": "quantitative", "title": "Drift (Days)"},
                {"field": "planned", "type": "quantitative", "title": "Planned Days"},
                {"field": "actual", "type": "quantitative", "title": "Actual Days"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_dimension_audit_donut(width: int = 560, height: int = 190) -> Dict[str, Any]:
    """Generates a donut chart of Master Data auto-remediations by category."""
    data = [
        {"category": "Transit Lead-Time Recalibration", "count": 14, "capital_freed_m": 2.4},
        {"category": "CubiScan 3D Laser Dimension Sync", "count": 9, "capital_freed_m": 0.9},
        {"category": "Safety Stock Float Compression", "count": 6, "capital_freed_m": 0.5},
    ]
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "Master Data Self-Healing Breakdown ($3.8M Excess Buffer Freed)",
            "font": FONT,
            "fontSize": 14,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "width": width,
        "height": height,
        "data": {"values": data},
        "mark": {"type": "arc", "innerRadius": 50, "stroke": "#ffffff", "strokeWidth": 2},
        "encoding": {
            "theta": {"field": "capital_freed_m", "type": "quantitative"},
            "color": {
                "field": "category",
                "type": "nominal",
                "scale": {"range": ["#1a73e8", "#f9ab00", "#188038"]},
                "legend": {
                    "orient": "right",
                    "labelFont": FONT,
                    "labelFontSize": 11,
                    "title": None,
                },
            },
            "tooltip": [
                {"field": "category", "type": "nominal", "title": "Remediation Category"},
                {"field": "count", "type": "quantitative", "title": "SKUs Remediated"},
                {"field": "capital_freed_m", "type": "quantitative", "title": "Working Capital Freed ($M)"},
            ],
        },
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }


def create_composite_master_data_spec(width: int = 560) -> Dict[str, Any]:
    """Combines lead time drift bars and remediation donut chart into an infographic."""
    bars = create_leadtime_drift_diverging_bars(width=width, height=190)
    donut = create_dimension_audit_donut(width=width, height=170)

    clean_bars = {k: v for k, v in bars.items() if k != "$schema"}
    clean_donut = {k: v for k, v in donut.items() if k != "$schema"}

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": "DataCleanse · Master Data Self-Healing Lead Time & Volume Cockpit",
            "font": FONT,
            "fontSize": 15,
            "fontWeight": "bold",
            "anchor": "start",
            "color": "#202124",
        },
        "vconcat": [clean_bars, clean_donut],
        "config": {"view": {"stroke": None}, "background": "#ffffff"},
    }
