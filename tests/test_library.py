"""
tests/test_library.py - Unit and snapshot tests for the 235+ VectorForge SVG Library.
"""

import os
import glob
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from library.catalog import build_catalog_metadata
from library.engine.color_palettes import PALETTES
from library.generators import CATEGORIES

REPO_ROOT = Path(__file__).resolve().parent.parent

class TestVectorForgeLibrary(unittest.TestCase):
    def test_catalog_exceeds_200_shapes(self):
        catalog = build_catalog_metadata()
        total = catalog["total_shapes"]
        self.assertGreaterEqual(total, 200, f"Expected >= 200 shapes, found {total}")
        self.assertEqual(total, 235)

    def test_all_seven_categories_present(self):
        self.assertEqual(len(CATEGORIES), 7)
        expected_cats = ["banners", "terminals", "skylines", "architectures", "badges", "repo_cards", "holograms"]
        for c in expected_cats:
            self.assertIn(c, CATEGORIES)

    def test_palettes_ten_themes_present(self):
        self.assertEqual(len(PALETTES), 10)
        self.assertIn("kemet_nocturne", PALETTES)
        self.assertIn("cyberpunk_2077", PALETTES)
        self.assertIn("nord_frost", PALETTES)

    def test_all_rendered_svgs_exist_and_valid_xml(self):
        shapes_dir = REPO_ROOT / "library" / "shapes"
        svg_files = list(shapes_dir.glob("**/*.svg"))
        self.assertEqual(len(svg_files), 235, f"Expected 235 rendered SVG files, found {len(svg_files)}")
        
        for svg_path in svg_files:
            # Budget check: < 100KB
            size = svg_path.stat().st_size
            self.assertLess(size, 100 * 1024, f"{svg_path.name} exceeded 100KB: {size} bytes")
            
            # Valid XML check
            try:
                tree = ET.parse(svg_path)
                root = tree.getroot()
                self.assertTrue(root.tag.endswith("svg"), f"{svg_path.name} root tag is not svg: {root.tag}")
            except Exception as e:
                self.fail(f"Failed parsing {svg_path.name}: {e}")

    def test_prefers_color_scheme_in_svgs(self):
        shapes_dir = REPO_ROOT / "library" / "shapes"
        svg_sample = next(shapes_dir.glob("**/*.svg"))
        content = svg_sample.read_text(encoding="utf-8")
        self.assertIn("prefers-color-scheme", content)

if __name__ == "__main__":
    unittest.main()
