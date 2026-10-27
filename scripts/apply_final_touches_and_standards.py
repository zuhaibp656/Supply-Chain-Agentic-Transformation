#!/usr/bin/env python3
"""Applies final touches, industry standards compliance metadata, FinOps profiles,
and 60-Agent / 60-Persona synchronization across:
1. data/supply_chain_catalog.json (metadata, periodicGroups, periodicAgentMeta for all 60 agents, standards & FinOps)
2. agents/*/agents-cli-manifest.yaml (standards_compliance & finops_profile)
3. enterprise_twin/* (60 personas & 60 agents support + cost_analysis_presentation.html bundling)
4. index.html, periodic_table.html, mind_map.html (zero stale 32/29/26 counts, updated Architecture SVG, and Cost & Scale Deck nav button)
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PILLAR_STANDARDS = {
    "demand_sop": [
        "ASCM SCOR DS v14.0 Plan (P1-P5)",
        "VICS CPFR Collaborative Planning Standard",
        "ISO 9001:2015 Quality Management",
        "Google ADK + A2A v1.0 + MCP + A2UI v0.9",
        "ISO/IEC 42001 AI Management System"
    ],
    "sourcing_procurement": [
        "ASCM SCOR DS v14.0 Source (S1-S3)",
        "ISO 20400:2017 Sustainable Procurement",
        "ANSI X12 EDI (850 PO / 855 Ack / 856 ASN / 810 Invoice)",
        "SOX Section 404 3-Way Match Internal Controls",
        "Google ADK + A2A v1.0 + MCP + A2UI v0.9"
    ],
    "manufacturing_prod": [
        "ASCM SCOR DS v14.0 Make (M1-M3)",
        "ISA-95 / IEC 62264 (Levels 2-4 MES/MOM Integration)",
        "OPC-UA Industrial Telemetry & IEEE 1588 PTP",
        "FDA 21 CFR Part 11 Electronic Batch Record (eBR) & cGMP",
        "ISO 50001 Energy Management + Google ADK / A2UI v0.9"
    ],
    "inventory_warehouse": [
        "ASCM SCOR DS v14.0 Deliver / Warehouse (D1-D3)",
        "GS1 EPCIS 2.0 & SSCC-18 Serialized Pallet Labelling",
        "USP <1079> Good Distribution Practice (GDP) Cold Chain",
        "OSHA 1910 Warehouse Ergonomics & Slotting Safety",
        "Google ADK + A2A v1.0 + MCP + A2UI v0.9"
    ],
    "logistics_fleet": [
        "ASCM SCOR DS v14.0 Deliver / Transport (D1-D4)",
        "ISO 28000:2022 Supply Chain Security Management",
        "ANSI X12 EDI (204 Tender / 214 Status / 210 Freight Invoice)",
        "FMCSA Hours-of-Service (HOS) & DOT Axle Weight Compliance",
        "Google ADK + A2A v1.0 + MCP + A2UI v0.9"
    ],
    "circular_enable": [
        "ASCM SCOR DS v14.0 Return & Enable (RL1-RL3, E1-E11)",
        "GHG Protocol Corporate Value Chain (Scope 1, 2 & 3) Standard",
        "EU CSRD (ESRS E1/E5) & CBAM Carbon Border Adjustment",
        "FDA FSMA Section 204 Food Traceability & HACCP",
        "Google ADK + A2A v1.0 + MCP + A2UI v0.9"
    ],
}

PRO_MODEL_AGENTS = {
    "npi_demand_profiler",
    "promo_lift_simulator",
    "sop_scenario_weaver",
    "disruption_war_room_orchestrator",
    "csco_control_tower_copilot",
    "legal_contract_redliner",
    "capex_simulator_agent",
    "network_design_digital_twin",
}


def update_catalog() -> dict:
    catalog_path = ROOT / "data" / "supply_chain_catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))

    # 1. Update top-level metadata
    catalog["metadata"] = {
        "title": "Gemini Enterprise — Supply Chain & Demand (Office of the CSCO) Agentic Transformation",
        "authors": ["Zuhaib Parvez", "Suman Banerjee"],
        "scorVerticalsCount": 6,
        "subPillarsCount": 20,
        "personasCount": 60,
        "agentsCount": 60,
        "universalAgentsCount": 4,
        "domainAgentsCount": 56,
        "valueChainsCount": 4,
        "verticalsCount": 6,
        "demoDataTablesCount": 245,
        "costAnalysisDeck": "cost_analysis_presentation.html",
        "standardsCompliance": [
            "ASCM SCOR Digital Standard (SCOR DS v14.0)",
            "ISA-95 / IEC 62264 & OPC-UA",
            "GS1 EPCIS 2.0 & FDA 21 CFR Part 11",
            "ANSI X12 EDI & UN/EDIFACT",
            "GHG Protocol Scope 1/2/3 & EU CSRD",
            "Google ADK + A2A Protocol + MCP + A2UI v0.9",
            "ISO/IEC 42001 & NIST AI RMF 1.0"
        ],
    }

    # 2. Update periodicGroups to match the 6 Pillars & 60 Agents
    catalog["periodicGroups"] = [
        {
            "id": "demand_sop",
            "code": "GROUP I · PLAN",
            "title": "01 · Planning & Strategy (9 Agents · 3 Sub-Pillars)",
            "color": "#10b981",
            "glow": "rgba(16,185,129,0.35)"
        },
        {
            "id": "sourcing_procurement",
            "code": "GROUP II · SOURCE",
            "title": "02 · Sourcing & Procurement (10 Agents · 3 Sub-Pillars)",
            "color": "#a855f7",
            "glow": "rgba(168,85,247,0.35)"
        },
        {
            "id": "manufacturing_prod",
            "code": "GROUP III · MAKE",
            "title": "03 · Manufacturing & Operations (10 Agents · 3 Sub-Pillars)",
            "color": "#3b82f6",
            "glow": "rgba(59,130,246,0.35)"
        },
        {
            "id": "inventory_warehouse",
            "code": "GROUP IV · STORE",
            "title": "04 · Warehousing & Fulfillment (10 Agents · 3 Sub-Pillars)",
            "color": "#00d2ff",
            "glow": "rgba(0,210,255,0.35)"
        },
        {
            "id": "logistics_fleet",
            "code": "GROUP V · MOVE",
            "title": "05 · Logistics & Transportation (12 Agents · 4 Sub-Pillars)",
            "color": "#f59e0b",
            "glow": "rgba(245,158,11,0.35)"
        },
        {
            "id": "circular_enable",
            "code": "GROUP VI · SUSTAIN",
            "title": "06 · Retail, Sustainability & Circular (9 Agents · 3 Sub-Pillars)",
            "color": "#f43f5e",
            "glow": "rgba(244,63,94,0.35)"
        }
    ]

    # 3. Ensure all 60 agents have periodicAgentMeta, standardsCompliance, and finopsProfile
    periodic_meta = catalog.get("periodicAgentMeta", {})
    for idx, (aid, agent) in enumerate(catalog["agents"].items(), start=1):
        dept_id = agent.get("departmentId", "demand_sop")
        standards = PILLAR_STANDARDS.get(dept_id, PILLAR_STANDARDS["demand_sop"])
        is_pro = aid in PRO_MODEL_AGENTS
        model_tier = "gemini-3.1-pro / gemini-4-argon" if is_pro else "gemini-3.8-flash"
        cost_per_1k = 15.80 if is_pro else 0.60

        agent["standardsCompliance"] = standards
        agent["finopsProfile"] = {
            "primaryRuntimeModel": model_tier,
            "contextCachingEnabled": True,
            "cacheDiscountPct": 75,
            "costPer1kInvocationsUsd": cost_per_1k,
            "fsp3YrDiscountPct": 20,
            "sharedBigQueryDataset": "supply_chain_twin",
            "tableCount": 4,
            "a2uiProtocolVersion": "v0.9"
        }

        # Populate periodicAgentMeta for all 60 agents
        words = [w for w in re.sub(r"[^A-Za-z0-9 ]+", " ", agent.get("plainName", aid)).split() if w]
        sym = (words[0][0] + (words[1][0] if len(words) > 1 else words[0][1:2])).capitalize()
        periodic_meta[aid] = {
            "num": idx,
            "sym": sym,
            "group": dept_id,
            "category": agent.get("category", ""),
            "subPillar": agent.get("subPillar", ""),
            "short": agent.get("plainName", aid)[:22],
            "role": agent.get("personaTitle", "Supply Chain Lead"),
            "kpi": (agent.get("roiBadges") or ["High ROI"])[0]
        }

    catalog["periodicAgentMeta"] = periodic_meta
    catalog_path.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    print(f"✅ Updated data/supply_chain_catalog.json: 60 agents, {len(periodic_meta)} periodicAgentMeta entries.")
    return catalog


def update_agent_manifests(catalog: dict) -> None:
    updated_count = 0
    for aid, agent in catalog["agents"].items():
        manifest_path = ROOT / "agents" / aid / "agents-cli-manifest.yaml"
        if not manifest_path.exists():
            continue
        text = manifest_path.read_text(encoding="utf-8")
        dept_id = agent.get("departmentId", "demand_sop")
        standards = PILLAR_STANDARDS.get(dept_id, PILLAR_STANDARDS["demand_sop"])
        is_pro = aid in PRO_MODEL_AGENTS
        model_tier = "gemini-3.1-pro / gemini-4-argon" if is_pro else "gemini-3.8-flash"
        cost_1k = "15.80" if is_pro else "0.60"

        if "standards_compliance:" not in text:
            addition = (
                f"  standards_compliance: \"{standards[0]} · {standards[1]} · A2UI v0.9\"\n"
                f"  finops_tier: \"{model_tier} (Context Cached -75%, 3-Yr FSP -20%, ${cost_1k}/1K calls)\"\n"
            )
            text = text.rstrip() + "\n" + addition
            manifest_path.write_text(text, encoding="utf-8")
            updated_count += 1
    print(f"✅ Enriched {updated_count} agents-cli-manifest.yaml files with standards_compliance & finops_tier.")


def update_enterprise_twin() -> None:
    # 1. Update enterprise_twin/agent.py
    agent_py = ROOT / "enterprise_twin" / "agent.py"
    txt = agent_py.read_text(encoding="utf-8")
    txt = txt.replace("26 SCOR roles", "60 SCOR roles")
    txt = txt.replace("26 SCOR personas", "60 SCOR personas")
    txt = txt.replace("32 AI Agents", "60 Categorized AI Agents")
    txt = txt.replace("32 AI agents", "60 Categorized AI agents")
    agent_py.write_text(txt, encoding="utf-8")

    # 2. Update enterprise_twin/generator/html_compiler.py to also include cost_analysis_presentation.html
    compiler_py = ROOT / "enterprise_twin" / "generator" / "html_compiler.py"
    ctxt = compiler_py.read_text(encoding="utf-8")
    if "cost_analysis_presentation.html" not in ctxt:
        ctxt = ctxt.replace(
            '        for f in [index_file, pt_file, mm_file]:\n            zf.write(f, arcname=f.name)',
            '        cost_src = ROOT_DIR / "cost_analysis_presentation.html"\n'
            '        if cost_src.exists():\n'
            '            cost_dst = out_dir / "cost_analysis_presentation.html"\n'
            '            cost_dst.write_text(cost_src.read_text(encoding="utf-8"), encoding="utf-8")\n'
            '        for f in [index_file, pt_file, mm_file] + ([out_dir / "cost_analysis_presentation.html"] if (out_dir / "cost_analysis_presentation.html").exists() else []):\n'
            '            zf.write(f, arcname=f.name)'
        )
        compiler_py.write_text(ctxt, encoding="utf-8")

    # 3. Update enterprise_twin/tools/agent_spec_miner.py to map new 60-agent IDs alongside legacy IDs
    asm_py = ROOT / "enterprise_twin" / "tools" / "agent_spec_miner.py"
    atxt = asm_py.read_text(encoding="utf-8")
    atxt = atxt.replace("32 AI Agents", "60 Categorized AI Agents").replace("32 AI agents", "60 Categorized AI agents")
    if "'finite_production_scheduler':" not in atxt:
        atxt += """

