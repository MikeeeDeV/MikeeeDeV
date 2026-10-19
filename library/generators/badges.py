"""
library/generators/badges.py - 35 HUD Status Badges & Cyber Pills.
Renders compact, high-density status cards, reactor gauges, and cryptographic pills.
"""

import html
from typing import Dict, List, Any
from library.engine.svg_builder import SVGBuilder

BADGE_PRESETS: List[Dict[str, Any]] = [
    {"id": "now-building-reactor-core", "title": "Now Building: Core Engine", "theme": "kemet_nocturne", "label": "NOW BUILDING", "val": "FastMCP System Tools", "status": "ACTIVE"},
    {"id": "cyberpunk-hud-target-lock", "title": "Cyberpunk HUD Target Lock", "theme": "cyberpunk_2077", "label": "TARGET LOCK", "val": "Zero-Day Exploit Guard", "status": "ENGAGED"},
    {"id": "satellite-orbital-uplink", "title": "Satellite Orbital Uplink", "theme": "nord_frost", "label": "ORBITAL UPLINK", "val": "Telemetry Synchronized", "status": "LOCKED"},
    {"id": "glass-pill-active-status", "title": "Glass Pill Active Status", "theme": "rose_pine", "label": "SYSTEM STATE", "val": "Operational & Healthy", "status": "GREEN"},
    {"id": "brutalist-solid-badge", "title": "Brutalist Mono Badge", "theme": "solarized_dark", "label": "DETERMINISTIC", "val": "NixOS / Pure Closure", "status": "VERIFIED"},
    {"id": "neon-pulse-live-indicator", "title": "Neon Pulse Live Indicator", "theme": "tokyo_night", "label": "STREAM STATUS", "val": "Live Event Dispatch", "status": "PULSING"},
    {"id": "terminal-prompt-pill", "title": "Terminal Prompt Pill", "theme": "monokai_pro", "label": "SHELL ENV", "val": "zsh 5.9 // starship", "status": "PROMPT"},
    {"id": "docker-healthy-container", "title": "Docker Container Health", "theme": "emerald_matrix", "label": "CONTAINER", "val": "k8s-pod-replica-01", "status": "HEALTHY"},
    {"id": "github-actions-pass-shield", "title": "CI Matrix Pass Shield", "theme": "nord_frost", "label": "GITHUB ACTIONS", "val": "Hermetic Build Matrix", "status": "PASSING"},
    {"id": "nix-deterministic-pill", "title": "Nix Flake Hash Pin", "theme": "nord_frost", "label": "NIX FLAKE", "val": "sha256-4b9e8...7a", "status": "LOCKED"},
    
    {"id": "uptime-99-99-sla-badge", "title": "99.99% SLA Uptime Badge", "theme": "emerald_matrix", "label": "SLA AVAILABILITY", "val": "99.995% Past 365 Days", "status": "OPTIMAL"},
    {"id": "zero-vulnerability-audit", "title": "Zero Vulnerability Audit", "theme": "dracula", "label": "SECURITY AUDIT", "val": "0 High / 0 Critical", "status": "CLEAN"},
    {"id": "cairo-gmt-plus-3-clock", "title": "Cairo Workstation Time", "theme": "kemet_nocturne", "label": "TIMEZONE", "val": "Africa/Cairo (UTC+3)", "status": "SYNCED"},
    {"id": "open-source-sponsor-tier", "title": "GitHub Sponsors Tier", "theme": "rose_pine", "label": "SPONSORSHIP", "val": "Open Source Patron", "status": "SPONSOR"},
    {"id": "security-shield-a-plus", "title": "Mozilla Observatory A+", "theme": "nord_frost", "label": "OBSERVATORY", "val": "Score: 125/100 (A+)", "status": "SECURE"},
    {"id": "type-safe-strict-guard", "title": "TypeScript Strict Mode", "theme": "solarized_dark", "label": "TYPE SYSTEM", "val": "tsc --strict --noImplicitAny", "status": "PASS"},
    {"id": "latency-sub-5ms-badge", "title": "Sub-5ms Edge Latency", "theme": "tokyo_night", "label": "EDGE LATENCY", "val": "P99: 4.2ms Worldwide", "status": "FAST"},
    {"id": "fastmcp-ai-tool-certified", "title": "FastMCP AI Protocol Ready", "theme": "kemet_nocturne", "label": "MODEL PROTOCOL", "val": "MCP Spec v1.0 Compliant", "status": "READY"},
    {"id": "dual-license-mit-apache", "title": "Dual License MIT / Apache", "theme": "amber_crt", "label": "OPEN SOURCE", "val": "MIT / Apache-2.0 Dual", "status": "PERMISSIVE"},
    {"id": "carbon-neutral-compute", "title": "100% Carbon Neutral Compute", "theme": "emerald_matrix", "label": "INFRASTRUCTURE", "val": "Green Energy Datacenter", "status": "VERIFIED"},
    
    {"id": "code-coverage-100-badge", "title": "Code Coverage 100% Suite", "theme": "dracula", "label": "TEST COVERAGE", "val": "Statements: 100% Branch: 98%", "status": "100%"},
    {"id": "git-branch-main-protected", "title": "Branch Protection Strict", "theme": "solarized_dark", "label": "BRANCH RULE", "val": "Require Signed PR & Review", "status": "LOCKED"},
    {"id": "sha256-verified-binary", "title": "Cosign SHA256 Sigstore", "theme": "nord_frost", "label": "SIGSTORE ATTEST", "val": "Cosign Keyless Verified", "status": "VALID"},
    {"id": "rust-zero-cost-badge", "title": "Rust Zero-Cost Abstraction", "theme": "amber_crt", "label": "MEMORY SAFETY", "val": "Borrow Checker Enforced", "status": "SAFE"},
    {"id": "grpc-http3-quic-badge", "title": "HTTP/3 QUIC Protocol", "theme": "tokyo_night", "label": "TRANSPORT", "val": "HTTP/3 (QUIC 0-RTT)", "status": "ACTIVE"},
    {"id": "edge-worker-active", "title": "Cloudflare Edge V8 Worker", "theme": "amber_crt", "label": "EDGE RUNTIME", "val": "V8 Isolate 0ms Cold Start", "status": "READY"},
    {"id": "battery-charge-100-hud", "title": "Energy Storage HUD", "theme": "emerald_matrix", "label": "POWER SYSTEM", "val": "100% Battery / Solar Grid", "status": "FULL"},
    {"id": "cpu-frequency-turbo-pill", "title": "CPU Turbo Boost 5.4 GHz", "theme": "cyberpunk_2077", "label": "HARDWARE CLOCK", "val": "5.4 GHz Turbo Boost", "status": "TURBO"},
    {"id": "ram-ecc-verified-badge", "title": "ECC Memory Bitflip Guard", "theme": "nord_frost", "label": "HARDWARE MEMORY", "val": "DDR5 ECC Error Correcting", "status": "ECC OK"},
    {"id": "dark-mode-native-toggle", "title": "Native CSS prefers-color", "theme": "monokai_pro", "label": "THEME ENGINE", "val": "prefers-color-scheme Native", "status": "ADAPTIVE"},
    
    {"id": "system-team-lead-crest", "title": "Senior Systems Engineer Crest", "theme": "kemet_nocturne", "label": "EXPERTISE", "val": "Senior Full-Stack & Systems Engineer", "status": "SENIOR"},
    {"id": "kemet-pharaonic-seal", "title": "Pharaonic Horus Eye Seal", "theme": "kemet_nocturne", "label": "KEMET SEAL", "val": "Ancient Geometry • Modern Core", "status": "SEALED"},
    {"id": "high-availability-active", "title": "Multi-Region HA Active", "theme": "dracula", "label": "AVAILABILITY", "val": "3 AZ Active-Active Failover", "status": "HA READY"},
    {"id": "immutable-root-fs-pill", "title": "Immutable Read-Only RootFS", "theme": "solarized_dark", "label": "ROOT FILESYSTEM", "val": "RO SquashFS / OSTree", "status": "IMMUTABLE"},
    {"id": "warp-drive-online-hud", "title": "Warp Drive Subspace HUD", "theme": "cyberpunk_2077", "label": "PROPULSION", "val": "Alcubierre Metric Online", "status": "WARP 9"},
]

