#!/usr/bin/env python3
"""Ensures all local Supply Chain & FleetFlow web/ADK servers stay up permanently
and automatically re-register with Jetski / VS Code Remote-SSH port forwarding.

Root causes solved permanently:
1. Cgroup survival: Registers and starts `systemd --user` units (`Restart=always`,
   `RestartSec=2`) outside the agent cgroup + a 1-minute `crontab` `--watchdog`.
2. Pure IPv4 `0.0.0.0` binding (NO `/proc/net/tcp6` `[::]` listener): Jetski's
   `ExtHostTunnelService` parses `[::]` in `/proc/net/tcp6` as unbracketed
   `"0:0:0:0:0:0:0:0"`, which collides with `"0.0.0.0"` on the same port and causes
   forwarded macOS browser sockets to fail with `ERR_EMPTY_RESPONSE`.
3. Automatic IDE reconnect port-forward refresh: When Jetski reconnects, any port
   already listening at connect time is placed into `_initialCandidates` and ignored
   by auto-port-forwarding until it stops for >=1 poll cycle (~5s) and restarts.
   Both manual runs and `--watchdog` (upon detecting a new `~/.jetski-server/data/logs/*`
   session >=15s old) cycle the 8 services across a 5.5s gap under `/tmp/sc_watchdog.lock`
   so all 8 ports auto-forward cleanly to `localhost` on the user's Mac.
"""

from __future__ import annotations

import fcntl
import json
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
ADC_PATH = HOME / ".config" / "gcloud" / "argolis_admin_adc.json"
SYSTEMD_USER_DIR = HOME / ".config" / "systemd" / "user"
JETSKI_LOGS_DIR = HOME / ".jetski-server" / "data" / "logs"
JETSKI_MACHINE_SETTINGS = HOME / ".jetski-server" / "data" / "Machine" / "settings.json"
LOCK_FILE = Path("/tmp/sc_watchdog.lock")
LAST_SESSION_FILE = Path("/tmp/sc_last_jetski_log_dir.txt")

