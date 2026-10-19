#!/usr/bin/env python3
"""
tests/test_tokens.py - Verifies design tokens integrity and completeness.
"""

import unittest
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent.parent
TOKENS_PATH = ROOT_DIR / "design" / "tokens.json"


class TestDesignTokens(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TOKENS_PATH.exists(), "tokens.json must exist")
        with open(TOKENS_PATH, "r", encoding="utf-8") as f:
            self.tokens = json.load(f)

    def test_color_schemes(self):
        colors = self.tokens.get("colors", {})
        self.assertIn("dark", colors)
        self.assertIn("light", colors)
        
        required_keys = [
            "bg", "card_bg", "card_elevated", "border", "text_primary",
            "text_secondary", "accent_gold", "accent_lapis", "accent_teal"
        ]
        for k in required_keys:
            self.assertIn(k, colors["dark"])
            self.assertIn(k, colors["light"])

    def test_typography(self):
        typo = self.tokens.get("typography", {})
        self.assertIn("font_mono", typo)
        self.assertIn("font_sans", typo)
        self.assertIn("font_arabic", typo)


if __name__ == "__main__":
    unittest.main()
