"""Google ADK Agent for [05 · Deliver | Route & Carrier] Automated Freight Bill & Accessorial Auditor (05 · Distribution & Logistics — Route & Carrier)."""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from . import tools
from .render.charts import create_freight_bill_audit_agent_chart_spec
from .render.surfaces import build_freight_bill_audit_agent_surface

AGENT_ID = 'freight_bill_audit_agent'
AGENT_CATEGORY = '05 · Distribution & Logistics — Route & Carrier'
AGENT_DISPLAY_NAME = '[05 · Deliver | Route & Carrier] Automated Freight Bill & Accessorial Auditor'
AGENT_DESCRIPTION = '[Category: 05 · Distribution & Logistics — Route & Carrier] Automated Freight Bill & Accessorial Auditor (Transportation Procurement Lead): Reconciles carrier EDI 210 freight invoices line-by-line against contracted lane tariffs, DOE Weekly Retail Diesel Fuel Surcharge (FSC) tables, and GPS geofence detention timestamps. Outcome: Recovers 3.9% of total freight spend by eliminating duplicate accessorials, FSC table errors, and unverified detention charges.'

_WRITE_TOOLS = {'action_approve_short_pay_voucher': ['freight_inv_id',
                                      'carrier_id',
                                      'verified_payable_usd',
                                      'overcharge_recovered_usd',
                                      'rationale'],
 'action_transmit_edi210_dispute_code': ['freight_inv_id',
                                         'carrier_id',
                                         'dispute_reason_code',
                                         'rationale']}

