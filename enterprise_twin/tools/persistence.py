"""Twin Persistence & Memory Service.

Saves, loads, and indexes company digital twins in local JSON storage,
provides in-memory caching, and stages records for BigQuery and GCS memory persistence.
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

TWINS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "twins"
TWINS_DIR.mkdir(parents=True, exist_ok=True)
BIGQUERY_STAGING_FILE = TWINS_DIR / "bigquery_staging.jsonl"

_MEMORY_CACHE: Dict[str, Dict[str, Any]] = {}


def slugify(text: str) -> str:
    """Converts company name to a clean URL/file slug."""
    text = text.lower().strip()
    text = re.sub(r'[\s\.\,\-\_\&\']+', '_', text)
    return text.strip('_')


def save_twin(twin_data: Dict[str, Any]) -> Path:
    """Saves a generated enterprise twin to JSON file and staging ledger."""
    company_name = twin_data.get("company_name") or twin_data.get("canonicalName", "Enterprise")
    slug = slugify(company_name)
    twin_data["company_slug"] = slug
    twin_data["saved_at"] = datetime.now(timezone.utc).isoformat()
    twin_data["status"] = twin_data.get("status", "approved")

    # 1. Save to JSON file
    file_path = TWINS_DIR / f"{slug}.json"
    file_path.write_text(json.dumps(twin_data, indent=2), encoding="utf-8")

    # 2. Update In-Memory Cache
    _MEMORY_CACHE[slug] = twin_data

    # 3. Append to BigQuery / GCS staging JSONL
    bq_record = {
        "twin_id": f"twin_{slug}_{int(datetime.now(timezone.utc).timestamp())}",
        "company_name": company_name,
        "company_slug": slug,
        "industry_id": twin_data.get("industryId") or twin_data.get("industry", "general"),
        "executive_title": twin_data.get("executiveTitle", ""),
        "brand_accent": twin_data.get("brandAccent", "#00d2ff"),
        "personas_count": len(twin_data.get("personaOverrides", {})),
        "agents_count": len(twin_data.get("agentOverrides", {})),
        "personas_json": json.dumps(twin_data.get("personaOverrides", {})),
        "agents_json": json.dumps(twin_data.get("agentOverrides", {})),
        "created_at": twin_data["saved_at"],
        "status": twin_data["status"]
    }
    with open(BIGQUERY_STAGING_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(bq_record) + "\n")

    return file_path


def load_twin(slug_or_name: str) -> Optional[Dict[str, Any]]:
    """Loads a twin from memory cache or file storage."""
    slug = slugify(slug_or_name)
    if slug in _MEMORY_CACHE:
        return _MEMORY_CACHE[slug]

    file_path = TWINS_DIR / f"{slug}.json"
    if file_path.exists():
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            _MEMORY_CACHE[slug] = data
            return data
        except Exception as e:
            print(f"Warning: Failed to parse twin at {file_path}: {e}")
            return None
    return None


def list_saved_twins() -> List[Dict[str, Any]]:
    """Lists all saved twins from disk with metadata."""
    twins = []
    for p in sorted(TWINS_DIR.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            twins.append({
                "company_slug": data.get("company_slug", p.stem),
                "company_name": data.get("company_name") or data.get("canonicalName", p.stem),
                "industry": data.get("industryId") or data.get("industry", "general"),
                "executive_title": data.get("executiveTitle", ""),
                "brand_accent": data.get("brandAccent", "#00d2ff"),
                "saved_at": data.get("saved_at", ""),
                "file_path": str(p)
            })
        except Exception:
            continue
    return twins
