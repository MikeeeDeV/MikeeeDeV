#!/usr/bin/env python3
"""
scripts/common.py - Shared design system tokens, SVG utilities, and zero-crash GitHub API client.
"""

import json
import os
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
import xml.sax.saxutils as saxutils

ROOT_DIR = Path(__file__).resolve().parent.parent
DESIGN_DIR = ROOT_DIR / "design"
DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
ASSETS_DIR = ROOT_DIR / "assets"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def load_tokens() -> Dict[str, Any]:
    """Loads design tokens from design/tokens.json."""
    tokens_path = DESIGN_DIR / "tokens.json"
    if not tokens_path.exists():
        raise FileNotFoundError(f"Tokens file not found at {tokens_path}")
    with open(tokens_path, "r", encoding="utf-8") as f:
        return json.load(f)


def escape_xml(text: Any) -> str:
    """Escapes XML entities safely."""
    if text is None:
        return ""
    s = str(text)
    return saxutils.escape(s, entities={
        '"': "&quot;",
        "'": "&apos;"
    })


def save_cache(name: str, data: Any) -> None:
    """Saves serialized data to data/cache/{name}.json."""
    path = CACHE_DIR / f"{name}.json"
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WARN] Failed to write cache {name}: {e}")


def load_cache(name: str, default: Any = None) -> Any:
    """Loads cached data from data/cache/{name}.json."""
    path = CACHE_DIR / f"{name}.json"
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Failed to read cache {name}: {e}")
    return default


def get_github_token() -> Optional[str]:
    """Retrieves GitHub token from environment."""
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def fetch_github_api(endpoint: str, default: Any = None) -> Any:
    """
    Zero-crash GitHub API fetcher:
    1. Tries `gh api` CLI if available.
    2. Falls back to urllib.request with GITHUB_TOKEN if present.
    3. On rate-limit or network failure, falls back to local cache.
    """
    cache_key = endpoint.replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_")
    
    # 1. Try gh api if installed
    try:
        proc = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True,
            text=True,
            timeout=15
        )
        if proc.returncode == 0 and proc.stdout.strip():
            data = json.loads(proc.stdout)
            save_cache(cache_key, data)
            return data
    except Exception:
        pass

    # 2. Try direct HTTP with urllib
    url = endpoint if endpoint.startswith("http") else f"https://api.github.com/{endpoint.lstrip('/')}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "MikeeeDeV-Profile-Engine"
    }
    token = get_github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                save_cache(cache_key, data)
                return data
    except (urllib.error.HTTPError, urllib.error.URLError, Exception) as e:
        print(f"[WARN] API request to {endpoint} failed: {e}. Falling back to cache.")

    # 3. Cache fallback
    cached = load_cache(cache_key, default=default)
    if cached is not None:
        return cached

    return default


def fetch_graphql(query: str, variables: Dict[str, Any], cache_key: str, default: Any = None) -> Any:
    """Executes a GraphQL query using `gh api graphql` or direct HTTP, with cache fallback."""
    # Try gh api graphql
    try:
        args = ["gh", "api", "graphql", "-f", f"query={query}"]
        for k, v in variables.items():
            args.extend(["-F", f"{k}={v}"])
        proc = subprocess.run(args, capture_output=True, text=True, timeout=15)
        if proc.returncode == 0 and proc.stdout.strip():
            res = json.loads(proc.stdout)
            if "data" in res:
                save_cache(cache_key, res["data"])
                return res["data"]
    except Exception:
        pass

    # Try urllib
    token = get_github_token()
    if token:
        try:
            req_data = json.dumps({"query": query, "variables": variables}).encode("utf-8")
            req = urllib.request.Request(
                "https://api.github.com/graphql",
                data=req_data,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "User-Agent": "MikeeeDeV-Profile-Engine"
                }
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                if response.status == 200:
                    res = json.loads(response.read().decode("utf-8"))
                    if "data" in res:
                        save_cache(cache_key, res["data"])
                        return res["data"]
        except Exception as e:
            print(f"[WARN] GraphQL fetch failed: {e}. Falling back to cache.")

    cached = load_cache(cache_key, default=default)
    if cached is not None:
        return cached

    return default


def calculate_account_age(created_at_iso: str) -> str:
    """Calculates human readable account age, e.g. '2 yrs 1 mo'."""
    try:
        dt = datetime.fromisoformat(created_at_iso.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        months = (now.year - dt.year) * 12 + (now.month - dt.month)
        years = months // 12
        rem_months = months % 12
        if years > 0 and rem_months > 0:
            return f"{years}y {rem_months}m"
        elif years > 0:
            return f"{years} years"
        return f"{months} months"
    except Exception:
        return "2+ years"


def format_relative_time(iso_str: str) -> str:
    """Formats an ISO timestamp into a concise relative string e.g. '3h ago' or '2d ago'."""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = now - dt
        seconds = int(diff.total_seconds())
        if seconds < 60:
            return "just now"
        if seconds < 3600:
            return f"{seconds // 60}m ago"
        if seconds < 86400:
            return f"{seconds // 3600}h ago"
        days = seconds // 86400
        if days < 30:
            return f"{days}d ago"
        if days < 365:
            return f"{days // 30}mo ago"
        return f"{days // 365}y ago"
    except Exception:
        return "recently"


def get_root_css(tokens: Dict[str, Any]) -> str:
    """Returns CSS with light/dark prefers-color-scheme custom variables."""
    d = tokens["colors"]["dark"]
    l = tokens["colors"]["light"]
    t = tokens["typography"]
    
    return f"""
    :root {{
      --bg: {d["bg"]};
      --card-bg: {d["card_bg"]};
      --card-elevated: {d["card_elevated"]};
      --border: {d["border"]};
      --border-accent: {d["border_accent"]};
      --text-primary: {d["text_primary"]};
      --text-secondary: {d["text_secondary"]};
      --text-muted: {d["text_muted"]};
      --accent-gold: {d["accent_gold"]};
      --accent-lapis: {d["accent_lapis"]};
      --accent-teal: {d["accent_teal"]};
      --accent-coral: {d["accent_coral"]};
      --term-green: {d["terminal_green"]};
      --term-yellow: {d["terminal_yellow"]};
      --term-blue: {d["terminal_blue"]};
      --term-purple: {d["terminal_purple"]};
      --font-mono: {t["font_mono"]};
      --font-sans: {t["font_sans"]};
      --font-arabic: {t["font_arabic"]};
    }}

    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: {l["bg"]};
        --card-bg: {l["card_bg"]};
        --card-elevated: {l["card_elevated"]};
        --border: {l["border"]};
        --border-accent: {l["border_accent"]};
        --text-primary: {l["text_primary"]};
        --text-secondary: {l["text_secondary"]};
        --text-muted: {l["text_muted"]};
        --accent-gold: {l["accent_gold"]};
        --accent-lapis: {l["accent_lapis"]};
        --accent-teal: {l["accent_teal"]};
        --accent-coral: {l["accent_coral"]};
        --term-green: {l["terminal_green"]};
        --term-yellow: {l["terminal_yellow"]};
        --term-blue: {l["terminal_blue"]};
        --term-purple: {l["terminal_purple"]};
      }}
    }}
    """