_INSTRUCTION = """You are [05 · Deliver | Route & Carrier] Automated Freight Bill & Accessorial Auditor, operating for XYZ Global Industries Corp. (XYZ-CORP-01).
Category: 05 · Distribution & Logistics — Route & Carrier
Persona Owner: Transportation Procurement Lead
Mission: [Category: 05 · Distribution & Logistics — Route & Carrier] Automated Freight Bill & Accessorial Auditor (Transportation Procurement Lead): Reconciles carrier EDI 210 freight invoices line-by-line against contracted lane tariffs, DOE Weekly Retail Diesel Fuel Surcharge (FSC) tables, and GPS geofence detention timestamps. Outcome: Recovers 3.9% of total freight spend by eliminating duplicate accessorials, FSC table errors, and unverified detention charges.

STRICT DETERMINISTIC & CONCISE EXECUTION RULES:
1. ZERO FLUFF / NON-VERBOSE: Lead with a crisp 1–2 sentence executive KPI conclusion citing exact IDs and numbers returned by Python tools. Never write filler paragraphs or generic consulting prose.
2. PYTHON TOOLS FIRST: Always call the domain `query_*` tools and `analyze_edi210_tariff_and_fsc_variance` to perform calculations in Python—never estimate math mentally. Call `lookup_xyz_master_context` when SKU/Facility/Supplier/Customer/Carrier master attributes are needed.
3. CHARTS & A2UI SEPARATION: Call `render_visual_chart` when visual comparison aids decision-making. An interactive A2UI `VegaChart` card is automatically attached from live tool data—NEVER output raw Vega-Lite JSON or base64 strings in text.
4. ATOMIC TABLES (<=5 COLUMNS): Keep Markdown tables outside the card to at most 5 columns so they copy cleanly into Google Sheets.
5. DRAFTING ON DEMAND: Use `draft_edi210_short_pay_remittance_notice` ONLY when a formal operational memo, claim, notice, or certificate is requested or required by the workflow.
6. GOVERNED WRITE-BACK: Never invoke `action_*` tools on read-only questions. Only execute mutations when requested and all required fields plus `idempotency_key` are satisfied.
"""


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Pre-execution quality gate validating required write-back parameters and idempotency."""
    if tool_name in _WRITE_TOOLS:
        missing = [k for k in _WRITE_TOOLS[tool_name] if args.get(k) in (None, "")]
        if missing:
            return {
                "error": "missing_required_inputs",
                "tool": tool_name,
                "missing": missing,
                "escalation": "request_more_info",
            }
        if not args.get("idempotency_key"):
            return {
                "error": "missing_idempotency_key",
                "tool": tool_name,
                "escalation": "request_confirmation",
            }
    return None


class FreightBillAuditAgentAgent:
    """Deterministic Python & Google ADK wrapper for [05 · Deliver | Route & Carrier] Automated Freight Bill & Accessorial Auditor."""

    def __init__(self, model: str = "gemini-3.1-pro-preview") -> None:
        self.name = AGENT_ID
        self.category = AGENT_CATEGORY
        self.display_name = AGENT_DISPLAY_NAME
        self.description = AGENT_DESCRIPTION
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable[..., Any]] = list(tools.ALL_TOOLS)
        self.tool_map: Dict[str, Callable[..., Any]] = {t.__name__: t for t in self.tools}
        self.system_connectors = list(tools.SYSTEM_CONNECTORS)

    def select_orchestrated_model(self, query: str = "") -> Dict[str, str]:
        """Dynamic routing between Gemini 3.8 Flash and Gemini 3.1 Pro / 4 Argon."""
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

    def execute_tool(self, tool_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Dispatches tool calls with deterministic contract enforcement on write-back tools."""
        if tool_name not in self.tool_map:
            return {"error": f"Tool '{tool_name}' not registered in agent contract."}
        gate = enforce_tool_contract(tool_name, kwargs)
        if gate:
            return gate
        return self.tool_map[tool_name](**kwargs)

    def run_scenario(self, prompt: str = "Execute end-to-end persona workflow") -> Dict[str, Any]:
        """Runs deterministic end-to-end persona analysis, PNG/Vega charting, and governed write-back."""
        t0 = tools.query_edi210_freight_invoices()
        t1 = tools.query_contracted_lane_fsc_tariffs()
        t2 = tools.query_gps_detention_verifications()
        t3 = tools.query_freight_overcharge_adjustments()
        analysis = tools.analyze_edi210_tariff_and_fsc_variance()
        chart_res = tools.render_visual_chart()
        mut = self.execute_tool('action_approve_short_pay_voucher', freight_inv_id='EDI210-7701', carrier_id='CAR-JBHT-FTL', verified_payable_usd=3369.6, overcharge_recovered_usd=614.8, rationale='Verified Transportation Procurement Lead threshold optimization', idempotency_key='SCENARIO-FREIGHT_-001')
        alert = self.execute_tool('action_transmit_edi210_dispute_code', freight_inv_id='EDI210-7701', carrier_id='CAR-JBHT-FTL', dispute_reason_code='VERIFIED-02', rationale='Verified Transportation Procurement Lead threshold optimization', idempotency_key='SCENARIO-FREIGHT_-002')

        kpi = analysis.get("kpi_summary", {})
        md = "\n".join(
            [
                f"**{self.display_name}**: Evaluated `{analysis.get('records_evaluated', 0)}` XYZ-CORP-01 records — "
                f"{kpi.get('series_a_label')}: `{kpi.get('total_series_a', 0):,.2f}` -> "
                f"{kpi.get('series_b_label')}: `{kpi.get('total_series_b', 0):,.2f}` (`{kpi.get('relative_shift_pct', 0):+.2f}%`).",
                "",
                analysis.get("concise_markdown_table", ""),
                "",
                f"### Chart & Action Receipt\n- **High-Res PNG Chart**: `{chart_res['png_infographic']['download_uri']}`\n"
                f"- **Write-Back Receipt**: `{mut.get('action_id')}` (`{mut.get('status')}`)",
            ]
        )

        surface_id = "freight-bill-live"
        a2ui_parts = build_freight_bill_audit_agent_surface(surface_id, spec=tools.get_latest_chart_spec())

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
            "analysis": analysis,
            "chart_artifact": chart_res,
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
    from google.genai import Client, types
    from vertexai.preview.reasoning_engines import AdkApp
    from .render.a2ui_envelope import A2A_DATA_PART_OPEN_TAG

    class GlobalGemini(Gemini):
        """Routes Gemini 3.1 Pro / 3.8 Flash calls to the global Vertex AI endpoint."""

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
        """Strips prior A2UI data parts from history so multi-turn chats never echo raw JSON."""
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
            content.parts = cleaned or [types.Part(text="[Visual VegaChart Surface Rendered in Card]")]
        return None

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        """Emits a blast-radius-protected A2UI v0.9 VegaChart card reflecting live turn tool state."""
        try:
            surface_id = f"freight-bill-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_freight_bill_audit_agent_surface(surface_id, spec=tools.get_latest_chart_spec())
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name=AGENT_ID,
        description=AGENT_DESCRIPTION,
        model=GlobalGemini(
            model="gemini-3.1-pro-preview",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=3072,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        ),
        instruction=_INSTRUCTION,
        tools=tools.ALL_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(name=f"{AGENT_ID}_app", root_agent=root_agent)
    adk_app = app

    class FreightBillAuditAgentAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for freight_bill_audit_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = FreightBillAuditAgentAgent()

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

except Exception:
    root_agent = FreightBillAuditAgentAgent()  # type: ignore
    app = None  # type: ignore
    adk_app = None  # type: ignore

    class FreightBillAuditAgentAdkApp:  # type: ignore
        pass
