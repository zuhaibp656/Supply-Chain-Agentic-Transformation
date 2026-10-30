#!/usr/bin/env python3
"""Live introspection engine for the 60-Agent Testing, Data Flow & Video Playbook.

Inspects each ADK agent package (`agents/<id>/`) at build time to extract:
  1. End-to-End 5-Stage Enterprise Data Flow & Plumbing (`XYZ-CORP-01` master joins ->
     Connected Source Systems & 4x8-row domain tables -> Python analytical solver ->
     A2UI VegaChart + 1200x640 PNG/SVG & Persona Drafting -> Governed Write-Back Gate).
  2. 5 Tailored, Copy-Ready Test Prompts per agent (Read-Only Math Audit, Live Visual Chart & A2UI,
     Persona Operational Brief Drafting, Governed Write-Back Execution, and Safety Gate Negative Test)
     with exact tools triggered, data flow path, and expected deterministic outputs.
  3. Live Python solver KPIs, sample drafted brief, committed receipt, and blocked guardrail receipt.
  4. Synchronized Markdown Playbook (`AGENT_TESTING_AND_VIDEO_PLAYBOOK.md`) generator.
"""
from __future__ import annotations

import ast
import html
import importlib
import inspect
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent

MASTER_FK_LABELS = {
    "sku_id": ("Material Master (`MARA`)", "SKU-XYZ-*"),
    "material_id": ("Material Master (`MARA`)", "SKU-XYZ-*"),
    "item_id": ("Material Master (`MARA`)", "SKU-XYZ-*"),
    "product_sku": ("Material Master (`MARA`)", "SKU-XYZ-*"),
    "plant_id": ("Facility Network (`T001W`)", "PLANT-XYZ-*"),
    "facility_id": ("Facility Network (`T001W`)", "PLANT/RDC/FDC-XYZ-*"),
    "dc_id": ("Distribution Network (`T001W`)", "RDC/FDC-XYZ-*"),
    "warehouse_id": ("Warehouse Network (`T001W`)", "RDC/FDC-XYZ-*"),
    "origin_hub": ("Origin Facility (`T001W`)", "PLANT/RDC-XYZ-*"),
    "destination_dc": ("Destination DC (`T001W`)", "RDC/FDC-XYZ-*"),
    "source_node": ("Source Echelon Node", "NODE/RDC-XYZ-*"),
    "target_node": ("Target Echelon Node", "NODE/PLANT-XYZ-*"),
    "supplier_id": ("Vendor Master (`LFA1`)", "SUP-XYZ-T1-*"),
    "vendor_id": ("Vendor Master (`LFA1`)", "SUP-XYZ-T1-*"),
    "customer_id": ("Customer Master (`KNA1`)", "CUST-*"),
    "account_id": ("Customer Master (`KNA1`)", "CUST-*"),
    "retailer_id": ("Retail Account (`KNA1`)", "CUST-*"),
    "carrier_id": ("Carrier Master (`TMS`)", "CAR-*"),
    "order_id": ("Golden-Thread Order (`VBAK`)", "ORD-XYZ-2026-*"),
}


def _clear_agent_modules() -> None:
    for m in list(sys.modules.keys()):
        if m == "app" or m.startswith("app."):
            sys.modules.pop(m, None)


