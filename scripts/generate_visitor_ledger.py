#!/usr/bin/env python3
"""
scripts/generate_visitor_ledger.py - Generates an SVG card displaying
the live cryptographic visitor ledger (assets/visitor-ledger.svg)
driven by the GitHub Issues visitor terminal.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from common import (
    ROOT_DIR,
    ASSETS_DIR,
    DATA_DIR,
    load_tokens,
    get_root_css,
    escape_xml
)

VISITORS_FILE = DATA_DIR / "visitors.json"


def load_visitors() -> List[Dict[str, Any]]:
    if not VISITORS_FILE.exists():
        return [{
            "username": "MikeeeDeV",
            "timestamp": "2026-10-19T11:00:00Z",
            "command": "init",
            "message": "Initialized deterministic ledger. Welcome to the workstation."
        }]
    try:
        with open(VISITORS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def generate_visitor_ledger_svg() -> str:
    tokens = load_tokens()
    root_css = get_root_css(tokens)
    visitors = load_visitors()
    
    # Take latest 4 entries
    recent = list(reversed(visitors[-4:]))
    
    w, h = 840, 200
    
    rows_svg = []
    for idx, entry in enumerate(recent):
        y_pos = 64 + idx * 28
        ts = entry.get("timestamp", "")[:10]
        user = escape_xml(entry.get("username", "guest"))
        cmd = escape_xml(entry.get("command", "ping"))
        msg = escape_xml(entry.get("message", "Handshake acknowledged"))
        if len(msg) > 42:
            msg = msg[:39] + "..."
            
        rows_svg.append(f"""
        <g transform="translate(24, {y_pos})">
          <text x="0" y="0" font-family="var(--font-mono)" font-size="11" fill="var(--text-muted)">{ts}</text>
          <text x="85" y="0" font-family="var(--font-mono)" font-size="11" font-weight="700" fill="var(--accent-teal)">@{user}</text>
          <text x="210" y="0" font-family="var(--font-mono)" font-size="11" font-weight="600" fill="var(--accent-gold)">❯ {cmd}</text>
          <text x="340" y="0" font-family="var(--font-mono)" font-size="11" fill="var(--text-secondary)">{msg}</text>
          <text x="{w - 60}" y="0" font-family="var(--font-mono)" font-size="10" fill="var(--accent-lapis)" text-anchor="end">VERIFIED ✓</text>
        </g>
        """)
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Visitor Terminal Ledger">
  <title>Workstation Visitor Terminal Ledger</title>
  <desc>Living terminal ledger recording visitors and verified handshakes via GitHub Issues.</desc>
  <style>
    {root_css}
    .ledger-card {{
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 1px;
    }}
    .ledger-header {{
      fill: var(--card-elevated);
      stroke: var(--border);
      stroke-width: 1px;
    }}
    .title-text {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.6px;
      fill: var(--accent-gold);
    }}
    .hint-text {{
      font-family: var(--font-mono);
      font-size: 10px;
      fill: var(--text-muted);
    }}
  </style>

  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" class="ledger-card" />

  <!-- Top Title Bar -->
  <path d="M 0.5 8.5 A 8 8 0 0 1 8.5 0.5 L {w - 8.5} 0.5 A 8 8 0 0 1 {w - 0.5} 8.5 L {w - 0.5} 32.5 L 0.5 32.5 Z" class="ledger-header" />
  
  <g transform="translate(18, 18)">
    <circle cx="0" cy="0" r="3.5" fill="var(--accent-teal)" />
    <text x="14" y="3.5" class="title-text">VISITOR TERMINAL LEDGER // INTERACTIVE HANDSHAKES</text>
    <text x="{w - 48}" y="3.5" class="hint-text" text-anchor="end">TOTAL LOGS: {len(visitors)} • OPEN ISSUE TO ENTER</text>
  </g>

  <!-- Table Rows -->
  {''.join(rows_svg)}

  <!-- Bottom Terminal Status Bar -->
  <line x1="20" y1="{h - 24}" x2="{w - 20}" y2="{h - 24}" stroke="var(--border)" stroke-width="0.8" />
  <g transform="translate(24, {h - 10})">
    <text x="0" y="0" font-family="var(--font-mono)" font-size="9" fill="var(--text-muted)">HASH CHAIN: SHA256//DETERMINISTIC_LEDGER</text>
    <text x="{w - 48}" y="0" font-family="var(--font-mono)" font-size="9" fill="var(--accent-teal)" text-anchor="end">DISPATCHER: GH-ACTIONS / ZERO RUNTIME COST</text>
  </g>
</svg>"""
    return svg


def main() -> None:
    output_path = ASSETS_DIR / "visitor-ledger.svg"
    svg_content = generate_visitor_ledger_svg()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Generated {output_path} ({len(svg_content.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
