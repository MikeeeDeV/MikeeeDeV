#!/usr/bin/env python3
"""
scripts/generate_cipher_banner.py - Generates an authentic, commit-seeded Egyptian geometric banner.
Uses the latest git commit SHA as a seed to mathematically evolve an 8-pointed rosette & Nile circuit matrix.
100% deterministic, zero external dependencies, pure SVG.
"""

import math
import subprocess
from pathlib import Path
from typing import Tuple, List

from common import (
    ASSETS_DIR,
    load_tokens,
    get_root_css,
    escape_xml
)


def get_current_sha() -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except Exception:
        pass
    return "a7d4e028b19f3c5e"


class SeededRNG:
    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF

    def next(self) -> float:
        self.state = (1664525 * self.state + 1013904223) & 0xFFFFFFFF
        return self.state / 0xFFFFFFFF


def generate_rosette_paths(cx: float, cy: float, base_r: float, angle_offset: float) -> List[str]:
    elements = []
    points_count = 8
    
    # Concentric rings
    elements.append(
        f'<circle cx="{cx}" cy="{cy}" r="{base_r * 1.25:.1f}" fill="none" stroke="var(--border)" stroke-width="1" stroke-dasharray="3,4" opacity="0.6" />'
    )
    elements.append(
        f'<circle cx="{cx}" cy="{cy}" r="{base_r:.1f}" fill="none" stroke="var(--accent-teal)" stroke-width="1.2" opacity="0.4" />'
    )
    elements.append(
        f'<circle cx="{cx}" cy="{cy}" r="{base_r * 0.45:.1f}" fill="none" stroke="var(--accent-gold)" stroke-width="1.2" opacity="0.8" />'
    )
    
    # 2 interpenetrating squares (8-pointed star)
    sq1_pts = []
    sq2_pts = []
    for i in range(4):
        ang1 = math.radians(angle_offset + i * 90)
        ang2 = math.radians(angle_offset + 45 + i * 90)
        r = base_r * 0.88
        sq1_pts.append(f"{cx + r * math.cos(ang1):.1f},{cy + r * math.sin(ang1):.1f}")
        sq2_pts.append(f"{cx + r * math.cos(ang2):.1f},{cy + r * math.sin(ang2):.1f}")
        
    elements.append(
        f'<polygon points="{" ".join(sq1_pts)}" fill="none" stroke="var(--accent-gold)" stroke-width="1.5" opacity="0.9" />'
    )
    elements.append(
        f'<polygon points="{" ".join(sq2_pts)}" fill="none" stroke="var(--accent-lapis)" stroke-width="1.2" opacity="0.8" />'
    )
    
    # Radial diamond nodes
    for i in range(points_count):
        ang = math.radians(angle_offset + i * (360 / points_count))
        nx = cx + base_r * 1.12 * math.cos(ang)
        ny = cy + base_r * 1.12 * math.sin(ang)
        elements.append(
            f'<rect x="{nx - 3.5:.1f}" y="{ny - 3.5:.1f}" width="7" height="7" transform="rotate(45 {nx:.1f} {ny:.1f})" fill="var(--accent-gold)" />'
        )
        elements.append(
            f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="var(--border-accent)" stroke-width="0.8" opacity="0.6" />'
        )
        
    elements.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="var(--accent-gold)" />')
    return elements


def generate_nile_circuits(rng: SeededRNG, w: int, h: int) -> List[str]:
    paths = []
    for _ in range(5):
        y_start = int(45 + rng.next() * (h - 90))
        pts = [(620, y_start)]
        x = 620
        y = y_start
        for _ in range(3):
            dx = -(80 + rng.next() * 110)
            dy = (rng.next() - 0.5) * 45
            x = max(70, x + dx)
            y = max(35, min(h - 35, y + dy))
            pts.append((x, y))
            
        d_str = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
        for pt in pts[1:]:
            d_str += f" L {pt[0]:.1f} {pt[1]:.1f}"
            
        color = "var(--accent-teal)" if rng.next() > 0.5 else "var(--accent-lapis)"
        paths.append(
            f'<path d="{d_str}" fill="none" stroke="{color}" stroke-width="1" opacity="0.32" stroke-dasharray="4,4" />'
        )
        last_x, last_y = pts[-1]
        paths.append(
            f'<circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="2.5" fill="{color}" opacity="0.75" />'
        )
    return paths


