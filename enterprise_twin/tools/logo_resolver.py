"""Official Brand Logo Downloader, Optical Trimmer & Adaptive Badge Framer.

Downloads real corporate logos (never AI-generated shapes) and prepares them so
they sit cleanly inside our Dark & Light portal headers without hotlink failures,
awkward whitespace margins, or invisible dark-on-dark contrast:
  1. Custom URL or Data URI (if explicitly provided by user)
  2. Wikimedia Commons Official SVG / High-Res Transparent PNG (`commons.wikimedia.org/w/api.php`)
  3. Official Corporate Domain `<link rel="apple-touch-icon">` / Brand SVG
  4. Google High-Res Brand Icon (`t2.gstatic.com/faviconV2?...&size=128`)
  5. Crisp Typography Monogram Crest fallback (only if completely offline)
"""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path
import re
import socket
from typing import Optional, Tuple
import urllib.parse
import urllib.request

from enterprise_twin.schema import LogoAssetSpec

_ORIG_GETADDRINFO = socket.getaddrinfo


def _ipv4_preferred_getaddrinfo(*args, **kwargs):
    res = _ORIG_GETADDRINFO(*args, **kwargs)
    v4 = [r for r in res if r[0] == socket.AF_INET]
    return v4 if v4 else res


socket.getaddrinfo = _ipv4_preferred_getaddrinfo

LOGOS_CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "twins" / "logos"
LOGOS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

USER_AGENT = (
    "Mozilla/5.0 (compatible; SupplyChainTwinStudio/2.0; +https://cloud.google.com)"
)

# Verified official domains for common global & Indian conglomerates to accelerate lookup
KNOWN_OFFICIAL_DOMAINS = {
    "itc": "itcportal.com",
    "itc limited": "itcportal.com",
    "aditya birla": "adityabirla.com",
    "aditya birla group": "adityabirla.com",
    "abg": "adityabirla.com",
    "ultratech": "ultratechcement.com",
    "ultratech cement": "ultratechcement.com",
    "hindalco": "hindalco.com",
    "novelis": "novelis.com",
    "grasim": "grasim.com",
    "tata": "tata.com",
    "tata motors": "tatamotors.com",
    "tata steel": "tatasteel.com",
    "tata consumer": "tataconsumer.com",
    "reliance": "ril.com",
    "mahindra": "mahindra.com",
    "maruti": "marutisuzuki.com",
    "asian paints": "asianpaints.com",
    "hul": "hul.co.in",
    "hindustan unilever": "hul.co.in",
    "unilever": "unilever.com",
    "nestle": "nestle.com",
    "procter & gamble": "pg.com",
    "p&g": "pg.com",
    "pepsico": "pepsico.com",
    "coca-cola": "coca-colacompany.com",
    "danone": "danone.com",
    "mondelez": "mondelezinternational.com",
    "walmart": "walmart.com",
    "amazon": "amazon.com",
    "target": "target.com",
    "home depot": "homedepot.com",
    "carrefour": "carrefour.com",
    "ikea": "ikea.com",
    "nike": "nike.com",
    "zara": "inditex.com",
    "inditex": "inditex.com",
    "apple": "apple.com",
    "samsung": "samsung.com",
    "tsmc": "tsmc.com",
    "intel": "intel.com",
    "nvidia": "nvidia.com",
    "ge appliances": "geappliances.com",
    "general electric": "ge.com",
    "siemens": "siemens.com",
    "schneider electric": "se.com",
    "bosch": "bosch.com",
    "caterpillar": "caterpillar.com",
    "john deere": "deere.com",
    "volkswagen": "volkswagen-group.com",
    "toyota": "global.toyota",
    "tesla": "tesla.com",
    "bmw": "bmwgroup.com",
    "boeing": "boeing.com",
    "airbus": "airbus.com",
    "pfizer": "pfizer.com",
    "novartis": "novartis.com",
    "roche": "roche.com",
    "astrazeneca": "astrazeneca.com",
    "johnson & johnson": "jnj.com",
    "sun pharma": "sunpharma.com",
    "dr reddys": "drreddys.com",
    "cipla": "cipla.com",
    "shell": "shell.com",
    "bp": "bp.com",
    "chevron": "chevron.com",
    "exxonmobil": "exxonmobil.com",
    "ups": "ups.com",
    "fedex": "fedex.com",
    "dhl": "dhl.com",
    "maersk": "maersk.com",
    "fm logistic": "fmlogistic.com",
    "tyson": "tysonfoods.com",
    "tyson foods": "tysonfoods.com",
}


