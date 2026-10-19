"""
library/generators/terminals.py - 35 Neofetch & System Terminal Cards.
Renders authentic terminal sessions with ASCII glyphs, system specs,
memory meter, and color matrix chips.
"""

from typing import Dict, List, Any
from library.engine.svg_builder import SVGBuilder

TERMINAL_PRESETS: List[Dict[str, Any]] = [
    {"id": "nixos-flake-minimal", "title": "NixOS Flake Zero-Drift", "theme": "nord_frost", "distro": "nixos", "uptime": "42d 13h", "shell": "zsh 5.9"},
    {"id": "arch-retro-amber", "title": "Arch Linux Rolling Release", "theme": "amber_crt", "distro": "arch", "uptime": "19d 04h", "shell": "fish 3.7"},
    {"id": "cyberdeck-terminal-hacker", "title": "Cyberdeck Offensive HUD", "theme": "cyberpunk_2077", "distro": "cyber", "uptime": "88d 21h", "shell": "bash 5.2"},
    {"id": "dracula-zsh-prompt", "title": "Dracula Nocturnal Console", "theme": "dracula", "distro": "dracula", "uptime": "14d 08h", "shell": "zsh (starship)"},
    {"id": "tokyo-night-fish-shell", "title": "Tokyo Night Neovim Host", "theme": "tokyo_night", "distro": "debian", "uptime": "31d 19h", "shell": "fish + tmux"},
    {"id": "retro-macintosh-classic", "title": "Classic Mac System 7", "theme": "solarized_dark", "distro": "apple", "uptime": "120d 00h", "shell": "mpw c-shell"},
    {"id": "ubuntu-server-motd", "title": "Ubuntu Server 24.04 LTS", "theme": "amber_crt", "distro": "ubuntu", "uptime": "365d 11h", "shell": "bash --login"},
    {"id": "kali-offensive-hud", "title": "Kali Vector Terminal", "theme": "emerald_matrix", "distro": "kali", "uptime": "06d 14h", "shell": "zsh 5.9"},
    {"id": "gentoo-kernel-compile", "title": "Gentoo Hardened Core", "theme": "monokai_pro", "distro": "gentoo", "uptime": "250d 02h", "shell": "sh (gcc-14)"},
    {"id": "freebsd-daemon-card", "title": "FreeBSD 14.1 Beastie", "theme": "kemet_nocturne", "distro": "bsd", "uptime": "410d 18h", "shell": "tcsh"},
    
    {"id": "monokai-coder-terminal", "title": "Monokai Pro IDE Console", "theme": "monokai_pro", "distro": "nixos", "uptime": "18d 06h", "shell": "nu-shell"},
    {"id": "solarized-tmux-split", "title": "Solarized Tmux Session", "theme": "solarized_dark", "distro": "debian", "uptime": "77d 09h", "shell": "tmux: 4 panes"},
    {"id": "matrix-green-code-rain", "title": "Emerald Code Matrix Node", "theme": "emerald_matrix", "distro": "cyber", "uptime": "999d 23h", "shell": "matrix.sh"},
    {"id": "synthwave-retro-console", "title": "Synthwave Outrun CLI", "theme": "cyberpunk_2077", "distro": "apple", "uptime": "22d 17h", "shell": "zsh (p10k)"},
    {"id": "docker-container-stats", "title": "Docker Engine Daemon", "theme": "nord_frost", "distro": "docker", "uptime": "84d 12h", "shell": "dockerd 26.1"},
    {"id": "k8s-pod-cluster-telemetry", "title": "Kubernetes Control Plane", "theme": "tokyo_night", "distro": "k8s", "uptime": "180d 05h", "shell": "kubectl v1.30"},
    {"id": "rust-cargo-build-summary", "title": "Rust Cargo Toolchain", "theme": "amber_crt", "distro": "rust", "uptime": "03d 01h", "shell": "cargo 1.78"},
    {"id": "python-fastmcp-daemon", "title": "FastMCP AI Agent Node", "theme": "kemet_nocturne", "distro": "python", "uptime": "09d 22h", "shell": "uv / python 3.12"},
    {"id": "redis-inmemory-stats", "title": "Redis Sentinel Memory", "theme": "dracula", "distro": "redis", "uptime": "115d 14h", "shell": "redis-cli 7.2"},
    {"id": "postgresql-database-cluster", "title": "PostgreSQL 16 Engine", "theme": "nord_frost", "distro": "postgres", "uptime": "204d 16h", "shell": "psql v16.3"},
    
    {"id": "git-commit-hash-log", "title": "Git Head Commit Ledger", "theme": "solarized_dark", "distro": "git", "uptime": "45d 08h", "shell": "git smart-sync"},
    {"id": "vax-vms-heritage-console", "title": "OpenVMS Heritage Console", "theme": "amber_crt", "distro": "vms", "uptime": "1420d 09h", "shell": "DCL Prompt"},
    {"id": "commodore-64-basic-prompt", "title": "Commodore 64 BASIC V2", "theme": "dracula", "distro": "c64", "uptime": "READY.", "shell": "64K RAM SYSTEM"},
    {"id": "cyberpunk-netrunner-rig", "title": "Netrunner Deck Interface", "theme": "cyberpunk_2077", "distro": "cyber", "uptime": "33d 19h", "shell": "icebreaker v4"},
    {"id": "deep-space-satellite-telemetry", "title": "Orbital Telemetry Rig", "theme": "rose_pine", "distro": "nasa", "uptime": "4892d 11h", "shell": "telecom/s-band"},
    {"id": "quantum-qubit-register", "title": "Qiskit Quantum Register", "theme": "tokyo_night", "distro": "quantum", "uptime": "00d 04h", "shell": "127 Qubits Coherent"},
    {"id": "linux-kernel-ring-buffer", "title": "Dmesg Kernel Ring Buffer", "theme": "monokai_pro", "distro": "linux", "uptime": "91d 15h", "shell": "vmlinuz-6.9.3"},
    {"id": "systemd-cgroup-monitor", "title": "Systemd Slice Inspector", "theme": "emerald_matrix", "distro": "systemd", "uptime": "54d 13h", "shell": "journalctl -f"},
    {"id": "btop-inspired-system-hud", "title": "Btop++ Resource Monitor", "theme": "tokyo_night", "distro": "btop", "uptime": "12d 10h", "shell": "btop v1.3.2"},
    {"id": "starship-prompt-showcase", "title": "Cross-Shell Starship", "theme": "nord_frost", "distro": "starship", "uptime": "27d 03h", "shell": "starship prompt"},
    
    {"id": "neovim-lua-dashboard", "title": "Neovim LazyVim Buffer", "theme": "rose_pine", "distro": "neovim", "uptime": "11d 07h", "shell": "nvim 0.10.0 (lua)"},
    {"id": "wasm-runtime-status", "title": "Wasmtime WASI Sandbox", "theme": "amber_crt", "distro": "wasm", "uptime": "05d 18h", "shell": "wasmtime 21.0"},
    {"id": "graphql-gateway-node", "title": "Apollo Router Federation", "theme": "dracula", "distro": "graphql", "uptime": "63d 20h", "shell": "subgraphs: 12"},
    {"id": "ai-agent-memory-context", "title": "LLM Context Window HUD", "theme": "cyberpunk_2077", "distro": "ai", "uptime": "02d 14h", "shell": "context: 1M tokens"},
    {"id": "kemet-nile-terminal-zero", "title": "Kemet Nile Terminal Zero", "theme": "kemet_nocturne", "distro": "kemet", "uptime": "100d 00h", "shell": "nile-daemon v1.0"},
]

