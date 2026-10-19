"""
library/generators/skylines.py - 30 Contribution Horizons & Telemetry Skylines.
Renders 53-week skyline profiles, mountain ridges, cityscapes, and audio spectrograms.
"""

import html
import math
from typing import Dict, List, Any
from library.engine.svg_builder import SVGBuilder
from library.engine.geometry import wave_spectrogram_points

SKYLINE_PRESETS: List[Dict[str, Any]] = [
    {"id": "nile-horizon-skyline", "title": "The Nile Horizon", "theme": "kemet_nocturne", "style": "nile"},
    {"id": "cyberpunk-megacity-blocks", "title": "Night City Megablocks", "theme": "cyberpunk_2077", "style": "city"},
    {"id": "tokyo-audio-equalizer", "title": "Tokyo Club Equalizer", "theme": "tokyo_night", "style": "spectrogram"},
    {"id": "alpine-mountain-peaks", "title": "Alpine Glacial Ridge", "theme": "nord_frost", "style": "mountain"},
    {"id": "nordic-fjord-depths", "title": "Nordic Fjord Depth Sounding", "theme": "nord_frost", "style": "sonar"},
    {"id": "audio-mastering-spectrogram", "title": "Studio Mastering Spectrum", "theme": "monokai_pro", "style": "spectrogram"},
    {"id": "binary-waterfall-stream", "title": "Matrix Binary Waterfall", "theme": "emerald_matrix", "style": "waterfall"},
    {"id": "sine-wave-harmonic-stack", "title": "Harmonic Sine Oscillator", "theme": "amber_crt", "style": "sine"},
    {"id": "cosmic-constellation-chart", "title": "Cosmic Nebular Ridge", "theme": "dracula", "style": "mountain"},
    {"id": "circuit-board-trace-horizon", "title": "PCB Logic Trace Skyline", "theme": "emerald_matrix", "style": "circuit"},
    
    {"id": "dracula-transylvania-towers", "title": "Gothic Castle Spires", "theme": "dracula", "style": "city"},
    {"id": "monokai-matrix-waterfall", "title": "Monokai Syntax Cascade", "theme": "monokai_pro", "style": "waterfall"},
    {"id": "pyramids-of-giza-silhouette", "title": "Pyramids of Giza Alignment", "theme": "kemet_nocturne", "style": "pyramids"},
    {"id": "cairo-tower-nightline", "title": "Cairo Corniche Nightline", "theme": "kemet_nocturne", "style": "city"},
    {"id": "manhattan-grid-skyline", "title": "Manhattan Highline Blocks", "theme": "solarized_dark", "style": "city"},
    {"id": "dubai-burj-horizon", "title": "Emirates Spire Ridge", "theme": "kemet_nocturne", "style": "city"},
    {"id": "seattle-needle-fog", "title": "Cascadia Ridge Skyline", "theme": "nord_frost", "style": "mountain"},
    {"id": "san-francisco-golden-gate", "title": "Pacific Bay Bridge Grid", "theme": "amber_crt", "style": "city"},
    {"id": "lunar-crater-elevation", "title": "Mare Tranquillitatis Rim", "theme": "solarized_dark", "style": "mountain"},
    {"id": "mars-olympus-mons-topography", "title": "Olympus Mons Topo Scan", "theme": "amber_crt", "style": "mountain"},
    
    {"id": "deep-sea-trench-sonar", "title": "Mariana Trench Bathymetry", "theme": "tokyo_night", "style": "sonar"},
    {"id": "neural-weight-distribution", "title": "Transformer Weight Histogram", "theme": "cyberpunk_2077", "style": "spectrogram"},
    {"id": "pulse-code-modulation-grid", "title": "PCM Digital Modulation", "theme": "monokai_pro", "style": "spectrogram"},
    {"id": "heartbeat-ecg-rhythm", "title": "Biometric Pulse Rhythm", "theme": "dracula", "style": "sine"},
    {"id": "seismic-faultline-monitor", "title": "Richter Vector Faultline", "theme": "amber_crt", "style": "sine"},
    {"id": "radio-telescope-signal", "title": "Arecibo SETI Beacon", "theme": "rose_pine", "style": "sine"},
    {"id": "aurora-borealis-curtain", "title": "Aurora Magnetic Curtain", "theme": "nord_frost", "style": "mountain"},
    {"id": "glitch-art-raster-horizon", "title": "CRT Raster Desync Scan", "theme": "cyberpunk_2077", "style": "waterfall"},
    {"id": "low-poly-isometric-terrain", "title": "Low-Poly Elevation Map", "theme": "solarized_dark", "style": "mountain"},
    {"id": "quantum-probability-density", "title": "Schrödinger Wave Packet", "theme": "tokyo_night", "style": "sine"},
]

