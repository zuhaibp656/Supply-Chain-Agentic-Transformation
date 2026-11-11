"""A2UI v0.9 Dual-Surface Builder for Store Capacity Agent.

Emits:
1. Inline Chat `Card` containing strictly the 2-Panel Executive `VegaChart` Infographic.
2. Optional Side-Panel `Canvas` (`autoOpen=False`) containing interactive `MaterialButton`
   actions, `MaterialExpansionPanel` solver & data-source cards, and a Looker Studio `RichTable`.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from .a2ui_builder import (
        build_explorer_canvas_parts,
        build_inline_vegachart_card_parts,
        enrich_to_executive_2panel_vegalite,
    )
    from .charts import create_store_capacity_agent_chart_spec
except ImportError:
    from a2ui_builder import (  # type: ignore
        build_explorer_canvas_parts,
        build_inline_vegachart_card_parts,
        enrich_to_executive_2panel_vegalite,
    )
    from charts import create_store_capacity_agent_chart_spec  # type: ignore


def build_store_capacity_agent_surface(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 430,
    canvas_context: Optional[Dict[str, Any]] = None,
    include_canvas: bool = True,
) -> List[Any]:
    """Builds validated A2UI v0.9 Parts: Inline `VegaChart` Card + Side-Panel `Canvas` Explorer."""
    rich_spec = enrich_to_executive_2panel_vegalite(
        spec=spec,
        fallback_fn=create_store_capacity_agent_chart_spec,
        agent_title='Store Capacity Agent',
    )
    parts = list(build_inline_vegachart_card_parts(surface_id, rich_spec, height=max(420, int(height))))

    if include_canvas and isinstance(canvas_context, dict) and canvas_context.get("rows"):
        canvas_sid = f"canvas-{surface_id[-8:]}"
        canvas_parts = build_explorer_canvas_parts(
            canvas_surface_id=canvas_sid,
            agent_id='store_capacity_agent',
            agent_short_label='Store Capacity',
            systems=canvas_context.get("systems") or [],
            source_table_name=str(canvas_context.get("source_table") or "enterprise_records"),
            table_rows=canvas_context.get("rows") or [],
            kpi_summary=canvas_context.get("kpi_summary"),
            writeback_summary=str(canvas_context.get("writeback_summary") or ""),
        )
        parts.extend(canvas_parts)
    return parts


def build_interactive_html_surface(
    surface_id: str,
    html_content: str,
    title: str = "Interactive Cockpit",
    height: int = 430,
) -> List[Any]:
    """Compatibility shim: Gemini Enterprise inline Cards strictly render VegaChart visuals."""
    return build_store_capacity_agent_surface(surface_id, spec=None, height=height, include_canvas=False)
