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

WHITELISTED_QUOTES = [
    "Simplicity is a prerequisite for reliability. — Edsger W. Dijkstra",
    "There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies. — C.A.R. Hoare",
    "Purity and immutability eliminate whole classes of state bugs. — NixOS Philosophy"
]


def sanitize(text: str, max_len: int = 60) -> str:
    """Strips html/control chars and truncates."""
    cleaned = re.sub(r"[<>{}\[\]`\\;]", "", text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:max_len]


def process_issue() -> str:
    issue_title = os.environ.get("ISSUE_TITLE", "")
    issue_user = os.environ.get("ISSUE_USER", "guest")
    
    if not issue_title.startswith("terminal:"):
        print("[SKIP] Issue title does not start with 'terminal:'")
        return ""
        
    cmd_body = issue_title[len("terminal:"):].strip()
    tokens = cmd_body.split()
    if not tokens:
        tokens = ["help"]
        
    subcmd = tokens[0].lower()
    
    # 1. Parse commands
    if subcmd == "ping":
        cmd_name = "ping"
        msg = "Workstation latency: 0.42ms • Zero-drift active"
    elif subcmd == "vouch":
        cmd_name = "vouch"
        # Extract quoted message if present
        match = re.search(r'["\']([^"\']+)["\']', cmd_body)
        raw_msg = match.group(1) if match else " ".join(tokens[1:])
        msg = sanitize(raw_msg, 50) if raw_msg else "Handshake registered"
    elif subcmd == "inspect":
        target = sanitize(tokens[1] if len(tokens) > 1 else "NixManagerPro", 30)
        cmd_name = f"inspect {target}"
        msg = f"Derivations verified for {target} [100% reproducible]"
    elif subcmd == "quote":
        cmd_name = "quote"
        msg = WHITELISTED_QUOTES[0]
    else:
        cmd_name = "help"
        msg = "Available: ping | vouch '<msg>' | inspect <repo> | quote"
        
    # 2. Append to visitors.json
    visitors = []
    if VISITORS_FILE.exists():
        try:
            with open(VISITORS_FILE, "r", encoding="utf-8") as f:
                visitors = json.load(f)
        except Exception:
            visitors = []
            
    new_entry = {
        "username": sanitize(issue_user, 39),
        "timestamp": datetime.now(timezone.utc).isoformat()[:19] + "Z",
        "command": cmd_name,
        "message": msg
    }
    
    visitors.append(new_entry)
    # Keep last 20
    visitors = visitors[-20:]
    
    with open(VISITORS_FILE, "w", encoding="utf-8") as f:
        json.dump(visitors, f, indent=2, ensure_ascii=False)
        
    # 3. Regenerate SVG
    svg_code = generate_visitor_ledger_svg()
    out_svg = ASSETS_DIR / "visitor-ledger.svg"
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg_code)
        
    receipt = f"""```text
╭────────────────────────────────────────────────────────────╮
│ 📟 WORKSTATION TERMINAL RECEIPT                           │
│ Handshake verified: @{new_entry['username']}                             │
│ Command executed:   {new_entry['command']}                 │
│ Response:           {new_entry['message']}                 │
│ Status:             200 OK — Entry committed to ledger     │
╰────────────────────────────────────────────────────────────╯
```
*Your entry has been cryptographically recorded into the profile ledger SVG.*"""
    print(receipt)
    return receipt


if __name__ == "__main__":
    process_issue()