DISTRO_ASCII = {
    "nixos": [
        "  ❄️   / \\  / \\  ❄️",
        "     /   \\/   \\   ",
        "    |  NixOS  |   ",
        "     \\   /\\   /   ",
        "  ❄️   \\/  \\/  ❄️",
    ],
    "arch": [
        "      /\\        ",
        "     /  \\       ",
        "    /\\   \\      ",
        "   /      \\     ",
        "  /   ,,   \\    ",
        " /   |  |  -\\   ",
    ],
    "cyber": [
        "  [⚡] CYBER // 2077",
        "  |  ██████╗  ██╗  ",
        "  |  ██╔═══╝  ██║  ",
        "  |  ██║      ██║  ",
        "  |  ╚═╝      ╚═╝  ",
    ],
    "apple": [
        "       .:'      ",
        "    __ :'__     ",
        " .'`  `-'  ``.  ",
        ":          .-'  ",
        ":         :     ",
        " :         `-;  ",
        "  `.__.-.__.'   ",
    ],
    "default": [
        "    .---.    ",
        "   /     \\   ",
        "  | () () |  ",
        "   \\  _  /   ",
        "    /___\\    ",
    ]
}

def generate_terminal_svg(preset_id: str, theme_override: str = None) -> str:
    preset = next((p for p in TERMINAL_PRESETS if p["id"] == preset_id), TERMINAL_PRESETS[0])
    theme = theme_override or preset["theme"]
    title = preset["title"]
    distro = preset["distro"]
    uptime = preset["uptime"]
    shell = preset["shell"]
    
    w, h = 680, 360
    builder = SVGBuilder(w, h, theme, title=f"{title} - Terminal Card", desc=f"System stats terminal {preset_id}")
    
    builder.add_custom_css("""
      .term-window { fill: var(--vf-card); stroke: var(--vf-border); stroke-width: 1; }
      .term-header { fill: var(--vf-bg); stroke: var(--vf-border); stroke-width: 0.5; }
      .traffic-red { fill: #EF4444; }
      .traffic-yellow { fill: #F59E0B; }
      .traffic-green { fill: #10B981; }
      .term-title { font-family: var(--vf-font-mono); font-size: 11px; fill: var(--vf-text-muted); }
      .code-line { font-family: var(--vf-font-mono); font-size: 12px; fill: var(--vf-text); }
      .ascii-art { font-family: var(--vf-font-mono); font-size: 13px; font-weight: 700; fill: var(--vf-accent-1); }
      .spec-key { font-family: var(--vf-font-mono); font-size: 12px; font-weight: 700; fill: var(--vf-accent-2); }
      .spec-val { font-family: var(--vf-font-mono); font-size: 12px; fill: var(--vf-text); }
      .accent-dot { fill: var(--vf-accent-1); }
    """)
    
    # Outer terminal window
    builder.add_body(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" class="term-window" />')
    
    # Header bar
    builder.add_body(f'<path d="M 1 9 A 8 8 0 0 1 9 1 L {w-9} 1 A 8 8 0 0 1 {w-1} 9 L {w-1} 34 L 1 34 Z" class="term-header" />')
    builder.add_body(f'<circle cx="20" cy="18" r="4.5" class="traffic-red" />')
    builder.add_body(f'<circle cx="36" cy="18" r="4.5" class="traffic-yellow" />')
    builder.add_body(f'<circle cx="52" cy="18" r="4.5" class="traffic-green" />')
    builder.add_body(f'<text x="{w/2}" y="22" text-anchor="middle" class="term-title">mikeeedev@engine: ~/vectorforge/{preset_id}</text>')
    
    # Top command
    builder.add_body(f'<text x="28" y="60" class="code-line"><tspan fill="var(--vf-accent-1)">❯</tspan> <tspan fill="var(--vf-accent-2)">neofetch</tspan> --target={preset_id} --theme={theme}</text>')
    builder.add_body(f'<line x1="28" y1="72" x2="{w-28}" y2="72" stroke="var(--vf-border)" stroke-width="0.8" />')
    
    # Left: ASCII Art
    art_lines = DISTRO_ASCII.get(distro, DISTRO_ASCII["default"])
    art_svg = []
    for idx, l in enumerate(art_lines):
        art_svg.append(f'<text x="36" y="{110 + idx * 20}" class="ascii-art">{l}</text>')
    builder.add_body(f'<g class="ascii-group">{"".join(art_svg)}</g>')
    
    # Right: Specifications
    specs = [
        ("OS", f"VectorOS / {preset['title'][:20]}"),
        ("Host", "Deterministic MicroVM v2.4"),
        ("Kernel", "6.9.12-kemet-hardened"),
        ("Uptime", uptime),
        ("Shell", shell),
        ("Resolution", f"{w}x{h} (Retina 2x)"),
        ("Terminal", "VectorForge WebTTY"),
        ("Memory", "1,844 MiB / 32,768 MiB"),
    ]
    
    specs_svg = []
    for s_idx, (k, v) in enumerate(specs):
        y_pos = 104 + s_idx * 21
        specs_svg.append(f'<text x="250" y="{y_pos}"><tspan class="spec-key">{k}:</tspan> <tspan class="spec-val">{v}</tspan></text>')
    builder.add_body(f'<g class="specs-group">{"".join(specs_svg)}</g>')
    
    # Memory Progress Bar
    builder.add_body(f"""
    <g transform="translate(250, 276)">
      <text x="0" y="11" font-family="var(--vf-font-mono)" font-size="10" fill="var(--vf-text-muted)">SYSTEM LOAD</text>
      <rect x="80" y="2" width="220" height="10" rx="3" fill="var(--vf-bg)" stroke="var(--vf-border)" />
      <rect x="81" y="3" width="140" height="8" rx="2" fill="var(--vf-accent-1)" />
      <text x="310" y="11" font-family="var(--vf-font-mono)" font-size="10" fill="var(--vf-accent-1)">64%</text>
    </g>
    """)
    
    # Bottom: Color Palette Chips
    palette_chips = []
    for p_i in range(8):
        chip_x = 250 + p_i * 26
        color_var = f"var(--vf-accent-{ (p_i % 3) + 1 })"
        palette_chips.append(f'<rect x="{chip_x}" y="306" width="20" height="12" rx="2" fill="{color_var}" opacity="{(0.4 + (p_i % 4) * 0.2):.2f}" />')
    builder.add_body(f'<g class="palette-chips">{"".join(palette_chips)}</g>')
    
    return builder.build()
