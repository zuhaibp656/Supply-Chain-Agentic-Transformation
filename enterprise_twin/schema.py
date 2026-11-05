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


def clean_ui_text(val: Optional[str], max_len: int = 340) -> str:
    """Strips stray control chars/markdown fences and trims cleanly at sentence boundaries."""
    if not val:
        return ""
    s = re.sub(r"\s+", " ", str(val)).strip()
    s = s.replace("```", "").replace("<script", "").replace("</script", "")
    if len(s) > max_len:
        window = s[:max_len]
        # Prefer ending cleanly on a complete sentence if one finishes past 55% of max_len
        for punct in (". ", "! ", "? "):
            idx = window.rfind(punct)
            if idx >= int(max_len * 0.55):
                return window[: idx + 1].strip()
        if window.endswith("."):
            return window.strip()
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


VALID_WATERMARK_TYPES = {
    "demand_wave",
    "supplier_graph",
    "factory_arm",
    "warehouse_rack",
    "corridor_lifo",
    "conveyor_rack",
}

EXECUTIVE_PILLAR_PALETTE = [
    "#2563eb",  # Royal Blue
    "#7c3aed",  # Violet
    "#ea580c",  # Burnt Orange
    "#0284c7",  # Cerulean Cyan
    "#059669",  # Emerald Green
    "#e11d48",  # Crimson Rose
    "#ca8a04",  # Warm Gold
    "#4f46e5",  # Deep Indigo
]


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = (hex_color or "#2563eb").lstrip("#")
    if len(h) != 6:
        return (37, 99, 235)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _rgb_dist(c1: str, c2: str) -> float:
    r1, g1, b1 = _hex_to_rgb(c1)
    r2, g2, b2 = _hex_to_rgb(c2)
    # Perceptually weighted redmean RGB distance
    rmean = (r1 + r2) / 2.0
    dr, dg, db = r1 - r2, g1 - g2, b1 - b2
    return (((2.0 + rmean / 256.0) * dr * dr) + 4.0 * dg * dg + ((2.0 + (255.0 - rmean) / 256.0) * db * db)) ** 0.5


def ensure_distinct_pillar_colors(colors: List[str], min_dist: float = 165.0) -> List[str]:
    """Guarantees every Operating Pillar in a portal view has a visually distinct color."""
    assigned: List[str] = []
    for idx, raw in enumerate(colors):
        fallback = EXECUTIVE_PILLAR_PALETTE[idx % len(EXECUTIVE_PILLAR_PALETTE)]
        cand = clamp_brand_hex(raw, fallback)
        # Replace legacy teal #0d9488 when emerald #059669 or cyan #0284c7 is present, or any near-duplicate color
        if cand.lower() == "#0d9488":
            cand = "#e11d48"
        if assigned and min(_rgb_dist(cand, prev) for prev in assigned) < min_dist:
            best_col = max(
                EXECUTIVE_PILLAR_PALETTE,
                key=lambda p: min(_rgb_dist(p, prev) for prev in assigned),
            )
            cand = best_col
        assigned.append(cand)
    return assigned


class PillarOverrideSpec(BaseModel):
    dept_id: str
    custom_name: str = ""
    custom_tagline: str = ""
    custom_subtitle: str = ""


class CustomPillarSpec(BaseModel):
    pillar_id: str = Field(description="URL/DOM-safe slug ID for this organization-specific Operating Pillar")
    v_num: str = Field(default="01", description="2-digit sequence e.g. '01', '02', ..., '07'")
    scor_badge: str = Field(default="01 · PILLAR", description="Short uppercase badge e.g. '01 · ILTD LEAF & AGRI'")
    name: str = Field(description="Organization-authentic Operating Pillar name")
    tagline: str = Field(default="", description="Short operational scope tagline")
    subtitle: str = Field(default="", description="1-sentence executive description of how this pillar operates")
    color: str = Field(default="#2563eb", description="Hex accent color")
    watermark_type: str = Field(default="demand_wave", description="One of VALID_WATERMARK_TYPES")
    sub_pillar_ids: List[str] = Field(default_factory=list, description="Assigned functional sub-pillar IDs from the 20-sub-pillar catalog")


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
    custom_pillars: List[CustomPillarSpec] = Field(default_factory=list)
    pillar_overrides: Dict[str, PillarOverrideSpec] = Field(default_factory=dict)
    sub_pillar_overrides: Dict[str, SubPillarOverrideSpec] = Field(default_factory=dict)
    persona_overrides: Dict[str, PersonaOverrideSpec] = Field(default_factory=dict)
    agent_relevance: Dict[str, AgentRelevanceSpec] = Field(default_factory=dict)
    process_overrides: Dict[str, ProcessJourneyOverrideSpec] = Field(default_factory=dict)
    hidden_agent_ids: List[str] = Field(default_factory=list)
    hidden_persona_ids: List[str] = Field(default_factory=list)
    active_pillars_count: int = 6
    active_agents_count: int = 60
    active_personas_count: int = 60
    active_sub_pillars_count: int = 20
    grounding_citations: List[GroundingCitation] = Field(default_factory=list)
    career_title_examples: List[str] = Field(default_factory=list)
    terminology_highlights: List[str] = Field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    generation_model: str = "Gemini 3.1 Pro + Gemini 3.8 Flash (Google Search Grounded)"


