#!/usr/bin/env python3
"""In-Place Cloud Updater & Live Dual-Surface A2UI + Data-Source Tool Smoke-Test Pipeline
for All 25 Curated Showcase Agents on Vertex AI Reasoning Engine (`zuhaibp-ai`, `us-central1`)
and Gemini Enterprise (`gemini-enterprise-zuhaibp_1784012666241`).

Usage:
    /usr/local/google/home/zuhaibp/high-code-agents/loadpilot-dispatch-agent/.venv/bin/python3 -u scripts/update_all_showcase_agents_inplace.py
"""
from __future__ import annotations

import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from typing import Any, Dict, List

# Force IPv4 to avoid CloudTop IPv6 timeouts
_orig_getaddrinfo = socket.getaddrinfo
socket.getaddrinfo = lambda host, port, family=0, type=0, proto=0, flags=0: _orig_getaddrinfo(
    host, port, socket.AF_INET, type, proto, flags
)
os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT))

from deploy_to_gemini_enterprise import (  # noqa: E402
    ALL_AGENTS_CONFIG,
    CURATED_SHOWCASE_25_IDS,
    enable_apis,
    ensure_bucket,
    get_credentials,
    register_gemini_enterprise,
    sync_gcloud_db_to_argolis_adc,
)

PROJECT = "zuhaibp-ai"
REGION = "us-central1"
GE_APP_ID = "gemini-enterprise-zuhaibp_1784012666241"
STAGING_BUCKET = f"{PROJECT}-agent-staging"
MEDIA_BUCKET = f"{PROJECT}-supply-chain-media"

FORBIDDEN_GENERIC_TOOLS = {
    "list_systems",
    "lookup_xyz_master_context",
    "analyze_operational_metrics",
    "render_visual_chart",
    "draft_operational_brief",
    "export_operational_csv_schedule",
    "generate_interactive_html_dashboard",
}


def live_smoke_test_engine(agent_id: str, prompt: str) -> Dict[str, Any]:
    """Queries the live deployed Vertex AI Reasoning Engine and validates Dual-Surface A2UI + data-source tools."""
    import google.auth
    import vertexai
    from vertexai import agent_engines

    state_file = REPO_ROOT / "agents" / agent_id / ".reasoning_engine_id"
    re_name = state_file.read_text().strip()
    creds = get_credentials()
    google.auth.default = lambda *a, **k: (creds, PROJECT)
    vertexai.init(project=PROJECT, location=REGION, staging_bucket=f"gs://{STAGING_BUCKET}", credentials=creds)

    remote_app = agent_engines.get(re_name)
    t0 = time.time()
    events: List[Any] = []
    for ev in remote_app.stream_query(user_id=f"live-verify-{int(t0)}", message=prompt):
        events.append(ev)
    elapsed = round(time.time() - t0, 1)

    raw_dump = json.dumps(events, default=str)
    has_a2ui_tag = "<a2a_datapart_json>" in raw_dump
    has_vega = "VegaChart" in raw_dump
    has_canvas = False
    has_rich_table = False
    has_vconcat = False
    has_iframe = "IFrameSrcdoc" in raw_dump

    text_chunks: List[str] = []
    a2ui_payloads: List[Dict[str, Any]] = []
    called_tools: List[str] = []

    for ev in events:
        if not isinstance(ev, dict):
            continue
        content = ev.get("content") or {}
        parts = content.get("parts") or []
        for p in parts:
            if not isinstance(p, dict):
                continue
            fc = p.get("function_call") or p.get("functionCall")
            if isinstance(fc, dict) and fc.get("name"):
                called_tools.append(str(fc["name"]))
            if p.get("text"):
                text_chunks.append(str(p["text"]))
            inl = p.get("inline_data") or p.get("inlineData")
            if isinstance(inl, dict) and inl.get("data"):
                data_val = inl["data"]
                decoded = ""
                if isinstance(data_val, (bytes, bytearray)):
                    decoded = bytes(data_val).decode("utf-8", errors="ignore")
                elif isinstance(data_val, str):
                    if "<a2a_datapart_json>" in data_val:
                        decoded = data_val
                    else:
                        try:
                            padded = data_val + "=" * (-len(data_val) % 4)
                            decoded = base64.urlsafe_b64decode(padded).decode("utf-8", errors="ignore")
                        except Exception:
                            decoded = data_val
                if "<a2a_datapart_json>" in decoded:
                    has_a2ui_tag = True
                    s = decoded.find("<a2a_datapart_json>") + len("<a2a_datapart_json>")
                    e = decoded.find("</a2a_datapart_json>")
                    if e > s:
                        try:
                            a2ui_payloads.append(json.loads(decoded[s:e]))
                        except Exception:
                            pass

    a2ui_dump = json.dumps(a2ui_payloads)
    if "VegaChart" in a2ui_dump:
        has_vega = True
    if "vconcat" in a2ui_dump:
        has_vconcat = True
    if '"Canvas"' in a2ui_dump:
        has_canvas = True
    if '"RichTable"' in a2ui_dump:
        has_rich_table = True

    generic_leaks = [t for t in called_tools if t in FORBIDDEN_GENERIC_TOOLS]
    full_text = "\n".join(text_chunks)
    result = {
        "agent_id": agent_id,
        "reasoning_engine": re_name,
        "elapsed_s": elapsed,
        "event_count": len(events),
        "called_tools": called_tools,
        "generic_tool_leaks": generic_leaks,
        "a2ui_part_count": len(a2ui_payloads),
        "has_a2ui_tag": has_a2ui_tag,
        "has_vega_chart": has_vega,
        "has_2panel_vconcat": has_vconcat,
        "has_canvas": has_canvas,
        "has_rich_table": has_rich_table,
        "has_iframe_leak": has_iframe,
        "text_length": len(full_text),
        "text_preview": full_text[:360].replace("\n", " "),
    }
    print(
        f"  [SMOKE TEST] {agent_id} ({re_name.split('/')[-1]}) in {elapsed}s | "
        f"tools={called_tools} | a2ui_parts={len(a2ui_payloads)} | "
        f"VegaChart={has_vega} (2Panel={has_vconcat}) | Canvas={has_canvas} | RichTable={has_rich_table} | "
        f"IFrameLeak={has_iframe} | text_len={len(full_text)}",
        flush=True,
    )
    return result


