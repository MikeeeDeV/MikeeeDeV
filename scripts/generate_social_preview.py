#!/usr/bin/env python3
"""
scripts/generate_social_preview.py - Generates 1280x640 OpenGraph social preview images
and README-header templates for each pinned repo (NixManagerPro, next-session-guard,
git-smart-sync, My-portfolio).
Saves output to distribution/repo-assets/.
"""

import os
from pathlib import Path
from typing import Dict, Any

from common import (
    ROOT_DIR,
    load_tokens,
    get_root_css,
    escape_xml
)

DIST_DIR = ROOT_DIR / "distribution" / "repo-assets"
PREVIEWS_DIR = DIST_DIR / "social-previews"
HEADERS_DIR = DIST_DIR / "headers"

PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
HEADERS_DIR.mkdir(parents=True, exist_ok=True)

REPOS = [
    {
        "name": "NixManagerPro",
        "tagline": "Asynchronous Desktop Client for Nix Package Manager",
        "desc": "Universal channels manager, Nix Flakes profile support, and zero-drift package orchestration on Ubuntu/Debian.",
        "badges": ["NIXOS", "PYTHON 3.11", "ASYNCIO", "SYSTEMD"],
        "icon": "❄️",
        "accent": "var(--accent-gold)"
    },
    {
        "name": "next-session-guard",
        "tagline": "Enterprise Multi-Device Session Management & SOC",
        "desc": "Real-time SSE session revocation, session hijacking defense, and Telegram SOC alerting for Next.js, Prisma & Drizzle.",
        "badges": ["NEXT.JS 15", "TYPESCRIPT", "SSE REVOCATION", "SECURITY"],
        "icon": "🛡️",
        "accent": "var(--accent-lapis)"
    },
    {
        "name": "git-smart-sync",
        "tagline": "Multi-Branch Git Sync & Divergence Protection",
        "desc": "Seamless branch presets, multi-remote synchronization, and silent overwrite prevention inside VS Code & Antigravity.",
        "badges": ["VS CODE", "TYPESCRIPT", "GIT ENGINE", "PRODUCTIVITY"],
        "icon": "⚡",
        "accent": "var(--accent-teal)"
    },
    {
        "name": "My-portfolio",
        "tagline": "Material Design 3 Architecture & Portfolio Engine",
        "desc": "Personal portfolio replicating Google's M3 system with Next.js App Router, Firebase, Telegram Bot API, and zero-latency SSR.",
        "badges": ["MATERIAL DESIGN 3", "NEXT.JS", "FIREBASE", "REACT"],
        "icon": "🎨",
        "accent": "var(--term-purple)"
    }
]


