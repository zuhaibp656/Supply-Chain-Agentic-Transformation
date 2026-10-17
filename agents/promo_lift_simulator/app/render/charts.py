"""Vega-Lite visual chart generators for ElasticityIQ Promo Simulator."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_promo_elasticity_spec(
    promo_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an executive Vega-Lite v5 causal promotional lift and cannibalization decomposition chart.
    
    Decomposes:
    - Gross Promotional Lift (+)
    - Sister-SKU Cannibalization (-)
    - Post-Promo Pull-Forward Dip (-)
    - Net Incremental Margin ($)
    """
    if not promo_data:
        promo_data = [
            {"campaign": "BOGO Hydration Blitz", "component": "Gross Promo Lift", "volume_units": 85000, "impact_usd": 170000.0, "type": "POSITIVE"},
            {"campaign": "BOGO Hydration Blitz", "component": "Cannibalization Loss", "volume_units": -26000, "impact_usd": -65000.0, "type": "NEGATIVE"},
            {"campaign": "BOGO Hydration Blitz", "component": "Post-Promo Trough", "volume_units": -11000, "impact_usd": -22000.0, "type": "NEGATIVE"},
            {"campaign": "BOGO Hydration Blitz", "component": "Net Incremental Gain", "volume_units": 48000, "impact_usd": 83000.0, "type": "NET"},

            {"campaign": "20% Off Protein Snack Pack", "component": "Gross Promo Lift", "volume_units": 42000, "impact_usd": 105000.0, "type": "POSITIVE"},
            {"campaign": "20% Off Protein Snack Pack", "component": "Cannibalization Loss", "volume_units": -8500, "impact_usd": -25500.0, "type": "NEGATIVE"},
            {"campaign": "20% Off Protein Snack Pack", "component": "Post-Promo Trough", "volume_units": -4500, "impact_usd": -11250.0, "type": "NEGATIVE"},
            {"campaign": "20% Off Protein Snack Pack", "component": "Net Incremental Gain", "volume_units": 29000, "impact_usd": 68250.0, "type": "NET"},

            {"campaign": "Bundle & Save Electrolytes", "component": "Gross Promo Lift", "volume_units": 31000, "impact_usd": 93000.0, "type": "POSITIVE"},
            {"campaign": "Bundle & Save Electrolytes", "component": "Cannibalization Loss", "volume_units": -4200, "impact_usd": -14700.0, "type": "NEGATIVE"},
            {"campaign": "Bundle & Save Electrolytes", "component": "Post-Promo Trough", "volume_units": -2800, "impact_usd": -8400.0, "type": "NEGATIVE"},
            {"campaign": "Bundle & Save Electrolytes", "component": "Net Incremental Gain", "volume_units": 24000, "impact_usd": 69900.0, "type": "NET"}
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "ElasticityIQ Causal Promotional Lift vs Cannibalization Matrix",
        "width": "container",
        "height": 380,
        "background": "#0b0f19",
        "padding": {"top": 16, "left": 18, "right": 18, "bottom": 16},
        "data": {"values": promo_data},
        "mark": {"type": "bar", "cornerRadius": 4},
        "encoding": {
            "x": {
                "field": "campaign",
                "type": "nominal",
                "axis": {
                    "labelColor": "#cbd5e1",
                    "labelFontSize": 11,
                    "title": None
                }
            },
            "y": {
                "field": "impact_usd",
                "type": "quantitative",
                "axis": {
                    "gridColor": "#1e293b",
                    "labelColor": "#94a3b8",
                    "title": "Net Economic Impact ($ USD)"
                }
            },
            "color": {
                "field": "component",
                "type": "nominal",
                "scale": {
                    "domain": [
                        "Gross Promo Lift",
                        "Cannibalization Loss",
                        "Post-Promo Trough",
                        "Net Incremental Gain"
                    ],
                    "range": ["#38bdf8", "#f43f5e", "#fb923c", "#10b981"]
                },
                "legend": {
                    "orient": "top",
                    "labelColor": "#cbd5e1",
                    "titleColor": "#94a3b8"
                }
            },
            "xOffset": {"field": "component"},
            "tooltip": [
                {"field": "campaign", "type": "nominal", "title": "Campaign"},
                {"field": "component", "type": "nominal", "title": "Component"},
                {"field": "volume_units", "type": "quantitative", "title": "Volume (Units)"},
                {"field": "impact_usd", "type": "quantitative", "title": "Dollar Impact ($)"}
            ]
        },
        "config": {
            "view": {"stroke": "transparent"}
        }
    }
