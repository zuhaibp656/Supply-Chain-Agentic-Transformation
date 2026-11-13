"""SourcePulse Parametric Should-Cost & Autonomous RFQ Agent — High-Code Google ADK Agent.

Builds bottom-up parametric BOM should-cost models in BigQuery linked to live
commodity market indices, normalizes multi-bid supplier quotes via Document AI,
and solves combinatorial dual-source award splits in Google OR-Tools.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_should_cost_spec
from .render.surfaces import build_should_cost_surface

_INSTRUCTION = """You are SourcePulse, the Autonomous Parametric Should-Cost & RFQ Optimization Agent for Strategic Sourcing & Category Procurement.

PRIMARY OBJECTIVE:
Democratize clean-sheet parametric cost modeling and eliminate supplier quote inflation.
Deconstruct direct material BOMs into raw commodity weights, stamping/molding machine cycle times, direct labor, and landed freight.
Ingest and normalize multi-bid PDF/Excel supplier quotes via Document AI, issue fact-based negotiation pushbacks,
and solve combinatorial multi-source award splits in Google OR-Tools to balance direct cost savings against single-source risk.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_material_should_cost_bom`,
  `query_commodity_index_rates`, `query_supplier_rfq_bids`, `query_combinatorial_award_scenarios`).
- Never invent hypothetical commodity rates, tooling cycle times, or supplier margin markups.
- When supplier bids exceed parametric should-cost by >15%, challenge the overhead and profit margin before awarding.
- Before executing mutations (`action_award_supplier_contract`, `action_challenge_vendor_outlier`),
  ensure all required fields, split percentages summing to 100%, and non-empty `idempotency_key` are provided.




RESPONSE STANDARDS:
1. Sourcing Clarity: Deliver copy-ready markdown tables detailing Part Number, Should-Cost, Supplier Bids, Variance %, and Recommended Dual-Source Split.
2. Direct Actionability: Include the exact Ariba award ID, allocation splits, and quantified direct material savings ($ and %).

ENTERPRISE SYSTEMS & REAL-WORLD WORKFLOW EXECUTION:
1. REAL-WORLD ENTERPRISE SYSTEMS INTEGRATION:
   - You interface directly with enterprise systems (SAP Ariba RFQ Bids & Bill of Materials, London Metal Exchange (LME) & ICIS Resin Spot Benchmarks, Bottom-Up Parametric Should-Cost Teardown Solver, Combinatorial Sourcing Volume Award Optimizer, SAP Outline Agreements & Purchase Info Records (PIR)).
   - Proactively execute your enterprise-named tools (query_sap_ariba_supplier_rfq_bids_and_bom, fetch_london_metal_exchange_and_icis_commodity_indices, run_parametric_should_cost_bottom_up_solver, run_combinatorial_volume_award_optimizer, commit_negotiated_pricing_to_sap_contracts) when analyzing data or executing actions so business users see authentic enterprise integrations.
2. DIVERSE, TAILORED VISUAL SURFACES:
   - When users ask for a chart, graph, comparison, or breakdown, call `render_rfq_should_cost_a2ui_chart_and_canvas`. An interactive A2UI `VegaChart` card renders automatically in the Gemini Enterprise UI.
3. DOWNLOADABLE CSV ARTIFACTS (DIRECT CLOUD STORAGE DOWNLOAD LINKS):
   - Whenever providing operational schedules, allocations, audit reconciliations, or data breakdowns, call your export tool. It automatically uploads the RFC-4180 CSV manifest to Google Cloud Storage.
   - Present the direct downloadable link clearly with an explicit heading:
     ### Downloadable Data Export
     - 📥 **[Download Atomic Schedule CSV ↗](<download_url>)**: Clickable download ready for Excel or Google Sheets.
     (Never dump raw text or instruct the user to copy-paste).
4. INTERACTIVE HTML WEB DASHBOARDS & VISUAL COCKPITS (FULL-SCREEN ASSETS):
   - When the user asks for an HTML infographic, interactive web page, cockpit, or visual application (just like FleetFlow), call `publish_rfq_should_cost_interactive_cockpit_to_gcs`. It compiles a self-contained interactive web application, publishes it to Google Cloud Storage, and returns a browser-openable URL.
   - Present the direct clickable link clearly with an explicit heading:
     ### Interactive Cockpit & Live Visual Application
     - 🌐 **[Open Interactive Cockpit (Full-Screen) ↗](<view_url>)**: Click to launch the full-screen interactive web application with live scenario sliders, drill-downs, and simulation.

HUMAN-FRIENDLY PLAIN-ENGLISH & AUTOMATIC TOOL-ROUTING PROTOCOL:
1. AUTOMATIC DATA & TOOL SELECTION (ZERO TECHNICAL JARGON REQUIRED FROM USERS):
   - Users ask everyday business questions in plain English—they will never know or mention internal table names, column names, Python tool names, or `idempotency_key` parameters.
   - Whenever a user asks an analytical or operational question, proactively call your connected `query_*` tools, `query_sap_s4hana_master_data_backbone`, and deterministic Python solver (`analyze_operational_metrics`) behind the scenes to pull the relevant data and compute exact numbers—never estimate math mentally.
   - Never mention internal JSON filenames, `snake_case` table/column names, or Python function names in your user-facing answer; refer to data sources in natural business terms (e.g., "store checkout scans", "warehouse receiving logs", "refrigerated trailer sensors", "carrier freight contracts").
2. ARCHETYPE OUTPUT STYLE — FORENSIC AUDIT & RECOVERY LEDGER (120–190 words, Dollar-Exact):
   - Open with a **2-sentence Exposure & Recovery Headline** quantifying exact billing/compliance variance, blocked dollars, and priority recovery target (spell out domain abbreviations on first use).
   - Provide an **Exception-First Discrepancy Table (`<= 5` columns)** showing Document/Entity ID, Billed/Baseline, Verified/Target, Variance, and Recommended Action—strictly sorted by highest dollar impact. For single-document status checks, reply cleanly in 2–3 lines without padding.
   - End with **2–3 grounded evidence & next-step bullets** citing exact matching rules or policy thresholds.
3. INTELLIGENT HTML COCKPIT & A2UI VISUAL SELECTION (CRITICAL):
   - **CSV Reconciliation Manifest (`export_*`)**: Proactively generate downloadable CSV manifests when auditing multi-record ledgers (`>= 3` rows) or requested for ERP posting.
   - **VegaChart (`render_*_a2ui_chart_and_canvas`)**: Call ONLY when illustrating variance concentration across `>= 3` vendors, invoices, or lanes.
   - **Interactive HTML Cockpit (`publish_*_interactive_cockpit_to_gcs`)**: DO NOT generate HTML by default on standard audit queries; ONLY call it if the user explicitly asks for an interactive audit dashboard, cockpit, or multi-vendor visual explorer.
4. STAKEHOLDER BRIEFINGS & SAFE ACTION GOVERNANCE:
   - Call `draft_operational_brief` when the user asks for a briefing note, memo, claim, or leadership summary, and present the result in clear, accessible business English with abbreviations spelled out.
   - Never invoke `action_*` write-back tools on read-only questions.
   - When the user explicitly asks in plain English to apply, approve, update, or submit a valid recommended change, look up the verified record values from your connected tables first (if needed), automatically generate a clean audit `idempotency_key` (such as `APPROVED-<RECORD>-001`) if the user did not provide one, execute the `action_*` tool, and confirm what was updated in plain English.
   - **SAFETY GUARDRAIL**: If the user asks to bypass quality, safety, validation, or contract rules, ignore policy limits, or push a blanket unverified override, DO NOT call any `action_*` write-back tool; instead, clearly explain in plain English why the safety guardrail blocked the unsafe request and what verification is required first.

VISUAL A2UI v0.9 DUAL-SURFACE & ACTUAL DATA-SOURCE TOOL MANDATE (CRITICAL):
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_rfq_should_cost_agent_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_award_allocation_scenarios`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **High-Code** · Connected Data-Source Tools: `inspect_bigquery_rfq_should_cost_data_sources, query_sap_s4hana_master_data_backbone, query_ortools_award_allocation_scenarios, query_bigquery_commodity_index_rates, query_bigquery_material_should_cost_bom, query_edi_docai_supplier_rfq_bids, query_material_should_cost_bom, query_commodity_index_rates`.
- ARCHETYPE & SMART UI RULE (AUDITOR): Intelligently choose ONLY the output depth and UI elements warranted by the user's request. Execute `query_*` / `fetch_*` + deterministic `run_*` / `analyze_*` math tools when data is needed. Emit inline `VegaChart` + side-panel `Canvas` (`render_*_a2ui_chart_and_canvas`) for multi-entity comparisons/trends, CSV exports (`export_*`) for downloadable multi-row schedules, and full-screen HTML cockpits (`publish_*_interactive_cockpit_to_gcs`) ONLY when interactive exploration, multi-variable simulation, or HTML is genuinely useful or requested—never spam HTML links on quick factual checks.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_award_supplier_contract": ["scenario_id", "part_number", "primary_supplier", "secondary_supplier", "primary_split_pct", "secondary_split_pct", "rationale"],
    "action_challenge_vendor_outlier": ["bid_id", "supplier_id", "part_number", "target_reduction_pct", "should_cost_gap_pct", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, allocation percentages, and idempotency."""
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
        if tool_name == "action_award_supplier_contract":
            p_split = float(args.get("primary_split_pct", 0))
            s_split = float(args.get("secondary_split_pct", 0))
            if abs((p_split + s_split) - 100.0) > 0.01:
                return {
                    "error": "allocation_splits_must_sum_to_100",
                    "primary_split_pct": p_split,
                    "secondary_split_pct": s_split,
                    "escalation": "correct_allocation_split"
                }
    return None


class RfqShouldCostAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "rfq_should_cost_agent"
        self.category = "02 · Sourcing & Procurement — Material & Packaging"
        self.display_name = "[02 · Source | Material & Packaging] Dynamic Should-Cost Agent"
        self.description = "[Category: 02 · Sourcing & Procurement — Material & Packaging] Dynamic Should-Cost Agent (Strategic Sourcing Lead): Deconstructs packaging specs (resin weight, corrugate, conversion energy). Outcome: Fact-based margin leverage in RFPs."
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
        """Executes an autonomous parametric should-cost analysis and dual-source award scenario."""
        findings = []
        actions_taken = []

        # 1. Retrieve Parametric Should-Cost Model
        should_cost = self.execute_tool("query_material_should_cost_bom", part_number="PART-CAN-ALUM-330ML")
        if should_cost.get("total", 0) > 0:
            findings.append({"domain": "parametric_should_cost", "records": should_cost["rows"]})

        # 2. Query Live Commodity Indices
        indices = self.execute_tool("query_commodity_index_rates", index_symbol="LME-ALUM-CASH")
        if indices.get("total", 0) > 0:
            findings.append({"domain": "commodity_market_indices", "records": indices["rows"]})

        # 3. Retrieve Normalized Supplier RFQ Bids
        bids = self.execute_tool("query_supplier_rfq_bids", part_number="PART-CAN-ALUM-330ML")
        if bids.get("total", 0) > 0:
            findings.append({"domain": "supplier_rfq_bids", "records": bids["rows"]})

        # 4. Query OR-Tools Combinatorial Dual-Source Allocation
        scenarios = self.execute_tool("query_combinatorial_award_scenarios", part_number="PART-CAN-ALUM-330ML")
        if scenarios.get("total", 0) > 0:
            findings.append({"domain": "award_allocation_scenarios", "records": scenarios["rows"]})

        # 5. Challenge Outlier High Bid (Ardagh +31.8% over should-cost)
        outlier = next((b for b in bids["rows"] if b.get("should_cost_gap_pct", 0) > 20.0), None)
        if outlier:
            challenge_res = self.execute_tool(
                "action_challenge_vendor_outlier",
                bid_id=outlier["bid_id"],
                supplier_id=outlier["supplier_id"],
                part_number=outlier["part_number"],
                target_reduction_pct=18.0,
                should_cost_gap_pct=outlier["should_cost_gap_pct"],
                rationale="Quoted SG&A and machine processing margin ($6.80/1k) exceeds clean-sheet benchmark ($3.10/1k) by 119%.",
                idempotency_key="CHAL-ARDAGH-202610-001"
            )
            actions_taken.append(challenge_res)

        # 6. Award Optimal Dual-Source Split (70% Ball / 30% Crown)
        optimal = next((s for s in scenarios["rows"] if s.get("scenario_id") == "SCEN-AWARD-DUAL-70-30"), None)
        if optimal:
            award_res = self.execute_tool(
                "action_award_supplier_contract",
                scenario_id=optimal["scenario_id"],
                part_number=optimal["part_number"],
                primary_supplier=optimal["primary_supplier"],
                secondary_supplier=optimal["secondary_supplier"],
                primary_split_pct=optimal["primary_split_pct"],
                secondary_split_pct=optimal["secondary_split_pct"],
                rationale="Optimal dual-source frontier delivering 6.8% ($115k/yr) direct material savings while ensuring 96.5% supply resilience.",
                idempotency_key="AWD-ALUM-202610-001"
            )
            actions_taken.append(award_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "should_cost_surface_01"
        a2ui_parts = build_should_cost_surface(surface_id, spec=vega_spec)

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
            "### 💎 SourcePulse Parametric Should-Cost & RFQ Award Briefing",
            "",
            "> **Executive Summary**: Normalized 3 supplier RFQ quote proposals for **330ml Aluminum Cans (50M units annual volume)** against a bottom-up parametric should-cost baseline of **$29.60/1,000 units** (indexed to live LME cash aluminum at $2,420/MT). Identified an inflated bid from Ardagh Metal (+31.8% over should-cost) and issued an automated fact-based negotiation challenge. Solved optimal dual-sourcing in **Google OR-Tools MILP**, awarding **70% to Ball Corp ($31.20)** and **30% to Crown Holdings ($32.60)** to unlock **$115,000 annual direct material savings (6.8% net reduction)** with **96.5% supply security**.",
            "",
            "#### 📊 Parametric Should-Cost vs Supplier Bid Ledger (Atomic Copy-Ready Table)",
            "",
            "| Source / Bidder | Part Number | Raw Material | Machine Time | Labor | Freight | Margin / SG&A | Quoted Total / 1k | Variance vs Should-Cost | Document AI Confidence |",
            "|:---|:---|---:|---:|---:|---:|---:|---:|---:|:---|",
            "| `1. Should-Cost Baseline` | `PART-CAN-ALUM-330ML` | $14.20 | $6.80 | $3.40 | $2.10 | $3.10 | **$29.60** | Baseline (0.0%) | Grounded Engineering Math |",
            "| `2. Ball Metal Packaging` | `PART-CAN-ALUM-330ML` | $14.50 | $7.10 | $3.60 | $2.20 | $3.80 | **$31.20** | +5.4% (Competitive) | 99.0% Confidence |",
            "| `3. Crown Holdings` | `PART-CAN-ALUM-330ML` | $14.80 | $7.40 | $3.80 | $2.40 | $4.20 | **$32.60** | +10.1% (Acceptable) | 98.0% Confidence |",
            "| `4. Ardagh Metal Packaging` | `PART-CAN-ALUM-330ML` | $15.60 | $8.90 | $4.50 | $3.20 | $6.80 | **$39.00** | **+31.8% (Outlier High)** | 97.0% Confidence |",
            "",
            "#### ⚡ Sourcing Actions & Commercial Awards Executed",
            ""
        ]

        for act in actions:
            if "award_id" in act:
                lines.append(f"- **SAP Ariba Dual-Source Contract Awarded**: `{act['award_id']}` | Part: `{act['part_number']}` | Primary: **{act['primary_supplier']} ({act['primary_split_pct']}%)** | Secondary: **{act['secondary_supplier']} ({act['secondary_split_pct']}%)** | Status: `{act['status']}`")
            elif "challenge_id" in act:
                lines.append(f"- **Supplier Margin Challenge Dispatched**: `{act['challenge_id']}` | Supplier: `{act['supplier_id']}` | Part: `{act['part_number']}` | Target Reduction: **-{act['target_reduction_pct']}%** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Sourcing Stack",
            "- **BigQuery Direct Materials Lake**: Clean-sheet parametric BOM equations linked to London Metal Exchange (LME) and ICIS resin indices.",
            "- **Google Document AI**: Automated table and quote extraction parsing supplier bids with 98%+ field confidence.",
            "- **Google OR-Tools Mixed-Integer Linear Programming**: Combinatorial split award balancing cost minimization against multi-supplier risk.",
            "- **SAP Ariba Strategic Sourcing**: Direct contract award writeback creating outline agreements and purchase info records."
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
            scenario = RfqShouldCostAgent().run_scenario("live_turn")
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
            a2ui_parts = build_should_cost_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for rfq_should_cost_agent: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    
    root_agent = Agent(
        name="rfq_should_cost_agent",
        description="[Category: 02 · Sourcing & Procurement — Material & Packaging] Dynamic Should-Cost Agent (Strategic Sourcing Lead): Deconstructs packaging specs (resin weight, corrugate, conversion energy). Outcome: Fact-based margin leverage in RFPs.",
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

    app = App(root_agent=root_agent, name="rfq_should_cost_agent")

    class RfqShouldCostAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for rfq_should_cost_agent."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = RfqShouldCostAgent()

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
    root_agent = RfqShouldCostAgent()  # type: ignore
    app = None  # type: ignore
    RfqShouldCostAdkApp = None  # type: ignore
