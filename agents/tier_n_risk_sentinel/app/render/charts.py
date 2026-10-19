"""Vega-Lite visual chart generators for NexusShield Multi-Tier Network Sentinel."""
from __future__ import annotations
from typing import Any, Dict, List, Optional


def create_tier_risk_radar_spec(
    network_data: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Generates an executive Vega-Lite v5 multi-tier supply network risk radar chart.
    
    Plots Tier-1 through Tier-4 supply nodes by:
    - X-Axis: Tier Level (Tier 1 -> Tier 4)
    - Y-Axis: Revenue at Risk ($M)
    - Size: Lead-Time Delay (Days)
    - Color: Disruption Severity / Chokepoint Risk
    """
    if not network_data:
        network_data = [
            {"tier": "Tier-1 Assembly", "node_id": "Ball Metal Packaging", "country": "US", "revenue_at_risk_m": 4.5, "lead_time_days": 18, "risk_level": "MODERATE", "chokepoint": False},
            {"tier": "Tier-1 Assembly", "node_id": "Crown Holdings", "country": "US", "revenue_at_risk_m": 2.1, "lead_time_days": 21, "risk_level": "LOW", "chokepoint": False},
            {"tier": "Tier-2 Smelting", "node_id": "Alcoa Int. Smelter", "country": "IS", "revenue_at_risk_m": 8.2, "lead_time_days": 35, "risk_level": "HIGH", "chokepoint": False},
            {"tier": "Tier-2 Smelting", "node_id": "Hydro Aluminium", "country": "NO", "revenue_at_risk_m": 3.8, "lead_time_days": 28, "risk_level": "LOW", "chokepoint": False},
            {"tier": "Tier-3 Refining", "node_id": "Bauxite Refining Hub", "country": "AU", "revenue_at_risk_m": 14.6, "lead_time_days": 48, "risk_level": "CRITICAL_CHOKEPOINT", "chokepoint": True},
            {"tier": "Tier-4 Mining", "node_id": "Weipa Bauxite Mine", "country": "AU", "revenue_at_risk_m": 18.4, "lead_time_days": 65, "risk_level": "CRITICAL_CHOKEPOINT", "chokepoint": True},
            {"tier": "Tier-2 Chem Precursor", "node_id": "Sumitomo Electrolyte", "country": "JP", "revenue_at_risk_m": 6.4, "lead_time_days": 42, "risk_level": "HIGH", "chokepoint": True},
            {"tier": "Tier-3 Specialty Salt", "node_id": "Showa Denko Chemical", "country": "JP", "revenue_at_risk_m": 9.8, "lead_time_days": 55, "risk_level": "CRITICAL_CHOKEPOINT", "chokepoint": True}
        ]

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "NexusShield Multi-Tier Supply Network Revenue at Risk Radar",
        "width": "container",
        "height": 380,
        "background": "#0b0f19",
        "padding": {"top": 16, "left": 18, "right": 18, "bottom": 16},
        "data": {"values": network_data},
        "mark": {
            "type": "circle",
            "opacity": 0.85,
            "stroke": "#ffffff",
            "strokeWidth": 1.2
        },
        "encoding": {
            "x": {
                "field": "tier",
                "type": "nominal",
                "axis": {
                    "labelColor": "#cbd5e1",
                    "labelFontSize": 11,
                    "title": "Supply Network Echelon Depth"
                }
            },
            "y": {
                "field": "revenue_at_risk_m",
                "type": "quantitative",
                "axis": {
                    "gridColor": "#1e293b",
                    "labelColor": "#94a3b8",
                    "title": "Revenue at Risk ($ Millions USD)"
                }
            },
            "size": {
                "field": "lead_time_days",
                "type": "quantitative",
                "scale": {"range": [80, 500]},
                "legend": {
                    "title": "Lead-Time (Days)",
                    "labelColor": "#cbd5e1",
                    "titleColor": "#94a3b8"
                }
            },
            "color": {
                "field": "risk_level",
                "type": "nominal",
                "scale": {
                    "domain": ["LOW", "MODERATE", "HIGH", "CRITICAL_CHOKEPOINT"],
                    "range": ["#10b981", "#38bdf8", "#f59e0b", "#f43f5e"]
                },
                "legend": {
                    "title": "Vulnerability Tier",
                    "labelColor": "#cbd5e1",
                    "titleColor": "#94a3b8"
                }
            },
            "tooltip": [
                {"field": "node_id", "type": "nominal", "title": "Supplier Node"},
                {"field": "tier", "type": "nominal", "title": "Echelon"},
                {"field": "country", "type": "nominal", "title": "Geography"},
                {"field": "revenue_at_risk_m", "type": "quantitative", "title": "Revenue at Risk ($M)"},
                {"field": "lead_time_days", "type": "quantitative", "title": "Lead Time (Days)"},
                {"field": "risk_level", "type": "nominal", "title": "Severity"}
            ]
        },
        "config": {
            "view": {"stroke": "transparent"}
        }
    }
