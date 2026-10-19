#!/usr/bin/env python3
"""
scripts/generate_now_building.py - Reads now.yml and renders:
1. Compact SVG status badge (assets/now-building.svg)
2. Injects formatted section into README.md between marker comments.
"""

import re
import sys
from pathlib import Path
from typing import Dict, Any

try:
    import yaml
except ImportError:
    yaml = None

from common import (
    ROOT_DIR,
    ASSETS_DIR,
    load_tokens,
    escape_xml,
    get_root_css
)

NOW_YML_PATH = ROOT_DIR / "now.yml"
README_PATH = ROOT_DIR / "README.md"
START_MARKER = "<!-- NOW-BUILDING:START -->"
END_MARKER = "<!-- NOW-BUILDING:END -->"


def parse_now_config() -> Dict[str, Any]:
    """Parses now.yml with yaml or robust fallback."""
    if not NOW_YML_PATH.exists():
        return {
            "current_focus": "Nix Flakes Desktop Engine & FastMCP Agent Tooling",
            "shipping": {
                "project": "NixManagerPro",
                "repo": "MikeeeDeV/NixManagerPro",
                "status": "Shipping v1.7.0",
                "tagline": "Asynchronous multi-channel Nix package manager for Debian/Ubuntu",
                "milestone": "v1.7.0 Released"
            },
            "secondary_focus": {
                "project": "git-smart-sync",
                "repo": "MikeeeDeV/git-smart-sync",
                "status": "Active Maintenance",
                "tagline": "Divergence protection and branch presets for VS Code"
            },
            "leadership": {
                "role": "Technical Team Leader",
                "organization": "Gawdah"
            },
            "updated": "2026-10-19"
        }
        
    with open(NOW_YML_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        
    if yaml is not None:
        return yaml.safe_load(content)
        
    # Minimal fallback parser if pyyaml absent
    data = {}
    for line in content.splitlines():
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def generate_now_building_svg(cfg: Dict[str, Any]) -> str:
    tokens = load_tokens()
    root_css = get_root_css(tokens)
    
    current_focus = escape_xml(cfg.get("current_focus", "Nix & MCP Engineering"))
    shipping = cfg.get("shipping", {})
    project = escape_xml(shipping.get("project", "NixManagerPro"))
    status = escape_xml(shipping.get("status", "Active"))
    milestone = escape_xml(shipping.get("milestone", "Shipping"))
    leadership = cfg.get("leadership", {})
    lead_role = escape_xml(leadership.get("role", "Technical Team Leader"))
    lead_org = escape_xml(leadership.get("organization", "Gawdah"))
    updated = escape_xml(cfg.get("updated", "2026-10-19"))
    
    w, h = 820, 116
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Now Building Status Card">
  <title>Now Building - Mohamed Ayman (@MikeeeDeV)</title>
  <desc>Current engineering focus: {current_focus}, shipping {project} ({status}), Team Lead at {lead_org}.</desc>
  <style>
    {root_css}
    .card-bg {{
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 1px;
    }}
    .badge-bar {{
      fill: var(--card-elevated);
      stroke: var(--border);
      stroke-width: 1px;
    }}
    .text-title {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.8px;
      fill: var(--accent-gold);
    }}
    .text-main {{
      font-family: var(--font-sans);
      font-size: 14px;
      font-weight: 600;
      fill: var(--text-primary);
    }}
    .text-sub {{
      font-family: var(--font-mono);
      font-size: 12px;
      fill: var(--text-secondary);
    }}
    .text-meta {{
      font-family: var(--font-mono);
      font-size: 11px;
      fill: var(--text-muted);
    }}
    .tag-pill {{
      fill: var(--card-elevated);
      stroke: var(--border-accent);
      stroke-width: 1px;
    }}
    .live-dot {{
      fill: var(--accent-teal);
      animation: pulse-ring 2.2s infinite ease-in-out;
    }}
    @keyframes pulse-ring {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; }}
    }}
  </style>

  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" class="card-bg" />

  <!-- Left Status Rail -->
  <g transform="translate(24, 20)">
    <!-- Live Beacon -->
    <circle cx="8" cy="8" r="4.5" class="live-dot" />
    <circle cx="8" cy="8" r="8" fill="none" stroke="var(--accent-teal)" stroke-width="1" opacity="0.3" />
    
    <text x="24" y="12" class="text-title">NOW SHIPPING &amp; ARCHITECTING</text>
    <text x="0" y="40" class="text-main">{current_focus}</text>
    <text x="0" y="64" class="text-sub">Active project: <tspan font-weight="700" fill="var(--accent-lapis)">{project}</tspan> • <tspan fill="var(--accent-gold)">{status}</tspan> ({milestone})</text>
    <text x="0" y="84" class="text-meta">Team Leadership: {lead_role} @ {lead_org} • Synced: {updated}</text>
  </g>

  <!-- Right Chamfered Badges -->
  <g transform="translate({w - 230}, 24)">
    <rect x="0" y="0" width="206" height="32" rx="4" class="tag-pill" />
    <text x="103" y="20" text-anchor="middle" font-family="var(--font-mono)" font-size="11" font-weight="600" fill="var(--accent-gold)">❄️ NIX ENGINE v1.7.0</text>
    
    <rect x="0" y="38" width="206" height="32" rx="4" class="tag-pill" />
    <text x="103" y="58" text-anchor="middle" font-family="var(--font-mono)" font-size="11" font-weight="600" fill="var(--accent-teal)">⚡ FASTMCP SPEC 1.0</text>
  </g>
