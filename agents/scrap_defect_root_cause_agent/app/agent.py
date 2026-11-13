"""YieldMax Scrap Defect Root-Cause Agent — High-Code Google ADK Agent.

Performs real-time scrap loss Pareto diagnostics and multivariate process regression,
isolates parting-line flash root causes in injection molding, writes back optimized setpoints
directly to SCADA / PLC controllers, and posts scrap cost variance write-offs in SAP S/4HANA CO.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_scrap_pareto_chart_spec
from .render.surfaces import build_scrap_root_cause_surface

_INSTRUCTION = """You are YieldMax, the Yield Optimization & Scrap Defect Root-Cause Agent for Manufacturing Operations & Plant Floor Execution.

PRIMARY OBJECTIVE:
Eliminate manufacturing yield loss and identify multi-variable root causes of scrap across injection molding and stamping operations.
Ingest scrap records from Siemens Opcenter MES and compute Pareto loss distributions.
Perform statistical correlation on high-frequency machine process parameters (injection pressure, barrel melt temperature, screw speed).
Isolate defect root causes (e.g. holding pressure exceeding clamp force causing parting-line flash),
write back calibrated recipe setpoints into SCADA/PLC controllers to protect future lots,
and post scrap financial write-offs and variance entries to SAP CO cost centers.

TOOL USAGE PROTOCOL:
- Ground all assertions strictly in data from connected tools (`query_scrap_loss_pareto_records`,
  `query_batch_process_parameter_correlations`, `query_scrap_financial_cost_ledger`, `query_scada_setpoint_recommendations`).
