"""Unified Google Cloud Auth Helper for Cloud Run, Vertex AI Agent Engine & Local CloudTop.

- In Cloud Run or Vertex AI Agent Engine containers: uses native default service account credentials.
- On local CloudTop workstations: disables mTLS client-cert proxy (`GOOGLE_API_USE_CLIENT_CERTIFICATE=false`)
  and loads Argolis credentials (`admin@zuhaibp.altostrat.com`) from `~/.config/gcloud/argolis_admin_adc.json`
  (syncing fresh refresh tokens from `~/.config/gcloud/credentials.db` while ignoring VSCode's 681255809395 client).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
from typing import Any, Optional, Tuple

DEFAULT_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai")
DEFAULT_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
DEFAULT_GCS_BUCKET = os.environ.get("SC_TWIN_BUCKET", "zuhaibp-ai-supply-chain-media")
DEFAULT_BQ_DATASET = os.environ.get("SC_TWIN_BQ_DATASET", "supply_chain_twin")
DEFAULT_BQ_TABLE = os.environ.get("SC_TWIN_BQ_TABLE", "enterprise_portals")

GCLOUD_DIR = Path.home() / ".config" / "gcloud"


def is_cloud_runtime() -> bool:
    """Returns True when executing inside Cloud Run (`K_SERVICE`) or Agent Engine."""
    return bool(os.environ.get("K_SERVICE") or os.environ.get("CLOUD_RUN_JOB") or os.path.exists("/code/app"))


def sync_local_argolis_adc(project: str = DEFAULT_PROJECT) -> Optional[Path]:
    """Syncs fresh Argolis OAuth refresh token on developer workstation if present."""
    if is_cloud_runtime():
        return None
    os.environ.setdefault("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
    adc_path = GCLOUD_DIR / "argolis_admin_adc.json"
    db_path = GCLOUD_DIR / "credentials.db"
    if db_path.exists():
        try:
            conn = sqlite3.connect(str(db_path))
            cur = conn.cursor()
            cur.execute("SELECT account_id, value FROM credentials")
            for account_id, val in cur.fetchall():
                if "zuhaibp.altostrat.com" in account_id:
                    data = json.loads(val)
                    cid = str(data.get("client_id", ""))
                    if cid.startswith("681255809395"):
                        continue
                    if data.get("refresh_token") and cid:
                        payload = {
                            "account": account_id,
                            "client_id": cid,
                            "client_secret": data["client_secret"],
                            "refresh_token": data["refresh_token"],
                            "type": "authorized_user",
                            "quota_project_id": project,
                        }
                        adc_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
                    break
            conn.close()
        except Exception:
            pass
    return adc_path if adc_path.exists() else None


_CLI_TOKEN_CACHE: Tuple[float, Optional[str]] = (0.0, None)


def _get_gcloud_cli_token() -> Optional[str]:
    global _CLI_TOKEN_CACHE
    import subprocess
    import time

    now = time.time()
    if _CLI_TOKEN_CACHE[1] and (now - _CLI_TOKEN_CACHE[0]) < 900:
        return _CLI_TOKEN_CACHE[1]
    try:
        env = os.environ.copy()
        env["CLOUDSDK_METRICS_ENVIRONMENT"] = (
            f"{env['CLOUDSDK_METRICS_ENVIRONMENT']} datacloud.antigravity"
            if env.get("CLOUDSDK_METRICS_ENVIRONMENT")
            else "datacloud.antigravity"
        )
        tok = subprocess.check_output(
            ["gcloud", "auth", "print-access-token", "--account=admin@zuhaibp.altostrat.com"],
            env=env,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=6,
        ).strip()
        if tok:
            _CLI_TOKEN_CACHE = (now, tok)
            return tok
    except Exception:
        pass
    return None


def get_gcp_credentials(project: str = DEFAULT_PROJECT) -> Tuple[Optional[Any], str]:
    """Returns `(google.auth.credentials.Credentials, project_id)` for Vertex AI / BQ / GCS."""
    import google.auth

    if not is_cloud_runtime():
        os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
        adc_path = sync_local_argolis_adc(project)
        if adc_path and adc_path.exists():
            try:
                import google.oauth2.credentials
                from google.auth.transport.requests import Request

                creds = google.oauth2.credentials.Credentials.from_authorized_user_file(
                    str(adc_path),
                    scopes=["https://www.googleapis.com/auth/cloud-platform"],
                )
                creds.refresh(Request())
                return creds, project
            except Exception:
                pass

        cli_tok = _get_gcloud_cli_token()
        if cli_tok:
            import google.oauth2.credentials

            return google.oauth2.credentials.Credentials(token=cli_tok, quota_project_id=project), project

    try:
        creds, detected_proj = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        return creds, (project or detected_proj or DEFAULT_PROJECT)
    except Exception:
        return None, project


def get_genai_client(location: str = "global") -> Any:
    """Builds a `google.genai.Client` routed to Vertex AI (`location='global'` for Gemini 3 series)."""
    from google import genai
    from google.genai import types

    creds, project = get_gcp_credentials(DEFAULT_PROJECT)
    kwargs: dict[str, Any] = {
        "vertexai": True,
        "project": project,
        "location": location,
        "http_options": types.HttpOptions(timeout=90_000),
    }
    if creds is not None:
        kwargs["credentials"] = creds
    return genai.Client(**kwargs)
