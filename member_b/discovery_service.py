"""
Live opportunity discovery for Member B.

Priority:
  1. Member A Node discovery service (GitHub, boards, LinkedIn, Twitter, careers)
  2. Python GitHub Search API fallback
  3. Optional mock dataset only when INROAD_ALLOW_MOCK_FALLBACK=true
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from member_b.dataset import get_mock_opportunities

logger = logging.getLogger(__name__)

SOURCE_TYPE_MAP = {
    "github": "github_repo",
    "jobboards": "job_board",
    "linkedin": "linkedin",
    "twitter": "founder_post",
    "companycareer": "employee_post",
    "unknown": "newsletter",
}

STAGE_DEFAULT = "series_a"


def _map_source_type(source: str) -> str:
    key = (source or "unknown").lower().replace("_", "")
    return SOURCE_TYPE_MAP.get(key, "newsletter")


def _adapt_opportunity(raw: Dict[str, Any], index: int) -> Dict[str, Any]:
    posted = raw.get("postedDate") or raw.get("posted_date")
    if posted:
        posted_date = str(posted)[:10]
    else:
        posted_date = datetime.now().strftime("%Y-%m-%d")

    description = raw.get("description") or raw.get("title") or ""
    skills = raw.get("skills") or []
    if skills:
        description = f"{description}\n\nSkills: {', '.join(skills)}"

    return {
        "id": index + 1,
        "title": raw.get("title") or "Opportunity",
        "company": raw.get("company") or "Unknown",
        "source_type": _map_source_type(raw.get("source")),
        "description": description.strip(),
        "team_size": int(raw.get("team_size") or 6),
        "stage": raw.get("stage") or STAGE_DEFAULT,
        "posted_date": posted_date,
        "url": raw.get("url"),
        "location": raw.get("location"),
        "opportunity_type": raw.get("opportunityType"),
    }


def _discover_via_node() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    member_a_dir = Path(__file__).resolve().parent.parent / "member_a"
    cli = member_a_dir / "cli_discover.js"
    if not cli.exists():
        return [], {"node": {"active": False, "error": "cli_discover.js missing"}}

    try:
        proc = subprocess.run(
            ["node", str(cli.name)],
            cwd=str(member_a_dir),
            capture_output=True,
            text=True,
            timeout=90,
            env=os.environ.copy(),
            check=False,
        )
    except FileNotFoundError:
        return [], {"node": {"active": False, "error": "Node.js not installed"}}
    except subprocess.TimeoutExpired:
        return [], {"node": {"active": False, "error": "Discovery timed out"}}

    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "Node discovery failed").strip()
        return [], {"node": {"active": False, "error": err[:500]}}

    payload = json.loads(proc.stdout)
    raw_list = payload.get("opportunities") or []
    source_status = payload.get("sourceStatus") or {}
    adapted = [_adapt_opportunity(item, i) for i, item in enumerate(raw_list)]
    return adapted, {"node": source_status}


def _discover_via_github_api() -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    query = urllib.parse.quote('hiring OR internship in:title is:issue is:open')
    url = f"https://api.github.com/search/issues?q={query}&sort=created&order=desc&per_page=15"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "InRoad-Opportunity-Engine"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        return [], {"github_api": {"active": False, "error": f"HTTP {exc.code}"}}
    except urllib.error.URLError as exc:
        return [], {"github_api": {"active": False, "error": str(exc.reason)}}

    items = data.get("items") or []
    opportunities: List[Dict[str, Any]] = []
    for i, issue in enumerate(items):
        repo_url = issue.get("repository_url") or ""
        company = repo_url.rstrip("/").split("/")[-1] if repo_url else "Open Source"
        opportunities.append(
            _adapt_opportunity(
                {
                    "title": issue.get("title"),
                    "company": company,
                    "description": issue.get("body") or issue.get("title"),
                    "source": "github",
                    "url": issue.get("html_url"),
                    "postedDate": issue.get("created_at"),
                    "location": "Remote/Unknown",
                    "opportunityType": "Open Source",
                },
                i,
            )
        )

    return opportunities, {"github_api": {"active": True, "count": len(opportunities)}}


def discover_opportunities() -> Dict[str, Any]:
    """
    Discover opportunities from live sources.

    Returns dict with keys: opportunities, discovery_mode, source_status
    """
    all_status: Dict[str, Any] = {}
    combined: List[Dict[str, Any]] = []

    node_opps, node_status = _discover_via_node()
    all_status.update(node_status)
    combined.extend(node_opps)

    if len(combined) < 5:
        gh_opps, gh_status = _discover_via_github_api()
        all_status.update(gh_status)
        seen = {f"{o['title']}|{o['company']}" for o in combined}
        for opp in gh_opps:
            key = f"{opp['title']}|{opp['company']}"
            if key not in seen:
                combined.append(opp)
                seen.add(key)

    # Re-assign sequential ids
    for i, opp in enumerate(combined):
        opp["id"] = i + 1

    if combined:
        return {
            "opportunities": combined,
            "discovery_mode": "live",
            "source_status": all_status,
        }

    if os.getenv("INROAD_ALLOW_MOCK_FALLBACK", "").lower() in ("1", "true", "yes"):
        logger.warning("Live discovery empty — using mock fallback (INROAD_ALLOW_MOCK_FALLBACK)")
        return {
            "opportunities": get_mock_opportunities(),
            "discovery_mode": "mock_fallback",
            "source_status": all_status,
        }

    return {
        "opportunities": [],
        "discovery_mode": "none",
        "source_status": all_status,
    }
