"""Keyless Public Web Corporate & Career Role Miner (Wikipedia API + Public Search Snippets).

Enriches `domain_synthesizer.py` with live company descriptions, headquarters/facilities,
and authentic supply chain job title patterns from public web listings whenever Vertex AI
ADC requires interactive RAPT re-login on a local workstation (while Cloud Run uses
Vertex AI Gemini 3.1 Pro + Google Search Grounding natively).
"""

from __future__ import annotations

import html
import json
import re
from typing import Any, Dict, List
import urllib.parse
import urllib.request

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def _http_text(url: str, timeout: float = 5.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read(500_000).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def fetch_wikipedia_company_summary(company_name: str, division_name: str = "") -> Dict[str, Any]:
    """Fetches real corporate summary & article URL from English Wikipedia REST/Action API."""
    q = f"{company_name} {division_name}".strip() if division_name and len(division_name) < 24 else company_name
    params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": f"{q} company",
        "srlimit": "2",
        "format": "json",
    })
    raw = _http_text(f"https://en.wikipedia.org/w/api.php?{params}")
    if not raw:
        return {}
    try:
        hits = ((json.loads(raw).get("query") or {}).get("search")) or []
        if not hits:
            return {}
        title = hits[0]["title"]
    except Exception:
        return {}

    sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
    sum_raw = _http_text(sum_url)
    if not sum_raw:
        return {}
    try:
        data = json.loads(sum_raw)
        return {
            "canonical_title": data.get("title", company_name),
            "extract": (data.get("extract") or "").strip(),
            "description": (data.get("description") or "").strip(),
            "page_url": ((data.get("content_urls") or {}).get("desktop") or {}).get("page", ""),
        }
    except Exception:
        return {}


def search_public_career_titles(company_name: str, division_name: str = "") -> List[str]:
    """Extracts real supply chain job titles for `company_name` from public search result titles."""
    q = f'"{company_name}" {division_name} ("Supply Chain" OR "Procurement" OR "Logistics" OR "Planning" OR "Operations") (site:linkedin.com/jobs OR site:naukri.com OR careers)'
    ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    page = _http_text(ddg_url, timeout=5.5)
    if not page:
        return []

    raw_titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', page, flags=re.IGNORECASE | re.DOTALL)
    discovered: List[str] = []
    role_kw = re.compile(
        r"\b(Manager|Director|Head|VP|Vice President|Lead|Executive|Officer|Planner|Controller|Engineer|Supervisor)\b",
        re.IGNORECASE,
    )
    for rt in raw_titles:
        clean = html.unescape(re.sub(r"<[^>]+>", "", rt)).strip()
        # Strip trailing "- LinkedIn", "| Naukri.com", company suffixes
        clean = re.split(r"\s+[\-\|\–]\s+(?:LinkedIn|Naukri|Glassdoor|Indeed|Jobs|Careers)", clean, flags=re.IGNORECASE)[0].strip()
        clean = re.sub(rf"^.*?hiring\s+", "", clean, flags=re.IGNORECASE)
        clean = re.sub(rf"\s+in\s+[A-Z][a-zA-Z\s,]+$", "", clean).strip()
        if 12 <= len(clean) <= 84 and role_kw.search(clean) and clean not in discovered:
            discovered.append(clean)
        if len(discovered) >= 6:
            break
    return discovered
