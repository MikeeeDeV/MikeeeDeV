"""
library/generators/repo_cards.py - 35 Bento & Glassmorphic Repo Cards.
Renders cards for featured repositories and project portfolios.
"""

import html
from typing import Dict, List, Any
from library.engine.svg_builder import SVGBuilder

REPO_PRESETS: List[Dict[str, Any]] = [
    {"id": "glass-bento-repo-card", "title": "Glass Bento Repo Card", "theme": "kemet_nocturne", "repo": "NixManagerPro", "lang": "Nix", "stars": 12, "desc": "Production-grade NixOS and Home-Manager multi-profile controller."},
    {"id": "cyber-outline-nixmanager", "title": "Cyber Outline Card", "theme": "cyberpunk_2077", "repo": "next-session-guard", "lang": "TypeScript", "stars": 24, "desc": "Zero-trust session middleware with rotation & tamper-proof cookies."},
    {"id": "terminal-box-sessionguard", "title": "Terminal Box Code Card", "theme": "nord_frost", "repo": "git-smart-sync", "lang": "Python", "stars": 38, "desc": "Intelligent multi-remote synchronization tool with rebase conflict detection."},
    {"id": "gradient-glow-smart-sync", "title": "Gradient Glow Bento Card", "theme": "tokyo_night", "repo": "My-portfolio", "lang": "TypeScript", "stars": 19, "desc": "Interactive personal engineering showcase with 3D canvas and dynamic themes."},
    {"id": "clean-minimal-portfolio", "title": "Clean Minimalist Mono Card", "theme": "solarized_dark", "repo": "fastmcp-kit", "lang": "Python", "stars": 52, "desc": "Ultra-lightweight FastMCP tool framework with type-safe schema reflection."},
    {"id": "deep-glass-fastmcp-tools", "title": "Deep Glass Frosted Card", "theme": "dracula", "repo": "vector-forge", "lang": "Python", "stars": 140, "desc": "Deterministic 200+ SVG developer component library with live preview."},
    {"id": "bordered-beam-next-kit", "title": "Bordered Beam Highlight Card", "theme": "monokai_pro", "repo": "cleankit-core", "lang": "TypeScript", "stars": 15, "desc": "Enterprise clean architecture starter kit with strict domain boundaries."},
    {"id": "monokai-ide-code-card", "title": "Monokai Syntax Card", "theme": "monokai_pro", "repo": "nile-vector-engine", "lang": "Rust", "stars": 67, "desc": "High-performance vector geometry and rosette math generator in Rust."},
    {"id": "dracula-shadow-card", "title": "Dracula Cast Shadow Card", "theme": "dracula", "repo": "al-raheq-al-makhtom", "lang": "Dart", "stars": 8, "desc": "Islamic biography and reference library with bilingual Arabic/English search."},
    {"id": "tokyo-night-glass-box", "title": "Tokyo Night Glass Container", "theme": "tokyo_night", "repo": "cairo-transit-tracker", "lang": "Go", "stars": 41, "desc": "Real-time Cairo metro and bus schedule engine with offline GTFS feed."},
    
    {"id": "nordic-frost-bento-tile", "title": "Nordic Frost Bento Tile", "theme": "nord_frost", "repo": "arctic-guard", "lang": "Rust", "stars": 89, "desc": "Cryptographic authentication guard for distributed bare-metal clusters."},
    {"id": "matrix-terminal-card", "title": "Matrix Terminal Green Card", "theme": "emerald_matrix", "repo": "cipher-stream", "lang": "C", "stars": 110, "desc": "Low-level POSIX ring buffer with SIMD acceleration and zero copy."},
    {"id": "amber-crt-vintage-card", "title": "Amber CRT Heritage Card", "theme": "amber_crt", "repo": "vintage-asm", "lang": "Assembly", "stars": 95, "desc": "x86 real-mode bootloader and retro graphical OS kernel in 512 bytes."},
    {"id": "rose-pine-minimal-tile", "title": "Rosé Pine Minimal Tile", "theme": "rose_pine", "repo": "pastel-ui", "lang": "CSS", "stars": 34, "desc": "Accessible, zero-runtime CSS tokens and theme variables collection."},
    {"id": "solarized-contrast-box", "title": "Solarized High-Contrast Box", "theme": "solarized_dark", "repo": "solar-query", "lang": "SQL", "stars": 29, "desc": "BigQuery cost optimization scripts and automated partition pruning."},
    {"id": "brutalist-mono-black", "title": "Brutalist Mono Card", "theme": "kemet_nocturne", "repo": "kemet-cli", "lang": "Python", "stars": 76, "desc": "Developer command-line generator for pharaonic SVG badges and cards."},
    {"id": "holographic-edge-card", "title": "Holographic Edge Card", "theme": "cyberpunk_2077", "repo": "holo-mesh", "lang": "TypeScript", "stars": 83, "desc": "WebGL shaders and procedural particle mesh generator for portfolios."},
    {"id": "chamfered-cyber-card", "title": "Chamfered Cyber Deck Card", "theme": "cyberpunk_2077", "repo": "cyber-proxy", "lang": "Go", "stars": 62, "desc": "Layer-7 reverse proxy with automatic SSL and dynamic rate limiting."},
    {"id": "circuit-traced-card", "title": "Circuit Traced Bento Card", "theme": "emerald_matrix", "repo": "pcb-autoroute", "lang": "Python", "stars": 54, "desc": "Topological A* autorouter for double-sided printed circuit boards."},
    {"id": "floating-glass-card", "title": "Floating Glass Acrylic Card", "theme": "rose_pine", "repo": "glass-components", "lang": "TypeScript", "stars": 47, "desc": "Pure CSS glassmorphic UI components with fallback backdrop-filters."},
    
    {"id": "double-border-accent", "title": "Double Border Accent Card", "theme": "monokai_pro", "repo": "accent-kit", "lang": "TypeScript", "stars": 33, "desc": "Dynamic design system tokens and automated Figma-to-code compiler."},
    {"id": "kemet-hieroglyph-bento", "title": "Kemet Hieroglyphic Bento", "theme": "kemet_nocturne", "repo": "hieroglyph-fonts", "lang": "SVG", "stars": 71, "desc": "Vectorized ancient Egyptian glyph library with OpenType SVG font tables."},
    {"id": "radar-swept-repo-card", "title": "Radar Swept Defense Card", "theme": "tokyo_night", "repo": "radar-sentinel", "lang": "Rust", "stars": 115, "desc": "Network anomaly detection using eBPF probes and realtime sliding windows."},
    {"id": "split-gradient-card", "title": "Split Gradient Bento Card", "theme": "dracula", "repo": "split-worker", "lang": "TypeScript", "stars": 28, "desc": "Edge compute worker pipeline splitting heavy JSON transforms across cores."},
    {"id": "code-diff-preview-card", "title": "Code Diff Review Card", "theme": "solarized_dark", "repo": "diff-lens", "lang": "Go", "stars": 92, "desc": "Semantic code diff engine that understands AST mutations and renames."},
    {"id": "astrolabe-corner-card", "title": "Astrolabe Corner Card", "theme": "kemet_nocturne", "repo": "celestial-clock", "lang": "Python", "stars": 44, "desc": "Astronomical calculations engine for prayer times and lunar phases."},
    {"id": "isometric-shadow-card", "title": "Isometric Shadow Card", "theme": "nord_frost", "repo": "iso-engine", "lang": "TypeScript", "stars": 58, "desc": "Tilemap rendering engine with depth sorting and isometric lightmaps."},
    {"id": "neon-underglow-card", "title": "Neon Underglow Card", "theme": "cyberpunk_2077", "repo": "underglow-term", "lang": "Rust", "stars": 133, "desc": "GPU-accelerated terminal emulator with customizable glow shaders."},
    {"id": "dotted-grid-blueprint", "title": "Dotted Blueprint Card", "theme": "solarized_dark", "repo": "cad-viewer", "lang": "C++", "stars": 81, "desc": "Lightweight DXF / DWG CAD file viewer with SVG export capabilities."},
    {"id": "striped-caution-card", "title": "Caution Stripe Warning Card", "theme": "amber_crt", "repo": "safety-harness", "lang": "Rust", "stars": 39, "desc": "Fault-injection testing harness for distributed consensus algorithms."},
    
    {"id": "metallic-chrome-sheen", "title": "Metallic Chrome Sheen Card", "theme": "nord_frost", "repo": "chrome-audio", "lang": "C++", "stars": 66, "desc": "Low-latency WebAudio DSP plugins and synthesizers in WebAssembly."},
    {"id": "quantum-dot-card", "title": "Quantum Dot Grid Card", "theme": "tokyo_night", "repo": "qubit-sim", "lang": "Python", "stars": 50, "desc": "Statevector quantum simulator supporting up to 30 qubits on GPU."},
    {"id": "frosted-acrylic-card", "title": "Frosted Acrylic Glass Card", "theme": "rose_pine", "repo": "acrylic-dock", "lang": "Swift", "stars": 77, "desc": "macOS status bar utility for toggling display resolutions and rates."},
    {"id": "vintage-cassette-card", "title": "Vintage Cassette Card", "theme": "amber_crt", "repo": "tape-archive", "lang": "C", "stars": 49, "desc": "FSK audio encoder converting binary tarballs to analog audio cassettes."},
    {"id": "kemet-nocturne-master-card", "title": "Kemet Nocturne Master Bento", "theme": "kemet_nocturne", "repo": "systems-core-suite", "lang": "TypeScript", "stars": 125, "desc": "Senior systems engineer workspace, dashboard, and telemetry stack."},
]

