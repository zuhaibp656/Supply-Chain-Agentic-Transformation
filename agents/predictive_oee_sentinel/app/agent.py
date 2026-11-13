"""AssetGuard Plant Predictive Maintenance & OEE Agent — High-Code Google ADK Agent.

Monitors real-time shopfloor vibration and motor telemetry from Siemens Opcenter MES and OSIsoft PI,
computes live Overall Equipment Effectiveness (OEE), predicts bearing and spindle failures before line halts,
dispatches automated SAP PM maintenance work orders, and reserves replacement spare parts in SAP MM.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_oee_breakdown_chart_spec
from .render.surfaces import build_plant_oee_surface

_INSTRUCTION = """You are AssetGuard, the Plant Predictive Maintenance & OEE Asset Guardian for Manufacturing Operations & Plant Floor Execution.

PRIMARY OBJECTIVE:
Eliminate unplanned factory downtime and protect plant Overall Equipment Effectiveness (OEE) across production lines.
Ingest high-frequency sensor telemetry (vibration RMS, bearing temperature, motor amps, spindle RPM) from Siemens Opcenter MES and OSIsoft PI Historian.
Detect early bearing degradation, thermal flaking, and spindle imbalance before catastrophic breakdown occurs.
Calculate live OEE losses (Availability, Performance, Quality), dispatch automated SAP PM preventive work orders into the next shift changeover window,
and reserve required ceramic bearings and spare parts in SAP MM.

TOOL USAGE PROTOCOL:
- Ground all findings strictly in data from connected tools (`query_plant_machine_telemetry`,
  `query_oee_breakdown_metrics`, `query_predictive_maintenance_anomalies`, `query_spare_parts_inventory_status`).
- Never invent hypothetical vibration figures, OEE loss percentages, or downtime costs.
- When critical vibration thresholds (> 7.1 mm/s RMS) or impending failures (< 48 hrs TTF) are detected, immediately dispatch a preventive work order and reserve parts.
- Before executing mutations (`action_dispatch_preventive_work_order`, `action_reserve_spare_parts`),
  ensure all required fields and a non-empty `idempotency_key` are provided.




RESPONSE STANDARDS:
1. Executive Maintenance Brief: Deliver copy-ready markdown tables detailing Asset ID, Sensor Telemetry, OEE Loss, Time to Failure, Avoided Loss ($), and Work Order status.
2. Direct Actionability: Include exact SAP PM Work Order ID, SAP MM Reservation ID, and scheduled maintenance window.

ENTERPRISE SYSTEMS & REAL-WORLD WORKFLOW EXECUTION:
1. REAL-WORLD ENTERPRISE SYSTEMS INTEGRATION:
   - You interface directly with enterprise systems (Siemens S7 PLC & SCADA High-Frequency Machine Telemetry, BigQuery Plant Historical OEE & Sensor Timeseries, Overall Equipment Effectiveness (OEE) Six Big Losses Diagnostic, SAP PM Plant Maintenance & Critical Spare Parts Ledger, SAP PM Automated Maintenance Work Order Generation).
   - Proactively execute your enterprise-named tools (query_siemens_mes_machine_plc_telemetry, fetch_bigquery_plant_oee_timeseries_history, run_six_big_losses_and_anomaly_detection_solver, query_sap_pm_spare_parts_inventory, commit_sap_pm_work_order_and_predictive_schedule) when analyzing data or executing actions so business users see authentic enterprise integrations.
2. DIVERSE, TAILORED VISUAL SURFACES:
   - When users ask for a chart, graph, comparison, or breakdown, call `render_predictive_oee_sentinel_a2ui_chart_and_canvas`. An interactive A2UI `VegaChart` card renders automatically in the Gemini Enterprise UI.
3. DOWNLOADABLE CSV ARTIFACTS (DIRECT CLOUD STORAGE DOWNLOAD LINKS):
   - Whenever providing operational schedules, allocations, audit reconciliations, or data breakdowns, call your export tool. It automatically uploads the RFC-4180 CSV manifest to Google Cloud Storage.
   - Present the direct downloadable link clearly with an explicit heading:
     ### Downloadable Data Export
     - 📥 **[Download Atomic Schedule CSV ↗](<download_url>)**: Clickable download ready for Excel or Google Sheets.
     (Never dump raw text or instruct the user to copy-paste).