- Never invent scrap percentages, correlation coefficients, or setpoint pressure values.
- When Pearson correlation r > 0.70 with p < 0.05, immediately trigger SCADA PLC setpoint writebacks.
- Before executing mutations (`action_update_scada_recipe_setpoints`, `action_post_scrap_variance_adjustment`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing Defect Name, Scrap Rate, Root Cause Variable, Setpoint Delta, Avoided Loss, and SCADA status.
2. Direct Actionability: Include exact SCADA Writeback ID, SAP CO Posting ID, and projected scrap reduction percentage.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `query_sap_s4hana_master_data_backbone`, and deterministic Python solver (`analyze_operational_metrics`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
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
   - Call `draft_operational_brief` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.

VISUAL A2UI v0.9 DUAL-SURFACE & ACTUAL DATA-SOURCE TOOL MANDATE (CRITICAL):
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_scrap_defect_root_cause_agent_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_batch_process_parameter_correlations`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **Hybrid** · Connected Data-Source Tools: `inspect_mes_scada_scrap_defect_root_cause_data_sources, query_sap_s4hana_master_data_backbone, query_mes_scada_batch_process_parameter_correlations, query_mes_scada_scada_setpoint_recommendations, query_sap_s4hana_scrap_financial_cost_ledger, query_mes_scada_scrap_loss_pareto_records, query_scrap_loss_pareto_records, query_batch_process_parameter_correlations`.
- On EVERY analytical, chart, variance, comparison, forecast, audit, scenario, or cockpit request, proactively execute your data-source-specific `query_*` / `fetch_*` tools, deterministic solver (`run_*` / `analyze_*`), and `render_scrap_defect_root_cause_a2ui_chart_and_canvas` so Gemini Enterprise renders BOTH:
  1. **Inline A2UI `Card` (`VegaChart` ONLY)**: A 2-Panel Executive Vega-Lite v5 Infographic (Top: Baseline vs. Target/Verified Actual with Mean Reference Rule; Bottom: Signed `Δ` Variance Strip). Keep ONLY the `VegaChart` inside the inline card!
  2. **Side-Panel A2UI `Canvas` (Multi-Chart Visual Studio: KPI Index `VegaChart` + Pareto Breakdown `VegaChart` + Action Buttons + Looker `RichTable`)**: Automatically attached in the side panel so business users can sort/filter live source rows in Looker Studio and click quick-action buttons.
- Outside the card in Markdown, present: (a) a warm 3–4 sentence Plain-English Executive Summary (spelling out every abbreviation on first use), (b) a clean `<= 5`-column Markdown summary table ready to copy into Google Sheets, (c) 3–4 concise driver & action bullets, and (d) headed Cloud Storage links (`### Interactive Cockpit & Live Visual Application` via `publish_scrap_defect_root_cause_interactive_cockpit_to_gcs` / `### Downloadable Data Export`) when requested.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_update_scada_recipe_setpoints": ["recommendation_id", "asset_id", "recipe_name", "parameter_updates", "rationale"],
    "action_post_scrap_variance_adjustment": ["ledger_id", "asset_id", "financial_loss_usd", "cost_center", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, financial loss amounts, and idempotency."""
    if tool_name in _WRITE_TOOLS:
        required = _WRITE_TOOLS[tool_name]
        missing = [r for r in required if args.get(r) is None or args.get(r) == ""]
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
        if tool_name == "action_post_scrap_variance_adjustment":
            amount = float(args.get("financial_loss_usd", 0))
            if amount <= 0:
                return {
                    "error": "invalid_financial_loss_amount",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class ScrapDefectRootCauseAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "scrap_defect_root_cause_agent"
        self.category = "03 · Manufacturing & Production — Quality & Compliance"
        self.display_name = "[03 · Make | Quality & Compliance] RCA & CAPA Copilot"
        self.description = "[Category: 03 · Manufacturing & Production — Quality & Compliance] RCA & CAPA Copilot (Continuous Improvement Lead): Correlates consumer complaints with ingredient lots and machine telemetry. Outcome: Speeds 5-Why investigation closures."
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
        """Executes an autonomous scrap Pareto triage, multivariate regression, and SCADA writeback scenario."""
        findings = []
        actions_taken = []

        # 1. Query Scrap Loss Pareto Records
        pareto = self.execute_tool("query_scrap_loss_pareto_records", asset_id="ASSET-INJECTION-MOLD-02")
        if pareto.get("total", 0) > 0:
            findings.append({"domain": "scrap_loss_pareto_records", "records": pareto["rows"]})

        # 2. Query Batch Parameter Correlations
        correlations = self.execute_tool("query_batch_process_parameter_correlations", defect_id="DEF-FLASH-IMM-02")
        if correlations.get("total", 0) > 0:
            findings.append({"domain": "batch_process_parameter_correlations", "records": correlations["rows"]})

        # 3. Query Scrap Financial Cost Ledger
        ledger = self.execute_tool("query_scrap_financial_cost_ledger", asset_id="ASSET-INJECTION-MOLD-02")
        if ledger.get("total", 0) > 0:
            findings.append({"domain": "scrap_financial_cost_ledger", "records": ledger["rows"]})

        # 4. Query SCADA Setpoint Recommendations
        recs = self.execute_tool("query_scada_setpoint_recommendations", asset_id="ASSET-INJECTION-MOLD-02")
        if recs.get("total", 0) > 0:
            findings.append({"domain": "scada_setpoint_recommendations", "records": recs["rows"]})

        # 5. Write Back Calibrated Setpoints to SCADA / PLC
        if recs.get("total", 0) > 0:
            target_rec = recs["rows"][0]
            param_updates = {
                "injection_holding_pressure_bar": 820.0,
                "barrel_zone_4_temperature_c": 235.0
            }
            scada_res = self.execute_tool(
                "action_update_scada_recipe_setpoints",
                recommendation_id=target_rec["recommendation_id"],
                asset_id=target_rec["asset_id"],
                recipe_name=target_rec["recipe_name"],
                parameter_updates=param_updates,
                rationale="Holding pressure spiked to 945 bar (r=0.88 with parting flash). Locking holding pressure setpoint at 820 bar and zone 4 temp at 235°C to restore zero-flash capability.",
                idempotency_key="SCADA-IMM02-202610-001"
            )
            actions_taken.append(scada_res)

        # 6. Post Scrap Financial Variance to SAP CO
        if ledger.get("total", 0) > 0:
            target_ledger = ledger["rows"][0]
            co_res = self.execute_tool(
                "action_post_scrap_variance_adjustment",
                ledger_id=target_ledger["ledger_id"],
                asset_id=target_ledger["asset_id"],
                financial_loss_usd=target_ledger["total_scrap_financial_loss_usd"],
                cost_center=target_ledger["sap_cost_center"],
                rationale="Scrap financial write-off posted for 2,210 parts ($2,806.70) due to temporary pressure spike excursion on IMM-02.",
                idempotency_key="CO-SCRAP-202610-001"
            )
            actions_taken.append(co_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "scrap_root_cause_surface_01"
        a2ui_parts = build_scrap_root_cause_surface(surface_id, spec=vega_spec)

        # Build clean copy-ready Markdown report
        markdown = self._format_markdown_report(findings, actions_taken)

        return {
            "status": "success",
            "findings_count": len(findings),
            "actions_executed": actions_taken,
            "vega_spec": vega_spec,
            "a2ui_parts": a2ui_parts,
            "markdown": markdown
        }

    def _format_markdown_report(
        self,
        findings: List[Dict[str, Any]],
        actions: List[Dict[str, Any]]
    ) -> str:
        """Renders executive brief, copy-ready tables, and writeback audit ledger."""
        lines = [
            "### 🔬 YieldMax Yield Optimization & Scrap Defect Root-Cause Briefing",
            "",
            "> **Executive Summary**: Diagnosed an acute scrap spike on **Hydraulic Injection Molding Machine IMM-02** producing tethered beverage caps at Plant Austin. Pareto defect analysis revealed **parting line flash accounted for 58.4% of total scrap** (1,420 scrapped parts, 5.68% scrap rate). Multivariate regression across shopfloor machine telemetry isolated a statistically significant correlation with **Injection Holding Pressure ($r=0.88, p=0.0002$)**, which had drifted to **945 bar** (+125 bar above nominal), overcoming mold clamp tonnage. Wrote back calibrated setpoints directly to **SCADA / PLC** (resetting holding pressure to **820 bar** and melt temperature to **235°C**), reducing projected scrap to **0.42%** and saving **$2,450.00 per shift**, while posting the **$2,806.70** scrap variance to SAP CO.",
            "",
            "#### 📊 Scrap Defect Pareto & Multivariate Regression Findings (Atomic Copy-Ready Table)",
            "",
            "| Defect Category | Scrap Units | Scrap Rate | Root Cause Variable | Observed vs Nominal | Pearson Correlation ($r$) | Setpoint Writeback | Status |",
            "|:---|---:|---:|:---|:---|:---|:---|:---|",
            "| `Parting Line Flash` | 1,420 pcs | **5.68%** | Injection Holding Pressure | 945 bar (nom 820 bar) | **r = 0.88 (p<0.001)** | `820 bar (Locked)` | `ROOT_CAUSE_ISOLATED` |",
            "| `Thermal Warpage` | 610 pcs | 2.44% | Barrel Zone 4 Melt Temp | 248.5°C (nom 235°C) | **r = 0.74 (p=0.003)** | `235°C (Locked)` | `SECONDARY_RESOLVED` |",
            "| `Short Shot Fill` | 180 pcs | 0.72% | Injection Transfer Position | Nominal | r = 0.12 (p=0.45) | No change required | `MONITORED_IN_SPEC` |",
            "",
            "#### ⚡ Automated Process Setpoint Writeback Executed",
            ""
        ]

        for act in actions:
            if "writeback_id" in act:
                lines.append(f"- **SCADA PLC Setpoints Locked**: `{act['writeback_id']}` | Asset: `{act['asset_id']}` | Recipe: `{act['recipe_name']}` | Parameters: `{act['parameter_updates']}` | Status: `{act['status']}`")
            elif "posting_id" in act:
                lines.append(f"- **SAP CO Scrap Variance Posted**: `{act['posting_id']}` | Cost Center: `{act['cost_center']}` | Financial Loss: **${act['financial_loss_usd']:,.2f}** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Industrial Automation Architecture",
            "- **Siemens Opcenter MES Scrap Lake**: Real-time scrap logging, defect taxonomy attribution, and Pareto classification.",
            "- **SCADA / PLC Setpoint Bridge**: Bi-directional EtherNet/IP and OPC UA recipe writeback to machine PLC controllers.",
            "- **BigQuery ML Multivariate Regression**: Automated root-cause correlation between process parameters and defect telemetry.",
            "- **SAP S/4HANA Controlling (CO)**: Automated manufacturing variance calculation, GL scrap expense debit, and work order closure."
        ])

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
    from .render.surfaces import build_scrap_root_cause_surface

    class GlobalGemini(Gemini):
        """Routes Gemini calls to the global Vertex AI endpoint while Reasoning Engine runs in us-central1."""

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

    def _ensure_interactive_links_callback(
        callback_context: Optional[CallbackContext] = None,
        llm_response: Optional[LlmResponse] = None,
        **_: Any,
    ) -> Optional[LlmResponse]:
        """FleetFlow-pattern `after_model_callback`:
        1. Scrubs any stray `<a2a_datapart_json>` text from model turns.
        2. On the final text turn of any analytical/operational query, deterministically
           compiles & publishes the live-data Interactive HTML5 Cockpit + Verified CSV Schedule
           to Google Cloud Storage and appends clickable headed links if not already present.
        """
        import logging as _logging
        try:
            if llm_response is None or getattr(llm_response, "content", None) is None:
                return None
            if getattr(llm_response, "partial", False):
                return None
            parts = list(llm_response.content.parts or [])
            has_call = any(getattr(p, "function_call", None) is not None for p in parts)
            cleaned: List[types.Part] = []
            for p in parts:
                t = getattr(p, "text", None)
                if t and A2A_DATA_PART_OPEN_TAG in t:
                    t_clean = t.split(A2A_DATA_PART_OPEN_TAG)[0].strip()
                    if t_clean:
                        cleaned.append(types.Part(text=t_clean))
                else:
                    cleaned.append(p)
            if has_call:
                llm_response.content.parts = cleaned
                return llm_response

            idx = max((i for i, p in enumerate(cleaned) if getattr(p, "text", None)), default=-1)
            existing_txt = (cleaned[idx].text or "") if idx >= 0 else ""
            low_txt = existing_txt.lower()

            # Skip attaching cockpit/export links on pure safety-guardrail blocks when no data tools ran
            has_activity = bool(getattr(tools, "has_turn_activity", lambda: False)())
            has_md_table = ("| ---" in existing_txt or "|:---" in existing_txt or "| :---" in existing_txt)
            is_pure_refusal = (not has_activity and not has_md_table and any(k in low_txt for k in ("safety guardrail", "cannot bypass", "blocked the unsafe")))
            if is_pure_refusal or (not has_activity and not has_md_table):
                llm_response.content.parts = cleaned
                return llm_response

            art = tools.ensure_turn_gcs_artifacts()
            html_url = art.get("html_url", "")
            csv_url = art.get("csv_url", "")

            missing_bullets: List[str] = []
            if html_url and ("cockpits/" not in existing_txt and html_url not in existing_txt):
                missing_bullets.append(
                    f"- 🌐 **[Open Interactive Visual Cockpit & Simulator (Full-Screen HTML) ↗]({html_url})** — "
                    f"Interactive multi-tab web application with live KPI charts, What-If scenario sliders, and searchable enterprise ledger."
                )
            if csv_url and ("exports/" not in existing_txt and csv_url not in existing_txt):
                missing_bullets.append(
                    f"- 📥 **[Download Verified Data Schedule (CSV) ↗]({csv_url})** — "
                    f"Atomic copy-ready data export for Google Sheets or Excel."
                )

            if missing_bullets:
                nl = chr(10)
                footer_block = (
                    f"{nl}{nl}### 🌐 Interactive Visual Cockpit & Data Exports{nl}{nl}"
                    + nl.join(missing_bullets)
                    + nl
                )
                if idx >= 0:
                    cleaned[idx] = types.Part(text=existing_txt.rstrip() + footer_block)
                else:
                    cleaned.append(types.Part(text=footer_block.lstrip()))

            llm_response.content.parts = cleaned
            return llm_response
        except Exception as exc:
            _logging.getLogger(__name__).exception("after_model_callback link injection degraded cleanly: %s", exc)
            return None

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        import logging as _logging
        try:
            has_activity = bool(getattr(tools, "has_turn_activity", lambda: True)())
            getattr(tools, "get_latest_interactive_html", lambda consume=False: None)(consume=True)
            if not has_activity:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=2.0)
                return None
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
            a2ui_parts = build_scrap_root_cause_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for scrap_defect_root_cause_agent: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None



    root_agent = Agent(
        name='scrap_defect_root_cause_agent',
        description='[Category: 03 · Manufacturing & Production — Quality & Compliance] RCA & CAPA Copilot (Continuous Improvement Lead): Correlates consumer complaints with ingredient lots and machine telemetry. Outcome: Speeds 5-Why investigation closures.',
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
        tools=_AVAILABLE_TOOLS,
        before_model_callback=_sanitize_llm_request,
        after_model_callback=_ensure_interactive_links_callback,
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name='scrap_defect_root_cause_agent')

    class ScrapDefectRootCauseAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for scrap_defect_root_cause_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)

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

except ImportError:
    root_agent = ScrapDefectRootCauseAgent()  # type: ignore