def generate_badge_svg(preset_id: str, theme_override: str = None) -> str:
    preset = next((p for p in BADGE_PRESETS if p["id"] == preset_id), BADGE_PRESETS[0])
    theme = theme_override or preset["theme"]
    title = preset["title"]
    label = html.escape(preset["label"])
    val = html.escape(preset["val"])
    status = html.escape(preset["status"])
    
    w, h = 420, 88
    builder = SVGBuilder(w, h, theme, title=f"{title} - HUD Badge", desc=f"Status badge {preset_id}")
    
    builder.add_custom_css("""
      .badge-frame { fill: var(--vf-card); stroke: var(--vf-border); stroke-width: 1; }
      .label-text { font-family: var(--vf-font-mono); font-size: 10px; font-weight: 700; fill: var(--vf-accent-1); letter-spacing: 1px; }
      .value-text { font-family: var(--vf-font-sans); font-size: 13.5px; font-weight: 700; fill: var(--vf-text); }
      .status-pill { fill: var(--vf-bg); stroke: var(--vf-border); stroke-width: 1; }
      .status-text { font-family: var(--vf-font-mono); font-size: 9.5px; font-weight: 700; fill: var(--vf-accent-2); }
      .hud-dot { fill: var(--vf-accent-1); }
      .hud-decor { stroke: var(--vf-border); stroke-width: 1; fill: none; }
    """)
    
    # Outer frame with subtle chamfered corners
    builder.add_body(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="6" class="badge-frame" />')
    
    # Decorative corner tick marks
    builder.add_body(f"""
    <path d="M 6 12 L 6 6 L 12 6" class="hud-decor" />
    <path d="M {w-6} 12 L {w-6} 6 L {w-12} 6" class="hud-decor" />
    <path d="M 6 {h-12} L 6 {h-6} L 12 {h-6}" class="hud-decor" />
    <path d="M {w-6} {h-12} L {w-6} {h-6} L {w-12} {h-6}" class="hud-decor" />
    """)
    
    # Left status indicator column
    builder.add_body(f"""
    <g transform="translate(20, 24)">
      <!-- Pulsing radar dot -->
      <circle cx="8" cy="8" r="8" fill="var(--vf-accent-1)" opacity="0.18" />
      <circle cx="8" cy="8" r="4" fill="var(--vf-accent-1)" />
      
      <!-- Content column -->
      <g transform="translate(26, 0)">
        <text x="0" y="4" class="label-text">{label}</text>
        <text x="0" y="24" class="value-text">{val}</text>
      </g>
    </g>
    """)
    
    # Right status chip
    chip_w = max(72, len(status) * 8 + 20)
    builder.add_body(f"""
    <g transform="translate({w - chip_w - 20}, 30)">
      <rect x="0" y="0" width="{chip_w}" height="24" rx="4" class="status-pill" />
      <circle cx="10" cy="12" r="3" fill="var(--vf-accent-2)" />
      <text x="{chip_w / 2 + 5}" y="15.5" text-anchor="middle" class="status-text">{status}</text>
    </g>
    """)
    
    # Bottom subtle progress or scanline
    builder.add_body(f'<line x1="20" y1="{h-10}" x2="{w-20}" y2="{h-10}" stroke="var(--vf-border)" stroke-width="0.8" />')
    builder.add_body(f'<line x1="20" y1="{h-10}" x2="{w*0.45}" y2="{h-10}" stroke="var(--vf-accent-1)" stroke-width="1.2" />')
    
    return builder.build()
