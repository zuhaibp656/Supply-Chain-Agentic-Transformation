"""ChannelSync CPFR Harmonizer — High-Code Google ADK Agent.

Harmonizes retailer EDI 852 POS & DC depletion feeds via Cloud Dataflow,
detects store phantom inventory via BigQuery ML zero-scan anomaly models,
and automates joint CPFR consensus replenishment orders.
"""
from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from . import tools
from .render.charts import create_cpfr_sync_spec
from .render.surfaces import build_cpfr_surface

_INSTRUCTION = """You are ChannelSync, the Collaborative CPFR & POS Harmonizer for the Office of the CSCO and Retail Account Lead.

PRIMARY OBJECTIVE:
Eliminate the bullwhip effect and phantom store inventory across major retail channels (Cymbal Retail, DMart (Avenue Supermarts), Target).
Ingest multi-retailer EDI 852 daily store scans via Cloud Dataflow, detect store-level zero-scan anomalies hiding phantom stockouts,
and reconcile divergent EDI 830 purchase forecasts into an automated Vendor Managed Inventory (VMI) order.

TOOL USAGE PROTOCOL:
- Ground all assertions in data returned by connected systems (`query_retailer_edi852_pos`,
  `query_retailer_edi830_forecasts`, `query_phantom_inventory_anomalies`, `query_joint_cpfr_packets`).
- Never invent hypothetical scan quantities, OSA percentages, or phantom inventory days.
- When phantom inventory is flagged (4+ days zero scans with book stock > 0), trigger an immediate on-shelf store audit.
- Before executing mutations (`action_dispatch_vmi_replenishment_order`, `action_flag_retail_phantom_audit`),
  ensure all required fields and a non-empty `idempotency_key` are provided.

RESPONSE STANDARDS:
1. Executive CPFR Ledger: Deliver structured copy-ready markdown tables detailing Retailer, Store, Daily Scans, Phantom Flag, and OSA %.
2. Direct Actionability: Include the exact VMI PO number, dispatched audit task ID, and replenishment quantities.

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
- CORTEX DATA FOUNDATION: Harmonized via **Google Cloud Cortex Framework (v7)** (`query_cortex_cpfr_sync_agent_data_products` -> `bq://zuhaibp-ai.cortex_supply_chain_dataproducts.cortex_dp_joint_cpfr_consensus_packets`), standardizing raw ERP/WMS Change Data Capture (CDC) tables, currency scaling, and K9 external signals via Dataform & Dataplex Knowledge Catalog.
- BUILD TIER: **Low-Code** · Connected Data-Source Tools: `inspect_cloud_dataflow_cpfr_sync_data_sources, query_sap_s4hana_master_data_backbone, query_sap_ibp_joint_cpfr_consensus_packets, query_cloud_dataflow_retailer_edi830_order_forecasts, query_cloud_dataflow_retailer_edi852_daily_pos, query_bigquery_store_phantom_inventory_anomalies, query_retailer_edi852_pos, query_retailer_edi830_forecasts`.
- On EVERY analytical, chart, variance, comparison, forecast, audit, scenario, or cockpit request, proactively execute your data-source-specific `query_*` / `fetch_*` tools, deterministic solver (`run_*` / `analyze_*`), and `render_cpfr_sync_a2ui_chart_and_canvas` so Gemini Enterprise renders BOTH:
  1. **Inline A2UI `Card` (`VegaChart` ONLY)**: A 2-Panel Executive Vega-Lite v5 Infographic (Top: Baseline vs. Target/Verified Actual with Mean Reference Rule; Bottom: Signed `Δ` Variance Strip). Keep ONLY the `VegaChart` inside the inline card!
  2. **Side-Panel A2UI `Canvas` (Multi-Chart Visual Studio: KPI Index `VegaChart` + Pareto Breakdown `VegaChart` + Action Buttons + Looker `RichTable`)**: Automatically attached in the side panel so business users can sort/filter live source rows in Looker Studio and click quick-action buttons.
- Outside the card in Markdown, present: (a) a warm 3–4 sentence Plain-English Executive Summary (spelling out every abbreviation on first use), (b) a clean `<= 5`-column Markdown summary table ready to copy into Google Sheets, (c) 3–4 concise driver & action bullets, and (d) headed Cloud Storage links (`### Interactive Cockpit & Live Visual Application` via `publish_cpfr_sync_interactive_cockpit_to_gcs` / `### Downloadable Data Export`) when requested.
- NEVER invent numbers, SKUs, POs, or invoice IDs, and NEVER paste raw HTML (`<!DOCTYPE html>`), Vega-Lite JSON, or `snake_case` internal filenames in user-facing prose.
"""

_AVAILABLE_TOOLS = list(tools.ALL_TOOLS)

