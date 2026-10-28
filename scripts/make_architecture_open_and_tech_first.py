#!/usr/bin/env python3
"""
Transforms all customer-facing Agent Architecture, Execution Flow, Source Systems,
Solver Stack, Write-Back, and Full Spec Sheet descriptions across:
  - `data/supply_chain_catalog.json`
  - `index.html`
  - `periodic_table.html`
  - `mind_map.html`
into an OPEN, TECHNOLOGY-FIRST, CUSTOMER-AGNOSTIC architecture (supporting BigQuery,
On-Premise SQL/Databases, 3rd-Party SaaS MCP Servers, and REST/EDI Gateways)
without locking into specific products like AlloyDB, Cloud Spanner, Apigee,
WeatherNext, TimesFM, OR-Tools, or single-vendor ERPs.
Internal built agent packages (`agents/<id>/...`) remain untouched.
"""
import json
import re
from pathlib import Path

import build_distinct_agent_flow_diagrams

ROOT = Path(__file__).resolve().parent.parent

TECH_REPLACEMENTS = [
    # Databases & Storage
    (r"BigQuery\s*&\s*AlloyDB", "BigQuery, On-Prem SQL & Vector DB"),
    (r"BigQuery\s*/\s*AlloyDB\s*Twin", "BigQuery / On-Prem SQL / MCP Data Layer"),
    (r"AlloyDB\s*pgvector", "Vector Search & Semantic Index (DB / MCP)"),
    (r"AlloyDB\s*Vector\s*Search", "Vector Search & Semantic Index (DB / MCP)"),
    (r"\bAlloyDB\b", "Operational SQL & Vector DB (On-Prem / Cloud)"),
    (r"Cloud\s*Spanner\s*Graph", "Multi-Hop Graph Database (Cloud / On-Prem)"),
    (r"Cloud\s*Spanner\s*Constraint\s*Graph", "Multi-Hop Constraint Graph DB"),
    (r"Cloud\s*Spanner", "Low-Latency Transactional State DB"),
    (r"\bSpanner\s*Graph\b", "Multi-Hop Graph Database"),
    (r"\bSpanner\s*ATP\b", "Low-Latency Transactional ATP"),
    (r"\bSpanner\b", "Transactional State DB"),
    (r"BigQuery\s*:\s*zuhaibp-ai\.supply_chain_twin", "Pluggable Data Layer: BigQuery · On-Prem SQL · 3rd-Party MCPs"),

    # AI, Forecasting & Optimization Solvers
    (r"Vertex\s*AI\s*TimesFM\s*Foundation\s*Model", "Time-Series Forecasting Foundation Model"),
    (r"Vertex\s*AI\s*TimesFM\s*2\.5", "Time-Series Forecasting Foundation Model"),
    (r"Vertex\s*AI\s*TimesFM", "Time-Series Forecasting Model"),
    (r"\bTimesFM\s*2\.5\b", "Time-Series Forecasting Model"),
    (r"\bTimesFM\b", "Time-Series Forecasting Model"),
    (r"Google\s*OR-Tools\s*CP-SAT\s*/\s*MILP", "Mathematical Optimization Solver (MILP / CP-SAT)"),
    (r"Google\s*OR-Tools\s*CP-SAT", "Constraint Programming Solver (CP-SAT)"),
    (r"Google\s*OR-Tools", "Mathematical Optimization Solver (MILP / CP-SAT)"),
    (r"\bOR-Tools\b", "Mathematical Optimization Solver (MILP / CP-SAT)"),

    # Geospatial, Weather & External Feeds
    (r"Google\s*WeatherNext\s*3", "Weather & Climate Ensemble Feed (MCP / API)"),
    (r"\bWeatherNext\s*3\b", "Weather & Climate Ensemble Feed"),
    (r"Google\s*Earth\s*Engine", "Satellite & Geospatial Remote Sensing API"),
    (r"Google\s*Maps\s*Routes\s*Preferred\s*API", "Geospatial Routing & Traffic Telemetry API"),
    (r"Google\s*Maps\s*Routes\s*Preferred", "Geospatial Routing & Traffic API"),
    (r"Google\s*Maps\s*Routes\s*API", "Geospatial Routing & Traffic API"),
    (r"Google\s*Maps\s*Fleet\s*Engine", "Fleet & Yard Geofencing Telemetry API"),
    (r"Google\s*Maps\s*Places", "Geospatial & Location Intelligence API"),
    (r"Google\s*Maps\s*Platform", "Geospatial Routing & ETA Telemetry API"),
    (r"Spire\s*Ocean\s*AIS", "Ocean Vessel AIS Telemetry (MCP / API)"),
    (r"FlightAware\s*ADS-B", "Air Cargo Flight Telemetry (MCP / API)"),
    (r"Project44\s*·\s*FourKites", "Real-Time Carrier Visibility Platforms (MCP / API)"),
    (r"\bProject44\b", "Real-Time Carrier Visibility (MCP / API)"),
    (r"\bFourKites\b", "Carrier Transit Telemetry (MCP / API)"),

    # Enterprise ERPs, WMS, TMS, Portals & Gateways (Vendor -> Open Tech Category)
    (r"SAP\s*IBP\s*&\s*S/4HANA", "Enterprise ERP & Supply Planning (MCP / On-Prem / API)"),
    (r"SAP\s*IBP\s*/\s*S/4HANA", "Enterprise Planning & ERP (MCP / On-Prem / API)"),
    (r"SAP\s*IBP\s*·\s*SAP\s*S/4HANA", "Supply Planning System · Enterprise ERP (MCP / On-Prem DB)"),
    (r"\bSAP\s*IBP\b", "Supply Planning System (MCP / API)"),
    (r"SAP\s*S/4HANA\s*PP/DS", "Production Planning & ERP (MCP / On-Prem DB)"),
    (r"SAP\s*S/4HANA\s*SD/FI", "ERP Order & Finance Ledger (MCP / On-Prem DB)"),
    (r"SAP\s*S/4HANA\s*MM/FI", "ERP Material & Finance Ledger (MCP / On-Prem DB)"),
    (r"\bSAP\s*S/4HANA\b", "Enterprise ERP (MCP / On-Prem DB)"),
    (r"\bSAP\s*ECC\b", "On-Premise ERP System (SQL / BAPI / MCP)"),
    (r"\bSAP\s*EWM\b", "Warehouse Management System (WMS / MCP)"),
    (r"\bSAP\s*QM\b", "Quality Management System (QMS / ERP)"),
    (r"\bSAP\s*PM\b", "Plant Maintenance System (EAM / ERP)"),
    (r"\bSAP\s*TM\b", "Transportation Management System (TMS / MCP)"),
    (r"\bSAP\s*GTS\b", "Global Trade & Tariff System (MCP / API)"),
    (r"\bSAP\s*TPM\b", "Trade Promotion Management (TPM / CRM)"),
    (r"\bSAP\s*SD\b", "ERP Order Management (SD / MCP)"),
    (r"SAP\s*Ariba\s*·\s*Coupa", "e-Procurement & Supplier Portals (MCP / REST API)"),
    (r"\bSAP\s*Ariba\b", "e-Procurement & Sourcing Portal (MCP / API)"),
    (r"\bCoupa\b", "Spend & Procurement Platform (MCP / API)"),
    (r"Kinaxis\s*RapidResponse", "Concurrent Supply Planning Platform (MCP / API)"),
    (r"\bKinaxis\b", "Supply Planning Platform (MCP / API)"),
    (r"Hyperion\s*/\s*Anaplan\s*FP&A", "Enterprise FP&A & Financial Planning (MCP / API)"),
    (r"\bAnaplan\b", "Connected Planning Platform (MCP / API)"),
    (r"Manhattan\s*Active\s*WMS", "Warehouse Management System (WMS / On-Prem / API)"),
    (r"Blue\s*Yonder\s*TMS", "Transportation Management System (TMS / API)"),
    (r"Blue\s*Yonder\s*WMS", "Warehouse Management System (WMS / API)"),
    (r"\bBlue\s*Yonder\b", "Supply Chain Execution Platform (MCP / API)"),
    (r"Oracle\s*OTM", "Transportation Management System (TMS / API)"),
    (r"Salesforce\s*Consumer\s*Goods\s*Cloud", "Commercial CRM & Trade Portal (MCP / API)"),
    (r"Walmart\s*Luminate\s*·\s*Target\s*Greenfield\s*·\s*Amazon\s*Vendor\s*Central", "Retail Customer POS & e-Commerce Portals (EDI / MCP)"),
    (r"Walmart\s*Luminate", "Retail Customer POS Portal (EDI / MCP)"),
    (r"Target\s*Greenfield", "Retail Partner POS Analytics (MCP / EDI)"),
    (r"Amazon\s*Vendor\s*Central", "e-Commerce Vendor Portal (API / EDI)"),
    (r"Circana\s*/\s*NielsenIQ", "Syndicated Market & POS Data Feeds (MCP / API)"),
    (r"OSIsoft\s*PI", "Plant Process Historian (OPC-UA / On-Prem)"),
    (r"Siemens\s*WinCC\s*/\s*Rockwell\s*PLC", "Plant SCADA & PLC Telemetry (OPC-UA / MQTT)"),
    (r"Cognex\s*/\s*Keyence", "Industrial Line Vision Cameras (RTSP / Edge)"),
    (r"Apigee\s*Signed\s*ERP\s*Write-Back", "Signed MCP / REST / On-Prem ERP Write-Back"),
    (r"Apigee\s*Signed\s*ERP\s*Connector", "Signed MCP / REST / On-Prem ERP Connector"),
    (r"Apigee\s*Signed\s*ERP\s*API", "Signed MCP / REST / On-Prem ERP API"),
    (r"Apigee\s*APIs", "Enterprise API & MCP Gateways"),
    (r"via\s*Apigee", "via MCP / REST / On-Prem Gateway"),
    (r"\bApigee\b", "Enterprise API & MCP Gateway"),
]


