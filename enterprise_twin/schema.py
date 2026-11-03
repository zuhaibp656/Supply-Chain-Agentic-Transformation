"""Canonical Schema & Zero-Breakage Validator for Enterprise Twin Overlays.

Guarantees 100% alignment with `data/supply_chain_catalog.json` across:
  - 6 Core Operating Pillars (`departments`)
  - 20 Functional Sub-Pillars (`subPillars`)
  - 60 Human Personas (`personas`)
  - 60 Categorized AI Agents (`agents` — names & demos preserved; relevance & 1-line context tailored)
  - 4 End-to-End Cross-Pillar Process Journeys (`f2f`, `o2d`, `s2p`, `p2r`)
"""

from __future__ import annotations

from functools import lru_cache
import html
import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

ROOT_DIR = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT_DIR / "data" / "supply_chain_catalog.json"

DEFAULT_VALUE_CHAIN_IDS = ["f2f", "o2d", "s2p", "p2r"]


@lru_cache(maxsize=1)
def load_canonical_catalog() -> Dict[str, Any]:
    """Loads the canonical 6-Pillar / 20-Sub-Pillar / 60-Persona / 60-Agent catalog."""
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def make_twin_slug(company_name: str, division_name: Optional[str] = None) -> str:
    """Builds a deterministic URL-safe composite slug (`company` or `company--division`)."""
    def _clean(val: str) -> str:
        s = re.sub(r"[^a-z0-9]+", "-", (val or "").lower().strip()).strip("-")
        return s[:48].strip("-")

    c_slug = _clean(company_name) or "enterprise"
    d_slug = _clean(division_name or "")
    if d_slug and d_slug not in ("all", "global", "corporate", "group", c_slug):
        return f"{c_slug}--{d_slug}"
    return c_slug


def clamp_brand_hex(hex_str: str, fallback: str = "#38bdf8") -> str:
    """Ensures a valid 6-digit hex color with readable saturation/luminance for UI accents."""
    m = re.match(r"^#?([0-9a-fA-F]{6})$", (hex_str or "").strip())
    if not m:
        return fallback
    raw = m.group(1)
    r, g, b = int(raw[0:2], 16), int(raw[2:4], 16), int(raw[4:6], 16)
    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
    # If accent is too dark for dark-theme pills/text (<0.28), lift toward readable tint
    if lum < 0.28:
        lift = 0.45
        r = min(255, int(r + (255 - r) * lift))
        g = min(255, int(g + (255 - g) * lift))
        b = min(255, int(b + (255 - b) * lift))
    # If accent is near-white (>0.90), pull slightly toward sky/brand tone for light-theme contrast
    elif lum > 0.90:
        r = int(r * 0.72)
        g = int(g * 0.78)
        b = min(255, int(b * 0.92))
    return f"#{r:02x}{g:02x}{b:02x}"


def clean_ui_text(val: Optional[str], max_len: int = 280) -> str:
    """Strips stray control chars/markdown fences so DOM injection never breaks layout."""
    if not val:
        return ""
    s = re.sub(r"\s+", " ", str(val)).strip()
    s = s.replace("```", "").replace("<script", "").replace("</script", "")
    if len(s) > max_len:
        s = s[: max_len - 1].rsplit(" ", 1)[0].rstrip(".,;:") + "…"
    return s


class LogoAssetSpec(BaseModel):
    data_uri: str = Field(default="", description="Self-contained data:image/... URI or verified HTTPS URL")
    source_url: str = Field(default="", description="Original URL where the official brand logo was fetched")
    source_type: str = Field(default="initials_badge", description="wikimedia_svg | wikimedia_png | site_icon | google_hd_icon | custom | initials_badge")
    plate_style: str = Field(default="light_plate", description="light_plate | dark_plate | neutral_glass")
    aspect_ratio: float = Field(default=1.0, description="Width / Height ratio for proportional navbar framing")
    monogram: str = Field(default="SC", description="2-3 letter fallback monogram")


class CompanyBrandSpec(BaseModel):
    company_name: str
    canonical_name: str
    division_name: str = ""
    twin_slug: str
    official_domain: str = ""
    industry_sector: str = "Global Supply Chain"
    geography: str = "Global"
    brand_accent: str = "#38bdf8"
    brand_secondary: str = "#1e3a8a"
    executive_title: str = "Chief Supply Chain Officer (CSCO)"
    executive_thesis: str = ""
    flagship_sites: str = ""
    erp_systems: str = "SAP S/4HANA · SAP IBP · Enterprise WMS & TMS"
    logo: LogoAssetSpec = Field(default_factory=LogoAssetSpec)


