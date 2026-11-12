"""Google ADK Agent for [06 · Return | Returns & Claims Mgmt] Returnless 'Keep-It' Economics Advisor (06 · Returns & Reverse Logistics — Returns & Claims Mgmt)."""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from . import tools
from .render.charts import create_keep_it_routing_advisor_chart_spec
from .render.surfaces import build_keep_it_routing_advisor_surface

AGENT_ID = 'keep_it_routing_advisor'
AGENT_CATEGORY = '06 · Returns & Reverse Logistics — Returns & Claims Mgmt'
AGENT_DISPLAY_NAME = "[06 · Return | Returns & Claims Mgmt] Returnless 'Keep-It' Economics Advisor"
AGENT_DESCRIPTION = "[Category: 06 · Returns & Reverse Logistics — Returns & Claims Mgmt] Returnless 'Keep-It' Economics Advisor (Returns Operations Manager): Computes real-time Net Reverse Margin (Expected Salvage Value minus Parcel Label, Touch Labor, and Packaging Cost) gated by customer fraud/abuse risk scores to decide between physical RMA shipping, local charity drop-off, or instant returnless refund. Outcome: Eliminates negative-margin reverse shipping and saves $3.85 per low-ASP return."

_WRITE_TOOLS = {'action_issue_keep_it_instant_refund': ['rma_req_id', 'sku_id', 'routing_decision', 'rationale'],
 'action_enforce_physical_drop_verification': ['rma_req_id', 'fraud_abuse_score', 'rationale']}