def deploy_one_subprocess(agent_id: str, skip_ge: bool = False) -> tuple[str, int, str]:
    cmd = [
        sys.executable,
        "-u",
        str(REPO_ROOT / "scripts" / "deploy_to_gemini_enterprise.py"),
        "--agent",
        agent_id,
        "--project",
        PROJECT,
        "--region",
        REGION,
        "--staging-bucket",
        STAGING_BUCKET,
        "--media-bucket",
        MEDIA_BUCKET,
    ]
    if skip_ge:
        cmd.append("--skip-ge")
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    out = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return agent_id, proc.returncode, out


def main() -> None:
    sync_gcloud_db_to_argolis_adc(PROJECT)
    enable_apis(PROJECT)
    ensure_bucket(PROJECT, REGION, STAGING_BUCKET)
    ensure_bucket(PROJECT, REGION, MEDIA_BUCKET)

    print("\n=== PHASE 1: PRIORITY IN-PLACE UPDATE OF `three_way_match_dispute` ===", flush=True)
    aid, rc, out = deploy_one_subprocess("three_way_match_dispute", skip_ge=False)
    print(out, flush=True)
    if rc != 0:
        raise RuntimeError(f"three_way_match_dispute deploy failed with exit code {rc}")

    res_3wm = live_smoke_test_engine(
        "three_way_match_dispute",
        "Review our open purchase orders, goods receipts, and vendor invoices for three-way match variances and show an interactive variance chart.",
    )
    assert res_3wm["has_a2ui_tag"] and res_3wm["has_vega_chart"], f"Cloud A2UI VegaChart missing: {res_3wm}"
    assert res_3wm["has_canvas"] and res_3wm["has_rich_table"], f"Cloud A2UI Canvas RichTable missing: {res_3wm}"
    assert not res_3wm["generic_tool_leaks"], f"Generic tools leaked: {res_3wm['generic_tool_leaks']}"

    remaining_24 = [a for a in CURATED_SHOWCASE_25_IDS if a != "three_way_match_dispute"]
    print(f"\n=== PHASE 2: PARALLEL IN-PLACE UPDATE OF REMAINING {len(remaining_24)} SHOWCASE AGENTS ===", flush=True)

    failures: List[str] = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futs = {pool.submit(deploy_one_subprocess, a, True): a for a in remaining_24}
        done_count = 0
        for fut in as_completed(futs):
            done_count += 1
            a_id, code, log_out = fut.result()
            key_lines = [
                ln for ln in log_out.splitlines()
                if any(k in ln for k in (f"[{a_id}]", "ERROR", "Traceback", "OK in"))
            ]
            print(f"[{done_count:02d}/{len(remaining_24)}] {a_id} (rc={code}): " + " | ".join(key_lines[-3:]), flush=True)
            if code != 0:
                failures.append(a_id)

    if failures:
        still_failed = []
        for a_id in failures:
            _, code, _ = deploy_one_subprocess(a_id, skip_ge=True)
            if code != 0:
                still_failed.append(a_id)
        failures = still_failed

    for a_id in CURATED_SHOWCASE_25_IDS:
        spec = ALL_AGENTS_CONFIG[a_id]
        state_file = REPO_ROOT / "agents" / a_id / ".reasoning_engine_id"
        engine_res = state_file.read_text().strip() if state_file.exists() else ""
        if engine_res:
            register_gemini_enterprise(a_id, spec, PROJECT, engine_res, GE_APP_ID, "global", dry_run=False)

    subprocess.run(
        [
            sys.executable,
            "-u",
            str(REPO_ROOT / "scripts" / "deploy_to_gemini_enterprise.py"),
            "--curated-showcase",
            "--skip-engine",
            "--skip-ge",
        ],
        cwd=str(REPO_ROOT),
        check=True,
    )

    print("\n=== PHASE 3: LIVE MULTI-PILLAR CLOUD SMOKE TESTS ===", flush=True)
    for s_id, s_prompt in [
        ("demand_sensing_agent", "Show me an interactive regional demand forecast comparison chart and highlight the largest upside signals."),
        ("cold_chain_auditor", "Audit our active cold-chain shipments for temperature excursions and render an interactive chart."),
        ("freight_bill_audit_agent", "Review carrier freight invoices against contracted tariffs and show an interactive overcharge variance chart."),
    ]:
        r = live_smoke_test_engine(s_id, s_prompt)
        assert r["has_a2ui_tag"] and r["has_vega_chart"] and r["has_canvas"] and r["has_rich_table"]

    if failures:
        raise RuntimeError(f"Some showcase agents failed to update: {failures}")

    print("\n🎉 ALL 25 CURATED SHOWCASE AGENTS UPDATED IN-PLACE & LIVE-VERIFIED!", flush=True)


if __name__ == "__main__":
    main()
