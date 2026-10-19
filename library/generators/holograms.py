"""
library/generators/holograms.py - 25 Holographic Ledgers, Radars & Scanning Dials.
Renders circular radar grids, scanning beams, access logs, and biometric ledgers.
"""

import html
import math
from typing import Dict, List, Any
from library.engine.svg_builder import SVGBuilder

HOLOGRAM_PRESETS: List[Dict[str, Any]] = [
    {"id": "visitor-terminal-ledger", "title": "Visitor Terminal Ledger", "theme": "kemet_nocturne", "type": "ledger"},
    {"id": "quantum-radar-sweep", "title": "Quantum Radar Sweep", "theme": "cyberpunk_2077", "type": "radar"},
    {"id": "circular-sonar-ping", "title": "Circular Sonar Ping", "theme": "nord_frost", "type": "sonar"},
    {"id": "blockchain-block-explorer", "title": "Blockchain Merkle Ledger", "theme": "amber_crt", "type": "ledger"},
    {"id": "cyber-docking-register", "title": "Orbital Docking Register", "theme": "tokyo_night", "type": "radar"},
    {"id": "punch-card-retro-ledger", "title": "Punch Card Heritage Log", "theme": "solarized_dark", "type": "ledger"},
    {"id": "satellite-tracker-hud", "title": "Low-Earth Satellite Tracker", "theme": "nord_frost", "type": "radar"},
    {"id": "matrix-stream-access-log", "title": "Matrix Terminal Access Log", "theme": "emerald_matrix", "type": "ledger"},
    {"id": "star-chart-navigator", "title": "Celestial Sextant Star Chart", "theme": "dracula", "type": "radar"},
    {"id": "atomic-orbital-compass", "title": "Atomic Electron Orbital Ring", "theme": "monokai_pro", "type": "sonar"},
    
    {"id": "seismic-station-register", "title": "Global Seismic Event Log", "theme": "amber_crt", "type": "ledger"},
    {"id": "deep-core-telemetry-dial", "title": "Geothermal Core Pressure", "theme": "amber_crt", "type": "sonar"},
    {"id": "retinal-scan-biometric", "title": "Biometric Retinal Scanner", "theme": "cyberpunk_2077", "type": "radar"},
    {"id": "particle-accelerator-ring", "title": "Hadron Synchrotron Beam", "theme": "tokyo_night", "type": "sonar"},
    {"id": "holographic-pyramid-wire", "title": "Holographic Giza Pyramid", "theme": "kemet_nocturne", "type": "radar"},
    {"id": "air-traffic-control-radar", "title": "Air Traffic Primary Radar", "theme": "emerald_matrix", "type": "radar"},
    {"id": "submarine-sonar-array", "title": "Towed Hydrophone Array", "theme": "nord_frost", "type": "sonar"},
    {"id": "cyber-compass-rose", "title": "Digital Compass Azimuth", "theme": "rose_pine", "type": "radar"},
    {"id": "pulsar-timing-ledger", "title": "Millisecond Pulsar Timing", "theme": "dracula", "type": "ledger"},
    {"id": "dna-helix-sequencer", "title": "Nanopore DNA Sequencer", "theme": "monokai_pro", "type": "sonar"},
    
    {"id": "magnetic-field-dipole", "title": "Geomagnetic Dipole Flux", "theme": "solarized_dark", "type": "sonar"},
    {"id": "interstellar-waypoint-beacon", "title": "Deep Space Waypoint Beacon", "theme": "rose_pine", "type": "radar"},
    {"id": "terminal-access-badge-card", "title": "Clearance Level 5 Access", "theme": "kemet_nocturne", "type": "ledger"},
    {"id": "kemet-astrolabe-clock", "title": "Pharaonic Astrolabe Clock", "theme": "kemet_nocturne", "type": "sonar"},
    {"id": "infinity-hyperdrive-gauge", "title": "Hyperdrive Warp Core Gauge", "theme": "cyberpunk_2077", "type": "radar"},
]

