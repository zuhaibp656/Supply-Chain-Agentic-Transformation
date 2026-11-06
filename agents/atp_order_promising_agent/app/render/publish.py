"""Publish media (interactive HTML dashboards, CSV exports) to GCS and return browser-openable URLs.

Pattern matches FleetFlow (LoadPilot):
  1. Authenticated Google Cloud Storage URL: https://storage.cloud.google.com/<bucket>/<object_name>
  2. V4 signed URL when service account credentials with signing capability are present.
"""
from __future__ import annotations

import datetime as dt
import logging
import os
import uuid

logger = logging.getLogger(__name__)

def media_bucket() -> str:
    return (
        os.environ.get("SC_MEDIA_BUCKET")
        or os.environ.get("FLEETFLOW_MEDIA_BUCKET")
        or os.environ.get("LOADPILOT_MEDIA_BUCKET")
        or f"{os.environ.get('GOOGLE_CLOUD_PROJECT', 'zuhaibp-ai')}-supply-chain-media"
    )

def upload_bytes(data: bytes, object_name: str, content_type: str) -> bool:
    try:
        from google.cloud import storage
        client = storage.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai"))
        blob = client.bucket(media_bucket()).blob(object_name)
        blob.cache_control = "private, max-age=3600"
        blob.upload_from_string(data, content_type=content_type)
        return True
    except Exception as exc:
        logger.warning("GCS upload failed for %s: %s", object_name, exc)
        return False

def links_for(object_name: str) -> dict[str, str]:
    bucket_name = media_bucket()
    signed = _sign(bucket_name, object_name) or ""
    auth = f"https://storage.cloud.google.com/{bucket_name}/{object_name}"
    return {"signed": signed, "auth": auth}

def _sign(bucket_name: str, object_name: str) -> str | None:
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
                    headers={"Metadata-Flavor": "Google"}
                )
                with urllib.request.urlopen(req, timeout=2) as r:
                    sa_email = r.read().decode().strip()
            except Exception:
                sa_email = None
        blob = storage.Client().bucket(bucket_name).blob(object_name)
        if hasattr(creds, "sign_bytes") and not sa_email:
            return blob.generate_signed_url(version="v4", expiration=dt.timedelta(days=7), method="GET", credentials=creds)
        if not sa_email:
            return None
        return blob.generate_signed_url(version="v4", expiration=dt.timedelta(days=7), method="GET",
                                        service_account_email=sa_email, access_token=creds.token)
    except Exception as exc:
        logger.info("signed URL unavailable (%s); using authenticated URL", exc)
        return None

def publish_bytes(data: bytes, object_name: str, content_type: str) -> dict[str, str]:
    upload_bytes(data, object_name, content_type)
    return links_for(object_name)

def publish_interactive_html(html_markup: str, agent_id: str, title: str = "") -> dict[str, str]:
    obj_name = f"cockpits/{agent_id}_{uuid.uuid4().hex[:8]}.html"
    links = publish_bytes(html_markup.encode("utf-8"), obj_name, "text/html")
    url = links.get("signed") or links.get("auth") or f"https://storage.cloud.google.com/{media_bucket()}/{obj_name}"
    return {"object_name": obj_name, "url": url}

def publish_csv_export(csv_text: str, agent_id: str) -> dict[str, str]:
    obj_name = f"exports/{agent_id}_{uuid.uuid4().hex[:8]}.csv"
    links = publish_bytes(csv_text.encode("utf-8"), obj_name, "text/csv")
    url = links.get("signed") or links.get("auth") or f"https://storage.cloud.google.com/{media_bucket()}/{obj_name}"
    return {"object_name": obj_name, "url": url}
