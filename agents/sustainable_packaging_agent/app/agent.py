"""Google ADK Agent for [02 · Source | Material & Packaging] Sustainable Packaging Agent (02 · Sourcing & Procurement — Material & Packaging)."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .render.charts import create_sustainable_packaging_agent_chart_spec
from .render.surfaces import build_sustainable_packaging_agent_surface
from .tools import (
    ALL_TOOLS,
    SYSTEM_CONNECTORS,
    query_sustainable_packaging_agent_telemetry_feed,
    query_sustainable_packaging_agent_constraint_matrix,
    query_sustainable_packaging_agent_optimization_scenarios,
    query_sustainable_packaging_agent_execution_ledger,
    action_commit_sustainable_packaging_agent_plan,
    action_dispatch_sustainable_packaging_agent_alert,
)

AGENT_ID = "sustainable_packaging_agent"
AGENT_CATEGORY = "02 · Sourcing & Procurement — Material & Packaging"
AGENT_DISPLAY_NAME = "[02 · Source | Material & Packaging] Sustainable Packaging Agent"
AGENT_DESCRIPTION = "[Category: 02 · Sourcing & Procurement — Material & Packaging] Sustainable Packaging Agent (Packaging R&D Engineer): Evaluates PCR resins and barrier materials against line runnability & taxes. Outcome: Mitigates EPR and landfill taxation."

INSTRUCTION = """You are [02 · Source | Material & Packaging] Sustainable Packaging Agent.
Category: 02 · Sourcing & Procurement — Material & Packaging
Primary Persona Owner: Packaging R&D Engineer
Mission: [Category: 02 · Sourcing & Procurement — Material & Packaging] Sustainable Packaging Agent (Packaging R&D Engineer): Evaluates PCR resins and barrier materials against line runnability & taxes. Outcome: Mitigates EPR and landfill taxation.

