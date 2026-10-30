"""Self-contained A2UI v0.9 lifecycle builders."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

DEFAULT_GE_CATALOG_ID: str = (
    "https://www.gstatic.com/vertexaisearch/a2ui/v0_9/gemini_enterprise_composite_catalog.json"
)


def build_create_surface(surface_id: str, catalog_id: str = DEFAULT_GE_CATALOG_ID) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    return {
        "message_type": "createSurface",
        "surface_id": surface_id,
        "payload": {"catalogId": catalog_id},
        "catalog_version": "v0.9",
    }


def build_update_components(surface_id: str, components: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    return {
        "message_type": "updateComponents",
        "surface_id": surface_id,
        "payload": {"components": components},
        "catalog_version": "v0.9",
    }


def build_update_data_model(surface_id: str, value: Dict[str, Any], path: Optional[str] = None) -> Dict[str, Any]:
    if not surface_id:
        raise ValueError("surface_id cannot be empty.")
    payload: Dict[str, Any] = {"value": value}
    if path:
        payload["path"] = path
    return {
        "message_type": "updateDataModel",
        "surface_id": surface_id,
        "payload": payload,
        "catalog_version": "v0.9",
    }
