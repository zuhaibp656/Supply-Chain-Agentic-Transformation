"""Enterprise Twin Studio — FastAPI + SSE Portal Server (`v2.0`).

Serves:
  1. `GET /` & `GET /welcome` -> `"Welcome to Supply Chain"` Enterprise Portal Studio (`welcome.html`).
  2. `GET /t/{twin_slug}` -> Hydrates `index.html` in `<200ms` from the persistent database
     with `<base href="/" />`, dynamic `<title>`, and `window.__INITIAL_TWIN__`.
  3. `GET /base` & `GET /index.html` -> Industry-agnostic base Supply Chain Portal (all 60 agents).
  4. `POST /api/v1/twins/generate-stream` -> Live Server-Sent Events (`text/event-stream`) streaming
     real-time 4-stage ADK research, logo optical framing, career job-title grounding, and agent filtering.
  5. `POST /api/v1/generate-twin`, `GET /api/v1/twins`, `GET /api/v1/twins/{twin_slug}`,
     `PATCH /api/v1/twins/{twin_slug}`, and `GET /api/v1/health`.

Cloud Run ready (`uvicorn enterprise_twin.server:app --host 0.0.0.0 --port ${PORT:-8080}`).
"""

from __future__ import annotations

import argparse
import asyncio
import html
import json
import os
from pathlib import Path
import sys
import threading
from typing import Any, AsyncGenerator, Dict, Optional, Tuple

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from enterprise_twin.agent import run_enterprise_twin_agent
from enterprise_twin.schema import TwinOverlaySpec, validate_and_normalize_overlay
from enterprise_twin.tools.logo_resolver import resolve_company_logo
from enterprise_twin.tools.persistence import list_saved_twins, load_twin_spec, save_twin_spec

WELCOME_HTML_PATH = CURRENT_DIR / "web" / "welcome.html"
PORTAL_HTML_FILES = {
    "index.html": PROJECT_ROOT / "index.html",
    "periodic_table.html": PROJECT_ROOT / "periodic_table.html",
    "mind_map.html": PROJECT_ROOT / "mind_map.html",
    "cost_analysis_presentation.html": PROJECT_ROOT / "cost_analysis_presentation.html",
    "agent_testing_and_video_playbook.html": PROJECT_ROOT / "agent_testing_and_video_playbook.html",
    "supply_chain_101_interactive_academy.html": PROJECT_ROOT / "supply_chain_101_interactive_academy.html",
}

# Cache canonical HTML strings in memory for sub-millisecond hydration
_HTML_TEMPLATE_CACHE: Dict[str, Tuple[float, str]] = {}


def _read_cached_html(path: Path) -> str:
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Portal file not found: {path.name}")
    mtime = path.stat().st_mtime
    key = str(path)
    cached = _HTML_TEMPLATE_CACHE.get(key)
    if cached and cached[0] == mtime:
        return cached[1]
    text = path.read_text(encoding="utf-8")
    _HTML_TEMPLATE_CACHE[key] = (mtime, text)
    return text


def _safe_json_for_script(obj: Any) -> str:
    """Serializes JSON safely for embedding inside an HTML `<script>` block."""
    raw = json.dumps(obj, ensure_ascii=False)
    return raw.replace("</", "<\\/")


def _hydrate_portal_html(
    html_filename: str,
    twin_spec: Optional[Dict[str, Any]] = None,
    inject_base_href: bool = False,
) -> str:
    path = PORTAL_HTML_FILES[html_filename]
    doc = _read_cached_html(path)

    scripts = ["window.__ENTERPRISE_STUDIO_SERVER__ = true;"]
    if twin_spec:
        scripts.append(f"window.__INITIAL_TWIN__ = {_safe_json_for_script(twin_spec)};")

    head_injection = ""
    if inject_base_href:
        head_injection += '\n  <base href="/" />'
    head_injection += f"\n  <script>{' '.join(scripts)}</script>\n"

    if twin_spec and twin_spec.get("display_label"):
        safe_title = html.escape(f"{twin_spec['display_label']} — Supply Chain Agentic Transformation")
        t_start = doc.find("<title>")
        t_end = doc.find("</title>")
        if t_start != -1 and t_end != -1 and t_end > t_start:
            doc = doc[: t_start + 7] + safe_title + doc[t_end:]

    head_pos = doc.find("<head>")
    if head_pos != -1:
        insert_at = head_pos + len("<head>")
        return doc[:insert_at] + head_injection + doc[insert_at:]
    return head_injection + doc