def generate_hologram_svg(preset_id: str, theme_override: str = None) -> str:
    preset = next((p for p in HOLOGRAM_PRESETS if p["id"] == preset_id), HOLOGRAM_PRESETS[0])
    theme = theme_override or preset["theme"]
    title = html.escape(preset["title"].upper())
    h_type = preset["type"]
    
    w, h = 560, 240
    builder = SVGBuilder(w, h, theme, title=f"{preset['title']} - Hologram Scanner", desc=f"Hologram widget {preset_id}")
    
    builder.add_custom_css("""
      .holo-card { fill: var(--vf-card); stroke: var(--vf-border); stroke-width: 1; }
      .holo-title { font-family: var(--vf-font-sans); font-size: 15px; font-weight: 800; fill: var(--vf-text); }
      .holo-sub { font-family: var(--vf-font-mono); font-size: 10.5px; fill: var(--vf-text-muted); }
      .ring-stroke { stroke: var(--vf-accent-1); stroke-width: 1.2; fill: none; }
      .ring-sub { stroke: var(--vf-border); stroke-width: 1; fill: none; stroke-dasharray: 4 4; }
      .sweep-line { stroke: var(--vf-accent-2); stroke-width: 1.8; }
      .log-line { font-family: var(--vf-font-mono); font-size: 10.5px; fill: var(--vf-text); }
    """)
    
    # Outer frame
    builder.add_body(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" class="holo-card" />')
    
    # Left Content Column
    builder.add_body(f"""
    <g transform="translate(28, 32)">
      <circle cx="0" cy="0" r="4" fill="var(--vf-accent-1)" />
      <text x="12" y="4" class="holo-title">{title}</text>
      <text x="12" y="20" class="holo-sub">SYSTEM // 0x{abs(hash(preset_id)) % 0xFFFFFF:06X} • PROTOCOL: HOLO-DIAL</text>
    </g>
    """)
    
    cx_dial, cy_dial = w - 120, h / 2
    r_dial = 75
    
    # Holographic Dial or Radar on Right
    dial_elements = []
    dial_elements.append(f'<circle cx="{cx_dial}" cy="{cy_dial}" r="{r_dial}" class="ring-sub" />')
    dial_elements.append(f'<circle cx="{cx_dial}" cy="{cy_dial}" r="{r_dial * 0.65}" class="ring-stroke" />')
    dial_elements.append(f'<circle cx="{cx_dial}" cy="{cy_dial}" r="{r_dial * 0.35}" class="ring-sub" />')
    dial_elements.append(f'<circle cx="{cx_dial}" cy="{cy_dial}" r="4" fill="var(--vf-accent-1)" />')
    
    # Crosshairs
    dial_elements.append(f'<line x1="{cx_dial - r_dial}" y1="{cy_dial}" x2="{cx_dial + r_dial}" y2="{cy_dial}" stroke="var(--vf-border)" stroke-width="0.8" />')
    dial_elements.append(f'<line x1="{cx_dial}" y1="{cy_dial - r_dial}" x2="{cx_dial}" y2="{cy_dial + r_dial}" stroke="var(--vf-border)" stroke-width="0.8" />')
    
    # Sweeping radar vector
    sweep_angle = (abs(hash(preset_id)) % 360) * (math.pi / 180)
    sx = cx_dial + r_dial * math.cos(sweep_angle)
    sy = cy_dial + r_dial * math.sin(sweep_angle)
    dial_elements.append(f'<line x1="{cx_dial}" y1="{cy_dial}" x2="{sx:.1f}" y2="{sy:.1f}" class="sweep-line" />')
    dial_elements.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4.5" fill="var(--vf-accent-3)" />')
    
    builder.add_body(f'<g class="dial-group">{"".join(dial_elements)}</g>')
    
    # Left ledger entries
    ledger_entries = [
        ("[0x1F4] Handshake OK", "SHA-256 Verified", "0.4ms"),
        ("[0x1F5] Synchronizing State", "Merkle Root: 0x9a8f", "1.2ms"),
        ("[0x1F6] Ingestion Complete", "Packets: 2,048", "0.8ms"),
        ("[0x1F7] Node Consensus", "Quorum: 3/3", "0.1ms"),
    ]
    
    rows = []
    for r_idx, (c1, c2, c3) in enumerate(ledger_entries):
        ry = 78 + r_idx * 32
        rows.append(f"""
        <g transform="translate(28, {ry})">
          <rect x="0" y="0" width="360" height="24" rx="3" fill="var(--vf-bg)" stroke="var(--vf-border)" stroke-width="0.7" />
          <circle cx="10" cy="12" r="2.5" fill="var(--vf-accent-2)" />
          <text x="20" y="16" class="log-line">{c1}</text>
          <text x="180" y="16" font-family="var(--vf-font-mono)" font-size="10" fill="var(--vf-text-muted)">{c2}</text>
          <text x="348" y="16" text-anchor="end" font-family="var(--vf-font-mono)" font-size="10" fill="var(--vf-accent-1)">{c3}</text>
        </g>
        """)
    builder.add_body(f'<g class="ledger-rows">{"".join(rows)}</g>')
    
    return builder.build()
