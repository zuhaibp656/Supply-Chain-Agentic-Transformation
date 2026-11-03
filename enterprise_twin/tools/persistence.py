"""Persistent Multi-Tier Enterprise Twin Database (In-Memory + Local Disk + GCS + BigQuery).

Every researched `(Company + Division)` portal overlay is persisted once across:
  1. In-memory process cache (`<1ms` hot lookup)
  2. Local JSON store (`data/twins/v2/<twin_slug>.json` — bundled in Git & Docker image)
  3. Google Cloud Storage (`gs://zuhaibp-ai-supply-chain-media/enterprise-twins/<twin_slug>.json`)
  4. Google BigQuery (`zuhaibp-ai.supply_chain_twin.enterprise_portals`)

This guarantees `<200ms` instant load on repeat visits, durable persistence across Cloud Run
scale-to-zero container restarts, and full queryable history in BigQuery.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
import threading
from typing import Any, Dict, List, Optional

from enterprise_twin.schema import TwinOverlaySpec, make_twin_slug, validate_and_normalize_overlay
from enterprise_twin.tools.gcp_auth import (
    DEFAULT_BQ_DATASET,
    DEFAULT_BQ_TABLE,
    DEFAULT_GCS_BUCKET,
    DEFAULT_PROJECT,
    get_gcp_credentials,
)

TWINS_ROOT = Path(__file__).resolve().parent.parent.parent / "data" / "twins"
TWINS_V2_DIR = TWINS_ROOT / "v2"
TWINS_V2_DIR.mkdir(parents=True, exist_ok=True)
BIGQUERY_STAGING_FILE = TWINS_ROOT / "bigquery_staging.jsonl"

_MEMORY_CACHE: Dict[str, Dict[str, Any]] = {}
_BQ_TABLE_READY = False
_LOCK = threading.Lock()


def slugify(company_name: str, division_name: Optional[str] = None) -> str:
    return make_twin_slug(company_name, division_name)


def _get_gcs_bucket():
    try:
        from google.cloud import storage

        creds, proj = get_gcp_credentials(DEFAULT_PROJECT)
        if creds is None:
            return None
        client = storage.Client(project=proj, credentials=creds)
        return client.bucket(DEFAULT_GCS_BUCKET)
    except Exception:
        return None


def _ensure_bigquery_table():
    global _BQ_TABLE_READY
    try:
        from google.cloud import bigquery

        creds, proj = get_gcp_credentials(DEFAULT_PROJECT)
        if creds is None:
            return None, ""
        client = bigquery.Client(project=proj, credentials=creds)
        ds_id = f"{proj}.{DEFAULT_BQ_DATASET}"
        tbl_id = f"{ds_id}.{DEFAULT_BQ_TABLE}"
        if not _BQ_TABLE_READY:
            ds = bigquery.Dataset(ds_id)
            ds.location = "US"
            client.create_dataset(ds, exists_ok=True)
            schema = [
                bigquery.SchemaField("twin_slug", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("company_name", "STRING"),
                bigquery.SchemaField("division_name", "STRING"),
                bigquery.SchemaField("display_label", "STRING"),
                bigquery.SchemaField("industry_sector", "STRING"),
                bigquery.SchemaField("geography", "STRING"),
                bigquery.SchemaField("brand_accent", "STRING"),
                bigquery.SchemaField("active_agents_count", "INTEGER"),
                bigquery.SchemaField("hidden_agents_count", "INTEGER"),
                bigquery.SchemaField("overlay_json", "STRING"),
                bigquery.SchemaField("updated_at", "TIMESTAMP"),
            ]
            tbl = bigquery.Table(tbl_id, schema=schema)
            client.create_table(tbl, exists_ok=True)
            _BQ_TABLE_READY = True
        return client, tbl_id
    except Exception:
        return None, ""


def _sync_to_cloud_async(payload: Dict[str, Any]) -> None:
    """Writes twin JSON to GCS (`enterprise-twins/<slug>.json`) and appends/upserts to BigQuery."""
    slug = payload["twin_slug"]
    raw_json = json.dumps(payload, ensure_ascii=False, indent=2)

    def _worker():
        # 1. Upload canonical JSON to GCS for durable fast key-value lookup across Cloud Run instances
        bucket = _get_gcs_bucket()
        if bucket is not None:
            try:
                blob = bucket.blob(f"enterprise-twins/{slug}.json")
                blob.cache_control = "no-cache"
                blob.upload_from_string(raw_json, content_type="application/json; charset=utf-8")
            except Exception as e:
                print(f"[Persistence] GCS upload warning for {slug}: {e}")

        # 2. Insert audit/snapshot row into BigQuery
        bq_client, tbl_id = _ensure_bigquery_table()
        if bq_client is not None and tbl_id:
            try:
                brand = payload.get("brand") or {}
                row = {
                    "twin_slug": slug,
                    "company_name": payload.get("canonical_name") or payload.get("company_name", ""),
                    "division_name": payload.get("division_name", ""),
                    "display_label": payload.get("display_label", ""),
                    "industry_sector": brand.get("industry_sector", ""),
                    "geography": brand.get("geography", ""),
                    "brand_accent": brand.get("brand_accent", "#38bdf8"),
                    "active_agents_count": int(payload.get("active_agents_count", 60)),
                    "hidden_agents_count": len(payload.get("hidden_agent_ids") or []),
                    "overlay_json": json.dumps(payload, ensure_ascii=False),
                    "updated_at": payload.get("updated_at") or datetime.now(timezone.utc).isoformat(),
                }
                bq_client.insert_rows_json(tbl_id, [row])
            except Exception as e:
                print(f"[Persistence] BigQuery insert warning for {slug}: {e}")

    t = threading.Thread(target=_worker, daemon=True)
    t.start()


def save_twin_spec(spec: TwinOverlaySpec, sync_cloud: bool = True) -> Dict[str, Any]:
    """Validates, normalizes, and persists a v2 `TwinOverlaySpec` locally and in GCP."""
    norm = validate_and_normalize_overlay(spec)
    now_iso = datetime.now(timezone.utc).isoformat()
    if not norm.created_at:
        norm.created_at = now_iso
    norm.updated_at = now_iso

    payload = norm.model_dump()
    slug = norm.twin_slug

    with _LOCK:
        _MEMORY_CACHE[slug] = payload
        out_path = TWINS_V2_DIR / f"{slug}.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        # Also append compact summary to local JSONL ledger
        try:
            with open(BIGQUERY_STAGING_FILE, "a", encoding="utf-8") as f:
                f.write(
                    json.dumps({
                        "twin_slug": slug,
                        "display_label": norm.display_label,
                        "industry_sector": norm.brand.industry_sector,
                        "active_agents_count": norm.active_agents_count,
                        "updated_at": now_iso,
                    })
                    + "\n"
                )
        except Exception:
            pass

    if sync_cloud:
        _sync_to_cloud_async(payload)

    return payload


_MEMORY_MTIME: Dict[str, float] = {}


def load_twin_spec(slug_or_company: str, division_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Loads a saved v2 twin from memory (mtime-checked) -> local v2 disk -> GCS bucket."""
    if "--" in (slug_or_company or "") and not division_name:
        slug = re.sub(r"[^a-z0-9\-]+", "", slug_or_company.lower().strip())
    else:
        slug = slugify(slug_or_company, division_name)

    local_file = TWINS_V2_DIR / f"{slug}.json"
    if local_file.exists():
        try:
            mtime = local_file.stat().st_mtime
            if slug in _MEMORY_CACHE and _MEMORY_MTIME.get(slug) == mtime:
                return _MEMORY_CACHE[slug]
            data = json.loads(local_file.read_text(encoding="utf-8"))
            _MEMORY_CACHE[slug] = data
            _MEMORY_MTIME[slug] = mtime
            return data
        except Exception:
            pass

    if slug in _MEMORY_CACHE:
        return _MEMORY_CACHE[slug]

    # Check GCS bucket (covers portals generated dynamically on previous Cloud Run instances!)
    bucket = _get_gcs_bucket()
    if bucket is not None:
        try:
            blob = bucket.blob(f"enterprise-twins/{slug}.json")
            if blob.exists():
                raw = blob.download_as_text(encoding="utf-8")
                data = json.loads(raw)
                _MEMORY_CACHE[slug] = data
                # Cache locally for sub-millisecond subsequent hits
                try:
                    local_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                except Exception:
                    pass
                return data
        except Exception:
            pass

    return None