def generate_og_svg(repo: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    root_css = get_root_css(tokens)
    w, h = 1280, 640
    
    name = escape_xml(repo["name"])
    tagline = escape_xml(repo["tagline"])
    desc = escape_xml(repo["desc"])
    icon = repo["icon"]
    accent = repo["accent"]
    
    badge_elements = []
    bx = 80
    for b in repo["badges"]:
        bw = len(b) * 11 + 24
        badge_elements.append(f"""
        <rect x="{bx}" y="480" width="{bw}" height="36" rx="6" fill="var(--card-elevated)" stroke="var(--border-accent)" stroke-width="1" />
        <text x="{bx + bw/2}" y="503" text-anchor="middle" font-family="var(--font-mono)" font-size="13" font-weight="700" fill="var(--accent-gold)">{escape_xml(b)}</text>
        """)
        bx += bw + 14

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{name} Social Preview">
  <title>{name} - OpenGraph Social Preview</title>
  <desc>{tagline}. {desc} Authored by Mohamed Ayman (@MikeeeDeV).</desc>
  <style>
    {root_css}
    .og-card {{
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 2px;
    }}
    .og-title {{
      font-family: var(--font-mono);
      font-size: 54px;
      font-weight: 700;
      letter-spacing: 2px;
      fill: var(--text-primary);
    }}
    .og-tagline {{
      font-family: var(--font-sans);
      font-size: 26px;
      font-weight: 600;
      fill: {accent};
    }}
    .og-desc {{
      font-family: var(--font-sans);
      font-size: 20px;
      line-height: 32px;
      fill: var(--text-secondary);
    }}
    .og-meta {{
      font-family: var(--font-mono);
      font-size: 16px;
      fill: var(--text-muted);
    }}
    .watermark-rosette {{
      opacity: 0.15;
    }}
  </style>

  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" class="og-card" />

  <!-- Background Geometry Watermark -->
  <g transform="translate({w - 240}, {h / 2})" class="watermark-rosette">
    <circle cx="0" cy="0" r="220" fill="none" stroke="var(--accent-gold)" stroke-width="2" stroke-dasharray="6,6" />
    <circle cx="0" cy="0" r="160" fill="none" stroke="var(--accent-teal)" stroke-width="2" />
    <polygon points="0,-140 40,-40 140,0 40,40 0,140 -40,40 -140,0 -40,-40" fill="none" stroke="var(--accent-lapis)" stroke-width="3" />
    <polygon points="-100,-100 0,-60 100,-100 60,0 100,100 0,60 -100,100 -60,0" fill="none" stroke="var(--accent-gold)" stroke-width="2.5" />
  </g>

  <!-- Top Metadata Bar -->
  <g transform="translate(80, 80)">
    <text x="0" y="0" class="og-meta">GITHUB REPOSITORY // MOHAMED AYMAN (@MikeeeDeV)</text>
    <text x="{w - 160}" y="0" class="og-meta" text-anchor="end" fill="var(--accent-teal)">SYSTEMS &amp; ARCHITECTURE</text>
  </g>

  <!-- Title & Icon -->
  <g transform="translate(80, 190)">
    <text x="0" y="0" font-size="48">{icon}</text>
    <text x="70" y="-4" class="og-title">{name}</text>
  </g>

  <!-- Tagline -->
  <g transform="translate(80, 260)">
    <text x="0" y="0" class="og-tagline">{tagline}</text>
  </g>

  <!-- Description -->
  <g transform="translate(80, 320)">
    <text x="0" y="0" class="og-desc">{desc}</text>
  </g>

  <!-- Badges -->
  <g>
    {''.join(badge_elements)}
  </g>

  <!-- Bottom Attribution -->
  <g transform="translate(80, 580)">
    <text x="0" y="0" class="og-meta">Designed with Kemet Nocturne Design System • 100% Deterministic</text>
    <text x="{w - 160}" y="0" class="og-meta" text-anchor="end" fill="var(--accent-gold)">GAWDAH ENGINEERING</text>
  </g>
</svg>"""
    return svg


def generate_header_markdown(repo: Dict[str, Any]) -> str:
    name = repo["name"]
    tagline = repo["tagline"]
    desc = repo["desc"]
    slug = name.lower()
    
    return f"""<!-- Header generated by MikeeeDeV Profile Engine (Kemet Nocturne) -->
<div align="center">

# `{name}`
### {tagline}

![{name} Social Preview](https://raw.githubusercontent.com/MikeeeDeV/MikeeeDeV/main/distribution/repo-assets/social-previews/{slug}-preview.svg)

<p align="center">
  <img src="https://img.shields.io/badge/Architecture-Deterministic-gold?style=flat-square" alt="Architecture" />
  <img src="https://img.shields.io/badge/Author-Mohamed%20Ayman%20(@MikeeeDeV)-blue?style=flat-square" alt="Author" />
  <img src="https://img.shields.io/badge/License-MIT-teal?style=flat-square" alt="License" />
</p>

> {desc}

</div>

---
"""


def main() -> None:
    tokens = load_tokens()
    
    for repo in REPOS:
        slug = repo["name"].lower()
        # 1. Preview SVG
        svg_code = generate_og_svg(repo, tokens)
        svg_path = PREVIEWS_DIR / f"{slug}-preview.svg"
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_code)
        print(f"[OK] Generated {svg_path} ({len(svg_code.encode('utf-8'))} bytes)")
        
        # 2. Header Markdown
        md_code = generate_header_markdown(repo)
        md_path = HEADERS_DIR / f"{repo['name']}-HEADER.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_code)
        print(f"[OK] Generated {md_path}")
        
    # Write distribution README
    dist_readme = DIST_DIR / "README.md"
    with open(dist_readme, "w", encoding="utf-8") as f:
        f.write("""# Repository Assets & Social Previews

These assets are generated by the profile design system (`design/tokens.json`) to unify branding across Mohamed Ayman's repositories:

- `social-previews/`: 1280x640 OpenGraph SVG cards ready to be set in GitHub repository settings (**Settings > General > Social preview**).
- `headers/`: Standardized, clean README header markdown blocks for:
  - `NixManagerPro`
  - `next-session-guard`
  - `git-smart-sync`
  - `My-portfolio`

Generated deterministically with zero third-party dependencies.
""")
    print(f"[OK] Generated {dist_readme}")


if __name__ == "__main__":
    main()
