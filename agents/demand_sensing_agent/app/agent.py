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

RESPONSE STANDARDS:
1. Grounded Analytics: Provide copy-ready markdown tables detailing SKU, P10/P50/P90 forecasts, WAPE reduction, and revenue at risk.
2. Direct Actionability: Include the exact writeback ID, target key figure, and committed PIR units.

STRICT CONCISE & PYTHON-FIRST EXECUTION PROTOCOL:
- Lead with a 1–2 sentence deterministic KPI conclusion citing exact IDs and numbers from Python tools (zero fluff/filler).
- Always run Python tools (`analyze_operational_metrics`, `query_*`, `lookup_xyz_master_context`) for math and aggregations—never estimate mentally.
- Call `render_visual_chart` when visual comparison helps; the interactive A2UI `VegaChart` card renders automatically (never paste raw Vega-Lite JSON or base64 in text).
- Keep Markdown tables outside the card concise (`<=5` columns) for clean Google Sheets copy-paste.
- Call `draft_operational_brief` ONLY when drafting a formal memo, claim, or brief is requested or required.
- Never call `action_*` write-back tools on read-only questions.
"""

_AVAILABLE_TOOLS = [
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
            "> **Executive Summary**: Identified unseasonable heatwave surge (+28.5% category lift) in US-Central via **Google DeepMind WeatherNext 3** paired with severe POS stockout censorship at Kroger. Imputed true latent demand in BigQuery and generated 14-day P10/P50/P90 quantile fans using **Vertex AI TimesFM** (WAPE reduced to **5.2%**). Neutralized chronic commercial optimism bias (-4.2% FVA) and committed updated PIR directly to **SAP IBP**.",
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
            surface_id = f"demand-sensi-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_demand_sensing_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
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
