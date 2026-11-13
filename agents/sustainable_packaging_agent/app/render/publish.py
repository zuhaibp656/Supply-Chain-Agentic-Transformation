"""Publish media (interactive HTML cockpits, CSV exports) to GCS and return browser-openable URLs.

Follows the exact FleetFlow (`loadpilot-dispatch-agent`) architecture:
  1. V4 Signed URL (`https://storage.googleapis.com/<bucket>/<obj>?X-Goog-Algorithm=...`) with
     `response_type="text/html; charset=utf-8"` and `response_disposition="inline"` so clicking
     the link in any browser tab renders the full-screen interactive HTML web application directly
     (zero login walls, zero file-download attachment prompts).
  2. Authenticated `https://storage.cloud.google.com/<bucket>/<obj>` fallback when local credentials
     do not expose a service-account signing identity.
  3. Background thread publishing (`start_turn_publishing` + `wait_turn_publishing`) so URL signing
     returns immediately in `after_model_callback` while bytes finish uploading before `after_agent_callback` exits.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import logging
import os
import socket
import threading
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Prefer IPv4 to avoid IPv6 connect stalls in containerized/workstation environments
try:
    import urllib3.util.connection as _u3_conn
    _u3_conn.allowed_gai_family = lambda: socket.AF_INET
except Exception:
    pass

_gcs_auth_unavailable = False
_ACTIVE_THREADS: List[threading.Thread] = []
_SIGN_CACHE: Dict[str, Dict[str, str]] = {}


def media_bucket() -> str:
    return (
        os.environ.get("SC_MEDIA_BUCKET")
        or os.environ.get("FLEETFLOW_MEDIA_BUCKET")
        or os.environ.get("LOADPILOT_MEDIA_BUCKET")
        or f"{os.environ.get('GOOGLE_CLOUD_PROJECT', 'zuhaibp-ai')}-supply-chain-media"
    )


def upload_bytes(
    data: bytes,
    object_name: str,
    content_type: str,
    content_disposition: Optional[str] = None,
) -> bool:
    global _gcs_auth_unavailable
    if _gcs_auth_unavailable or os.environ.get("SC_SKIP_GCS_UPLOAD") == "1":
        return False
    try:
        from google.cloud import storage

        project = os.environ.get("GOOGLE_CLOUD_PROJECT") or "zuhaibp-ai"
        client = storage.Client(project=project)
        blob = client.bucket(media_bucket()).blob(object_name)
        blob.cache_control = "public, max-age=3600"
        if content_disposition:
            blob.content_disposition = content_disposition
        blob.upload_from_string(data, content_type=content_type)
        return True
    except Exception as exc:
        msg = str(exc)
        if "Reauthentication is needed" in msg or "DefaultCredentialsError" in msg:
            _gcs_auth_unavailable = True
        logger.warning("GCS upload failed for %s: %s", object_name, exc)
        return False


def _sign(
    bucket_name: str,
    object_name: str,
    response_type: Optional[str] = None,
    response_disposition: Optional[str] = None,
) -> Optional[str]:
    if os.environ.get("SC_SKIP_GCS_UPLOAD") == "1":
        return None
    cache_key = f"{bucket_name}/{object_name}|{response_type}|{response_disposition}"
    if cache_key in _SIGN_CACHE:
        return _SIGN_CACHE[cache_key].get("signed") or None
    try:
        import google.auth
        from google.auth.transport.requests import Request
        from google.cloud import storage

        creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        creds.refresh(Request())
        sa_email = getattr(creds, "service_account_email", None)
        if not sa_email or sa_email == "default":
            try:
                import urllib.request

                req = urllib.request.Request(
                    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email",
                    headers={"Metadata-Flavor": "Google"},
                )
                with urllib.request.urlopen(req, timeout=2) as r:
                    sa_email = r.read().decode("utf-8").strip()
            except Exception:
                sa_email = None

        blob = storage.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT") or "zuhaibp-ai").bucket(bucket_name).blob(object_name)
        sign_kwargs = {
            "version": "v4",
            "expiration": dt.timedelta(days=7),
            "method": "GET",
        }
        if response_type:
            sign_kwargs["response_type"] = response_type
        if response_disposition:
            sign_kwargs["response_disposition"] = response_disposition

        if hasattr(creds, "sign_bytes") and not sa_email:
            url = blob.generate_signed_url(credentials=creds, **sign_kwargs)
        elif sa_email:
            url = blob.generate_signed_url(
                service_account_email=sa_email,
                access_token=creds.token,
                **sign_kwargs,
            )
        else:
            return None
        _SIGN_CACHE[cache_key] = {"signed": url}
        return url
    except Exception as exc:
        logger.info("V4 signed URL unavailable (%s); falling back to authenticated URL", exc)
        return None


def links_for(
    object_name: str,
    response_type: Optional[str] = None,
    response_disposition: Optional[str] = None,
) -> Dict[str, str]:
    bucket_name = media_bucket()
    signed = _sign(bucket_name, object_name, response_type=response_type, response_disposition=response_disposition) or ""
    auth = f"https://storage.cloud.google.com/{bucket_name}/{object_name}"
    return {"signed": signed, "auth": auth, "best": signed or auth}


def publish_bytes(
    data: bytes,
    object_name: str,
    content_type: str,
    content_disposition: Optional[str] = None,
) -> Dict[str, str]:
    upload_bytes(data, object_name, content_type, content_disposition=content_disposition)
    return links_for(object_name, response_type=content_type, response_disposition=content_disposition)


def publish_interactive_html(html_markup: str, agent_id: str, title: str = "") -> Dict[str, str]:
    digest = hashlib.sha1(html_markup.encode("utf-8")).hexdigest()[:10]
    obj_name = f"cockpits/{agent_id}_{digest}.html"
    ctype = "text/html; charset=utf-8"
    links = links_for(obj_name, response_type=ctype, response_disposition="inline")
    if os.environ.get("SC_SKIP_GCS_UPLOAD") != "1":
        def _bg() -> None:
            upload_bytes(html_markup.encode("utf-8"), obj_name, ctype, content_disposition="inline")
        t = threading.Thread(target=_bg, name=f"gcs-html-{agent_id}", daemon=True)
        t.start()
        _ACTIVE_THREADS.append(t)
    return {"object_name": obj_name, "url": links["best"], "auth_url": links["auth"], "signed_url": links["signed"]}


def publish_csv_export(csv_text: str, agent_id: str) -> Dict[str, str]:
    digest = hashlib.sha1(csv_text.encode("utf-8")).hexdigest()[:10]
    obj_name = f"exports/{agent_id}_{digest}.csv"
    ctype = "text/csv; charset=utf-8"
    disp = f'attachment; filename="{agent_id}_verified_schedule.csv"'
    links = links_for(obj_name, response_type=ctype, response_disposition=disp)
    if os.environ.get("SC_SKIP_GCS_UPLOAD") != "1":
        def _bg() -> None:
            upload_bytes(csv_text.encode("utf-8"), obj_name, ctype, content_disposition=disp)
        t = threading.Thread(target=_bg, name=f"gcs-csv-{agent_id}", daemon=True)
        t.start()
        _ACTIVE_THREADS.append(t)
    return {"object_name": obj_name, "url": links["best"], "auth_url": links["auth"], "signed_url": links["signed"]}


def wait_for_uploads(timeout: float = 12.0) -> None:
    global _ACTIVE_THREADS
    pending = list(_ACTIVE_THREADS)
    _ACTIVE_THREADS = []
    for t in pending:
        if t.is_alive():
            t.join(timeout=timeout)
