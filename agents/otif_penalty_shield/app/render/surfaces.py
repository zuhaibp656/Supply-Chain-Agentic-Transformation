"""A2UI Surface Builder for OTIFShield — Customer SLA Rescue & Chargeback Dispute Agent."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
    build_update_data_model,
)
from .charts import create_otif_penalty_shield_chart_spec


def build_otif_penalty_shield_surface(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 340,
) -> List[Any]:
    """Renders ONLY the visual VegaChart inside the Card component, keeping markdown tables outside."""
    chart_spec = spec or create_otif_penalty_shield_chart_spec()

    parts = [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_data_model(surface_id, {"spec": chart_spec})),
        wrap_a2ui_part(build_update_components(
            surface_id,
            [
                {
                    "id": "root",
                    "component": "Card",
                    "child": "chart-wrapper",
                },
                {
                    "id": "chart-wrapper",
                    "component": "VegaChart",
                    "spec": chart_spec,
                    "height": height,
                },
            ]
        )),
    ]
    return parts


def build_interactive_html_surface(
    surface_id: str,
    html_content: str,
    title: str = "Interactive Cockpit",
    height: int = 720,
) -> list[Any]:
    """Renders a self-contained interactive web application inside an A2UI IFrameSrcdoc Card."""
    parts = [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_data_model(surface_id, {"title": title})),
        wrap_a2ui_part(build_update_components(
            surface_id,
            [
                {
                    "id": "root",
                    "component": "Card",
                    "child": "iframe-view",
                },
                {
                    "id": "iframe-view",
                    "component": "IFrameSrcdoc",
                    "height": height,
                    "htmlContent": html_content,
                    "title": title,
                },
            ]
        )),
    ]
    return parts
