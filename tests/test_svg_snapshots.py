#!/usr/bin/env python3
"""
tests/test_svg_snapshots.py - Validates that all generated SVGs conform to:
1. Valid XML syntax.
2. File size strictly under 100KB (Hard Rule 4).
3. Accessibility tags (<title> and <desc> present).
4. Dual mode support (prefers-color-scheme).
5. Zero runtime external scripts/fonts.
"""

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "assets"

REQUIRED_SVGS = [
    ASSETS_DIR / "cipher-banner.svg",
    ASSETS_DIR / "hero-typing.svg",
    ASSETS_DIR / "neofetch.svg",
    ASSETS_DIR / "now-building.svg",
    ASSETS_DIR / "contributions.svg",
    ASSETS_DIR / "visitor-ledger.svg",
    ASSETS_DIR / "mcp-topology.svg",
    ASSETS_DIR / "pins" / "nixmanagerpro.svg",
    ASSETS_DIR / "pins" / "next-session-guard.svg",
    ASSETS_DIR / "pins" / "git-smart-sync.svg",
    ASSETS_DIR / "pins" / "my-portfolio.svg",
]


class TestSVGSnapshots(unittest.TestCase):
    def test_all_svgs_exist(self):
        for svg_path in REQUIRED_SVGS:
            self.assertTrue(svg_path.exists(), f"Missing required SVG: {svg_path.name}")

    def test_svg_file_size_under_100kb(self):
        for svg_path in REQUIRED_SVGS:
            size_bytes = svg_path.stat().st_size
            self.assertLess(
                size_bytes,
                100 * 1024,
                f"{svg_path.name} exceeds 100KB limit: {size_bytes} bytes"
            )

    def test_svg_valid_xml_and_a11y(self):
        for svg_path in REQUIRED_SVGS:
            try:
                tree = ET.parse(svg_path)
                root = tree.getroot()
                self.assertTrue(root.tag.endswith("svg"), f"{svg_path.name} root tag is not svg")
                
                # Check accessibility
                has_title = any(c.tag.endswith("title") for c in root)
                has_desc = any(c.tag.endswith("desc") for c in root)
                self.assertTrue(has_title, f"{svg_path.name} missing <title>")
                self.assertTrue(has_desc, f"{svg_path.name} missing <desc>")
            except ET.ParseError as e:
                self.fail(f"XML parse failure in {svg_path.name}: {e}")

    def test_prefers_color_scheme_present(self):
        for svg_path in REQUIRED_SVGS:
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(
                "prefers-color-scheme",
                content,
                f"{svg_path.name} must contain prefers-color-scheme for light/dark theme adaptation"
            )

    def test_no_external_insecure_resources(self):
        for svg_path in REQUIRED_SVGS:
            with open(svg_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("<script", content.lower(), f"{svg_path.name} contains script tag")
            self.assertNotIn("@import url('http", content.lower(), f"{svg_path.name} imports external font over HTTP")


if __name__ == "__main__":
    unittest.main()
