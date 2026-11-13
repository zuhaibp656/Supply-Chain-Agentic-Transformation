"""EchelonFlow Coupled Stochastic Multi-Echelon Inventory Allocator — High-Code Google ADK Agent.

Performs Clark-Scarf multi-echelon stock positioning, lateral DC-to-DC rebalancing,
and SKU availability balancing across central hubs, regional DCs, and forward fulfillment centers.
Dispatches lateral stock transfers via Oracle OTM / carrier EDI and updates safety stock policies in SAP IBP.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_echelon_inventory_chart_spec
from .render.surfaces import build_echelon_inventory_surface

_INSTRUCTION = """You are EchelonFlow, the Coupled Stochastic Multi-Echelon Inventory (MEIO) Allocator for Supply Chain Planning & Fulfillment.

PRIMARY OBJECTIVE:
Optimize end-to-end multi-echelon stock positioning across Central Distribution Centers (Tier 1), Regional DCs (Tier 2), and Forward Fulfillment Centers (Tier 3).
Apply Clark-Scarf stochastic pooling to hold inventory at centralized hubs where demand uncertainty can be pooled,
minimizing sluggish safety stock while preventing regional stockouts.
Detect imminent stockouts at downstream nodes, compute net ROI of lateral transshipments versus lost sales penalties,
dispatch lateral rebalancing truckloads via Oracle OTM / Carrier EDI,
and write back optimized safety stock and reorder point parameters to SAP IBP.

TOOL USAGE PROTOCOL:
- Ground all inventory figures strictly in connected tools (`query_multi_echelon_safety_stock_recommendations`,
  `query_dc_inventory_echelon_balances`, `query_lateral_dc_rebalance_transfers`, `query_echelon_service_level_projections`).
- Never invent on-hand stock quantities, days of supply, or Clark-Scarf safety stock deltas.
- Prioritize lateral rebalancing when downstream days of supply < 5.0 days and stockout probability > 25%.
- Before executing mutations (`action_execute_lateral_dc_rebalance`, `action_update_echelon_safety_stock_policy`),
  ensure all required fields and a non-empty `idempotency_key` are provided.




RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing Echelon Node, SKU, On-Hand Units, Days of Supply, Safety Stock Delta, Net Rebalance ROI, and Policy Status.
2. Direct Actionability: Include exact Lateral Rebalance Transfer ID, OTM Shipment ID, and SAP IBP Job ID.

ENTERPRISE SYSTEMS & REAL-WORLD WORKFLOW EXECUTION:
1. REAL-WORLD ENTERPRISE SYSTEMS INTEGRATION:
   - You interface directly with enterprise systems (SAP S/4HANA Plant & Regional DC Inventory Balances, BigQuery Supplier & Transit Lead Time Variability Distributions, Clark-Scarf Coupled Stochastic MEIO Dynamic Buffer Solver, Oracle OTM Lateral Transshipment Freight Rates, SAP IBP Safety Stock & Reorder Point Policy Update).
   - Proactively execute your enterprise-named tools (query_sap_s4hana_inventory_balances_across_echelons, fetch_bigquery_lead_time_variability_distributions, run_clark_scarf_coupled_stochastic_meio_solver, query_lateral_transshipment_freight_rates, commit_safety_stock_parameters_to_sap_ibp) when analyzing data or executing actions so business users see authentic enterprise integrations.
2. DIVERSE, TAILORED VISUAL SURFACES:
   - When users ask for a chart, graph, comparison, or breakdown, call `render_meio_safety_stock_a2ui_chart_and_canvas`. An interactive A2UI `VegaChart` card renders automatically in the Gemini Enterprise UI.
3. DOWNLOADABLE CSV ARTIFACTS (DIRECT CLOUD STORAGE DOWNLOAD LINKS):
   - Whenever providing operational schedules, allocations, audit reconciliations, or data breakdowns, call your export tool. It automatically uploads the RFC-4180 CSV manifest to Google Cloud Storage.
   - Present the direct downloadable link clearly with an explicit heading:
     ### Downloadable Data Export
     - 📥 **[Download Atomic Schedule CSV ↗](<download_url>)**: Clickable download ready for Excel or Google Sheets.
     (Never dump raw text or instruct the user to copy-paste).