Always ground your analysis in the deterministic enterprise tools, enforce pre-execution quality gates, and return concise executive tables paired with the interactive A2UI VegaChart surface.
"""


class SustainablePackagingAgentAgent:
    """Deterministic & ADK execution wrapper for [02 · Source | Material & Packaging] Sustainable Packaging Agent."""

    def __init__(self, model: str = "gemini-3.1-pro-preview") -> None:
        self.name = "sustainable_packaging_agent"
        self.category = AGENT_CATEGORY
        self.display_name = AGENT_DISPLAY_NAME
        self.description = AGENT_DESCRIPTION
        self.model = model
        self.tools = list(ALL_TOOLS)
        self.system_connectors = list(SYSTEM_CONNECTORS)

    def select_orchestrated_model(self, query: str = "") -> Dict[str, str]:
        """Agent Orchestrator dynamically decides whether to use Gemini 3.8 Flash or Gemini 3.1 Pro / 4 Argon."""
        q_lower = (query or "").lower()
        needs_pro_or_argon = any(
            k in q_lower
            for k in ("scenario", "multi-echelon", "war room", "redline", "capex", "trade-off", "optimize", "simulate", "optimization")
        )
        selected = "gemini-3.1-pro / gemini-4-argon (subject to availability)" if needs_pro_or_argon else "gemini-3.8-flash"
        return {
            "orchestrator_policy": "Dynamic Agent Orchestrator Routing (Gemini 3.8 Flash <-> Gemini 3.1 Pro / 4 Argon subject to availability)",
            "selected_model": selected,
            "fast_model": "gemini-3.8-flash",
            "pro_argon_model": "gemini-3.1-pro / gemini-4-argon (subject to availability)",
            "eval_judge_model": "gemini-4-argon (fallback: gemini-3.1-pro, subject to availability)",
        }

    def run_scenario(self, prompt: str = "Execute end-to-end optimization") -> Dict[str, Any]:
        t0 = query_sustainable_packaging_agent_telemetry_feed()
        t1 = query_sustainable_packaging_agent_constraint_matrix()
        t2 = query_sustainable_packaging_agent_optimization_scenarios()
        t3 = query_sustainable_packaging_agent_execution_ledger()
        mut = action_commit_sustainable_packaging_agent_plan()
        alert = action_dispatch_sustainable_packaging_agent_alert()

        rows0 = t0.get("rows", [])
        table_lines = [
            "#### 📊 [02 · Source | Material & Packaging] Sustainable Packaging Agent — Verified Enterprise Telemetry",
            "",
            "| Record ID | Facility | SKU | Baseline | Optimized | Status |",
            "| :--- | :--- | :--- | ---: | ---: | :--- |",
        ]
        for r in rows0[:4]:
            table_lines.append(
                f"| `{r.get('record_id')}` | `{r.get('facility_id')}` | `{r.get('sku_id')}` | "
                f"{r.get('baseline_metric')}% | **{r.get('optimized_metric')}%** | `{r.get('status')}` |"
            )
        table_lines.extend([
            "",
            f"**Category**: `02 · Sourcing & Procurement — Material & Packaging` · **Persona**: `Packaging R&D Engineer` · "
            f"**Write-Back Receipt**: `{mut.get('action_id')}` (`{mut.get('status')}`)",
        ])
        md = "\n".join(table_lines)

        surface_id = f"sustainable--live"
        a2ui_parts = build_sustainable_packaging_agent_surface(surface_id, spec=create_sustainable_packaging_agent_chart_spec())

        return {
            "status": "SUCCESS",
            "agent": self.name,
            "display_name": self.display_name,
            "category": self.category,
            "description": self.description,
            "model": self.model,
            "orchestrator_routing": self.select_orchestrated_model(prompt),
            "prompt": prompt,
            "telemetry": t0,
            "constraints": t1,
            "scenarios": t2,
            "ledger": t3,
            "mutation_receipt": mut,
            "alert_receipt": alert,
            "actions_taken": [mut, alert],
            "markdown": md,
            "markdown_response": md,
            "a2ui_surface": a2ui_parts,
        }


# ==============================================================================
# Google ADK & Vertex AI Reasoning Engine Integration
# ==============================================================================
try:
    import os
    import uuid
    from functools import cached_property
    from google.adk.agents import Agent
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.apps import App
    from google.adk.models import Gemini
    from google.adk.models.llm_request import LlmRequest
    from google.adk.models.llm_response import LlmResponse
    from google.genai import Client, types
    from vertexai.preview.reasoning_engines import AdkApp
    from .render.a2ui_envelope import A2A_DATA_PART_OPEN_TAG

    class GlobalGemini(Gemini):
        """Routes Gemini 3.8 Flash and Gemini 3.1 Pro / 4 Argon (subject to availability) calls to the global Vertex AI endpoint even when the Reasoning Engine runs in us-central1."""

        @cached_property
        def api_client(self) -> Client:
            return Client(
                vertexai=True,
                project=os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai"),
                location="global",
                http_options=types.HttpOptions(
                    headers=self._tracking_headers(),
                    retry_options=self.retry_options,
                ),
            )

    def _sanitize_llm_request(
        callback_context: Optional[CallbackContext] = None,
        llm_request: Optional[LlmRequest] = None,
        **_: Any,
    ) -> None:
        if llm_request is None or not llm_request.contents:
            return None
        for content in llm_request.contents:
            if not content.parts:
                continue
            cleaned: List[types.Part] = []
            for part in content.parts:
                if getattr(part, "inline_data", None) is not None:
                    continue
                t = getattr(part, "text", None)
                if t and A2A_DATA_PART_OPEN_TAG in t:
                    continue
                cleaned.append(part)
            content.parts = cleaned or [types.Part(text="[Visual Chart Surface Rendered in UI]")]
        return None

    def _append_verified_report(
        callback_context: Optional[CallbackContext] = None,
        llm_response: Optional[LlmResponse] = None,
        **_: Any,
    ) -> Optional[LlmResponse]:
        if llm_response is None or llm_response.content is None:
            return None
        parts = llm_response.content.parts or []
        has_call = any(getattr(p, "function_call", None) is not None for p in parts)
        if has_call:
            return llm_response
        try:
            scenario = SustainablePackagingAgentAgent().run_scenario("live_turn")
            report_md = scenario.get("markdown", "")
            if report_md:
                idx = max((i for i, p in enumerate(parts) if getattr(p, "text", None)), default=-1)
                if idx >= 0:
                    existing = (parts[idx].text or "").strip()
                    if "#### 📊" not in existing:
                        parts[idx] = types.Part(text=f"{existing}\n\n---\n\n{report_md}")
                else:
                    parts.append(types.Part(text=report_md))
            llm_response.content.parts = parts
        except Exception:
            pass
        return llm_response

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            surface_id = f"sustainable--{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_sustainable_packaging_agent_surface(surface_id, spec=create_sustainable_packaging_agent_chart_spec())
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="sustainable_packaging_agent",
        description=AGENT_DESCRIPTION,
        model=GlobalGemini(
            model="gemini-3.1-pro-preview",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.2,
        ),
        instruction=INSTRUCTION,
        tools=ALL_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_model_callback=_append_verified_report,
        after_agent_callback=_emit_a2ui_surface,
    )

    adk_app = App(name="sustainable_packaging_agent_app", root_agent=root_agent)

    class SustainablePackagingAgentAdkApp(AdkApp):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(agent=root_agent, **kwargs)

        def query(self, *args: Any, **kwargs: Any) -> Any:
            return super().query(*args, **kwargs)

        def stream_query(self, *args: Any, **kwargs: Any) -> Any:
            yield from super().stream_query(*args, **kwargs)

except Exception:
    root_agent = SustainablePackagingAgentAgent()  # type: ignore
    adk_app = None

    class SustainablePackagingAgentAdkApp:  # type: ignore
        pass