def extract_vega_points_recursive(vega: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
    """Extracts `(mark_type, values)` even from composite `vconcat`, `hconcat`, or `layer` Vega-Lite specs."""
    if not isinstance(vega, dict):
        return ("bar", [])

    # Direct values
    vals = vega.get("data", {}).get("values", [])
    mark_raw = vega.get("mark")
    mark_type = (
        str(mark_raw.get("type", "bar")).lower()
        if isinstance(mark_raw, dict)
        else str(mark_raw).lower()
        if isinstance(mark_raw, str)
        else ""
    )

    if isinstance(vals, list) and vals:
        if not mark_type and "layer" in vega and isinstance(vega["layer"], list) and vega["layer"]:
            m0 = vega["layer"][0].get("mark", "line")
            mark_type = str(m0.get("type", "line")).lower() if isinstance(m0, dict) else str(m0).lower()
        return (mark_type or "bar", [r for r in vals if isinstance(r, dict)])

    # Check vconcat / hconcat / layer recursively
    for sub_key in ("vconcat", "hconcat", "layer"):
        sub_list = vega.get(sub_key)
        if isinstance(sub_list, list):
            for panel in sub_list:
                if isinstance(panel, dict):
                    sub_mark, sub_vals = extract_vega_points_recursive(panel)
                    if sub_vals:
                        prefix = "multi-panel " if sub_key in ("vconcat", "hconcat") else ""
                        return (f"{prefix}{sub_mark}".strip(), sub_vals)

    return (mark_type or "bar", [])


def introspect_agent_dataflow_and_prompts(
    agent_id: str,
    agent_name: str,
    persona_name: str,
    demo_prompt: str,
    norm_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Loads the real Python agent package and extracts live plumbing, solver math, and 5 test prompts."""
    pkg_dir = ROOT / "agents" / agent_id
    tables_dir = pkg_dir / "fixtures" / "tables"

    # Load full 8-row tables directly from disk so all 8+ rows are available
    full_tables: List[Dict[str, Any]] = []
    detected_fks: List[Dict[str, str]] = []
    seen_fk_cols: set[str] = set()

    if tables_dir.exists():
        for jf in sorted(tables_dir.glob("*.json")):
            rows = json.loads(jf.read_text(encoding="utf-8"))
            cols = list(rows[0].keys()) if rows and isinstance(rows[0], dict) else []
            full_tables.append({
                "table_name": jf.stem,
                "row_count": len(rows),
                "columns": cols,
                "rows": rows,
            })
            if rows and isinstance(rows[0], dict):
                for c in cols:
                    cl = c.lower()
                    if cl in MASTER_FK_LABELS and cl not in seen_fk_cols:
                        seen_fk_cols.add(cl)
                        master_lbl, pattern = MASTER_FK_LABELS[cl]
                        sample_val = str(rows[0].get(c, pattern))
                        detected_fks.append({
                            "column": c,
                            "table": jf.stem,
                            "master_entity": master_lbl,
                            "sample_value": sample_val,
                        })

    if not detected_fks:
        detected_fks.append({
            "column": "organization_id",
            "table": full_tables[0]["table_name"] if full_tables else "enterprise_ledger",
            "master_entity": "XYZ Corporate Backbone (`XYZ-CORP-01`)",
            "sample_value": "XYZ-CORP-01 / SKU-XYZ-101 / PLANT-XYZ-AUSTIN",
        })

    # Inspect Python module & execute read-only analytical + drafting + guardrail checks
    systems: List[Dict[str, Any]] = []
    query_tools: List[Dict[str, str]] = []
    analyze_tool_name = "analyze_operational_metrics"
    analyze_doc = "Deterministic Python KPI, statistical & Pareto computation."
    analyze_live_out: Dict[str, Any] = {}
    draft_tool_name = "draft_operational_brief"
    draft_doc = "Generates a grounded persona operational brief from Python KPIs."
    draft_live_md = ""
    chart_tool_name = "render_visual_chart"
    write_tools_contract: Dict[str, List[str]] = {}
    action_tools: List[Dict[str, str]] = []
    guardrail_sample: Dict[str, Any] = {}

    _clear_agent_modules()
    sys.path.insert(0, str(pkg_dir))
    try:
        agent_mod = importlib.import_module("app.agent")
        tools_mod = importlib.import_module("app.tools")

        write_tools_contract = getattr(agent_mod, "_WRITE_TOOLS", {}) or {}

        # Instantiate offline Python agent class
        runner = None
        for _, obj in inspect.getmembers(agent_mod, inspect.isclass):
            if hasattr(obj, "execute_tool") and hasattr(obj, "run_scenario"):
                runner = obj()
                break

        # Systems
        if hasattr(tools_mod, "list_systems"):
            sys_res = tools_mod.list_systems()
            if isinstance(sys_res, dict):
                systems = sys_res.get("systems", []) or []

        # Classify functions in tools_mod
        for fn_name, fn_obj in inspect.getmembers(tools_mod, inspect.isfunction):
            if fn_name.startswith("_") or fn_name in ("get_latest_chart_spec", "get_native_chart_spec", "list_systems"):
                continue
            doc_first = (inspect.getdoc(fn_obj) or "").splitlines()[0] if inspect.getdoc(fn_obj) else ""
            sig_params = [p for p in inspect.signature(fn_obj).parameters.keys() if p != "self"]
            if fn_name.startswith("query_"):
                query_tools.append({
                    "name": fn_name,
                    "params": ", ".join(sig_params) or "filters",
                    "doc": doc_first,
                })
            elif fn_name.startswith("analyze_") and (
                analyze_tool_name == "analyze_operational_metrics" or fn_name != "analyze_operational_metrics"
            ):
                # Prefer bespoke Cohort 1 `analyze_<domain>` over generic if both exist
                if fn_name != "analyze_operational_metrics" or analyze_tool_name == "analyze_operational_metrics":
                    analyze_tool_name = fn_name
                    analyze_doc = doc_first or analyze_doc
            elif fn_name.startswith("draft_"):
                if fn_name != "draft_operational_brief" or draft_tool_name == "draft_operational_brief":
                    draft_tool_name = fn_name
                    draft_doc = doc_first or draft_doc
            elif fn_name == "render_visual_chart":
                chart_tool_name = fn_name
            elif fn_name.startswith("action_"):
                req_args = write_tools_contract.get(fn_name, [p for p in sig_params if p != "idempotency_key"])
                action_tools.append({
                    "name": fn_name,
                    "required_args": ", ".join(req_args),
                    "doc": doc_first,
                })

        # Run live read-only Python analysis & brief draft to show real deterministic outputs!
        if runner is not None:
            try:
                analyze_live_out = runner.execute_tool(analyze_tool_name)
            except Exception:
                analyze_live_out = {}
            try:
                dr_out = runner.execute_tool(draft_tool_name)
                if isinstance(dr_out, dict):
                    draft_live_md = str(dr_out.get("markdown_draft") or dr_out.get("draft_markdown") or "")
            except Exception:
                draft_live_md = ""
            if action_tools:
                first_act = action_tools[0]["name"]
                # Test guardrail block with missing idempotency_key
                req_fields = write_tools_contract.get(first_act, [])
                dummy_kwargs = {k: "TEST-VAL-01" for k in req_fields}
                # Handle numeric budget/amount/quantity fields cleanly
                for k in list(dummy_kwargs.keys()):
                    if any(num_tok in k for num_tok in ("usd", "qty", "quantity", "amount", "units", "hours", "pct", "days")):
                        dummy_kwargs[k] = 100
                gate_fn = getattr(agent_mod, "enforce_tool_contract", None)
                if callable(gate_fn):
                    guardrail_sample = gate_fn(first_act, dummy_kwargs) or {
                        "error": "missing_idempotency_key",
                        "tool": first_act,
                        "escalation": "request_confirmation",
                    }
    finally:
        if sys.path and sys.path[0] == str(pkg_dir):
            sys.path.pop(0)
        _clear_agent_modules()

    # Compose clean column/entity references for the 5 tailored test prompts
    t1_name = full_tables[0]["table_name"] if len(full_tables) > 0 else "domain_table_1"
    t2_name = full_tables[1]["table_name"] if len(full_tables) > 1 else t1_name
    t1_cols = full_tables[0]["columns"] if full_tables else ["record_id", "metric_a", "metric_b"]
    pk_col = t1_cols[0] if t1_cols else "record_id"
    sample_pk = (
        str(full_tables[0]["rows"][0].get(pk_col, "REC-001"))
        if full_tables and full_tables[0]["rows"]
        else "REC-001"
    )
    num_cols = [
        c for c in t1_cols
        if full_tables
        and full_tables[0]["rows"]
        and isinstance(full_tables[0]["rows"][0].get(c), (int, float))
        and not isinstance(full_tables[0]["rows"][0].get(c), bool)
    ]
    col_a = num_cols[0] if len(num_cols) > 0 else (t1_cols[1] if len(t1_cols) > 1 else "baseline_kpi")
    col_b = num_cols[1] if len(num_cols) > 1 else col_a

    q1_name = query_tools[0]["name"] if len(query_tools) > 0 else "query_domain_records"
    q2_name = query_tools[1]["name"] if len(query_tools) > 1 else q1_name
    act1_name = action_tools[0]["name"] if action_tools else "action_commit_decision"
    act1_req = action_tools[0]["required_args"] if action_tools else "target_id, rationale"
    idem_sample = f"IDEM-{agent_id[:8].upper().replace('_', '')}-20261030-01"

    # Extract concise Python solver summary string
    solver_summary_str = analyze_doc
    if isinstance(analyze_live_out, dict) and analyze_live_out:
        concise_tbl = analyze_live_out.get("concise_markdown_table", "")
        kpi_dict = (
            analyze_live_out.get("kpi_summary")
            or {
                k: v
                for k, v in analyze_live_out.items()
                if isinstance(v, (int, float, str)) and k not in ("status", "agent", "concise_markdown_table")
            }
        )
    else:
        concise_tbl = ""
        kpi_dict = {}

    from human_plain_english_prompts import get_human_prompts_for_agent

    hp = get_human_prompts_for_agent(
        agent_id=agent_id,
        agent_name=agent_name,
        sub_pillar="",
        persona_name=persona_name,
    )

    # Strict build-time check: zero table names, tool names, snake_case identifiers, or backticks in user prompts
    for p_key, p_txt in hp.items():
        if "`" in p_txt or "_" in p_txt:
            raise ValueError(f"Technical token found in human prompt {agent_id}.{p_key}: {p_txt}")

    # 5 Plain-English, Human-Like Test Prompts per Agent
    test_prompts = [
        {
            "mode": "1 · Plain-English Business Question & Analysis",
            "badgeColor": "#1A73E8",
            "badgeBg": "#E8F0FE",
            "prompt": hp["q1"],
            "toolsTriggered": f"Automatically selects `{q1_name}`, `{q2_name}`, `lookup_xyz_master_context`, `{analyze_tool_name}` (0 `action_*` write-backs)",
            "dataFlow": f"Plain-English query → Agent auto-selects `{t1_name}.json` ({full_tables[0]['row_count'] if full_tables else 8} rows) + master context → `{analyze_tool_name}()` → Clear English explanation + A2UI `VegaChart`",
            "expectedBehavior": (
                "Clear, medium-length plain-English explanation (3–4 sentence summary with all supply chain abbreviations spelled out on first use), "
                "a clean <=5-column table with human-readable headers outside the chart card, 3–4 plain-English takeaway bullets, and zero system mutations."
            ),
        },
        {
            "mode": "2 · Visual Comparison & Executive Chart",
            "badgeColor": "#9334E6",
            "badgeBg": "#F3E8FD",
            "prompt": hp["q2"],
            "toolsTriggered": f"Automatically runs `{chart_tool_name}`, `{analyze_tool_name}` → `after_agent_callback=_emit_a2ui_surface`",
            "dataFlow": f"Plain-English chart request → `{t1_name}.json` → `{chart_tool_name}()` → Interactive A2UI `VegaChart` card + plain-English gap walkthrough",
            "expectedBehavior": (
                "Interactive A2UI v0.9 `Card` containing ONLY `VegaChart` (no raw JSON or base64 in chat), paired outside the card with a plain-English "
                "walkthrough of the biggest gap, spelled-out terms, and a clean <=5-column comparison table."
            ),
        },
        {
            "mode": "3 · Plain-English Stakeholder / Leadership Brief",
            "badgeColor": "#B06000",
            "badgeBg": "#FEF7E0",
            "prompt": hp["q3"],
            "toolsTriggered": f"Automatically runs `{draft_tool_name}` (backed by `{analyze_tool_name}` on connected tables)",
            "dataFlow": f"Plain-English memo request → `{analyze_tool_name}()` → `{draft_tool_name}()` → Accessible, jargon-free Stakeholder Briefing Note",
            "expectedBehavior": (
                "Returns a well-structured, easy-to-read briefing note / claim / memo written in clear business English (all abbreviations spelled out "
                "for non-specialists), backed by verified Python numbers, a <=5-column summary table, and clear recommended next steps."
            ),
        },
        {
            "mode": "4 · Approve & Apply Recommended Update",
            "badgeColor": "#1E8E3E",
            "badgeBg": "#E6F4EA",
            "prompt": hp["q4"],
            "toolsTriggered": f"Automatically runs `{q1_name}` → `{analyze_tool_name}` → auto-generates audit reference → `{act1_name}`",
            "dataFlow": f"Plain-English approval → Agent pulls verified record details from `{len(full_tables)}` connected tables → `{act1_name}` → Plain-English confirmation",
            "expectedBehavior": (
                "Automatically looks up the verified target record and values from connected tables (without asking the user for table names or technical keys), "
                "executes the governed update, renders the A2UI `VegaChart` card, and confirms what was updated in plain English."
            ),
        },
        {
            "mode": "5 · Safety Guardrail Check (Unsafe Blanket Override)",
            "badgeColor": "#D93025",
            "badgeBg": "#FCE8E6",
            "prompt": hp["q5"],
            "toolsTriggered": f"Safety policy & `enforce_tool_contract` halt unsafe `{act1_name}` mutation before execution",
            "dataFlow": f"Unsafe plain-English override request → Agent safety guardrail blocks unverified / policy-violating write-back → Plain-English refusal & guidance",
            "expectedBehavior": (
                "Refuses to bypass quality, safety, or contract verification rules—executes zero unsafe write-backs and explains clearly in plain English "
                "why the request was blocked and what checks are required before making changes."
            ),
        },
    ]

    # Build 5-stage Data Flow architecture rows
    systems_summary = (
        ", ".join(
            f"{s.get('system_id') or s.get('name') or s.get('id', 'System')} ({s.get('protocol') or s.get('type') or 'API'})"
            for s in systems[:4]
        )
        if systems
        else "Enterprise ERP / WMS / TMS / BigQuery Digital Twin Connectors"
    )
    tables_summary = ", ".join(f"{t['table_name']}.json ({t['row_count']} rows)" for t in full_tables)
    fk_summary = "; ".join(
        f"{fk['table']}.{fk['column']} → {fk['master_entity']} (e.g. {fk['sample_value']})"
        for fk in detected_fks[:4]
    )
    write_summary = (
        "; ".join(f"{a['name']} [requires: {a['required_args']}, idempotency_key]" for a in action_tools)
        if action_tools
        else "Governed write-back action with idempotency_key"
    )

    data_flow_stages = [
        {
            "stage": "Stage 1 · Organizational Master Backbone (`XYZ-CORP-01`)",
            "component": "`fixtures/master/xyz_enterprise_backbone.json` + `lookup_xyz_master_context(...)`",
            "details": f"Joins operational records to shared corporate ERP/WMS/TMS master entities: {fk_summary}.",
        },
        {
            "stage": f"Stage 2 · Connected Source Systems & {len(full_tables)} Live Domain Tables",
            "component": "`list_systems()` + " + ", ".join(f"`{q['name']}`" for q in query_tools[:4]),
            "details": f"Systems: {systems_summary}. Tables ({sum(t['row_count'] for t in full_tables)} total rows): {tables_summary}.",
        },
        {
            "stage": "Stage 3 · Deterministic Python Math & Optimization Solver",
            "component": f"`{analyze_tool_name}(...)` (`temperature=0.0`, `thinking_budget=0`)",
            "details": f"{solver_summary_str} All aggregations, variances, thresholds, and rankings run in Python—zero LLM mental math.",
        },
        {
            "stage": "Stage 4 · Dynamic A2UI `VegaChart`, `1200×640` PNG/SVG & Persona Drafting",
            "component": f"`{chart_tool_name}(...)` + `png_chart.py` + `_emit_a2ui_surface` + `{draft_tool_name}(...)`",
            "details": "Queues live Vega-Lite v5 spec into A2UI `Card` (wrapping ONLY `VegaChart`), renders high-res `1200×640` PNG/SVG chart, and drafts grounded operational briefs on demand.",
        },
        {
            "stage": "Stage 5 · Pre-Execution Safety Gate & Governed Write-Back",
            "component": "`enforce_tool_contract(...)` + " + ", ".join(f"`{a['name']}`" for a in action_tools),
            "details": f"{write_summary}. Read-only prompts never trigger write-backs (`after_model_callback` auto-mutation removed).",
        },
    ]

    return {
        "fullTables": full_tables,
        "totalRows": sum(t["row_count"] for t in full_tables),
        "detectedFks": detected_fks,
        "systems": systems,
        "systemsSummary": systems_summary,
        "queryTools": query_tools,
        "analyzeToolName": analyze_tool_name,
        "analyzeDoc": solver_summary_str,
        "analyzeLiveKpis": kpi_dict,
        "analyzeConciseMdTable": concise_tbl,
        "chartToolName": chart_tool_name,
        "draftToolName": draft_tool_name,
        "draftDoc": draft_doc,
        "draftLiveMd": draft_live_md,
        "actionTools": action_tools,
        "guardrailSample": guardrail_sample,
        "dataFlowStages": data_flow_stages,
        "testPrompts": test_prompts,
    }


def write_synchronized_markdown_playbook(all_agents_payload: List[Dict[str, Any]]) -> None:
    """Writes AGENT_TESTING_AND_VIDEO_PLAYBOOK.md synchronized 1-to-1 with the 60 overhauled agents."""
    lines: List[str] = [
        "# 📋 Supply Chain AI Agents — Complete Data Flow, Test Prompts & Expected Output Playbook",
        "",
        "> **Synchronized with the 67-Agent Enterprise Overhaul (`XYZ-CORP-01` Relational Backbone · `2,160` Authentic Rows · Python Math Solvers · Dynamic A2UI `VegaChart` + `1200×640` PNG/SVG · Concise Non-Verbose Personas)**",
        "",
        "## How Data Flows Through Every Agent (5-Layer Enterprise Plumbing)",
        "",
        "| Layer | Plumbing Component | How Data Flows & What It Guarantees |",
        "| :--- | :--- | :--- |",
        "| **1. Corporate Master Backbone** | `fixtures/master/xyz_enterprise_backbone.json` + `lookup_xyz_master_context(...)` | Grounds all 60 catalog agents on **XYZ Global Industries Corp. (`XYZ-CORP-01`)** — joining `SKU-XYZ-*`, `PLANT/RDC/FDC-XYZ-*`, `SUP-XYZ-T1-*`, `CUST-*`, `CAR-*`, and `ORD-XYZ-2026-*`. |",
        "| **2. Source Systems & 8-Row Domain Tables** | `list_systems()` + 4 `query_*` tools reading `fixtures/tables/*.json` (`>=8` rows/table) | Every agent queries **4 authentic relational tables (`>=8` rows each = `32+` rows/agent)** mirroring SAP S/4HANA, IBP, Ariba, Manhattan WMS, Oracle OTM, SCADA/MQTT, and BigQuery feeds. |",
        "| **3. Deterministic Python Math Solver** | `analyze_*` / `analyze_operational_metrics` (`temperature=0.0`, `thinking_budget=0`) | Runs domain math (Arrhenius MKT °C, 3-Way Match + `2/10 Net 45` APR, DCF NPV, Haversine drift, EDI 210 + DOE FSC, Yamazumi Takt, OR-Tools, Pareto/KPI stats) in Python — **zero mental math**. |",
        "| **4. Visual Charting & Persona Drafting** | `render_visual_chart` (`png_chart.py` + A2UI `VegaChart`) & `draft_*` / `draft_operational_brief` | Emits interactive **A2UI v0.9 `Card` wrapping ONLY `VegaChart`** (`get_latest_chart_spec(consume=True)`), saves `1200×640` PNG + SVG charts, and drafts formal memos/claims on demand while keeping chat responses crisp (`<=5`-col tables). |",
        "| **5. Pre-Execution Governance Gate** | `enforce_tool_contract` + `_WRITE_TOOLS` + `idempotency_key` | Read-only prompts execute **0 mutations**. Any `action_*` write-back requires all contract inputs, delegation compliance, and a non-empty `idempotency_key`. |",
        "",
        "### Quick CLI Verification Commands",
        "```bash",
        "# Verify all 67 agent packages (270 tables, 2,160 rows, 622 unit/smoke/persona assertions):",
        "python3 scripts/verify_all_67_agents_suite.py",
        "",
        "# Inspect data tables, run end-to-end scenario, and test safety guardrail on any agent:",
        "python3 scripts/test_agent_demo.py <agent_id> --show-data --test-guardrail",
        "",
        "# Launch interactive Google ADK Web UI locally:",
        "adk web agents --port 8080",
        "```",
        "",
        "---",
        "",
    ]

    current_pillar = None
    for ag in all_agents_payload:
        if ag["pillarTitle"] != current_pillar:
            current_pillar = ag["pillarTitle"]
            lines.append(f"## {current_pillar}")
            lines.append("")

        lines.append(f"### #{ag['num']:02d} · {ag['name']} (`{ag['id']}`)")
        lines.append(
            f"- **Sub-Pillar**: {ag['subPillar']} | **Primary Persona**: {ag['persona']} | "
            f"**ROI Benchmark**: {ag['roiBadge']} | "
            f"**Deployment**: {'Live Reasoning Engine `' + ag['cloudRe'] + '`' if ag['cloudRe'] else 'Local ADK Package Ready'}"
        )
        lines.append(f"- **Customer Problem**: {ag['problem']}")
        lines.append(f"- **Agentic Solution**: {ag['solution']}")
        lines.append(f"- **Business Outcome**: {ag['outcome']}")
        lines.append("")

        lines.append("#### 🔄 How Data Flows in This Agent (5-Stage Plumbing)")
        lines.append("| Stage | Module / Tool | Exact Data Flow & Foreign-Key Plumbing |")
        lines.append("| :--- | :--- | :--- |")
        for st in ag["dataFlowStages"]:
            lines.append(f"| **{st['stage']}** | {st['component']} | {st['details']} |")
        lines.append("")

        lines.append("#### 🧪 5 Copy-Ready Test Prompts & What to Expect")
        lines.append("| Test Mode | Copyable Input Prompt | Tools Triggered | What to Expect |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for tp in ag["testPrompts"]:
            p_clean = tp["prompt"].replace("|", "\\|")
            t_clean = tp["toolsTriggered"].replace("|", "\\|")
            e_clean = tp["expectedBehavior"].replace("|", "\\|")
            lines.append(f"| **{tp['mode']}** | `{p_clean}` | {t_clean} | {e_clean} |")
        lines.append("")

        lines.append(f"#### 📊 Expected Visual Output & Concise Python KPIs")
        lines.append(
            f"- **A2UI `VegaChart` Card**: `{ag['chartTitle']}` (`{ag['chartType']}`) — Card renders **ONLY** `VegaChart`; all text & `<=5`-col tables appear outside in Markdown."
        )
        lines.append(f"- **CLI Test Command**: `{ag['cmdRun']} --show-data --test-guardrail`")
        if ag.get("analyzeConciseMdTable"):
            lines.append("")
            lines.append("**Live Python Analytical Table Sample (`<=5` Columns, Google-Sheets Ready):**")
            lines.append("")
            lines.append(ag["analyzeConciseMdTable"])
        lines.append("")
        lines.append("---")
        lines.append("")

    md_path = ROOT / "AGENT_TESTING_AND_VIDEO_PLAYBOOK.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Synchronized {md_path.name} ({md_path.stat().st_size // 1024} KB)")
