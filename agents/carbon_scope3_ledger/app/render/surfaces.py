"""A2UI v0.9 Dual-Surface Builder for ESG & Scope 3 Auditor.

Emits:
1. Surface 1 (Inline Chat `Card`): Strictly renders ONLY the commensurate 2-Panel Executive `VegaChart` Infographic.
2. Surface 2 (Side-Panel `Canvas`): FleetFlow-grade Visual Studio containing 2 interactive `VegaChart`s
   (Horizontal Multi-Metric Performance Index + Ranked Pareto Concentration Breakdown),
   Quick-Action Scenario `MaterialButton`s, and a live Looker Studio `RichTable` (zero text-audit boxes).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from .a2ui_builder import (
        build_explorer_canvas_parts,
        build_inline_vegachart_card_parts,
        enrich_to_executive_2panel_vegalite,
    )
    from .charts import create_carbon_scope3_ledger_chart_spec
except ImportError:
    from a2ui_builder import (  # type: ignore
        build_explorer_canvas_parts,
        build_inline_vegachart_card_parts,
        enrich_to_executive_2panel_vegalite,
    )
    from charts import create_carbon_scope3_ledger_chart_spec  # type: ignore


def build_carbon_scope3_ledger_surface(
    surface_id: str,
    spec: Optional[Dict[str, Any]] = None,
    height: int = 440,
    canvas_context: Optional[Dict[str, Any]] = None,
    include_canvas: bool = True,
) -> List[Any]:
    """Builds validated A2UI v0.9 Parts: Inline `VegaChart` Card + Visual Multi-Chart `Canvas` Studio."""
    live_rows = (canvas_context or {}).get("rows") if isinstance(canvas_context, dict) else None
    rich_spec = enrich_to_executive_2panel_vegalite(
        spec=spec,
        fallback_fn=create_carbon_scope3_ledger_chart_spec,
        agent_title='ESG & Scope 3 Auditor',
        live_rows=live_rows,
    )
    parts = list(build_inline_vegachart_card_parts(surface_id, rich_spec, height=max(430, int(height))))

    if include_canvas and isinstance(canvas_context, dict) and canvas_context.get("rows"):
        canvas_sid = f"canvas-{surface_id[-8:]}"
        canvas_parts = build_explorer_canvas_parts(
            canvas_surface_id=canvas_sid,
            agent_id='carbon_scope3_ledger',
            agent_short_label='ESG & Scope 3 Auditor',
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
    height: int = 440,
) -> List[Any]:
    """Compatibility shim: Gemini Enterprise inline Cards strictly render VegaChart visuals."""
    return build_carbon_scope3_ledger_surface(surface_id, spec=None, height=height, include_canvas=False)
