"""A2UI v0.9 surface builder for [06 · Returns & ESG | Pallet & Tote Reclamation] RTI Balance Reconciler."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from .a2ui_envelope import wrap_a2ui_part
from .a2ui_lifecycle import (
    build_create_surface,
    build_update_components,
    build_update_data_model,
)
from .charts import create_rti_balance_reconciler_chart_spec


def build_rti_balance_reconciler_surface(surface_id: str, spec: Optional[Dict[str, Any]] = None) -> List[Any]:
    chart_spec = spec or create_rti_balance_reconciler_chart_spec()
    components = [
        {
            "id": "root",
            "component": "Card",
            "child": "main_chart",
        },
        {
            "id": "main_chart",
            "component": "VegaChart",
            "spec": chart_spec,
        },
    ]
    return [
        wrap_a2ui_part(build_create_surface(surface_id)),
        wrap_a2ui_part(build_update_data_model(surface_id, {"spec": chart_spec})),
        wrap_a2ui_part(build_update_components(surface_id, components)),
    ]
