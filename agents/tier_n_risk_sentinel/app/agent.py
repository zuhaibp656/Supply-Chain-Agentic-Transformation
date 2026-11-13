"""NexusShield Multi-Tier Supply Network Sentinel — High-Code Google ADK Agent.

Maps Tier-1 through Tier-4 supplier dependencies in Cloud Spanner Graph,
traces BOM revenue at risk during geopolitical or climate disruptions,
and autonomously drafts backup dual-source PO splits and MEIO buffer increases.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_tier_risk_radar_spec
from .render.surfaces import build_tier_risk_surface

_INSTRUCTION = """You are NexusShield, the Multi-Tier Supply Network Sentinel for Strategic Sourcing & Tier-N Risk.

PRIMARY OBJECTIVE:
Eliminate the blindspot of Tier-2 through Tier-4 sub-supplier disruptions where 65% of supply chain shocks originate.
Maintain an enterprise knowledge graph in Cloud Spanner Graph mapping component lineage to bill-of-materials (BOM) and finished goods.
Ingest live cyclone, seismic, and port congestion feeds via Google DeepMind WeatherNext 3, compute exact revenue at risk,
and execute autonomous dual-source PO splits and MEIO safety buffer surges 11 days ahead of factory line-down impact.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_subtier_network_nodes`,
  `query_active_disruption_threats`, `query_bom_revenue_lineage`, `query_mitigation_playbook_options`).
- Never invent hypothetical supplier node names, revenue at risk figures, or cyclone categories.
- When single-source Tier-3/Tier-4 chokepoints face severe disruption, prioritize dual-source PO split execution.
- Before executing mutations (`action_dispatch_dual_source_po_split`, `action_surge_meio_safety_buffer`),
  ensure all required fields and non-empty `idempotency_key` are provided.




RESPONSE STANDARDS:
1. Executive Risk Brief: Deliver copy-ready markdown tables detailing Threat, Impacted Node, Echelon Tier, Finished SKUs, Revenue at Risk, and Days to Impact.
2. Direct Actionability: Include the exact PO split reallocation percentage, secondary supplier, and safety buffer days increased.

ENTERPRISE SYSTEMS & REAL-WORLD WORKFLOW EXECUTION:
1. REAL-WORLD ENTERPRISE SYSTEMS INTEGRATION:
   - You interface directly with enterprise systems (Cloud Spanner Graph Multi-Tier BOM Lineage, Dun & Bradstreet Financial Health & Credit Ratings, BigQuery Geopolitical & Port Strike Threat Indices, Tier-N Revenue Vulnerability & Single-Source Detector, SAP Ariba Dual-Sourcing Allocation & Safety Stock Order).
   - Proactively execute your enterprise-named tools (query_spanner_graph_subtier_supplier_lineage, fetch_dun_bradstreet_financial_health_ratings, query_bigquery_geopolitical_and_port_risk_indices, run_tier_n_bom_revenue_vulnerability_solver, commit_dual_sourcing_allocation_to_sap_ariba) when analyzing data or executing actions so business users see authentic enterprise integrations.
2. DIVERSE, TAILORED VISUAL SURFACES:
   - When users ask for a chart, graph, comparison, or breakdown, call `render_tier_n_risk_sentinel_a2ui_chart_and_canvas`. An interactive A2UI `VegaChart` card renders automatically in the Gemini Enterprise UI.
3. DOWNLOADABLE CSV ARTIFACTS (DIRECT CLOUD STORAGE DOWNLOAD LINKS):
   - Whenever providing operational schedules, allocations, audit reconciliations, or data breakdowns, call your export tool. It automatically uploads the RFC-4180 CSV manifest to Google Cloud Storage.
   - Present the direct downloadable link clearly with an explicit heading:
     ### Downloadable Data Export
     - 📥 **[Download Atomic Schedule CSV ↗](<download_url>)**: Clickable download ready for Excel or Google Sheets.
     (Never dump raw text or instruct the user to copy-paste).
4. INTERACTIVE HTML WEB DASHBOARDS & VISUAL COCKPITS (FULL-SCREEN ASSETS):
   - When the user asks for an HTML infographic, interactive web page, cockpit, or visual application (just like FleetFlow), call `publish_tier_n_risk_sentinel_interactive_cockpit_to_gcs`. It compiles a self-contained interactive web application, publishes it to Google Cloud Storage, and returns a browser-openable URL.
   - Present the direct clickable link clearly with an explicit heading:
     ### Interactive Cockpit & Live Visual Application
     - 🌐 **[Open Interactive Cockpit (Full-Screen) ↗](<view_url>)**: Click to launch the full-screen interactive web application with live scenario sliders, drill-downs, and simulation.

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
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_tier_n_risk_sentinel_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_active_disruption_threats`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **Hybrid** · Connected Data-Source Tools: `inspect_cloud_spanner_tier_n_risk_sentinel_data_sources, query_sap_s4hana_master_data_backbone, query_weathernext_active_disruption_threats, query_cloud_spanner_bom_finished_good_lineage, query_meio_buffer_mitigation_playbook_options, query_cloud_spanner_subtier_supplier_network, query_subtier_network_nodes, query_active_disruption_threats`.
- On EVERY analytical, chart, variance, comparison, forecast, audit, scenario, or cockpit request, proactively execute your data-source-specific `query_*` / `fetch_*` tools, deterministic solver (`run_*` / `analyze_*`), and `render_tier_n_risk_sentinel_a2ui_chart_and_canvas` so Gemini Enterprise renders BOTH:
  1. **Inline A2UI `Card` (`VegaChart` ONLY)**: A 2-Panel Executive Vega-Lite v5 Infographic (Top: Baseline vs. Target/Verified Actual with Mean Reference Rule; Bottom: Signed `Δ` Variance Strip). Keep ONLY the `VegaChart` inside the inline card!
  2. **Side-Panel A2UI `Canvas` (Multi-Chart Visual Studio: KPI Index `VegaChart` + Pareto Breakdown `VegaChart` + Action Buttons + Looker `RichTable`)**: Automatically attached in the side panel so business users can sort/filter live source rows in Looker Studio and click quick-action buttons.
