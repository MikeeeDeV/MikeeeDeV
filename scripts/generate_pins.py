#!/usr/bin/env python3
"""
scripts/generate_pins.py - Generates 4 custom-styled SVG cards for featured pinned repos:
1. NixManagerPro
2. next-session-guard
3. git-smart-sync
4. My-portfolio
Replaces generic github-readme-stats with deterministic, high-craft cards.
"""

from pathlib import Path
from typing import Dict, Any, List

from common import (
    ASSETS_DIR,
    load_tokens,
    get_root_css,
    escape_xml,
    fetch_github_api,
    format_relative_time
)

PINS_DIR = ASSETS_DIR / "pins"
PINS_DIR.mkdir(parents=True, exist_ok=True)
USERNAME = "MikeeeDeV"

FEATURED_REPOS = [
    {
        "repo": "NixManagerPro",
        "badge_icon": "❄️",
        "custom_desc": "Asynchronous desktop client for Nix Package Manager on Ubuntu/Debian multi-user setups.",
        "primary_color": "var(--accent-gold)"
    },
    {
        "repo": "next-session-guard",
        "badge_icon": "🛡️",
        "custom_desc": "Multi-device session security, real-time SSE revocation, hijacking defense & SOC for Next.js.",
        "primary_color": "var(--accent-lapis)"
    },
    {
        "repo": "git-smart-sync",
        "badge_icon": "⚡",
        "custom_desc": "Multi-branch Git synchronization, branch presets, and divergence protection for VS Code.",
        "primary_color": "var(--accent-teal)"
    },
    {
        "repo": "My-portfolio",
        "badge_icon": "🎨",
        "custom_desc": "Material Design 3 portfolio system built with Next.js App Router, Firebase & Telegram API.",
        "primary_color": "var(--term-purple)"
    }
]


def generate_pin_svg(repo_meta: Dict[str, Any], tokens: Dict[str, Any]) -> str:
    repo_name = repo_meta["repo"]
    data = fetch_github_api(f"repos/{USERNAME}/{repo_name}", default={
        "name": repo_name,
        "stargazers_count": 2,
        "forks_count": 0,
        "language": "Python" if "Nix" in repo_name else "TypeScript",
        "pushed_at": "2026-10-18T23:31:53Z",
        "description": repo_meta["custom_desc"]
    })
    
    lang_data = fetch_github_api(f"repos/{USERNAME}/{repo_name}/languages", default={})
    if not lang_data:
        lang_data = {data.get("language", "TypeScript"): 1000}
        
    total_bytes = sum(lang_data.values()) or 1
    sorted_langs = sorted(lang_data.items(), key=lambda x: x[1], reverse=True)[:3]
    
    stars = data.get("stargazers_count", 0)
    forks = data.get("forks_count", 0)
    primary_lang = data.get("language") or (sorted_langs[0][0] if sorted_langs else "TypeScript")
    updated_str = format_relative_time(data.get("pushed_at") or data.get("updated_at") or "")
    
    # Description wrapping into 2 lines
    desc = repo_meta.get("custom_desc") or data.get("description") or "Production-grade engineering tool."
    words = desc.split()
    line1_words, line2_words = [], []
    cur_len = 0
    for w in words:
        if cur_len + len(w) < 42:
            line1_words.append(w)
            cur_len += len(w) + 1
        else:
            line2_words.append(w)
    line1 = " ".join(line1_words)
    line2 = " ".join(line2_words[:7]) + ("..." if len(line2_words) > 7 else "")
    
    root_css = get_root_css(tokens)
    w, h = 400, 160
    
    # Build mini language bar segments
    bar_w = 120
    cur_x = 0
    bar_rects = []
    colors_cycle = ["var(--accent-lapis)", "var(--accent-gold)", "var(--accent-teal)"]
    for idx, (l_name, b_count) in enumerate(sorted_langs):
        seg_w = max(4, int((b_count / total_bytes) * bar_w))
        c = colors_cycle[idx % len(colors_cycle)]
        bar_rects.append(f'<rect x="{cur_x}" y="0" width="{seg_w}" height="4" rx="2" fill="{c}" />')
        cur_x += seg_w + 1
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Pinned Repository {repo_name}">
  <title>{repo_name} - Featured Repository</title>
  <desc>{escape_xml(desc)}</desc>
  <style>
    {root_css}
    .pin-card {{
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 1px;
      transition: stroke 0.2s ease;
    }}
    .pin-title {{
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 700;
      fill: var(--text-primary);
    }}
    .pin-desc {{
      font-family: var(--font-sans);
      font-size: 12px;
      fill: var(--text-secondary);
      line-height: 16px;
    }}
    .pin-meta {{
      font-family: var(--font-mono);
      font-size: 11px;
      fill: var(--text-muted);
    }}
    .badge-icon {{
      font-size: 14px;
    }}
    .stat-label {{
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      fill: var(--text-secondary);
    }}
  </style>

  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" class="pin-card" />

  <!-- Card Top Header -->
  <g transform="translate(18, 24)">
    <!-- Icon & Title -->
    <text x="0" y="2" class="badge-icon">{repo_meta['badge_icon']}</text>
    <text x="24" y="2" class="pin-title">{escape_xml(repo_name)}</text>

    <!-- Star & Fork Metrics -->
    <g transform="translate({w - 110}, -4)">
      <text x="0" y="6" class="stat-label">★ {stars}</text>
      <text x="44" y="6" class="stat-label">⑂ {forks}</text>
    </g>
  </g>

  <!-- Description Body -->
  <g transform="translate(18, 56)">
    <text x="0" y="10" class="pin-desc">{escape_xml(line1)}</text>
    <text x="0" y="28" class="pin-desc">{escape_xml(line2)}</text>
  </g>

  <!-- Language Bar and Footer -->
  <g transform="translate(18, 126)">
    <!-- Primary Language -->
    <circle cx="4" cy="0" r="4" fill="{repo_meta['primary_color']}" />
    <text x="14" y="4" class="pin-meta">{escape_xml(primary_lang)}</text>

    <!-- Micro Language Stack -->
    <g transform="translate(120, -2)">
      {''.join(bar_rects)}
    </g>

    <!-- Updated Time -->
    <text x="{w - 40}" y="4" class="pin-meta" text-anchor="end">Synced {escape_xml(updated_str)}</text>
  </g>
</svg>"""
    return svg


def main() -> None:
    tokens = load_tokens()
    for repo_meta in FEATURED_REPOS:
        repo_slug = repo_meta["repo"].lower()
        out_file = PINS_DIR / f"{repo_slug}.svg"
        svg_code = generate_pin_svg(repo_meta, tokens)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(svg_code)
        print(f"[OK] Generated {out_file} ({len(svg_code.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