def clean_tech_text(val):
    if isinstance(val, str):
        out = val
        for pat, rep in TECH_REPLACEMENTS:
            out = re.sub(pat, rep, out, flags=re.IGNORECASE)
        return out
    if isinstance(val, list):
        return [clean_tech_text(v) for v in val]
    if isinstance(val, dict):
        return {
            k: (v if k == "id" else clean_tech_text(v))
            for k, v in val.items()
        }
    return val


def clean_agent_dict(ag: dict) -> dict:
    """Cleans customer-facing architectural fields in an agent dictionary without altering IDs or tool function names."""
    fields_to_clean = [
        "systems",
        "solverStack",
        "apiWriteback",
        "solution",
        "advantage",
        "problem",
        "outcome",
        "description",
    ]
    for f in fields_to_clean:
        if f in ag and isinstance(ag[f], str):
            ag[f] = clean_tech_text(ag[f])

    if "subAgents" in ag and isinstance(ag["subAgents"], list):
        for sa in ag["subAgents"]:
            if isinstance(sa, dict):
                if "name" in sa:
                    sa["name"] = clean_tech_text(sa["name"])
                if "role" in sa:
                    sa["role"] = clean_tech_text(sa["role"])

    if "adkSpec" in ag and isinstance(ag["adkSpec"], dict):
        spec = ag["adkSpec"]
        if "systems" in spec and isinstance(spec["systems"], list):
            for s in spec["systems"]:
                if isinstance(s, dict):
                    if "name" in s:
                        s["name"] = clean_tech_text(s["name"])
                    if "protocol" in s:
                        s["protocol"] = clean_tech_text(s["protocol"])
                    else:
                        s["protocol"] = "MCP Server / REST API / BigQuery / On-Prem SQL"
        if "toolsMeta" in spec and isinstance(spec["toolsMeta"], list):
            for tm in spec["toolsMeta"]:
                if isinstance(tm, dict) and "description" in tm:
                    tm["description"] = clean_tech_text(tm["description"])
        if "evalScenarios" in spec and isinstance(spec["evalScenarios"], list):
            for ev in spec["evalScenarios"]:
                if isinstance(ev, dict):
                    if "query" in ev:
                        ev["query"] = clean_tech_text(ev["query"])
                    if "expected_proof_obligations" in ev and isinstance(ev["expected_proof_obligations"], list):
                        ev["expected_proof_obligations"] = [clean_tech_text(x) for x in ev["expected_proof_obligations"]]
    return ag


