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
import socket
from typing import Any, Dict, List
import urllib.parse
import urllib.request

_ORIG_GETADDRINFO = socket.getaddrinfo


def _ipv4_preferred_getaddrinfo(*args, **kwargs):
    res = _ORIG_GETADDRINFO(*args, **kwargs)
    v4 = [r for r in res if r[0] == socket.AF_INET]
    return v4 if v4 else res


socket.getaddrinfo = _ipv4_preferred_getaddrinfo

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
    clean_co = (company_name or "").strip()
    if not clean_co:
        return {}
    # Search strictly on the company entity name (avoiding division words like "Procurement" that match non-company articles)
    queries = [f'"{clean_co}" (company OR corporation OR conglomerate OR Limited OR Inc)', f"{clean_co} company"]
    corp_markers = (
        "company", "corporation", "conglomerate", "multinational", "manufacturer",
        "retailer", "enterprise", "headquartered", "founded", "listed", "subsidiary", "bank", "pharmaceutical",
    )
    for sq in queries:
        params = urllib.parse.urlencode({
            "action": "query",
            "list": "search",
            "srsearch": sq,
            "srlimit": "5",
            "format": "json",
        })
        raw = _http_text(f"https://en.wikipedia.org/w/api.php?{params}")
        if not raw:
            continue
        try:
            hits = ((json.loads(raw).get("query") or {}).get("search")) or []
        except Exception:
            hits = []
        for hit in hits:
            title = str(hit.get("title") or "").strip()
            if not title or "disambiguation" in title.lower():
                continue
            sum_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
            sum_raw = _http_text(sum_url)
            if not sum_raw:
                continue
            try:
                data = json.loads(sum_raw)
                if data.get("type") == "disambiguation":
                    continue
                ext = (data.get("extract") or "").strip()
                desc = (data.get("description") or "").strip()
                combined_low = f"{title} {desc} {ext}".lower()
                if any(k in combined_low for k in corp_markers):
                    return {
                        "canonical_title": data.get("title", clean_co),
                        "extract": ext,
                        "description": desc,
                        "page_url": ((data.get("content_urls") or {}).get("desktop") or {}).get("page", ""),
                    }
            except Exception:
                continue
    return {}


def search_public_career_titles(company_name: str, division_name: str = "") -> List[str]:
    """Extracts real supply chain job titles for `company_name` from public career portals & job boards."""
    q = (
        f'"{company_name}" {division_name} '
        f'("Supply Chain" OR "Procurement" OR "Logistics" OR "Demand Planning" OR "Manufacturing" OR "Warehouse" OR "Sourcing") '
        f'(site:linkedin.com/jobs OR site:naukri.com OR site:indeed.com OR site:glassdoor.com OR careers)'
    )
    ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    page = _http_text(ddg_url, timeout=5.5)
    if not page:
        return []

    raw_titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', page, flags=re.IGNORECASE | re.DOTALL)
    discovered: List[str] = []
    role_kw = re.compile(
        r"\b(Manager|Director|Head|VP|Vice President|Lead|Executive|Officer|Planner|Controller|Engineer|Supervisor|Buyer|Specialist|Coordinator)\b",
        re.IGNORECASE,
    )
    for rt in raw_titles:
        clean = html.unescape(re.sub(r"<[^>]+>", "", rt)).strip()
        # Strip trailing "- LinkedIn", "| Naukri.com", "| Glassdoor", company suffixes
        clean = re.split(
            r"\s+[\-\|\–]\s+(?:LinkedIn|Naukri|Glassdoor|Indeed|Workday|Greenhouse|Lever|Jobs|Careers)",
            clean,
            flags=re.IGNORECASE,
        )[0].strip()
        clean = re.sub(r"^.*?hiring\s+", "", clean, flags=re.IGNORECASE)
        clean = re.sub(r"\s+in\s+[A-Z][a-zA-Z\s,]+$", "", clean).strip()
        if 10 <= len(clean) <= 86 and role_kw.search(clean) and clean not in discovered:
            discovered.append(clean)
        if len(discovered) >= 8:
            break
    return discovered


def mine_public_job_descriptions(company_name: str, division_name: str = "") -> List[Dict[str, str]]:
    """Extracts public Supply Chain job postings, URLs, and JD process snippets revealing internal org units & tools."""
    q = (
        f'"{company_name}" {division_name} '
        f'("Supply Chain" OR "Procurement" OR "Logistics" OR "Planning" OR "Manufacturing" OR "Warehouse") '
        f'("Responsibilities" OR "SAP" OR "Kinaxis" OR "Blue Yonder" OR "WMS" OR "S&OP") '
        f'(site:linkedin.com/jobs OR site:naukri.com OR site:indeed.com OR careers)'
    )
    ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    page = _http_text(ddg_url, timeout=6.0)
    if not page:
        return []

    blocks = re.findall(
        r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?(?:<a[^>]*class="result__snippet"[^>]*>(.*?)</a>|<div[^>]*class="result__snippet"[^>]*>(.*?)</div>)',
        page,
        flags=re.IGNORECASE | re.DOTALL,
    )
    results: List[Dict[str, str]] = []
    for raw_href, raw_title, snip1, snip2 in blocks:
        url = html.unescape(raw_href)
        m_uddg = re.search(r"uddg=([^&]+)", url)
        if m_uddg:
            url = urllib.parse.unquote(m_uddg.group(1))
        title = html.unescape(re.sub(r"<[^>]+>", "", raw_title)).strip()
        title = re.split(
            r"\s+[\-\|\–]\s+(?:LinkedIn|Naukri|Glassdoor|Indeed|Jobs|Careers)",
            title,
            flags=re.IGNORECASE,
        )[0].strip()
        snippet = html.unescape(re.sub(r"<[^>]+>", " ", snip1 or snip2 or "")).strip()
        snippet = re.sub(r"\s+", " ", snippet)
        if title and url.startswith("http") and len(snippet) >= 25:
            results.append({
                "job_title": title[:110],
                "url": url,
                "snippet": snippet[:320],
            })
        if len(results) >= 8:
            break
    return results

