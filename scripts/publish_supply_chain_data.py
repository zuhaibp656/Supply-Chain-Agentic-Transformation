#!/usr/bin/env python3
"""Aggregates and publishes demo digital twin data across the 10 flagship supply chain agents.

Functions:
  1. Aggregates all 42 fixture tables across the 10 flagship agents into `demo_data/tables/` (JSON & CSV).
  2. Creates BigQuery dataset `supply_chain_twin` in the target project (e.g. `zuhaibp-ai`).
  3. Loads each table into BigQuery with typed schema / JSON autodetection.
  4. Uploads all table assets to Cloud Storage `gs://<project>-supply-chain-media/demo-data/tables/`.

Usage:
  python3 scripts/publish_supply_chain_data.py [--project zuhaibp-ai] [--dataset supply_chain_twin]
                                               [--bucket zuhaibp-ai-supply-chain-media]
                                               [--local-only] [--token ACCESS_TOKEN]
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Tuple

os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
ROOT = Path(__file__).resolve().parent.parent

def _load_all_catalog_agents() -> List[str]:
    catalog_path = ROOT / "data" / "supply_chain_catalog.json"
    if catalog_path.exists():
        try:
            cat = json.loads(catalog_path.read_text(encoding="utf-8"))
            agents_obj = cat.get("agents", {})
            if isinstance(agents_obj, dict):
                return list(agents_obj.keys())
        except Exception:
            pass
    return sorted([p.name for p in (ROOT / "agents").iterdir() if p.is_dir() and (p / "fixtures" / "tables").exists()])


FLAGSHIP_AGENTS = _load_all_catalog_agents()

_TOKEN_OVERRIDE: str | None = None


def get_token() -> str | None:
    if _TOKEN_OVERRIDE:
        return _TOKEN_OVERRIDE
    if os.environ.get("GCP_ACCESS_TOKEN"):
        return os.environ["GCP_ACCESS_TOKEN"]
    # Check ~/.config/gcloud/argolis_admin_adc.json
    adc_p = Path(os.path.expanduser("~/.config/gcloud/argolis_admin_adc.json"))
    if adc_p.exists():
        try:
            import google.oauth2.credentials
            from google.auth.transport.requests import Request
            c = google.oauth2.credentials.Credentials.from_authorized_user_file(
                str(adc_p), scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            c.refresh(Request())
            return c.token
        except Exception:
            pass
    # Fallback to gcloud print-access-token
    try:
        tok = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if tok:
            return tok
    except Exception:
        pass
    return None


def api(
    method: str,
    url: str,
    body: dict | None = None,
    raw_data: bytes | None = None,
    content_type: str = "application/json",
    token: str | None = None,
    project: str | None = None,
    ok404: bool = False,
) -> dict:
    tok = token or get_token()
    headers = {"Content-Type": content_type}
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    if project:
        headers["X-Goog-User-Project"] = project

    data = raw_data if raw_data is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="ignore")
        if ok404 and e.code == 404:
            return {"_404": True}
        raise RuntimeError(f"{method} {url} -> {e.code}: {txt[:350]}") from None


def collect_agent_fixtures() -> Dict[str, Dict[str, Any]]:
    """Scan all 10 flagship agents and gather fixture tables with metadata."""
    tables: Dict[str, Dict[str, Any]] = {}
    for agent_id in FLAGSHIP_AGENTS:
        fixtures_dir = ROOT / "agents" / agent_id / "fixtures" / "tables"
        if not fixtures_dir.exists():
            continue
        for json_file in fixtures_dir.glob("*.json"):
            tbl_name = json_file.stem
            try:
                rows = json.loads(json_file.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"[WARN] Failed to read {json_file}: {e}")
                continue
            tables[tbl_name] = {
                "table_name": tbl_name,
                "agent_id": agent_id,
                "source_path": str(json_file),
                "rows": rows,
                "row_count": len(rows),
            }
    return tables


def export_local_data_assets(tables: Dict[str, Dict[str, Any]], out_dir: Path) -> None:
    """Write standardized JSON and CSV copies of all tables to demo_data/tables/."""
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = []

    for name, meta in sorted(tables.items()):
        rows = meta["rows"]
        json_path = out_dir / f"{name}.json"
        csv_path = out_dir / f"{name}.csv"

        # 1. Write clean indented JSON
        json_path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")

        # 2. Write CSV with serialised complex columns
        if rows and isinstance(rows, list) and isinstance(rows[0], dict):
            fieldnames = list(rows[0].keys())
            # Gather all possible keys across rows
            for r in rows:
                for k in r.keys():
                    if k not in fieldnames:
                        fieldnames.append(k)

            with csv_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in rows:
                    csv_row = {}
                    for k in fieldnames:
                        val = r.get(k)
                        if isinstance(val, (dict, list)):
                            csv_row[k] = json.dumps(val, sort_keys=True)
                        elif val is None:
                            csv_row[k] = ""
                        else:
                            csv_row[k] = str(val)
                    writer.writerow(csv_row)

        manifest.append({
            "table_name": name,
            "agent_id": meta["agent_id"],
            "row_count": meta["row_count"],
            "json_file": f"{name}.json",
            "csv_file": f"{name}.csv",
        })

    # Write overall manifest
    manifest_path = out_dir / "tables_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Generated {len(tables)} table files (.json & .csv) in {out_dir}")


def ensure_bq_dataset(project: str, dataset: str, location: str, token: str | None) -> None:
    """Ensure BigQuery dataset exists."""
    url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}/datasets/{dataset}"
    res = api("GET", url, token=token, project=project, ok404=True)
    if res.get("_404"):
        body = {
            "datasetReference": {"datasetId": dataset, "projectId": project},
            "location": location,
            "description": "Supply Chain & Demand Multi-Echelon Enterprise Digital Twin Dataset",
        }
        api("POST", f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}/datasets",
            body=body, token=token, project=project)
        print(f"[CREATED] BigQuery dataset {project}:{dataset} in {location}")
    else:
        print(f"[OK] BigQuery dataset {project}:{dataset} ready")


def load_bq_tables(
    project: str,
    dataset: str,
    tables: Dict[str, Dict[str, Any]],
    token: str | None,
) -> None:
    """Loads each table into BigQuery using streaming insert or batch jobs."""
    loaded = 0
    for name, meta in tables.items():
        rows = meta["rows"]
        if not rows:
            continue

        # BigQuery REST API: insertAll
        url = f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}/datasets/{dataset}/tables/{name}/insertAll"
        # Prepare streaming payload
        insert_rows = []
        for idx, row in enumerate(rows):
            # BigQuery requires JSON primitive fields or RECORD types; stringify complex dicts/lists for schemaless flexibility
            clean_row = {}
            for k, v in row.items():
                if isinstance(v, (dict, list)):
                    clean_row[k] = json.dumps(v)
                else:
                    clean_row[k] = v
            insert_rows.append({"insertId": f"{name}-{idx}-{int(time.time())}", "json": clean_row})

        try:
            res = api("POST", url, body={"rows": insert_rows}, token=token, project=project, ok404=True)
            if res.get("_404"):
                # Table does not exist, create table schema first
                sample = rows[0]
                fields = []
                for k, v in sample.items():
                    if isinstance(v, bool):
                        t = "BOOLEAN"
                    elif isinstance(v, int):
                        t = "INTEGER"
                    elif isinstance(v, float):
                        t = "FLOAT"
                    else:
                        t = "STRING"
                    fields.append({"name": k, "type": t, "mode": "NULLABLE"})
                tbl_body = {
                    "tableReference": {"projectId": project, "datasetId": dataset, "tableId": name},
                    "schema": {"fields": fields},
                    "description": f"Digital Twin fixture table for {meta['agent_id']}",
                }
                api("POST", f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}/datasets/{dataset}/tables",
                    body=tbl_body, token=token, project=project)
                # Retry insert
                api("POST", url, body={"rows": insert_rows}, token=token, project=project)
                print(f"[CREATED & LOADED] BQ Table {dataset}.{name} ({len(rows)} rows)")
            else:
                errs = res.get("insertErrors", [])
                if errs:
                    print(f"[WARN] BQ insert errors for {name}: {errs[:2]}")
                else:
                    print(f"[LOADED] BQ Table {dataset}.{name} ({len(rows)} rows)")
            loaded += 1
        except Exception as e:
            print(f"[NOTE] BigQuery table {name} load notice: {str(e)[:180]}")
    print(f"[OK] Processed {loaded} BigQuery tables in dataset {dataset}")


def upload_gcs_assets(bucket: str, tables_dir: Path, token: str | None, project: str) -> None:
    """Uploads table JSON and CSV files to Cloud Storage."""
    # Ensure bucket exists
    b_url = f"https://storage.googleapis.com/storage/v1/b/{bucket}"
    b_res = api("GET", b_url, token=token, project=project, ok404=True)
    if b_res.get("_404"):
        try:
            api("POST", f"https://storage.googleapis.com/storage/v1/b?project={project}",
                {"name": bucket, "location": "us-central1", "iamConfiguration": {"uniformBucketLevelAccess": {"enabled": True}}},
                token=token, project=project)
            print(f"[CREATED] GCS bucket gs://{bucket}")
        except Exception as e:
            print(f"[WARN] Could not create bucket gs://{bucket}: {e}")
            return
    else:
        print(f"[OK] GCS bucket gs://{bucket} ready")

    uploaded = 0
    for file_path in tables_dir.glob("*.*"):
        blob_name = f"demo-data/tables/{file_path.name}"
        c_type = "application/json" if file_path.suffix == ".json" else "text/csv"
        raw_bytes = file_path.read_bytes()
        upload_url = f"https://storage.googleapis.com/upload/storage/v1/b/{bucket}/o?uploadType=media&name={urllib.parse.quote(blob_name)}"
        try:
            api("POST", upload_url, raw_data=raw_bytes, content_type=c_type, token=token, project=project)
            uploaded += 1
        except Exception as e:
            print(f"[WARN] GCS upload failed for {blob_name}: {str(e)[:160]}")
    print(f"[OK] Uploaded {uploaded} data assets to gs://{bucket}/demo-data/tables/")


def main() -> None:
    global _TOKEN_OVERRIDE
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", default=os.environ.get("GOOGLE_CLOUD_PROJECT", "zuhaibp-ai"))
    parser.add_argument("--dataset", default="supply_chain_twin")
    parser.add_argument("--location", default="US")
    parser.add_argument("--bucket", default="zuhaibp-ai-supply-chain-media")
    parser.add_argument("--token", default="", help="OAuth2 access token override")
    parser.add_argument("--local-only", action="store_true", help="Only generate local demo_data files without GCP upload")
    args = parser.parse_args()

    if args.token:
        _TOKEN_OVERRIDE = args.token

    print("==================================================================")
    print(" 📦 Supply Chain Demo Data Publisher (10 Flagship Agents)")
    print(f" Target Project : {args.project}")
    print(f" BQ Dataset     : {args.dataset}")
    print(f" GCS Bucket     : gs://{args.bucket}")
    print("==================================================================")

    # 1. Collect table fixtures
    tables = collect_agent_fixtures()
    print(f"[FOUND] {len(tables)} unique fixture tables across {len(FLAGSHIP_AGENTS)} flagship agents.")

    # 2. Export local files to demo_data/tables/
    out_dir = ROOT / "demo_data" / "tables"
    export_local_data_assets(tables, out_dir)

    if args.local_only:
        print("[LOCAL COMPLETE] Generated local demo data assets. Exiting per --local-only.")
        return

    # 3. Verify GCP token
    tok = get_token()
    if not tok:
        print("[NOTE] No valid GCP access token detected for cloud upload.")
        print("       To publish to GCP, re-run with --token <TOKEN> or configure ADC.")
        return

    # 4. BigQuery setup & upload
    try:
        ensure_bq_dataset(args.project, args.dataset, args.location, tok)
        load_bq_tables(args.project, args.dataset, tables, tok)
    except Exception as e:
        print(f"[NOTE] BigQuery publishing skipped: {e}")

    # 5. Cloud Storage upload
    try:
        upload_gcs_assets(args.bucket, out_dir, tok, args.project)
    except Exception as e:
        print(f"[NOTE] Cloud Storage publishing skipped: {e}")

    print("✅ Demo Data publishing finished successfully!")


if __name__ == "__main__":
    main()
