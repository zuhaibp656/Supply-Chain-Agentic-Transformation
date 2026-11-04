#!/usr/bin/env python3
"""Ensures all local Supply Chain & FleetFlow web/ADK servers stay up permanently.

Why servers previously stopped:
- Child processes spawned directly inside an agent session share the agent server's
  cgroup, so when the agent server restarts, systemd kills the entire cgroup.

Permanent 2-layer fix:
1. Registers and starts `systemd --user` units (`Restart=always`, `RestartSec=2`)
   so every server runs in the user's own `user@<uid>.service` slice outside the
   agent cgroup and auto-restarts on crash or reboot.
2. Installs an idempotent 1-minute user `crontab` watchdog (`--watchdog`) as a
   belt-and-suspenders fallback in case `systemd --user` is ever unavailable.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import signal
import socket
import subprocess
import sys
import time
import urllib.request

HOME = Path.home()
SC_DIR = HOME / "Supply_chain_Agentic_Transformation"
FF_DIR = HOME / "high-code-agents" / "loadpilot-dispatch-agent"
VENV_BIN = FF_DIR / ".venv" / "bin"
DUAL_SERVE = SC_DIR / "scripts" / "dual_stack_serve.py"
ADC_PATH = HOME / ".config" / "gcloud" / "argolis_admin_adc.json"
SYSTEMD_USER_DIR = HOME / ".config" / "systemd" / "user"

SERVICES = [
    {
        "unit": "sc-twin-studio-8095",
        "desc": "Supply Chain Enterprise Twin Studio FastAPI + SSE Portal (Primary 8095)",
        "port": 8095,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "python3"), "-m", "enterprise_twin.server", "--host", "::", "--port", "8095"],
        "check_url": "http://127.0.0.1:8095/api/v1/health",
        "dual_stack": True,
        "requires_path": VENV_BIN / "python3",
    },
    {
        "unit": "sc-portal-8899",
        "desc": "Supply Chain Portal & Enterprise Twin Studio (Primary 8899)",
        "port": 8899,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "python3"), "-m", "enterprise_twin.server", "--host", "::", "--port", "8899"],
        "check_url": "http://127.0.0.1:8899/api/v1/health",
        "dual_stack": True,
        "requires_path": VENV_BIN / "python3",
    },
    {
        "unit": "sc-portal-8090",
        "desc": "Supply Chain Portal & Enterprise Twin Studio (Mirror 8090)",
        "port": 8090,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "python3"), "-m", "enterprise_twin.server", "--host", "::", "--port", "8090"],
        "check_url": "http://127.0.0.1:8090/api/v1/health",
        "dual_stack": True,
        "requires_path": VENV_BIN / "python3",
    },
    {
        "unit": "sc-portal-8000",
        "desc": "Supply Chain Portal & Enterprise Twin Studio (Mirror 8000)",
        "port": 8000,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "python3"), "-m", "enterprise_twin.server", "--host", "::", "--port", "8000"],
        "check_url": "http://127.0.0.1:8000/api/v1/health",
        "dual_stack": True,
        "requires_path": VENV_BIN / "python3",
    },
    {
        "unit": "sc-adk-8502",
        "desc": "Supply Chain ADK Web Runner (8502)",
        "port": 8502,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "python3"), str(DUAL_SERVE), "--port", "8502", "adk", "web", "agents", "--port", "8502", "--host", "::"],
        "check_url": "http://127.0.0.1:8502/",
        "dual_stack": True,
        "requires_path": VENV_BIN / "adk",
    },
    {
        "unit": "ff-api-8085",
        "desc": "FleetFlow Control Tower FastAPI + UI (8085)",
        "port": 8085,
        "cwd": FF_DIR,
        "cmd": [str(VENV_BIN / "python3"), str(DUAL_SERVE), "--port", "8085", "uvicorn", "app.fast_api_app:app", "--host", "::", "--port", "8085"],
        "check_url": "http://127.0.0.1:8085/ui",
        "dual_stack": True,
        "requires_path": VENV_BIN / "uvicorn",
    },
    {
        "unit": "ff-static-8080",
        "desc": "FleetFlow Executive Deck & Static Assets (8080)",
        "port": 8080,
        "cwd": FF_DIR,
        "cmd": ["/usr/bin/python3", str(DUAL_SERVE), "--port", "8080", "static-http", "--directory", str(FF_DIR)],
        "check_url": "http://127.0.0.1:8080/fleetflow_executive_presentation.html",
        "dual_stack": True,
        "requires_path": FF_DIR,
    },
    {
        "unit": "ff-adk-8501",
        "desc": "FleetFlow ADK Web Runner (8501)",
        "port": 8501,
        "cwd": FF_DIR,
        "cmd": [str(VENV_BIN / "python3"), str(DUAL_SERVE), "--port", "8501", "adk", "web", ".", "--port", "8501", "--host", "::"],
        "check_url": "http://127.0.0.1:8501/",
        "dual_stack": True,
        "requires_path": VENV_BIN / "adk",
    },
]


def _proc_net_has_listen(proc_path: str, port: int) -> bool:
    hex_port = f":{port:04X}"
    try:
        with open(proc_path, "r", encoding="utf-8", errors="ignore") as f:
            next(f, None)
            for line in f:
                parts = line.split()
                if len(parts) >= 4 and parts[3] == "0A" and parts[1].endswith(hex_port):
                    return True
    except OSError:
        return True
    return False


def is_port_open(port: int, dual_stack: bool = True) -> bool:
    if dual_stack and not (_proc_net_has_listen("/proc/net/tcp", port) and _proc_net_has_listen("/proc/net/tcp6", port)):
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s4:
        s4.settimeout(0.5)
        v4_ok = s4.connect_ex(("127.0.0.1", port)) == 0
    if not dual_stack:
        return v4_ok
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s6:
        s6.settimeout(0.5)
        v6_ok = s6.connect_ex(("::1", port)) == 0
    return v4_ok and v6_ok


def reap_rogue_port_holder(port: int, unit: str | None = None, env: dict[str, str] | None = None) -> None:
    """Terminates orphaned processes holding `port` outside the target systemd unit (never uses `fuser`)."""
    allowed_pids: set[int] = set()
    if unit and env:
        try:
            r = subprocess.run(
                ["systemctl", "--user", "show", "-p", "MainPID", "--value", f"{unit}.service"],
                env=env,
                capture_output=True,
                text=True,
                timeout=4,
            )
            mpid = int((r.stdout or "0").strip() or "0")
            if mpid > 0:
                allowed_pids.add(mpid)
        except Exception:
            pass

    try:
        res = subprocess.run(
            ["ss", "-H", "-tlnp", "sport", "=", f":{port}"],
            capture_output=True,
            text=True,
            timeout=4,
        )
        killed = False
        for m in re.finditer(r"pid=(\d+)", res.stdout or ""):
            pid = int(m.group(1))
            if pid > 1 and pid not in allowed_pids:
                try:
                    os.kill(pid, signal.SIGKILL)
                    killed = True
                except ProcessLookupError:
                    pass
                except PermissionError:
                    pass
        if killed:
            time.sleep(0.25)
    except Exception:
        pass


def build_env() -> dict[str, str]:
    env = os.environ.copy()
    env["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
    env["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
    env["GOOGLE_CLOUD_PROJECT"] = "zuhaibp-ai"
    env["GOOGLE_CLOUD_LOCATION"] = "global"
    if ADC_PATH.is_file():
        env["GOOGLE_APPLICATION_CREDENTIALS"] = str(ADC_PATH)
    return env


def install_systemd_user_units(quiet: bool = False) -> bool:
    try:
        SYSTEMD_USER_DIR.mkdir(parents=True, exist_ok=True)
        adc_line = f'Environment="GOOGLE_APPLICATION_CREDENTIALS={ADC_PATH}"\n' if ADC_PATH.is_file() else ""
        for svc in SERVICES:
            req = svc.get("requires_path")
            if req and not Path(req).exists():
                continue
            exec_start = " ".join(f'"{c}"' if " " in c else c for c in svc["cmd"])
            unit_text = f"""[Unit]
