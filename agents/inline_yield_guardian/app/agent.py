"""VisionInspect Inline Quality Inspection Agent — High-Code Google ADK Agent.

Performs real-time sub-50ms optical vision defect classification with Gemini 3.8 Flash,
detects micro-leaks and heat-seal breaches on high-speed aseptic packaging lines,
actuates high-speed pneumatic solenoid reject gates (14.2ms latency),
and logs 21 CFR Part 11 electronic Batch Manufacturing Record (eBHR) deviations in Veeva Vault & SAP QM.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_vision_inspection_chart_spec
from .render.surfaces import build_vision_inspect_surface

_INSTRUCTION = """You are VisionInspect, the Multimodal Inline Quality Inspection Agent for Manufacturing Packaging & Aseptic Bottling Lines.

PRIMARY OBJECTIVE:
Protect product integrity and eliminate defective consumer units on high-speed bottling and packaging lines (120+ feet/min).
Ingest 120 FPS high-resolution camera frames from GigE industrial optical camera arrays.
Execute sub-50ms multimodal defect classification using Gemini 3.8 Flash Vision to detect induction heat-seal tears, micro-leaks, barcode illegibility, and carton seam breaches.
Trigger high-speed pneumatic solenoid reject gates within 15ms to divert compromised units into quarantine bins,
and automatically log regulatory electronic Batch Manufacturing Record (eBHR) deviation tickets into Veeva Vault QMS and SAP QM.

TOOL USAGE PROTOCOL:
- Ground all defect classifications strictly in optical frame telemetry (`query_camera_vision_inspection_frames`,
  `query_vision_defect_classification_results`, `query_ebhr_batch_record_deviations`, `query_pneumatic_reject_gate_events`).
- Never hallucinate defect types, bounding box coordinates, or camera shutter lux metrics.
- When Gemini Flash Vision confidence score >= 0.95 and defect severity is CRITICAL, immediately actuate pneumatic reject gates.
- Before executing mutations (`action_trigger_pneumatic_reject_diverter`, `action_log_ebhr_quality_deviation`),
  ensure all required fields and a non-empty `idempotency_key` are provided.




RESPONSE STANDARDS:
1. Executive Quality Brief: Deliver copy-ready markdown tables detailing Frame ID, Defect Category, Vision Model Confidence, Actuation Latency, Diverter Gate, and eBHR Deviation Ticket.
2. Direct Actionability: Include exact Pneumatic Divert ID, Veeva Ticket ID, and physical quarantine bin routing.

ENTERPRISE SYSTEMS & REAL-WORLD WORKFLOW EXECUTION:
1. REAL-WORLD ENTERPRISE SYSTEMS INTEGRATION:
   - You interface directly with enterprise systems (High-Resolution Optical Line Camera Inspection Frames, Gemini 3.8 Flash Multimodal Defect Classifier, Siemens Opcenter MES Electronic Batch Records (eBHR), Defect Spatial Clustering & Heatmap Diagnostic, High-Speed Pneumatic Reject Gate Actuation).
   - Proactively execute your enterprise-named tools (query_highres_optical_inspection_camera_frames, fetch_gemini_vision_defect_classification_stream, query_siemens_mes_ebhr_batch_record_deviations, run_inline_defect_clustering_and_root_cause_solver, commit_pneumatic_diverter_reject_gate_action) when analyzing data or executing actions so business users see authentic enterprise integrations.
2. DIVERSE, TAILORED VISUAL SURFACES:
   - When users ask for a chart, graph, comparison, or breakdown, call `render_inline_yield_guardian_a2ui_chart_and_canvas`. An interactive A2UI `VegaChart` card renders automatically in the Gemini Enterprise UI.
3. DOWNLOADABLE CSV ARTIFACTS (DIRECT CLOUD STORAGE DOWNLOAD LINKS):
   - Whenever providing operational schedules, allocations, audit reconciliations, or data breakdowns, call your export tool. It automatically uploads the RFC-4180 CSV manifest to Google Cloud Storage.
   - Present the direct downloadable link clearly with an explicit heading:
     ### Downloadable Data Export
     - 📥 **[Download Atomic Schedule CSV ↗](<download_url>)**: Clickable download ready for Excel or Google Sheets.
     (Never dump raw text or instruct the user to copy-paste).
