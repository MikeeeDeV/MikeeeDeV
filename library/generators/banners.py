"""
library/generators/banners.py - 40 Algorithmic Geometric Banners.
Each banner renders a responsive 960x240 header card with algorithmic centerpieces,
circuit traces, callouts, and multi-theme support.
"""

import html
import math
from typing import Dict, List, Any
from library.engine.svg_builder import SVGBuilder
from library.engine.color_palettes import get_palette, list_palette_ids
from library.engine.geometry import (
    rosette_path, hypocycloid_path, lissajous_path,
    phyllotaxis_points, tesseract_projected_edges, circuit_trace_path
)

BANNER_PRESETS: List[Dict[str, Any]] = [
    {"id": "kemet-nocturne-rosette", "title": "Kemet 8-Pointed Rosette", "theme": "kemet_nocturne", "type": "rosette", "petals": 8},
    {"id": "cyberpunk-matrix-hex", "title": "Cyberpunk Neon Matrix", "theme": "cyberpunk_2077", "type": "hex_grid", "petals": 6},
    {"id": "nordic-constellation", "title": "Nordic Frost Starfield", "theme": "nord_frost", "type": "constellation", "petals": 12},
    {"id": "dracula-astrolabe", "title": "Dracula Cryptographic Astrolabe", "theme": "dracula", "type": "astrolabe", "petals": 16},
    {"id": "tokyo-neon-sine", "title": "Tokyo Neon Sine Harmonics", "theme": "tokyo_night", "type": "lissajous", "petals": 5},
    {"id": "solarized-tesseract", "title": "Solarized 4D Hypercube", "theme": "solarized_dark", "type": "tesseract", "petals": 4},
    {"id": "emerald-circuit-bus", "title": "Emerald Logic Bus", "theme": "emerald_matrix", "type": "circuits", "petals": 8},
    {"id": "amber-crt-scanline", "title": "Amber CRT Vector Horizon", "theme": "amber_crt", "type": "crt_grid", "petals": 8},
    {"id": "rose-pine-mandala", "title": "Rosé Pine Sacred Mandala", "theme": "rose_pine", "type": "mandala", "petals": 10},
    {"id": "monokai-flow-mesh", "title": "Monokai Pro Polytope Mesh", "theme": "monokai_pro", "type": "mesh", "petals": 7},
    
    {"id": "golden-ratio-spiral", "title": "Fibonacci Golden Spiral", "theme": "kemet_nocturne", "type": "phyllotaxis", "petals": 14},
    {"id": "penrose-tiling-grid", "title": "Penrose Quasi-Lattice", "theme": "cyberpunk_2077", "type": "penrose", "petals": 5},
    {"id": "sacred-octagon-shrine", "title": "Sacred Octagon Shrine", "theme": "kemet_nocturne", "type": "rosette", "petals": 8},
    {"id": "warp-speed-hypergrid", "title": "Warp Speed Starburst", "theme": "tokyo_night", "type": "warp", "petals": 24},
    {"id": "quantum-field-ripples", "title": "Quantum Wave Ripple", "theme": "nord_frost", "type": "lissajous", "petals": 9},
    {"id": "isometric-cube-lattice", "title": "Isometric Cube Matrix", "theme": "solarized_dark", "type": "iso_cubes", "petals": 6},
    {"id": "cyber-wireframe-horizon", "title": "Cyber Synthwave Horizon", "theme": "cyberpunk_2077", "type": "wire_horizon", "petals": 8},
    {"id": "hypocycloid-gear-star", "title": "Hypocycloid Chrono Star", "theme": "monokai_pro", "type": "hypocycloid", "petals": 12},
    {"id": "torus-wire-knot", "title": "Trefoil Torus Knot", "theme": "dracula", "type": "lissajous", "petals": 3},
    {"id": "delaunay-triangulation", "title": "Delaunay Vector Web", "theme": "emerald_matrix", "type": "mesh", "petals": 15},
    
    {"id": "hyperbolic-poincare-disk", "title": "Poincaré Hyperbolic Disk", "theme": "rose_pine", "type": "astrolabe", "petals": 8},
    {"id": "chladni-resonance-plate", "title": "Chladni Harmonic Modal", "theme": "amber_crt", "type": "chladni", "petals": 6},
    {"id": "lorenz-attractor-orbit", "title": "Lorenz Strange Attractor", "theme": "tokyo_night", "type": "lorenz", "petals": 2},
    {"id": "sierpinski-vector-gasket", "title": "Sierpinski Fractal Gasket", "theme": "kemet_nocturne", "type": "sierpinski", "petals": 3},
    {"id": "lissajous-3d-harmonics", "title": "Lissajous Resonance Knot", "theme": "dracula", "type": "lissajous", "petals": 7},
    {"id": "hexagonal-nexus-hive", "title": "Honeycomb Nexus Hive", "theme": "cyberpunk_2077", "type": "hex_grid", "petals": 18},
    {"id": "nile-circuit-archway", "title": "Nile Digital Archway", "theme": "kemet_nocturne", "type": "circuits", "petals": 10},
    {"id": "archimedean-vortex", "title": "Archimedean Dual Vortex", "theme": "monokai_pro", "type": "phyllotaxis", "petals": 16},
    {"id": "quantum-spin-network", "title": "Quantum Spin Lattice", "theme": "nord_frost", "type": "mesh", "petals": 8},
    {"id": "mobius-strip-ribbon", "title": "Möbius Topology Ribbon", "theme": "rose_pine", "type": "lissajous", "petals": 4},
    
    {"id": "klein-bottle-contour", "title": "Klein Manifold Contour", "theme": "tokyo_night", "type": "astrolabe", "petals": 12},
    {"id": "hypercube-shadow-cast", "title": "Orthogonal 4D Projection", "theme": "solarized_dark", "type": "tesseract", "petals": 8},
    {"id": "calabi-yau-manifold", "title": "Calabi-Yau String Compact", "theme": "dracula", "type": "hypocycloid", "petals": 10},
    {"id": "holographic-prism-beam", "title": "Holographic Prism Beam", "theme": "cyberpunk_2077", "type": "warp", "petals": 14},
    {"id": "synaptic-neural-web", "title": "Synaptic Neural Matrix", "theme": "emerald_matrix", "type": "mesh", "petals": 20},
    {"id": "vector-radar-compass", "title": "Navigational Vector Rose", "theme": "kemet_nocturne", "type": "rosette", "petals": 16},
    {"id": "infinity-oscillator", "title": "Infinity Lemniscate Wave", "theme": "amber_crt", "type": "lissajous", "petals": 2},
    {"id": "stellar-pulsar-burst", "title": "Stellar Pulsar Core", "theme": "tokyo_night", "type": "constellation", "petals": 24},
    {"id": "celtic-vector-knotwork", "title": "Interlocking Vector Ribbon", "theme": "nord_frost", "type": "rosette", "petals": 8},
    {"id": "kemet-pharaonic-sun", "title": "Pharaonic Solar Disc & Wings", "theme": "kemet_nocturne", "type": "mandala", "petals": 12},
]

