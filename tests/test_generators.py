#!/usr/bin/env python3
"""
tests/test_generators.py - Unit tests for generator scripts and configurations.
"""

import unittest
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from generate_now_building import parse_now_config, generate_now_building_svg
from generate_mcp_card import load_mcp_manifest, generate_mcp_card_svg
from generate_cipher_banner import SeededRNG, get_current_sha


class TestGenerators(unittest.TestCase):
    def test_now_building_config(self):
        cfg = parse_now_config()
        self.assertIn("current_focus", cfg)
        self.assertIn("shipping", cfg)
        self.assertIn("project", cfg["shipping"])
        svg = generate_now_building_svg(cfg)
        self.assertTrue(svg.startswith("<svg"))

    def test_mcp_manifest(self):
        manifest = load_mcp_manifest()
        self.assertIn("tools", manifest)
        self.assertGreaterEqual(len(manifest["tools"]), 3)
        tool_names = [t["name"] for t in manifest["tools"]]
        self.assertIn("nix_inspect_channel", tool_names)
        self.assertIn("git_smart_sync_audit", tool_names)
        self.assertIn("session_guard_revoke_device", tool_names)

    def test_seeded_rng_determinism(self):
        rng1 = SeededRNG(0x12345678)
        rng2 = SeededRNG(0x12345678)
        vals1 = [rng1.next() for _ in range(10)]
        vals2 = [rng2.next() for _ in range(10)]
        self.assertEqual(vals1, vals2, "SeededRNG must be bit-for-bit deterministic")


if __name__ == "__main__":
    unittest.main()