4. INTERACTIVE HTML WEB DASHBOARDS & VISUAL COCKPITS (FULL-SCREEN ASSETS):
   - When the user asks for an HTML infographic, interactive web page, cockpit, or visual application (just like FleetFlow), call `publish_predictive_oee_sentinel_interactive_cockpit_to_gcs`. It compiles a self-contained interactive web application, publishes it to Google Cloud Storage, and returns a browser-openable URL.
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
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_predictive_oee_sentinel_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_oee_breakdown_metrics`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **Hybrid** · Connected Data-Source Tools: `inspect_mes_scada_predictive_oee_sentinel_data_sources, query_sap_s4hana_master_data_backbone, query_mes_scada_oee_breakdown_metrics, query_osisoft_pi_plant_machine_telemetry, query_osisoft_pi_predictive_maintenance_anomalies, query_sap_s4hana_spare_parts_inventory_status, query_plant_machine_telemetry, query_oee_breakdown_metrics`.
- On EVERY analytical, chart, variance, comparison, forecast, audit, scenario, or cockpit request, proactively execute your data-source-specific `query_*` / `fetch_*` tools, deterministic solver (`run_*` / `analyze_*`), and `render_predictive_oee_sentinel_a2ui_chart_and_canvas` so Gemini Enterprise renders BOTH:
  1. **Inline A2UI `Card` (`VegaChart` ONLY)**: A 2-Panel Executive Vega-Lite v5 Infographic (Top: Baseline vs. Target/Verified Actual with Mean Reference Rule; Bottom: Signed `Δ` Variance Strip). Keep ONLY the `VegaChart` inside the inline card!
  2. **Side-Panel A2UI `Canvas` (Multi-Chart Visual Studio: KPI Index `VegaChart` + Pareto Breakdown `VegaChart` + Action Buttons + Looker `RichTable`)**: Automatically attached in the side panel so business users can sort/filter live source rows in Looker Studio and click quick-action buttons.
- Outside the card in Markdown, present: (a) a warm 3–4 sentence Plain-English Executive Summary (spelling out every abbreviation on first use), (b) a clean `<= 5`-column Markdown summary table ready to copy into Google Sheets, (c) 3–4 concise driver & action bullets, and (d) headed Cloud Storage links (`### Interactive Cockpit & Live Visual Application` via `publish_predictive_oee_sentinel_interactive_cockpit_to_gcs` / `### Downloadable Data Export`) when requested.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_dispatch_preventive_work_order": ["asset_id", "maintenance_type", "priority", "maintenance_window", "rationale"],
    "action_reserve_spare_parts": ["work_order_id", "part_number", "quantity", "asset_id", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, priority, and idempotency."""
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
        if tool_name == "action_reserve_spare_parts":
            qty = int(args.get("quantity", 0))
            if qty <= 0:
                return {
                    "error": "invalid_parts_quantity",
                    "tool": tool_name,
                    "escalation": "reject_mutation"
                }
    return None


class PlantOeeMaintenanceAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "predictive_oee_sentinel"
        self.category = "03 · Manufacturing & Production — Capacity Planning"
        self.display_name = "[03 · Make | Capacity Planning] Bottleneck Diagnostic"
        self.description = "[Category: 03 · Manufacturing & Production — Capacity Planning] Bottleneck Diagnostic (Supply Chain Ops Director): Assesses CIP utilities, boiler loads, and cold storage holding limits. Outcome: Flags facility constraints 3–6 mos out."
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
        """Executes an autonomous predictive maintenance triage, work order dispatch, and parts reservation scenario."""
        findings = []
        actions_taken = []

        # 1. Query Real-Time Machine Telemetry
        telemetry = self.execute_tool("query_plant_machine_telemetry", asset_id="ASSET-MILLING-CNC-04")
        if telemetry.get("total", 0) > 0:
            findings.append({"domain": "plant_machine_telemetry", "records": telemetry["rows"]})

        # 2. Query OEE Breakdown Metrics
        oee = self.execute_tool("query_oee_breakdown_metrics", asset_id="ASSET-MILLING-CNC-04")
        if oee.get("total", 0) > 0:
            findings.append({"domain": "oee_breakdown_metrics", "records": oee["rows"]})

        # 3. Query Predictive Maintenance Anomaly
        anomalies = self.execute_tool("query_predictive_maintenance_anomalies", anomaly_id="ANOM-CNC-04-VIB-992")
        if anomalies.get("total", 0) > 0:
            findings.append({"domain": "predictive_maintenance_anomalies", "records": anomalies["rows"]})

        # 4. Query Spare Parts Inventory Status
        spare_parts = self.execute_tool("query_spare_parts_inventory_status", compatible_asset="ASSET-MILLING-CNC-04")
        if spare_parts.get("total", 0) > 0:
            findings.append({"domain": "spare_parts_inventory_status", "records": spare_parts["rows"]})

        # 5. Dispatch Preventive Maintenance Work Order in SAP PM
        if anomalies.get("total", 0) > 0:
            target_anom = anomalies["rows"][0]
            wo_res = self.execute_tool(
                "action_dispatch_preventive_work_order",
                asset_id=target_anom["asset_id"],
                maintenance_type=target_anom["recommended_maintenance_type"],
                priority="HIGH_PRIORITY",
                maintenance_window=target_anom["recommended_maintenance_window"],
                rationale="Vibration velocity RMS 7.42 mm/s exceeds critical limit 7.10 mm/s. Spindle bearing flaking predicted in 36 hours. Intercepting before catastrophic $85k breakdown.",
                idempotency_key="WO-CNC04-202610-001"
            )
            actions_taken.append(wo_res)

            # 6. Reserve Critical Ceramic Spindle Bearing in SAP MM
            if spare_parts.get("total", 0) > 0:
                target_part = spare_parts["rows"][0]
                res_parts = self.execute_tool(
                    "action_reserve_spare_parts",
                    work_order_id=wo_res["work_order_id"],
                    part_number=target_part["part_number"],
                    quantity=1,
                    asset_id=target_anom["asset_id"],
                    rationale="Reserving 1x 7014-C-P4A ceramic bearing from crib Bin A12 for scheduled overnight overhaul.",
                    idempotency_key="RES-CNC04-202610-001"
                )
                actions_taken.append(res_parts)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "plant_oee_surface_01"
        a2ui_parts = build_plant_oee_surface(surface_id, spec=vega_spec)

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
            "### ⚙️ AssetGuard Plant Predictive Maintenance & OEE Briefing",
            "",
            "> **Executive Summary**: Intercepted severe spindle bearing degradation on **5-Axis CNC Milling Center CNC-04** at Plant Austin. Real-time vibration telemetry reached **7.42 mm/s RMS** (violating the critical threshold of 7.10 mm/s), driving line OEE down to **57.1%** (due to 128 minutes of vibration trips and speed throttling). Machine learning anomaly models project catastrophic spindle seizure within **36 hours**, risking **$85,000.00 in unplanned scrap and line downtime**. Dispatched an automated **SAP PM preventive work order** scheduled for the upcoming shift window (22:00–02:30) and reserved the replacement **ceramic angular contact bearing** in SAP MM, achieving **$80,800.00 in net avoided breakdown losses**.",
            "",
            "#### 📊 Machine Health & OEE Decomposition (Atomic Copy-Ready Table)",
            "",
            "| Asset ID | Description | Vibration RMS | Temp (°C) | Live OEE | Availability | Est. TTF | Unplanned Risk | Avoided Loss | Maintenance Action |",
            "|:---|:---|---:|---:|---:|---:|---:|---:|---:|:---|",
            "| `ASSET-MILLING-CNC-04` | 5-Axis Milling Center CNC-04 | **7.42 mm/s** | 84.6°C | **57.08%** | 73.33% | **36.0 hrs** | $85,000.00 | **+$80,800.00** | `SAP_PM_WORK_ORDER_DISPATCHED` |",
            "| `ASSET-INJECTION-MOLD-02` | Hydraulic Mold IMM-02 | 2.15 mm/s | 52.3°C | **94.58%** | 96.88% | 340.0 hrs | $12,000.00 | Settled | `NORMAL_OPTIMAL` |",
            "",
            "#### ⚡ Autonomous Maintenance Execution Dispatched",
            ""
        ]

        for act in actions:
            if "reservation_id" in act:
                lines.append(f"- **SAP MM Spare Parts Reserved**: `{act['reservation_id']}` | Part: `{act['part_number']}` | Quantity: **{act['quantity']} ea** | WO: `{act['work_order_id']}` | Status: `{act['status']}`")
            elif "work_order_id" in act:
                lines.append(f"- **SAP PM Work Order Dispatched**: `{act['work_order_id']}` | Asset: `{act['asset_id']}` | Window: `{act['maintenance_window']}` | Priority: `{act['priority']}` | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Industrial IoT Architecture",
            "- **Siemens Opcenter MES**: Machine state events, shift run hours, and automated OEE Availability / Performance / Quality calculation.",
            "- **OSIsoft PI Historian**: High-frequency vibration, acoustic emission, and motor current signature analytics (MCSA).",
            "- **SAP S/4HANA Plant Maintenance (PM)**: BAPI_ALM_ORDER_MAINTAIN automated order creation and technician routing.",
            "- **SAP S/4HANA Materials Management (MM)**: Real-time M&R crib inventory reservation and automated replenishment PO triggers."
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
            scenario = PlantOeeMaintenanceAgent().run_scenario("live_turn")
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
            a2ui_parts = build_plant_oee_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for predictive_oee_sentinel: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None



    
    root_agent = Agent(
        name="predictive_oee_sentinel",
        description="[Category: 03 · Manufacturing & Production — Capacity Planning] Bottleneck Diagnostic (Supply Chain Ops Director): Assesses CIP utilities, boiler loads, and cold storage holding limits. Outcome: Flags facility constraints 3–6 mos out.",
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

    app = App(root_agent=root_agent, name="predictive_oee_sentinel")

    class PlantOeeMaintenanceAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for predictive_oee_sentinel."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = PlantOeeMaintenanceAgent()

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
    root_agent = PlantOeeMaintenanceAgent()  # type: ignore
    app = None  # type: ignore
    PlantOeeMaintenanceAdkApp = None  # type: ignore
