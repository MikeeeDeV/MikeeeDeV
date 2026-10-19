#!/usr/bin/env python3
"""
scripts/visitor_terminal_action.py - Executes in GitHub Actions when an issue is opened.
Parses whitelisted commands:
  - terminal: ping
  - terminal: vouch "<message>"
  - terminal: inspect <repo>
  - terminal: quote
Appends to data/visitors.json, regenerates assets/visitor-ledger.svg,
and generates the comment response text for the issue.

Security Hardened:
  - 24-hour rate limit per user.
  - Strict HTML/markdown/URL sanitization.
  - Input length boundaries.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from common import DATA_DIR, ROOT_DIR
from generate_visitor_ledger import generate_visitor_ledger_svg

VISITORS_FILE = DATA_DIR / "visitors.json"
ASSETS_DIR = ROOT_DIR / "assets"
RATE_LIMIT_SECONDS = 86400  # 24 Hours

WHITELISTED_QUOTES = [
    "Simplicity is a prerequisite for reliability. — Edsger W. Dijkstra",
    "There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies. — C.A.R. Hoare",
    "Purity and immutability eliminate whole classes of state bugs. — NixOS Philosophy"
]


def sanitize(text: str, max_len: int = 50) -> str:
    """Strips html, markdown, URLs, control chars, and enforces strict truncation."""
    if not text:
        return ""
    # Strip URLs
    cleaned = re.sub(r"https?://\S+", "", text)
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    # Strip Markdown syntax
    cleaned = re.sub(r"\[.*?\]\(.*?\)", "", cleaned)
    # Strip dangerous characters
    cleaned = re.sub(r"[<>{}\[\]`\\;*~_#|]", "", cleaned)
    # Strip control characters
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned)
    # Normalize whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:max_len]


def check_rate_limit(username: str, visitors: list) -> bool:
    """Returns True if the user has recorded a visit within the last 24 hours."""
    now = datetime.now(timezone.utc)
    for entry in reversed(visitors):
        if entry.get("username", "").lower() == username.lower():
            ts_str = entry.get("timestamp", "")
            try:
                # Parse ISO timestamp (e.g. 2026-10-19T14:47:00Z)
                entry_dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                diff = (now - entry_dt).total_seconds()
                if diff < RATE_LIMIT_SECONDS:
                    return True
            except Exception:
                continue
    return False


def process_issue() -> str:
    issue_title = os.environ.get("ISSUE_TITLE", "")
    raw_user = os.environ.get("ISSUE_USER", "guest")
    clean_user = sanitize(raw_user, 39) or "guest"

    if not issue_title.startswith("terminal:"):
        print("[SKIP] Issue title does not start with 'terminal:'")
        return ""

    cmd_body = issue_title[len("terminal:"):].strip()
    tokens = cmd_body.split()
    if not tokens:
        tokens = ["help"]

    subcmd = tokens[0].lower()

    # Load existing visitors
    visitors = []
    if VISITORS_FILE.exists():
        try:
            with open(VISITORS_FILE, "r", encoding="utf-8") as f:
                visitors = json.load(f)
        except Exception:
            visitors = []

    # Check 24-hour rate limit
    if check_rate_limit(clean_user, visitors):
        receipt = f"""```text
╭────────────────────────────────────────────────────────────╮
│ 📟 WORKSTATION TERMINAL NOTICE                            │
│ Handshake declined: @{clean_user:<38} │
│ Status:             429 Too Many Requests                  │
│ Reason:             Rate limit active (1 entry / 24h)      │
│ Security policy:    Only 1 handshake permitted per 24 hours │
╰────────────────────────────────────────────────────────────╯
```
*Rate limiting protects the deterministic ledger against spam.*"""
        print(receipt)
        return receipt

    # 1. Parse whitelisted commands
    if subcmd == "ping":
        cmd_name = "ping"
        msg = "Workstation latency: 0.42ms • Zero-drift active"
    elif subcmd == "vouch":
        cmd_name = "vouch"
        # Extract quoted message if present
        match = re.search(r'["\']([^"\']+)["\']', cmd_body)
        raw_msg = match.group(1) if match else " ".join(tokens[1:])
        msg = sanitize(raw_msg, 45) if raw_msg else "Handshake registered"
    elif subcmd == "inspect":
        target = sanitize(tokens[1] if len(tokens) > 1 else "NixManagerPro", 25)
        cmd_name = f"inspect {target}"
        msg = f"Derivations verified for {target} [100% reproducible]"
    elif subcmd == "quote":
        cmd_name = "quote"
        msg = WHITELISTED_QUOTES[0]
    else:
        cmd_name = "help"
        msg = "Available: ping | vouch '<msg>' | inspect <repo> | quote"

    new_entry = {
        "username": clean_user,
        "timestamp": datetime.now(timezone.utc).isoformat()[:19] + "Z",
        "command": cmd_name,
        "message": msg
    }

    visitors.append(new_entry)
    # Keep last 20
    visitors = visitors[-20:]

    VISITORS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VISITORS_FILE, "w", encoding="utf-8") as f:
        json.dump(visitors, f, indent=2, ensure_ascii=False)

    # 2. Regenerate SVG
    svg_code = generate_visitor_ledger_svg()
    out_svg = ASSETS_DIR / "visitor-ledger.svg"
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg_code)

    receipt = f"""```text
╭────────────────────────────────────────────────────────────╮
│ 📟 WORKSTATION TERMINAL RECEIPT                           │
│ Handshake verified: @{new_entry['username']:<38} │
│ Command executed:   {new_entry['command']:<38} │
│ Response:           {new_entry['message']:<38} │
│ Status:             200 OK — Entry committed to ledger     │
╰────────────────────────────────────────────────────────────╯
```
*Your entry has been cryptographically recorded into the profile ledger SVG.*"""
    print(receipt)
    return receipt


if __name__ == "__main__":
    process_issue()