# Automatically alias canonical 60-agent IDs to industry-specific overrides
_ORIG_MINE_SPECS = mine_company_agent_specs

def mine_company_agent_specs(company_name: str, industry_id: str) -> Dict[str, Any]:
    res = dict(_ORIG_MINE_SPECS(company_name, industry_id))
    alias_pairs = [
        ("mps_finite_scheduler", "finite_production_scheduler"),
        ("category_should_cost", "rfq_should_cost_agent"),
        ("category_should_cost", "commodity_index_advisor"),
        ("tier_n_spanner_graph", "tier_n_risk_sentinel"),
        ("reverse_logistics_mgr", "reverse_rma_recommerce_agent"),
        ("reverse_logistics_mgr", "returns_triage_agent"),
    ]
    for old_k, new_k in alias_pairs:
        if old_k in res and new_k not in res:
            res[new_k] = dict(res[old_k])
    return res
"""
        asm_py.write_text(atxt, encoding="utf-8")

    # 4. Update enterprise_twin/tools/career_persona_miner.py to map new 60-persona IDs alongside legacy IDs
    cpm_py = ROOT / "enterprise_twin" / "tools" / "career_persona_miner.py"
    ptxt = cpm_py.read_text(encoding="utf-8")
    ptxt = ptxt.replace("26 supply chain roles", "60 supply chain roles").replace("26 SCOR roles", "60 SCOR roles")
    if "_ORIG_MINE_PERSONAS" not in ptxt:
        ptxt += """

