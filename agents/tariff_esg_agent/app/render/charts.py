"""Vega-Lite visual chart generators for ClauseGuard Contract & Trade Compliance Agent."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_tariff_rebate_spec(
    compliance_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an executive Vega-Lite v5 customs duty savings and rebate recovery chart.
    
    Displays:
    - Standard Tariff Duty ($) vs Optimized FTA Preferential Duty ($)
    - Earned Supplier Rebate Recovered ($)
    """
    if not compliance_data:
        compliance_data = [
            {"lane": "Rotterdam -> New York", "category": "Aluminum Beverage Cans", "standard_duty_usd": 68000.0, "optimized_duty_usd": 12000.0, "rebate_recovered_usd": 42000.0},
            {"lane": "Tokyo -> Los Angeles", "category": "Electrolyte Specialty Salts", "standard_duty_usd": 45000.0, "optimized_duty_usd": 0.0, "rebate_recovered_usd": 28500.0},
            {"lane": "Reykjavik -> Houston", "category": "Primary Aluminum Ingot", "standard_duty_usd": 92000.0, "optimized_duty_usd": 18000.0, "rebate_recovered_usd": 55000.0},
            {"lane": "Santos -> Savannah", "category": "Organic Cane Sweeteners", "standard_duty_usd": 38000.0, "optimized_duty_usd": 6500.0, "rebate_recovered_usd": 18000.0}
        ]

    # Transform into unpivoted format for grouped bar chart
    unpivoted = []
    for row in compliance_data:
        unpivoted.append({"lane": row["lane"], "metric": "1. Standard Duty (Unoptimized)", "amount_usd": row["standard_duty_usd"]})
        unpivoted.append({"lane": row["lane"], "metric": "2. Optimized Preferential Duty", "amount_usd": row["optimized_duty_usd"]})
        unpivoted.append({"lane": row["lane"], "metric": "3. Supplier Rebate Recovered", "amount_usd": row["rebate_recovered_usd"]})

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "ClauseGuard Trade Duty Optimization & Supplier Rebate Recovery",
        "width": "container",
        "height": 380,
        "background": "#0b0f19",
        "padding": {"top": 16, "left": 18, "right": 18, "bottom": 16},
        "data": {"values": unpivoted},
        "mark": {"type": "bar", "cornerRadius": 4},
        "encoding": {
            "x": {
                "field": "lane",
                "type": "nominal",
                "axis": {
                    "labelColor": "#cbd5e1",
                    "labelFontSize": 11,
                    "title": "Import Trade Corridor"
                }
            },
            "y": {
                "field": "amount_usd",
                "type": "quantitative",
                "axis": {
                    "gridColor": "#1e293b",
                    "labelColor": "#94a3b8",
                    "title": "Financial Value ($ USD)"
                }
            },
            "color": {
                "field": "metric",
                "type": "nominal",
                "scale": {
                    "domain": [
                        "1. Standard Duty (Unoptimized)",
                        "2. Optimized Preferential Duty",
                        "3. Supplier Rebate Recovered"
                    ],
                    "range": ["#f43f5e", "#38bdf8", "#10b981"]
                },
                "legend": {
                    "orient": "top",
                    "labelColor": "#cbd5e1",
                    "titleColor": "#94a3b8"
                }
            },
            "xOffset": {"field": "metric"},
            "tooltip": [
                {"field": "lane", "type": "nominal", "title": "Trade Lane"},
                {"field": "metric", "type": "nominal", "title": "Audit Metric"},
                {"field": "amount_usd", "type": "quantitative", "title": "Amount ($)"}
            ]
        },
        "config": {
            "view": {"stroke": "transparent"}
        }
    }