def compute_monogram(company_name: str) -> str:
    words = [w for w in re.split(r"[\s&\-\.]+", (company_name or "").strip()) if w and w.lower() not in ("the", "limited", "ltd", "inc", "corp", "corporation", "plc", "group", "company", "ag", "sa")]
    if not words:
        return "SC"
    if len(words) == 1:
        w = words[0].upper()
        return w[:3] if len(w) <= 4 else w[:2]
    return "".join(w[0].upper() for w in words[:3])


def _http_get(url: str, timeout: float = 6.0) -> Tuple[Optional[bytes], str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "image/svg+xml,image/png,image/webp,image/*,*/*;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ctype = (resp.headers.get("Content-Type") or "").lower()
            data = resp.read(1_500_000)
            return data, ctype
    except Exception:
        return None, ""


def _inspect_and_normalize_raster(raw_bytes: bytes) -> Optional[Tuple[bytes, float, str]]:
    """Trims excess transparent padding, resizes cleanly to height<=96px, and detects ink luminance."""
    try:
        from PIL import Image
    except ImportError:
        return None

    try:
        img = Image.open(io.BytesIO(raw_bytes)).convert("RGBA")
        w, h = img.size
        if w < 16 or h < 16:
            return None

        # Check alpha channel to crop excessive empty margin around transparent logos
        alpha = img.getchannel("A")
        bbox = alpha.getbbox()
        if bbox:
            cropped = img.crop(bbox)
            if cropped.width >= 12 and cropped.height >= 12:
                img = cropped

        # Resize proportionally so embedded data URI stays crisp & lightweight (~4-15KB)
        max_h = 88
        max_w = 260
        scale = min(max_h / float(img.height), max_w / float(img.width), 1.0)
        if scale < 1.0:
            img = img.resize(
                (max(16, int(round(img.width * scale))), max(16, int(round(img.height * scale)))),
                Image.Resampling.LANCZOS,
            )

        aspect = round(img.width / max(1.0, float(img.height)), 2)

        # Sample visible pixels to decide optimal backing plate (light_plate vs dark_plate)
        pixels = list(img.getdata())
        vis = [(r, g, b) for (r, g, b, a) in pixels if a > 55]
        corners_opaque = sum(
            1 for (x, y) in [(0, 0), (img.width - 1, 0), (0, img.height - 1), (img.width - 1, img.height - 1)]
            if img.getpixel((x, y))[3] > 235
        )
        if corners_opaque == 4:
            # Logo already has its own solid background tile; frame softly with zero extra white border
            plate_style = "self_plated"
        elif vis:
            avg_lum = sum((0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0 for (r, g, b) in vis) / len(vis)
            plate_style = "dark_plate" if avg_lum > 0.84 else "light_plate"
        else:
            plate_style = "light_plate"

        out = io.BytesIO()
        img.save(out, format="PNG", optimize=True)
        return out.getvalue(), aspect, plate_style
    except Exception:
        return None


def _inspect_svg(svg_bytes: bytes) -> Optional[Tuple[bytes, float, str]]:
    """Validates SVG markup, estimates aspect ratio from viewBox/width/height, and checks fill luminance."""
    try:
        txt = svg_bytes.decode("utf-8", errors="ignore").strip()
    except Exception:
        return None
    if "<svg" not in txt.lower() or "<html" in txt.lower():
        return None
    # Strip scripts if any
    txt = re.sub(r"<script[\s\S]*?</script>", "", txt, flags=re.IGNORECASE)

    aspect = 2.2
    vb = re.search(r'viewBox=["\']\s*([-\d\.]+)[,\s]+([-\d\.]+)[,\s]+([\d\.]+)[,\s]+([\d\.]+)\s*["\']', txt, re.IGNORECASE)
    if vb:
        vw, vh = float(vb.group(3)), float(vb.group(4))
        if vw > 0 and vh > 0:
            aspect = round(min(5.0, max(0.5, vw / vh)), 2)
    else:
        wm = re.search(r'\bwidth=["\']([\d\.]+)', txt)
        hm = re.search(r'\bheight=["\']([\d\.]+)', txt)
        if wm and hm and float(hm.group(1)) > 0:
            aspect = round(min(5.0, max(0.5, float(wm.group(1)) / float(hm.group(1)))), 2)

    # Check if SVG only uses white fills
    hexes = re.findall(r"#([0-9a-fA-F]{6})\b", txt)
    plate_style = "light_plate"
    if hexes:
        lums = []
        for hx in hexes[:12]:
            r, g, b = int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16)
            lums.append((0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0)
        if lums and (sum(lums) / len(lums)) > 0.88:
            plate_style = "dark_plate"

    clean_bytes = txt.encode("utf-8")
    if len(clean_bytes) > 350_000:
        return None
    return clean_bytes, aspect, plate_style


def _lookup_wikidata_p154_logo(company_name: str) -> Optional[Tuple[bytes, str, str, float, str]]:
    """Resolves the exact canonical corporate logo via Wikipedia -> Wikidata Property P154 ('logo image')."""
    # Step 1: Search English Wikipedia for the exact corporate article
    wp_params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": f"{company_name} company",
        "srlimit": "3",
        "format": "json",
    })
    raw_wp, _ = _http_get(f"https://en.wikipedia.org/w/api.php?{wp_params}", timeout=6.0)
    if not raw_wp:
        return None
    try:
        hits = ((json.loads(raw_wp.decode("utf-8")).get("query") or {}).get("search")) or []
    except Exception:
        return None
    if not hits:
        return None

    # Pick the closest matching article title
    q_low = company_name.lower().strip()
    chosen_title = hits[0]["title"]
    for h in hits:
        t_low = h["title"].lower()
        if t_low == q_low or t_low.startswith(q_low.split()[0]):
            chosen_title = h["title"]
            break

    # Step 2: Fetch Wikidata Q-ID via pageprops
    pp_params = urllib.parse.urlencode({
        "action": "query",
        "titles": chosen_title,
        "prop": "pageprops",
        "ppprop": "wikibase_item",
        "redirects": "1",
        "format": "json",
    })
    raw_pp, _ = _http_get(f"https://en.wikipedia.org/w/api.php?{pp_params}", timeout=6.0)
    if not raw_pp:
        return None
    try:
        pages = list(((json.loads(raw_pp.decode("utf-8")).get("query") or {}).get("pages") or {}).values())
        qid = ((pages[0].get("pageprops") or {}).get("wikibase_item")) if pages else None
    except Exception:
        qid = None
    if not qid:
        return None

    # Step 3: Read Wikidata P154 ('logo image') claim; if absent on Commons (fair-use logo on enwiki),
    # check English Wikipedia's official article infobox `pageimages` (when its filename contains 'logo')!
    raw_wd, _ = _http_get(
        f"https://www.wikidata.org/w/api.php?action=wbgetclaims&entity={qid}&property=P154&format=json",
        timeout=6.0,
    )
    filename = None
    if raw_wd:
        try:
            claims = ((json.loads(raw_wd.decode("utf-8")).get("claims") or {}).get("P154")) or []
            if claims:
                claims.sort(key=lambda c: 0 if c.get("rank") == "preferred" else 1)
                filename = claims[0]["mainsnak"]["datavalue"]["value"]
        except Exception:
            filename = None

    if not filename:
        # Check English Wikipedia's official infobox thumbnail (`prop=pageimages`)
        pi_params = urllib.parse.urlencode({
            "action": "query",
            "titles": chosen_title,
            "prop": "pageimages",
            "piprop": "thumbnail|name",
            "pithumbsize": "320",
            "redirects": "1",
            "format": "json",
        })
        raw_pi, _ = _http_get(f"https://en.wikipedia.org/w/api.php?{pi_params}", timeout=6.0)
        if raw_pi:
            try:
                pi_pages = list(((json.loads(raw_pi.decode("utf-8")).get("query") or {}).get("pages") or {}).values())
                page_img_name = (pi_pages[0].get("pageimage") or "").lower()
                thumb_src = ((pi_pages[0].get("thumbnail") or {}).get("source")) or ""
                if thumb_src and any(k in page_img_name for k in ("logo", "wordmark", "insignia", "crest", "symbol")):
                    img_b, _ = _http_get(thumb_src, timeout=6.0)
                    if img_b:
                        parsed = _inspect_and_normalize_raster(img_b)
                        if parsed:
                            b_clean, aspect, plate = parsed
                            return b_clean, "image/png", thumb_src, aspect, plate
            except Exception:
                pass
        return None

    # Step 4: Resolve file URL via Wikimedia Commons imageinfo
    ci_params = urllib.parse.urlencode({
        "action": "query",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
        "iiurlwidth": "320",
        "format": "json",
    })
    raw_ci, _ = _http_get(f"https://commons.wikimedia.org/w/api.php?{ci_params}", timeout=6.0)
    if not raw_ci:
        return None
    try:
        c_pages = list(((json.loads(raw_ci.decode("utf-8")).get("query") or {}).get("pages") or {}).values())
        ii = (c_pages[0].get("imageinfo") or [{}])[0]
    except Exception:
        return None

    mime = (ii.get("mime") or "").lower()
    orig_url = ii.get("url") or ""
    thumb_url = ii.get("thumburl") or ""

    if "svg" in mime and orig_url:
        svg_b, _ = _http_get(orig_url, timeout=6.0)
        if svg_b:
            parsed = _inspect_svg(svg_b)
            if parsed:
                b_clean, aspect, plate = parsed
                return b_clean, "image/svg+xml", orig_url, aspect, plate

    target_png = thumb_url or orig_url
    if target_png:
        img_b, _ = _http_get(target_png, timeout=6.0)
        if img_b:
            parsed = _inspect_and_normalize_raster(img_b)
            if parsed:
                b_clean, aspect, plate = parsed
                return b_clean, "image/png", orig_url or target_png, aspect, plate
    return None


