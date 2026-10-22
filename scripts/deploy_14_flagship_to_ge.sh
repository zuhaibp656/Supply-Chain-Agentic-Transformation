#!/usr/bin/env bash
# ==============================================================================
# One-Command Deployer: 14 Flagship Supply Chain Agents (2 per Pillar) -> GE
# ==============================================================================
# Deploys 2 agents from each of the 6 SCOR Pillars + 2 from Universal CSCO Core:
#   1. Universal Core       : csco_control_tower_copilot & disruption_war_room_orchestrator
#   2. 01 · Plan            : demand_sensing_agent & sop_scenario_weaver
#   3. 02 · Source          : rfq_should_cost_agent & tier_n_risk_sentinel
#   4. 03 · Make            : plant_oee_maintenance_agent & inline_quality_inspection_agent
#   5. 04 · Fulfill         : echelon_inventory_allocator & dynamic_order_promising_atp
#   6. 05 · Deliver         : fleetflow_dispatch & load_consolidation_agent
#   7. 06 · Return & Enable : reverse_rma_optimizer & carbon_scope3_ledger
# ==============================================================================
set -euo pipefail

cd "$(dirname "$0")/.."
export GOOGLE_API_USE_CLIENT_CERTIFICATE=false

PYTHON_BIN="/usr/local/google/home/zuhaibp/high-code-agents/loadpilot-dispatch-agent/.venv/bin/python3"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python3"
fi

echo "Checking Argolis ADC credentials (~/.config/gcloud/application_default_credentials.json)..."
if ! "$PYTHON_BIN" -c '
import os, sys
from pathlib import Path
import google.oauth2.credentials
from google.auth.transport.requests import Request
os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
p = Path(os.path.expanduser("~/.config/gcloud/application_default_credentials.json"))
if not p.exists():
    sys.exit(1)
c = google.oauth2.credentials.Credentials.from_authorized_user_file(
    str(p), scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
c.refresh(Request())
' 2>/dev/null; then
  echo "Argolis ADC session expired (RAPT). Launching gcloud auth application-default login (sign in as admin@zuhaibp.altostrat.com)..."
  gcloud auth application-default login
fi

cp -f ~/.config/gcloud/application_default_credentials.json ~/.config/gcloud/argolis_admin_adc.json

echo "1/2 Publishing 142 Supply Chain Demo Data Tables to BigQuery & Cloud Storage..."
"$PYTHON_BIN" scripts/publish_supply_chain_data.py "$@"

echo "2/2 Deploying 14 Flagship Agents (2 per Pillar) to Vertex AI Agent Engine & Gemini Enterprise..."
"$PYTHON_BIN" scripts/deploy_to_gemini_enterprise.py --all-flagship "$@"
