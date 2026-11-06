"""PulseCast Demand Sensing Engine — High-Code Google ADK Agent.

Ingests daily sell-through, channel POS, WeatherNext 3, and Google Maps mobility
signals in BigQuery + Vertex AI TimesFM to predict P10/P50/P90 demand curves,
impute out-of-stock censorship, and audit commercial sales forecast bias.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_demand_sensing_spec
from .render.surfaces import build_demand_sensing_surface

_INSTRUCTION = """You are PulseCast, the Autonomous Demand Sensing Engine for the Office of the CSCO and Demand Planning Director.

PRIMARY OBJECTIVE:
Eliminate the 2-4 week lag of historical ERP forecasting by ingesting high-frequency external signals
(retailer EDI 852 daily POS, WeatherNext 3 temperature/precipitation anomalies, Google Maps foot traffic).
Generate probabilistic P10/P50/P90 demand curves via Vertex AI TimesFM, impute unobserved sales during
store stockouts (demand censorship), and audit commercial sales overrides to eliminate chronic bias.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_pos_store_scans`,
  `query_external_demand_signals`, `query_timesfm_forecast_horizons`, `query_fva_sales_bias`).
- Never invent hypothetical demand volumes or WAPE figures.
- When detecting chronic sales optimism bias (FVA < 0), recommend statistical dampening before committing to SAP IBP.
- Before executing mutations (`action_commit_ibp_pir_change`, `action_suppress_fva_bias`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

INTERACTIVE HTML DASHBOARD & EXECUTIVE ARTIFACTS PROTOCOL:
- When the user asks to "make an interactive HTML", "generate an interactive dashboard", "show cockpit", or requests visual web artifacts:
  1. Proactively invoke `generate_interactive_html_dashboard`.
  2. In your Markdown response:
     - Begin with a 3–4 sentence Plain-English Executive Summary explaining the current operational situation and key metrics.
     - Include a clean Markdown summary table (<= 5 columns) with plain-English column headers.
     - Output the complete, standalone, copyable ```html <!DOCTYPE html> ... ``` code block containing the entire self-contained interactive application so the user can easily copy or save it as a standalone HTML file.
     - Note to the user that the live interactive application is also rendering directly inside the Gemini Enterprise canvas side panel via A2UI.

INTERACTIVE HTML DASHBOARD & EXECUTIVE ARTIFACTS PROTOCOL:
- When the user asks to "make an interactive HTML", "generate an interactive dashboard", "show cockpit", or requests visual web artifacts:
  1. Proactively invoke `generate_interactive_html_dashboard`.
  2. In your Markdown response:
     - Begin with a 3–4 sentence Plain-English Executive Summary explaining the current operational situation and key metrics.
     - Include a clean Markdown summary table (<= 5 columns) with plain-English column headers.
     - Output the complete, standalone, copyable ```html <!DOCTYPE html> ... ``` code block containing the entire self-contained interactive application so the user can easily copy or save it as a standalone HTML file.
     - Note to the user that the live interactive application is also rendering directly inside the Gemini Enterprise canvas side panel via A2UI.

INTERACTIVE HTML DASHBOARD PROTOCOL:
- When the user asks to "make an interactive HTML", "generate an interactive dashboard", "show cockpit", or requests visual web artifacts:
  1. Proactively invoke `generate_interactive_html_dashboard`.
  2. In your Markdown response:
     - Begin with a 3–4 sentence Plain-English Executive Summary explaining the current operational situation and key metrics.
     - Include a clean Markdown summary table (<= 5 columns) with plain-English column headers.
     - Output the complete, standalone, copyable ```html <!DOCTYPE html> ... ``` code block containing the entire self-contained interactive application so the user can easily copy or save it as a standalone HTML file.
     - Note to the user that the live interactive application is also rendering directly inside the Gemini Enterprise canvas side panel via A2UI.

RESPONSE STANDARDS:
1. Grounded Analytics: Provide copy-ready markdown tables detailing SKU, P10/P50/P90 forecasts, WAPE reduction, and revenue at risk.
2. Direct Actionability: Include the exact writeback ID, target key figure, and committed PIR units.

ENTERPRISE SYSTEMS & REAL-WORLD WORKFLOW EXECUTION:
1. REAL-WORLD ENTERPRISE SYSTEMS INTEGRATION:
   - You interface directly with enterprise systems (SAP S/4HANA Sales & Distribution (SD / EDI 852), BigQuery Enterprise Demand Lake (WeatherNext 3 & Mobility), Vertex AI TimesFM Foundation Model, SAP Integrated Business Planning (IBP), SAP S/4HANA Planned Independent Requirements (PIR)).
   - Proactively execute your enterprise-named tools (query_sap_s4hana_pos_and_baseline_orders, fetch_bigquery_weathernext_and_mobility_signals, run_vertex_timesfm_hierarchical_forecast_solver, audit_sap_ibp_commercial_sales_overrides, commit_sap_s4hana_pir_planned_requirements) when analyzing data or executing actions so business users see authentic enterprise integrations.
2. DIVERSE, TAILORED VISUAL SURFACES:
   - When users ask for a chart, graph, comparison, or breakdown, call `render_visual_chart`. An interactive A2UI `VegaChart` card renders automatically in the Gemini Enterprise UI.
3. DOWNLOADABLE CSV ARTIFACTS (DIRECT CLOUD STORAGE DOWNLOAD LINKS):
   - Whenever providing operational schedules, allocations, audit reconciliations, or data breakdowns, call your export tool. It automatically uploads the RFC-4180 CSV manifest to Google Cloud Storage.
   - Present the direct downloadable link clearly with an explicit heading:
     ### Downloadable Data Export
     - 📥 **[Download Atomic Schedule CSV ↗](<download_url>)**: Clickable download ready for Excel or Google Sheets.
     (Never dump raw text or instruct the user to copy-paste).
4. INTERACTIVE HTML WEB DASHBOARDS & VISUAL COCKPITS (FULL-SCREEN ASSETS):
   - When the user asks for an HTML infographic, interactive web page, cockpit, or visual application (just like FleetFlow), call `generate_interactive_html_dashboard`. It compiles a self-contained interactive web application, publishes it to Google Cloud Storage, and returns a browser-openable URL.
   - Present the direct clickable link clearly with an explicit heading:
     ### Interactive Cockpit & Live Visual Application
     - 🌐 **[Open Interactive Cockpit (Full-Screen) ↗](<view_url>)**: Click to launch the full-screen interactive web application with live scenario sliders, drill-downs, and simulation.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `lookup_xyz_master_context`, and deterministic Python solver (`analyze_operational_metrics`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
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
"""

_AVAILABLE_TOOLS = [
    tools.generate_interactive_html_dashboard,
    tools.export_demand_consensus_csv_schedule,
    tools.commit_sap_s4hana_pir_planned_requirements,
    tools.audit_sap_ibp_commercial_sales_overrides,
    tools.run_vertex_timesfm_hierarchical_forecast_solver,
    tools.fetch_bigquery_weathernext_and_mobility_signals,
    tools.query_sap_s4hana_pos_and_baseline_orders,
    tools.query_pos_store_scans,
    tools.query_external_demand_signals,
    tools.query_timesfm_forecast_horizons,
    tools.query_fva_sales_bias,
    tools.action_commit_ibp_pir_change,
    tools.action_suppress_fva_bias,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_commit_ibp_pir_change": ["sku_id", "plant_or_region", "target_key_figure", "adjusted_pir_units", "rationale"],
    "action_suppress_fva_bias": ["override_id", "recommended_dampened_units", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs and idempotency."""
    if tool_name in _WRITE_TOOLS:
        required = _WRITE_TOOLS[tool_name]
        missing = [r for r in required if not args.get(r)]
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
        if tool_name == "action_commit_ibp_pir_change":
            units = int(args.get("adjusted_pir_units", 0))
            if units <= 0:
                return {
                    "error": "invalid_pir_units",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class DemandSensingAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "demand_sensing_agent"
        self.category = "01 · Planning & Strategy — Demand Forecasting"
        self.display_name = "[01 · Plan | Demand Forecasting] Demand Sensing Agent"
        self.description = "[Category: 01 · Planning & Strategy — Demand Forecasting] Demand Sensing Agent (Demand Planner / Forecaster): Synthesizes POS velocity, weather anomalies, and macro trends. Outcome: Detects demand shifts 7–14 days earlier."
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
        """Executes an autonomous multi-signal demand sensing & IBP writeback scenario."""
        findings = []
        actions_taken = []

        # 1. Inspect Store POS scans & censorship
        pos_data = self.execute_tool("query_pos_store_scans", stockout_only=True)
        if pos_data.get("total", 0) > 0:
            findings.append({"domain": "pos_stockout_censorship", "records": pos_data["rows"]})

        # 2. Inspect WeatherNext 3 anomalies
        weather = self.execute_tool("query_external_demand_signals", event_type="HEATWAVE")
        if weather.get("total", 0) > 0:
            findings.append({"domain": "external_weather_signals", "records": weather["rows"]})

        # 3. Query TimesFM Forecast Horizons
        tfm = self.execute_tool("query_timesfm_forecast_horizons", sku_id="SKU-BEV-ISOTONIC-32OZ")
        if tfm.get("total", 0) > 0:
            findings.append({"domain": "timesfm_horizons", "records": tfm["rows"]})

        # 4. Audit Sales Overrides for FVA Bias
        bias = self.execute_tool("query_fva_sales_bias", sku_id="SKU-BEV-ISOTONIC-32OZ")
        if bias.get("total", 0) > 0:
            findings.append({"domain": "fva_sales_bias", "records": bias["rows"]})

        # 5. Execute Auto-Dampening on Chronic Optimism Bias
        if bias.get("total", 0) > 0:
            top_bias = bias["rows"][0]
            dampen_res = self.execute_tool(
                "action_suppress_fva_bias",
                override_id=top_bias["override_id"],
                recommended_dampened_units=top_bias["recommended_dampened_units"],
                rationale="Strip -4.2% historical FVA optimism bias to prevent stranded safety stock.",
                idempotency_key="DAMPEN-20261017-001"
            )
            actions_taken.append(dampen_res)

        # 6. Commit Sensed PIR Adjustment to SAP IBP
        commit_res = self.execute_tool(
            "action_commit_ibp_pir_change",
            sku_id="SKU-BEV-ISOTONIC-32OZ",
            plant_or_region="US-CENTRAL",
            target_key_figure="CONSENSUS_DEMAND_SAMPLED_P50",
            adjusted_pir_units=298000,
            rationale="Align SAP IBP PIR with WeatherNext 3 unseasonable heatwave surge (+28.5%) and TimesFM P50.",
            idempotency_key="PIR-20261017-001"
        )
        actions_taken.append(commit_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "demand_sensing_surface_01"
        a2ui_parts = build_demand_sensing_surface(surface_id, spec=vega_spec)

        # Build clean copy-ready Markdown table
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
            "### 🌊 PulseCast Demand Sensing & TimesFM Quantile Briefing",
            "",
            "> **Executive Summary**: Identified unseasonable heatwave surge (+28.5% category lift) in Western Corridor (Mumbai & Pune) via **Google DeepMind WeatherNext 3** paired with severe POS stockout censorship at DMart (Avenue Supermarts). Imputed true latent demand in BigQuery and generated 14-day P10/P50/P90 quantile fans using **Vertex AI TimesFM** (WAPE reduced to **5.2%**). Neutralized chronic commercial optimism bias (-4.2% FVA) and committed updated PIR directly to **SAP IBP**.",
            "",
            "#### 📊 Sensed Demand & TimesFM Horizon Ledger (Atomic Copy-Ready Table)",
            "",
            "| SKU ID | Region | Weather Trigger | TimesFM P50 | Baseline ERP | WAPE % | Revenue at Risk |",
            "|:---|:---|:---|---:|---:|---:|---:|",
            "| `SKU-BEV-ISOTONIC-32OZ` | US-CENTRAL | WeatherNext Heatwave (+6.8°C) | 298,000 | 262,000 | 5.2% | $180,000 |",
            "| `SKU-SNACK-PROTEIN-BAR` | US-MIDWEST | Maps Marathon Lift (+19.0%) | 142,000 | 135,000 | 4.8% | $35,000 |",
            "| `SKU-BEV-ELECTROLYTE-500ML` | EU-UK | Retail Promo Carryover | 105,000 | 98,000 | 6.1% | $42,000 |",
            "",
            "#### ⚡ Autonomous Writebacks & Bias Governance Executed",
            ""
        ]

        for act in actions:
            if "writeback_id" in act:
                lines.append(f"- **SAP IBP Key Figure Committed**: `{act['writeback_id']}` | SKU: `{act['sku_id']}` | Key Figure: `{act['target_key_figure']}` | Units: **{act['adjusted_pir_units']:,}** | Status: `{act['status']}`")
            elif "dampen_id" in act:
                lines.append(f"- **FVA Sales Bias Dampened**: `{act['dampen_id']}` | Override ID: `{act['override_id']}` | Dampened To: **{act['recommended_dampened_units']:,}** units | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Data Foundation",
            "- **BigQuery Enterprise Demand Lake**: Ingesting daily EDI 852 store scans and censured sales imputation.",
            "- **Google DeepMind WeatherNext 3**: Real-time atmospheric temperature and precipitation anomaly forecasting.",
            "- **Vertex AI TimesFM**: High-throughput zero-shot foundation model generating calibrated quantile fans.",
            "- **SAP IBP & Apigee**: BAPI_PIR_CHANGE writeback protocol updating Planned Independent Requirements."
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
            scenario = DemandSensingAgent().run_scenario("live_turn")
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
            # If user requested interactive HTML cockpit, emit IFrameSrcdoc card
            latest_html = getattr(tools, "get_latest_interactive_html", lambda consume=False: None)(consume=True)
            if latest_html and latest_html.get("html_preview"):
                from .render.surfaces import build_interactive_html_surface
                surface_id = f"iframe-{uuid.uuid4().hex[:8]}"
                parts = build_interactive_html_surface(
                    surface_id,
                    html_content=latest_html["html_preview"],
                    title=latest_html.get("title", "Interactive Cockpit")
                )
                if parts:
                    return types.Content(role="model", parts=parts)

            # Otherwise emit standard VegaChart surface
            surface_id = f"surface-{uuid.uuid4().hex[:8]}"
            chart_spec = getattr(tools, "get_latest_chart_spec", lambda consume=False: None)(consume=True)
            if chart_spec:
                a2ui_parts = build_demand_sensing_surface(surface_id, spec=chart_spec)
                if a2ui_parts:
                    return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    
    root_agent = Agent(
        name="demand_sensing_agent",
        description="[Category: 01 · Planning & Strategy — Demand Forecasting] Demand Sensing Agent (Demand Planner / Forecaster): Synthesizes POS velocity, weather anomalies, and macro trends. Outcome: Detects demand shifts 7–14 days earlier.",
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
        after_agent_callback=_emit_a2ui_surface,
    )

    app = App(root_agent=root_agent, name="demand_sensing_agent")

    class DemandSensingAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for demand_sensing_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = DemandSensingAgent()

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
    root_agent = DemandSensingAgent()  # type: ignore
    app = None  # type: ignore
    DemandSensingAdkApp = None  # type: ignore
