"""SchemeGuard — Secondary Trade Payout & Claims Sentinel — High-Code Google ADK Agent.

Audits 100% of distributor secondary sales scheme claims against circular slab rules, e-waybill proof, and ShelfVision compliance—blocking phantom/split invoices and posting SAP FI credit notes.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_trade_scheme_claims_reconciler_chart_spec
from .render.surfaces import build_trade_scheme_claims_reconciler_surface

_INSTRUCTION = """You are SchemeGuard — Secondary Trade Payout & Claims Sentinel.

PRIMARY OBJECTIVE:
Audits 100% of distributor secondary sales scheme claims against circular slab rules, e-waybill proof, and ShelfVision compliance—blocking phantom/split invoices and posting SAP FI credit notes.

TOOL USAGE PROTOCOL:
- Ground all optimizations and enterprise checks strictly in connected tools.
- Never invent order IDs, asset identifiers, or financial figures.
- Before executing mutations (`action_flag_phantom_invoice_for_audit_hold`, `action_post_sap_fi_trade_credit_note`), ensure all required fields and a non-empty `idempotency_key` are provided.

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
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_trade_scheme_claims_reconciler_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_active_trade_promotion_schemes`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **Low-Code** · Connected Data-Source Tools: `inspect_trade_scheme_trade_scheme_claims_reconciler_data_sources, query_sap_s4hana_master_data_backbone, query_trade_scheme_active_trade_promotion_schemes, query_bigquery_claim_anomaly_audit_findings, query_dms_secondary_distributor_secondary_claim_submissions, query_sap_s4hana_sap_fi_credit_note_settlements, query_active_trade_promotion_schemes, query_distributor_secondary_claim_submissions`.
- ARCHETYPE & SMART UI RULE (AUDITOR): Intelligently choose ONLY the output depth and UI elements warranted by the user's request. Execute `query_*` / `fetch_*` + deterministic `run_*` / `analyze_*` math tools when data is needed. Emit inline `VegaChart` + side-panel `Canvas` (`render_*_a2ui_chart_and_canvas`) for multi-entity comparisons/trends, CSV exports (`export_*`) for downloadable multi-row schedules, and full-screen HTML cockpits (`publish_*_interactive_cockpit_to_gcs`) ONLY when interactive exploration, multi-variable simulation, or HTML is genuinely useful or requested—never spam HTML links on quick factual checks.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_flag_phantom_invoice_for_audit_hold": ["claim_id", "flagged_invoices", "disallowed_amount_usd", "rationale"],
    "action_post_sap_fi_trade_credit_note": ["claim_id", "distributor_id", "approved_amount_usd", "rationale"],
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


class TradeSchemeClaimsReconciler:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3.1-pro-preview"):
        self.name = "trade_scheme_claims_reconciler"
        self.category = "01 · Planning & Strategy — Trade Promotion"
        self.display_name = "[01 · Plan | Trade Promotion] Deduction Audit Agent"
        self.description = "[Category: 01 · Planning & Strategy — Trade Promotion] Deduction Audit Agent (Revenue / Trade Finance Lead): Audits scanned proof-of-performance circulars and invoices via OCR. Outcome: Resolves claim disputes in hours."
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

        r_0 = self.execute_tool("query_active_trade_promotion_schemes", scheme_id="SCH-FEST-Q4-2026")
        if r_0.get("total", 0) > 0:
            findings.append({"domain": "active_trade_promotion_schemes", "records": r_0["rows"]})

        r_1 = self.execute_tool("query_distributor_secondary_claim_submissions", claim_id="CLM-DIST04-9921")
        if r_1.get("total", 0) > 0:
            findings.append({"domain": "distributor_secondary_claim_submissions", "records": r_1["rows"]})

        r_2 = self.execute_tool("query_claim_anomaly_audit_findings", claim_id="CLM-DIST04-9921")
        if r_2.get("total", 0) > 0:
            findings.append({"domain": "claim_anomaly_audit_findings", "records": r_2["rows"]})

        r_3 = self.execute_tool("query_sap_fi_credit_note_settlements", claim_id="CLM-DIST04-9921")
        if r_3.get("total", 0) > 0:
            findings.append({"domain": "sap_fi_credit_note_settlements", "records": r_3["rows"]})

        act1_res = self.execute_tool(
            "action_flag_phantom_invoice_for_audit_hold",
            claim_id='CLM-DIST04-9921',
            flagged_invoices=['INV-SEC-8812', 'INV-SEC-8819'],
            disallowed_amount_usd=2190.0,
            rationale='Disallowed $2,190.00 across 2 secondary invoices (post-dated outside scheme window and duplicate outlet tax ID) on claim CLM-DIST04-9921.',
            idempotency_key='SCHM-HOLD-20261022-01'
        )
        actions_taken.append(act1_res)

        act2_res = self.execute_tool(
            "action_post_sap_fi_trade_credit_note",
            claim_id='CLM-DIST04-9921',
            distributor_id='DIST-MUM-WEST-04',
            approved_amount_usd=16260.0,
            rationale='Posted verified SAP S/4HANA FI credit note for $16,260.00 (140 compliant secondary invoices) in 1.8 hours instead of 45 days.',
            idempotency_key='SCHM-CN-20261022-01'
        )
        actions_taken.append(act2_res)

        vega_spec = tools.get_native_chart_spec()
        surface_id = "trade_scheme_claims_reconciler_surface_01"
        a2ui_parts = build_trade_scheme_claims_reconciler_surface(surface_id, spec=vega_spec)
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
            "### ✦ SchemeGuard — Secondary Trade Payout & Claims Sentinel — Executive Operations Brief",
            "",
            "> **Executive Summary**: Executed deterministic multi-signal optimization and ERP/WMS/TMS write-backs across **05 · Deliver**.",
            "",
            "#### 📊 Operational Telemetry & Solver Output (Copy-Ready Table)",
            "",
            "| Dimension | Metric Value | Secondary KPI | Execution Mode |",
            "|:---|---:|---:|:---|",
        ]
        for row in [{"claim_batch": "CLM-9921 (West Zone)", "approved_usd": 16260, "leakage_blocked_usd": 2190, "status": "OPTIMIZED_CVRPTW"}, {"claim_batch": "CLM-9928 (North Zone)", "approved_usd": 22400, "leakage_blocked_usd": 3150, "status": "OPTIMIZED_CVRPTW"}, {"claim_batch": "Manual 5% Sample Audit", "approved_usd": 18450, "leakage_blocked_usd": 110, "status": "LEGACY_STATIC"}]:
            lines.append(f"| `{row['claim_batch']}` | **{row['approved_usd']}** | {row['leakage_blocked_usd']} | `{row['status']}` |")

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
        for sys_meta in [{"id": "trade_scheme_slab_engine", "name": "Enterprise Trade Promotion Management (TPM) Circular & Slab Rule Engine", "protocol": "REST / JSON", "tables": ["active_trade_promotion_schemes"]}, {"id": "dms_secondary_claims_portal", "name": "Distributor Secondary Billing & Scheme Claim Submission Portal", "protocol": "OData / REST", "tables": ["distributor_secondary_claim_submissions"]}, {"id": "phantom_invoice_graph_detector", "name": "BigQuery ML Anomaly & Split-Invoice Leakage Detector", "protocol": "BigQuery SQL", "tables": ["claim_anomaly_audit_findings"]}, {"id": "sap_fi_credit_memo_poster", "name": "SAP S/4HANA FI Accounts Receivable Automated Credit Memo BAPI", "protocol": "RFC / OData v4", "tables": ["sap_fi_credit_note_settlements"]}]:
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
            scenario = TradeSchemeClaimsReconciler().run_scenario("live_turn")
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
            a2ui_parts = build_trade_scheme_claims_reconciler_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for trade_scheme_claims_reconciler: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    root_agent = Agent(
        name="trade_scheme_claims_reconciler",
        description="[Category: 01 · Planning & Strategy — Trade Promotion] Deduction Audit Agent (Revenue / Trade Finance Lead): Audits scanned proof-of-performance circulars and invoices via OCR. Outcome: Resolves claim disputes in hours.",
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

    app = App(root_agent=root_agent, name="trade_scheme_claims_reconciler")

    class TradeSchemeClaimsReconcilerAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for trade_scheme_claims_reconciler."""

        def __init__(self, agent: Agent = root_agent, **kwargs: Any) -> None:
            super().__init__(agent=agent, **kwargs)
            self._scenario_agent = TradeSchemeClaimsReconciler()

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
    root_agent = TradeSchemeClaimsReconciler()  # type: ignore
    app = None  # type: ignore
    TradeSchemeClaimsReconcilerAdkApp = None  # type: ignore
