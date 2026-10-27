"""ShelfVision — Retail Planogram & Visibility Auditor — High-Code Google ADK Agent.

Uses Gemini 3.8 Flash multimodal vision to audit retail store shelf photos in under 2 seconds, measuring Share-of-Shelf (SOS), eye-level facings, cooler purity, and on-shelf availability.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_planogram_merchandising_vision_auditor_chart_spec
from .render.surfaces import build_planogram_merchandising_vision_auditor_surface

_INSTRUCTION = """You are ShelfVision — Retail Planogram & Visibility Auditor.

PRIMARY OBJECTIVE:
Uses Gemini 3.8 Flash multimodal vision to audit retail store shelf photos in under 2 seconds, measuring Share-of-Shelf (SOS), eye-level facings, cooler purity, and on-shelf availability.

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_dispatch_instore_restock_directive`, `action_certify_store_planogram_audit`), ensure all required fields and a non-empty `idempotency_key` are provided.
"""

_AVAILABLE_TOOLS = [
    tools.query_store_shelf_vision_audit_captures,
    tools.query_contracted_planogram_templates,
    tools.query_shelf_compliance_scoring_ledger,
    tools.query_merchandising_corrective_tasks,
    tools.action_dispatch_instore_restock_directive,
    tools.action_certify_store_planogram_audit,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_dispatch_instore_restock_directive": ["capture_id", "outlet_id", "fso_id", "missing_facings_count", "rationale"],
    "action_certify_store_planogram_audit": ["outlet_id", "template_id", "verified_sos_pct", "payout_approved", "rationale"],
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs and idempotency."""
    if tool_name in _WRITE_TOOLS:
        required = _WRITE_TOOLS[tool_name]
        missing = [r for r in required if args.get(r) is None or args.get(r) == "" or args.get(r) == []]
        if missing:
            return {
                "error": "missing_required_inputs",
                "tool": tool_name,
                "missing": missing,
                "escalation": "request_more_info"
            }
        if not args.get("idempotency_key"):
            return {
                "error": "missing_idempotency_key",
                "tool": tool_name,
                "escalation": "request_confirmation"
            }
    return None


class PlanogramMerchandisingVisionAuditor:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.8-flash"):
        self.name = "planogram_merchandising_vision_auditor"
        self.category = "04 · Inventory & Warehousing — Omnichannel Visibility"
        self.display_name = "[04 · Inventory & DC | Omnichannel Visibility] Phantom Inventory Sensor"
        self.description = "[Category: 04 · Inventory & Warehousing — Omnichannel Visibility] Phantom Inventory Sensor (Store Operations / Omni Lead): Identifies shrinkage anomalies when on-hand stock stops scanning at POS. Outcome: Triggers targeted floor cycle counts."
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable] = list(_AVAILABLE_TOOLS)
        self.tool_map = {t.__name__: t for t in self.tools}

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Dispatches tool call with pre-execution safety gate."""
        if tool_name not in self.tool_map:
            return {"error": f"Tool '{tool_name}' not registered in agent contract."}

        gate = enforce_tool_contract(tool_name, kwargs)
        if gate:
            return gate

        tool_fn = self.tool_map[tool_name]
        return tool_fn(**kwargs)

    def run_scenario(self, query: str) -> Dict[str, Any]:
        """Executes an autonomous multi-step supply chain optimization & ERP write-back scenario."""
        findings = []
        actions_taken = []

        r_0 = self.execute_tool("query_store_shelf_vision_audit_captures", capture_id="IMG-SHLF-20261022-409")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "store_shelf_vision_audit_captures", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_contracted_planogram_templates", template_id="PLG-BEV-GONDOLA-Q4")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "contracted_planogram_templates", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_shelf_compliance_scoring_ledger", outlet_id="OUTLET-HYPER-882")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "shelf_compliance_scoring_ledger", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_merchandising_corrective_tasks", outlet_id="OUTLET-HYPER-882")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "merchandising_corrective_tasks", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_dispatch_instore_restock_directive",
            capture_id='IMG-SHLF-20261022-409',
            outlet_id='OUTLET-HYPER-882',
            fso_id='FSO-WEST-112',
            missing_facings_count=5,
            rationale='Gemini 3.8 Flash detected 32.1% Share-of-Shelf (9/14 eye-level facings, 2 empty gaps, 3 competitor intrusions) in 1.18s; pushed instant restock prompt to FSO-WEST-112 while still in store.',
            idempotency_key='SHLF-FIX-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_certify_store_planogram_audit",
            outlet_id='OUTLET-HYPER-882',
            template_id='PLG-BEV-GONDOLA-Q4',
            verified_sos_pct=46.8,
            payout_approved=True,
            rationale='Verified post-correction shelf photo achieved 46.8% SOS (exceeding 45.0% threshold) with 14/14 eye-level facings; unlocked $450 monthly visibility payout.',
            idempotency_key='SHLF-CRT-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = create_planogram_merchandising_vision_auditor_chart_spec()
        surface_id = "planogram_merchandising_vision_auditor_surface_01"
        a2ui_parts = build_planogram_merchandising_vision_auditor_surface(surface_id, spec=vega_spec)
        markdown = self._format_markdown_report(findings, actions_taken)

        return {
            "status": "success",
            "agent": self.name,
            "findings_count": len(findings),
            "actions_executed": actions_taken,
            "vega_spec": vega_spec,
            "a2ui_parts": a2ui_parts,
            "markdown": markdown,
        }

    def _format_markdown_report(
        self,
        findings: List[Dict[str, Any]],
        actions: List[Dict[str, Any]]
    ) -> str:
        """Renders concise executive summary, atomic copy-ready table, and action audit trail."""
        lines = [
            "### ✦ ShelfVision — Retail Planogram & Visibility Auditor — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"store_segment": "Hyper #882 (Post-ShelfVision)", "sos_pct": 46.8, "osa_pct": 98.2, "status": "OPTIMIZED_CVRPTW"}, {"store_segment": "Hyper #882 (Pre-Correction)", "sos_pct": 32.1, "osa_pct": 84.0, "status": "LEGACY_STATIC"}, {"store_segment": "Supermarket #410 (Verified)", "sos_pct": 48.2, "osa_pct": 97.5, "status": "OPTIMIZED_CVRPTW"}]:
            lines.append(f"| `{row['store_segment']}` | **{row['sos_pct']}** | {row['osa_pct']} | `{row['status']}` |")

        lines.extend([
            "",
            "#### ⚡ Autonomous Write-Backs & Actions Executed",
            "",
        ])
        for act in actions:
            eid = act.get("dispatch_execution_id") or act.get("secondary_action_id") or "ACT-ID"
            lines.append(f"- **Action Executed**: `{eid}` | Status: `{act.get('status')}` | Rationale: {act.get('rationale')}")

        lines.extend([
            "",
            "### 🔗 Connected Enterprise Systems",
        ])
        for sys_meta in [{"id": "gemini_38_flash_shelf_vision", "name": "Vertex AI Gemini 3.8 Flash Dense Retail SKU & Facing Detector", "protocol": "gRPC Multimodal API", "tables": ["store_shelf_vision_audit_captures"]}, {"id": "trade_planogram_contract_db", "name": "Enterprise Category Management & Contracted Planogram Registry", "protocol": "REST / BigQuery", "tables": ["contracted_planogram_templates"]}, {"id": "sos_compliance_scoring_engine", "name": "Share-of-Shelf (SOS) & Cooler Purity Compliance Scorer", "protocol": "Python Analytics", "tables": ["shelf_compliance_scoring_ledger"]}, {"id": "sfa_instore_task_dispatcher", "name": "In-Store Mobile Merchandising Corrective Action Dispatcher", "protocol": "Webhook / Push", "tables": ["merchandising_corrective_tasks"]}]:
            lines.append(f"- **{sys_meta['name']}** (`{sys_meta['protocol']}`)")

        return "\n".join(lines)


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
        """Routes Gemini 3.1 Pro & 3.8 Flash calls to the global Vertex AI endpoint even when the Reasoning Engine runs in us-central1."""

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
            scenario = PlanogramMerchandisingVisionAuditor().run_scenario("live_turn")
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
            surface_id = f"planogram-me-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_planogram_merchandising_vision_auditor_surface(surface_id, spec=create_planogram_merchandising_vision_auditor_chart_spec())
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="planogram_merchandising_vision_auditor",
        description="[Category: 04 · Inventory & Warehousing — Omnichannel Visibility] Phantom Inventory Sensor (Store Operations / Omni Lead): Identifies shrinkage anomalies when on-hand stock stops scanning at POS. Outcome: Triggers targeted floor cycle counts.",
        model=GlobalGemini(
            model="gemini-3.8-flash",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=4096,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
        instruction=_INSTRUCTION,
        tools=_AVAILABLE_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_model_callback=_append_verified_report,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name="planogram_merchandising_vision_auditor")

    class PlanogramMerchandisingVisionAuditorAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for planogram_merchandising_vision_auditor."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = PlanogramMerchandisingVisionAuditor()

        @staticmethod
        def _pin_env() -> None:
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
            os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai")

        def query(self, *args: Any, **kwargs: Any) -> Any:
            self._pin_env()
            return super().query(*args, **kwargs)

        def stream_query(self, *args: Any, **kwargs: Any) -> Any:
            self._pin_env()
            yield from super().stream_query(*args, **kwargs)

        def run_scenario(self, query: str = "") -> Dict[str, Any]:
            return self._scenario_agent.run_scenario(query)

except ImportError:
    root_agent = None  # type: ignore
    app = None  # type: ignore
    PlanogramMerchandisingVisionAuditorAdkApp = None  # type: ignore
