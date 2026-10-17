"""A2UI Protocol Contracts and Message Models for Google ADK & Gemini Enterprise.

Adheres strictly to A2UI v0.9 specification and Google Agent Development Kit patterns.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class A2uiCatalogVersion(str, Enum):
    V0_9 = "v0.9"


@dataclass
class A2uiMessage:
    """Represents a single atomic lifecycle message in the A2UI event stream."""
    message_type: str
    surface_id: str
    payload: Dict[str, Any] = field(default_factory=dict)
    catalog_version: A2uiCatalogVersion = A2uiCatalogVersion.V0_9
