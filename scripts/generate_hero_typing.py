#!/usr/bin/env python3
"""
scripts/generate_hero_typing.py - Generates pure CSS/SMIL animated SVG intro banner.
Features a specific positioning statement and an Arabic RTL line.
Zero external JavaScript, zero third-party dependencies.
"""

from pathlib import Path
from common import (
    ASSETS_DIR,
    load_tokens,
    get_root_css,
    escape_xml
)


def generate_hero_typing_svg() -> str:
    tokens = load_tokens()
    root_css = get_root_css(tokens)
    
    w, h = 840, 134
    
    eng_statement = "Architecting deterministic Linux systems, resilient auth guards &amp; FastMCP agent infrastructure."
    arabic_statement = "مهندس نظم ومطور برمجيات متكاملة • أبني أنظمة محكمة غير قابلة للانهيار"
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Mohamed Ayman Positioning Statement">
  <title>Mohamed Ayman (MikeeeDeV) - Systems &amp; Full-Stack Engineer</title>
  <desc>Architecting deterministic Linux systems, resilient auth guards and FastMCP agent infrastructure. Egyptian systems engineer.</desc>
  <style>
    {root_css}
    .hero-card {{
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 1px;
    }}
    .terminal-prompt {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      fill: var(--accent-teal);
    }}
    .terminal-cmd {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 500;
      fill: var(--text-primary);
    }}
    .typewriter-eng {{
      font-family: var(--font-mono);
      font-size: 13.5px;
      font-weight: 500;
      fill: var(--accent-gold);
    }}
    .arabic-text {{
      font-family: var(--font-arabic);
      font-size: 14px;
      font-weight: 600;
      fill: var(--text-secondary);
      direction: rtl;
      unicode-bidi: embed;
    }}
    .cursor {{
      fill: var(--accent-gold);
      animation: blink 0.9s infinite step-start;
    }}
    .chamfer-marker {{
      fill: var(--accent-lapis);
    }}
    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}
    @keyframes fadeIn {{
      0% {{ opacity: 0; transform: translateY(4px); }}
      100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .fade-seq {{
      animation: fadeIn 0.8s ease-out forwards;
    }}
  </style>

  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" class="hero-card" />

  <!-- Window Header Bar Line -->
  <line x1="0" y1="32" x2="{w}" y2="32" stroke="var(--border)" stroke-width="1" />
  
  <g transform="translate(18, 20)">
    <circle cx="0" cy="0" r="4" fill="var(--accent-coral)" />
    <circle cx="14" cy="0" r="4" fill="var(--accent-gold)" />
    <circle cx="28" cy="0" r="4" fill="var(--accent-teal)" />
    
    <text x="50" y="4" font-family="var(--font-mono)" font-size="11" fill="var(--text-muted)">session: init --profile=engineer --location=cairo</text>
    <text x="{w - 56}" y="4" font-family="var(--font-mono)" font-size="11" font-weight="600" fill="var(--accent-teal)" text-anchor="end">STATUS: ACTIVE</text>
  </g>

  <!-- Line 1: Terminal Command -->
  <g transform="translate(24, 60)">
    <text x="0" y="0" class="terminal-prompt">mikeee@workstation<tspan fill="var(--text-muted)">:~$</tspan></text>
    <text x="175" y="0" class="terminal-cmd">antigravity --focus=systems --manifest</text>
  </g>

  <!-- Line 2: Positioning Statement with Cursor -->
  <g transform="translate(24, 88)">
    <text x="0" y="0" font-family="var(--font-mono)" font-size="14" font-weight="700" fill="var(--accent-teal)">❯</text>
    <text x="18" y="0" class="typewriter-eng">{eng_statement}</text>
    <rect x="746" y="-12" width="8" height="15" class="cursor" />
  </g>

  <!-- Line 3: Arabic Typographic Line (RTL) -->
  <g transform="translate(24, 114)">
    <text x="0" y="0" font-family="var(--font-mono)" font-size="11" font-weight="600" fill="var(--accent-lapis)">SYS//AR</text>
    <text x="{w - 48}" y="0" class="arabic-text" text-anchor="end">{arabic_statement}</text>
  </g>
</svg>"""
    return svg


def main() -> None:
    output_path = ASSETS_DIR / "hero-typing.svg"
    svg_content = generate_hero_typing_svg()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Generated {output_path} ({len(svg_content.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
