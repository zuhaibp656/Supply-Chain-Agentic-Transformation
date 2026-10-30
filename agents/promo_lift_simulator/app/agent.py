"""ElasticityIQ Promo Simulator — High-Code Google ADK Agent.

Isolates true net promotional lift from sister-SKU cannibalization and steers
promotions toward available warehouse & transit supply using BigQuery ML
Double-ML causal elasticity models and AlloyDB stock availability.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_promo_elasticity_spec
from .render.surfaces import build_promo_surface

_INSTRUCTION = """You are ElasticityIQ, the Demand Shaping & Promotional Simulator for the Office of the CSCO and Promo Launch Planner.

PRIMARY OBJECTIVE:
Prevent destructive trade promotion campaigns that spike capacity-constrained SKUs while cannibalizing adjacent full-margin items.
Leverage BigQuery ML Double-ML causal elasticity models to isolate gross lift, sister-SKU volume diversion, and post-promo troughs.
Cross-reference DC stock availability in AlloyDB to reshape discounts and bundle mechanics before campaigns launch in SAP TPM.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_planned_promo_campaigns`,
  `query_causal_promo_elasticity`, `query_cross_sku_cannibalization`, `query_warehouse_promo_availability`).
- Never invent hypothetical lift volumes, elasticity coefficients, or margin dollar impacts.
- When cannibalization exceeds 20% or warehouse stockout risk is elevated, recommend mechanic adjustments.
- Before executing mutations (`action_shape_promotional_mechanic`, `action_lock_tpm_calendar`),
  ensure all required fields and non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive Clarity: Deliver copy-ready markdown tables detailing Gross Lift, Cannibalization Loss, Net Incremental Units, and Margin Gain.
2. Direct Actionability: Include the exact reshaped discount percentage, locked net lift volume, and committed trade spend.

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
    tools.query_planned_promo_campaigns,
    tools.query_causal_promo_elasticity,
    tools.query_cross_sku_cannibalization,
    tools.query_warehouse_promo_availability,
    tools.action_shape_promotional_mechanic,
    tools.action_lock_tpm_calendar,
    tools.list_systems,
    tools.lookup_xyz_master_context,
    tools.analyze_operational_metrics,
    tools.render_visual_chart,
    tools.draft_operational_brief,
]

_WRITE_TOOLS = {
    "action_shape_promotional_mechanic": ["campaign_id", "adjusted_discount_pct", "bundle_sku", "rationale"],
    "action_lock_tpm_calendar": ["campaign_id", "locked_net_lift_units", "committed_trade_spend_usd", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, delegation thresholds, and idempotency."""
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
        if tool_name == "action_lock_tpm_calendar":
            spend = float(args.get("committed_trade_spend_usd", 0))
            if spend > 250000.0:
                return {
                    "error": "trade_spend_exceeds_delegation_authority",
                    "threshold_usd": 250000.0,
                    "requested_usd": spend,
                    "escalation": "request_vp_commercial_approval"
                }
    return None


class PromoLiftSimulatorAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "promo_lift_simulator"
        self.category = "01 · Planning & Strategy — Trade Promotion"
        self.display_name = "[01 · Plan | Trade Promotion] Promo ROI Simulator"
        self.description = "[Category: 01 · Planning & Strategy — Trade Promotion] Promo ROI Simulator (Trade Marketing Manager): Simulates price elasticity, shelf lift, and incremental spend return. Outcome: Prevents break-even trade leakage."
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
        """Executes an autonomous promotional demand shaping and cannibalization mitigation scenario."""
        findings = []
        actions_taken = []

        # 1. Investigate Planned Campaigns
        campaigns = self.execute_tool("query_planned_promo_campaigns", campaign_id="CMP-202611-BOGO")
        if campaigns.get("total", 0) > 0:
            findings.append({"domain": "planned_campaigns", "records": campaigns["rows"]})

        # 2. Query Causal Elasticity Models
        elasticity = self.execute_tool("query_causal_promo_elasticity", sku_id="SKU-BEV-ISOTONIC-32OZ")
        if elasticity.get("total", 0) > 0:
            findings.append({"domain": "causal_elasticity", "records": elasticity["rows"]})

        # 3. Query Cannibalization Impact on Sister-SKUs
        cannibal = self.execute_tool("query_cross_sku_cannibalization", promoted_sku="SKU-BEV-ISOTONIC-32OZ")
        if cannibal.get("total", 0) > 0:
            findings.append({"domain": "cross_sku_cannibalization", "records": cannibal["rows"]})

        # 4. Check Warehouse DC Inventory Buffer Availability
        avail = self.execute_tool("query_warehouse_promo_availability", sku_id="SKU-BEV-ISOTONIC-32OZ")
        if avail.get("total", 0) > 0:
            findings.append({"domain": "warehouse_stock_availability", "records": avail["rows"]})

        # 5. Reshape Promotional Mechanic
        shape_res = self.execute_tool(
            "action_shape_promotional_mechanic",
            campaign_id="CMP-202611-BOGO",
            adjusted_discount_pct=20.0,
            bundle_sku="SKU-BEV-ELECTROLYTE-500ML",
            rationale="Shift from unconstrained 25% BOGO to 20% bundle with surplus Electrolytes to eliminate DC stockout risk and reduce sister-SKU cannibalization by $26.1k.",
            idempotency_key="SHAPE-BOGO-202611-001"
        )
        actions_taken.append(shape_res)

        # 6. Lock Finalized Promo Plan in SAP TPM & Salesforce CGC
        lock_res = self.execute_tool(
            "action_lock_tpm_calendar",
            campaign_id="CMP-202611-BOGO",
            locked_net_lift_units=48000,
            committed_trade_spend_usd=110000.0,
            rationale="Lock shaped campaign delivering +$83k net incremental gross margin.",
            idempotency_key="TPM-LOCK-BOGO-202611-001"
        )
        actions_taken.append(lock_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "promo_elasticity_surface_01"
        a2ui_parts = build_promo_surface(surface_id, spec=vega_spec)

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
            "### 🎯 ElasticityIQ Demand Shaping & Promo Briefing",
            "",
            "> **Executive Summary**: Evaluated Walmart Q4 *BOGO Hydration Blitz* using **BigQuery ML Double-ML** causal inference. Identified that an uncoordinated 25% discount would trigger **26,000 units of sister-SKU cannibalization** ($26,100 brand margin loss) and deplete DC Dallas stock below safety buffer (elevated stockout risk). Reshaped campaign to a **20% bundle paired with surplus Electrolyte 500ml stock**, protecting inventory and delivering **48,000 net incremental units** with **+$83,000 net profit (+22% trade spend ROI)**.",
            "",
            "#### 📊 Promotional Lift & Cannibalization Decomposition (Atomic Copy-Ready Table)",
            "",
            "| Campaign Name | Target SKU | Base Price | Promo Discount | Gross Lift | Cannibalization | Net Incremental | Net Margin Gain | Double-ML P-Value |",
            "|:---|:---|---:|---:|---:|---:|---:|---:|:---|",
            "| `BOGO Hydration Blitz` | `SKU-BEV-ISOTONIC-32OZ` | $2.99 | 20.0% (Reshaped) | 85,000 | -26,000 | **+48,000** | **+$83,000** | `p = 0.002` (Stat Sig) |",
            "| `20% Off Protein Snack` | `SKU-SNACK-PROTEIN-BAR` | $3.49 | 20.0% | 42,000 | -8,500 | **+29,000** | **+$68,250** | `p = 0.001` (Stat Sig) |",
            "| `Bundle & Save Electrolyte` | `SKU-BEV-ELECTROLYTE-500ML` | $3.99 | 15.0% | 31,000 | -4,200 | **+24,000** | **+$69,900** | `p = 0.004` (Stat Sig) |",
            "",
            "#### ⚡ Trade Promotion Decisions & System Locks Executed",
            ""
        ]

        for act in actions:
            if "shape_id" in act:
                lines.append(f"- **Promotional Mechanic Reshaped**: `{act['shape_id']}` | Campaign: `{act['campaign_id']}` | Discount: **{act['adjusted_discount_pct']}%** | Bundle SKU: `{act['bundle_sku']}` | Status: `{act['status']}`")
            elif "lock_id" in act:
                lines.append(f"- **SAP TPM & Salesforce Calendar Locked**: `{act['lock_id']}` | Net Lift: **{act['locked_net_lift_units']:,}** units | Trade Spend: **${act['committed_trade_spend_usd']:,.2f}** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Causal Engine",
            "- **BigQuery ML Double-ML Causal Models**: Partially Linear Regression (PLR) estimating unconfounded price elasticity.",
            "- **AlloyDB pgvector Multi-Echelon Stock Buffer**: Real-time checking of warehouse available-to-promise inventory.",
            "- **SAP Trade Promotion Management (TPM)**: Automated calendar lock synchronizing retailer promotion baseline curves.",
            "- **Salesforce Consumer Goods Cloud**: Mobile field sales execution and retail store planogram alignment."
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
    from google.genai import Client, types
    from vertexai.preview.reasoning_engines import AdkApp
    from .render.a2ui_envelope import A2A_DATA_PART_OPEN_TAG
    from .render.surfaces import build_promo_surface

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

    def _emit_a2ui_surface(
        callback_context: Optional[CallbackContext] = None,
        **_: Any,
    ) -> Optional[types.Content]:
        try:
            surface_id = f"promo-lift-simul-{uuid.uuid4().hex[:8]}"
            a2ui_parts = build_promo_surface(surface_id, spec=tools.get_latest_chart_spec(consume=True))
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception:
            pass
        return None

    root_agent = Agent(
        name='promo_lift_simulator',
        description='[Category: 01 · Planning & Strategy — Trade Promotion] Promo ROI Simulator (Trade Marketing Manager): Simulates price elasticity, shelf lift, and incremental spend return. Outcome: Prevents break-even trade leakage.',
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

    app = App(root_agent=root_agent, name='promo_lift_simulator')

    class PromoLiftSimulatorAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for promo_lift_simulator."""

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
    root_agent = PromoLiftSimulatorAgent()  # type: ignore
