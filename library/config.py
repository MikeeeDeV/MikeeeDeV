"""
library/config.py - VectorForge Declarative Configuration & Parameter Engine.
Supports vectorforge.json / vectorforge.yaml configuration files, parameter placeholders,
and automated batch builds.
"""

import os
import json
import html
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

STARTER_CONFIG = {
    "$schema": "https://mikeeedev.github.io/MikeeeDeV/schema.json",
    "version": "1.0",
    "output_dir": "./assets/generated",
    "shapes": [
        {
            "preset": "kemet-nocturne-rosette",
            "theme": "kemet_nocturne",
            "out": "profile-hero-banner.svg",
            "params": {
                "title": "Senior Systems Engineer",
                "subtitle": "Zero-Crash • High-Throughput • Deterministic"
            }
        },
        {
            "preset": "raft-consensus-cluster",
            "theme": "nord_frost",
            "out": "architecture-topology.svg",
            "params": {
                "title": "Distributed Consensus Pipeline"
            }
        },
        {
            "preset": "docker-healthy-container",
            "theme": "emerald_matrix",
            "out": "system-status-pill.svg"
        }
    ]
}

def apply_parameters(svg: str, params: Dict[str, Any], preset_info: Optional[Dict[str, Any]] = None) -> str:
    """
    Intelligently injects user-defined parameters into generated SVG markup.
    Ensures safe W3C XML escaping, handles {{placeholders}}, and semantically overrides
    preset titles, subtitles, and labels.
    """
    if not params:
        return svg

    preset_title = preset_info.get("title", "") if preset_info else ""

    # 1. Direct template placeholder substitutions: {{key}} and ${key}
    for key, val in params.items():
        escaped_val = html.escape(str(val))
        svg = svg.replace(f"{{{{{key}}}}}", escaped_val)
        svg = svg.replace(f"${{{key}}}", escaped_val)

    # 2. Semantic title override
    if "title" in params:
        user_title = str(params["title"])
        escaped_user_title = html.escape(user_title)
        
        if preset_title:
            # Replace in title tag
            svg = re.sub(
                rf'<title id="title-[^"]*">[^<]*</title>',
                f'<title id="title-id">{escaped_user_title}</title>',
                svg,
                count=1
            )
            # Replace exact title text content
            svg = svg.replace(f">{preset_title}<", f">{escaped_user_title}<")
            svg = svg.replace(f">{preset_title.upper()}<", f">{escaped_user_title.upper()}<")
            svg = svg.replace(html.escape(preset_title), escaped_user_title)

    # 3. Semantic subtitle override
    if "subtitle" in params:
        user_sub = str(params["subtitle"])
        escaped_user_sub = html.escape(user_sub)
        
        # Replace in desc tag
        svg = re.sub(
            rf'<desc id="desc-[^"]*">[^<]*</desc>',
            f'<desc id="desc-id">{escaped_user_sub}</desc>',
            svg,
            count=1
        )
        # Search for secondary/subtitle text tags
        svg = re.sub(
            r'(<text[^>]*class="[^"]*(?:sub|desc|meta|badge)[^"]*"[^>]*>)[^<]*(</text>)',
            rf'\g<1>{escaped_user_sub}\g<2>',
            svg,
            count=1
        )

    # 4. Semantic role override
    if "role" in params:
        escaped_role = html.escape(str(params["role"]))
        svg = re.sub(
            r'(<text[^>]*class="[^"]*(?:role|subtitle)[^"]*"[^>]*>)[^<]*(</text>)',
            rf'\g<1>{escaped_role}\g<2>',
            svg,
            count=1
        )

    return svg

def find_config_file(explicit_path: Optional[str] = None) -> Optional[Path]:
    """Finds vectorforge configuration file in current working directory."""
    if explicit_path:
        p = Path(explicit_path)
        if p.is_file():
            return p
        raise FileNotFoundError(f"Configuration file not found: {explicit_path}")

    candidates = [
        "vectorforge.json",
        ".vectorforgerc.json",
        ".vectorforge.json",
        "vectorforge.yaml",
        "vectorforge.yml"
    ]
    for c in candidates:
        p = Path(c)
        if p.is_file():
            return p
    return None

def load_config(path: Path) -> Dict[str, Any]:
    """Parses JSON or YAML configuration file."""
    content = path.read_text(encoding="utf-8")
    if path.suffix.lower() in [".yaml", ".yml"]:
        if not HAS_YAML:
            raise ImportError("PyYAML is required to parse YAML config files. Install via 'pip install PyYAML'.")
        return yaml.safe_load(content)
    return json.loads(content)

def init_config(target_path: Optional[str] = None) -> Path:
    """Scaffolds a starter vectorforge.json file."""
    out_file = Path(target_path or "vectorforge.json")
    if out_file.exists():
        raise FileExistsError(f"Configuration file already exists: {out_file}")
    
    out_file.write_text(json.dumps(STARTER_CONFIG, indent=2), encoding="utf-8")
    return out_file