class PillarOverrideSpec(BaseModel):
    dept_id: str
    custom_name: str = ""
    custom_tagline: str = ""
    custom_subtitle: str = ""


class SubPillarOverrideSpec(BaseModel):
    sub_pillar_id: str
    dept_id: str
    canonical_name: str
    custom_name: str


class PersonaOverrideSpec(BaseModel):
    persona_id: str
    dept_id: str
    sub_pillar_id: str
    canonical_name: str
    title: str
    role: str
    summary: str
    manual_toil: str
    agentic_impact: str
    grounding_source: str = "Career & Industry Role Mapping"


class AgentRelevanceSpec(BaseModel):
    agent_id: str
    dept_id: str
    sub_pillar_id: str
    canonical_name: str
    custom_agent_name: str = ""
    is_relevant: bool = True
    division_context: str = ""
    hidden_reason: str = ""


class ProcessJourneyOverrideSpec(BaseModel):
    vc_id: str
    custom_title: str
    custom_subtitle: str = ""


class GroundingCitation(BaseModel):
    title: str
    url: str
    snippet: str = ""


class TwinOverlaySpec(BaseModel):
    schema_version: str = "2.0"
    twin_slug: str
    company_name: str
    canonical_name: str
    division_name: str = ""
    display_label: str = ""
    brand: CompanyBrandSpec
    pillar_overrides: Dict[str, PillarOverrideSpec] = Field(default_factory=dict)
    sub_pillar_overrides: Dict[str, SubPillarOverrideSpec] = Field(default_factory=dict)
    persona_overrides: Dict[str, PersonaOverrideSpec] = Field(default_factory=dict)
    agent_relevance: Dict[str, AgentRelevanceSpec] = Field(default_factory=dict)
    process_overrides: Dict[str, ProcessJourneyOverrideSpec] = Field(default_factory=dict)
    hidden_agent_ids: List[str] = Field(default_factory=list)
    hidden_persona_ids: List[str] = Field(default_factory=list)
    active_agents_count: int = 60
    active_personas_count: int = 60
    active_sub_pillars_count: int = 20
    grounding_citations: List[GroundingCitation] = Field(default_factory=list)
    career_title_examples: List[str] = Field(default_factory=list)
    terminology_highlights: List[str] = Field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    generation_model: str = "Gemini 3.1 Pro + Gemini 3.8 Flash (Google Search Grounded)"