Description={svc['desc']}
After=network.target

[Service]
Type=simple
WorkingDirectory={svc['cwd']}
Environment="GOOGLE_API_USE_CLIENT_CERTIFICATE=false"
Environment="GOOGLE_GENAI_USE_VERTEXAI=TRUE"
Environment="GOOGLE_CLOUD_PROJECT=zuhaibp-ai"
Environment="GOOGLE_CLOUD_LOCATION=global"
{adc_line}ExecStart={exec_start}
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
"""
            unit_file = SYSTEMD_USER_DIR / f"{svc['unit']}.service"
            changed = (not unit_file.exists()) or (unit_file.read_text() != unit_text)
            if changed:
                unit_file.write_text(unit_text)
            svc["_unit_changed"] = changed

        uid = os.getuid()
        env = os.environ.copy()
        env.setdefault("XDG_RUNTIME_DIR", f"/run/user/{uid}")
        subprocess.run(["systemctl", "--user", "daemon-reload"], env=env, check=True, timeout=8, capture_output=True)
        for svc in SERVICES:
            req = svc.get("requires_path")
            if req and not Path(req).exists():
                continue
            reap_rogue_port_holder(svc["port"], svc["unit"], env)
            subprocess.run(
                ["systemctl", "--user", "enable", "--now", f"{svc['unit']}.service"],
                env=env,
                check=False,
                timeout=8,
                capture_output=True,
            )
            if svc.get("_unit_changed") or not is_port_open(svc["port"], bool(svc.get("dual_stack", True))):
                reap_rogue_port_holder(svc["port"], svc["unit"], env)
                subprocess.run(
                    ["systemctl", "--user", "restart", f"{svc['unit']}.service"],
                    env=env,
                    check=False,
                    timeout=8,
                    capture_output=True,
                )
        if not quiet:
            print("[SYSTEMD --USER] Installed and enabled auto-restarting user units (Restart=always).", flush=True)
        return True
    except Exception as exc:
        if not quiet:
            print(f"[SYSTEMD --USER] Fallback mode ({exc})", flush=True)
        return False


def ensure_fallback_processes(quiet: bool = False) -> None:
    env = build_env()
    for svc in SERVICES:
        req = svc.get("requires_path")
        if req and not Path(req).exists():
            continue
        if not is_port_open(svc["port"], bool(svc.get("dual_stack", True))):
            reap_rogue_port_holder(svc["port"])
            logf = open(f"/tmp/{svc['unit']}.log", "ab")
            subprocess.Popen(
                svc["cmd"],
                cwd=str(svc["cwd"]),
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=logf,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                close_fds=True,
            )
            logf.close()
            if not quiet:
                print(f"[FALLBACK START] {svc['unit']} on port {svc['port']}", flush=True)


def install_cron_watchdog(quiet: bool = False) -> None:
    script_path = Path(__file__).resolve()
    marker = "# sc-portal-persistent-watchdog"
    cron_line = f"* * * * * /usr/bin/python3 {script_path} --watchdog >/tmp/sc_watchdog.log 2>&1 {marker}"
    try:
        res = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
        existing = res.stdout if res.returncode == 0 else ""
        if marker not in existing:
            new_cron = (existing.rstrip() + "\n" + cron_line + "\n").lstrip()
            subprocess.run(["crontab", "-"], input=new_cron, text=True, check=True, timeout=5)
            if not quiet:
                print("[CRON WATCHDOG] Installed 1-minute self-healing crontab entry.", flush=True)
        else:
            if not quiet:
                print("[CRON WATCHDOG] Already active.", flush=True)
    except Exception as exc:
        if not quiet:
            print(f"[CRON WATCHDOG] Skipped ({exc})", flush=True)


def main() -> None:
    watchdog = "--watchdog" in sys.argv
    systemd_ok = False
    if not watchdog:
        systemd_ok = install_systemd_user_units(quiet=False)
        install_cron_watchdog(quiet=False)
    else:
        uid = os.getuid()
        env = os.environ.copy()
        env.setdefault("XDG_RUNTIME_DIR", f"/run/user/{uid}")
        systemd_ok = True
        for svc in SERVICES:
            req = svc.get("requires_path")
            if req and not Path(req).exists():
                continue
            if not is_port_open(svc["port"], bool(svc.get("dual_stack", True))):
                reap_rogue_port_holder(svc["port"], svc["unit"], env)
                r = subprocess.run(
                    ["systemctl", "--user", "restart", f"{svc['unit']}.service"],
                    env=env,
                    capture_output=True,
                    timeout=8,
                )
                if r.returncode != 0:
                    systemd_ok = False

    # Wait up to 12s for uvicorn / adk web to bind under systemd before falling back
    for _ in range(24):
        if all(
            is_port_open(s["port"], bool(s.get("dual_stack", True)))
            for s in SERVICES
            if not s.get("requires_path") or Path(s["requires_path"]).exists()
        ):
            break
        time.sleep(0.5)

    if not systemd_ok:
        ensure_fallback_processes(quiet=watchdog)

    if watchdog:
        return

    check_urls = [
        ("Enterprise Twin Base Reset (localhost:8095)", "http://localhost:8095/base?reset_twin=1"),
        ("Enterprise Twin Base Reset (127.0.0.1:8095)", "http://127.0.0.1:8095/base?reset_twin=1"),
        ("Enterprise Twin Base Reset ([::1]:8095)", "http://[::1]:8095/base?reset_twin=1"),
        ("Enterprise Twin Studio (Primary 8095)", "http://localhost:8095/welcome"),
        ("Supply Chain Playbook (Primary 8899)", "http://localhost:8899/agent_testing_and_video_playbook.html"),
        ("Supply Chain Portal (Primary 8899)", "http://localhost:8899/index.html"),
        ("Supply Chain 101 Academy (8899)", "http://localhost:8899/supply_chain_101_interactive_academy.html"),
        ("Cost & FinOps Deck (8899)", "http://localhost:8899/cost_analysis_presentation.html"),
        ("Supply Chain Playbook (Mirror 8090)", "http://localhost:8090/agent_testing_and_video_playbook.html"),
        ("Supply Chain Portal (Mirror 8090)", "http://localhost:8090/index.html"),
        ("Supply Chain Playbook (Mirror 8000)", "http://localhost:8000/agent_testing_and_video_playbook.html"),
        ("Supply Chain ADK Web (8502)", "http://localhost:8502/"),
        ("FleetFlow Control Tower UI (8085)", "http://localhost:8085/ui"),
        ("FleetFlow Exec Deck (8080)", "http://localhost:8080/fleetflow_executive_presentation.html"),
        ("FleetFlow ADK Web (8501)", "http://localhost:8501/"),
    ]
    for label, url in check_urls:
        try:
            with urllib.request.urlopen(url, timeout=4) as r:
                print(f"[HTTP {r.status}] {label} -> {url}", flush=True)
        except Exception as exc:
            print(f"[HTTP ERR] {label} -> {url} ({exc})", flush=True)


if __name__ == "__main__":
    main()