def generate_banner_svg(preset_id: str, theme_override: str = None) -> str:
    preset = next((p for p in BANNER_PRESETS if p["id"] == preset_id), BANNER_PRESETS[0])
    theme = theme_override or preset["theme"]
    title = html.escape(preset["title"].upper())
    p_type = preset["type"]
    petals = preset["petals"]
    
    w, h = 960, 240
    builder = SVGBuilder(w, h, theme, title=f"{preset['title']} - VectorForge Banner", desc=f"Algorithmic banner preset {preset_id}")
    
    builder.add_custom_css("""
      .card-bg { fill: var(--vf-card); stroke: var(--vf-border); stroke-width: 1; }
      .grid-line { stroke: var(--vf-border); stroke-width: 0.5; opacity: 0.4; }
      .glow-layer { filter: drop-shadow(0 0 10px var(--vf-glow)); }
      .badge-bg { fill: var(--vf-bg); stroke: var(--vf-border); stroke-width: 1; }
      .title-text { font-family: var(--vf-font-sans); font-size: 24px; font-weight: 800; fill: var(--vf-text); letter-spacing: -0.5px; }
      .subtitle-text { font-family: var(--vf-font-mono); font-size: 12px; fill: var(--vf-text-muted); letter-spacing: 0.5px; }
      .tag-text { font-family: var(--vf-font-mono); font-size: 10px; font-weight: 700; fill: var(--vf-accent-1); }
      .center-stroke { stroke: var(--vf-accent-1); stroke-width: 1.5; fill: none; }
      .center-sub { stroke: var(--vf-accent-2); stroke-width: 1.0; fill: none; opacity: 0.75; }
      .center-dot { fill: var(--vf-accent-3); }
      .circuit-line { stroke: var(--vf-border); stroke-width: 1; fill: none; }
    """)
    
    # Outer frame
    builder.add_body(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" class="card-bg" />')
    
    # Background Grid pattern
    grid_lines = []
    for gx in range(40, w, 60):
        grid_lines.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{h}" class="grid-line" />')
    for gy in range(30, h, 30):
        grid_lines.append(f'<line x1="0" y1="{gy}" x2="{w}" y2="{gy}" class="grid-line" />')
    builder.add_body(f'<g class="grid-layer">{"".join(grid_lines)}</g>')
    
    # Left Content block
    cx_art, cy_art = w - 170, h / 2
    
    # Circuit connecting left block to art centerpiece
    circuits = []
    for i, offset_y in enumerate([-40, 0, 40]):
        trace = circuit_trace_path(420, cy_art + offset_y, cx_art - 100, cy_art + offset_y * 0.8, 30 + i * 15)
        circuits.append(f'<path d="{trace}" class="circuit-line" />')
        circuits.append(f'<circle cx="{420}" cy="{cy_art + offset_y}" r="2.5" fill="var(--vf-accent-2)" opacity="0.6" />')
    builder.add_body(f'<g>{"".join(circuits)}</g>')
    
    # Text metadata
    builder.add_body(f"""
    <g transform="translate(48, 48)">
      <!-- Category & Status Badge -->
      <rect x="0" y="0" width="170" height="22" rx="4" class="badge-bg" />
      <circle cx="10" cy="11" r="3.5" fill="var(--vf-accent-1)" />
      <text x="22" y="15" class="tag-text">VECTORFORGE // BANNERS</text>
      
      <!-- Main Title -->
      <text x="0" y="56" class="title-text">{title}</text>
      
      <!-- Subtitle & Specs -->
      <text x="0" y="82" class="subtitle-text">Deterministic 1-of-1 SVG Canvas • Seed 0x{abs(hash(preset_id)) % 0xFFFFFF:06X}</text>
      <text x="0" y="104" font-family="var(--vf-font-mono)" font-size="11" fill="var(--vf-text-muted)">Theme: {theme} • Resolution: 960x240 • Zero Runtime Dependency</text>
      
      <!-- Badges row -->
      <g transform="translate(0, 122)">
        <rect x="0" y="0" width="80" height="20" rx="3" fill="var(--vf-bg)" stroke="var(--vf-border)" />
        <text x="40" y="14" text-anchor="middle" font-family="var(--vf-font-mono)" font-size="10" fill="var(--vf-accent-2)">STANDALONE</text>
        <rect x="90" y="0" width="70" height="20" rx="3" fill="var(--vf-bg)" stroke="var(--vf-border)" />
        <text x="125" y="14" text-anchor="middle" font-family="var(--vf-font-mono)" font-size="10" fill="var(--vf-accent-1)">A11Y READY</text>
        <rect x="170" y="0" width="60" height="20" rx="3" fill="var(--vf-bg)" stroke="var(--vf-border)" />
        <text x="200" y="14" text-anchor="middle" font-family="var(--vf-font-mono)" font-size="10" fill="var(--vf-accent-3)">&lt; 15 KB</text>
      </g>
    </g>
    """)
    
    # Centerpiece Art based on p_type
    art_elements = []
    if p_type == "rosette" or p_type == "mandala":
        r_outer = 78
        path_outer = rosette_path(cx_art, cy_art, r_outer, petals=petals, pointiness=0.48)
        path_inner = rosette_path(cx_art, cy_art, r_outer * 0.6, petals=petals, pointiness=0.6)
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="{r_outer + 12}" fill="none" stroke="var(--vf-border)" stroke-dasharray="4 4" />')
        art_elements.append(f'<path d="{path_outer}" class="center-stroke glow-layer" />')
        art_elements.append(f'<path d="{path_inner}" class="center-sub" />')
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="6" fill="var(--vf-accent-1)" />')
    elif p_type == "tesseract":
        edges = tesseract_projected_edges(cx_art, cy_art, size=68)
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="90" fill="none" stroke="var(--vf-border)" stroke-dasharray="3 3" />')
        for x1, y1, x2, y2 in edges:
            art_elements.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="center-stroke" />')
        for x1, y1, _, _ in edges[:8]:
            art_elements.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="3" fill="var(--vf-accent-2)" />')
    elif p_type == "phyllotaxis":
        pts = phyllotaxis_points(cx_art, cy_art, n_points=84, c=7.2)
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="86" fill="none" stroke="var(--vf-border)" />')
        for px, py, pr in pts:
            art_elements.append(f'<circle cx="{px}" cy="{py}" r="{pr}" fill="var(--vf-accent-1)" opacity="0.85" />')
    elif p_type == "lissajous" or p_type == "lorenz":
        l_path = lissajous_path(cx_art, cy_art, A=76, B=64, a=petals, b=petals-1 if petals>2 else 3, delta=math.pi/4)
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="88" fill="none" stroke="var(--vf-border)" />')
        art_elements.append(f'<path d="{l_path}" class="center-stroke glow-layer" />')
    elif p_type == "hypocycloid":
        h_path = hypocycloid_path(cx_art, cy_art, R=76, r=24, d=38)
        art_elements.append(f'<path d="{h_path}" class="center-stroke glow-layer" />')
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="78" fill="none" stroke="var(--vf-accent-2)" stroke-dasharray="2 4" />')
    else:  # hex_grid, constellation, circuits, warp, mesh, etc.
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="82" fill="none" stroke="var(--vf-border)" />')
        for i in range(petals):
            ang = (2 * math.pi * i) / petals
            x_tip = cx_art + 74 * math.cos(ang)
            y_tip = cy_art + 74 * math.sin(ang)
            art_elements.append(f'<line x1="{cx_art}" y1="{cy_art}" x2="{x_tip:.1f}" y2="{y_tip:.1f}" class="center-sub" />')
            art_elements.append(f'<circle cx="{x_tip:.1f}" cy="{y_tip:.1f}" r="4" fill="var(--vf-accent-1)" />')
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="18" fill="var(--vf-card)" stroke="var(--vf-accent-2)" stroke-width="2" />')
        art_elements.append(f'<circle cx="{cx_art}" cy="{cy_art}" r="6" fill="var(--vf-accent-3)" />')
        
    builder.add_body(f'<g class="art-layer">{"".join(art_elements)}</g>')
    
    return builder.build()