class GenerateTwinRequest(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=140)
    division_name: str = Field(default="", max_length=160)
    geography: str = Field(default="Global", max_length=80)
    industry: Optional[str] = Field(default=None)
    focus: str = Field(default="", max_length=2000)
    custom_logo_input: str = Field(default="")
    force_refresh: bool = Field(default=False)


class PatchTwinRequest(BaseModel):
    executive_title: Optional[str] = None
    executive_thesis: Optional[str] = None
    flagship_sites: Optional[str] = None
    custom_logo_input: Optional[str] = None
    persona_overrides: Optional[Dict[str, Dict[str, Any]]] = None
    agent_relevance: Optional[Dict[str, Dict[str, Any]]] = None


app = FastAPI(
    title="Supply Chain Enterprise Twin Studio",
    version="2.0.0",
    description="Google ADK + Gemini 3.1 Pro / Gemini 3.8 Flash Enterprise Portal Generator & Persistent Twin Server",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

if (PROJECT_ROOT / "videos").exists():
    app.mount("/videos", StaticFiles(directory=str(PROJECT_ROOT / "videos")), name="videos")

if (PROJECT_ROOT / "data" / "twins" / "logos").exists():
    app.mount(
        "/assets/logos",
        StaticFiles(directory=str(PROJECT_ROOT / "data" / "twins" / "logos")),
        name="twin_logos",
    )


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
@app.api_route("/welcome", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def serve_welcome_studio() -> HTMLResponse:
    return HTMLResponse(content=_read_cached_html(WELCOME_HTML_PATH))


@app.api_route("/base", methods=["GET", "HEAD"], response_class=HTMLResponse)
@app.api_route("/index.html", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def serve_base_or_query_portal(twin: Optional[str] = Query(default=None)) -> HTMLResponse:
    spec = None
    if twin and twin not in ("base", "reset"):
        spec = load_twin_spec(twin)
    return HTMLResponse(content=_hydrate_portal_html("index.html", twin_spec=spec, inject_base_href=False))


@app.api_route("/t/{twin_slug}", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def serve_tailored_company_portal(twin_slug: str) -> HTMLResponse:
    spec = load_twin_spec(twin_slug)
    if not spec:
        # Auto-synthesize on the fly if someone visits a shared URL slug not yet in local cache
        parts = twin_slug.split("--", 1)
        co_guess = parts[0].replace("-", " ").title()
        div_guess = parts[1].replace("-", " ").title() if len(parts) > 1 else ""
        res = await asyncio.to_thread(
            run_enterprise_twin_agent,
            company_name=co_guess,
            division_name=div_guess,
        )
        spec = res["overlay"]
    return HTMLResponse(content=_hydrate_portal_html("index.html", twin_spec=spec, inject_base_href=True))


@app.api_route("/periodic_table.html", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def serve_periodic_table(twin: Optional[str] = Query(default=None)) -> HTMLResponse:
    spec = load_twin_spec(twin) if twin and twin not in ("base", "reset") else None
    return HTMLResponse(content=_hydrate_portal_html("periodic_table.html", twin_spec=spec))


@app.api_route("/mind_map.html", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def serve_mind_map(twin: Optional[str] = Query(default=None)) -> HTMLResponse:
    spec = load_twin_spec(twin) if twin and twin not in ("base", "reset") else None
    return HTMLResponse(content=_hydrate_portal_html("mind_map.html", twin_spec=spec))


@app.api_route("/cost_analysis_presentation.html", methods=["GET", "HEAD"])
async def serve_cost_deck() -> FileResponse:
    return FileResponse(str(PORTAL_HTML_FILES["cost_analysis_presentation.html"]))


@app.api_route("/agent_testing_and_video_playbook.html", methods=["GET", "HEAD"])
async def serve_playbook() -> FileResponse:
    return FileResponse(str(PORTAL_HTML_FILES["agent_testing_and_video_playbook.html"]))


@app.api_route("/supply_chain_101_interactive_academy.html", methods=["GET", "HEAD"])
async def serve_academy() -> FileResponse:
    return FileResponse(str(PORTAL_HTML_FILES["supply_chain_101_interactive_academy.html"]))


@app.get("/api/v1/health")
async def api_health() -> Dict[str, Any]:
    twins = list_saved_twins(include_cloud=False)
    return {
        "status": "healthy",
        "service": "EnterpriseTwinStudio",
        "version": "2.0.0",
        "models": {
            "deep_research_grounding": os.environ.get("SC_TWIN_PRO_MODEL", "gemini-3.1-pro-preview"),
            "parallel_pillar_synthesis": os.environ.get("SC_TWIN_FLASH_MODEL", "gemini-3.8-flash"),
        },
        "saved_portals_count": len(twins),
    }


@app.get("/api/v1/twins")
async def api_list_twins() -> Dict[str, Any]:
    twins = await asyncio.to_thread(list_saved_twins, True)
    return {"status": "success", "count": len(twins), "twins": twins}


@app.get("/api/v1/twins/{twin_slug}")
async def api_get_twin(twin_slug: str) -> Dict[str, Any]:
    spec = await asyncio.to_thread(load_twin_spec, twin_slug)
    if not spec:
        raise HTTPException(status_code=404, detail=f"Portal '{twin_slug}' not found.")
    return {"status": "success", "twin": spec}


@app.patch("/api/v1/twins/{twin_slug}")
async def api_patch_twin(twin_slug: str, req: PatchTwinRequest) -> Dict[str, Any]:
    existing = await asyncio.to_thread(load_twin_spec, twin_slug)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Portal '{twin_slug}' not found.")

    brand = existing.get("brand", {})
    if req.executive_title:
        brand["executive_title"] = req.executive_title
    if req.executive_thesis:
        brand["executive_thesis"] = req.executive_thesis
    if req.flagship_sites:
        brand["flagship_sites"] = req.flagship_sites
    if req.custom_logo_input:
        logo_spec = await asyncio.to_thread(
            resolve_company_logo,
            existing.get("canonical_name") or existing.get("company_name", ""),
            brand.get("official_domain", ""),
            req.custom_logo_input,
        )
        brand["logo"] = logo_spec.model_dump(mode="json")
    existing["brand"] = brand

    if req.persona_overrides:
        cur_p = existing.get("persona_overrides", {})
        for pid, patch_obj in req.persona_overrides.items():
            if pid in cur_p and isinstance(patch_obj, dict):
                cur_p[pid].update(patch_obj)
        existing["persona_overrides"] = cur_p

    if req.agent_relevance:
        cur_a = existing.get("agent_relevance", {})
        for aid, patch_obj in req.agent_relevance.items():
            if aid in cur_a and isinstance(patch_obj, dict):
                cur_a[aid].update(patch_obj)
        existing["agent_relevance"] = cur_a

    validated = validate_and_normalize_overlay(TwinOverlaySpec.model_validate(existing))
    saved = await asyncio.to_thread(save_twin_spec, validated, True)
    return {
        "status": "success",
        "twin_slug": saved["twin_slug"],
        "portal_url": f"/t/{saved['twin_slug']}",
        "twin": saved,
    }


@app.post("/api/v1/generate-twin")
async def api_generate_twin(req: GenerateTwinRequest) -> Dict[str, Any]:
    division = req.division_name.strip() or (req.industry or "").strip()
    result = await asyncio.to_thread(
        run_enterprise_twin_agent,
        company_name=req.company_name.strip(),
        division_name=division,
        geography=req.geography.strip() or "Global",
        focus=req.focus.strip(),
        custom_logo_input=req.custom_logo_input.strip(),
        force_refresh=req.force_refresh,
    )
    ov = result["overlay"]
    return {
        "status": "success",
        "source": result["source"],
        "twin_slug": ov["twin_slug"],
        "portal_url": f"/t/{ov['twin_slug']}",
        "display_label": ov["display_label"],
        "active_agents_count": ov["active_agents_count"],
        "hidden_agent_ids": ov["hidden_agent_ids"],
        "overlay": ov,
    }


@app.post("/api/v1/twins/generate-stream")
async def api_generate_twin_stream(req: GenerateTwinRequest) -> StreamingResponse:
    """Streams real-time SSE progress events during synthesis and finishes with redirect URL."""
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue()

    def progress_callback(ev: Dict[str, Any]) -> None:
        loop.call_soon_threadsafe(queue.put_nowait, ev)

    def worker() -> None:
        try:
            division = req.division_name.strip() or (req.industry or "").strip()
            res = run_enterprise_twin_agent(
                company_name=req.company_name.strip(),
                division_name=division,
                geography=req.geography.strip() or "Global",
                focus=req.focus.strip(),
                custom_logo_input=req.custom_logo_input.strip(),
                force_refresh=req.force_refresh,
                progress_cb=progress_callback,
            )
            ov = res["overlay"]
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {
                    "pct": 100,
                    "stage": "done",
                    "source": res["source"],
                    "twin_slug": ov["twin_slug"],
                    "display_label": ov["display_label"],
                    "active_pillars_count": ov.get("active_pillars_count", 6),
                    "active_agents_count": ov["active_agents_count"],
                    "hidden_agents_count": len(ov.get("hidden_agent_ids") or []),
                    "redirect_url": f"/t/{ov['twin_slug']}",
                    "overlay": ov,
                    "message": f"Portal ready: {ov['display_label']} ({ov.get('active_pillars_count', 6)} Pillars · {ov['active_agents_count']}/60 Agents)",
                },
            )
        except Exception as exc:
            loop.call_soon_threadsafe(
                queue.put_nowait,
                {"pct": 0, "stage": "error", "error": str(exc)},
            )

    threading.Thread(target=worker, daemon=True).start()

    async def event_generator() -> AsyncGenerator[str, None]:
        yield f"data: {json.dumps({'pct': 5, 'stage': 'accepted', 'message': f'Starting live research & synthesis for {req.company_name}...'})}\n\n"
        while True:
            ev = await queue.get()
            yield f"data: {json.dumps(ev, ensure_ascii=False)}\n\n"
            if ev.get("stage") in ("done", "error"):
                break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.api_route("/{asset_path:path}", methods=["GET", "HEAD"])
async def serve_safe_static_asset(asset_path: str) -> FileResponse:
    """Serves static HTML/CSS/JS/media files from PROJECT_ROOT while protecting dotfiles and source secrets."""
    cleaned = asset_path.strip("/")
    if not cleaned or cleaned.startswith(".") or "/." in cleaned or cleaned.startswith("enterprise_twin"):
        raise HTTPException(status_code=404, detail="Not found")
    candidate = (PROJECT_ROOT / cleaned).resolve()
    if not str(candidate).startswith(str(PROJECT_ROOT.resolve())) or not candidate.is_file():
        raise HTTPException(status_code=404, detail="Asset not found")
    return FileResponse(str(candidate))


def run_server(port: int = 8080, host: str = "0.0.0.0") -> None:
    import uvicorn

    bind_host = "0.0.0.0" if host in ("", "::", "dual") else host
    uvicorn.run(app, host=bind_host, port=port, log_level="info")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enterprise Twin Studio FastAPI Server")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8080")))
    parser.add_argument("--host", type=str, default="0.0.0.0")
    args = parser.parse_args()
    run_server(port=args.port, host=args.host)