</svg>"""
    return svg


def render_now_building_markdown(cfg: Dict[str, Any]) -> str:
    current = cfg.get("current_focus", "Nix & MCP Engineering")
    shipping = cfg.get("shipping", {})
    sec = cfg.get("secondary_focus", {})
    lead = cfg.get("leadership", {})
    exploring = cfg.get("exploring", [])
    
    exploring_md = " • ".join(exploring) if exploring else "Zero-drift systems • MCP Autonomous loops"
    
    md = f"""<div align="center">
  <a href="https://github.com/{shipping.get('repo', 'MikeeeDeV/NixManagerPro')}">
    <img src="assets/now-building.svg" width="100%" alt="Now Building Status Badge" />
  </a>
</div>

- **Primary Focus**: **{current}**
- **Active Release**: [`{shipping.get('project', 'NixManagerPro')}`](https://github.com/{shipping.get('repo', '')}) — *{shipping.get('status', '')}* ({shipping.get('tagline', '')})
- **Secondary Track**: [`{sec.get('project', 'git-smart-sync')}`](https://github.com/{sec.get('repo', '')}) — *{sec.get('status', '')}* ({sec.get('tagline', '')})
- **Leadership**: **{lead.get('role', 'Technical Team Leader')}** at **{lead.get('organization', 'Gawdah')}**
- **Current R&amp;D**: `{exploring_md}`"""
    return md


def update_readme_now_building() -> None:
    cfg = parse_now_config()
    svg_content = generate_now_building_svg(cfg)
    
    output_path = ASSETS_DIR / "now-building.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Generated {output_path} ({len(svg_content.encode('utf-8'))} bytes)")
    
    if README_PATH.exists():
        now_md = render_now_building_markdown(cfg)
        with open(README_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            
        pattern = re.compile(
            rf"({re.escape(START_MARKER)})(.*?)({re.escape(END_MARKER)})",
            re.DOTALL
        )
        if pattern.search(content):
            new_content = pattern.sub(f"\\1\n{now_md}\n\\3", content)
            with open(README_PATH, "w", encoding="utf-8") as f:
                f.write(new_content)
            print("[OK] Updated README.md now-building section.")
        else:
            print("[INFO] Markers not found in README.md; will be embedded during README synthesis.")


def main() -> None:
    update_readme_now_building()


if __name__ == "__main__":
    main()
