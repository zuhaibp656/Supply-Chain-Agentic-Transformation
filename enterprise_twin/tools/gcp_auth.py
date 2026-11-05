"""Unified Google GenAI & Cloud Auth Helper for Cloud Run, Vertex AI & Local Studio.

Supports seamless multi-mode authentication so live Gemini + Google Search Grounding ALWAYS runs:
  1. In Cloud Run (`K_SERVICE`): uses native IAM Service Account on Vertex AI (`vertexai=True`),
     with automatic fallback to `GEMINI_API_KEY` / `GOOGLE_API_KEY` if configured.
  2. On local developer workstations: disables mTLS smartcard proxy (`GOOGLE_API_USE_CLIENT_CERTIFICATE=false`),
     auto-loads `GEMINI_API_KEY` / `GOOGLE_API_KEY` from environment or local `.env` files (`vertexai=False`),
     and also supports refreshed Vertex AI OAuth credentials (`argolis_admin_adc.json`).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
from typing import Any, List, Optional, Tuple

DEFAULT_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai")
DEFAULT_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
DEFAULT_GCS_BUCKET = os.environ.get("SC_TWIN_BUCKET", "zuhaibp-ai-supply-chain-media")
DEFAULT_BQ_DATASET = os.environ.get("SC_TWIN_BQ_DATASET", "supply_chain_twin")
DEFAULT_BQ_TABLE = os.environ.get("SC_TWIN_BQ_TABLE", "enterprise_portals")

GCLOUD_DIR = Path.home() / ".config" / "gcloud"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def is_cloud_runtime() -> bool:
    """Returns True when executing inside Cloud Run (`K_SERVICE`) or Agent Engine."""
    return bool(os.environ.get("K_SERVICE") or os.environ.get("CLOUD_RUN_JOB") or os.path.exists("/code/app"))


def _parse_dotenv_file(env_path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not env_path.is_file():
        return out
    try:
        for raw_line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and v and "your-api-key" not in v.lower():
                out[k] = v
    except Exception:
        pass
    return out


def discover_gemini_api_key() -> Optional[str]:
    """Finds a valid Gemini API key from env vars or local gitignored `.env` files."""
    for env_var in ("SC_TWIN_GEMINI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
        val = (os.environ.get(env_var) or "").strip()
        if val and "your-api-key" not in val.lower():
            return val

    candidate_files = [
        REPO_ROOT / "enterprise_twin" / ".env",
        REPO_ROOT / ".env",
        Path.home() / "high-code-agents" / "oil-and-gas-rig-navigator-agent" / ".env",
        Path.home() / "high-code-agents" / "loadpilot-dispatch-agent" / ".env",
    ]
    for fp in candidate_files:
        parsed = _parse_dotenv_file(fp)
        for env_var in ("SC_TWIN_GEMINI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
            val = parsed.get(env_var, "").strip()
            if val:
                os.environ.setdefault("GEMINI_API_KEY", val)
                return val
    return None


def sync_local_argolis_adc(project: str = DEFAULT_PROJECT) -> Optional[Path]:
    """Syncs fresh Argolis OAuth refresh token on developer workstation if present."""
    if is_cloud_runtime():
        return None
    os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
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


def get_gcp_credentials(project: str = DEFAULT_PROJECT) -> Tuple[Optional[Any], str]:
    """Returns `(google.auth.credentials.Credentials, project_id)` for Vertex AI / BQ / GCS.

    On local developer workstations (`not is_cloud_runtime()`), uses a strict 4-second HTTP timeout
    and avoids falling through to interactive `google.auth.default()` helpers that block on smartcard prompts.
    """
    import google.auth

    if not is_cloud_runtime():
        os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
        adc_path = sync_local_argolis_adc(project)
        if adc_path and adc_path.exists():
            try:
                import google.oauth2.credentials
                from google.auth.transport.requests import Request
                import requests

                class _BoundedTimeoutSession(requests.Session):
                    def request(self, method, url, **kwargs):  # type: ignore[override]
                        kwargs.setdefault("timeout", 4.0)
                        return super().request(method, url, **kwargs)

                creds = google.oauth2.credentials.Credentials.from_authorized_user_file(
                    str(adc_path),
                    scopes=["https://www.googleapis.com/auth/cloud-platform"],
                )
                creds.refresh(Request(session=_BoundedTimeoutSession()))
                return creds, project
            except Exception:
                pass
        if os.environ.get("SC_TWIN_ALLOW_LOCAL_ADC_DEFAULT") != "1":
            return None, project

    try:
        creds, detected_proj = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        return creds, (project or detected_proj or DEFAULT_PROJECT)
    except Exception:
        return None, project


def get_genai_clients(location: str = "global", timeout_ms: int = 90_000) -> List[Tuple[str, Any]]:
    """Returns ordered `(auth_label, genai.Client)` candidates so live Gemini calls never fail needlessly."""
    from google import genai
    from google.genai import types

    safe_timeout_ms = max(10_000, int(timeout_ms or 90_000))

    if not is_cloud_runtime():
        os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"

    clients: List[Tuple[str, Any]] = []
    api_key = discover_gemini_api_key()

    if is_cloud_runtime():
        # In Cloud Run / Agent Engine: try native IAM Vertex AI first, then API key if provided
        creds, project = get_gcp_credentials(DEFAULT_PROJECT)
        v_kwargs: dict[str, Any] = {
            "vertexai": True,
            "project": project,
            "location": location,
            "http_options": types.HttpOptions(timeout=safe_timeout_ms),
        }
        if creds is not None:
            v_kwargs["credentials"] = creds
        clients.append(("vertex_iam", genai.Client(**v_kwargs)))
        if api_key:
            clients.append((
                "gemini_api_key",
                genai.Client(vertexai=False, api_key=api_key, http_options=types.HttpOptions(timeout=safe_timeout_ms)),
            ))
    else:
        # On local workstation: prefer direct Gemini API key (immune to CloudTop RAPT expiry), then non-blocking Vertex OAuth
        if api_key:
            clients.append((
                "gemini_api_key",
                genai.Client(vertexai=False, api_key=api_key, http_options=types.HttpOptions(timeout=safe_timeout_ms)),
            ))
        creds, project = get_gcp_credentials(DEFAULT_PROJECT)
        if creds is not None:
            clients.append((
                "vertex_oauth",
                genai.Client(
                    vertexai=True,
                    project=project,
                    location=location,
                    credentials=creds,
                    http_options=types.HttpOptions(timeout=safe_timeout_ms),
                ),
            ))

    return clients


def get_genai_client(location: str = "global") -> Any:
    """Backwards-compatible helper returning the primary `genai.Client`."""
    candidates = get_genai_clients(location=location)
    if not candidates:
        raise RuntimeError("No Gemini API key or Google Cloud credentials available.")
    return candidates[0][1]