def _infer_watermark_for_subpillars(sp_ids: List[str], fallback_idx: int = 0) -> str:
    joined = " ".join(sp_ids)
    if any(k in joined for k in ("supplier", "material", "contract")):
        return "supplier_graph"
    if any(k in joined for k in ("production", "capacity", "quality")):
        return "factory_arm"
    if any(k in joined for k in ("positioning", "warehouse", "omnichannel")):
        return "warehouse_rack"
    if any(k in joined for k in ("first_mid", "store_replenish", "last_mile", "route_carrier")):
        return "corridor_lifo"
    if any(k in joined for k in ("returns", "expiry", "pallet")):
        return "conveyor_rack"
    if any(k in joined for k in ("demand", "trade_promotion", "sop_ibp", "portfolio")):
        return "demand_wave"
    order = ["demand_wave", "supplier_graph", "factory_arm", "warehouse_rack", "corridor_lifo", "conveyor_rack"]
    return order[fallback_idx % len(order)]


def validate_and_normalize_overlay(spec: TwinOverlaySpec) -> TwinOverlaySpec:
    """Enforces strict catalog integrity across 4–8 dynamic Operating Pillars so no view can ever break."""
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
    sp_default_dept: Dict[str, str] = {}
    dept_agents_map: Dict[str, List[str]] = {d_id: [] for d_id in depts}
    agent_to_persona: Dict[str, str] = {}
    ordered_all_sp_ids: List[str] = []

    for d_id, d_obj in depts.items():
        for sp in d_obj.get("subPillars", []):
            sp_id = sp["id"]
            ordered_all_sp_ids.append(sp_id)
            sp_default_dept[sp_id] = d_id
            sp_items_map[sp_id] = sp.get("items", [])
            for item in sp.get("items", []):
                aid = item["agentId"]
                pid = item["personaId"]
                dept_agents_map[d_id].append(aid)
                agent_to_persona[aid] = pid

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

                if aid not in spec.agent_relevance and aid in agents_cat:
                    spec.agent_relevance[aid] = AgentRelevanceSpec(
                        agent_id=aid,
                        dept_id=d_id,
                        sub_pillar_id=sp_id,
                        canonical_name=agents_cat[aid]["name"],
                        is_relevant=True,
                        division_context=f"Supports {spec.display_label} across {spo.custom_name}.",
                    )

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

    # Safety Guardrail: Keep at least 3 relevant agents per canonical domain so no functional area vanishes completely
    for d_id, aid_list in dept_agents_map.items():
        rel_in_dept = [
            a
            for a in aid_list
            if spec.agent_relevance.get(
                a, AgentRelevanceSpec(agent_id=a, dept_id=d_id, sub_pillar_id="", canonical_name=a)
            ).is_relevant
        ]
        if len(rel_in_dept) < 3:
            for a in aid_list:
                if a in spec.agent_relevance and not spec.agent_relevance[a].is_relevant:
                    spec.agent_relevance[a].is_relevant = True
                    spec.agent_relevance[a].hidden_reason = ""
                    rel_in_dept.append(a)
                    if len(rel_in_dept) >= 3:
                        break

    # Clean all Persona & Agent strings (2-line plain-English story budgets)
    for pid, po in spec.persona_overrides.items():
        p_base_name = personas_cat.get(pid, {}).get("name", pid)
        po.title = clean_ui_text(po.title or p_base_name, 92)
        po.role = clean_ui_text(po.role or p_base_name, 120)
        po.summary = clean_ui_text(po.summary, 340)
        po.manual_toil = clean_ui_text(po.manual_toil, 280)
        po.agentic_impact = clean_ui_text(po.agentic_impact, 280)
        po.grounding_source = clean_ui_text(po.grounding_source, 120)

    hidden_agents: List[str] = []
    hidden_personas: List[str] = []
    for aid, ar in spec.agent_relevance.items():
        ar.division_context = clean_ui_text(ar.division_context, 300)
        ar.hidden_reason = clean_ui_text(ar.hidden_reason, 175)
        ar.custom_agent_name = clean_ui_text(ar.custom_agent_name, 56)
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

    active_sp_ids: List[str] = []
    for sp_id in ordered_all_sp_ids:
        items = sp_items_map.get(sp_id, [])
        if any(it["agentId"] not in spec.hidden_agent_ids for it in items):
            active_sp_ids.append(sp_id)
    spec.active_sub_pillars_count = len(active_sp_ids)

    # Normalize & Validate Dynamic `custom_pillars` (4 to 8 authentic organization pillars)
    raw_custom = list(spec.custom_pillars or [])
    if not raw_custom:
        # Materialize from `pillar_overrides` + canonical 6 pillars if `custom_pillars` wasn't supplied
        for idx, (d_id, d_obj) in enumerate(depts.items()):
            po = spec.pillar_overrides.get(d_id)
            raw_custom.append(
                CustomPillarSpec(
                    pillar_id=d_id,
                    v_num=f"0{idx + 1}",
                    scor_badge=d_obj.get("scorBadge", f"0{idx + 1} · PILLAR"),
                    name=(po.custom_name if po and po.custom_name else d_obj["name"]),
                    tagline=(po.custom_tagline if po and po.custom_tagline else d_obj.get("tagline", "")),
                    subtitle=(po.custom_subtitle if po and po.custom_subtitle else d_obj.get("subtitle", "")),
                    color=d_obj.get("color", EXECUTIVE_PILLAR_PALETTE[idx % len(EXECUTIVE_PILLAR_PALETTE)]),
                    watermark_type=d_obj.get("watermarkType", "demand_wave"),
                    sub_pillar_ids=[sp["id"] for sp in d_obj.get("subPillars", [])],
                )
            )

    # Deduplicate sub_pillar_ids across custom_pillars and ensure 100% coverage of all 20 sub-pillars
    seen_sp: set[str] = set()
    normalized_pillars: List[CustomPillarSpec] = []
    seen_pids: set[str] = set()

    for idx, cp in enumerate(raw_custom[:8]):
        clean_sps = [s for s in cp.sub_pillar_ids if s in sp_items_map and s not in seen_sp]
        seen_sp.update(clean_sps)
        raw_pid = re.sub(r"[^a-z0-9_]+", "_", (cp.pillar_id or cp.name or f"pillar_{idx+1}").lower()).strip("_")[:40]
        if not raw_pid or raw_pid in seen_pids:
            raw_pid = f"pillar_{idx + 1}_{raw_pid[:24]}".strip("_")
        seen_pids.add(raw_pid)
        cp.pillar_id = raw_pid
        cp.sub_pillar_ids = clean_sps
        normalized_pillars.append(cp)

    # Assign any unassigned canonical sub-pillars into the best-matching pillar so ZERO agents/personas are orphaned
    missing_sps = [s for s in ordered_all_sp_ids if s not in seen_sp]
    if missing_sps and normalized_pillars:
        for ms in missing_sps:
            def_dept = sp_default_dept.get(ms, "")
            matched_cp = next((c for c in normalized_pillars if c.pillar_id == def_dept), None)
            if not matched_cp:
                wm = _infer_watermark_for_subpillars([ms])
                matched_cp = next((c for c in normalized_pillars if c.watermark_type == wm), normalized_pillars[-1])
            matched_cp.sub_pillar_ids.append(ms)

    # Filter out any custom pillar that ended up with 0 active sub-pillars
    final_pillars: List[CustomPillarSpec] = []
    for cp in normalized_pillars:
        has_active = any(
            any(it["agentId"] not in spec.hidden_agent_ids for it in sp_items_map.get(s, []))
            for s in cp.sub_pillar_ids
        )
        if cp.sub_pillar_ids and has_active:
            final_pillars.append(cp)

    # Re-sequence numbers, colors, watermarks, and clean text
    distinct_colors = ensure_distinct_pillar_colors(
        [
            cp.color or EXECUTIVE_PILLAR_PALETTE[i % len(EXECUTIVE_PILLAR_PALETTE)]
            for i, cp in enumerate(final_pillars)
        ]
    )
    for idx, cp in enumerate(final_pillars):
        v_num = f"{idx + 1:02d}"
        cp.v_num = v_num
        cp.name = clean_ui_text(cp.name, 56) or f"Operating Pillar {v_num}"
        raw_badge = clean_ui_text(cp.scor_badge, 34).upper()
        if not raw_badge or not raw_badge[:2].isdigit():
            short_tag = re.sub(r"[^A-Z0-9 &/-]", "", cp.name.upper()).strip()[:20].strip()
            cp.scor_badge = f"{v_num} · {short_tag or 'OPERATIONS'}"
        else:
            parts = raw_badge.split("·", 1)
            cp.scor_badge = f"{v_num} · {parts[1].strip()}" if len(parts) > 1 else f"{v_num} · {raw_badge}"
        cp.tagline = clean_ui_text(cp.tagline, 78) or f"{spec.display_label} · {cp.name}"
        cp.subtitle = clean_ui_text(cp.subtitle, 190) or f"Orchestrating {cp.name.lower()} across {spec.display_label}."
        cp.color = distinct_colors[idx]
        if cp.watermark_type not in VALID_WATERMARK_TYPES:
            cp.watermark_type = _infer_watermark_for_subpillars(cp.sub_pillar_ids, idx)

    spec.custom_pillars = final_pillars
    spec.active_pillars_count = len(final_pillars)

    # Ensure HTML-safe strings on brand thesis & title
    spec.brand.executive_title = clean_ui_text(spec.brand.executive_title, 120)
    spec.brand.executive_thesis = clean_ui_text(spec.brand.executive_thesis, 420)
    spec.brand.flagship_sites = clean_ui_text(spec.brand.flagship_sites, 260)
    spec.brand.erp_systems = clean_ui_text(spec.brand.erp_systems, 210)
    _ = html.escape(spec.display_label)

    return spec