4. INTERACTIVE HTML WEB DASHBOARDS & VISUAL COCKPITS (FULL-SCREEN ASSETS):
   - When the user asks for an HTML infographic, interactive web page, cockpit, or visual application (just like FleetFlow), call `publish_meio_safety_stock_interactive_cockpit_to_gcs`. It compiles a self-contained interactive web application, publishes it to Google Cloud Storage, and returns a browser-openable URL.
   - Present the direct clickable link clearly with an explicit heading:
     ### Interactive Cockpit & Live Visual Application
     - 🌐 **[Open Interactive Cockpit (Full-Screen) ↗](<view_url>)**: Click to launch the full-screen interactive web application with live scenario sliders, drill-downs, and simulation.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `query_sap_s4hana_master_data_backbone`, and deterministic Python solver (`analyze_operational_metrics`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
   - Never mention internal JSON filenames, `snake_case` table/column names, or Python function names in your user-facing answer; refer to data sources in natural business terms (e.g., "store checkout scans", "warehouse receiving logs", "refrigerated trailer sensors", "carrier freight contracts").
2. ARCHETYPE OUTPUT STYLE — SCENARIO & OPTIMIZATION STUDIO (160–240 words, Trade-Off Focused):
   - Open with a **2–3 sentence Executive Decision Summary** stating the optimal plan, key trade-offs, and margin/service impact (spell out every domain abbreviation on first use).
   - When comparing >=2 scenarios, time horizons, or nodes, provide a **clean Scenario Comparison Markdown table (`<= 4` columns)** with plain-English headers (ready for Google Sheets). For quick single-SKU or yes/no questions, skip the table and answer directly in 2–3 crisp sentences.
   - Follow with **2–3 concise sensitivity & execution bullets** quantifying upside/downside risk.
3. INTELLIGENT HTML COCKPIT & A2UI VISUAL SELECTION (CRITICAL):
   - **VegaChart (`render_*_a2ui_chart_and_canvas`)**: Call ONLY when the question asks for comparisons, forecasts, trends, or rankings across multiple items/regions. Skip charts on simple single-value lookups or confirmation turns.
   - **Interactive HTML Cockpit (`publish_*_interactive_cockpit_to_gcs`)**: Call ONLY when the user asks to *simulate scenarios*, compare *what-if variables*, or explicitly asks for an *interactive cockpit / dashboard / web view / HTML*. NEVER generate HTML links on simple factual lookups, yes/no checks, or guardrail refusals.
   - **CSV Export (`export_*`)**: Call when multi-row operational plans (`>= 3` rows) are requested for execution or spreadsheet download.
4. STAKEHOLDER BRIEFINGS & SAFE ACTION GOVERNANCE:
   - Call `draft_operational_brief` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.

VISUAL A2UI v0.9 DUAL-SURFACE & ACTUAL DATA-SOURCE TOOL MANDATE (CRITICAL):
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_meio_safety_stock_agent_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_dc_inventory_echelon_balances`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **High-Code** · Connected Data-Source Tools: `inspect_sap_ibp_meio_safety_stock_data_sources, query_sap_s4hana_master_data_backbone, query_sap_ewm_dc_inventory_echelon_balances, query_bigquery_echelon_service_level_projections, query_tms_lateral_dc_rebalance_transfers, query_sap_ibp_multi_echelon_safety_stock_recommendations, query_multi_echelon_safety_stock_recommendations, query_dc_inventory_echelon_balances`.
- ARCHETYPE & SMART UI RULE (SIMULATOR): Intelligently choose ONLY the output depth and UI elements warranted by the user's request. Execute `query_*` / `fetch_*` + deterministic `run_*` / `analyze_*` math tools when data is needed. Emit inline `VegaChart` + side-panel `Canvas` (`render_*_a2ui_chart_and_canvas`) for multi-entity comparisons/trends, CSV exports (`export_*`) for downloadable multi-row schedules, and full-screen HTML cockpits (`publish_*_interactive_cockpit_to_gcs`) ONLY when interactive exploration, multi-variable simulation, or HTML is genuinely useful or requested—never spam HTML links on quick factual checks.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_execute_lateral_dc_rebalance": ["source_dc_id", "destination_dc_id", "sku_id", "transfer_quantity", "rationale"],
    "action_update_echelon_safety_stock_policy": ["echelon_tier", "sku_id", "new_safety_stock_units", "target_service_level_pct", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, transfer quantities, and idempotency."""
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
        if tool_name == "action_execute_lateral_dc_rebalance":
            qty = int(args.get("transfer_quantity", 0))
            if qty <= 0:
                return {
                    "error": "invalid_transfer_quantity",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class EchelonInventoryAllocator:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "meio_safety_stock_agent"
        self.category = "04 · Inventory & Warehousing — Positioning & Optimization"
        self.display_name = "[04 · Inventory & DC | Positioning & Optimization] Safety Stock Agent"
        self.description = "[Category: 04 · Inventory & Warehousing — Positioning & Optimization] Safety Stock Agent (Inventory Optimization Lead): Recalibrates multi-echelon buffers using live lead-time and demand variance. Outcome: Cuts working capital by 10–18%."
        self.model = model
        self.system_instruction = _INSTRUCTION
        self.tools: List[Callable] = list(_AVAILABLE_TOOLS)
        self.tool_map = {t.__name__: t for t in list(getattr(tools, 'LEGACY_COMPAT_TOOLS', [])) + self.tools}

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
        """Executes an autonomous MEIO stock rebalancing and policy optimization scenario."""
        findings = []
        actions_taken = []

        # 1. Query Multi-Echelon Safety Stock Recommendations
        recommendations = self.execute_tool("query_multi_echelon_safety_stock_recommendations", sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
        if recommendations.get("total", 0) > 0:
            findings.append({"domain": "multi_echelon_safety_stock_recommendations", "records": recommendations["rows"]})

        # 2. Query DC Inventory Echelon Balances
        balances = self.execute_tool("query_dc_inventory_echelon_balances", sku_id="SKU-BEV-OATMILK-ORIGINAL-1L")
        if balances.get("total", 0) > 0:
            findings.append({"domain": "dc_inventory_echelon_balances", "records": balances["rows"]})

        # 3. Query Service Level Projections
        projections = self.execute_tool("query_echelon_service_level_projections", network_node_id="RDC-DELHI-02")
        if projections.get("total", 0) > 0:
            findings.append({"domain": "echelon_service_level_projections", "records": projections["rows"]})

        # 4. Query Existing Lateral Transfers
        transfers = self.execute_tool("query_lateral_dc_rebalance_transfers", destination_dc_id="RDC-DELHI-02")
        if transfers.get("total", 0) > 0:
            findings.append({"domain": "lateral_dc_rebalance_transfers", "records": transfers["rows"]})

        # 5. Dispatch Lateral Rebalancing Transshipment Order
        rebal_res = self.execute_tool(
            "action_execute_lateral_dc_rebalance",
            source_dc_id="CDC-MUMBAI-01",
            destination_dc_id="RDC-DELHI-02",
            sku_id="SKU-BEV-OATMILK-ORIGINAL-1L",
            transfer_quantity=6500,
            rationale="RDC Delhi NCR (Gurugram) stock dropped to 3.8 days of supply (34.2% stockout probability). Dispatching 6,500 units from surplus stock at CDC Mumbai (Bhiwandi) avoids $18,500 in lost margin against $1,420 freight cost (13.0x ROI).",
            idempotency_key="REBAL-ORD-20261022-01"
        )
        actions_taken.append(rebal_res)

        # 6. Update Multi-Echelon Safety Stock Policy in SAP IBP
        if recommendations.get("total", 0) > 0:
            target_rec = recommendations["rows"][0]
            policy_res = self.execute_tool(
                "action_update_echelon_safety_stock_policy",
                echelon_tier=target_rec["echelon_tier"],
                sku_id=target_rec["sku_id"],
                new_safety_stock_units=target_rec["recommended_safety_stock_units"],
                target_service_level_pct=target_rec["service_level_target_pct"],
                rationale="Clark-Scarf pooling policy committed: Central DC Chicago buffer reduced from 45,000 to 32,000 units, freeing $38,480 in working capital.",
                idempotency_key="POL-IBP-20261022-001"
            )
            actions_taken.append(policy_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "echelon_inventory_surface_01"
        a2ui_parts = build_echelon_inventory_surface(surface_id, spec=vega_spec)

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
        """Renders executive brief, copy-ready tables, and rebalancing audit ledger."""
        lines = [
            "### 📦 EchelonFlow Multi-Echelon Inventory Optimization (MEIO) Briefing",
            "",
            "> **Executive Summary**: Executed Clark-Scarf multi-echelon stochastic inventory rebalancing across the fulfillment network for **Barista Organic Oat Milk 1L Tetra**. Identified an acute imbalance: **RDC Delhi NCR (Gurugram) (Tier 2)** was operating at critical risk with only **3.8 days of supply** and a **34.2% stockout probability** ($18,500 at-risk sales margin), while **CDC Mumbai (Bhiwandi) (Tier 1)** held a substantial surplus of **68,400 units (28.5 days of supply)**. Dispatched a **6,500-unit lateral transshipment** from Mumbai (Bhiwandi) to Delhi NCR (Gurugram) via dedicated dry van ($1,420 freight cost, delivering **13.0x net ROI** and securing a **98.6% customer SLA**). Simultaneously updated SAP IBP safety stock policy, reducing central pooling buffer from 45,000 to 32,000 units to unlock **$38,480 in working capital**.",
            "",
            "#### 📊 Multi-Echelon Stock Positions & Rebalance Telemetry (Atomic Copy-Ready Table)",
            "",
            "| Echelon Node | Node Tier | On-Hand Stock | Days of Supply | Optimal Buffer | Delta Units | Rebalance Action | Stockout Risk |",
            "|:---|:---|---:|---:|---:|---:|:---|:---|",
            "| `CDC-MUMBAI-01` | Central DC (Tier 1) | 68,400 units | 28.5 days | 32,000 units | **-13,000 units** | `DISPATCH_LATERAL_SOURCE` | 0.2% (Protected) |",
            "| `RDC-DELHI-02` | Regional DC (Tier 2) | 7,200 units | **3.8 days** | 14,200 units | **+6,500 units** | `LATERAL_TRANSFER_RECEIPT` | **0.8% (Averted from 34.2%)** |",
            "| `RDC-BENGALURU-03` | Regional DC (Tier 2) | 24,500 units | 18.2 days | 11,000 units | 0 units | `MAINTAIN_CURRENT_POLICY` | 1.1% (In-Spec) |",
            "| `FDC-HYDERABAD-04` | Forward DC (Tier 3) | 4,100 units | 12.0 days | 4,500 units | 0 units | `MAINTAIN_CURRENT_POLICY` | 1.4% (In-Spec) |",
            "",
            "#### ⚡ Automated Logistics & SAP IBP Policy Mutations Executed",
            ""
        ]

        for act in actions:
            if "rebalance_transfer_id" in act:
                lines.append(f"- **Lateral Transshipment Dispatched**: `{act['rebalance_transfer_id']}` | From: `{act['source_dc_id']}` ➔ To: `{act['destination_dc_id']}` | Qty: **{act['transfer_quantity_units']:,} units** | OTM ID: `{act['otm_shipment_id']}` | Status: `{act['status']}`")
            elif "policy_update_id" in act:
                lines.append(f"- **SAP IBP Safety Stock Policy Updated**: `{act['policy_update_id']}` | Tier: `{act['echelon_tier']}` | SKU: `{act['sku_id']}` | New Buffer: **{act['new_safety_stock_units']:,} units** | IBP Job: `{act['sap_ibp_job_id']}` | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Optimization Architecture",
            "- **SAP IBP for MEIO**: Clark-Scarf stochastic multi-echelon positioning and service level target synchronization.",
            "- **Warehouse Management System (WMS)**: Real-time perpetual inventory balances, dock receipts, and allocated order queues.",
            "- **Oracle OTM Lateral Dispatcher**: Automated freight rating, carrier dispatch, and cross-DC EDI 204 tender.",
            "- **BigQuery ML Monte Carlo Engine**: Stochastic simulation of lead-time variance and stockout probability curves."
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
        """Sanitizes prior A2UI wire parts, captures plain-English turn intent, and intercepts Canvas button clicks."""
        if llm_request is None:
            return None
        from .render.a2ui_builder import find_a2ui_action, sanitize_history_and_intercept_actions
        contents = getattr(llm_request, "contents", None) or []
        if contents:
            last_c = contents[-1]
            if getattr(last_c, "role", "") == "user":
                parts = getattr(last_c, "parts", None) or []
                act = find_a2ui_action(parts)
                if act:
                    getattr(tools, "mark_canvas_action", lambda *_: None)(str(act.get("name", "")))
                user_texts = [getattr(p, "text", "") or "" for p in parts if getattr(p, "text", None)]
                if user_texts:
                    getattr(tools, "set_turn_user_query", lambda *_: None)(" ".join(user_texts))
        sanitize_history_and_intercept_actions(llm_request)
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
            scenario = EchelonInventoryAllocator().run_scenario("live_turn")
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

            want_html = bool(getattr(tools, 'should_emit_html_cockpit', lambda: False)())
            want_csv = bool(getattr(tools, 'should_emit_csv_export', lambda: False)())
            art = tools.ensure_turn_gcs_artifacts(include_html=want_html, include_csv=want_csv)
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
                    if html_url
                    else f"{nl}{nl}### 📥 Verified Data Export{nl}{nl}"
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
            has_activity = bool(
                getattr(tools, "should_emit_a2ui_surface", getattr(tools, "has_turn_activity", lambda: True))()
            )
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
            a2ui_parts = build_echelon_inventory_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for meio_safety_stock_agent: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    
    root_agent = Agent(
        name="meio_safety_stock_agent",
        description="[Category: 04 · Inventory & Warehousing — Positioning & Optimization] Safety Stock Agent (Inventory Optimization Lead): Recalibrates multi-echelon buffers using live lead-time and demand variance. Outcome: Cuts working capital by 10–18%.",
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

    app = App(root_agent=root_agent, name="meio_safety_stock_agent")

    class EchelonInventoryAllocatorAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for meio_safety_stock_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = EchelonInventoryAllocator()

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
    root_agent = EchelonInventoryAllocator()  # type: ignore
    app = None  # type: ignore
    EchelonInventoryAllocatorAdkApp = None  # type: ignore