def generate_skyline_svg(preset_id: str, theme_override: str = None) -> str:
    preset = next((p for p in SKYLINE_PRESETS if p["id"] == preset_id), SKYLINE_PRESETS[0])
    theme = theme_override or preset["theme"]
    title = html.escape(preset["title"].upper())
    style = preset["style"]
    
    w, h = 880, 210
    builder = SVGBuilder(w, h, theme, title=f"{preset['title']} - Contribution Skyline", desc=f"Telemetry horizon {preset_id}")
    
    builder.add_custom_css("""
      .card-frame { fill: var(--vf-card); stroke: var(--vf-border); stroke-width: 1; }
      .skyline-bar { fill: var(--vf-accent-1); }
      .skyline-sub { fill: var(--vf-accent-2); opacity: 0.65; }
      .grid-h { stroke: var(--vf-border); stroke-width: 0.5; stroke-dasharray: 2 4; }
      .metric-title { font-family: var(--vf-font-mono); font-size: 13px; font-weight: 700; fill: var(--vf-text); }
      .metric-stat { font-family: var(--vf-font-mono); font-size: 11px; fill: var(--vf-text-muted); }
      .accent-pill { fill: var(--vf-bg); stroke: var(--vf-border); stroke-width: 1; }
    """)
    
    # Background frame
    builder.add_body(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" class="card-frame" />')
    
    # Top Telemetry Bar
    builder.add_body(f"""
    <g transform="translate(28, 26)">
      <circle cx="0" cy="0" r="4" fill="var(--vf-accent-1)" />
      <text x="12" y="4" class="metric-title">{title}</text>
      <text x="12" y="20" class="metric-stat">52 WEEKS • 1,844 TOTAL COMMITS • 99.8% CI PASS RATE</text>
      
      <g transform="translate({w - 240}, -8)">
        <rect x="0" y="0" width="180" height="26" rx="4" class="accent-pill" />
        <circle cx="12" cy="13" r="3" fill="var(--vf-accent-3)" />
        <text x="24" y="17" font-family="var(--vf-font-mono)" font-size="10" font-weight="700" fill="var(--vf-accent-1)">PEAK: 34 COMMITS/DAY</text>
      </g>
    </g>
    """)
    
    # Horizontal grid baseline
    base_y = h - 28
    for gy in [base_y - 30, base_y - 65, base_y - 100]:
        builder.add_body(f'<line x1="28" y1="{gy}" x2="{w-28}" y2="{gy}" class="grid-h" />')
        
    bars_svg = []
    num_bars = 52
    seed = abs(hash(preset_id)) % 1000
    
    if style in ["city", "nile"]:
        # City skyline stepped buildings
        bar_w = 12
        spacing = (w - 56) / num_bars
        for i in range(num_bars):
            bx = 28 + i * spacing
            val = math.sin((i + seed) * 0.4) * 35 + math.cos(i * 0.15) * 45 + 55
            val = max(10, min(115, val))
            by = base_y - val
            fill_color = "var(--vf-accent-1)" if (i % 3 == 0) else "var(--vf-accent-2)"
            bars_svg.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" height="{val:.1f}" rx="1" fill="{fill_color}" opacity="0.85" />')
            # Antenna
            if i % 7 == 0:
                bars_svg.append(f'<line x1="{bx + bar_w/2:.1f}" y1="{by}" x2="{bx + bar_w/2:.1f}" y2="{by - 12}" stroke="var(--vf-accent-3)" stroke-width="1.2" />')
    elif style == "pyramids":
        # Pyramid silhouettes
        p_path = f"M 28 {base_y} L 180 {base_y - 95} L 330 {base_y} L 460 {base_y - 110} L 600 {base_y} L 720 {base_y - 85} L {w-28} {base_y}"
        bars_svg.append(f'<path d="{p_path}" fill="var(--vf-accent-1)" opacity="0.45" />')
        bars_svg.append(f'<path d="{p_path}" fill="none" stroke="var(--vf-accent-1)" stroke-width="2" />')
    elif style == "spectrogram":
        bars = wave_spectrogram_points(w - 56, 110, bars=52, seed_seed=seed)
        for bx, by, bw, bh in bars:
            bars_svg.append(f'<rect x="{28 + bx}" y="{base_y - bh}" width="{bw}" height="{bh}" rx="2" fill="var(--vf-accent-1)" opacity="0.8" />')
    else:  # mountain, sonar, sine, waterfall
        # Continuous waveform path
        pts = []
        for i in range(120):
            x = 28 + i * ((w - 56) / 119)
            norm = i / 120
            y = base_y - (math.sin(norm * 14 + seed) * 25 + math.cos(norm * 6) * 40 + 50)
            pts.append(f"{'M' if i==0 else 'L'} {x:.1f} {y:.1f}")
        pts.append(f"L {w-28} {base_y} L 28 {base_y} Z")
        bars_svg.append(f'<path d="{" ".join(pts)}" fill="var(--vf-accent-2)" opacity="0.35" />')
        bars_svg.append(f'<path d="{" ".join(pts[:120])}" fill="none" stroke="var(--vf-accent-1)" stroke-width="2" />')
        
    builder.add_body(f'<g class="skyline-content">{"".join(bars_svg)}</g>')
    builder.add_body(f'<line x1="28" y1="{base_y}" x2="{w-28}" y2="{base_y}" stroke="var(--vf-border)" stroke-width="1.5" />')
    
    return builder.build()