def _search_wikimedia_logo(company_name: str) -> Optional[Tuple[bytes, str, str, float, str]]:
    """Queries Wikimedia Commons API for official `<Company> logo.svg` or `.png`."""
    # First try canonical Wikidata P154 / Wikipedia Infobox corporate logo!
    p154 = _lookup_wikidata_p154_logo(company_name)
    if p154:
        return p154

    clean_co = re.sub(r"\b(Limited|Ltd\.?|Inc\.?|PLC|Corp\.?|Corporation|Group|The)\b", "", company_name, flags=re.IGNORECASE).strip()
    queries = [f'intitle:logo "{company_name}"', f'intitle:logo "{clean_co}" filetype:drawing']
    co_tokens = [t.lower() for t in re.findall(r"[a-zA-Z0-9]+", clean_co) if len(t) >= 2]
    q_full_low = company_name.lower()

    for q in queries:
        params = urllib.parse.urlencode({
            "action": "query",
            "generator": "search",
            "gsrsearch": q,
            "gsrnamespace": "6",
            "gsrlimit": "6",
            "prop": "imageinfo",
            "iiprop": "url|mime|size",
            "iiurlwidth": "320",
            "format": "json",
        })
        api_url = f"https://commons.wikimedia.org/w/api.php?{params}"
        raw, _ = _http_get(api_url, timeout=6.0)
        if not raw:
            continue
        try:
            payload = json.loads(raw.decode("utf-8"))
            pages = list((payload.get("query") or {}).get("pages", {}).values())
        except Exception:
            continue

        def _rank(p: dict) -> Tuple[int, int]:
            title = (p.get("title") or "").lower()
            has_logo = 1 if ("logo" in title or "wordmark" in title) else 0
            tok_hits = sum(1 for t in co_tokens if re.search(rf"\b{re.escape(t)}\b", title))
            exact_co = 2 if company_name.lower() in title else 0
            subbrand_pen = 2 if ("hotel" in title and "hotel" not in q_full_low) else 0
            is_svg = 1 if title.endswith(".svg") else 0
            bad = 1 if any(b in title for b in ("building", "headquarters", "factory", "store", "product", "map", "chart", "founder", "award", "presenting")) else 0
            return (bad + subbrand_pen, -(exact_co + tok_hits * 3 + has_logo * 2 + is_svg))

        pages.sort(key=_rank)
        for p in pages:
            title_l = (p.get("title") or "").lower()
            # Strictly require 'logo' or 'wordmark' in filename so event photos are never matched!
            if "logo" not in title_l and "wordmark" not in title_l:
                continue
            if any(b in title_l for b in ("building", "headquarters", "factory", "store", "map", "chart", "station", "award", "presenting")):
                continue
            if "hotel" in title_l and "hotel" not in q_full_low:
                continue
            if co_tokens and not any(re.search(rf"\b{re.escape(t)}\b", title_l) for t in co_tokens):
                continue
            ii = (p.get("imageinfo") or [{}])[0]
            mime = (ii.get("mime") or "").lower()
            thumb_url = ii.get("thumburl") or ""
            orig_url = ii.get("url") or ""

            if "svg" in mime and orig_url:
                svg_b, _ = _http_get(orig_url, timeout=6.0)
                if svg_b:
                    parsed = _inspect_svg(svg_b)
                    if parsed:
                        b_clean, aspect, plate = parsed
                        return b_clean, "image/svg+xml", orig_url, aspect, plate

            target_png_url = thumb_url or orig_url
            if target_png_url:
                img_b, _ = _http_get(target_png_url, timeout=6.0)
                if img_b:
                    parsed = _inspect_and_normalize_raster(img_b)
                    if parsed:
                        b_clean, aspect, plate = parsed
                        return b_clean, "image/png", orig_url or target_png_url, aspect, plate
    return None