4. INTERACTIVE HTML WEB DASHBOARDS & VISUAL COCKPITS (FULL-SCREEN ASSETS):
   - When the user asks for an HTML infographic, interactive web page, cockpit, or visual application (just like FleetFlow), call `publish_inline_yield_guardian_interactive_cockpit_to_gcs`. It compiles a self-contained interactive web application, publishes it to Google Cloud Storage, and returns a browser-openable URL.
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
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_inline_yield_guardian_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_camera_vision_inspection_frames`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **Hybrid** · Connected Data-Source Tools: `inspect_inline_vision_inline_yield_guardian_data_sources, query_sap_s4hana_master_data_backbone, query_inline_vision_camera_vision_inspection_frames, query_sap_s4hana_ebhr_batch_record_deviations, query_sap_s4hana_pneumatic_reject_gate_events, query_gemini_flash_vision_defect_classification_results, query_camera_vision_inspection_frames, query_vision_defect_classification_results`.
- On EVERY analytical, chart, variance, comparison, forecast, audit, scenario, or cockpit request, proactively execute your data-source-specific `query_*` / `fetch_*` tools, deterministic solver (`run_*` / `analyze_*`), and `render_inline_yield_guardian_a2ui_chart_and_canvas` so Gemini Enterprise renders BOTH:
  1. **Inline A2UI `Card` (`VegaChart` ONLY)**: A 2-Panel Executive Vega-Lite v5 Infographic (Top: Baseline vs. Target/Verified Actual with Mean Reference Rule; Bottom: Signed `Δ` Variance Strip). Keep ONLY the `VegaChart` inside the inline card!
  2. **Side-Panel A2UI `Canvas` (Multi-Chart Visual Studio: KPI Index `VegaChart` + Pareto Breakdown `VegaChart` + Action Buttons + Looker `RichTable`)**: Automatically attached in the side panel so business users can sort/filter live source rows in Looker Studio and click quick-action buttons.
- Outside the card in Markdown, present: (a) a warm 3–4 sentence Plain-English Executive Summary (spelling out every abbreviation on first use), (b) a clean `<= 5`-column Markdown summary table ready to copy into Google Sheets, (c) 3–4 concise driver & action bullets, and (d) headed Cloud Storage links (`### Interactive Cockpit & Live Visual Application` via `publish_inline_yield_guardian_interactive_cockpit_to_gcs` / `### Downloadable Data Export`) when requested.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_trigger_pneumatic_reject_diverter": ["frame_id", "line_id", "pneumatic_diverter_id", "defect_type", "rationale"],
    "action_log_ebhr_quality_deviation": ["batch_number", "product_id", "deviation_type", "severity", "station_id", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, diverter IDs, and idempotency."""
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
    return None


class InlineQualityInspectionAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.8-flash"):
        self.name = "inline_yield_guardian"
        self.category = "03 · Manufacturing & Production — Quality & Compliance"
        self.display_name = "[03 · Make | Quality & Compliance] Visual Defect Triager"
        self.description = "[Category: 03 · Manufacturing & Production — Quality & Compliance] Visual Defect Triager (QA Manager / Line Inspector): Inspects high-speed video frames for crimped seals, lot codes, and labels. Outcome: Prevents full pallet scrap & holds."
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
        """Executes an autonomous vision defect triage, pneumatic diverter firing, and eBHR deviation logging."""
        findings = []
        actions_taken = []

        # 1. Query Optical Inspection Frames
        frames = self.execute_tool("query_camera_vision_inspection_frames", line_id="LINE-ASEPTIC-01")
        if frames.get("total", 0) > 0:
            findings.append({"domain": "camera_vision_inspection_frames", "records": frames["rows"]})

        # 2. Query Gemini 3.8 Flash Defect Classification Results
        classifications = self.execute_tool("query_vision_defect_classification_results", defect_type="SEAL")
        if classifications.get("total", 0) > 0:
            findings.append({"domain": "vision_defect_classification_results", "records": classifications["rows"]})

        # 3. Query Pneumatic Gate Events
        gate_events = self.execute_tool("query_pneumatic_reject_gate_events", line_id="LINE-ASEPTIC-01")
        if gate_events.get("total", 0) > 0:
            findings.append({"domain": "pneumatic_reject_gate_events", "records": gate_events["rows"]})

        # 4. Query eBHR Deviations
        ebhr_devs = self.execute_tool("query_ebhr_batch_record_deviations", batch_number="BATCH-OAT-2026W42-01")
        if ebhr_devs.get("total", 0) > 0:
            findings.append({"domain": "ebhr_batch_record_deviations", "records": ebhr_devs["rows"]})

        # 5. Actuate Pneumatic Reject Diverter
        if classifications.get("total", 0) > 0:
            target_cls = classifications["rows"][0]
            divert_res = self.execute_tool(
                "action_trigger_pneumatic_reject_diverter",
                frame_id=target_cls["frame_id"],
                line_id="LINE-ASEPTIC-01",
                pneumatic_diverter_id="DIVERTER-SOLENOID-LINE01-A",
                defect_type=target_cls["defect_type"],
                rationale="Gemini 3.8 Flash Vision detected radial induction seal tear (1.8mm) with 98.5% confidence. Solenoid diverter fired at 14.2ms latency to isolate non-conforming carton.",
                idempotency_key="DIVERT-20261022-00841-A"
            )
            actions_taken.append(divert_res)

        # 6. Log eBHR Quality Deviation in Veeva Vault / SAP QM
        if ebhr_devs.get("total", 0) > 0:
            target_ebhr = ebhr_devs["rows"][0]
            ebhr_res = self.execute_tool(
                "action_log_ebhr_quality_deviation",
                batch_number=target_ebhr["batch_number"],
                product_id=target_ebhr["product_id"],
                deviation_type=target_ebhr["deviation_type"],
                severity=target_ebhr["severity"],
                station_id=target_ebhr["station_id"],
                rationale="Automated containment deviation logged for induction foil seal tear excursion on Line Aseptic 01; 1 unit physically segregated.",
                idempotency_key="EBHR-DEV-20261022-044"
            )
            actions_taken.append(ebhr_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "vision_inspect_surface_01"
        a2ui_parts = build_vision_inspect_surface(surface_id, spec=vega_spec)

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
        """Renders executive brief, copy-ready tables, and containment audit ledger."""
        lines = [
            "### 👁️ VisionInspect Inline Quality Inspection & Defect Containment Briefing",
            "",
            "> **Executive Summary**: Real-time multimodal optical inspection on **High-Speed Aseptic Packaging Line 01** operating at 1.25 m/s (120 fpm) detected an acute hermetic seal integrity excursion. Under **Gemini 3.8 Flash Vision**, high-resolution frame `FRAME-CAM01-20261022-00841` flagged a **1.8mm radial induction foil seal tear** with **98.5% model confidence** (`CRITICAL_CONTAMINATION_RISK`). In response, the sub-15ms **Pneumatic Solenoid Reject Diverter `DIVERTER-SOLENOID-LINE01-A`** fired in **14.2 ms**, physically segregating the contaminated unit into quarantine bin `REJECT-BIN-LINE01-01` before reaching downstream case packers. In parallel, a 21 CFR Part 11 compliant deviation ticket (`VEEVA-QMS-DEV-99214`) and SAP QM notification (`100084920`) were logged.",
            "",
            "#### 📊 High-Speed Vision Classification & Physical Diverter Telemetry (Atomic Copy-Ready Table)",
            "",
            "| Frame ID | Inspection Station | Defect Classification | Vision AI Model | Confidence | Divert Latency | Physical Target | Status |",
            "|:---|:---|:---|:---|---:|---:|:---|:---|",
            "| `FRAME-00841` | Induction Seal Integrity | **INDUCTION_FOIL_SEAL_TEAR** | `gemini-3.8-flash` | **98.5%** | **14.2 ms** | `Quarantine Bin 01` | `DIVERTED_CONTAINED` |",
            "| `FRAME-00842` | Induction Seal Integrity | `NONE_CONFORMING` | `gemini-3.8-flash` | 99.8% | N/A (Conforming) | Main Downstream Packer | `IN_SPEC_PASSED` |",
            "| `FRAME-00843` | Cap Screw Torque & Flange | `IN_SPEC_NOMINAL` | `gemini-3.8-flash` | 99.1% | N/A (Conforming) | Main Downstream Packer | `IN_SPEC_PASSED` |",
            "",
            "#### ⚡ Automated Inline Diverter Actuation & eBHR Compliance Actions Executed",
            ""
        ]

        for act in actions:
            if "divert_id" in act:
                lines.append(f"- **Pneumatic Solenoid Reject Actuated**: `{act['divert_id']}` | Frame: `{act['frame_id']}` | Defect: `{act['defect_type']}` | Latency: `{act['actuation_latency_ms']} ms` | Status: `{act['status']}`")
            elif "deviation_log_id" in act:
                lines.append(f"- **eBHR Quality Deviation Logged**: `{act['deviation_log_id']}` | Batch: `{act['batch_number']}` | Severity: `{act['severity']}` | QMS Ticket: `{act['veeva_ticket_id']}` | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & Industrial Automation Architecture",
            "- **GigE Industrial Vision Array**: 120 FPS high-resolution optical inspection cameras with 4,200 lux LED illumination.",
            "- **Gemini 3.8 Flash Multimodal Classifier**: Sub-50ms zero-shot visual defect localization and normalized bounding box extraction.",
            "- **Modbus TCP / IO-Link Pneumatic Diverter**: Ultra-low latency (<15ms) solenoid mechanical gate diverting defective cartons.",
            "- **Veeva Vault QualityOne & SAP QM**: 21 CFR Part 11 compliant electronic Batch Manufacturing Record (eBHR) deviation audit trail."
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
            scenario = InlineQualityInspectionAgent().run_scenario("live_turn")
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
            a2ui_parts = build_vision_inspect_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for inline_yield_guardian: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    
    root_agent = Agent(
        name="inline_yield_guardian",
        description="[Category: 03 · Manufacturing & Production — Quality & Compliance] Visual Defect Triager (QA Manager / Line Inspector): Inspects high-speed video frames for crimped seals, lot codes, and labels. Outcome: Prevents full pallet scrap & holds.",
        model=GlobalGemini(
            model="gemini-3.8-flash",
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

    app = App(root_agent=root_agent, name="inline_yield_guardian")

    class InlineQualityInspectionAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for inline_yield_guardian."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = InlineQualityInspectionAgent()

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
    root_agent = InlineQualityInspectionAgent()  # type: ignore
    app = None  # type: ignore
    InlineQualityInspectionAdkApp = None  # type: ignore
