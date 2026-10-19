#!/usr/bin/env python3
"""
scripts/generate_mcp_card.py - Reads mcp.json and generates an SVG visualization
of the Model Context Protocol (FastMCP) tool topology and agent specifications.
"""

import json
from pathlib import Path
from typing import Dict, Any

from common import (
    ROOT_DIR,
    ASSETS_DIR,
    load_tokens,
    get_root_css,
    escape_xml
)

MCP_FILE = ROOT_DIR / "mcp.json"


def load_mcp_manifest() -> Dict[str, Any]:
    if not MCP_FILE.exists():
        return {"tools": []}
    with open(MCP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_mcp_card_svg() -> str:
    tokens = load_tokens()
    root_css = get_root_css(tokens)
    manifest = load_mcp_manifest()
    tools = manifest.get("tools", [])
    
    w, h = 840, 220
    col_w = 250
    gap = 20
    start_x = 24
    
    tools_svg = []
    for idx, tool in enumerate(tools[:3]):
        x = start_x + idx * (col_w + gap)
        name = escape_xml(tool.get("name", ""))
        repo = escape_xml(tool.get("repo", "").split("/")[-1])
        desc = escape_xml(tool.get("description", ""))
        guarantees = tool.get("guarantees", [])
        
        # Wrap description
        desc_words = desc.split()
        l1, l2 = [], []
        c = 0
        for wd in desc_words:
            if c + len(wd) < 36:
                l1.append(wd)
                c += len(wd) + 1
            else:
                l2.append(wd)
        d1 = " ".join(l1)
        d2 = " ".join(l2[:6]) + ("..." if len(l2) > 6 else "")
        
        badge_text = " • ".join(guarantees[:2])
        
        tools_svg.append(f"""
        <g transform="translate({x}, 66)">
          <rect x="0" y="0" width="{col_w}" height="114" rx="6" fill="var(--card-elevated)" stroke="var(--border)" stroke-width="1" />
          
          <text x="14" y="22" font-family="var(--font-mono)" font-size="12" font-weight="700" fill="var(--accent-teal)">{name}()</text>
          <text x="14" y="38" font-family="var(--font-mono)" font-size="10" fill="var(--text-muted)">repo: {repo}</text>
          
          <text x="14" y="60" font-family="var(--font-sans)" font-size="11" fill="var(--text-secondary)">{d1}</text>
          <text x="14" y="76" font-family="var(--font-sans)" font-size="11" fill="var(--text-secondary)">{d2}</text>
          
          <rect x="14" y="88" width="{col_w - 28}" height="18" rx="3" fill="var(--card-bg)" stroke="var(--border-accent)" stroke-width="0.8" />
          <text x="{col_w / 2}" y="100" text-anchor="middle" font-family="var(--font-mono)" font-size="9" font-weight="600" fill="var(--accent-gold)">{escape_xml(badge_text)}</text>
        </g>
        """)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Model Context Protocol (FastMCP) Tools Topology">
  <title>Model Context Protocol (FastMCP) Tool Topology</title>
  <desc>Standardized agent tools authored by Mohamed Ayman: nix_inspect_channel, git_smart_sync_audit, and session_guard_revoke_device.</desc>
  <style>
    {root_css}
    .mcp-frame {{
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 1px;
    }}
    .mcp-header {{
      fill: var(--card-elevated);
      stroke: var(--border);
      stroke-width: 1px;
    }}
    .title-main {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.8px;
      fill: var(--accent-gold);
    }}
    .title-sub {{
      font-family: var(--font-mono);
      font-size: 10px;
      fill: var(--accent-teal);
    }}
    .footer-note {{
      font-family: var(--font-mono);
      font-size: 9.5px;
      fill: var(--text-muted);
    }}
  </style>

  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" class="mcp-frame" />

  <!-- Top Bar -->
  <path d="M 0.5 8.5 A 8 8 0 0 1 8.5 0.5 L {w - 8.5} 0.5 A 8 8 0 0 1 {w - 0.5} 8.5 L {w - 0.5} 34.5 L 0.5 34.5 Z" class="mcp-header" />
  
  <g transform="translate(18, 20)">
    <circle cx="0" cy="0" r="3.5" fill="var(--accent-teal)" />
    <text x="14" y="3.5" class="title-main">MODEL CONTEXT PROTOCOL (FASTMCP) // AGENT RUNTIME SPEC</text>
    <text x="{w - 48}" y="3.5" class="title-sub" text-anchor="end">TRANSPORT: STDIO / SSE • SPEC v1.0</text>
  </g>

  <!-- Tool Cards -->
  {''.join(tools_svg)}

  <!-- Footer Link -->
  <g transform="translate(24, {h - 12})">
    <text x="0" y="0" class="footer-note">AGENT DISCOVERY ENDPOINT: <tspan fill="var(--accent-lapis)">raw.githubusercontent.com/MikeeeDeV/MikeeeDeV/main/mcp.json</tspan></text>
    <text x="{w - 48}" y="0" class="footer-note" text-anchor="end">COMPATIBLE: Claude Desktop • Antigravity • Gemini CLI</text>
  </g>
</svg>"""
    return svg


def main() -> None:
    output_path = ASSETS_DIR / "mcp-topology.svg"
    svg_content = generate_mcp_card_svg()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Generated {output_path} ({len(svg_content.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