def generate_repo_card_svg(preset_id: str, theme_override: str = None) -> str:
    preset = next((p for p in REPO_PRESETS if p["id"] == preset_id), REPO_PRESETS[0])
    theme = theme_override or preset["theme"]
    title = preset["title"]
    repo = html.escape(preset["repo"])
    lang = html.escape(preset["lang"])
    stars = preset["stars"]
    desc = html.escape(preset["desc"])
    
    w, h = 420, 160
    builder = SVGBuilder(w, h, theme, title=f"{repo} - Repo Card", desc=f"Featured repo bento card {preset_id}")
    
    builder.add_custom_css("""
      .card-box { fill: var(--vf-card); stroke: var(--vf-border); stroke-width: 1; }
      .repo-name { font-family: var(--vf-font-sans); font-size: 15px; font-weight: 700; fill: var(--vf-accent-2); }
      .repo-badge { fill: var(--vf-bg); stroke: var(--vf-border); stroke-width: 1; }
      .repo-desc { font-family: var(--vf-font-sans); font-size: 11.5px; fill: var(--vf-text-muted); }
      .meta-text { font-family: var(--vf-font-mono); font-size: 10.5px; fill: var(--vf-text); }
      .card-decor { stroke: var(--vf-border); stroke-width: 0.8; fill: none; }
    """)
    
    # Outer frame
    builder.add_body(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" class="card-box" />')
    
    # Header: Repo Icon + Name + Public Pill
    builder.add_body(f"""
    <g transform="translate(24, 28)">
      <!-- Book / Repo Icon -->
      <g transform="translate(0, -12)">
        <path d="M 0 2 L 6 0 L 12 2 L 12 14 L 6 12 L 0 14 Z" fill="none" stroke="var(--vf-accent-1)" stroke-width="1.4" />
        <line x1="6" y1="0" x2="6" y2="12" stroke="var(--vf-accent-1)" stroke-width="1.2" />
      </g>
      
      <!-- Repo Name -->
      <text x="22" y="0" class="repo-name">{repo}</text>
      
      <!-- Public Badge -->
      <g transform="translate({w - 110}, -14)">
        <rect x="0" y="0" width="58" height="20" rx="10" class="repo-badge" />
        <text x="29" y="13.5" text-anchor="middle" font-family="var(--vf-font-mono)" font-size="9" font-weight="600" fill="var(--vf-accent-1)">PUBLIC</text>
      </g>
    </g>
    """)
    
    # Description (with safe multiline split)
    desc_words = desc.split()
    line1 = " ".join(desc_words[:6])
    line2 = " ".join(desc_words[6:13])
    if len(desc_words) > 13:
        line2 += "..."
        
    builder.add_body(f"""
    <g transform="translate(24, 66)">
      <text x="0" y="0" class="repo-desc">{line1}</text>
      <text x="0" y="18" class="repo-desc">{line2}</text>
    </g>
    """)
    
    # Footer: Language + Stars + Forks + Deterministic License Tag
    builder.add_body(f"""
    <g transform="translate(24, 130)">
      <!-- Language -->
      <circle cx="5" cy="-4" r="4.5" fill="var(--vf-accent-1)" />
      <text x="16" y="0" class="meta-text">{lang}</text>
      
      <!-- Stars -->
      <g transform="translate(90, 0)">
        <path d="M 0 -8 L 2.5 -3 L 8 -2.5 L 4 1.5 L 5 7 L 0 4 L -5 7 L -4 1.5 L -8 -2.5 L -2.5 -3 Z" fill="var(--vf-accent-1)" transform="scale(0.8) translate(6, -6)" />
        <text x="18" y="0" class="meta-text">{stars}</text>
      </g>
      
      <!-- License Pill -->
      <g transform="translate({w - 130}, -12)">
        <rect x="0" y="0" width="78" height="18" rx="3" fill="var(--vf-bg)" stroke="var(--vf-border)" />
        <text x="39" y="12" text-anchor="middle" font-family="var(--vf-font-mono)" font-size="9" fill="var(--vf-accent-2)">MIT LICENSE</text>
      </g>
    </g>
    """)
    
    return builder.build()