def generate_cipher_banner_svg() -> str:
    tokens = load_tokens()
    root_css = get_root_css(tokens)
    sha = get_current_sha()
    
    seed_val = int(sha[:8], 16)
    rng = SeededRNG(seed_val)
    angle_offset = (seed_val % 360) / 4.0
    
    w, h = 980, 240
    rosette_cx = w - 170
    rosette_cy = h / 2
    rosette_r = 82
    
    rosette_elements = generate_rosette_paths(rosette_cx, rosette_cy, rosette_r, angle_offset)
    circuit_elements = generate_nile_circuits(rng, w, h)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="{h}" role="img" aria-label="Mohamed Ayman Generative Geometric Banner">
  <title>Mohamed Ayman (@MikeeeDeV) - Systems Engineer Banner</title>
  <desc>Generative Egyptian geometric rosette and circuit matrix seeded by git commit hash 0x{sha[:8]}.</desc>
  <style>
    {root_css}
    .banner-frame {{
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 1px;
    }}
    .inner-panel {{
      fill: var(--card-elevated);
      stroke: var(--border-accent);
      stroke-width: 1px;
    }}
    .kemet-name {{
      font-family: var(--font-mono);
      font-size: 34px;
      font-weight: 700;
      letter-spacing: 4px;
      fill: var(--text-primary);
    }}
    .kemet-role {{
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 1.5px;
      fill: var(--accent-gold);
    }}
    .kemet-tagline {{
      font-family: var(--font-sans);
      font-size: 13.5px;
      fill: var(--text-secondary);
    }}
    .seed-tag {{
      font-family: var(--font-mono);
      font-size: 10.5px;
      fill: var(--accent-teal);
      letter-spacing: 1px;
    }}
    .arabic-watermark {{
      font-family: var(--font-arabic);
      font-size: 22px;
      font-weight: 700;
      fill: var(--border-accent);
      opacity: 0.22;
    }}
    .badge-pill {{
      fill: var(--card-elevated);
      stroke: var(--border-accent);
      stroke-width: 1px;
    }}
    .badge-text {{
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 600;
      fill: var(--accent-lapis);
    }}
    .glow-pulse {{
      animation: banner-pulse 3s infinite ease-in-out;
    }}
    @keyframes banner-pulse {{
      0%, 100% {{ opacity: 0.95; }}
      50% {{ opacity: 0.45; }}
    }}
  </style>

  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" class="banner-frame" />

  <!-- Arabic Watermark (Clean subtle placement) -->
  <text x="{w - 360}" y="48" class="arabic-watermark" text-anchor="end" direction="rtl" xml:lang="ar">محمد أيمن • مهندس نظم وبرمجيات</text>

  <!-- Nile Circuit Traces -->
  <g>
    {''.join(circuit_elements)}
  </g>

  <!-- Left Content Branding -->
  <g transform="translate(42, 54)">
    <!-- Header Seed Indicator -->
    <g transform="translate(0, 0)">
      <rect x="0" y="-12" width="240" height="22" rx="4" class="inner-panel" />
      <circle cx="10" cy="-1" r="3.5" fill="var(--accent-teal)" class="glow-pulse" />
      <text x="22" y="3" class="seed-tag">CIPHER SEED: 0x{sha[:8]} // DETERMINISTIC</text>
    </g>

    <!-- Name -->
    <text x="0" y="46" class="kemet-name">MOHAMED AYMAN</text>
    
    <!-- Title -->
    <text x="0" y="74" class="kemet-role">TECHNICAL TEAM LEADER @ GAWDAH • SYSTEMS &amp; FULL-STACK</text>
    
    <!-- Engineering Focus Statement -->
    <text x="0" y="100" class="kemet-tagline">Architecting Zero-Drift Linux Tooling, Next.js Security Guards &amp; FastMCP AI Agents</text>

    <!-- Stack Badges -->
    <g transform="translate(0, 120)">
      <rect x="0" y="0" width="84" height="22" rx="3" class="badge-pill" />
      <text x="42" y="15" text-anchor="middle" class="badge-text">❄️ NIXOS</text>

      <rect x="94" y="0" width="98" height="22" rx="3" class="badge-pill" />
      <text x="143" y="15" text-anchor="middle" class="badge-text">⚡ FASTMCP</text>

      <rect x="202" y="0" width="102" height="22" rx="3" class="badge-pill" />
      <text x="253" y="15" text-anchor="middle" class="badge-text">🐍 PYTHON</text>

      <rect x="314" y="0" width="112" height="22" rx="3" class="badge-pill" />
      <text x="370" y="15" text-anchor="middle" class="badge-text">🛡️ NEXT.JS AUTH</text>
    </g>
  </g>

  <!-- Right Geometric 8-Point Rosette -->
  <g id="rosette">
    {''.join(rosette_elements)}
  </g>

  <!-- Architectural Corner Brackets (Egyptian Masonry Chamfers) -->
  <g stroke="var(--accent-gold)" stroke-width="1.5" fill="none">
    <path d="M 12 24 L 12 12 L 24 12" />
    <path d="M {w - 24} 12 L {w - 12} 12 L {w - 12} 24" />
    <path d="M 12 {h - 24} L 12 {h - 12} L 24 {h - 12}" />
    <path d="M {w - 24} {h - 12} L {w - 12} {h - 12} L {w - 12} {h - 24}" />
  </g>
</svg>"""
    return svg


def main() -> None:
    output_path = ASSETS_DIR / "cipher-banner.svg"
    svg_content = generate_cipher_banner_svg()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[OK] Generated {output_path} ({len(svg_content.encode('utf-8'))} bytes)")


if __name__ == "__main__":
    main()
