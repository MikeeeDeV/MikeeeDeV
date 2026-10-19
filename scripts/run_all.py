#!/usr/bin/env python3
"""
scripts/run_all.py - Master pipeline runner.
Executes all SVG and Markdown generators deterministically and validates outputs.
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from common import ASSETS_DIR
import generate_neofetch
import generate_cipher_banner
import generate_now_building
import generate_contributions
import generate_pins
import generate_hero_typing
import generate_visitor_ledger
import generate_mcp_card
import generate_social_preview
import generate_shipping_log


def validate_svg(path: Path) -> bool:
    """Validates SVG syntax, size < 100KB, and accessibility tags."""
    if not path.exists():
        print(f"[FAIL] Missing {path.name}")
        return False
        
    size_bytes = path.stat().st_size
    if size_bytes > 100 * 1024:
        print(f"[FAIL] {path.name} exceeds 100KB ({size_bytes} bytes)")
        return False
        
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        if not root.tag.endswith("svg"):
            print(f"[FAIL] {path.name} root element is not <svg>")
            return False
            
        # Check accessibility
        has_title = any(child.tag.endswith("title") for child in root)
        if not has_title:
            print(f"[WARN] {path.name} lacks <title>")
            
    except ET.ParseError as e:
        print(f"[FAIL] XML Parse Error in {path.name}: {e}")
        return False
        
    print(f"[PASS] {path.name} ({size_bytes:,} bytes, valid XML)")
    return True


def run_pipeline() -> bool:
    print("=" * 60)
    print("🚀 Running MikeeeDeV Deterministic Profile Generation Pipeline")
    print("=" * 60)
    
    generators = [
        ("Cipher Banner", generate_cipher_banner.main),
        ("Hero Typing Animation", generate_hero_typing.main),
        ("Neofetch Terminal Card", generate_neofetch.main),
        ("Now Building Card", generate_now_building.main),
        ("The Nile Horizon Skyline", generate_contributions.main),
        ("Pinned Repo Cards", generate_pins.main),
        ("Visitor Ledger Terminal", generate_visitor_ledger.main),
        ("Model Context Protocol Card", generate_mcp_card.main),
        ("Social Previews & Headers", generate_social_preview.main),
        ("Shipping Log Injection", generate_shipping_log.main)
    ]
    
    for name, fn in generators:
        print(f"\n▶ Executing: {name}...")
        try:
            fn()
        except Exception as e:
            print(f"[FAIL] Generator {name} crashed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    print("\n" + "=" * 60)
    print("🔍 Validating Generated SVG Artifacts (<100KB, XML, Accessibility)")
    print("=" * 60)
    
    expected_svgs = [
        ASSETS_DIR / "cipher-banner.svg",
        ASSETS_DIR / "hero-typing.svg",
        ASSETS_DIR / "neofetch.svg",
        ASSETS_DIR / "now-building.svg",
        ASSETS_DIR / "contributions.svg",
        ASSETS_DIR / "pins" / "nixmanagerpro.svg",
        ASSETS_DIR / "pins" / "next-session-guard.svg",
        ASSETS_DIR / "pins" / "git-smart-sync.svg",
        ASSETS_DIR / "pins" / "my-portfolio.svg",
        ASSETS_DIR / "visitor-ledger.svg",
        ASSETS_DIR / "mcp-topology.svg"
    ]
    
    all_ok = True
    for svg_p in expected_svgs:
        if not validate_svg(svg_p):
            all_ok = False
            
    if all_ok:
        print("\n✨ All profile generators finished successfully and passed validation!")
    else:
        print("\n❌ One or more artifacts failed validation.")
        
    return all_ok


if __name__ == "__main__":
    success = run_pipeline()
    if not success:
        sys.exit(1)