- Outside the card in Markdown, present: (a) a warm 3–4 sentence Plain-English Executive Summary (spelling out every abbreviation on first use), (b) a clean `<= 5`-column Markdown summary table ready to copy into Google Sheets, (c) 3–4 concise driver & action bullets, and (d) headed Cloud Storage links (`### Interactive Cockpit & Live Visual Application` via `publish_tier_n_risk_sentinel_interactive_cockpit_to_gcs` / `### Downloadable Data Export`) when requested.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_dispatch_dual_source_po_split": ["playbook_id", "backup_supplier", "reallocation_split_pct", "target_po_reallocation_units", "rationale"],
    "action_surge_meio_safety_buffer": ["playbook_id", "sku_ids", "days_buffer_increase", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, buffer limits, and idempotency."""
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
        if tool_name == "action_surge_meio_safety_buffer":
            days = float(args.get("days_buffer_increase", 0))
            if days <= 0 or days > 30.0:
                return {
                    "error": "days_buffer_increase_out_of_bounds",
                    "min_days": 1.0,
                    "max_days": 30.0,
                    "requested_days": days,
                    "escalation": "request_buffer_verification"
                }
    return None


class TierNRiskSentinelAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "tier_n_risk_sentinel"
        self.category = "02 · Sourcing & Procurement — Supplier Network"
        self.display_name = "[02 · Source | Supplier Network] Disruption Sensing Agent"
        self.description = "[Category: 02 · Sourcing & Procurement — Supplier Network] Disruption Sensing Agent (Procurement Dir. / Risk Mgr): Monitors multi-tier supply feeds, port delays, and vendor financials. Outcome: 2–3 week advance disruption warning."
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
        """Executes an autonomous sub-tier risk detection, BOM revenue tracing, and PO mitigation scenario."""
        findings = []
        actions_taken = []

        # 1. Detect Active Weather / Geopolitical Threat
        threats = self.execute_tool("query_active_disruption_threats", threat_id="THREAT-CYCLONE-QLD-01")
        if threats.get("total", 0) > 0:
            findings.append({"domain": "active_threats", "records": threats["rows"]})

        # 2. Query Sub-Tier Network Nodes in Spanner Graph
        nodes = self.execute_tool("query_subtier_network_nodes", node_id="NODE-WEIPA-BAUXITE-AU")
        if nodes.get("total", 0) > 0:
            findings.append({"domain": "subtier_nodes", "records": nodes["rows"]})

        # 3. Trace Exposed Finished Goods & Revenue at Risk
        lineage = self.execute_tool("query_bom_revenue_lineage", impacted_node="NODE-WEIPA-BAUXITE-AU")
        if lineage.get("total", 0) > 0:
            findings.append({"domain": "bom_revenue_lineage", "records": lineage["rows"]})

        # 4. Query Mitigation Playbook Options
        playbooks = self.execute_tool("query_mitigation_playbook_options", threat_id="THREAT-CYCLONE-QLD-01")
        if playbooks.get("total", 0) > 0:
            findings.append({"domain": "mitigation_playbooks", "records": playbooks["rows"]})

        # 5. Dispatch Dual-Source PO Volume Reallocation in SAP S/4HANA
        po_res = self.execute_tool(
            "action_dispatch_dual_source_po_split",
            playbook_id="PB-DUAL-SOURCE-ALUM",
            backup_supplier="Hydro Aluminium (NO)",
            reallocation_split_pct=50.0,
            target_po_reallocation_units=4500000,
            rationale="Reallocate 50% ingot demand to backup qualified Norwegian smelter to bypass Australian cyclone disruption.",
            idempotency_key="SPLIT-ALUM-202610-001"
        )
        actions_taken.append(po_res)

        # 6. Surge MEIO Safety Buffers across Regional DCs
        buffer_res = self.execute_tool(
            "action_surge_meio_safety_buffer",
            playbook_id="PB-DUAL-SOURCE-ALUM",
            sku_ids=["SKU-BEV-ISOTONIC-32OZ", "SKU-BEV-ELECTROLYTE-500ML"],
            days_buffer_increase=7.0,
            rationale="Raise regional DC safety buffer from 16.5 days to 23.5 days (+7 days) to absorb maritime transshipment lag.",
            idempotency_key="SURGE-ALUM-202610-001"
        )
        actions_taken.append(buffer_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "tier_risk_surface_01"
        a2ui_parts = build_tier_risk_surface(surface_id, spec=vega_spec)

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
            "### 🛡️ NexusShield Multi-Tier Supply Network Risk Briefing",
            "",
            "> **Executive Summary**: Detected a **Category 4 Tropical Cyclone (11-day advance warning)** threatening the *Weipa Bauxite Mining & Refinery* in Queensland, Australia via **Google DeepMind WeatherNext 3**. Queried the multi-tier enterprise knowledge graph in **Cloud Spanner Graph** to traverse 4 supply chain echelons (Tier-4 Bauxite Mine &rarr; Tier-2 Smelter in Iceland &rarr; Tier-1 Can Plant in Colorado &rarr; Finished RTD Beverage). Traced **$18,243,000 revenue at risk** across 2 high-volume SKUs with only 16.5 days of line-side buffer remaining. Autonomously reallocated **50% of PO ingot volume (4.5M units) to Hydro Aluminium in Norway** and **surged regional MEIO safety buffers by +7.0 days**, preventing factory line-down with zero customer stockouts.",
            "",
            "#### 📊 Multi-Tier Sub-Supplier Disruption Ledger (Atomic Copy-Ready Table)",
            "",
            "| Tier Depth | Impacted Supplier Node | Country | Threat Trigger | Finished SKU Lineage | Revenue at Risk | Current Buffer | Advance Warning | Mitigation Action |",
            "|:---|:---|:---|:---|:---|---:|---:|---:|:---|",
            "| `Tier-4 Mine` | `Weipa Bauxite Refinery` | Australia | Category 4 Cyclone | `SKU-BEV-ISOTONIC-32OZ` | $13,455,000 | 16.5 Days | **+11 Days** | Dual-Source PO Split to Norway |",
            "| `Tier-4 Mine` | `Weipa Bauxite Refinery` | Australia | Category 4 Cyclone | `SKU-BEV-ELECTROLYTE-500ML` | $4,788,000 | 16.5 Days | **+11 Days** | +7.0 Days MEIO Buffer Surge |",
            "| `Tier-3 Chem` | `Showa Denko Chemical` | Japan | Seismic Precaution | `SKU-BEV-ELECTROLYTE-500ML` | $4,788,000 | 24.0 Days | +4 Days | Monitored / Stable |",
            "",
            "#### ⚡ Autonomous Risk Mitigations Executed",
            ""
        ]

        for act in actions:
            if "po_split_id" in act:
                lines.append(f"- **SAP S/4HANA PO Split Reallocated**: `{act['po_split_id']}` | Backup Supplier: **{act['backup_supplier']}** | Reallocation Split: **{act['reallocation_split_pct']}%** | Units: **{act['target_po_reallocation_units']:,}** | Status: `{act['status']}`")
            elif "buffer_id" in act:
                lines.append(f"- **MEIO Safety Stock Buffer Surged**: `{act['buffer_id']}` | Impacted SKUs: `{', '.join(act['sku_ids'])}` | Days Increase: **+{act['days_buffer_increase']} Days** | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Graph Architecture",
            "- **Cloud Spanner Multi-Tier Knowledge Graph**: Sub-tier vendor relationships inferred from customs Bill of Lading (BOL) and supplier declarations.",
            "- **Google DeepMind WeatherNext 3**: Real-time atmospheric cyclone tracking with 11-day advance predictive trajectory.",
            "- **SAP S/4HANA Strategic Sourcing**: BAPI_PO_CREATE1 writeback executing secondary supplier purchase order splits.",
            "- **Multi-Echelon Inventory Optimization (MEIO)**: Dynamic safety stock recalibration protecting finished goods OTIF."
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
        """Sanitizes prior A2UI wire parts and intercepts synthetic Canvas button clicks."""
        if llm_request is None:
            return None
        from .render.a2ui_builder import sanitize_history_and_intercept_actions
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
            scenario = TierNRiskSentinelAgent().run_scenario("live_turn")
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
            a2ui_parts = build_tier_risk_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for tier_n_risk_sentinel: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    
    root_agent = Agent(
        name="tier_n_risk_sentinel",
        description="[Category: 02 · Sourcing & Procurement — Supplier Network] Disruption Sensing Agent (Procurement Dir. / Risk Mgr): Monitors multi-tier supply feeds, port delays, and vendor financials. Outcome: 2–3 week advance disruption warning.",
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

    app = App(root_agent=root_agent, name="tier_n_risk_sentinel")

    class TierNRiskSentinelAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for tier_n_risk_sentinel."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = TierNRiskSentinelAgent()

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
    root_agent = TierNRiskSentinelAgent()  # type: ignore
    app = None  # type: ignore
    TierNRiskSentinelAdkApp = None  # type: ignore
