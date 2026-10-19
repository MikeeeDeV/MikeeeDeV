"""
tests/test_cli_config.py - Unit tests for VectorForge config engine and parameter substitution.
"""

import unittest
import tempfile
import json
import shutil
from pathlib import Path
from library.config import apply_parameters, init_config, load_config
from library.cli import main

class TestCliConfig(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_apply_parameters_placeholder(self):
        template = '<svg><text>{{title}}</text><desc>{{subtitle}}</desc></svg>'
        params = {"title": "Mohamed Ayman", "subtitle": "Staff Engineer"}
        result = apply_parameters(template, params)
        self.assertIn("Mohamed Ayman", result)
        self.assertIn("Staff Engineer", result)
        self.assertNotIn("{{title}}", result)

    def test_apply_parameters_xml_escaping(self):
        template = '<svg><text>{{custom}}</text></svg>'
        params = {"custom": "<Dangerous & Unescaped>"}
        result = apply_parameters(template, params)
        self.assertIn("&lt;Dangerous &amp; Unescaped&gt;", result)

    def test_init_and_load_config(self):
        cfg_file = self.test_path / "vectorforge.json"
        init_config(str(cfg_file))
        self.assertTrue(cfg_file.exists())

        loaded = load_config(cfg_file)
        self.assertIn("shapes", loaded)
        self.assertGreater(len(loaded["shapes"]), 0)
        self.assertEqual(loaded["version"], "1.0")

if __name__ == "__main__":
    unittest.main()
