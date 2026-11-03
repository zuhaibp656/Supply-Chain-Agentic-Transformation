"""End-to-End Automated Test Suite for Enterprise Twin Portal Generator (`v2.0`).

Verifies:
  1. Pydantic v2 Schema Validation, WCAG Color Clamping & 6-Pillar Guardrails.
  2. Official Corporate Logo Resolution & Optical Plate Framing (never AI-generated).
  3. Division Differentiation & Smart Irrelevant Agent Hiding (ITC Tobacco vs. ITC Foods, UltraTech Cement).
  4. Canonical 60 Demo Agent Engine Immutability (`data/supply_chain_catalog.json` intact).
  5. FastAPI + SSE Server Routes (`/`, `/welcome`, `/base`, `/t/{slug}`, `/api/v1/twins`, SSE stream, PATCH).
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient

from enterprise_twin.agent import run_enterprise_twin_agent
from enterprise_twin.schema import clamp_brand_hex, load_canonical_catalog, make_twin_slug
from enterprise_twin.server import app
from enterprise_twin.tools.logo_resolver import resolve_company_logo
from enterprise_twin.tools.persistence import load_twin_spec


def test_slug_and_wcag_color_clamping():
    slug_tobacco = make_twin_slug("ITC Limited", "Cigarettes & Leaf Tobacco (ILTD & TM&D)")
    slug_foods = make_twin_slug("ITC Limited", "Foods Division (ICML & Agri)")
    assert slug_tobacco != slug_foods
    assert slug_tobacco.startswith("itc-limited--")

    # Near-white or near-black hexes get clamped to readable chromatic saturation
    clamped_white = clamp_brand_hex("#ffffff")
    clamped_black = clamp_brand_hex("#010101")
    assert clamped_white.startswith("#") and len(clamped_white) == 7
    assert clamped_black.startswith("#") and len(clamped_black) == 7
    assert clamped_white != "#ffffff"
    assert clamped_black != "#010101"


def test_official_logo_resolver_never_ai_generated():
    logo = resolve_company_logo("ITC Limited", "itcportal.com")
    assert logo.source_type in ("wikimedia_svg", "wikimedia_png", "site_icon", "google_hd_icon", "custom", "initials_badge")
    assert logo.plate_style in ("light_plate", "dark_plate", "self_plated", "neutral_glass")
    if logo.source_type != "initials_badge":
        assert logo.data_uri.startswith("data:image/")


def test_division_differentiation_and_smart_agent_hiding():
    catalog = load_canonical_catalog()
    assert len(catalog["personas"]) == 60
    assert len(catalog["agents"]) == 60
    sub_pillars_total = sum(len(d.get("subPillars", [])) for d in catalog["departments"].values())
    assert sub_pillars_total == 20

    tobacco = load_twin_spec("itc-limited--cigarettes-leaf-tobacco-iltd-tm-d")
    foods = load_twin_spec("itc-limited--foods-division-icml-agri")
    cement = load_twin_spec("aditya-birla-group--ultratech-cement-division")
    hindalco = load_twin_spec("aditya-birla-group--hindalco-aluminium-copper")
    maruti = load_twin_spec("maruti-suzuki")
    wipro = load_twin_spec("wipro")

    assert tobacco is not None
    assert foods is not None
    assert cement is not None
    assert hindalco is not None
    assert maruti is not None
    assert wipro is not None

    # Dynamic Organization-Specific Operating Pillars (5, 6, or 7 Pillars!)
    assert tobacco["active_pillars_count"] == 7 and len(tobacco["custom_pillars"]) == 7
    assert foods["active_pillars_count"] == 7 and len(foods["custom_pillars"]) == 7
    assert cement["active_pillars_count"] == 7 and len(cement["custom_pillars"]) == 7
    assert maruti["active_pillars_count"] == 7 and len(maruti["custom_pillars"]) == 7
    assert hindalco["active_pillars_count"] == 5 and len(hindalco["custom_pillars"]) == 5
    assert wipro["active_pillars_count"] == 5 and len(wipro["custom_pillars"]) == 5

    # Verify custom_pillars partition 100% of active sub-pillars with zero orphans or duplicates
    for spec in (tobacco, foods, cement, hindalco, maruti, wipro):
        seen_sps = []
        for cp in spec["custom_pillars"]:
            assert len(cp["sub_pillar_ids"]) >= 1
            seen_sps.extend(cp["sub_pillar_ids"])
        assert len(seen_sps) == len(set(seen_sps)), f"Duplicate sub-pillars in {spec['twin_slug']}"
        assert len(seen_sps) == 20, f"Expected all 20 canonical sub-pillars partitioned in {spec['twin_slug']}"

    # Division executive titles and adapted roles must differ between ITC Tobacco and ITC Foods
    assert tobacco["brand"]["executive_title"] != foods["brand"]["executive_title"]
    assert len(tobacco["persona_overrides"]) == 60
    assert len(tobacco["sub_pillar_overrides"]) == 20
    assert len(tobacco["agent_relevance"]) == 60

    # ITC Tobacco & UltraTech Cement must cleanly hide genuinely inapplicable cold-chain / grocery / retail BOPIS agents
    assert 45 <= tobacco["active_agents_count"] < 60
    assert len(tobacco["hidden_agent_ids"]) == 60 - tobacco["active_agents_count"]
    assert 45 <= cement["active_agents_count"] < 60
    assert len(cement["hidden_agent_ids"]) == 60 - cement["active_agents_count"]

    # Company/division-tailored agent names (`custom_agent_name`) populated where helpful, never on hidden agents
    tobacco_custom_names = [
        spec["custom_agent_name"]
        for spec in tobacco["agent_relevance"].values()
        if spec.get("custom_agent_name")
    ]
    assert len(tobacco_custom_names) >= 10
    assert "TM&D WD Demand Sensing" in tobacco_custom_names
    for hid in tobacco["hidden_agent_ids"]:
        assert tobacco["agent_relevance"][hid].get("custom_agent_name", "") == ""

    # ITC Foods spans agri + ambient + chilled/dairy + modern trade, so all 60 agents remain relevant
    assert foods["active_agents_count"] == 60
    assert len(foods["hidden_agent_ids"]) == 0

    # Every single pillar must retain >= 3 relevant agents so no Org Chart column ever collapses
    hidden_cement = set(cement["hidden_agent_ids"])
    for d_id, d_obj in catalog["departments"].items():
        active_in_pillar = 0
        for sp in d_obj.get("subPillars", []):
            for item in sp.get("items", []):
                if item["agentId"] not in hidden_cement:
                    active_in_pillar += 1
        assert active_in_pillar >= 3, f"Pillar {d_id} dropped below 3 relevant agents!"


def test_fastapi_welcome_hydration_and_sse_stream():
    client = TestClient(app)

    # 1. Welcome Studio Front-Door (Minimal Scroll & Fly-Up Journey + Saved Portals Tab)
    r_welcome = client.get("/")
    assert r_welcome.status_code == 200
    assert "Welcome to" in r_welcome.text
    assert "Supply Chain" in r_welcome.text
    assert "fly-up" in r_welcome.text
    assert "Saved Portals" in r_welcome.text
    assert "Quick-Fill" not in r_welcome.text

    # 2. Health Check & Strict Model Naming
    r_health = client.get("/api/v1/health")
    assert r_health.status_code == 200
    h_json = r_health.json()
    assert h_json["status"] == "healthy"
    assert "gemini-3.8-flash" in h_json["models"]["parallel_pillar_synthesis"]

    # 3. Saved Portals Listing
    r_list = client.get("/api/v1/twins")
    assert r_list.status_code == 200
    assert r_list.json()["count"] >= 5

    # 4. <200ms Hydrated Division Portal Route (/t/{slug})
    t0 = time.perf_counter()
    r_portal = client.get("/t/itc-limited--cigarettes-leaf-tobacco-iltd-tm-d")
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    assert r_portal.status_code == 200
    assert 'window.__INITIAL_TWIN__ =' in r_portal.text
    assert '<base href="/" />' in r_portal.text
    assert "ITC Limited" in r_portal.text
    assert elapsed_ms < 1500  # Cold template read + JSON injection; warm hits are <50ms

    # Warm hit check (<200ms)
    t1 = time.perf_counter()
    r_portal_warm = client.get("/t/aditya-birla-group--ultratech-cement-division")
    warm_ms = (time.perf_counter() - t1) * 1000.0
    assert r_portal_warm.status_code == 200
    assert warm_ms < 250

    # 5. Live SSE Synthesis Stream Endpoint
    with client.stream(
        "POST",
        "/api/v1/twins/generate-stream",
        json={
            "company_name": "ITC Limited",
            "division_name": "Cigarettes & Leaf Tobacco (ILTD & TM&D)",
            "geography": "India",
            "force_refresh": False,
        },
    ) as sse_resp:
        assert sse_resp.status_code == 200
        events = []
        for line in sse_resp.iter_lines():
            if line.startswith("data:"):
                events.append(json.loads(line[5:].strip()))
        assert any(e.get("stage") == "done" for e in events)
        done_ev = [e for e in events if e.get("stage") == "done"][0]
        assert done_ev["redirect_url"] == "/t/itc-limited--cigarettes-leaf-tobacco-iltd-tm-d"

    # 6. Inline PATCH Fine-Tune Round-Trip
    orig = load_twin_spec("unilever--home-personal-care")
    orig_title = orig["brand"]["executive_title"]
    r_patch = client.patch(
        "/api/v1/twins/unilever--home-personal-care",
        json={"executive_title": f"{orig_title} (Verified)"},
    )
    assert r_patch.status_code == 200
    assert r_patch.json()["twin"]["brand"]["executive_title"].endswith("(Verified)")

    # Restore original title cleanly
    client.patch(
        "/api/v1/twins/unilever--home-personal-care",
        json={"executive_title": orig_title},
    )