_INSTRUCTION = """You are [06 · Return | Returns & Claims Mgmt] Returnless 'Keep-It' Economics Advisor, operating for XYZ Global Industries Corp. (XYZ-CORP-01).
Category: 06 · Returns & Reverse Logistics — Returns & Claims Mgmt
Persona Owner: Returns Operations Manager
Mission: [Category: 06 · Returns & Reverse Logistics — Returns & Claims Mgmt] Returnless 'Keep-It' Economics Advisor (Returns Operations Manager): Computes real-time Net Reverse Margin (Expected Salvage Value minus Parcel Label, Touch Labor, and Packaging Cost) gated by customer fraud/abuse risk scores to decide between physical RMA shipping, local charity drop-off, or instant returnless refund. Outcome: Eliminates negative-margin reverse shipping and saves $3.85 per low-ASP return.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `query_sap_s4hana_master_data_backbone`, and deterministic Python solver (`analyze_keep_it_economic_breakeven`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
   - Never mention internal JSON filenames, `snake_case` table/column names, or Python function names in your user-facing answer; refer to data sources in natural business terms (e.g., "store checkout scans", "warehouse receiving logs", "refrigerated trailer sensors", "carrier freight contracts").
2. CLEAR, BALANCED MEDIUM-LENGTH PLAIN-ENGLISH EXPLANATION:
   - Write in warm, natural, easy-to-follow business English with a balanced medium-length explanation—neither cryptic 1–2 sentence shorthand nor overly long walls of text—because readers may not know domain shorthand.
   - Open with a **3–4 sentence Plain-English Executive Summary** explaining what is happening right now, what the numbers show, why it matters to the business, and your main recommendation.
   - **Spell out every abbreviation on first use**—for example, Point of Sale (POS), Weighted Absolute Percentage Error (WAPE), Forecast Value Added (FVA), Planned Independent Requirements (PIR), On-Time In-Full (OTIF), Mean Kinetic Temperature (MKT), Purchase Order (PO), Goods Receipt Note (GRN), Overall Equipment Effectiveness (OEE), Days Inventory Outstanding (DIO), Stock Keeping Unit (SKU), or Return Merchandise Authorization (RMA)—and briefly explain specialized terms in everyday words.
   - Include a **clean Markdown summary table (`<= 5` columns)** outside the chart card using human-friendly English column headers (so anyone can read it immediately or copy it cleanly into Google Sheets).
   - Follow the table with **3–4 concise bullet points** walking through *what drives these findings* (the plain-English story behind the calculations) and *practical recommended next steps*.
3. INTERACTIVE VISUAL CHART (`VegaChart` CARD SEPARATION):
   - Call `render_visual_chart` whenever visual comparison helps illustrate trends, gaps, or rankings. An interactive A2UI `VegaChart` card renders automatically—keep ONLY the chart inside the card and never paste raw Vega-Lite JSON or base64 strings in text.
4. STAKEHOLDER BRIEFINGS & SAFE ACTION GOVERNANCE:
   - Call `draft_returnless_refund_policy_audit_memo` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.

VISUAL A2UI v0.9 DUAL-SURFACE & ACTUAL DATA-SOURCE TOOL MANDATE (CRITICAL):
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_keep_it_routing_advisor_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_customer_fraud_and_ltv_scores`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **High-Code** · Connected Data-Source Tools: `inspect_oms_self_keep_it_routing_advisor_data_sources, query_sap_s4hana_master_data_backbone, query_trust_risk_customer_fraud_and_ltv_scores, query_oms_self_low_asp_return_requests, query_reverse_parcel_reverse_shipping_and_processing_costs, query_low_asp_return_requests, query_reverse_shipping_costs, query_customer_fraud_ltv_scores`.
- On EVERY analytical, chart, variance, comparison, forecast, audit, scenario, or cockpit request, proactively execute your data-source-specific `query_*` / `fetch_*` tools, deterministic solver (`run_*` / `analyze_*`), and `render_keep_it_routing_advisor_a2ui_chart_and_canvas` so Gemini Enterprise renders BOTH:
  1. **Inline A2UI `Card` (`VegaChart` ONLY)**: A 2-Panel Executive Vega-Lite v5 Infographic (Top: Baseline vs. Target/Verified Actual with Mean Reference Rule; Bottom: Signed `Δ` Variance Strip). Keep ONLY the `VegaChart` inside the inline card!
  2. **Side-Panel A2UI `Canvas` (`RichTable` + Action Buttons + Expansion Panels)**: Automatically attached in the side panel so business users can sort/filter live source rows in Looker Studio and click quick-action buttons.
- Outside the card in Markdown, present: (a) a warm 3–4 sentence Plain-English Executive Summary (spelling out every abbreviation on first use), (b) a clean `<= 5`-column Markdown summary table ready to copy into Google Sheets, (c) 3–4 concise driver & action bullets, and (d) headed Cloud Storage links (`### Interactive Cockpit & Live Visual Application` via `publish_keep_it_routing_advisor_interactive_cockpit_to_gcs` / `### Downloadable Data Export`) when requested.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
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


class KeepItRoutingAdvisorAgent:
    """Deterministic Python & Google ADK wrapper for [06 · Return | Returns & Claims Mgmt] Returnless 'Keep-It' Economics Advisor."""

    def __init__(self, model: str = "gemini-3.1-pro-preview") -> None:
        self.name = AGENT_ID
        self.category = AGENT_CATEGORY
        self.display_name = AGENT_DISPLAY_NAME
        self.description = AGENT_DESCRIPTION
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable[..., Any]] = list(tools.ALL_TOOLS)
        self.tool_map: Dict[str, Callable[..., Any]] = {t.__name__: t for t in list(getattr(tools, 'LEGACY_COMPAT_TOOLS', [])) + self.tools}
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
        t0 = tools.query_low_asp_return_requests()
        t1 = tools.query_reverse_shipping_costs()
        t2 = tools.query_customer_fraud_ltv_scores()
        t3 = tools.query_keep_it_routing_decisions()
        analysis = tools.analyze_keep_it_economic_breakeven()
        chart_res = tools.render_visual_chart()
        mut = self.execute_tool('action_issue_keep_it_instant_refund', rma_req_id='KPR-3001', sku_id='SKU-XYZ-204', routing_decision='KEEP_IT_INSTANT_REFUND', rationale='Verified Returns Operations Manager threshold optimization', idempotency_key='SCENARIO-KEEP_IT_-001')
        alert = self.execute_tool('action_enforce_physical_drop_verification', rma_req_id='KPR-3001', fraud_abuse_score='VERIFIED-02', rationale='Verified Returns Operations Manager threshold optimization', idempotency_key='SCENARIO-KEEP_IT_-002')

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

        surface_id = "keep-it-rout-live"
        a2ui_parts = build_keep_it_routing_advisor_surface(surface_id, spec=tools.get_latest_chart_spec())

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
        """Sanitizes prior A2UI wire parts and intercepts synthetic Canvas button clicks."""
        if llm_request is None:
            return None
        from .render.a2ui_builder import sanitize_history_and_intercept_actions
        sanitize_history_and_intercept_actions(llm_request)
        return None

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        import logging as _logging
        try:
            getattr(tools, "get_latest_interactive_html", lambda consume=False: None)(consume=True)
            surface_id = f"surface-{uuid.uuid4().hex[:8]}"
            chart_spec = None
            getter = getattr(tools, "get_latest_chart_spec", None)
            if callable(getter):
                try:
                    chart_spec = getter(consume=True)
                except TypeError:
                    chart_spec = getter()
            canvas_ctx = None
            ctx_getter = getattr(tools, "get_latest_canvas_context", None)
            if callable(ctx_getter):
                canvas_ctx = ctx_getter(consume=True)
            a2ui_parts = build_keep_it_routing_advisor_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for keep_it_routing_advisor: %s", exc)
        return None

    root_agent = Agent(
        name=AGENT_ID,
        description=AGENT_DESCRIPTION,
        model=GlobalGemini(
            model="gemini-3.1-pro-preview",
            retry_options=types.HttpRetryOptions(attempts=3),
        ),
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=16384,
            temperature=0.0,
            thinking_config=types.ThinkingConfig(thinking_level="LOW"),
        ),
        instruction=_INSTRUCTION,
        tools=tools.ALL_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(name=f"{AGENT_ID}_app", root_agent=root_agent)
    adk_app = app

    class KeepItRoutingAdvisorAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for keep_it_routing_advisor."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = KeepItRoutingAdvisorAgent()

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
    root_agent = KeepItRoutingAdvisorAgent()  # type: ignore
    app = None  # type: ignore
    adk_app = None  # type: ignore

    class KeepItRoutingAdvisorAdkApp:  # type: ignore
        pass