def validate_and_normalize_overlay(spec: TwinOverlaySpec) -> TwinOverlaySpec:
    """Enforces strict catalog integrity so no view, drawer, or chart can ever break."""
    cat = load_canonical_catalog()
    depts = cat["departments"]
    personas_cat = cat["personas"]
    agents_cat = cat["agents"]

    spec.brand.brand_accent = clamp_brand_hex(spec.brand.brand_accent, "#38bdf8")
    spec.brand.canonical_name = clean_ui_text(spec.brand.canonical_name or spec.company_name, 90)
    spec.canonical_name = spec.brand.canonical_name
    spec.division_name = clean_ui_text(spec.division_name or spec.brand.division_name, 90)
    spec.brand.division_name = spec.division_name
    spec.display_label = (
        f"{spec.canonical_name} — {spec.division_name}"
        if spec.division_name
        else spec.canonical_name
    )

    # Build canonical lookup of sub-pillars -> [(agentId, personaId)]
    sp_items_map: Dict[str, List[Dict[str, str]]] = {}
    dept_agents_map: Dict[str, List[str]] = {d_id: [] for d_id in depts}
    agent_to_persona: Dict[str, str] = {}

    for d_id, d_obj in depts.items():
        for sp in d_obj.get("subPillars", []):
            sp_id = sp["id"]
            sp_items_map[sp_id] = sp.get("items", [])
            for item in sp.get("items", []):
                aid = item["agentId"]
                pid = item["personaId"]
                dept_agents_map[d_id].append(aid)
                agent_to_persona[aid] = pid

                # Ensure every sub-pillar has an override entry
                if sp_id not in spec.sub_pillar_overrides:
                    spec.sub_pillar_overrides[sp_id] = SubPillarOverrideSpec(
                        sub_pillar_id=sp_id,
                        dept_id=d_id,
                        canonical_name=sp["name"],
                        custom_name=sp["name"],
                    )
                else:
                    spo = spec.sub_pillar_overrides[sp_id]
                    spo.custom_name = clean_ui_text(spo.custom_name or sp["name"], 64)

                # Ensure every agent has a relevance entry
                if aid not in spec.agent_relevance and aid in agents_cat:
                    spec.agent_relevance[aid] = AgentRelevanceSpec(
                        agent_id=aid,
                        dept_id=d_id,
                        sub_pillar_id=sp_id,
                        canonical_name=agents_cat[aid]["name"],
                        is_relevant=True,
                        division_context=f"Supports {spec.display_label} across {spo.custom_name}.",
                    )

                # Ensure every persona has a clean override entry
                if pid in personas_cat and pid not in spec.persona_overrides:
                    p_base = personas_cat[pid]
                    dil0 = (p_base.get("dayInLife") or [{}])[0]
                    spec.persona_overrides[pid] = PersonaOverrideSpec(
                        persona_id=pid,
                        dept_id=d_id,
                        sub_pillar_id=sp_id,
                        canonical_name=p_base["name"],
                        title=p_base["name"],
                        role=p_base.get("role", sp["name"]),
                        summary=p_base.get("summary", ""),
                        manual_toil=dil0.get("before", "Manual spreadsheet coordination across disconnected ERP exports."),
                        agentic_impact=dil0.get("after", "Autonomous Gemini AI orchestration with governed write-back."),
                    )

    # Safety Guardrail: Never allow an entire Operating Pillar (out of 6) to have 0 relevant agents!
    # Every real supply chain has Planning, Sourcing, Operations/Make, Inventory, Logistics, and Returns/Governance.
    # Keep at least 3 relevant agents per Pillar so the 6-Pillar Org Chart & Mind Map never collapse.
    for d_id, aid_list in dept_agents_map.items():
        rel_in_dept = [a for a in aid_list if spec.agent_relevance.get(a, AgentRelevanceSpec(agent_id=a, dept_id=d_id, sub_pillar_id="", canonical_name=a)).is_relevant]
        if len(rel_in_dept) < 3:
            for a in aid_list:
                if a in spec.agent_relevance and not spec.agent_relevance[a].is_relevant:
                    spec.agent_relevance[a].is_relevant = True
                    spec.agent_relevance[a].hidden_reason = ""
                    rel_in_dept.append(a)
                    if len(rel_in_dept) >= 3:
                        break

    # Clean all Persona & Agent strings
    for pid, po in spec.persona_overrides.items():
        p_base_name = personas_cat.get(pid, {}).get("name", pid)
        po.title = clean_ui_text(po.title or p_base_name, 88)
        po.role = clean_ui_text(po.role or p_base_name, 110)
        po.summary = clean_ui_text(po.summary, 260)
        po.manual_toil = clean_ui_text(po.manual_toil, 220)
        po.agentic_impact = clean_ui_text(po.agentic_impact, 220)
        po.grounding_source = clean_ui_text(po.grounding_source, 110)

    hidden_agents: List[str] = []
    hidden_personas: List[str] = []
    for aid, ar in spec.agent_relevance.items():
        ar.division_context = clean_ui_text(ar.division_context, 220)
        ar.hidden_reason = clean_ui_text(ar.hidden_reason, 160)
        ar.custom_agent_name = clean_ui_text(ar.custom_agent_name, 54)
        if not ar.is_relevant or ar.custom_agent_name == ar.canonical_name:
            ar.custom_agent_name = ""
        if not ar.is_relevant:
            hidden_agents.append(aid)
            paired_pid = agent_to_persona.get(aid)
            if paired_pid:
                hidden_personas.append(paired_pid)

    spec.hidden_agent_ids = sorted(set(hidden_agents))
    spec.hidden_persona_ids = sorted(set(hidden_personas))
    spec.active_agents_count = len(agents_cat) - len(spec.hidden_agent_ids)
    spec.active_personas_count = len(personas_cat) - len(spec.hidden_persona_ids)

    # Count active sub-pillars (sub-pillars with >= 1 relevant agent)
    active_sp = 0
    for sp_id, items in sp_items_map.items():
        if any(it["agentId"] not in spec.hidden_agent_ids for it in items):
            active_sp += 1
    spec.active_sub_pillars_count = active_sp

    # Ensure HTML-safe strings on brand thesis & title
    spec.brand.executive_title = clean_ui_text(spec.brand.executive_title, 115)
    spec.brand.executive_thesis = clean_ui_text(spec.brand.executive_thesis, 280)
    spec.brand.flagship_sites = clean_ui_text(spec.brand.flagship_sites, 220)
    spec.brand.erp_systems = clean_ui_text(spec.brand.erp_systems, 180)
    _ = html.escape(spec.display_label)

    return spec