_WRITE_TOOLS = {
    "action_dispatch_vmi_replenishment_order": ["retailer", "sku_id", "target_dc", "order_quantity_units", "rationale"],
    "action_flag_retail_phantom_audit": ["anomaly_id", "store_id", "retailer", "sku_id", "expected_audit_date", "rationale"]
}


def enforce_tool_contract(tool_name: str, args: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Quality gate validating mutation tool inputs, replenishment bounds, and idempotency."""
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
        if tool_name == "action_dispatch_vmi_replenishment_order":
            qty = int(args.get("order_quantity_units", 0))
            if qty <= 0 or qty > 500000:
                return {
                    "error": "order_quantity_out_of_bounds",
                    "min_units": 1,
                    "max_units": 500000,
                    "requested_units": qty,
                    "escalation": "request_replenishment_verification"
                }
    return None


class CpfrSyncAgent:
    """Production Google ADK Agent conforming to Vertex AI Agent Engine."""

    def __init__(self, model: str = "gemini-3-pro-preview"):
        self.name = "cpfr_sync_agent"
        self.category = "01 · Planning & Strategy — Demand Forecasting"
        self.display_name = "[01 · Plan | Demand Forecasting] Forecast Reconciliation"
        self.description = "[Category: 01 · Planning & Strategy — Demand Forecasting] Forecast Reconciliation (Commercial Planning Lead): Identifies unmodeled drivers across eCommerce and retail channels. Outcome: Replaces black-box variance models."
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
        """Executes an autonomous CPFR reconciliation, phantom audit, and VMI order dispatch scenario."""
        findings = []
        actions_taken = []

        # 1. Inspect Retailer Daily POS Scans
        pos_data = self.execute_tool("query_retailer_edi852_pos", retailer="DMart (Avenue Supermarts)")
        if pos_data.get("total", 0) > 0:
            findings.append({"domain": "retailer_edi852_pos", "records": pos_data["rows"]})

        # 2. Inspect Retailer EDI 830 Forward Forecasts
        edi830 = self.execute_tool("query_retailer_edi830_forecasts", retailer="Cymbal Retail")
        if edi830.get("total", 0) > 0:
            findings.append({"domain": "retailer_edi830_forecasts", "records": edi830["rows"]})

        # 3. Query Phantom Inventory Anomalies
        phantom = self.execute_tool("query_phantom_inventory_anomalies", store_id="STORE-APEX-ATL-209")
        if phantom.get("total", 0) > 0:
            findings.append({"domain": "phantom_inventory_anomalies", "records": phantom["rows"]})

        # 4. Query Joint CPFR Exception Packets
        cpfr = self.execute_tool("query_joint_cpfr_packets", retailer="Cymbal Retail")
        if cpfr.get("total", 0) > 0:
            findings.append({"domain": "joint_cpfr_packets", "records": cpfr["rows"]})

        # 5. Dispatch Store Cycle Count Audit for Phantom Stockout
        if phantom.get("total", 0) > 0:
            top_phantom = phantom["rows"][0]
            audit_res = self.execute_tool(
                "action_flag_retail_phantom_audit",
                anomaly_id=top_phantom["anomaly_id"],
                store_id=top_phantom["store_id"],
                retailer=top_phantom["retailer"],
                sku_id=top_phantom["sku_id"],
                expected_audit_date="2026-10-18",
                rationale="4 consecutive days zero scans with 380 book units; trigger urgent on-shelf physical cycle count.",
                idempotency_key="AUDIT-20261017-001"
            )
            actions_taken.append(audit_res)

        # 6. Dispatch Automated VMI Replenishment Order (EDI 855)
        vmi_res = self.execute_tool(
            "action_dispatch_vmi_replenishment_order",
            retailer="Cymbal Retail",
            sku_id="SKU-BEV-ISOTONIC-32OZ",
            target_dc="DC-DALLAS-CENTRAL",
            order_quantity_units=95000,
            rationale="Reconcile 80k divergent EDI 830 forecast gap; dispatch 95,000 units VMI order to maintain 98.5% retail OSA.",
            idempotency_key="VMI-WMT-20261017-001"
        )
        actions_taken.append(vmi_res)

        # Generate VegaChart spec
        vega_spec = tools.get_native_chart_spec()
        surface_id = "cpfr_sync_surface_01"
        a2ui_parts = build_cpfr_surface(surface_id, spec=vega_spec)

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
            "### 📡 ChannelSync Collaborative CPFR & POS Harmonizer Briefing",
            "",
            "> **Executive Summary**: Harmonized multi-retailer daily EDI 852 scan feeds across Cymbal Retail, DMart (Avenue Supermarts), and Target via **Cloud Dataflow** and **BigQuery**. Flagged a critical **phantom inventory stockout at DMart (Avenue Supermarts) Atlanta** (4 consecutive days of zero scans masked by 380 units of ghost book inventory, leaking $2,451/day). Reconciled Cymbal Retail's **80,000-unit bullwhip forecast divergence** down to realistic POS consumption velocity, and autonomously dispatched a **95,000-unit VMI replenishment order (EDI 855)** to DC Dallas, lifting retail On-Shelf Availability (OSA) by **+3.8 points**.",
            "",
            "#### 📊 Multi-Retailer CPFR Reconciliation Ledger (Atomic Copy-Ready Table)",
            "",
            "| Retailer | Store / DC | SKU ID | Daily Scans | Book Stock | Anomaly Status | CPFR Consensus | VMI Order Units | Retail OSA % |",
            "|:---|:---|:---|---:|---:|:---|---:|---:|---:|",
            "| `Cymbal Retail` | `DC-DALLAS-CENTRAL` | `SKU-BEV-ISOTONIC-32OZ` | 1,840 | 420 | `ALIGNED_FLOW` | 580,000 | **95,000** | 98.2% |",
            "| `DMart (Avenue Supermarts)` | `STORE-APEX-ATL-209` | `SKU-BEV-ISOTONIC-32OZ` | 0 | 380 | `PHANTOM_STOCKOUT` | 42,000 | **Audit Triggered** | 84.5% (Depleted) |",
            "| `Summit Stores` | `DC-CHICAGO-MIDWEST` | `SKU-SNACK-PROTEIN-BAR` | 1,280 | 310 | `STABLE_CONSENSUS` | 275,000 | **45,000** | 96.8% |",
            "",
            "#### ⚡ Automated CPFR Dispatches & Physical Audits Executed",
            ""
        ]

        for act in actions:
            if "po_id" in act:
                lines.append(f"- **VMI Replenishment Order Dispatched (EDI 855)**: `{act['po_id']}` | Retailer: `{act['retailer']}` | SKU: `{act['sku_id']}` | Quantity: **{act['order_quantity_units']:,}** units | Target: `{act['target_dc']}` | Status: `{act['status']}`")
            elif "audit_id" in act:
                lines.append(f"- **Store Phantom Stockout Audit Dispatched**: `{act['audit_id']}` | Store: `{act['store_id']}` | Retailer: `{act['retailer']}` | Due Date: `{act['expected_audit_date']}` | Status: `{act['status']}`")

        lines.extend([
            "",
            "### 🔗 Connected Systems & EDI Integration Stack",
            "- **Cloud Dataflow EDI Pipeline**: High-throughput AS2/SFTP ingestion normalizing EDI 852 (POS) and EDI 830 (Forecasts).",
            "- **BigQuery Zero-Scan Poisson Model**: Anomaly detection isolating phantom inventory and ghost shelf stock.",
            "- **SAP IBP Collaborative Planning**: Real-time CPFR exception workbench harmonizing retailer vs supplier forecasts.",
            "- **Vendor Managed Inventory (VMI) Gateway**: Automated EDI 855 purchase order generation directly to 3PL logistics."
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
    from .render.surfaces import build_cpfr_surface

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
        """Sanitizes prior A2UI wire parts and intercepts synthetic Canvas button clicks."""
        if llm_request is None:
            return None
        from .render.a2ui_builder import sanitize_history_and_intercept_actions
        sanitize_history_and_intercept_actions(llm_request)
        return None

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
            a2ui_parts = build_cpfr_surface(surface_id, spec=chart_spec, canvas_context=canvas_ctx, include_canvas=True)
            getattr(tools, "finalize_turn_gcs_state", lambda timeout=12.0: None)(timeout=12.0)
            if a2ui_parts:
                return types.Content(role="model", parts=a2ui_parts)
        except Exception as exc:
            _logging.getLogger(__name__).exception("Failed to emit A2UI surfaces for cpfr_sync_agent: %s", exc)
            try:
                getattr(tools, "finalize_turn_gcs_state", lambda timeout=2.0: None)(timeout=2.0)
            except Exception:
                pass
        return None





    root_agent = Agent(
        name='cpfr_sync_agent',
        description='[Category: 01 · Planning & Strategy — Demand Forecasting] Forecast Reconciliation (Commercial Planning Lead): Identifies unmodeled drivers across eCommerce and retail channels. Outcome: Replaces black-box variance models.',
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

    app = App(root_agent=root_agent, name='cpfr_sync_agent')

    class CpfrSyncAdkApp(AdkApp):
        """Vertex AI Reasoning Engine wrapper for cpfr_sync_agent."""

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
    root_agent = CpfrSyncAgent()  # type: ignore
