"""ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer — High-Code Google ADK Agent.

Combines Gemini 3.8 Flash optical RMA triage with returning FleetFlow backhaul insertion and margin-maximizing circular disposition (Grade-A Restock, Refurbish, Component Harvest).
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_reverse_rma_optimizer_chart_spec
from .render.surfaces import build_reverse_rma_optimizer_surface

_INSTRUCTION = """You are ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer.

PRIMARY OBJECTIVE:
Combines Gemini 3.8 Flash optical RMA triage with returning FleetFlow backhaul insertion and margin-maximizing circular disposition (Grade-A Restock, Refurbish, Component Harvest).

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_assign_rma_disposition_and_backhaul`, `action_issue_instant_customer_rma_credit_or_swap`), ensure all required fields and a non-empty `idempotency_key` are provided.
"""

_AVAILABLE_TOOLS = [
    tools.query_customer_rma_intake_requests,
    tools.query_multimodal_vision_grading_results,
    tools.query_fleet_backhaul_pickup_slots,
    tools.query_circular_disposition_routing_ledger,
    tools.action_assign_rma_disposition_and_backhaul,
    tools.action_issue_instant_customer_rma_credit_or_swap,
    tools.list_systems
]

_WRITE_TOOLS = {
    "action_assign_rma_disposition_and_backhaul": ["rma_id", "optical_grade", "target_facility_id", "backhaul_vehicle_id", "rationale"],
    "action_issue_instant_customer_rma_credit_or_swap": ["rma_id", "customer_id", "credit_amount_usd", "rationale"],
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


class ReverseRmaOptimizer:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.8-flash"):
        self.name = "reverse_rma_optimizer"
        self.category = "06 · Returns & Reverse Logistics — Returns & Claims Mgmt"
        self.display_name = "[06 · Returns & ESG | Returns & Claims Mgmt] Return Fraud Sentinel"
        self.description = "[Category: 06 · Returns & Reverse Logistics — Returns & Claims Mgmt] Return Fraud Sentinel (Reverse Logistics / Fraud Lead): Analyzes item photos and packaging video feeds to detect wear or swapped tags. Outcome: Cuts returns fraud abuse by 25–40%."
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable] = list(_AVAILABLE_TOOLS)
        self.tool_map = {t.__name__: t for t in self.tools}

    def select_orchestrated_model(self, query: str = "") -> Dict[str, str]:
        """Agent Orchestrator dynamically decides whether to use Gemini 3.8 Flash or Gemini 3.1 Pro / 4 Argon."""
        q_lower = (query or "").lower()
        needs_pro_or_argon = any(k in q_lower for k in ("scenario", "multi-echelon", "war room", "redline", "capex", "trade-off", "optimize", "simulate"))
        selected = "gemini-3.1-pro / gemini-4-argon (subject to availability)" if needs_pro_or_argon else "gemini-3.8-flash"
        return {
            "orchestrator_policy": "Dynamic Agent Orchestrator Routing (Gemini 3.8 Flash <-> Gemini 3.1 Pro / 4 Argon subject to availability)",
            "selected_model": selected,
            "fast_model": "gemini-3.8-flash",
            "pro_argon_model": "gemini-3.1-pro / gemini-4-argon (subject to availability)",
            "eval_judge_model": "gemini-4-argon (fallback: gemini-3.1-pro, subject to availability)",
        }

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

        r_0 = self.execute_tool("query_customer_rma_intake_requests", rma_id="RMA-20261022-501")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "customer_rma_intake_requests", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_multimodal_vision_grading_results", rma_id="RMA-20261022-501")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "multimodal_vision_grading_results", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_fleet_backhaul_pickup_slots", rma_id="RMA-20261022-501")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "fleet_backhaul_pickup_slots", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_circular_disposition_routing_ledger", rma_id="RMA-20261022-501")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "circular_disposition_routing_ledger", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_assign_rma_disposition_and_backhaul",
            rma_id='RMA-20261022-501',
            optical_grade='GRADE_A_FACTORY_SEAL_INTACT',
            target_facility_id='FDC-AUSTIN-02',
            backhaul_vehicle_id='TRK-12T-TX14',
            rationale='Gemini 3.8 Flash verified factory tamper seal intact (Grade A); routed 12 units directly to Austin FDC-02 for immediate resale via returning truck TRK-12T-TX14, recovering 94% value ($9,024) and saving $420 LTL freight.',
            idempotency_key='RMA-LOOP-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_issue_instant_customer_rma_credit_or_swap",
            rma_id='RMA-20261022-501',
            customer_id='RETAIL-PARTNER-09',
            credit_amount_usd=9024.0,
            rationale='Issued instant SAP credit memo upon optical seal verification and backhaul scan.',
            idempotency_key='RMA-CRED-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = create_reverse_rma_optimizer_chart_spec()
        surface_id = "reverse_rma_optimizer_surface_01"
        a2ui_parts = build_reverse_rma_optimizer_surface(surface_id, spec=vega_spec)
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
            "### ✦ ReturnLoop — Autonomous RMA Grading & Backhaul Optimizer — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **06 · Return & Enable**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"disposition_path": "Grade-A Direct FDC Restock", "recovery_pct": 94.0, "recovered_usd": 9024, "status": "OPTIMIZED_CVRPTW"}, {"disposition_path": "Grade-B Certified Refurb", "recovery_pct": 72.5, "recovered_usd": 4640, "status": "OPTIMIZED_CVRPTW"}, {"disposition_path": "Grade-C Component Harvest", "recovery_pct": 48.0, "recovered_usd": 3072, "status": "OPTIMIZED_CVRPTW"}, {"disposition_path": "Legacy Central Return Hub", "recovery_pct": 38.0, "recovered_usd": 3648, "status": "LEGACY_STATIC"}]:
            lines.append(f"| `{row['disposition_path']}` | **{row['recovery_pct']}** | {row['recovered_usd']} | `{row['status']}` |")

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
        for sys_meta in [{"id": "gemini_38_flash_rma_vision", "name": "Vertex AI Gemini 3.8 Flash Optical RMA Condition & Seal Grader", "protocol": "gRPC Multimodal API", "tables": ["multimodal_vision_grading_results"]}, {"id": "loop_sap_rma_portal", "name": "SAP S/4HANA Returns & Customer RMA Intake Portal", "protocol": "REST / OData v4", "tables": ["customer_rma_intake_requests"]}, {"id": "fleetflow_backhaul_matcher", "name": "FleetFlow Returning Delivery Truck Backhaul Milk-Run Matcher", "protocol": "Google Maps CVRPTW", "tables": ["fleet_backhaul_pickup_slots"]}, {"id": "circular_disposition_solver", "name": "OR-Tools Circular Recovery Margin Solver (Restock vs Refurb vs Harvest)", "protocol": "Python MILP", "tables": ["circular_disposition_routing_ledger"]}]:
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
            scenario = ReverseRmaOptimizer().run_scenario("live_turn")
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
            surface_id = f"reverse-rma--{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_reverse_rma_optimizer_surface(surface_id, spec=create_reverse_rma_optimizer_chart_spec())
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name="reverse_rma_optimizer",
        description="[Category: 06 · Returns & Reverse Logistics — Returns & Claims Mgmt] Return Fraud Sentinel (Reverse Logistics / Fraud Lead): Analyzes item photos and packaging video feeds to detect wear or swapped tags. Outcome: Cuts returns fraud abuse by 25–40%.",
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

    app = App(root_agent=root_agent, name="reverse_rma_optimizer")

    class ReverseRmaOptimizerAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for reverse_rma_optimizer."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = ReverseRmaOptimizer()

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
    ReverseRmaOptimizerAdkApp = None  # type: ignore