def resolve_company_logo(
    company_name: str,
    official_domain: str = "",
    custom_logo_input: str = "",
    brand_accent: str = "#38bdf8",
    brand_secondary: str = "#1e3a8a",
) -> LogoAssetSpec:
    """Downloads, trims, caches, and frames the authentic brand logo for `company_name`."""
    monogram = compute_monogram(company_name)
    slug = re.sub(r"[^a-z0-9]+", "_", company_name.lower()).strip("_") or "enterprise"

    # 0. Check custom user-supplied logo URL or data URI first
    if custom_logo_input and custom_logo_input.strip():
        inp = custom_logo_input.strip()
        if inp.startswith("data:image/"):
            return LogoAssetSpec(
                data_uri=inp,
                source_url="user_supplied_data_uri",
                source_type="custom",
                plate_style="light_plate",
                aspect_ratio=1.8,
                monogram=monogram,
            )
        if inp.startswith(("http://", "https://")):
            raw, ctype = _http_get(inp, timeout=7.0)
            if raw:
                if "svg" in ctype or inp.lower().endswith(".svg"):
                    parsed = _inspect_svg(raw)
                    if parsed:
                        b_clean, aspect, plate = parsed
                        b64 = base64.b64encode(b_clean).decode("ascii")
                        return LogoAssetSpec(
                            data_uri=f"data:image/svg+xml;base64,{b64}",
                            source_url=inp,
                            source_type="custom",
                            plate_style=plate,
                            aspect_ratio=aspect,
                            monogram=monogram,
                        )
                parsed = _inspect_and_normalize_raster(raw)
                if parsed:
                    b_clean, aspect, plate = parsed
                    b64 = base64.b64encode(b_clean).decode("ascii")
                    return LogoAssetSpec(
                        data_uri=f"data:image/png;base64,{b64}",
                        source_url=inp,
                        source_type="custom",
                        plate_style=plate,
                        aspect_ratio=aspect,
                        monogram=monogram,
                    )

    # 1. Check disk cache (`data/twins/logos/<slug>.json`)
    cache_meta = LOGOS_CACHE_DIR / f"{slug}.json"
    if cache_meta.exists() and not custom_logo_input:
        try:
            cached = json.loads(cache_meta.read_text(encoding="utf-8"))
            if cached.get("data_uri"):
                return LogoAssetSpec(**cached)
        except Exception:
            pass

    # Infer official domain if not passed
    dom = (official_domain or "").strip().lower()
    dom = re.sub(r"^https?://", "", dom).split("/")[0].replace("www.", "")
    if not dom:
        c_key = re.sub(r"\s+", " ", company_name.lower()).strip()
        for k, v in KNOWN_OFFICIAL_DOMAINS.items():
            if k == c_key or k in c_key:
                dom = v
                break

    # 2. Try Wikimedia Commons Official Vector / Transparent Brand Logo
    wiki = _search_wikimedia_logo(company_name)
    if wiki:
        b_clean, mime, src_url, aspect, plate = wiki
        ext = "svg" if "svg" in mime else "png"
        (LOGOS_CACHE_DIR / f"{slug}.{ext}").write_bytes(b_clean)
        b64 = base64.b64encode(b_clean).decode("ascii")
        spec = LogoAssetSpec(
            data_uri=f"data:{mime};base64,{b64}",
            source_url=src_url,
            source_type="wikimedia_svg" if ext == "svg" else "wikimedia_png",
            plate_style=plate,
            aspect_ratio=aspect,
            monogram=monogram,
        )
        cache_meta.write_text(spec.model_dump_json(indent=2), encoding="utf-8")
        return spec

    # 3. Try Google High-Res Official Domain Brand Icon (`t2.gstatic.com/faviconV2`, 128px)
    if dom:
        g_icon_url = (
            f"https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON"
            f"&fallback_opts=TYPE,SIZE,URL&url=https://{dom}&size=128"
        )
        raw, _ = _http_get(g_icon_url, timeout=6.0)
        if raw:
            parsed = _inspect_and_normalize_raster(raw)
            if parsed:
                b_clean, aspect, plate = parsed
                (LOGOS_CACHE_DIR / f"{slug}.png").write_bytes(b_clean)
                b64 = base64.b64encode(b_clean).decode("ascii")
                spec = LogoAssetSpec(
                    data_uri=f"data:image/png;base64,{b64}",
                    source_url=f"https://{dom}",
                    source_type="google_hd_icon",
                    plate_style=plate,
                    aspect_ratio=aspect,
                    monogram=monogram,
                )
                cache_meta.write_text(spec.model_dump_json(indent=2), encoding="utf-8")
                return spec

    # 4. Crisp Executive Monogram Badge (offline-safe fallback, cleanly styled)
    fallback_svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 72">'
        f'<rect x="2" y="2" width="116" height="68" rx="16" fill="{brand_secondary}" stroke="{brand_accent}" stroke-width="3"/>'
        f'<text x="60" y="46" fill="#ffffff" font-family="Inter,Arial,sans-serif" font-size="28" font-weight="800" text-anchor="middle" letter-spacing="1">{monogram}</text>'
        f'</svg>'
    )
    b64_fb = base64.b64encode(fallback_svg.encode("utf-8")).decode("ascii")
    return LogoAssetSpec(
        data_uri=f"data:image/svg+xml;base64,{b64_fb}",
        source_url="",
        source_type="initials_badge",
        plate_style="self_plated",
        aspect_ratio=1.67,
        monogram=monogram,
    )