def update_catalog():
    cat_path = ROOT / "data" / "supply_chain_catalog.json"
    cat = json.loads(cat_path.read_text(encoding="utf-8"))
    for ag_id, ag in cat.get("agents", {}).items():
        clean_agent_dict(ag)
    cat_path.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Updated data/supply_chain_catalog.json with open technology-first metadata")


def update_html_file(path: Path):
    text = path.read_text(encoding="utf-8")

    # 1. Clean ONLY the `const AGENTS = { ... }` data block (up to `const PERSONAS = {`)
    ag_start = text.find("const AGENTS = {")
    pe_start = text.find("const PERSONAS = {")
    if ag_start != -1 and pe_start != -1 and pe_start > ag_start:
        seg_a = text[ag_start:pe_start]
        for pat, rep in TECH_REPLACEMENTS:
            seg_a = re.sub(pat, rep, seg_a, flags=re.IGNORECASE)
        text = text[:ag_start] + seg_a + text[pe_start:]

    # 2. Clean ONLY `renderAgentAtAGlanceStrip` and `renderAgentFullSpecSheet` (up to `function openAgentPage(`)
    spec_start = text.find("function renderAgentAtAGlanceStrip(")
    open_ag_start = text.find("function openAgentPage(")
    if spec_start != -1 and open_ag_start != -1 and open_ag_start > spec_start:
        seg_b = text[spec_start:open_ag_start]
        for pat, rep in TECH_REPLACEMENTS:
            seg_b = re.sub(pat, rep, seg_b, flags=re.IGNORECASE)
        seg_b = seg_b.replace(
            "Guarantees exactly-once execution across SAP S/4HANA, IBP, WMS, and TMS connectors.",
            "Guarantees exactly-once execution across Enterprise ERP, Planning, WMS, TMS, On-Premise DBs, and 3rd-party MCP connectors.",
        )
        seg_b = seg_b.replace(
            "Protocol: 'REST / OData v4 / BigQuery SQL'",
            "Protocol: 'MCP Server / REST API / BigQuery / On-Prem SQL'",
        )
        text = text[:spec_start] + seg_b + text[open_ag_start:]

    # 3. Clean `getAgentBuildClassification` labels
    cls_start = text.find("function getAgentBuildClassification(")
    cls_end = text.find("function getClickedCardRect(")
    if cls_start != -1 and cls_end != -1 and cls_end > cls_start:
        seg_c = text[cls_start:cls_end]
        seg_c = seg_c.replace(
            "label: '🟢 Low-Code · Gemini Enterprise Studio'",
            "label: '🟢 Low-Code · Conversational Agent + BigQuery / MCP RAG'",
        )
        seg_c = seg_c.replace(
            "label: '🔵 Hybrid · Low-Code Agent + Cloud Run Tool'",
            "label: '🔵 Hybrid · Conversational Agent + Serverless API / MCP Tool'",
        )
        seg_c = seg_c.replace(
            "label: '🟣 High-Code · Vertex ADK + OR-Tools Solver'",
            "label: '🟣 High-Code · Multi-Agent ADK + Mathematical Optimization Solver'",
        )
        text = text[:cls_start] + seg_c + text[cls_end:]

    path.write_text(text, encoding="utf-8")
    print(f"Cleaned open technology terminology in {path.name}")


def main():
    # Step 1: Update catalog & HTML data blocks
    update_catalog()
    for name in ("index.html", "periodic_table.html", "mind_map.html"):
        p = ROOT / name
        if p.exists():
            update_html_file(p)

    # Step 2: Inject fresh `NEW_ARCH_DIAGRAM_JS` AFTER text replacements so JS regex literals in `toOpenTechLabel` are never mutated!
    build_distinct_agent_flow_diagrams.main()


if __name__ == "__main__":
    main()
