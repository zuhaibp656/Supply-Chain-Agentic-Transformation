"""A2UI Surface Builders for Google ADK & Gemini Enterprise.

Rule from User Directives:
In A2UI / Gemini Enterprise agent responses, render ONLY the visual image or
interactive infographic inside the card rendering (VegaChart), and keep all text,
atomic copy-ready tables (for copying to Google Sheets), and properly headed links
(with clear ### headings and vertical spacing) outside in the main Markdown response.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional

try:
    from .envelope import wrap_a2ui_part
    from .lifecycle import (
        build_create_surface,
        build_update_components,
        build_update_data_model,
    )
except ImportError:
    from envelope import wrap_a2ui_part
    from lifecycle import (
        build_create_surface,
        build_update_components,
        build_update_data_model,
    )


def build_card_chart_surface(
    surface_id: str,
    vega_spec: Dict[str, Any],
    height: int = 380,
    data_model: Optional[Dict[str, Any]] = None,
) -> List[Any]:
    """Constructs the A2UI wire parts for a visual Card containing a VegaChart."""
    parts = [wrap_a2ui_part(build_create_surface(surface_id))]

    if data_model is not None:
        parts.append(wrap_a2ui_part(build_update_data_model(surface_id, data_model)))

    components: List[Dict[str, Any]] = [
        {
            "id": "root",
            "component": "Card",
            "child": "chart-wrapper",
        },
        {
            "id": "chart-wrapper",
            "component": "VegaChart",
            "spec": vega_spec,
            "height": height,
        },
    ]

    parts.append(wrap_a2ui_part(build_update_components(surface_id, components)))
    return parts
