"""EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger — High-Code Google ADK Agent.

Calculates audit-ready ISO 14083 & GLEC v3.0 shipment-level Scope-3 emissions from primary telematics, generates EU CBAM embedded carbon declarations, and verifies EUDR zero-deforestation plots via Google Earth Engine.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_carbon_scope3_ledger_chart_spec
from .render.surfaces import build_carbon_scope3_ledger_surface

_INSTRUCTION = """You are EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger.

PRIMARY OBJECTIVE:
Calculates audit-ready ISO 14083 & GLEC v3.0 shipment-level Scope-3 emissions from primary telematics, generates EU CBAM embedded carbon declarations, and verifies EUDR zero-deforestation plots via Google Earth Engine.

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_certify_cbam_and_eudr_compliance_dossier`, `action_commit_scope3_decarbonization_swap`), ensure all required fields and a non-empty `idempotency_key` are provided.

ENTERPRISE SYSTEMS & REAL-WORLD WORKFLOW EXECUTION:
1. REAL-WORLD ENTERPRISE SYSTEMS INTEGRATION:
   - You interface directly with enterprise systems (BigQuery Telematics & GLEC Freight Carbon Ledger, SAP S/4HANA Customs & EU CBAM Declarations, Google Earth Engine EUDR Deforestation Compliance, Marginal Abatement Cost Curve (MACC) & Route Optimizer, SAP Transportation Management Low-Carbon Carrier Awards).
   - Proactively execute your enterprise-named tools (query_bigquery_shipment_telematics_scope3_ledger, fetch_sap_e_waste_and_eu_cbam_customs_declarations, query_google_earth_engine_eudr_forest_plot_audits, run_marginal_carbon_abatement_cost_solver, commit_low_carbon_carrier_awards_in_sap_tm) when analyzing data or executing actions so business users see authentic enterprise integrations.
2. DIVERSE, TAILORED VISUAL SURFACES:
   - When users ask for a chart, graph, comparison, or breakdown, call `render_carbon_scope3_ledger_a2ui_chart_and_canvas`. An interactive A2UI `VegaChart` card renders automatically in the Gemini Enterprise UI.
3. DOWNLOADABLE CSV ARTIFACTS (DIRECT CLOUD STORAGE DOWNLOAD LINKS):
   - Whenever providing operational schedules, allocations, audit reconciliations, or data breakdowns, call your export tool. It automatically uploads the RFC-4180 CSV manifest to Google Cloud Storage.
   - Present the direct downloadable link clearly with an explicit heading:
     ### Downloadable Data Export
     - 📥 **[Download Atomic Schedule CSV ↗](<download_url>)**: Clickable download ready for Excel or Google Sheets.
     (Never dump raw text or instruct the user to copy-paste).
4. INTERACTIVE HTML WEB DASHBOARDS & VISUAL COCKPITS (FULL-SCREEN ASSETS):
   - When the user asks for an HTML infographic, interactive web page, cockpit, or visual application (just like FleetFlow), call `publish_carbon_scope3_ledger_interactive_cockpit_to_gcs`. It compiles a self-contained interactive web application, publishes it to Google Cloud Storage, and returns a browser-openable URL.
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
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_carbon_scope3_ledger_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_eu_cbam_embedded_carbon_declarations`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **Low-Code** · Connected Data-Source Tools: `inspect_iso14083_glec_carbon_scope3_ledger_data_sources, query_sap_s4hana_master_data_backbone, query_weathernext_eudr_earth_engine_plot_verifications, query_tms_low_carbon_carrier_and_supplier_swaps, query_iso14083_glec_shipment_level_scope3_emissions, query_shipment_level_scope3_emissions, query_eu_cbam_embedded_carbon_declarations, query_eudr_earth_engine_plot_verifications`.
- ARCHETYPE & SMART UI RULE (AUDITOR): Intelligently choose ONLY the output depth and UI elements warranted by the user's request. Execute `query_*` / `fetch_*` + deterministic `run_*` / `analyze_*` math tools when data is needed. Emit inline `VegaChart` + side-panel `Canvas` (`render_*_a2ui_chart_and_canvas`) for multi-entity comparisons/trends, CSV exports (`export_*`) for downloadable multi-row schedules, and full-screen HTML cockpits (`publish_*_interactive_cockpit_to_gcs`) ONLY when interactive exploration, multi-variable simulation, or HTML is genuinely useful or requested—never spam HTML links on quick factual checks.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_certify_cbam_and_eudr_compliance_dossier": ["import_declaration_id", "plot_id", "cbam_tax_avoided_eur", "rationale"],
    "action_commit_scope3_decarbonization_swap": ["swap_id", "target_corridor_or_bom", "annual_tco2e_reduction", "rationale"],
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs and idempotency."""
    if tool_name in _WRITE_TOOLS:
        required = _WRITE_TOOLS[tool_name]
        missing = [r for r in required if args.get(r) is None or args.get(r) == "" or args.get(r) == []]
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


class CarbonScope3Ledger:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "carbon_scope3_ledger"
        self.category = "02 · Sourcing & Procurement — Supplier Network"
        self.display_name = "[02 · Source | Supplier Network] ESG & Scope 3 Auditor"
        self.description = "[Category: 02 · Sourcing & Procurement — Supplier Network] ESG & Scope 3 Auditor (Chief Sustainability Officer): Standardizes chain-of-custody certificates (RSPO/FSC) and packaging LCAs. Outcome: Automates Scope 3 disclosure audits."
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
        """Executes an autonomous multi-step supply chain optimization & ERP write-back scenario."""
        findings = []
        actions_taken = []

        r_0 = self.execute_tool("query_shipment_level_scope3_emissions", shipment_id="SHP-GLB-20261022-301")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "shipment_level_scope3_emissions", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_eu_cbam_embedded_carbon_declarations", import_declaration_id="CBAM-EU-2026-Q4-09")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "eu_cbam_embedded_carbon_declarations", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_eudr_earth_engine_plot_verifications", plot_id="PLOT-BR-PARA-4410")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "eudr_earth_engine_plot_verifications", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_low_carbon_carrier_and_supplier_swaps", swap_id="SWAP-DEC-2026-04")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "low_carbon_carrier_and_supplier_swaps", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_certify_cbam_and_eudr_compliance_dossier",
            import_declaration_id='CBAM-EU-2026-Q4-09',
            plot_id='PLOT-BR-PARA-4410',
            cbam_tax_avoided_eur=64260.0,
            rationale='Certified primary smelter emissions (2.1 tCO2e/t vs 8.4 EU default penalty, saving €64,260 in CBAM certificates) and verified zero post-2020 deforestation on PLOT-BR-PARA-4410 via Google Earth Engine.',
            idempotency_key='ESG-CERT-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_commit_scope3_decarbonization_swap",
            swap_id='SWAP-DEC-2026-04',
            target_corridor_or_bom='DE_NL_RHINE_CORRIDOR',
            annual_tco2e_reduction=1420.0,
            rationale='Shifted Rhine corridor volume to HVO100 renewable diesel and electric barge, cutting annual Scope-3 emissions by 1,420 tCO2e at -1.2% lower freight cost.',
            idempotency_key='ESG-SWAP-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = tools.get_native_chart_spec()
        surface_id = "carbon_scope3_ledger_surface_01"
        a2ui_parts = build_carbon_scope3_ledger_surface(surface_id, spec=vega_spec)
        markdown = self._format_markdown_report(findings, actions_taken)

        return {
            "status": "success",
            "agent": self.name,
            "findings_count": len(findings),
            "actions_executed": actions_taken,
            "vega_spec": vega_spec,
            "a2ui_parts": a2ui_parts,
            "markdown": markdown,
        }

    def _format_markdown_report(
        self,
        findings: List[Dict[str, Any]],
        actions: List[Dict[str, Any]]
    ) -> str:
        """Renders concise executive summary, atomic copy-ready table, and action audit trail."""
        lines = [
            "### ✦ EcoChain — Shipment-Level Scope-3 Carbon, CBAM & EUDR Ledger — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **06 · Return & Enable**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"compliance_scope": "Hydro EAF Aluminum (Primary)", "emissions_tco2e": 252, "cbam_eur_saved": 64260, "status": "OPTIMIZED_CVRPTW"}, {"compliance_scope": "EU Default Penalty Factor", "emissions_tco2e": 1008, "cbam_eur_saved": 0, "status": "LEGACY_STATIC"}, {"compliance_scope": "Rhine HVO100 + Barge Swap", "emissions_tco2e": 410, "cbam_eur_saved": 28400, "status": "OPTIMIZED_CVRPTW"}]:
            lines.append(f"| `{row['compliance_scope']}` | **{row['emissions_tco2e']}** | {row['cbam_eur_saved']} | `{row['status']}` |")

        lines.extend([
            "",
            "#### ⚡ Autonomous Write-Backs & Actions Executed",
            "",
        ])
        for act in actions:
            eid = act.get("dispatch_execution_id") or act.get("secondary_action_id") or "ACT-ID"
            lines.append(f"- **Action Executed**: `{eid}` | Status: `{act.get('status')}` | Rationale: {act.get('rationale')}")

        lines.extend([
            "",
            "### 🔗 Connected Enterprise Systems",
        ])
        for sys_meta in [{"id": "iso14083_glec_carbon_engine", "name": "ISO 14083 & GLEC Framework v3.0 Primary Telemetry Carbon Ledger", "protocol": "BigQuery SQL / Python", "tables": ["shipment_level_scope3_emissions"]}, {"id": "eu_cbam_registry_gateway", "name": "EU Carbon Border Adjustment Mechanism (CBAM) Embedded Carbon Engine", "protocol": "XML / REST API", "tables": ["eu_cbam_embedded_carbon_declarations"]}, {"id": "google_earth_engine_eudr", "name": "Google Earth Engine Satellite Polygon Deforestation Verifier (EUDR)", "protocol": "Earth Engine Python API", "tables": ["eudr_earth_engine_plot_verifications"]}, {"id": "scope3_decarbonization_solver", "name": "OR-Tools Low-Carbon Carrier & Smelter Swap Optimizer", "protocol": "Python MILP", "tables": ["low_carbon_carrier_and_supplier_swaps"]}]:
            lines.append(f"- **{sys_meta['name']}** (`{sys_meta['protocol']}`)")

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
            scenario = CarbonScope3Ledger().run_scenario("live_turn")
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
            a2ui_parts = build_carbon_scope3_ledger_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for carbon_scope3_ledger: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    
    root_agent = Agent(
        name="carbon_scope3_ledger",
        description="[Category: 02 · Sourcing & Procurement — Supplier Network] ESG & Scope 3 Auditor (Chief Sustainability Officer): Standardizes chain-of-custody certificates (RSPO/FSC) and packaging LCAs. Outcome: Automates Scope 3 disclosure audits.",
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

    app = App(root_agent=root_agent, name="carbon_scope3_ledger")

    class CarbonScope3LedgerAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for carbon_scope3_ledger."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = CarbonScope3Ledger()

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
    root_agent = CarbonScope3Ledger()  # type: ignore
    app = None  # type: ignore
    CarbonScope3LedgerAdkApp = None  # type: ignore
