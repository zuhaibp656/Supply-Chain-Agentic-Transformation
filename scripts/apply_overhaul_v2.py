import re

with open("build_site.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove the Interactive Multi-Echelon Safety Stock & ROP Calculator HTML block
calc_html_pattern = r'<!-- Interactive Multi-Echelon Safety Stock & ROP Calculator -->\s*<div class="ss-calc-card">[\s\S]*?</div>\s*(?=<!-- End-to-End Agentic Value Chains)'
if re.search(calc_html_pattern, content):
    content = re.sub(calc_html_pattern, '', content)
    print("Removed ss-calc-card HTML block successfully.")
else:
    print("Warning: calc_html_pattern not matched.")

# 2. Remove runSSCalc() call in selectDepartment
content = re.sub(r'\s*runSSCalc\(\);', '', content)

# 3. Remove runSSCalc() definition
run_ss_calc_def_pattern = r'/\* Live Interactive Safety Stock & ROP Calculator \*/\s*function runSSCalc\(\)\s*\{[\s\S]*?\n    \}'
if re.search(run_ss_calc_def_pattern, content):
    content = re.sub(run_ss_calc_def_pattern, '', content)
    print("Removed runSSCalc() function definition.")
else:
    print("Warning: run_ss_calc_def_pattern not matched.")

# 4. Update the "Three Rivers Flow" banner to "Three Synchronized Enterprise Flows" and remove confusing "River" nomenclature
content = content.replace(
    'across the <strong class="sc-hl-bold">Three Rivers Flow</strong> (Physical Material Flow, Demand/Information Flow, Cash/Working Capital Flow)',
    'across the <strong class="sc-hl-bold">Three Synchronized Enterprise Flows</strong> (Physical Material, Demand Signal, and Working Capital Cash)'
)

old_rivers_banner = """      <!-- Three Rivers Flow Architecture Banner -->
      <div class="rivers-banner">
        <div class="river-box">
          <h4>🌊 River 1: Physical Material Flow (Downstream ──▶)</h4>
          <p>Raw Materials / Agri Nodes ──▶ Factory WIP ──▶ Mother Warehouses ──▶ Regional Depots ──▶ Distributors ──▶ Retail Shelf / Kirana.</p>
        </div>
        <div class="river-box signal">
          <h4>📡 River 2: Demand &amp; Information Flow (◀── Upstream)</h4>
          <p>Consumer POS Scans ◀── FSO Beat Orders ◀── DMS Inventory ◀── S&amp;OP Consensus Forecast ◀── MRP BOM Explosion ◀── Vendor POs.</p>
        </div>
        <div class="river-box cash">
          <h4>💰 River 3: Cash &amp; Working Capital Flow (◀──▶ Cyclic)</h4>
          <p>Cash Conversion Cycle = Days Inventory (DIO) + Receivables (DSO) − Payables (DPO). Every excess day of dead stock locks corporate liquidity.</p>
        </div>
      </div>"""

new_rivers_banner = """      <!-- Three Synchronized Enterprise Flows Architecture Banner -->
      <div class="rivers-banner">
        <div class="river-box">
          <h4>📦 Flow 1: Physical Material Flow (Downstream ──▶)</h4>
          <p>Raw Materials / Sourcing ──▶ Manufacturing Transformation ──▶ Mother Warehouses ──▶ Multi-Modal Transit ──▶ Regional Hubs ──▶ Retail Shelf.</p>
        </div>
        <div class="river-box signal">
          <h4>📡 Flow 2: Demand &amp; Information Signal Flow (◀── Upstream)</h4>
          <p>Consumer POS Checkouts ◀── Channel Sell-Through ◀── Continuous Replenishment ◀── S&amp;OP Consensus ◀── MRP Master Schedule ◀── Supplier Contracts.</p>
        </div>
        <div class="river-box cash">
          <h4>💰 Flow 3: Working Capital &amp; Cash Flow (◀──▶ Cyclic)</h4>
          <p>Cash-to-Cash Cycle = Days Inventory Outstanding (DIO) + Days Sales Outstanding (DSO) − Days Payables (DPO). Unlocking trapped capital while protecting service fill rates.</p>
        </div>
      </div>"""

if old_rivers_banner in content:
    content = content.replace(old_rivers_banner, new_rivers_banner)
    print("Updated Three Rivers Flow banner to Three Synchronized Enterprise Flows.")
else:
    print("Warning: old_rivers_banner exact match not found; checking regex.")

# 5. Enhance renderVerticalWorkflowStrip to support all 8 departments (add V5, V6, V8)
workflow_insert = """      if (dept.id === 'warehouse_intralogistics') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(59, 130, 246, 0.06); border: 1px solid rgba(59, 130, 246, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#60a5fa; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>🏢 5-Stage Inbound Inwarding, Cross-Dock &amp; Automated Slotting Flow</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                ASN Scheduling &rarr; Vision Gate &rarr; Cross-Dock Decision &rarr; 3D AS/RS Slotting &rarr; Wave Pick
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 1 · Advance ASN</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Dock Door Scheduling</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">EDI 856 ingestion, trailer yard check-in, dynamic dock door assignment &amp; demurrage prevention.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 2 · Vision Gate</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Automated Inspection</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Camera portal pallet scan; detects crushed cartons, tilted stacks, and barcode read errors in &lt;1.2s.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 3 · Cross-Dock</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Zero-Putaway Staging</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Matches hot outbound backorders to bypass storage racks, moving straight to outbound outbound trailers.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 4 · 3D Slotting</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">AS/RS &amp; High-Bay Racks</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Multi-objective integer program places high-velocity SKUs at ergonomic levels with strict thermal zoning.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(59,130,246,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#60a5fa; text-transform:uppercase;">Stage 5 · Outbound Wave</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Pick Path Optimization</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Batch wave releases and AGV traveling salesman routing, minimizing picker deadhead travel by 32%.</div>
              </div>
            </div>
          </div>
        `;
      }
      if (dept.id === 'logistics_fleet') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(99, 102, 241, 0.06); border: 1px solid rgba(99, 102, 241, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#818cf8; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>🚚 5-Stage Multi-Modal Corridor Dispatch &amp; Linehaul Flow</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                3D Bay Packing &rarr; Mode Split &rarr; Dynamic Route Dispatch &rarr; Cold-Chain Tracking &rarr; Digital ePOD
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 1 · 3D Bay Packing</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">LIFO Axle-Weight Balance</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Physics-constrained 3D bin packing; optimizes axle weight distribution and reverse stop-drop sequencing.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 2 · Mode Split</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Air / Rail / Ocean / Road</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Trade-off solver balances freight cost vs carbon vs customer SLA, shifting freight to rail or ocean where viable.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 3 · Dynamic Routing</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Google Maps Fleet Engine</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Routes Preferred routing with live traffic, bridge height clearances, and driver corridor familiarity.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 4 · In-Transit Hub</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Satellite &amp; Telematics IoT</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Real-time Spire AIS / FlightAware / ELD tracking, geofence ETA countdowns, and cold-chain alert triggers.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(99,102,241,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase;">Stage 5 · Digital ePOD</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Instant Proof of Delivery</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Geofenced signature capture, discrepancy OS&amp;D logging, and automated freight audit freight billing lock.</div>
              </div>
            </div>
          </div>
        `;
      }
      if (dept.id === 'reverse_logistics_esg') {
        return `
          <div style="margin: 18px 0 20px; padding: 16px 20px; background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.28); border-radius: 14px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
              <div style="font-size:14px; font-weight:800; color:#34d399; text-transform:uppercase; letter-spacing:0.06em; display:flex; align-items:center; gap:8px;">
                <span>♻️ 5-Stage Circular Recovery, Component Harvesting &amp; ESG Audit Flow</span>
              </div>
              <div style="font-size:12px; color:#94a3b8;">
                RMA Intake &rarr; Visual Triage &rarr; Component Harvest &rarr; Secondary Resale &rarr; Scope 3 Audit
              </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 1 · RMA Intake</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Customer Tele-Diagnosis</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Instant digital returns portal; validates warranty, captures failure mode, and generates return routing label.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 2 · Visual Triage</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Gemini 3.8 Flash Grading</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Optical grade classification: directs item to Grade-A Restock, Component Harvest, or E-Waste Recycling.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 3 · Harvesting</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Remanufacturing Ingestion</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Disassembles high-value assemblies; recertifies sub-components and credits net recoverable inventory to MRP.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 4 · Secondary B2B</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">Liquidation &amp; Resale</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Dynamic secondary pricing agent matches refurbished inventory to certified outlet channels, recovering 42% margin.</div>
              </div>
              <div style="background:rgba(15,23,42,0.85); border:1px solid rgba(16,185,129,0.3); border-radius:10px; padding:12px;">
                <div style="font-size:11px; font-weight:700; color:#34d399; text-transform:uppercase;">Stage 5 · Scope 3 ESG</div>
                <div style="font-weight:700; color:#fff; font-size:13px; margin:4px 0 6px;">CBAM &amp; Audit Trail</div>
                <div style="font-size:12px; color:#94a3b8; line-height:1.45;">Automated emissions ledger tracking avoided carbon and circularity ratio for SEC / EU CSRD compliance.</div>
              </div>
            </div>
          </div>
        `;
      }
"""

if "if (dept.id === 'warehouse_intralogistics')" not in content:
    content = content.replace("return '';\n    }\n\n    function renderDepartmentShowcaseBox()", workflow_insert + "\n      return '';\n    }\n\n    function renderDepartmentShowcaseBox()")
    print("Enhanced renderVerticalWorkflowStrip with all 8 verticals.")

with open("build_site.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Pass 1 of build_site.py complete.")