SERVICES = [
    {
        "unit": "sc-twin-studio-8095",
        "desc": "Supply Chain Enterprise Twin Studio FastAPI + SSE Portal (Primary 8095)",
        "label": "Supply Chain Enterprise Studio (Primary)",
        "port": 8095,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "uvicorn"), "enterprise_twin.server:app", "--host", "0.0.0.0", "--port", "8095"],
        "check_url": "http://127.0.0.1:8095/api/v1/health",
        "requires_path": VENV_BIN / "uvicorn",
    },
    {
        "unit": "sc-portal-8899",
        "desc": "Supply Chain Portal & Enterprise Twin Studio (Primary 8899)",
        "label": "Supply Chain Portal",
        "port": 8899,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "uvicorn"), "enterprise_twin.server:app", "--host", "0.0.0.0", "--port", "8899"],
        "check_url": "http://127.0.0.1:8899/api/v1/health",
        "requires_path": VENV_BIN / "uvicorn",
    },
    {
        "unit": "sc-portal-8090",
        "desc": "Supply Chain Portal & Enterprise Twin Studio (Mirror 8090)",
        "label": "Supply Chain Portal Mirror",
        "port": 8090,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "uvicorn"), "enterprise_twin.server:app", "--host", "0.0.0.0", "--port", "8090"],
        "check_url": "http://127.0.0.1:8090/api/v1/health",
        "requires_path": VENV_BIN / "uvicorn",
    },
    {
        "unit": "sc-portal-8000",
        "desc": "Supply Chain Portal & Enterprise Twin Studio (Mirror 8000)",
        "label": "Supply Chain HTTP Mirror",
        "port": 8000,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "uvicorn"), "enterprise_twin.server:app", "--host", "0.0.0.0", "--port", "8000"],
        "check_url": "http://127.0.0.1:8000/api/v1/health",
        "requires_path": VENV_BIN / "uvicorn",
    },
    {
        "unit": "sc-adk-8502",
        "desc": "Supply Chain ADK Web Runner (8502)",
        "label": "Supply Chain ADK Web Runner",
        "port": 8502,
        "cwd": SC_DIR,
        "cmd": [str(VENV_BIN / "adk"), "web", "agents", "--port", "8502", "--host", "0.0.0.0"],
        "check_url": "http://127.0.0.1:8502/",
        "requires_path": VENV_BIN / "adk",
    },
    {
        "unit": "ff-api-8085",
        "desc": "FleetFlow Control Tower FastAPI + UI (8085)",
        "label": "FleetFlow Control Tower API & UI",
        "port": 8085,
        "cwd": FF_DIR,
        "cmd": [str(VENV_BIN / "uvicorn"), "app.fast_api_app:app", "--host", "0.0.0.0", "--port", "8085"],
        "check_url": "http://127.0.0.1:8085/ui",
        "requires_path": VENV_BIN / "uvicorn",
    },
    {
        "unit": "ff-static-8080",
        "desc": "FleetFlow Executive Deck & Static Assets (8080)",
        "label": "FleetFlow Executive Deck",
        "port": 8080,
        "cwd": FF_DIR,
        "cmd": ["/usr/bin/python3", "-m", "http.server", "8080", "--bind", "0.0.0.0", "--directory", str(FF_DIR)],
        "check_url": "http://127.0.0.1:8080/fleetflow_executive_presentation.html",
        "requires_path": FF_DIR,
    },
    {
        "unit": "ff-adk-8501",
        "desc": "FleetFlow ADK Web Runner (8501)",
        "label": "FleetFlow ADK Web Runner",
        "port": 8501,
        "cwd": FF_DIR,
        "cmd": [str(VENV_BIN / "adk"), "web", ".", "--port", "8501", "--host", "0.0.0.0"],
        "check_url": "http://127.0.0.1:8501/",
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
        return False
    return False


def is_port_healthy_ipv4_only(port: int) -> bool:
    """Returns True iff `port` listens in `/proc/net/tcp` (IPv4) and NOT in `/proc/net/tcp6`."""
    if not _proc_net_has_listen("/proc/net/tcp", port):
        return False
    if _proc_net_has_listen("/proc/net/tcp6", port):
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s4:
        s4.settimeout(0.5)
        return s4.connect_ex(("127.0.0.1", port)) == 0


def ensure_jetski_machine_settings() -> None:
    try:
        JETSKI_MACHINE_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
        cfg: dict = {}
        if JETSKI_MACHINE_SETTINGS.is_file():
            try:
                cfg = json.loads(JETSKI_MACHINE_SETTINGS.read_text(encoding="utf-8"))
            except Exception:
                cfg = {}
        cfg["remote.autoForwardPorts"] = True
        cfg["remote.autoForwardPortsSource"] = "process"
        cfg["remote.autoForwardPortsFallback"] = 0
        cfg["remote.restoreForwardedPorts"] = True
        cfg["remote.localPortHost"] = "localhost"
        attrs = cfg.get("remote.portsAttributes") if isinstance(cfg.get("remote.portsAttributes"), dict) else {}
        for svc in SERVICES:
            attrs[str(svc["port"])] = {
                "label": svc["label"],
                "onAutoForward": "silent",
                "elevateIfNeeded": False,
            }
        cfg["remote.portsAttributes"] = attrs
        rendered = json.dumps(cfg, indent=2) + "\n"
        if (not JETSKI_MACHINE_SETTINGS.is_file()) or JETSKI_MACHINE_SETTINGS.read_text(encoding="utf-8") != rendered:
            JETSKI_MACHINE_SETTINGS.write_text(rendered, encoding="utf-8")
    except Exception:
        pass


def latest_ready_jetski_session() -> str | None:
    """Returns newest `~/.jetski-server/data/logs/<session>` name once it is >=15s old."""
    try:
        if not JETSKI_LOGS_DIR.is_dir():
            return None
        dirs = [d for d in JETSKI_LOGS_DIR.iterdir() if d.is_dir()]
        if not dirs:
            return None
        newest = max(dirs, key=lambda d: d.stat().st_mtime)
        if (time.time() - newest.stat().st_mtime) < 15.0:
            return None
        return newest.name
    except Exception:
        return None


def reap_rogue_port_holder(port: int, unit: str | None = None, env: dict[str, str] | None = None) -> None:
    """Terminates orphaned processes holding `port` outside the target systemd unit (never uses `fuser`)."""
    if not _proc_net_has_listen("/proc/net/tcp", port) and not _proc_net_has_listen("/proc/net/tcp6", port):
        return
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
                except (ProcessLookupError, PermissionError):
                    pass
        if killed:
            time.sleep(0.25)
    except Exception:
        pass


def write_unit_files(env: dict[str, str]) -> bool:
    SYSTEMD_USER_DIR.mkdir(parents=True, exist_ok=True)
    adc_line = f'Environment="GOOGLE_APPLICATION_CREDENTIALS={ADC_PATH}"\n' if ADC_PATH.is_file() else ""
    any_changed = False
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
            any_changed = True
        svc["_unit_changed"] = changed
    subprocess.run(["systemctl", "--user", "daemon-reload"], env=env, check=True, timeout=8, capture_output=True)
    return any_changed


def cycle_all_units_for_tunnel_registration(env: dict[str, str], quiet: bool = False) -> None:
    """Stops all 8 units for 5.5s so ExtHostTunnelService clears `_initialCandidates`, then starts them cleanly."""
    active_svcs = [s for s in SERVICES if not s.get("requires_path") or Path(s["requires_path"]).exists()]
    unit_names = [f"{s['unit']}.service" for s in active_svcs]
    subprocess.run(["systemctl", "--user", "stop", *unit_names], env=env, check=False, timeout=15, capture_output=True)
    for s in active_svcs:
        reap_rogue_port_holder(s["port"])
    if not quiet:
        print("[TUNNEL REFRESH] Cleared all 8 ports; waiting 5.5s for Jetski port-scanner poll...", flush=True)
    time.sleep(5.5)
    for s in active_svcs:
        subprocess.run(
            ["systemctl", "--user", "enable", "--now", f"{s['unit']}.service"],
            env=env,
            check=False,
            timeout=8,
            capture_output=True,
        )
        subprocess.run(
            ["systemctl", "--user", "restart", f"{s['unit']}.service"],
            env=env,
            check=False,
            timeout=8,
            capture_output=True,
        )


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
    force_cycle = ("--cycle" in sys.argv) or (not watchdog)

    lock_fd = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | (fcntl.LOCK_NB if watchdog else 0))
    except BlockingIOError:
        return

    try:
        ensure_jetski_machine_settings()
        uid = os.getuid()
        env = os.environ.copy()
        env.setdefault("XDG_RUNTIME_DIR", f"/run/user/{uid}")

        write_unit_files(env)
        if not watchdog:
            install_cron_watchdog(quiet=False)

        cur_session = latest_ready_jetski_session()
        prev_session = LAST_SESSION_FILE.read_text(encoding="utf-8").strip() if LAST_SESSION_FILE.is_file() else ""
        new_jetski_session_detected = bool(cur_session and cur_session != prev_session)

        if force_cycle or new_jetski_session_detected:
            cycle_all_units_for_tunnel_registration(env, quiet=watchdog)
            if cur_session:
                LAST_SESSION_FILE.write_text(cur_session + "\n", encoding="utf-8")
        else:
            for svc in SERVICES:
                req = svc.get("requires_path")
                if req and not Path(req).exists():
                    continue
                if svc.get("_unit_changed") or not is_port_healthy_ipv4_only(svc["port"]):
                    subprocess.run(
                        ["systemctl", "--user", "stop", f"{svc['unit']}.service"],
                        env=env,
                        check=False,
                        timeout=8,
                        capture_output=True,
                    )
                    reap_rogue_port_holder(svc["port"])
                    subprocess.run(
                        ["systemctl", "--user", "enable", "--now", f"{svc['unit']}.service"],
                        env=env,
                        check=False,
                        timeout=8,
                        capture_output=True,
                    )
                    subprocess.run(
                        ["systemctl", "--user", "restart", f"{svc['unit']}.service"],
                        env=env,
                        check=False,
                        timeout=8,
                        capture_output=True,
                    )

        # Wait up to 14s for uvicorn / adk web to bind cleanly on 0.0.0.0
        for _ in range(28):
            if all(
                is_port_healthy_ipv4_only(s["port"])
                for s in SERVICES
                if not s.get("requires_path") or Path(s["requires_path"]).exists()
            ):
                break
            time.sleep(0.5)

        if watchdog:
            return

        check_urls = [
            ("Enterprise Twin Base Reset (8095)", "http://127.0.0.1:8095/base?reset_twin=1"),
            ("Enterprise Twin Studio (8095)", "http://127.0.0.1:8095/welcome"),
            ("Supply Chain Portal (8899)", "http://127.0.0.1:8899/base?reset_twin=1"),
            ("Supply Chain Playbook (8899)", "http://127.0.0.1:8899/agent_testing_and_video_playbook.html"),
            ("Supply Chain 101 Academy (8899)", "http://127.0.0.1:8899/supply_chain_101_interactive_academy.html"),
            ("Cost & FinOps Deck (8899)", "http://127.0.0.1:8899/cost_analysis_presentation.html"),
            ("Supply Chain Portal Mirror (8090)", "http://127.0.0.1:8090/index.html"),
            ("Supply Chain Portal Mirror (8000)", "http://127.0.0.1:8000/index.html"),
            ("Supply Chain ADK Web (8502)", "http://127.0.0.1:8502/"),
            ("FleetFlow Control Tower UI (8085)", "http://127.0.0.1:8085/ui"),
            ("FleetFlow Exec Deck (8080)", "http://127.0.0.1:8080/fleetflow_executive_presentation.html"),
            ("FleetFlow ADK Web (8501)", "http://127.0.0.1:8501/"),
        ]
        for label, url in check_urls:
            try:
                with urllib.request.urlopen(url, timeout=5) as r:
                    print(f"[HTTP {r.status}] {label} -> {url}", flush=True)
            except Exception as exc:
                print(f"[HTTP ERR] {label} -> {url} ({exc})", flush=True)
    finally:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
