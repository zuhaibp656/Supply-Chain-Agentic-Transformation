import json
import re
from pathlib import Path

ROOT = Path("/usr/local/google/home/zuhaibp/Supply_chain_Agentic_Transformation")

# 1. Update data/supply_chain_catalog.json: update "river" keys to "flow"
cat_path = ROOT / "data/supply_chain_catalog.json"
with open(cat_path, "r", encoding="utf-8") as f:
    cat = json.load(f)

flow_map = {
    "demand_sop": "Demand & Information Signal Flow (◀── Upstream)",
    "sourcing_procurement": "Inbound Supply & Invoicing Flow (Supplier to Plant)",
    "manufacturing_prod": "Physical Material Transformation Flow (Factory WIP & Assembly)",
    "inventory_meio": "Working Capital & Buffer Flow (Multi-Echelon DIO Optimization)",
    "warehouse_intralogistics": "Physical Material Flow (Node Custody & Automated Intralogistics)",
    "logistics_fleet": "Physical Material Flow (Multi-Modal Arteries: Road, Rail, Air & Ocean)",
    "trade_mkt_dist": "Last-Mile Distribution & Sell-Through Flow (Distributor, FSO Beat & Retail Shelf)",
    "reverse_logistics_esg": "Reverse Circular Material & Scope 3 ESG Audit Flow"
}

for dept_id, dept in cat.get("departments", {}).items():
    if "river" in dept:
        del dept["river"]
    dept["flow"] = flow_map.get(dept_id, "End-to-End Enterprise Synchronized Flow")

with open(cat_path, "w", encoding="utf-8") as f:
    json.dump(cat, f, indent=2)

print("Updated data/supply_chain_catalog.json flow definitions.")

