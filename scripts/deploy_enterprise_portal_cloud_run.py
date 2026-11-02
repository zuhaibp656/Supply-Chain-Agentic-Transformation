#!/usr/bin/env python3
"""Deploys/Updates the Enterprise Twin Studio on Vertex AI Agent Engine + Google Cloud Run (`zuhaibp-ai`).

Follows strict repository rules:
  1. Never creates duplicate Vertex AI Agent Engines — reads `enterprise_twin/.reasoning_engine_id`
     and performs an in-place `remote_engine.update(...)` if already deployed!
  2. Deploys the unified FastAPI + SSE `"Welcome to Supply Chain"` Portal Studio to Cloud Run
     (`sc-enterprise-portal` in `us-central1`, project `zuhaibp-ai`) with `--allow-unauthenticated`,
     `2Gi` RAM, `2` vCPU, and `GOOGLE_CLOUD_PROJECT=zuhaibp-ai`.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai")
REGION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
STAGING_BUCKET = f"gs://{PROJECT_ID}-supply-chain-media"
CLOUD_RUN_SERVICE = "sc-enterprise-portal"
ENGINE_ID_FILE = ROOT_DIR / "enterprise_twin" / ".reasoning_engine_id"


def deploy_or_update_agent_engine() -> str:
    """Deploys or updates `EnterpriseTwinStudioAdkApp` in-place on Vertex AI Agent Engine."""
    import vertexai
    from vertexai import agent_engines

    from enterprise_twin.agent import EnterpriseTwinStudioAdkApp, root_agent
    from enterprise_twin.tools.gcp_auth import get_gcp_credentials

    if EnterpriseTwinStudioAdkApp is None or root_agent is None:
        raise RuntimeError("Google ADK / Vertex AI SDK not available in active Python environment.")

    creds, _ = get_gcp_credentials(PROJECT_ID)
    vertexai.init(
        project=PROJECT_ID,
        location=REGION,
        staging_bucket=STAGING_BUCKET,
        credentials=creds,
    )

    adk_app = EnterpriseTwinStudioAdkApp(agent=root_agent)
    requirements = [
        "google-cloud-aiplatform[adk,agent_engines]>=1.88.0",
        "google-genai>=1.16.0",
        "google-adk>=1.0.0",
        "pydantic>=2.8.0",
        "Pillow>=10.3.0",
        "google-cloud-storage>=2.16.0",
        "google-cloud-bigquery>=3.25.0",
    ]
    extra_packages = ["enterprise_twin", "data/supply_chain_catalog.json"]

    if ENGINE_ID_FILE.is_file():
        existing_res_name = ENGINE_ID_FILE.read_text(encoding="utf-8").strip()
        if existing_res_name:
            print(f"[Agent Engine] Updating existing deployment in-place: {existing_res_name}")
            existing = agent_engines.get(existing_res_name)
            updated = existing.update(
                agent_engine=adk_app,
                requirements=requirements,
                display_name="Supply Chain Enterprise Twin Studio Orchestrator",
                description="Researches enterprise companies & divisions, grounds career job titles & processes, filters relevant supply chain agents, and persists bespoke portals.",
                extra_packages=extra_packages,
            )
            return updated.resource_name

    print("[Agent Engine] Creating initial Enterprise Twin Studio Agent Engine...")
    created = agent_engines.create(
        agent_engine=adk_app,
        requirements=requirements,
        display_name="Supply Chain Enterprise Twin Studio Orchestrator",
        description="Researches enterprise companies & divisions, grounds career job titles & processes, filters relevant supply chain agents, and persists bespoke portals.",
        extra_packages=extra_packages,
    )
    ENGINE_ID_FILE.write_text(created.resource_name + "\n", encoding="utf-8")
    print(f"[Agent Engine] Saved resource ID -> {ENGINE_ID_FILE}: {created.resource_name}")
    return created.resource_name


def deploy_cloud_run() -> str:
    """Deploys the containerized FastAPI + SSE Welcome Studio & Portal Server to Cloud Run."""
    cmd = [
        "gcloud",
        "run",
        "deploy",
        CLOUD_RUN_SERVICE,
        "--source",
        str(ROOT_DIR),
        "--project",
        PROJECT_ID,
        "--region",
        REGION,
        "--allow-unauthenticated",
        "--memory",
        "2Gi",
        "--cpu",
        "2",
        "--timeout",
        "300",
        "--set-env-vars",
        f"GOOGLE_CLOUD_PROJECT={PROJECT_ID},GOOGLE_GENAI_USE_VERTEXAI=TRUE,SC_TWIN_PRO_MODEL=gemini-3.1-pro-preview,SC_TWIN_FLASH_MODEL=gemini-3.8-flash",
    ]
    env = os.environ.copy()
    env["CLOUDSDK_METRICS_ENVIRONMENT"] = (
        f"{env['CLOUDSDK_METRICS_ENVIRONMENT']} datacloud.antigravity"
        if env.get("CLOUDSDK_METRICS_ENVIRONMENT")
        else "datacloud.antigravity"
    )
    print("[Cloud Run] Deploying service:", " ".join(cmd))
    subprocess.run(cmd, cwd=str(ROOT_DIR), env=env, check=True)
    out = subprocess.check_output(
        [
            "gcloud",
            "run",
            "services",
            "describe",
            CLOUD_RUN_SERVICE,
            "--project",
            PROJECT_ID,
            "--region",
            REGION,
            "--format=value(status.url)",
        ],
        env=env,
        text=True,
    ).strip()
    print(f"[Cloud Run] Live Service URL: {out}")
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy Enterprise Twin Studio to Agent Engine + Cloud Run")
    parser.add_argument("--skip-agent-engine", action="store_true")
    parser.add_argument("--skip-cloud-run", action="store_true")
    args = parser.parse_args()

    if not args.skip_agent_engine:
        deploy_or_update_agent_engine()
    if not args.skip_cloud_run:
        deploy_cloud_run()
