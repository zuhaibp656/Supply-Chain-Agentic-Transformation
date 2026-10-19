"""Vega-Lite visual chart generators for SourcePulse Parametric Should-Cost Agent."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_should_cost_spec(
    cost_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an executive Vega-Lite v5 stacked cost breakdown comparison chart.
    
    Compares bottom-up Parametric Should-Cost vs. actual supplier RFQ bid proposals
    across Raw Material, Machine Processing, Direct Labor, Landed Freight, and SG&A/Margin.
    """
    if not cost_data:
        cost_data = [
            {"source": "1. Parametric Should-Cost", "cost_component": "Raw Material", "cost_usd": 14.20},
            {"source": "1. Parametric Should-Cost", "cost_component": "Machine Processing", "cost_usd": 6.80},
            {"source": "1. Parametric Should-Cost", "cost_component": "Direct Labor", "cost_usd": 3.40},
            {"source": "1. Parametric Should-Cost", "cost_component": "Landed Logistics", "cost_usd": 2.10},
            {"source": "1. Parametric Should-Cost", "cost_component": "SG&A & Margin", "cost_usd": 3.10},

            {"source": "2. Supplier A (Ball Corp)", "cost_component": "Raw Material", "cost_usd": 14.50},
            {"source": "2. Supplier A (Ball Corp)", "cost_component": "Machine Processing", "cost_usd": 7.10},
            {"source": "2. Supplier A (Ball Corp)", "cost_component": "Direct Labor", "cost_usd": 3.60},
            {"source": "2. Supplier A (Ball Corp)", "cost_component": "Landed Logistics", "cost_usd": 2.20},
            {"source": "2. Supplier A (Ball Corp)", "cost_component": "SG&A & Margin", "cost_usd": 3.80},

            {"source": "3. Supplier B (Crown)", "cost_component": "Raw Material", "cost_usd": 14.80},
            {"source": "3. Supplier B (Crown)", "cost_component": "Machine Processing", "cost_usd": 7.40},
            {"source": "3. Supplier B (Crown)", "cost_component": "Direct Labor", "cost_usd": 3.80},
            {"source": "3. Supplier B (Crown)", "cost_component": "Landed Logistics", "cost_usd": 2.40},
            {"source": "3. Supplier B (Crown)", "cost_component": "SG&A & Margin", "cost_usd": 4.20},

            {"source": "4. Supplier C (Ardagh)", "cost_component": "Raw Material", "cost_usd": 15.60},
            {"source": "4. Supplier C (Ardagh)", "cost_component": "Machine Processing", "cost_usd": 8.90},
            {"source": "4. Supplier C (Ardagh)", "cost_component": "Direct Labor", "cost_usd": 4.50},
            {"source": "4. Supplier C (Ardagh)", "cost_component": "Landed Logistics", "cost_usd": 3.20},
            {"source": "4. Supplier C (Ardagh)", "cost_component": "SG&A & Margin", "cost_usd": 6.80}
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "SourcePulse Parametric Should-Cost vs Supplier RFQ Bid Breakdown",
        "width": "container",
        "height": 380,
        "background": "#0b0f19",
        "padding": {"top": 16, "left": 18, "right": 18, "bottom": 16},
        "data": {"values": cost_data},
        "mark": {"type": "bar", "cornerRadiusTop": 4},
        "encoding": {
            "x": {
                "field": "source",
                "type": "nominal",
                "axis": {
                    "labelColor": "#cbd5e1",
                    "labelFontSize": 11,
                    "title": None
                }
            },
            "y": {
                "field": "cost_usd",
                "type": "quantitative",
                "axis": {
                    "gridColor": "#1e293b",
                    "labelColor": "#94a3b8",
                    "title": "Unit Cost ($ USD / Unit)"
                }
            },
            "color": {
                "field": "cost_component",
                "type": "nominal",
                "scale": {
                    "domain": [
                        "Raw Material",
                        "Machine Processing",
                        "Direct Labor",
                        "Landed Logistics",
                        "SG&A & Margin"
                    ],
                    "range": ["#38bdf8", "#818cf8", "#34d399", "#fbbf24", "#f43f5e"]
                },
                "legend": {
                    "orient": "top",
                    "labelColor": "#cbd5e1",
                    "titleColor": "#94a3b8"
                }
            },
            "tooltip": [
                {"field": "source", "type": "nominal", "title": "Source / Vendor"},
                {"field": "cost_component", "type": "nominal", "title": "Cost Component"},
                {"field": "cost_usd", "type": "quantitative", "title": "Unit Cost ($)"}
            ]
        },
        "config": {
            "view": {"stroke": "transparent"}
        }
    }