def list_saved_twins(include_cloud: bool = True) -> List[Dict[str, Any]]:
    """Returns summary cards for all saved v2 Enterprise Portals (local + GCS)."""
    seen: Dict[str, Dict[str, Any]] = {}

    def _summarize(data: Dict[str, Any]) -> Dict[str, Any]:
        brand = data.get("brand") or {}
        logo = brand.get("logo") or {}
        slug = data.get("twin_slug", "")
        return {
            "twin_slug": slug,
            "company_name": data.get("canonical_name") or data.get("company_name", slug),
            "division_name": data.get("division_name", ""),
            "display_label": data.get("display_label") or data.get("canonical_name", slug),
            "industry_sector": brand.get("industry_sector", "Supply Chain"),
            "geography": brand.get("geography", "Global"),
            "executive_title": brand.get("executive_title", ""),
            "executive_thesis": brand.get("executive_thesis", ""),
            "brand_accent": brand.get("brand_accent", "#38bdf8"),
            "logo_data_uri": logo.get("data_uri", ""),
            "logo_plate_style": logo.get("plate_style", "light_plate"),
            "logo_monogram": logo.get("monogram", "SC"),
            "active_agents_count": data.get("active_agents_count", 60),
            "hidden_agents_count": len(data.get("hidden_agent_ids") or []),
            "active_sub_pillars_count": data.get("active_sub_pillars_count", 20),
            "terminology_highlights": (data.get("terminology_highlights") or [])[:4],
            "career_title_examples": (data.get("career_title_examples") or [])[:4],
            "updated_at": data.get("updated_at", ""),
        }

    for p in sorted(TWINS_V2_DIR.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if d.get("schema_version") == "2.0" and d.get("twin_slug"):
                seen[d["twin_slug"]] = _summarize(d)
        except Exception:
            continue

    if include_cloud:
        bucket = _get_gcs_bucket()
        if bucket is not None:
            try:
                for blob in bucket.list_blobs(prefix="enterprise-twins/"):
                    if not blob.name.endswith(".json"):
                        continue
                    slug = Path(blob.name).stem
                    if slug in seen:
                        continue
                    raw = blob.download_as_text(encoding="utf-8")
                    d = json.loads(raw)
                    if d.get("schema_version") == "2.0" and d.get("twin_slug"):
                        seen[d["twin_slug"]] = _summarize(d)
                        # Hydrate local disk cache
                        try:
                            (TWINS_V2_DIR / f"{slug}.json").write_text(raw, encoding="utf-8")
                        except Exception:
                            pass
            except Exception:
                pass

    items = list(seen.values())
    items.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return items


# Backward-compatible aliases for legacy callers
def save_twin(twin_data: Dict[str, Any]) -> Path:
    if isinstance(twin_data, TwinOverlaySpec):
        payload = save_twin_spec(twin_data)
        return TWINS_V2_DIR / f"{payload['twin_slug']}.json"
    slug = twin_data.get("twin_slug") or slugify(twin_data.get("company_name") or twin_data.get("canonicalName", "enterprise"))
    p = TWINS_V2_DIR / f"{slug}.json"
    p.write_text(json.dumps(twin_data, indent=2), encoding="utf-8")
    return p


def load_twin(slug_or_name: str, division_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    return load_twin_spec(slug_or_name, division_name)
