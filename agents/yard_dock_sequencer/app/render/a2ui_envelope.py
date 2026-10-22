"""A2UI message envelope serializer for YardPulse Yard & Dock Orchestrator."""
from __future__ import annotations
import json
from typing import Any, Dict

try:
    from google.genai import types
except ImportError:
    types = None

A2A_DATA_PART_OPEN_TAG: str = "<a2a_datapart_json>"
A2A_DATA_PART_CLOSE_TAG: str = "</a2a_datapart_json>"
A2UI_MIME: str = "application/json+a2ui"


def wrap_a2ui_part(message: Any) -> Any:
    surface_id = getattr(message, "surface_id", None) or message.get("surface_id")
    message_type = getattr(message, "message_type", None) or message.get("message_type")
    payload = getattr(message, "payload", None) or message.get("payload", {})
    catalog_version = getattr(message, "catalog_version", "v0.9")
    version_str = catalog_version.value if hasattr(catalog_version, "value") else str(catalog_version)

    raw_message_body: Dict[str, Any] = {
        "version": version_str,
        message_type: {
            "surfaceId": surface_id,
            **payload,
        },
    }

    payload_envelope: Dict[str, Any] = {
        "kind": "data",
        "metadata": {"mimeType": A2UI_MIME},
        "data": raw_message_body,
    }

    json_str = json.dumps(payload_envelope, separators=(",", ":"))
    wire_payload = (
        f"{A2A_DATA_PART_OPEN_TAG}"
        f"{json_str}"
        f"{A2A_DATA_PART_CLOSE_TAG}"
    ).encode("utf-8")

    if types is not None:
        return types.Part(
            inline_data=types.Blob(
                data=wire_payload,
                mime_type="text/plain",
            ),
            part_metadata={"mimeType": A2UI_MIME},
        )

    return {
        "inline_data": {
            "data": wire_payload.decode("utf-8"),
            "mime_type": "text/plain",
        },
        "part_metadata": {"mimeType": A2UI_MIME},
        "wire_payload": wire_payload.decode("utf-8"),
    }