# Automatically alias canonical 60-persona IDs to industry-specific overrides
_ORIG_MINE_PERSONAS = mine_company_personas

def mine_company_personas(company_name: str, industry_id: str) -> Dict[str, Any]:
    res = dict(_ORIG_MINE_PERSONAS(company_name, industry_id))
    persona_aliases = [
        ("demand_planning_dir", "demand_planner_forecaster"),
        ("sop_ibp_lead", "sop_supply_planning_dir"),
        ("category_sourcing_mgr", "category_manager_portfolio"),
        ("supplier_risk_lead", "supplier_risk_manager"),
        ("mps_scheduling_lead", "master_production_scheduler"),
        ("meio_inventory_mgr", "inventory_planning_manager"),
        ("dock_yard_supervisor", "yard_master_gate_controller"),
        ("fleet_dispatch_mgr", "transportation_planner_router"),
        ("reverse_logistics_mgr", "value_recovery_recommerce"),
    ]
    for old_k, new_k in persona_aliases:
        if old_k in res and new_k not in res:
            res[new_k] = dict(res[old_k])
    return res
"""
        cpm_py.write_text(ptxt, encoding="utf-8")
    print("✅ Updated enterprise_twin modules for 60 Categorized Agents & 60 Personas.")


def update_html_portals(catalog: dict) -> None:
    html_files = ["index.html", "periodic_table.html", "mind_map.html"]
    pg_json = json.dumps(catalog["periodicGroups"])
    pam_json = json.dumps(catalog["periodicAgentMeta"])

    for fname in html_files:
        fpath = ROOT / fname
        if not fpath.exists():
            continue
        html = fpath.read_text(encoding="utf-8")

        # 1. Replace stale text counts
        replacements = [
            ("32 AGENTS & 26 PERSONAS", "60 CATEGORIZED AGENTS & 60 PERSONAS"),
            ("26 PERSONAS & 32 AGENTS", "60 PERSONAS & 60 CATEGORIZED AGENTS"),
            ("26 SCOR personas and 32 AI agents", "60 SCOR personas and 60 categorized AI agents"),
            ("across all 26 personas", "across all 60 personas"),
            ("Used by All 29 Personas Across 6 SCOR Pillars", "Used by All 60 Personas Across 6 SCOR Pillars & 20 Sub-Pillars"),
            ("Explore All 32 Agents in Directory", "Explore All 60 Agents in Directory"),
            ("🌐 Universal · All 29 Personas", "🌐 Universal · All 60 Personas"),
            ("All 32 Agents Enterprise Architecture", "All 60 Agents Enterprise Architecture"),
            ("🤖 Browse All 32 Agents", "🤖 Browse All 60 Agents"),
            ("so all 35 agents operate in tandem", "so all 60 categorized agents operate in tandem"),
            ("🤖 Explore All 32 AI Agents", "🤖 Explore All 60 AI Agents"),
            ("👥 Explore All 29 Personas", "👥 Explore All 60 Personas"),
            (">32 Agents</div>", ">60 Agents</div>"),
            ("31 Domain Agents · 105 A2A Sub-Agents · 29 Personas", "56 Domain Agents · 180 A2A Sub-Agents · 60 Personas"),
            ("(SHARED ACROSS ALL 26 ROLES)", "(SHARED ACROSS ALL 60 ROLES)"),
            ("All 32 Agents", "All 60 Agents"),
            ("Universal Core Agents (Shared Across All 29 Roles)", "Universal Core Agents (Shared Across All 60 Roles)"),
            ("🌐 Universal Core · All 29 Roles", "🌐 Universal Core · All 60 Roles"),
            ("Mining VP & Director titles for 26 SCOR roles...", "Mining VP & Director titles for 60 SCOR roles..."),
            ("Calibrated 26 SCOR personas", "Calibrated 60 SCOR personas"),
            ("Customizing operational details inside 32 AI agents...", "Customizing operational details inside 60 categorized AI agents..."),
            # Architecture Swarm SVG 6 Pillars update
            ("{ title: '01 · PLAN (4 Agents)', sub1: 'PulseCast · Consensus', sub2: 'PromoLift · CPFR Sync', col: '#10b981', x: 34 }",
             "{ title: '01 · PLAN (9 Agents)', sub1: 'Demand · NPI · Promo · CPFR', sub2: 'Assortment · S&OP · Tower', col: '#10b981', x: 34 }"),
            ("{ title: '02 · SOURCE (4 Agents)', sub1: 'SourcePulse · NexusShield', sub2: 'ClauseGuard · QualiShield', col: '#a855f7', x: 210 }",
             "{ title: '02 · SOURCE (10 Agents)', sub1: 'Spend · Commodity · ShouldCost', sub2: 'Tier-N · Redliner · 3-Way Match', col: '#a855f7', x: 210 }"),
            ("{ title: '03 · MAKE (4 Agents)', sub1: 'ChronosMake · SpindleGuard', sub2: 'YieldVision · ChangeSync', col: '#3b82f6', x: 386 }",
             "{ title: '03 · MAKE (10 Agents)', sub1: 'Scheduler · CIP · LineBalance', sub2: 'PdM OEE · EMS · Batch Audit', col: '#3b82f6', x: 386 }"),
            ("{ title: '04 · FULFILL (5 Agents)', sub1: 'EchelonFlow · SlotMaster 3D', sub2: 'PromiseGuard · Yard · CrossDock', col: '#00d2ff', x: 562 }",
             "{ title: '04 · STORE (10 Agents)', sub1: 'MEIO · SLOB · Dock-to-Stock', sub2: '3D Slot · Wave · Cold Chain', col: '#00d2ff', x: 562 }"),
            ("{ title: '05 · DELIVER (7 Agents)', sub1: 'PortWatch · AeroFreight · Rail', sub2: 'ModalShift · FleetFlow · LIFO 3D', col: '#f59e0b', x: 738 }",
             "{ title: '05 · MOVE (12 Agents)', sub1: 'Fleet · 3D Load · EV · Yard', sub2: 'Drayage · FBAP · Last-Mile', col: '#f59e0b', x: 738 }"),
            ("{ title: '06 · ENABLE (4 Agents)', sub1: 'OTIFShield · ReturnLoop RMA', sub2: 'EcoChain ESG · TwinDesign', col: '#ec4899', x: 914 }",
             "{ title: '06 · SUSTAIN (9 Agents)', sub1: 'Markdown · Short-Dated · RMA', sub2: 'Scope 3 · Food Waste · RTI', col: '#ec4899', x: 914 }"),
        ]

        for old_s, new_s in replacements:
            html = html.replace(old_s, new_s)

        # 2. Add Cost & Scale Analysis Presentation link in top header if not already present
        if "cost_analysis_presentation.html" not in html:
            target_btn = 'onclick="openMindMapPage(\'mindmap\', null, null, false)"'
            if target_btn in html:
                # Insert a direct link button right after the Mind Map button in the top navigation
                html = re.sub(
                    r'(<button[^>]*onclick="openMindMapPage\(\'mindmap\'[^>]*>.*?</button>)',
                    r'\1\n        <a href="cost_analysis_presentation.html" class="top-nav-pill" style="text-decoration:none;display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,rgba(16,185,129,0.18),rgba(56,189,248,0.18));border:1px solid rgba(16,185,129,0.45);color:#ecfdf5;padding:7px 13px;border-radius:999px;font-size:12px;font-weight:700;" title="Open 9-Slide Enterprise Scale Cost &amp; FinOps Presentation">💰 Cost &amp; Scale Deck</a>',
                    html,
                    count=1,
                    flags=re.S
                )

        fpath.write_text(html, encoding="utf-8")
        print(f"✅ Updated {fname} with 60-agent counts, Architecture SVG, and Cost & Scale Deck link.")


if __name__ == "__main__":
    cat = update_catalog()
    update_agent_manifests(cat)
    update_enterprise_twin()
    update_html_portals(cat)
